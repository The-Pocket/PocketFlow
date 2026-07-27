from openai import OpenAI
import os

def call_llm(prompt):    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))
    r = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def get_embeddings(text_list : list) -> list:    
#     # DUMMY EMBEDDING API
#     return

# VIBE CODING WARNING:
# This is a minimal prototype for controlled/educational use.
# It is NOT a complete security boundary. Do not run untrusted code in production.
# Reference Article : https://www.anthropic.com/engineering/advanced-tool-use
# Reference Notebook : https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_search_with_embeddings.ipynb

import yaml
import numpy as np

# Define our tool library with 2 domains
TOOL_LIBRARY = [
    # Weather Tools
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The unit of temperature",
                },
            },
            "required": ["location"],
        },
    },
    {
        "name": "get_forecast",
        "description": "Get the weather forecast for multiple days ahead",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state",
                },
                "days": {
                    "type": "number",
                    "description": "Number of days to forecast (1-10)",
                },
            },
            "required": ["location", "days"],
        },
    },
    {
        "name": "get_timezone",
        "description": "Get the current timezone and time for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or timezone identifier",
                }
            },
            "required": ["location"],
        },
    },
    {
        "name": "get_air_quality",
        "description": "Get current air quality index and pollutant levels for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or coordinates",
                }
            },
            "required": ["location"],
        },
    },
    # Finance Tools
    {
        "name": "get_stock_price",
        "description": "Get the stock price for a given ticker symbol at a specified timestamp (UTC+8) .",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., AAPL, GOOGL)",
                },
                "timestamp": {
                    "type": "string",
                    "description": "to locate the ticket price with exact timestamp from NASDAQ database",
                },
            },
            "required": ["ticker", "timestamp"],
        },
    },
    {
        "name": "convert_currency",
        "description": "Convert an amount from one currency to another using current exchange rates",
        "input_schema": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "Amount to convert",
                },
                "from_currency": {
                    "type": "string",
                    "description": "Source currency code (e.g., USD)",
                },
                "to_currency": {
                    "type": "string",
                    "description": "Target currency code (e.g., EUR)",
                },
            },
            "required": ["amount", "from_currency", "to_currency"],
        },
    },
    {
        "name": "calculate_compound_interest",
        "description": "Calculate compound interest for investments over time",
        "input_schema": {
            "type": "object",
            "properties": {
                "principal": {
                    "type": "number",
                    "description": "Initial investment amount",
                },
                "rate": {
                    "type": "number",
                    "description": "Annual interest rate (as percentage)",
                },
                "years": {"type": "number", "description": "Number of years"},
                "frequency": {
                    "type": "string",
                    "enum": ["daily", "monthly", "quarterly", "annually"],
                    "description": "Compounding frequency",
                },
            },
            "required": ["principal", "rate", "years"],
        },
    },
    {
        "name": "get_market_news",
        "description": "Get recent financial news and market updates for a specific company or sector",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Company name, ticker symbol, or sector",
                },
                "limit": {
                    "type": "number",
                    "description": "Maximum number of news articles to return",
                },
            },
            "required": ["query"],
        },
    },
]


# Line #71 of Notebook
def tool_to_text(tool) -> str:
    """
    Convert a tool definition into a text representation for embedding.
    Combines the tool name, description, and parameter information.
    """
    text_parts = [
        f"Tool: {tool['name']}",
        f"Description: {tool['description']}",
    ]

    # Add parameter information
    if "input_schema" in tool and "properties" in tool["input_schema"]:
        params = tool["input_schema"]["properties"]
        param_descriptions = []
        for param_name, param_info in params.items():
            param_desc = param_info.get("description", "")
            param_type = param_info.get("type", "")
            param_descriptions.append(f"{param_name} ({param_type}): {param_desc}")

        if param_descriptions:
            text_parts.append("Parameters: " + ", ".join(param_descriptions))

    return "\n".join(text_parts)


def create_all_tools_embedding():
    """
    Create tools text embedding in TOOL_LIBRARY

    Args: 
        None

    Returns:
        List of tool embedding numpy array
    """
    # Create embeddings for all tools
    print("Creating embeddings for all tools...")

    tool_texts = [tool_to_text(tool) for tool in TOOL_LIBRARY]

    # ⚠️⚠️ API NOTICE
    # Please adapt to your embedding APIs
    tool_embeddings = []
    temp_obj = get_embeddings(tool_texts)
    for item in temp_obj.data:
        t_array = np.array(item.embedding)
        tool_embeddings.append(t_array)

    print(f"✅ Defined {len(TOOL_LIBRARY)} tools in the library")

    return tool_embeddings



# Refer from 
# Line #73 of : https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_search_with_embeddings.ipynb
def search_tools(query: str, top_k: int = 5, tool_embeddings:list=[]) -> list[dict]:
    """
    Search for tools using semantic similarity.

    Args:
        query: Natural language description of what tool is needed
        top_k: Number of top tools to return

    Returns:
        List of tool definitions most relevant to the query
    """
    
    # ⚠️⚠️ API NOTICE
    # Please adapt to your embedding APIs
    query_embedding = get_embeddings(query)

    q_array = np.array(query_embedding.data[0].embedding)
    similarities = []
    for index, value in enumerate(tool_embeddings):
        tmp = np.dot(value, q_array)
        similarities.append(tmp)
        
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    results = []
    for idx in top_indices:
        results.append({"tool": TOOL_LIBRARY[idx], "similarity_score": float(similarities[idx])})

    return results



# The tool_search tool definition
TOOL_SEARCH_DEFINITION = {
    "name": "tool_search",
    "description": "Search for available tools that can help with a task. Returns tool definitions for matching tools. Use this when you need a tool but don't have it available yet.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language description of what kind of tool you need (e.g., 'weather information', 'currency conversion', 'stock prices')",
            },
            "top_k": {
                "type": "number",
                "description": "Number of tools to return (default: 5)",
            },
        },
        "required": ["query"],
    },
}

def handle_tool_exec(tool_name:str, tool_params:dict):
    if tool_name == "get_weather" :
        return "NYC : sunny"
    elif tool_name == "get_forecast" :
        return "NYC : tommorrow : sunny"
    else :
        return "tool executed"

# in Line #75 of https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_search_with_embeddings.ipynb
# there is no input schema for tool search, adding it for my local experiment
def handle_tool_search(query: str, top_k: int = 5, tool_embeddings:list=[]) -> list[dict[str, any]]:
    """
    Handle a tool_search invocation and return tool references.

    Returns a list of tool_reference content blocks for discovered tools.
    """
    # Search for relevant tools
    results = search_tools(query, top_k, tool_embeddings)

    # Create tool_reference objects instead of full definitions
    tool_references = [
        {"type": "tool_reference", "tool_name": result["tool"]["name"], "similarity_score":f"{result['similarity_score']:.3f}","input_schema": result["tool"]["input_schema"]} for result in results
    ]

    # the print is only for debug , not changing tool_references contents
    print(f"\n🔍 Tool search: '{query}'")
    print(f"   Found {len(tool_references)} tools:")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['tool']['name']} (similarity: {result['similarity_score']:.3f})")

    return tool_references


import time, tempfile, os, textwrap, sys, subprocess

def run_user_code(
    code: str,
    input_data: str = "",
):
    """
    Execute user Python code in a restricted subprocess.
    Captures stdout/stderr and enforces time/memory limits.

    Returns:
        dict: {
            stdout (str),
            stderr (str),
            returncode (int)
        }
    """
    start = time.time()
    with tempfile.TemporaryDirectory() as tmpdir:
        user_code_path = os.path.join(tmpdir, "user_code.py")

        body = textwrap.dedent(code).strip("\n")
        body = textwrap.indent(code, "    ")

        # assemble tool code code 
        tmp_code = f"""

def get_stock_price(ticker, timestamp):
    if ticker == "NVDA":
        return ticker + ": 888.88"
    elif ticker == "MSFT":
        return ticker + ": 666.66"
    elif ticker == "QCOM":
        return ticker + ": 444.44"
    else:
        return "Wrong Ticket or Timestamp"

def __entry__():
{body}

if __name__ == "__main__":
    __entry__()

        """

        print(tmp_code)

        # Write user code to a temp file
        with open(user_code_path, "w", encoding="utf-8") as f:
            f.write(tmp_code)

        # Run Python in a more isolated mode:
        # -I: isolated mode (ignores user site-packages and env vars)
        # -S: do not import site automatically
        # -u: unbuffered I/O for reliable output capture
        cmd = [sys.executable, "-I", "-S", "-u", user_code_path]

        try:
            result = subprocess.run(
                cmd,
                input=input_data,
                capture_output=True,
                text=True,
                cwd=tmpdir,          # confined working dir
                env={},              # empty environment for fewer side effects
                start_new_session=True,  # separate session for termination control
            )
            # duration = time.time() - start
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired as e:
            # On timeout, report and mark as timed_out
            # duration = time.time() - start
            return {
                "stdout": e.stdout or "",
                "stderr": (e.stderr or "") ,
                "returncode": -1,
                # "duration": duration,
                "timed_out": True,
            }


if __name__ == "__main__":
    print("✅ Tool search definition created")

    # Test with one tool
    sample_text = tool_to_text(TOOL_LIBRARY[0])
    print("Sample tool text representation:")
    print(sample_text)

    # create tool embeddings
    tool_embeddings = create_all_tools_embedding()

    test_query = "I need to check the weather"
    test_results = search_tools(test_query, top_k=3, tool_embeddings=[])
    
    print(f"➡️ Test Search Tool API, Query: '{test_query}'\n")
    print("🔍 Top 3 matching tools:")
    for i, result in enumerate(test_results, 1):
        tool_name = result["tool"]["name"]
        score = result["similarity_score"]
        print(f"{i}. {tool_name} (similarity: {score:.3f})")

    res = handle_tool_search("stock market data", top_k=3, tool_embeddings=[])
    print(f"\nReturned {len(res)} tool references:")
    for ref in res:
        print(f"{ref}")