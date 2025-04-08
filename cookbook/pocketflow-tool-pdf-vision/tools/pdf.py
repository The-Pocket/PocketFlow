import fitz  # PyMuPDF
from PIL import Image
import io
import base64
from typing import List, Tuple

def pdf_to_images(pdf_path: str, max_size: int = 2000) -> List[Tuple[Image.Image, int]]:
    """Convert PDF pages to PIL Images with size limit
    
    Args:
        pdf_path (str): Path to PDF file
        max_size (int): Maximum dimension (width/height) for images
        
    Returns:
        list: List of tuples (PIL Image, page number)
    """
    doc = fitz.open(pdf_path)
    images = []
    
    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap()
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Resize if needed while maintaining aspect ratio
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            images.append((img, page_num + 1))
            
    finally:
        doc.close()
        
    return images

def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string
    
    Args:
        image (PIL.Image): Image to convert
        
    Returns:
        str: Base64 encoded image string
    """
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
