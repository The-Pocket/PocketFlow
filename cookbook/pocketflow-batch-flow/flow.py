from pocketflow import Flow, BatchFlow
from nodes import LoadImage, ApplyFilter, SaveImage

def create_base_flow():
    """Create the base Flow for processing a single image."""
    # Create nodes
    load = LoadImage()
    filter_node = ApplyFilter()
    save = SaveImage()
    
    # Connect nodes
    load - "apply_filter" >> filter_node
    filter_node - "save" >> save
    
    # Create and return flow
    return Flow(start=load)

class ImageBatchFlow(BatchFlow):
    """BatchFlow for processing multiple images with different filters."""
    
    def prep(self, shared):
        """Generate parameters for each image-filter combination."""
        # List of images to process
        images = ["cat.jpg", "dog.jpg", "bird.jpg"]
        
        # List of filters to apply
        filters = ["grayscale", "blur", "sepia"]
        
        # Generate all combinations
        params = []
        for img in images:
            for f in filters:
                params.append({
                    "input": img,
                    "filter": f
                })
        
        return params

def create_flow():
    """Create the complete batch processing flow."""
    # Create base flow for single image processing
    base_flow = create_base_flow()
    
    # Wrap in BatchFlow for multiple images
    batch_flow = ImageBatchFlow(start=base_flow)
    
    return batch_flow 