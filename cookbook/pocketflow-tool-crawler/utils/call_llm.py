from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt: str) -> str:
    """Call OpenAI API to analyze text
    
    Args:
        prompt (str): Input prompt for the model
        
    Returns:
        str: Model response
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error calling LLM API: {str(e)}")
        return ""

if __name__ == "__main__":
    # Test LLM call
    response = call_llm("What is web crawling?")
    print("Response:", response)
