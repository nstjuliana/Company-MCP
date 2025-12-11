# FastMCP Server with Tribal Knowledge Search

This repo provides a FastMCP server with **FTS5 full-text search** and **vector similarity search** capabilities, containerized with Docker, plus a Python client to exercise the tools.

## Features

- **FTS5 Full-Text Search**: BM25-ranked keyword search with porter stemming
- **Vector Similarity Search**: Semantic search using OpenAI embeddings (1536 dimensions)
- **Hybrid Search**: Reciprocal Rank Fusion combining FTS5 + vector results
- **SQLite-backed**: Persistent storage with sqlite-vec extension for vectors

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up environment
Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Initialize the database
```bash
python setup_db.py
```

This creates `data/tribal-knowledge.db` with:
- FTS5 full-text search index
- Vector embeddings for semantic search
- Pre-computed relationships and keywords

### 4. Build and run with Docker
```bash
docker build -t fastmcp-server .
docker run -p 8000:8000 --env-file .env fastmcp-server
```

The MCP endpoint is served at `http://localhost:8000/mcp`.

### 5. Test with the Python client
```bash
python client.py
```

## Database Schema

The SQLite database (`data/tribal-knowledge.db`) contains:

### `documents` - Main document storage
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_type TEXT NOT NULL,           -- 'table', 'column', 'relationship', 'domain'
    database_name TEXT NOT NULL,       -- Source database name
    schema_name TEXT,                  -- Schema within database
    table_name TEXT,                   -- Table name (if applicable)
    column_name TEXT,                  -- Column name (if applicable)
    domain TEXT,                       -- Business domain grouping
    content TEXT NOT NULL,             -- Full document content
    summary TEXT,                      -- Compressed summary
    keywords TEXT,                     -- Extracted keywords (JSON array)
    file_path TEXT,                    -- Source file path
    content_hash TEXT,                 -- Hash for change detection
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_documents_database ON documents(database_name);
CREATE INDEX idx_documents_table ON documents(database_name, schema_name, table_name);
CREATE INDEX idx_documents_domain ON documents(domain);
CREATE INDEX idx_documents_type ON documents(doc_type);
```

### `documents_fts` - FTS5 Full-Text Search Index
```sql
CREATE VIRTUAL TABLE documents_fts USING fts5(
    content,
    summary,
    keywords,
    content='documents',
    content_rowid='id',
    tokenize='porter'
);
```

### `documents_vec` - Vector Similarity Search (sqlite-vec)
```sql
CREATE VIRTUAL TABLE documents_vec USING vec0(
    document_id INTEGER PRIMARY KEY,
    embedding float[1536]              -- OpenAI text-embedding-3-small
);
```

### `relationships` - Pre-computed join paths
```sql
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    database_name TEXT NOT NULL,
    source_table TEXT NOT NULL,
    target_table TEXT NOT NULL,
    join_path TEXT NOT NULL,           -- JSON array of join steps
    hop_count INTEGER NOT NULL,
    sql_snippet TEXT,                  -- Pre-generated SQL JOIN clause
    confidence REAL,
    UNIQUE(database_name, source_table, target_table)
);
```

### `keywords` - Extracted keywords cache
```sql
CREATE TABLE keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT NOT NULL UNIQUE,
    source_type TEXT,                  -- 'column_name', 'sample_data', 'inferred'
    frequency INTEGER DEFAULT 1
);
```

### `index_weights` - Search weight configuration
```sql
CREATE TABLE index_weights (
    doc_type TEXT PRIMARY KEY,
    fts_weight REAL DEFAULT 1.0,
    vec_weight REAL DEFAULT 1.0,
    boost REAL DEFAULT 1.0
);

-- Default weights
INSERT INTO index_weights VALUES ('table', 1.0, 1.0, 1.5);
INSERT INTO index_weights VALUES ('relationship', 1.0, 1.0, 1.2);
INSERT INTO index_weights VALUES ('column', 0.8, 0.8, 1.0);
INSERT INTO index_weights VALUES ('domain', 1.0, 1.0, 1.0);
```

## Available Tools

### Search Tools

| Tool | Description |
|------|-------------|
| `search_fts(query, database?, domain?, doc_type?, limit?)` | FTS5 full-text search with BM25 ranking. Supports FTS5 query syntax (AND, OR, NOT, quotes). |
| `search_vector(query, database?, domain?, doc_type?, limit?)` | Semantic vector search using OpenAI embeddings. Finds documents with similar meaning. |
| `search_db_map(query, top_k?)` | Quick free-text lookup over the curated context map. |
| `search_tables(query, database?, domain?, limit?)` | Token overlap search with optional filters. |

### Schema Tools

| Tool | Description |
|------|-------------|
| `list_tables(database?, domain?)` | Enumerate tables, optionally filtered. |
| `list_columns(table)` | Get column names/types for a table. |
| `get_table_schema(table, include_samples?)` | Detailed schema with PK/FK/columns. |
| `list_domains(database?)` | List domains and table counts. |
| `get_domain_overview(domain, database?)` | Summarize all tables in a domain. |

### Relationship Tools

| Tool | Description |
|------|-------------|
| `get_join_path(source_table, target_table, max_hops?)` | Find join path via FK graph traversal. |
| `get_common_relationships(database?, domain?, limit?)` | List FK-based join patterns. |

### Utility Tools

| Tool | Description |
|------|-------------|
| `add(a, b)` | Sanity-check connectivity; returns a+b. |
| `echo(message)` | Sanity-check connectivity; echoes message. |

## Example Queries

### FTS5 Search
```python
# Find tables mentioning "payment"
await client.call_tool("search_fts", {"query": "payment", "limit": 5})

# Search for fraud-related content in tables only
await client.call_tool("search_fts", {"query": "fraud", "doc_type": "table"})

# Boolean search
await client.call_tool("search_fts", {"query": "submission AND task"})
```

### Vector Search
```python
# Semantic search - finds related concepts
await client.call_tool("search_vector", {
    "query": "tables related to financial transactions",
    "limit": 3
})

# Find fraud detection columns
await client.call_tool("search_vector", {
    "query": "how to detect suspicious activity"
})

# Domain-filtered semantic search
await client.call_tool("search_vector", {
    "query": "credit card details",
    "domain": "payments"
})
```

## Testing

Run the comprehensive test suite:
```bash
python test_all_search.py
```

This tests:
1. OpenAI embedding generation
2. sqlite-vec storage
3. FTS5 full-text search
4. Vector similarity search
5. Hybrid search with Reciprocal Rank Fusion

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Client                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastMCP Server                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ search_fts  │  │search_vector│  │  Other Tools        │  │
│  └──────┬──────┘  └──────┬──────┘  └─────────────────────┘  │
│         │                │                                   │
│         ▼                ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              SQLite Database                         │    │
│  │  ┌───────────┐  ┌───────────┐  ┌────────────────┐   │    │
│  │  │ documents │  │documents_ │  │ documents_vec  │   │    │
│  │  │  (main)   │  │   fts     │  │  (sqlite-vec)  │   │    │
│  │  └───────────┘  └───────────┘  └────────────────┘   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │  OpenAI API    │
                   │  (embeddings)  │
                   └────────────────┘
```

## Notes

- The MCP HTTP endpoint expects MCP clients (SSE + handshake). Use `client.py` or another MCP client.
- Vector search requires `OPENAI_API_KEY` to be set for generating query embeddings.
- FTS5 search works without OpenAI but requires the database to be initialized.
- Run `setup_db.py` after any changes to `context_map.json` to rebuild the index.
