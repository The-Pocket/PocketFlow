from flow import flow

def main():
    print("\nWelcome to Text Converter!")
    print("=========================")
    
    # Initialize shared store
    shared = {}
    
    # Run the flow
    flow.run(shared)
    
    print("\nThank you for using Text Converter!")

if __name__ == "__main__":
    main() 