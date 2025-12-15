# System Patterns

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Nginx Reverse Proxy (Port 80)             │
│  Routes: / → frontend, /mcp/dabstep → mcp-dabstep, etc.      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Frontend   │   │ mcp-dabstep   │   │  mcp-synth   │
│  (FastAPI)   │   │  (FastMCP)    │   │  (FastMCP)   │
│   Port 80    │   │   Port 8000   │   │  Port 8000   │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       │                  ▼                  │
       │         ┌─────────────────┐        │
       │         │  SQLite Index    │        │
       │         │  (FTS5 + Vector) │        │
       │         └─────────────────┘        │
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  Shared Data Volume   │
              │  data/{mcp_name}/     │
              │  ├── index/index.db   │
              │  └── map/...          │
              └───────────────────────┘
```

## Key Technical Decisions

### 1. Multi-Instance Architecture
- **Pattern**: Environment-based instance isolation
- **Implementation**: `MCP_NAME` environment variable determines data directory
- **Benefit**: Single codebase supports multiple isolated MCP instances
- **Data Isolation**: Each instance uses `data/{mcp_name}/` directory

### 2. Lazy Loading with Caching
- **Pattern**: Per-MCP-name cache with lazy initialization
- **Implementation**: `_MCP_CACHE` dictionary keyed by MCP name
- **Benefit**: Fast startup, memory efficient, supports multiple instances
- **Cache Structure**:
  ```python
  {
    "mcp_name": {
      "DB_SEGMENTS": [],      # Loaded table segments
      "INDEX": {},             # Inverted index
      "SEGMENT_BY_ID": {},     # Quick lookup
      "GRAPH": {},             # Relationship graph
      "initialized": False
    }
  }
  ```

### 3. Dual Search Strategy
- **FTS5 Search**: Fast keyword search using SQLite FTS5 with BM25 ranking
- **Vector Search**: Semantic search using OpenAI embeddings (optional, requires API key)
- **Fallback**: If vector search unavailable, FTS5 still works

### 4. Database-First with In-Memory Fallback
- **Primary**: Query SQLite index database for accurate, up-to-date results
- **Fallback**: Use in-memory segments if database unavailable
- **Benefit**: Resilient to database issues, supports development without full index

### 5. JSON File as Source of Truth
- **Pattern**: Schema files in `data/{mcp_name}/map/` are authoritative
- **Database**: SQLite index is derived from JSON files
- **Benefit**: Human-readable, version-controllable schema definitions

## Component Relationships

### MCP Server (`server.py`)
- **Core**: FastMCP server with 14 tools
- **Dependencies**: SQLite, sqlite-vec (optional), OpenAI (optional)
- **Data Access**: Reads from `data/{mcp_name}/index/index.db` and `data/{mcp_name}/map/`
- **Tools**: Discovery, search, schema retrieval, relationship discovery

### Frontend (`frontend/main.py`)
- **Core**: FastAPI web server
- **Dependencies**: OpenAI (for chat), paramiko (for SFTP), httpx (for MCP calls)
- **Features**:
  - MCP tool proxy
  - GPT-4o chat with tool integration
  - SFTP file browser
  - MCP server management

### Nginx Reverse Proxy
- **Purpose**: Route requests to appropriate services
- **Routes**:
  - `/` → frontend
  - `/mcp/dabstep` → mcp-dabstep:8000
  - `/mcp/synth` → mcp-synth:8000
  - `/health/*` → health checks

### SFTP Server
- **Purpose**: Programmatic file access to data directory
- **Access**: `sftp -P 2222 datauser@localhost`
- **Mount**: `./data` → `/home/datauser/data`

### Markdown Download Utilities
- **Pattern**: Git branch navigation + SFTP file retrieval
- **Implementation**: 
  - `download_markdown_from_branches.py`: Iterates through all git branches, checks out each, connects to SFTP, downloads `.md` files
  - `download_markdown.py`: Downloads from current SFTP state
  - `get_markdown_files.sh`: Orchestrates SFTP server startup and download
- **Output**: Files saved to `sftp-markdown-files/{branch}/` preserving directory structure
- **Benefit**: Automated collection of schema documentation from multiple branches

## Design Patterns

### 1. Tool-Based API
- All functionality exposed as MCP tools
- Tools are stateless and idempotent
- Clear separation between discovery, search, and schema tools

### 2. Filtering Pattern
- Most tools support optional `database` and `domain` filters
- Enables scoped queries within large schemas
- Consistent across all search/listing tools

### 3. Path Translation
- Database stores paths like `databases/postgres_production/domains/...`
- Actual filesystem: `data/{mcp_name}/map/postgres_production/domains/...`
- `_db_path_to_file_path()` handles translation

### 4. Graph-Based Relationship Discovery
- Foreign keys and relationships stored as graph
- BFS traversal for join path finding
- Bidirectional edges for flexible traversal

## Data Flow Patterns

### Search Flow
1. User query → MCP tool call
2. Tool normalizes query (tokenization for FTS5, embedding for vector)
3. Query SQLite index (FTS5 or vector table)
4. Join with documents table for metadata
5. Return ranked results

### Schema Retrieval Flow
1. Tool call with table name
2. Query database for file_path
3. Load actual JSON file from `data/map/`
4. Return complete schema with all metadata

### Multi-Instance Flow
1. Request arrives at nginx with path `/mcp/{mcp_name}`
2. Nginx routes to appropriate container
3. Container has `MCP_NAME={mcp_name}` environment variable
4. Server uses `data/{mcp_name}/` for all operations
5. Cache is isolated per MCP name
