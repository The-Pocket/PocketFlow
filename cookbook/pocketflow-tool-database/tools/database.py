import sqlite3
from typing import List, Tuple, Any

def execute_sql(query: str, params: Tuple = None) -> List[Tuple[Any, ...]]:
    """Execute a SQL query and return results
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters to prevent SQL injection
        
    Returns:
        list: Query results as a list of tuples
    """
    conn = sqlite3.connect("example.db")
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        return result
    finally:
        conn.close()

def init_db():
    """Initialize database with example table"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    execute_sql(create_table_sql)
