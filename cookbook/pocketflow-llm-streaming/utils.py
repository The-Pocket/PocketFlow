from openai import OpenAI
import os

def stream_llm(prompt):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))

    # Make a streaming chat completion request
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        stream=True  # Enable streaming
    )
    return response

def fake_stream_llm(prompt, predefined_text="This is a fake response. Today is a sunny day. The sun is shining. The birds are singing. The flowers are blooming. The bees are buzzing. The wind is blowing. The clouds are drifting. The sky is blue. The grass is green. The trees are tall. The water is clear. The fish are swimming. The sun is shining. The birds are singing. The flowers are blooming. The bees are buzzing. The wind is blowing. The clouds are drifting. The sky is blue. The grass is green. The trees are tall. The water is clear. The fish are swimming."):
    """
    Returns a list of simple objects that mimic the structure needed
    for OpenAI streaming responses.
    """
    # Split text into small chunks
    chunk_size = 10
    chunks = []
    
    # Create the chunks using a simple class outside the nested structure
    class SimpleObject:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    # Build the chunks
    for i in range(0, len(predefined_text), chunk_size):
        text_chunk = predefined_text[i:i+chunk_size]
        
        # Create the nested structure using simple objects
        delta = SimpleObject(content=text_chunk)
        choice = SimpleObject(delta=delta)
        chunk = SimpleObject(choices=[choice])
        
        chunks.append(chunk)
    
    return chunks

if __name__ == "__main__":
    print("## Testing streaming LLM")
    prompt = "What's the meaning of life?"
    print(f"## Prompt: {prompt}")
    # response = fake_stream_llm(prompt)
    response = stream_llm(prompt)
    print(f"## Response: ")
    for chunk in response:
        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
            chunk_content = chunk.choices[0].delta.content
            # Print the incoming text without a newline (simulate real-time streaming)
            print(chunk_content, end="", flush=True)

