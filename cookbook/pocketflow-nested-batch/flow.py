import os
from pocketflow import Flow, BatchFlow
from nodes import LoadGrades, CalculateAverage

def create_base_flow():
    """Create base flow for processing one student's grades."""
    # Create nodes
    load = LoadGrades()
    calc = CalculateAverage()
    
    # Connect nodes
    load - "calculate" >> calc
    
    # Create and return flow
    return Flow(start=load)

class ClassBatchFlow(BatchFlow):
    """BatchFlow for processing all students in a class."""
    
    def prep(self, shared):
        """Generate parameters for each student in the class."""
        # Get class folder from parameters
        class_folder = self.params["class"]
        
        # List all student files
        class_path = os.path.join("school", class_folder)
        students = [f for f in os.listdir(class_path) if f.endswith(".txt")]
        
        # Return parameters for each student
        return [{"student": student} for student in students]
    
    def post(self, shared, prep_res, exec_res):
        """Calculate and print class average."""
        class_name = self.params["class"]
        class_results = shared["results"][class_name]
        class_average = sum(class_results.values()) / len(class_results)
        
        print(f"Class {class_name.split('_')[1].upper()} Average: {class_average:.2f}\n")
        return "default"

class SchoolBatchFlow(BatchFlow):
    """BatchFlow for processing all classes in the school."""
    
    def prep(self, shared):
        """Generate parameters for each class."""
        # List all class folders
        classes = [d for d in os.listdir("school") if os.path.isdir(os.path.join("school", d))]
        
        # Return parameters for each class
        return [{"class": class_name} for class_name in classes]
    
    def post(self, shared, prep_res, exec_res):
        """Calculate and print school average."""
        all_grades = []
        for class_results in shared["results"].values():
            all_grades.extend(class_results.values())
            
        school_average = sum(all_grades) / len(all_grades)
        print(f"School Average: {school_average:.2f}")
        return "default"

def create_flow():
    """Create the complete nested batch processing flow."""
    # Create base flow for single student
    base_flow = create_base_flow()
    
    # Wrap in ClassBatchFlow for processing all students in a class
    class_flow = ClassBatchFlow(start=base_flow)
    
    # Wrap in SchoolBatchFlow for processing all classes
    school_flow = SchoolBatchFlow(start=class_flow)
    
    return school_flow 