from pocketflow import Flow
from nodes import GetUserQuestionNode, RetrieveNode, AnswerNode, EmbedNode

def create_chat_flow():
    # Create the nodes
    question_node = GetUserQuestionNode()
    retrieve_node = RetrieveNode()
    answer_node = AnswerNode()
    embed_node = EmbedNode()
    
    # Connect the flow:
    # 1. Start with getting a question
    # 2. Retrieve relevant conversations
    # 3. Generate an answer
    # 4. Optionally embed old conversations
    # 5. Loop back to get the next question

    # Main flow path
    question_node - "retrieve" >> retrieve_node
    retrieve_node - "answer" >> answer_node
    
    # When we need to embed old conversations
    answer_node - "embed" >> embed_node
    
    # Loop back for next question
    answer_node - "question" >> question_node
    embed_node - "question" >> question_node
    
    # Create the flow starting with question node
    return Flow(start=question_node)

# Initialize the flow
chat_flow = create_chat_flow() 