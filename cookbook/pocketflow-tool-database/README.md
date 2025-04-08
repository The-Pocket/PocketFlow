# SQLite Database with PocketFlow

This example demonstrates how to properly integrate SQLite database operations with PocketFlow, focusing on:

1. Clean code organization with separation of concerns:
   - Tools layer for database operations (`tools/database.py`)
   - Node implementation for PocketFlow integration (`nodes.py`)
   - Flow configuration (`flow.py`)
   - Safe SQL query execution with parameter binding

2. Best practices for database operations:
   - Connection management with proper closing
   - SQL injection prevention using parameterized queries
   - Error handling and resource cleanup
   - Simple schema management

3. Example task management system:
   - Database initialization
   - Task creation
   - Task listing
   - Status tracking

## Project Structure

```
pocketflow-tool-database/
├── tools/
│   └── database.py    # SQLite database operations
├── nodes.py          # PocketFlow node implementation
├── flow.py          # Flow configuration
└── main.py          # Example usage
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the example:
```bash
python main.py
```

This will:
1. Initialize a SQLite database with a tasks table
2. Create an example task
3. List all tasks in the database
4. Display the results

## Key Concepts Demonstrated

1. **Database Operations**
   - Safe connection handling
   - Query parameterization
   - Schema management

2. **Code Organization**
   - Clear separation between database operations and PocketFlow components
   - Modular project structure
   - Type hints and documentation

3. **PocketFlow Integration**
   - Node implementation with prep->exec->post lifecycle
   - Flow configuration
   - Shared store usage for data passing

## Example Output

```
Database Status: Database initialized
Task Status: Task created successfully

All Tasks:
- ID: 1
  Title: Example Task
  Description: This is an example task created using PocketFlow
  Status: pending
  Created: 2024-03-02 12:34:56
```
