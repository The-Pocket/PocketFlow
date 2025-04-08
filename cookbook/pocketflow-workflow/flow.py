from pocketflow import Flow
from nodes import GenerateOutline, WriteSimpleContent, ApplyStyle

def create_article_flow():
    """
    Create and configure the article writing workflow
    """
    # Create node instances
    outline_node = GenerateOutline()
    write_node = WriteSimpleContent()
    style_node = ApplyStyle()
    
    # Connect nodes in sequence
    outline_node >> write_node >> style_node
    
    # Create flow starting with outline node
    article_flow = Flow(start=outline_node)
    
    return article_flow