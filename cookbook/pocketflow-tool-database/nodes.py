from pocketflow import Node
from tools.database import execute_sql, init_db

class InitDatabaseNode(Node):
    """Node for initializing the database"""
    
    def exec(self, _):
        init_db()
        return "Database initialized"
        
    def post(self, shared, prep_res, exec_res):
        shared["db_status"] = exec_res
        return "default"

class CreateTaskNode(Node):
    """Node for creating a new task"""
    
    def prep(self, shared):
        return (
            shared.get("task_title", ""),
            shared.get("task_description", "")
        )
        
    def exec(self, inputs):
        title, description = inputs
        query = "INSERT INTO tasks (title, description) VALUES (?, ?)"
        execute_sql(query, (title, description))
        return "Task created successfully"
        
    def post(self, shared, prep_res, exec_res):
        shared["task_status"] = exec_res
        return "default"

class ListTasksNode(Node):
    """Node for listing all tasks"""
    
    def exec(self, _):
        query = "SELECT * FROM tasks"
        return execute_sql(query)
        
    def post(self, shared, prep_res, exec_res):
        shared["tasks"] = exec_res
        return "default"
