from pocketflow import Flow
from nodes import InitDatabaseNode, CreateTaskNode, ListTasksNode

def create_database_flow():
    """Create a flow for database operations"""
    
    # Create nodes
    init_db = InitDatabaseNode()
    create_task = CreateTaskNode()
    list_tasks = ListTasksNode()
    
    # Connect nodes
    init_db >> create_task >> list_tasks
    
    # Create and return flow
    return Flow(start=init_db)
