from smolagents import CodeAgent, ToolCollection
from smolagents.models import LiteLLMModel
from smolagents.mcp_client import MCPClient
from mcp import StdioServerParameters

def main():
    """
    This is the main function to run the smol-agent.
    """
    # Define the MCP servers
    duckduckgo = StdioServerParameters(
        command="uvx", args=["duckduckgo-mcp-server"]
    )
    firecrawl = StdioServerParameters(
        command="npx", args=["-y", "firecrawl-mcp"],
        env={"FIRECRAWL_API_KEY": "fc-4eff1f299bb14e16bc6538780aa5c166"}
    )

    # Connect to the MCP servers
    with MCPClient(duckduckgo) as ddg_tools, MCPClient(firecrawl) as fc_tools:
        # Create an agent with the MCP tools
        model = LiteLLMModel(model_id="gpt-3.5-turbo")
        agent = CodeAgent(tools=[*ddg_tools, *fc_tools], model=model)

        # Run the agent with a task
        task = "Crawl the website 'https://www.firecrawl.dev' and then search for 'PocketFlow' on the web and tell me what it is."
        result = agent.run(task)
        print(result)

if __name__ == "__main__":
    main()
