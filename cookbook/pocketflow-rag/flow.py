from pocketflow import Flow
from nodes import EmbedDocumentsNode, CreateIndexNode, EmbedQueryNode, RetrieveDocumentNode, ChunkDocumentsNode, GenerateAnswerNode

def get_offline_flow():
    # Create offline flow for document indexing
    chunk_docs_node = ChunkDocumentsNode()
    embed_docs_node = EmbedDocumentsNode()
    create_index_node = CreateIndexNode()
    
    # Connect the nodes
    chunk_docs_node >> embed_docs_node >> create_index_node
    
    offline_flow = Flow(start=chunk_docs_node)
    return offline_flow

def get_online_flow():
    # Create online flow for document retrieval and answer generation
    embed_query_node = EmbedQueryNode()
    retrieve_doc_node = RetrieveDocumentNode()
    generate_answer_node = GenerateAnswerNode()
    
    # Connect the nodes
    embed_query_node >> retrieve_doc_node >> generate_answer_node
    
    online_flow = Flow(start=embed_query_node)
    return online_flow

# Initialize flows
offline_flow = get_offline_flow()
online_flow = get_online_flow()