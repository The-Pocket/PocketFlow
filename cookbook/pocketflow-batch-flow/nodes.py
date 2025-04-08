"""Node implementations for image processing."""

import os
from PIL import Image, ImageEnhance, ImageFilter
from pocketflow import Node

class LoadImage(Node):
    """Node that loads an image file."""
    
    def prep(self, shared):
        """Get image path from parameters."""
        return os.path.join("images", self.params["input"])
    
    def exec(self, image_path):
        """Load the image using PIL."""
        return Image.open(image_path)
    
    def post(self, shared, prep_res, exec_res):
        """Store the image in shared store."""
        shared["image"] = exec_res
        return "apply_filter"

class ApplyFilter(Node):
    """Node that applies a filter to an image."""
    
    def prep(self, shared):
        """Get image and filter type."""
        return shared["image"], self.params["filter"]
    
    def exec(self, inputs):
        """Apply the specified filter."""
        image, filter_type = inputs
        
        if filter_type == "grayscale":
            return image.convert("L")
        elif filter_type == "blur":
            return image.filter(ImageFilter.BLUR)
        elif filter_type == "sepia":
            # Sepia implementation
            enhancer = ImageEnhance.Color(image)
            grayscale = enhancer.enhance(0.3)
            colorize = ImageEnhance.Brightness(grayscale)
            return colorize.enhance(1.2)
        else:
            raise ValueError(f"Unknown filter: {filter_type}")
    
    def post(self, shared, prep_res, exec_res):
        """Store the filtered image."""
        shared["filtered_image"] = exec_res
        return "save"

class SaveImage(Node):
    """Node that saves the processed image."""
    
    def prep(self, shared):
        """Get filtered image and prepare output path."""
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Generate output filename
        input_name = os.path.splitext(self.params["input"])[0]
        filter_name = self.params["filter"]
        output_path = os.path.join("output", f"{input_name}_{filter_name}.jpg")
        
        return shared["filtered_image"], output_path
    
    def exec(self, inputs):
        """Save the image to file."""
        image, output_path = inputs
        image.save(output_path, "JPEG")
        return output_path
    
    def post(self, shared, prep_res, exec_res):
        """Print success message."""
        print(f"Saved filtered image to: {exec_res}")
        return "default" 