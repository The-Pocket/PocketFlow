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

# Document store — summaries about PocketFlow concepts
DOCS = {
    "overview": "PocketFlow is a 100-line LLM framework. Core abstraction: Graph with Nodes and Flows. Zero dependencies.",
    "nodes": "Nodes have prep/exec/post. prep reads shared store, exec does work (LLM calls), post writes back. Only exec retries on failure. BatchNode handles lists.",
    "flows": "Flows connect nodes: >> chains, action strings branch, self-loops loop. Flow is also a Node, so flows nest inside flows.",
    "rag": "RAG = Retrieval Augmented Generation. Offline: chunk, embed, store. Online: embed query, retrieve top-K, generate answer with context.",
    "agents": "An agent is an LLM + tools + loop. DecideNode picks an action, tool nodes execute, loop back. ReAct pattern: Reason, Act, Observe, Repeat.",
}

if __name__ == "__main__":
    print("=== Testing call_llm ===")
    prompt = "In a few words, what is the meaning of life?"
    print(f"Prompt: {prompt}")
    response = call_llm(prompt)
    print(f"Response: {response}")

    print("\n=== Testing DOCS store ===")
    for name, summary in DOCS.items():
        print(f"  [{name}]: {summary[:60]}...")
