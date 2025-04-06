from fastmcp import FastMCP

# Create a named server
mcp = FastMCP("Addition Server")

# Define an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

# Start the server
if __name__ == "__main__":
    mcp.run()