# Product Context

## Why This Project Exists
Database schemas are complex and constantly evolving. Developers, analysts, and AI assistants need quick access to accurate schema information without:
- Connecting to production databases
- Parsing scattered documentation
- Manually tracking relationships between tables

This MCP server solves this by providing a centralized, searchable index of database schemas that can be queried programmatically.

## Problems It Solves
1. **Schema Discovery**: Quickly find tables, columns, and relationships across multiple databases
2. **Context for AI**: Provides structured schema context to AI assistants (like GPT-4o) so they can answer database questions accurately
3. **Documentation Access**: Centralized access to pre-indexed schema documentation
4. **Multi-Database Support**: Handle schemas from different database systems (Postgres, Snowflake) in one place
5. **Isolation**: Each MCP instance (dabstep, synth) has its own isolated data context

## How It Should Work

### Data Flow
1. **Indexing Phase** (manual/setup):
   - JSON schema files are placed in `data/{mcp_name}/map/` directory structure
   - `setup_db.py` (referenced but not in repo) indexes these files into SQLite
   - Creates FTS5 full-text index and optional vector embeddings

2. **Query Phase** (runtime):
   - MCP client sends tool calls via HTTP/JSON-RPC
   - Server queries SQLite index (FTS5 or vector search)
   - Returns structured results with metadata

3. **Web Interface**:
   - Users interact via web UI at `http://localhost/`
   - Frontend calls MCP tools via FastAPI backend
   - GPT-4o chat can use MCP tools to answer questions

### User Experience Goals
- **Fast**: Sub-second search results even with large schemas
- **Intuitive**: Natural language queries work via AI chat
- **Comprehensive**: All schema information accessible (columns, keys, relationships)
- **Reliable**: No dependency on live database connections
- **Scalable**: Support multiple MCP instances without conflicts

## Target Users
1. **Developers**: Need to understand database structure for application development
2. **Data Analysts**: Exploring available tables and relationships for analysis
3. **AI Assistants**: Require structured schema context to answer questions accurately
4. **DevOps**: Managing and updating schema documentation

## Key Features
- **14 MCP Tools**: Discovery, search, schema retrieval, relationship tools
- **Dual Search**: FTS5 (keyword) and vector (semantic) search
- **Multi-Instance**: Support for dabstep, synth, and other MCP instances
- **Web UI**: FastAPI frontend with GPT-4o integration
- **File Browser**: SFTP access to data directory
- **Markdown Download Utilities**: Scripts to download schema documentation from all git branches via SFTP
