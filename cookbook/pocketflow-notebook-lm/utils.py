import os

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

def text_to_speech(text, voice="alloy"):
    """Convert text to speech. OpenAI TTS or Gemini TTS based on available key."""
    if os.environ.get("OPENAI_API_KEY"):
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        return response.content  # returns bytes
    elif os.environ.get("GEMINI_API_KEY"):
        import base64
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        # Map OpenAI voices to Gemini voices
        voice_map = {"alloy": "Kore", "echo": "Puck", "nova": "Aoede", "shimmer": "Leda"}
        gemini_voice = voice_map.get(voice, "Kore")
        resp = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=gemini_voice)
                    )
                ),
            ),
        )
        data = resp.candidates[0].content.parts[0].inline_data.data
        if isinstance(data, bytes):
            return data
        return base64.b64decode(data + "=" * (-len(data) % 4))  # fix padding
    else:
        raise ValueError("Set OPENAI_API_KEY or GEMINI_API_KEY")


DOCS = [
    "PocketFlow is a 100-line minimalist LLM framework. Zero dependencies, zero vendor lock-in. "
    "The core abstraction is a nested directed graph that lets you compose complex AI workflows from simple building blocks.",
    "Nodes have three phases: prep reads from shared store, exec does the work, post writes results back. "
    "This clean separation makes each node easy to test, debug, and reuse across different flows.",
    "A Flow connects nodes with >> for chaining and action strings for branching. "
    "You can nest flows inside flows, giving you infinite composability without complexity.",
    "The key design patterns: Workflow for linear pipelines, Agent for autonomous loops, "
    "RAG for retrieval-augmented generation, Map-Reduce for parallel processing, and Reflection for self-improving outputs.",
]


if __name__ == "__main__":
    print("## Testing call_llm")
    prompt = "In a few words, what is the meaning of life?"
    print(f"## Prompt: {prompt}")
    response = call_llm(prompt)
    print(f"## Response: {response}")

    print("\n## Testing text_to_speech")
    audio = text_to_speech("Hello, this is a test of the text to speech API.")
    print(f"## Audio bytes received: {len(audio)}")
