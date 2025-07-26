from mcp.server.fastmcp import FastMCP
from datetime import datetime

# Initialize the MCP server
mcp = FastMCP("toolserver")

@mcp.tool()
def get_current_time(timezone: str = "UTC") -> str:
    """
    Returns the current date and time.
    Args:
        timezone: An optional timezone, defaults to UTC.
    """
    return f"The current date and time is: {datetime.now().isoformat()}"

# Run the tool server if the file is executed directly
if __name__ == "__main__":
    print("Starting Tool Server...")
    mcp.run(transport="stdio")
