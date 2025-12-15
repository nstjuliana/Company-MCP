# Project Brief

## Project Name
Company MCP - Database Context MCP Server

## Core Purpose
A FastMCP server that provides **database schema context** through search and metadata tools. This MCP serves pre-indexed database documentation — it does **not** connect to actual databases.

## Primary Goals
1. **Index database schemas** from JSON/Markdown files stored in a structured directory hierarchy
2. **Provide search capabilities**:
   - FTS5 full-text search with BM25 ranking
   - Vector similarity search using OpenAI embeddings
   - Token-based search over in-memory indexes
3. **Enable schema discovery**:
   - List databases, domains, tables, and columns
   - Retrieve full table schemas with relationships
   - Find join paths between tables
4. **Support multiple MCP instances** via environment-based configuration (dabstep, synth, etc.)
5. **Provide web interface** for MCP interaction, file browsing, and AI-powered chat

## Key Requirements
- **No direct database connections**: Serves pre-indexed context only
- **Multi-instance support**: Each container runs with its own MCP_NAME (dabstep, synth)
- **Data isolation**: Each MCP instance uses its own data directory (`data/{mcp_name}/`)
- **Search flexibility**: Support both keyword (FTS5) and semantic (vector) search
- **Web UI**: FastAPI frontend with GPT-4o integration for natural language queries
- **File access**: SFTP server for programmatic file management
- **Docker deployment**: Full docker-compose setup with nginx reverse proxy

## Scope Boundaries
- **In scope**: Schema indexing, search, metadata retrieval, web UI, multi-instance support
- **Out of scope**: Direct database connections, data modification, real-time schema updates (requires re-indexing)

## Success Criteria
- Successfully index database schemas from JSON files
- Provide fast and accurate search results (FTS5 and vector)
- Support multiple concurrent MCP instances
- Web UI enables non-technical users to explore database schemas
- AI chat can answer questions using MCP tools
