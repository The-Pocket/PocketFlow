import os
import numpy as np
from openai import OpenAI

def get_embedding(text):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY"))
    
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    
    # Extract the embedding vector from the response
    embedding = response.data[0].embedding
    
    # Convert to numpy array for consistency with other embedding functions
    return np.array(embedding, dtype=np.float32)


if __name__ == "__main__":
    # Test the embedding function
    text1 = "The quick brown fox jumps over the lazy dog."
    text2 = "Python is a popular programming language for data science."
    
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    
    print(f"Embedding 1 shape: {emb1.shape}")
    print(f"Embedding 2 shape: {emb2.shape}")
    
    # Calculate similarity (dot product)
    similarity = np.dot(emb1, emb2)
    print(f"Similarity between texts: {similarity:.4f}") 