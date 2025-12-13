# Database Context MCP Server

A FastMCP server that provides **database schema context** through search and metadata tools. This MCP serves pre-indexed database documentation — it does **not** connect to actual databases.

## Purpose

This server indexes database schemas (tables, columns, relationships) from JSON/Markdown files and provides:
- **FTS5 Full-Text Search**: BM25-ranked keyword search
- **Vector Similarity Search**: Semantic search using OpenAI embeddings
- **Schema Retrieval**: Get table/column definitions from indexed JSON files
- **Relationship Discovery**: Find join paths between tables

## Data Structure

### Directory Layout

```
data/
├── index/
│   └── index.db              # SQLite index with FTS5 + vector search
└── map/
    ├── postgres_production/
    │   └── domains/
    │       ├── authentication/
    │       │   └── tables/
    │       │       ├── auth.users.json
    │       │       ├── auth.users.md
    │       │       ├── auth.sessions.json
    │       │       └── ...
    │       ├── payments/
    │       │   └── tables/
    │       │       ├── public.payments.json
    │       │       ├── public.merchants.json
    │       │       └── ...
    │       ├── realtime/
    │       ├── security/
    │       └── storage/
    └── snowflake_production/
        └── domains/
            ├── payments/
            │   └── tables/
            │       └── PUBLIC.DABSTEP_PAYMENTS.json
            └── workflow/
                └── tables/
                    ├── PUBLIC.DABSTEP_TASKS.json
                    ├── PUBLIC.DABSTEP_SUBMISSIONS.json
                    └── PUBLIC.DABSTEP_TASK_SCORES.json
```

### JSON Schema File Format

Each table is documented in a JSON file with this structure:

```json
{
  "table": "payments",
  "schema": "public",
  "database": "postgres_production",
  "description": "Payment transactions processed through the system...",
  "row_count": 138236,
  "columns": [
    {
      "name": "payment_id",
      "type": "character varying",
      "nullable": false,
      "description": "Unique identifier for each payment transaction..."
    }
  ],
  "primary_key": ["payment_id"],
  "foreign_keys": [],
  "indexes": [
    {
      "index_name": "payments_pkey",
      "columns": ["payment_id"],
      "is_unique": true
    }
  ]
}
```

---

## Index Database Schema

The SQLite index database (`data/index/index.db`) contains the following tables:

### `documents` — Main Document Index
Stores all indexed content (tables and columns).

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `doc_type` | TEXT | `'table'` or `'column'` |
| `database_name` | TEXT | `'postgres_production'` or `'snowflake_production'` |
| `schema_name` | TEXT | Schema (e.g., `'auth'`, `'public'`, `'PUBLIC'`) |
| `table_name` | TEXT | Table name |
| `column_name` | TEXT | Column name (for column docs) |
| `domain` | TEXT | Business domain category |
| `content` | TEXT | Full JSON/Markdown content |
| `summary` | TEXT | Generated summary |
| `keywords` | TEXT | JSON array of keywords |
| `file_path` | TEXT | Path to source file in `data/map/` |
| `content_hash` | TEXT | SHA256 for change detection |
| `indexed_at` | DATETIME | When indexed |
| `parent_doc_id` | INTEGER | FK to parent (for columns) |

### `documents_fts` — FTS5 Full-Text Search
Virtual table for BM25-ranked text search.

```sql
CREATE VIRTUAL TABLE documents_fts USING fts5(
    content, summary, keywords,
    content='documents', content_rowid='id'
);
```

### `documents_vec` — Vector Embeddings
Virtual table for semantic similarity search (requires sqlite-vec extension).

```sql
CREATE VIRTUAL TABLE documents_vec USING vec0(
    document_id INTEGER PRIMARY KEY,
    embedding float[1536]  -- OpenAI text-embedding-3-small
);
```

### `keywords` — Extracted Search Terms
Cached keywords with frequency counts.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `term` | TEXT | Keyword |
| `source_type` | TEXT | `'table'` or `'column'` |
| `frequency` | INTEGER | Occurrence count |

### `index_weights` — Search Ranking Configuration

| doc_type | fts_weight | vec_weight | boost |
|----------|------------|------------|-------|
| table | 1.0 | 1.0 | 1.5 |
| column | 0.8 | 0.8 | 1.0 |
| relationship | 1.0 | 1.0 | 1.2 |

### `index_metadata` — Index Configuration
Key-value store for metadata like `embedding_model`, `embedding_dimensions`, `document_count`, `last_full_index`.

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up environment (optional, for vector search)
Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Initialize the database
```bash
python setup_db.py
```

This creates `data/index/index.db` with:
- FTS5 full-text search index
- Vector embeddings for semantic search (if OpenAI key provided)
- Pre-computed keywords

### 4. Run the server
```bash
python server.py
```

Or with Docker:
```bash
docker build -t db-context-mcp .
docker run -p 8000:8000 --env-file .env db-context-mcp
```

The MCP endpoint is served at `http://localhost:8000/mcp`.

### 5. Access the Chatbot UI (Optional)
```bash
python chatbot/web_app.py
```

Open your browser to `http://localhost:3000` to use the interactive chatbot interface.

### 6. Test with the Python client
```bash
python client.py
```

---

## Docker Compose Deployment

For a full deployment with **MCP Server** and **SFTP Server**:

### Quick Start with Docker Compose

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your configuration
#    - Set a secure SFTP_PASSWORD
#    - Add OPENAI_API_KEY for vector search

# 3. Start all services
docker-compose up -d
```

### Services

| Service | Port | Description |
|---------|------|-------------|
| **MCP Server** | `8000` | Database context MCP endpoint |
| **Chatbot UI** | `3000` | Web-based chatbot interface |
| **SFTP Server** | `2222` | SFTP access to `/data` directory |

### SFTP Access

Connect to the SFTP server for programmatic file access:

```bash
# Connect via SFTP
sftp -P 2222 datauser@localhost

# Default credentials (change in .env):
# User: datauser
# Password: changeme
```

Files are accessible at `/home/datauser/data/` which maps to the `./data` directory.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_PORT` | `8000` | MCP server HTTP port |
| `WEB_PORT` | `3000` | Chatbot UI web port |
| `OPENAI_API_KEY` | - | OpenAI API key for vector search |
| `SFTP_PORT` | `2222` | SFTP server port |
| `SFTP_USER` | `datauser` | SFTP username |
| `SFTP_PASSWORD` | `changeme` | SFTP password |

### Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild after changes
docker-compose up -d --build

# View service status
docker-compose ps
```

---

## Chatbot UI

The Database Context MCP includes a modern web-based chatbot interface that allows you to interact with your database schemas using natural language.

### Features

- **Natural Language Queries**: Ask questions like "What databases are available?" or "Show me payment-related tables"
- **Interactive Chat**: Conversational interface with message history
- **Quick Suggestions**: Pre-built query suggestions to get you started
- **Rich Formatting**: Clean, readable responses with proper formatting
- **Responsive Design**: Works on desktop and mobile devices

### Accessing the Chatbot

#### Local Development
```bash
# Start the MCP server first
python server.py &

# Start the chatbot UI
python chatbot/web_app.py
```

Open `http://localhost:3000` in your browser.

#### Docker Deployment
The chatbot UI is included in the Docker Compose setup:

```bash
docker-compose up -d
```

Access the chatbot at `http://localhost:3000`.

### Example Queries

Try these natural language queries:

- "What databases are available?"
- "Show me all tables in the payments domain"
- "Find tables related to user authentication"
- "Get schema for the payments table"
- "List all domains in postgres_production"
- "What tables are related to merchants?"

The chatbot intelligently routes your queries to the appropriate MCP tools and formats the responses for easy reading.

---

## Available Tools (14 total)

### Discovery Tools

| Tool | Description |
|------|-------------|
| `list_databases` | List all indexed databases with table counts and schemas |
| `list_domains` | List all business domains with table counts |
| `list_tables` | List all tables, optionally filtered by database/domain |

#### `list_databases`
Discover what databases are available in the index.

```python
list_databases()
```

**Returns:**
```json
{
  "databases": [
    {"name": "postgres_production", "table_count": 37, "domains": [...], "schemas": [...]},
    {"name": "snowflake_production", "table_count": 4, "domains": [...], "schemas": [...]}
  ]
}
```

#### `list_domains`
List all business domains with table counts.

```python
list_domains(
    database: str = ""    # Optional: filter by database
)
```

**Returns:** `{domains: [{name, description, table_count, databases}]}`

#### `list_tables`
List available tables with metadata.

```python
list_tables(
    database: str = "",   # Optional: filter by database
    domain: str = ""      # Optional: filter by domain
)
```

**Returns:** List of `{name, title, database, schema, domain, summary, file_path}`

---

### Search Tools

| Tool | Description |
|------|-------------|
| `search_fts` | FTS5 full-text search with BM25 ranking |
| `search_vector` | Semantic vector search using OpenAI embeddings |
| `search_db_map` | Quick token-based search over indexed tables |
| `search_tables` | Find tables matching a natural language query |

#### `search_fts`
Full-text search using SQLite FTS5 with BM25 ranking.

```python
search_fts(
    query: str,           # Search text (supports AND, OR, NOT, "exact phrase")
    database: str = "",   # Optional: filter by database
    domain: str = "",     # Optional: filter by domain
    doc_type: str = "",   # Optional: filter by type ("table" or "column")
    limit: int = 10       # Max results (1-50)
)
```

**Returns:** Results with `id`, `table_name`, `summary`, `file_path`, `bm25_rank`

#### `search_vector`
Semantic search using OpenAI embeddings. Finds documents with similar meaning.

```python
search_vector(
    query: str,           # Natural language query
    database: str = "",   # Optional: filter by database
    domain: str = "",     # Optional: filter by domain
    doc_type: str = "",   # Optional: filter by type
    limit: int = 10       # Max results (1-50)
)
```

**Returns:** Results with `id`, `table_name`, `summary`, `file_path`, `distance`

**Note:** Requires `OPENAI_API_KEY` environment variable.

#### `search_db_map`
Quick token-based search over the in-memory table index.

```python
search_db_map(
    query: str,           # Free-text search string
    top_k: int = 3        # Number of results
)
```

**Returns:** List of `{id, title, score, snippet}`

#### `search_tables`
Find tables relevant to a query using token overlap matching.

```python
search_tables(
    query: str,           # Search text
    database: str = "",   # Optional: filter by database
    domain: str = "",     # Optional: filter by domain
    limit: int = 5        # Max results (1-20)
)
```

**Returns:** `{tables: [...], total_matches, tokens_used}`

---

### Schema Tools

| Tool | Description |
|------|-------------|
| `list_columns` | Get columns for a specific table |
| `get_table_schema` | Get full schema details from JSON file |
| `get_domain_overview` | Get all tables in a domain |

#### `list_columns`
Get column definitions for a table.

```python
list_columns(
    table: str,           # Table name (e.g., "merchants", "DABSTEP_PAYMENTS")
    database: str = ""    # Optional: filter by database
)
```

**Returns:** `{table, columns: [{name, type, nullable, description}], file_path}`

#### `get_table_schema`
Retrieve full schema details from the source JSON file.

```python
get_table_schema(
    table: str,                    # Table name
    database: str = "",            # Optional: filter by database
    include_samples: bool = False  # Include sample values if available
)
```

**Returns:** Complete schema including:
- `name`, `database`, `schema`, `description`
- `columns` with types and descriptions
- `primary_key`, `foreign_keys`, `indexes`
- `related_tables`, `file_path`

#### `get_domain_overview`
Get summary of all tables in a business domain.

```python
get_domain_overview(
    domain: str,          # Domain name (e.g., "payments", "authentication")
    database: str = ""    # Optional: filter by database
)
```

**Returns:** `{domain, description, databases, tables: [{name, description}]}`

---

### Relationship Tools

| Tool | Description |
|------|-------------|
| `get_join_path` | Find join path between two tables |
| `get_common_relationships` | List FK-based join patterns |

#### `get_join_path`
Find the join path between two tables via foreign key traversal.

```python
get_join_path(
    source_table: str,    # Starting table
    target_table: str,    # Target table
    database: str = "",   # Optional: filter by database
    max_hops: int = 3     # Maximum join hops
)
```

**Returns:** `{source, target, found, hop_count, path: [...], sql_snippet}`

#### `get_common_relationships`
List frequently used join patterns based on foreign keys.

```python
get_common_relationships(
    database: str = "",   # Optional: filter by database
    domain: str = "",     # Optional: filter by domain
    limit: int = 10       # Max relationships
)
```

**Returns:** `{relationships: [{source_table, target_table, join_sql, description}]}`

---

### Utility Tools

| Tool | Description |
|------|-------------|
| `add(a, b)` | Returns a + b (connectivity test) |
| `echo(message)` | Returns the message (connectivity test) |

---

## Example Usage

### Discover Available Data
```python
# List all databases
list_databases()
# → postgres_production (37 tables), snowflake_production (4 tables)

# List tables in a specific database
list_tables(database="snowflake_production")

# List business domains
list_domains()
```

### Search for Tables
```python
# FTS5 search
search_fts(query="payment fraud", limit=5)

# Semantic search
search_vector(query="tables related to financial transactions", limit=3)

# Search within a specific database
search_fts(query="merchant", database="postgres_production")
```

### Get Schema Details
```python
# Get schema for a table (auto-detects database)
get_table_schema(table="payments")

# Get schema from specific database
get_table_schema(table="payments", database="postgres_production")
get_table_schema(table="DABSTEP_PAYMENTS", database="snowflake_production")

# Get columns only
list_columns(table="merchants", database="postgres_production")
```

### Explore Relationships
```python
# Find join path between tables
get_join_path(
    source_table="merchants",
    target_table="payments",
    database="postgres_production"
)

# Get common relationships in a domain
get_common_relationships(domain="payments")
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Client                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastMCP Server                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ search_fts  │  │search_vector│  │ Schema Tools        │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         │                │                     │            │
│         ▼                ▼                     ▼            │
│  ┌─────────────────────────────┐    ┌─────────────────────┐│
│  │   data/index/index.db      │    │   data/map/*.json   ││
│  │  ┌───────────┐ ┌─────────┐ │    │   (source schemas)  ││
│  │  │   FTS5    │ │ Vectors │ │    └─────────────────────┘│
│  │  └───────────┘ └─────────┘ │                            │
│  └─────────────────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼ (vector search only)
                   ┌────────────────┐
                   │  OpenAI API    │
                   │  (embeddings)  │
                   └────────────────┘
```

---

## Indexed Content Summary

| Database | Tables | Domains | Schemas |
|----------|--------|---------|---------|
| postgres_production | 37 | analytics, authentication, customers, general, messaging, payments | auth, public, realtime, storage, vault |
| snowflake_production | 4 | general, payments | PUBLIC |

**Total:** 41 tables, 428 indexed documents (tables + columns)

---

## Notes

- **No database connections**: This MCP serves pre-indexed context only — it does not connect to actual Postgres or Snowflake databases.
- **Vector search** requires `OPENAI_API_KEY` to generate query embeddings at runtime.
- **FTS5 search** works without OpenAI using the pre-built index.
- **Database parameter**: Use `database="postgres_production"` or `database="snowflake_production"` to target specific databases when table names might overlap.
- Run `setup_db.py` after adding new JSON files to `data/map/` to rebuild the index.
