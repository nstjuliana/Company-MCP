# Active Context

## Current Work Focus
**Status**: Wiki page implementation complete

## Recent Changes
- **Wiki Page Added**: New Wiki page for browsing database documentation
  - Hierarchical navigation: Databases → Domains → Tables
  - Search functionality for quick table lookup
  - Markdown rendering with tables, code blocks, and formatting
  - Responsive design matching existing site styling
- **Memory Bank Creation**: Complete memory bank structure established
- **Multi-Instance Support**: Server supports multiple MCP instances via `MCP_NAME` environment variable
- **Docker Compose Setup**: Full deployment with nginx, frontend, multiple MCP servers, and SFTP
- **Web Frontend**: FastAPI frontend with GPT-4o integration for natural language queries

## Current State

### Working Components
1. **MCP Server** (`server.py`):
   - 14 tools implemented (discovery, search, schema, relationships)
   - Multi-instance support via environment variables
   - Dual search (FTS5 and vector)
   - Lazy loading with per-instance caching

2. **Frontend** (`frontend/main.py`):
   - FastAPI web server
   - MCP tool proxy
   - GPT-4o chat with tool integration
   - SFTP file browser
   - MCP server management

3. **Infrastructure**:
   - Docker Compose with nginx reverse proxy
   - Multiple MCP server instances (dabstep, synth)
   - SFTP server for file access

### Data Structure
- **Location**: `data/{mcp_name}/` for each instance
- **Index**: `data/{mcp_name}/index/index.db` (SQLite with FTS5 + vector)
- **Schemas**: `data/{mcp_name}/map/{database}/domains/{domain}/tables/*.json`

### Known Databases
- **postgres_production**: 37 tables across multiple domains
- **snowflake_production**: 4 tables
- **Total**: 41 tables, 428 indexed documents

## Next Steps
1. **Indexing Script**: `setup_db.py` referenced in README but not in repository
   - Need to create or document existing indexing process
   - Should handle FTS5 index creation and vector embedding generation

2. **Testing**: 
   - Verify multi-instance isolation works correctly
   - Test search functionality (FTS5 and vector)
   - Validate web UI functionality

3. **Documentation**:
   - Complete API documentation
   - Deployment guide
   - Indexing guide

## Active Decisions and Considerations

### Multi-Instance Architecture
- **Decision**: Use `MCP_NAME` environment variable for instance isolation
- **Rationale**: Single codebase, multiple isolated instances
- **Consideration**: Each instance needs its own data directory

### Search Strategy
- **Decision**: Support both FTS5 (keyword) and vector (semantic) search
- **Rationale**: Different use cases require different search types
- **Consideration**: Vector search requires OpenAI API key, adds latency

### Data Organization
- **Decision**: Domain-based organization (`data/map/{database}/domains/{domain}/tables/`)
- **Rationale**: Business logic organization, easier navigation
- **Consideration**: Requires consistent file placement

### Frontend Architecture
- **Decision**: FastAPI backend with GPT-4o integration
- **Rationale**: Natural language queries, better UX
- **Consideration**: Requires OpenAI API key, adds cost

## Open Questions
1. **Indexing Process**: How is `setup_db.py` supposed to work? Is it missing or documented elsewhere?
2. **Schema Updates**: What's the workflow for updating schemas? Manual file placement + re-index?
3. **Vector Embeddings**: Are embeddings generated during indexing or on-demand?
4. **Health Checks**: Are health check endpoints implemented for all services?

## Current Blockers
None identified at this time.

## Recent Discoveries
- Server uses lazy loading with per-MCP-name caching for performance
- Frontend can manage multiple MCP servers via configuration file
- Nginx routes `/mcp/{mcp_name}` to appropriate container
- SFTP server provides programmatic file access to data directory
