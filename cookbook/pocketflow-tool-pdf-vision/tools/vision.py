from PIL import Image
from utils.call_llm import client
from tools.pdf import image_to_base64

def extract_text_from_image(image: Image.Image, prompt: str = None) -> str:
    """Extract text from image using OpenAI Vision API
    
    Args:
        image (PIL.Image): Image to process
        prompt (str, optional): Custom prompt for extraction. Defaults to general OCR.
        
    Returns:
        str: Extracted text from image
    """
    # Convert image to base64
    img_base64 = image_to_base64(image)
    
    # Default prompt for general OCR
    if prompt is None:
        prompt = "Please extract all text from this image."
    
    # Call Vision API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
            ]
        }]
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    # Test vision processing
    test_image = Image.open("example.png")
    result = extract_text_from_image(test_image)
    print("Extracted text:", result)
