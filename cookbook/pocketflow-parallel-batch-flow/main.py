import os
import asyncio
import time
from flow import create_flows

def get_image_paths():
    """Get paths of existing images in the images directory."""
    images_dir = "images"
    if not os.path.exists(images_dir):
        raise ValueError(f"Directory '{images_dir}' not found!")
    
    # List all jpg files in the images directory
    image_paths = []
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_paths.append(os.path.join(images_dir, filename))
    
    if not image_paths:
        raise ValueError(f"No images found in '{images_dir}' directory!")
    
    print(f"Found {len(image_paths)} images:")
    for path in image_paths:
        print(f"- {path}")
    
    return image_paths

async def main():
    """Run the parallel image processing example."""
    print("Parallel Image Processor")
    print("-" * 30)
    
    # Get existing image paths
    image_paths = get_image_paths()
    
    # Create shared store with image paths
    shared = {"images": image_paths}
    
    # Create both flows
    batch_flow, parallel_batch_flow = create_flows()
    
    # Run and time batch flow
    start_time = time.time()
    print("\nRunning sequential batch flow...")
    await batch_flow.run_async(shared)
    batch_time = time.time() - start_time
    
    # Run and time parallel batch flow
    start_time = time.time()
    print("\nRunning parallel batch flow...")
    await parallel_batch_flow.run_async(shared)
    parallel_time = time.time() - start_time
    
    # Print timing results
    print("\nTiming Results:")
    print(f"Sequential batch processing: {batch_time:.2f} seconds")
    print(f"Parallel batch processing: {parallel_time:.2f} seconds")
    print(f"Speedup: {batch_time/parallel_time:.2f}x")
    
    print("\nProcessing complete! Check the output/ directory for results.")

if __name__ == "__main__":
    asyncio.run(main()) 