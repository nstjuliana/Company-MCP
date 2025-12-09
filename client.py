import asyncio

from fastmcp import Client


async def main() -> None:
    # Point to the MCP HTTP endpoint exposed by server.py (default path /mcp).
    async with Client("http://localhost:8000/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        print("Tools:", [t.name for t in tools])

        # Call the sample tools
        add_result = await client.call_tool("add", {"a": 2, "b": 3})
        print("add(2,3) =", add_result.content[0].text)

        echo_result = await client.call_tool("echo", {"message": "hello"})
        print("echo =", echo_result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())

