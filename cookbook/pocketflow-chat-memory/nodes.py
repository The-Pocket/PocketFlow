from pocketflow import Node
from utils.vector_index import create_index, add_vector, search_vectors
from utils.call_llm import call_llm
from utils.get_embedding import get_embedding

class GetUserQuestionNode(Node):
    def prep(self, shared):
        """Initialize messages if first run"""
        if "messages" not in shared:
            shared["messages"] = []
            print("Welcome to the interactive chat! Type 'exit' to end the conversation.")
        
        return None
    
    def exec(self, _):
        """Get user input interactively"""
        # Get interactive input from user
        user_input = input("\nYou: ")
            
        # Check if user wants to exit
        if user_input.lower() == 'exit':
            return None
            
        return user_input
    
    def post(self, shared, prep_res, exec_res):
        # If exec_res is None, the user wants to exit
        if exec_res is None:
            print("\nGoodbye!")
            return None  # End the conversation
            
        # Add user message to current messages
        shared["messages"].append({"role": "user", "content": exec_res})
        
        return "retrieve"

class AnswerNode(Node):
    def prep(self, shared):
        """Prepare context for the LLM"""
        if not shared.get("messages"):
            return None
            
        # 1. Get the last 3 conversation pairs (or fewer if not available)
        recent_messages = shared["messages"][-6:] if len(shared["messages"]) > 6 else shared["messages"]
        
        # 2. Add the retrieved relevant conversation if available
        context = []
        if shared.get("retrieved_conversation"):
            # Add a system message to indicate this is a relevant past conversation
            context.append({
                "role": "system", 
                "content": "The following is a relevant past conversation that may help with the current query:"
            })
            context.extend(shared["retrieved_conversation"])
            context.append({
                "role": "system", 
                "content": "Now continue the current conversation:"
            })
        
        # 3. Add the recent messages
        context.extend(recent_messages)
        
        return context
    
    def exec(self, messages):
        """Generate a response using the LLM"""
        if messages is None:
            return None
        
        # Call LLM with the context
        response = call_llm(messages)
        return response
    
    def post(self, shared, prep_res, exec_res):
        """Process the LLM response"""
        if prep_res is None or exec_res is None:
            return None  # End the conversation
        
        # Print the assistant's response
        print(f"\nAssistant: {exec_res}")
        
        # Add assistant message to history
        shared["messages"].append({"role": "assistant", "content": exec_res})
        
        # If we have more than 6 messages (3 conversation pairs), archive the oldest pair
        if len(shared["messages"]) > 6:
            return "embed"
        
        # We only end if the user explicitly typed 'exit'
        # Even if last_question is set, we continue in interactive mode
        return "question"

class EmbedNode(Node):
    def prep(self, shared):
        """Extract the oldest conversation pair for embedding"""
        if len(shared["messages"]) <= 6:
            return None
            
        # Extract the oldest user-assistant pair
        oldest_pair = shared["messages"][:2]
        # Remove them from current messages
        shared["messages"] = shared["messages"][2:]
        
        return oldest_pair
    
    def exec(self, conversation):
        """Embed a conversation"""
        if not conversation:
            return None
            
        # Combine user and assistant messages into a single text for embedding
        user_msg = next((msg for msg in conversation if msg["role"] == "user"), {"content": ""})
        assistant_msg = next((msg for msg in conversation if msg["role"] == "assistant"), {"content": ""})
        combined = f"User: {user_msg['content']} Assistant: {assistant_msg['content']}"
        
        # Generate embedding
        embedding = get_embedding(combined)
        
        return {
            "conversation": conversation,
            "embedding": embedding
        }
    
    def post(self, shared, prep_res, exec_res):
        """Store the embedding and add to index"""
        if not exec_res:
            # If there's nothing to embed, just continue with the next question
            return "question"
            
        # Initialize vector index if not exist
        if "vector_index" not in shared:
            shared["vector_index"] = create_index()
            shared["vector_items"] = []  # Track items separately
            
        # Add the embedding to the index and store the conversation
        position = add_vector(shared["vector_index"], exec_res["embedding"])
        shared["vector_items"].append(exec_res["conversation"])
        
        print(f"✅ Added conversation to index at position {position}")
        print(f"✅ Index now contains {len(shared['vector_items'])} conversations")
        
        # Continue with the next question
        return "question"

class RetrieveNode(Node):
    def prep(self, shared):
        """Get the current query for retrieval"""
        if not shared.get("messages"):
            return None
            
        # Get the latest user message for searching
        latest_user_msg = next((msg for msg in reversed(shared["messages"]) 
                                if msg["role"] == "user"), {"content": ""})
        
        # Check if we have a vector index with items
        if ("vector_index" not in shared or 
            "vector_items" not in shared or 
            len(shared["vector_items"]) == 0):
            return None
            
        return {
            "query": latest_user_msg["content"],
            "vector_index": shared["vector_index"],
            "vector_items": shared["vector_items"]
        }
    
    def exec(self, inputs):
        """Find the most relevant past conversation"""
        if not inputs:
            return None
            
        query = inputs["query"]
        vector_index = inputs["vector_index"]
        vector_items = inputs["vector_items"]
        
        print(f"🔍 Finding relevant conversation for: {query[:30]}...")
        
        # Create embedding for the query
        query_embedding = get_embedding(query)
        
        # Search for the most similar conversation
        indices, distances = search_vectors(vector_index, query_embedding, k=1)
        
        if not indices:
            return None
            
        # Get the corresponding conversation
        conversation = vector_items[indices[0]]
        
        return {
            "conversation": conversation,
            "distance": distances[0]
        }
    
    def post(self, shared, prep_res, exec_res):
        """Store the retrieved conversation"""
        if exec_res is not None:
            shared["retrieved_conversation"] = exec_res["conversation"]
            print(f"📄 Retrieved conversation (distance: {exec_res['distance']:.4f})")
        else:
            shared["retrieved_conversation"] = None
        
        return "answer"