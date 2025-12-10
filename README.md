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
- calls the sample tools and exercises the PRD2 data tools

## Notes
- The MCP HTTP endpoint expects MCP clients (SSE + handshake). Use `client.py` or another MCP client; plain curl without the protocol will return a JSON error.
- If you change the MCP path or port, update both `server.py` and `Dockerfile` (CMD) and adjust the client URL accordingly.

## Available tools
- `add(a, b)`: demo add.
- `echo(message)`: demo echo.
- `search_db_map(query, top_k)`: semantic-ish lookup over the context map.
- `list_tables(database?, domain?)`: list tables in the map with optional filters.
- `list_columns(table)`: columns for a given table id/title.
- `search_tables(query, database?, domain?, limit?)`: relevance-ranked tables for a query.
- `get_table_schema(table, include_samples?)`: schema details for one table.
- `get_join_path(source_table, target_table, max_hops?)`: suggested join path between tables.
- `get_domain_overview(domain, database?)`: summary of tables in a domain.
- `list_domains(database?)`: available domains and counts.
- `get_common_relationships(database?, domain?, limit?)`: FK-based join patterns.


