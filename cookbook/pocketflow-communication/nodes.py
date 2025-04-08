"""Node implementations for the communication example."""

from pocketflow import Node

class EndNode(Node):
    """Node that handles flow termination."""
    pass

class TextInput(Node):
    """Node that reads text input and initializes the shared store."""
    
    def prep(self, shared):
        """Get user input and ensure shared store is initialized."""
        return input("Enter text (or 'q' to quit): ")
    
    def post(self, shared, prep_res, exec_res):
        """Store text and initialize/update statistics."""
        if prep_res == 'q':
            return "exit"
        
        # Store the text
        shared["text"] = prep_res
        
        # Initialize statistics if they don't exist
        if "stats" not in shared:
            shared["stats"] = {
                "total_texts": 0,
                "total_words": 0
            }
        shared["stats"]["total_texts"] += 1
        
        return "count"

class WordCounter(Node):
    """Node that counts words in the text."""
    
    def prep(self, shared):
        """Get text from shared store."""
        return shared["text"]
    
    def exec(self, text):
        """Count words in the text."""
        return len(text.split())
    
    def post(self, shared, prep_res, exec_res):
        """Update word count statistics."""
        shared["stats"]["total_words"] += exec_res
        return "show"

class ShowStats(Node):
    """Node that displays statistics from the shared store."""
    
    def prep(self, shared):
        """Get statistics from shared store."""
        return shared["stats"]
    
    def post(self, shared, prep_res, exec_res):
        """Display statistics and continue the flow."""
        stats = prep_res
        print(f"\nStatistics:")
        print(f"- Texts processed: {stats['total_texts']}")
        print(f"- Total words: {stats['total_words']}")
        print(f"- Average words per text: {stats['total_words'] / stats['total_texts']:.1f}\n")
        return "continue" 