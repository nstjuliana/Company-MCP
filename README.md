# FastMCP Docker Example

This repo provides a minimal FastMCP server, containerized with Docker, plus a small Python client to exercise the tools.

## Build and run with Docker
```
docker build -t fastmcp-example .
docker run -p 8000:8000 fastmcp-example
```
The MCP endpoint is served at `http://localhost:8000/mcp`.

## Test with the Python client
In another shell (with Python and `fastmcp` available):
```
python client.py
```
The client:
- connects to `http://localhost:8000/mcp`
- lists tools
- calls `add(2,3)` and `echo("hello")`

## Notes
- The MCP HTTP endpoint expects MCP clients (SSE + handshake). Use `client.py` or another MCP client; plain curl without the protocol will return a JSON error.
- If you change the MCP path or port, update both `server.py` and `Dockerfile` (CMD) and adjust the client URL accordingly.

