import os
import base64

def call_llm(prompt):
    """Call LLM — auto-detects OpenAI or Gemini based on available API key."""
    if os.environ.get("OPENAI_API_KEY"):
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        r = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content
    elif os.environ.get("GEMINI_API_KEY"):
        from google import genai
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        r = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return r.text
    else:
        raise ValueError("Set OPENAI_API_KEY or GEMINI_API_KEY")

def call_llm_with_image(prompt, image_base64):
    """Call LLM with vision — auto-detects OpenAI or Gemini."""
    if os.environ.get("OPENAI_API_KEY"):
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        r = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
            ]}]
        )
        return r.choices[0].message.content
    elif os.environ.get("GEMINI_API_KEY"):
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        image_bytes = base64.b64decode(image_base64)
        r = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                prompt,
            ],
        )
        return r.text
    else:
        raise ValueError("Set OPENAI_API_KEY or GEMINI_API_KEY")

# Example usage
if __name__ == "__main__":
    print(call_llm("Tell me a short joke"))
