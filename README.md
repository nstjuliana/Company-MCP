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

## Available tools (purpose and intended use)
- `add(a, b)`: sanity-check connectivity and round-trip latency; returns a+b.
- `echo(message)`: sanity-check connectivity; echoes your message.
- `search_db_map(query, top_k)`: quick free-text lookup over the curated context map; use to discover relevant tables by keywords.
- `list_tables(database?, domain?)`: enumerate tables, optionally filtered by database/domain; use to browse available entities.
- `list_columns(table)`: get column names/types for a table id/title; use before crafting filters or joins.
- `search_tables(query, database?, domain?, limit?)`: semantic-ish table search with optional filters; use to shortlist candidate tables for a question.
- `get_table_schema(table, include_samples?)`: detailed schema (PK/FK/columns); use to validate joins, constraints, and nullable flags. `include_samples` is reserved for future sample values.
- `get_join_path(source_table, target_table, max_hops?)`: suggest join path via FK graph; use to draft JOIN clauses between tables.
- `get_domain_overview(domain, database?)`: summarize all tables in a domain; use for onboarding or scoping analysis.
- `list_domains(database?)`: list domains and table counts; use to navigate the dataset.
- `get_common_relationships(database?, domain?, limit?)`: list FK-based join patterns; use as templates for common joins.


