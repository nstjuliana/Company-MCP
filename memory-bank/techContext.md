# Technical Context

## Technologies Used

### Backend (MCP Server)
- **Python 3.11**: Core runtime
- **FastMCP 2.13.3**: MCP server framework with HTTP transport
- **SQLite**: Index database with FTS5 extension
- **sqlite-vec 0.1.1+**: Vector similarity search extension
- **OpenAI 1.0.0+**: Embedding generation for vector search
- **python-dotenv 1.0.0+**: Environment variable management

### Frontend
- **FastAPI 0.109.0**: Web framework
- **Uvicorn 0.27.0**: ASGI server
- **Jinja2 3.1.2**: Template engine
- **httpx 0.26.0**: Async HTTP client for MCP calls
- **OpenAI 1.68.0**: GPT-4o integration
- **paramiko 3.4.0**: SFTP client
- **aiofiles 23.2.1**: Async file operations

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy and load balancing
- **SFTP Server**: File access (atmoz/sftp:alpine)

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- OpenAI API key (optional, for vector search)

### Environment Variables
```bash
# Required for vector search
OPENAI_API_KEY=sk-...

# MCP Server Configuration
MCP_NAME=dabstep  # or synth, etc.
MCP_PORT=8000

# SFTP Configuration
SFTP_PORT=2222
SFTP_USER=datauser
SFTP_PASSWORD=changeme
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run server (requires data/index/index.db)
python server.py

# Run frontend (separate terminal)
cd frontend
pip install -r requirements.txt
python main.py
```

### Docker Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose up -d --build

# Stop all services
docker-compose down
```

## Technical Constraints

### 1. No Direct Database Connections
- **Constraint**: MCP server does NOT connect to Postgres/Snowflake
- **Reason**: Security, performance, and separation of concerns
- **Implication**: All schema data must be pre-indexed

### 2. Index Rebuild Required
- **Constraint**: Adding new schema files requires running `setup_db.py`
- **Reason**: SQLite index must be rebuilt to include new files
- **Implication**: Schema updates are not real-time

### 3. Vector Search Optional
- **Constraint**: Vector search requires `OPENAI_API_KEY`
- **Fallback**: FTS5 search works without OpenAI
- **Implication**: System degrades gracefully without API key

### 4. Data Directory Structure
- **Constraint**: Must follow `data/{mcp_name}/map/{database}/domains/{domain}/tables/` structure
- **Reason**: Enables organized, domain-based schema organization
- **Implication**: Schema files must be placed in correct locations

### 5. Single SQLite Database Per Instance
- **Constraint**: Each MCP instance uses one SQLite database
- **Reason**: Simplicity and performance
- **Implication**: All databases (postgres_production, snowflake_production) indexed in same DB

## Dependencies

### Core Dependencies (`requirements.txt`)
```
fastmcp==2.13.3
sqlite-vec>=0.1.1
openai>=1.0.0
python-dotenv>=1.0.0
paramiko>=3.4.0
```

### Frontend Dependencies (`frontend/requirements.txt`)
```
fastapi==0.109.0
uvicorn==0.27.0
httpx==0.26.0
python-multipart==0.0.6
jinja2==3.1.2
paramiko==3.4.0
aiofiles==23.2.1
openai==1.68.0
```

## Database Schema

### SQLite Index Structure
- **documents**: Main document index (tables, columns)
- **documents_fts**: FTS5 virtual table for full-text search
- **documents_vec**: Vector embeddings table (sqlite-vec)
- **keywords**: Extracted search terms with frequency
- **index_weights**: Search ranking configuration
- **index_metadata**: Index configuration and stats

### Key Fields
- `doc_type`: 'table' or 'column'
- `database_name`: 'postgres_production' or 'snowflake_production'
- `domain`: Business domain (e.g., 'payments', 'authentication')
- `file_path`: Path relative to `databases/` prefix
- `content`: Full JSON/Markdown content
- `summary`: Generated summary text

## API Transport

### MCP Protocol
- **Transport**: HTTP (FastMCP HTTP transport)
- **Format**: JSON-RPC 2.0
- **Endpoint**: `/mcp` (or `/mcp/{mcp_name}` via nginx)
- **Methods**: `tools/list`, `tools/call`

### Example Request
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_fts",
    "arguments": {
      "query": "payment",
      "limit": 10
    }
  }
}
```

## Performance Considerations

### Indexing
- **FTS5**: Fast keyword search, no external dependencies
- **Vector Search**: Requires OpenAI API call per query (latency consideration)
- **Caching**: In-memory cache per MCP instance for fast lookups

### Scalability
- **Horizontal**: Multiple MCP instances (dabstep, synth) can run independently
- **Vertical**: SQLite handles thousands of documents efficiently
- **Limits**: FTS5 and vector search have practical limits (50 results default)

## Security Considerations

### Environment Variables
- **Sensitive**: `OPENAI_API_KEY`, `SFTP_PASSWORD`
- **Storage**: Use `.env` file (not committed to git)
- **Docker**: Passed via environment variables

### File Access
- **SFTP**: User/password authentication
- **Data Volume**: Shared read-only mount for frontend, read-write for MCP servers
- **Path Validation**: Frontend validates paths to prevent directory traversal

### Network
- **Internal**: Services communicate via Docker network
- **External**: Only nginx (port 80) and SFTP (port 2222) exposed
- **MCP Servers**: Not directly exposed, accessed via nginx
