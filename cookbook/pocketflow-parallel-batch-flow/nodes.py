"""AsyncNode implementations for image processing."""
import os
import asyncio
from PIL import Image, ImageFilter
import numpy as np
from pocketflow import AsyncNode

class LoadImage(AsyncNode):
    """Node that loads an image from file."""
    async def prep_async(self, shared):
        """Get image path from parameters."""
        image_path = self.params["image_path"]
        print(f"Loading image: {image_path}")
        return image_path
    
    async def exec_async(self, image_path):
        """Load image using PIL."""
        # Simulate I/O delay
        await asyncio.sleep(0.5)
        return Image.open(image_path)
    
    async def post_async(self, shared, prep_res, exec_res):
        """Store image in shared store."""
        shared["image"] = exec_res
        return "apply_filter"

class ApplyFilter(AsyncNode):
    """Node that applies a filter to an image."""
    async def prep_async(self, shared):
        """Get image and filter type."""
        image = shared["image"]
        filter_type = self.params["filter"]
        print(f"Applying {filter_type} filter...")
        return image, filter_type
    
    async def exec_async(self, inputs):
        """Apply the specified filter."""
        image, filter_type = inputs
        
        # Simulate processing delay
        await asyncio.sleep(0.5)
        
        if filter_type == "grayscale":
            return image.convert("L")
        elif filter_type == "blur":
            return image.filter(ImageFilter.BLUR)
        elif filter_type == "sepia":
            # Convert to array for sepia calculation
            img_array = np.array(image)
            sepia_matrix = np.array([
                [0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]
            ])
            sepia_array = img_array.dot(sepia_matrix.T)
            sepia_array = np.clip(sepia_array, 0, 255).astype(np.uint8)
            return Image.fromarray(sepia_array)
        else:
            raise ValueError(f"Unknown filter: {filter_type}")
    
    async def post_async(self, shared, prep_res, exec_res):
        """Store filtered image."""
        shared["filtered_image"] = exec_res
        return "save"

class SaveImage(AsyncNode):
    """Node that saves the processed image."""
    async def prep_async(self, shared):
        """Prepare output path."""
        image = shared["filtered_image"]
        base_name = os.path.splitext(os.path.basename(self.params["image_path"]))[0]
        filter_type = self.params["filter"]
        output_path = f"output/{base_name}_{filter_type}.jpg"
        
        # Create output directory if needed
        os.makedirs("output", exist_ok=True)
        
        return image, output_path
    
    async def exec_async(self, inputs):
        """Save the image."""
        image, output_path = inputs
        
        # Simulate I/O delay
        await asyncio.sleep(0.5)
        
        image.save(output_path)
        return output_path
    
    async def post_async(self, shared, prep_res, exec_res):
        """Print success message."""
        print(f"Saved: {exec_res}")
        return "default" 