import faiss
import numpy as np

from pocketflow import BatchNode, Node
from utils import call_llm, fixed_size_chunk, get_embedding


# Nodes for the offline flow
class ChunkDocumentsNode(BatchNode):
    def prep(self, shared):
        """Read texts from shared store"""
        return shared["texts"]
    
    def exec(self, prep_res):
        """Chunk a single text into smaller pieces"""
        return fixed_size_chunk(prep_res)
    
    def post(self, shared, prep_res, exec_res):
        """Store chunked texts in the shared store"""
        # Flatten the list of lists into a single list of chunks
        all_chunks = []
        for chunks in exec_res:
            all_chunks.extend(chunks)
        
        # Replace the original texts with the flat list of chunks
        shared["texts"] = all_chunks
        
        print(f"✅ Created {len(all_chunks)} chunks from {len(prep_res)} documents")
        return "default"
    
class EmbedDocumentsNode(BatchNode):
    def prep(self, shared):
        """Read texts from shared store and return as an iterable"""
        return shared["texts"]
    
    def exec(self, prep_res):
        """Embed a single text"""
        return get_embedding(prep_res)
    
    def post(self, shared, prep_res, exec_res):
        """Store embeddings in the shared store"""
        embeddings = np.array(exec_res, dtype=np.float32)
        shared["embeddings"] = embeddings
        print(f"✅ Created {len(embeddings)} document embeddings")
        return "default"

class CreateIndexNode(Node):
    def prep(self, shared):
        """Get embeddings from shared store"""
        return shared["embeddings"]
    
    def exec(self, prep_res):
        """Create FAISS index and add embeddings"""
        print("🔍 Creating search index...")
        dimension = prep_res.shape[1]
        
        # Create a flat L2 index
        index = faiss.IndexFlatL2(dimension)
        
        # Add the embeddings to the index
        index.add(prep_res)
        
        return index
    
    def post(self, shared, prep_res, exec_res):
        """Store the index in shared store"""
        shared["index"] = exec_res
        print(f"✅ Index created with {exec_res.ntotal} vectors")
        return "default"

# Nodes for the online flow
class EmbedQueryNode(Node):
    def prep(self, shared):
        """Get query from shared store"""
        return shared["query"]
    
    def exec(self, prep_res):
        """Embed the query"""
        print(f"🔍 Embedding query: {prep_res}")
        query_embedding = get_embedding(prep_res)
        return np.array([query_embedding], dtype=np.float32)
    
    def post(self, shared, prep_res, exec_res):
        """Store query embedding in shared store"""
        shared["query_embedding"] = exec_res
        return "default"

class RetrieveDocumentNode(Node):
    def prep(self, shared):
        """Get query embedding, index, and texts from shared store"""
        return shared["query_embedding"], shared["index"], shared["texts"]
    
    def exec(self, prep_res):
        """Search the index for similar documents"""
        print("🔎 Searching for relevant documents...")
        query_embedding, index, texts = prep_res
        
        # Search for the most similar document
        distances, indices = index.search(query_embedding, k=1)
        
        # Get the index of the most similar document
        best_idx = indices[0][0]
        distance = distances[0][0]
        
        # Get the corresponding text
        most_relevant_text = texts[best_idx]
        
        return {
            "text": most_relevant_text,
            "index": best_idx,
            "distance": distance
        }
    
    def post(self, shared, prep_res, exec_res):
        """Store retrieved document in shared store"""
        shared["retrieved_document"] = exec_res
        print(f"📄 Retrieved document (index: {exec_res['index']}, distance: {exec_res['distance']:.4f})")
        print(f"📄 Most relevant text: \"{exec_res['text']}\"")
        return "default"
    
class GenerateAnswerNode(Node):
    def prep(self, shared):
        """Get query, retrieved document, and any other context needed"""
        return shared["query"], shared["retrieved_document"]
    
    def exec(self, prep_res):
        """Generate an answer using the LLM"""
        query, retrieved_doc = prep_res
        
        prompt = f"""
Briefly answer the following question based on the context provided:
Question: {query}
Context: {retrieved_doc['text']}
Answer:
"""
        
        answer = call_llm(prompt)
        return answer
    
    def post(self, shared, prep_res, exec_res):
        """Store generated answer in shared store"""
        shared["generated_answer"] = exec_res
        print("\n🤖 Generated Answer:")
        print(exec_res)
        return "default"
