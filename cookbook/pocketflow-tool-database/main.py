from flow import create_database_flow

def main():
    # Create the flow
    flow = create_database_flow()
    
    # Prepare example task data
    shared = {
        "task_title": "Example Task",
        "task_description": "This is an example task created using PocketFlow"
    }
    
    # Run the flow
    flow.run(shared)
    
    # Print results
    print("Database Status:", shared.get("db_status"))
    print("Task Status:", shared.get("task_status"))
    print("\nAll Tasks:")
    for task in shared.get("tasks", []):
        print(f"- ID: {task[0]}")
        print(f"  Title: {task[1]}")
        print(f"  Description: {task[2]}")
        print(f"  Status: {task[3]}")
        print(f"  Created: {task[4]}")
        print()

if __name__ == "__main__":
    main()
