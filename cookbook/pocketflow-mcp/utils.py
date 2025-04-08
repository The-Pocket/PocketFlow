from openai import OpenAI
import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Global flag to control whether to use MCP or local implementation
MCP = False

def call_llm(prompt):    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))
    r = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def get_tools(server_script_path=None):
    """Get available tools, either from MCP server or locally based on MCP global setting."""
    if MCP:
        return mcp_get_tools(server_script_path)
    else:
        return local_get_tools(server_script_path)
    
def mcp_get_tools(server_script_path):
    """Get available tools from an MCP server.
    """
    async def _get_tools():
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_response = await session.list_tools()
                return tools_response.tools
    
    return asyncio.run(_get_tools())

def local_get_tools(server_script_path=None):
    """A simple dummy implementation of get_tools without MCP."""
    tools = [
        {
            "name": "add",
            "description": "Add two numbers together",
            "inputSchema": {
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        },
        {
            "name": "subtract",
            "description": "Subtract b from a",
            "inputSchema": {
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        },
        {
            "name": "multiply",
            "description": "Multiply two numbers together",
            "inputSchema": {
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        },
        {
            "name": "divide",
            "description": "Divide a by b",
            "inputSchema": {
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    ]

    class DictObject(dict):
        """A simple class that behaves both as a dictionary and as an object with attributes."""
        def __init__(self, data):
            super().__init__(data)
            for key, value in data.items():
                if isinstance(value, dict):
                    self[key] = DictObject(value)
                elif isinstance(value, list) and value and isinstance(value[0], dict):
                    self[key] = [DictObject(item) for item in value]
        
        def __getattr__(self, key):
            try:
                return self[key]
            except KeyError:
                raise AttributeError(f"'DictObject' object has no attribute '{key}'")

    return [DictObject(tool) for tool in tools]

def call_tool(server_script_path=None, tool_name=None, arguments=None):
    """Call a tool, either from MCP server or locally based on MCP global setting."""
    if MCP:
        return mcp_call_tool(server_script_path, tool_name, arguments)
    else:
        return local_call_tool(server_script_path, tool_name, arguments)
    
def mcp_call_tool(server_script_path=None, tool_name=None, arguments=None):
    """Call a tool on an MCP server.
    """
    async def _call_tool():
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content[0].text
    
    return asyncio.run(_call_tool())

def local_call_tool(server_script_path=None, tool_name=None, arguments=None):
    """A simple dummy implementation of call_tool without MCP."""
    # Simple implementation of tools
    if tool_name == "add":
        if "a" in arguments and "b" in arguments:
            return arguments["a"] + arguments["b"]
        else:
            return "Error: Missing required arguments 'a' or 'b'"
    elif tool_name == "subtract":
        if "a" in arguments and "b" in arguments:
            return arguments["a"] - arguments["b"]
        else:
            return "Error: Missing required arguments 'a' or 'b'"
    elif tool_name == "multiply":
        if "a" in arguments and "b" in arguments:
            return arguments["a"] * arguments["b"]
        else:
            return "Error: Missing required arguments 'a' or 'b'"
    elif tool_name == "divide":
        if "a" in arguments and "b" in arguments:
            if arguments["b"] == 0:
                return "Error: Division by zero is not allowed"
            return arguments["a"] / arguments["b"]
        else:
            return "Error: Missing required arguments 'a' or 'b'"
    else:
        return f"Error: Unknown tool '{tool_name}'"

if __name__ == "__main__":
    print("=== Testing call_llm ===")
    prompt = "In a few words, what is the meaning of life?"
    print(f"Prompt: {prompt}")
    response = call_llm(prompt)
    print(f"Response: {response}")

        # Find available tools
    print("=== Finding available tools ===")
    tools = get_tools("simple_server.py")
    
    # Print tool information nicely formatted
    for i, tool in enumerate(tools, 1):
        print(f"\nTool {i}: {tool.name}")
        print("=" * (len(tool.name) + 8))
        print(f"Description: {tool.description}")
        
        # Parameters section
        print("Parameters:")
        properties = tool.inputSchema.get('properties', {})
        required = tool.inputSchema.get('required', [])
        
        # No parameters case
        if not properties:
            print("  None")
        
        # Print each parameter with its details
        for param_name, param_info in properties.items():
            param_type = param_info.get('type', 'unknown')
            req_status = "(Required)" if param_name in required else "(Optional)"
            print(f"  • {param_name}: {param_type} {req_status}")
    
    # Call a tool
    print("\n=== Calling the add tool ===")
    a, b = 5, 3
    result = call_tool("simple_server.py", "add", {"a": a, "b": b})
    print(f"Result of {a} + {b} = {result}")
    
    # You can easily call with different parameters
    a, b = 10, 20
    result = call_tool("simple_server.py", "add", {"a": a, "b": b})
    print(f"Result of {a} + {b} = {result}")

