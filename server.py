from fastmcp import FastMCP

# Minimal FastMCP server with a couple of example tools.
mcp = FastMCP("Example Server")


@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers to verify tool execution."""
    return a + b


@mcp.tool
def echo(message: str) -> str:
    """Echo a message to confirm connectivity."""
    return message


if __name__ == "__main__":
    # Bind to 0.0.0.0 for container networking; use HTTP transport for remote access.
    mcp.run(transport="http", host="0.0.0.0", port=8000)

