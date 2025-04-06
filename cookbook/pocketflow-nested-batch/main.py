import os
from flow import create_flow

def create_sample_data():
    """Create sample grade files."""
    # Create directory structure
    os.makedirs("school/class_a", exist_ok=True)
    os.makedirs("school/class_b", exist_ok=True)
    
    # Sample grades
    data = {
        "class_a": {
            "student1.txt": [7.5, 8.0, 9.0],
            "student2.txt": [8.5, 7.0, 9.5]
        },
        "class_b": {
            "student3.txt": [6.5, 8.5, 7.0],
            "student4.txt": [9.0, 9.5, 8.0]
        }
    }
    
    # Create files
    for class_name, students in data.items():
        for student, grades in students.items():
            file_path = os.path.join("school", class_name, student)
            with open(file_path, 'w') as f:
                for grade in grades:
                    f.write(f"{grade}\n")

def main():
    """Run the nested batch example."""
    # Create sample data
    create_sample_data()
    
    print("Processing school grades...\n")
    
    # Create and run flow
    flow = create_flow()
    flow.run({})

if __name__ == "__main__":
    main() 