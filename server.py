from fastmcp import FastMCP
import json
import os
import re
import sqlite3
from collections import defaultdict, deque
from pathlib import Path
from typing import List, Dict, Any, DefaultDict, Set, Optional

# Try to import sqlite_vec for vector search
try:
    import sqlite_vec
    HAS_SQLITE_VEC = True
except ImportError:
    HAS_SQLITE_VEC = False

# Try to import OpenAI for embeddings
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Load environment variables from .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Database Context MCP Server - provides schema context through search and metadata tools.
mcp = FastMCP("Database Context Server")

BASE_DIR = Path(__file__).resolve().parent
DATA_MAP_PATH = BASE_DIR / "data" / "map"
DB_PATH = BASE_DIR / "data" / "index" / "index.db"

# OpenAI embedding configuration
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536

# Initialize OpenAI client if available
_openai_client: Optional["OpenAI"] = None
if HAS_OPENAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        _openai_client = OpenAI(api_key=api_key)


def _load_json(path: Path) -> Any:
    """Load JSON from a file path."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _db_path_to_file_path(db_path: str) -> Path:
    """
    Translate a database file_path to an actual filesystem path.
    DB stores: databases/postgres_production/domains/...
    Actual:    data/map/postgres_production/domains/...
    """
    # Remove 'databases/' prefix and prepend actual data/map path
    if db_path.startswith("databases/"):
        relative = db_path[len("databases/"):]
    else:
        relative = db_path
    return DATA_MAP_PATH / relative


def _load_map_file(db_path: str) -> Optional[Dict[str, Any]]:
    """Load a JSON file from data/map given a database file_path."""
    try:
        file_path = _db_path_to_file_path(db_path)
        if file_path.exists() and file_path.suffix == ".json":
            return _load_json(file_path)
    except Exception:
        pass
    return None


def _safe_load_map() -> List[Dict[str, Any]]:
    """Load table segments from index.db database."""
    db = _get_db_connection()
    if not db:
        return []
    
    try:
        cursor = db.execute("""
            SELECT DISTINCT table_name, database_name, schema_name, domain, file_path, summary, content
            FROM documents 
            WHERE doc_type = 'table' AND file_path LIKE '%.json'
        """)
        segments = []
        for row in cursor.fetchall():
            try:
                # Parse JSON content directly from DB
                content = json.loads(row["content"]) if row["content"] else {}
                
                # Get clean table name (strip .json suffix if present)
                table_name = row["table_name"]
                if table_name.endswith(".json"):
                    table_name = table_name[:-5]
                
                seg = {
                    "id": table_name,
                    "title": f"{table_name} table",
                    "summary": row["summary"] or content.get("description", ""),
                    "database": row["database_name"],
                    "domain": row["domain"] or "default",
                    "schema": row["schema_name"],
                    "file_path": row["file_path"],
                    "columns": content.get("columns", []),
                    "keys": {
                        "primary": content.get("primary_key", []),
                        "foreign": content.get("foreign_keys", []),
                    },
                    "relationships": content.get("relationships", {}),
                }
                segments.append(seg)
            except (json.JSONDecodeError, TypeError):
                continue
        db.close()
        return segments
    except Exception:
        db.close()
        return []


# Defer loading DB_SEGMENTS until after _get_db_connection is defined
DB_SEGMENTS: List[Dict[str, Any]] = []


def _normalize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _segment_tokens(seg: Dict[str, Any]) -> Set[str]:
    text_parts = [
        seg.get("id", ""),
        seg.get("title", ""),
        seg.get("summary", ""),
        seg.get("database", ""),
        seg.get("domain", ""),
        " ".join(col.get("name", "") for col in seg.get("columns", [])),
    ]
    return set(_normalize(" ".join(text_parts)))


def _build_index(segments: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
    """
    Build a lightweight inverted index: token -> set(segment_ids).
    Scales better as the context map grows.
    """
    index: DefaultDict[str, Set[str]] = defaultdict(set)
    for seg in segments:
        for token in _segment_tokens(seg):
            index[token].add(seg["id"])
    return dict(index)


def _safe_load_index() -> Dict[str, Set[str]]:
    """Build inverted index from DB_SEGMENTS."""
    return _build_index(DB_SEGMENTS)


# These will be initialized after _get_db_connection is defined
INDEX: Dict[str, Set[str]] = {}
SEGMENT_BY_ID: Dict[str, Dict[str, Any]] = {}


def _find_table(table: str, database: str = "") -> Dict[str, Any]:
    """Find a table segment by name (flexible matching), optionally filtered by database."""
    # Normalize input: strip .json suffix if present
    table_clean = table
    if table_clean.endswith(".json"):
        table_clean = table_clean[:-5]
    table_norm = table_clean.lower()
    
    # Filter by database if specified
    segments = DB_SEGMENTS
    if database:
        segments = [s for s in DB_SEGMENTS if s.get("database") == database]
    
    # Try exact match first (case-insensitive)
    for seg in segments:
        if seg["id"].lower() == table_norm:
            return seg
    
    # Try matching title
    for seg in segments:
        if seg.get("title", "").lower() == f"{table_norm} table":
            return seg
    
    # Try partial match (table name contains search term)
    for seg in segments:
        if table_norm in seg["id"].lower():
            return seg
    
    return {}


def _estimate_tokens(text: str) -> int:
    # Rough heuristic: 1 token ≈ 4 chars; sufficient for budget hints.
    return max(1, len(text) // 4)


def _foreign_key_edges(seg: Dict[str, Any]) -> List[Dict[str, Any]]:
    edges = []
    for fk in seg.get("keys", {}).get("foreign", []) or []:
        ref = fk.get("references", "")
        ref_table = ref.split("(")[0] if "(" in ref else ref
        edges.append(
            {
                "from": seg["id"],
                "to": ref_table,
                "columns": fk.get("columns", []),
                "references": ref,
            }
        )
    return edges


def _build_graph() -> Dict[str, List[Dict[str, Any]]]:
    graph: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
    for seg in DB_SEGMENTS:
        # Foreign key edges (bidirectional for traversal)
        for edge in _foreign_key_edges(seg):
            graph[edge["from"]].append({"to": edge["to"], "info": edge})
            graph[edge["to"]].append({"to": edge["from"], "info": edge})
        rel = seg.get("relationships", {}) or {}
        for dep in rel.get("depends_on", []) or []:
            graph[seg["id"]].append({"to": dep, "info": {"note": "depends_on"}})
            graph[dep].append({"to": seg["id"], "info": {"note": "referenced_by"}})
        for ref in rel.get("referenced_by", []) or []:
            graph[seg["id"]].append({"to": ref, "info": {"note": "referenced_by"}})
            graph[ref].append({"to": seg["id"], "info": {"note": "depends_on"}})
    return graph


GRAPH: Dict[str, List[Dict[str, Any]]] = {}


# --- Database connection helpers ---

def _get_db_connection() -> Optional[sqlite3.Connection]:
    """Get a connection to the SQLite database."""
    if not DB_PATH.exists():
        return None
    
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    
    # Load sqlite-vec extension if available
    if HAS_SQLITE_VEC:
        try:
            db.enable_load_extension(True)
            sqlite_vec.load(db)
            db.enable_load_extension(False)
        except Exception:
            pass  # Vector search won't work but FTS will
    
    return db


def _initialize_globals():
    """Initialize global data structures after DB connection is available."""
    global DB_SEGMENTS, INDEX, SEGMENT_BY_ID, GRAPH
    DB_SEGMENTS = _safe_load_map()
    INDEX = _safe_load_index()
    SEGMENT_BY_ID = {seg["id"]: seg for seg in DB_SEGMENTS}
    GRAPH = _build_graph()


# Initialize globals now that _get_db_connection is defined
_initialize_globals()


def _generate_query_embedding(query: str) -> Optional[List[float]]:
    """Generate embedding for a search query using OpenAI."""
    if not _openai_client:
        return None
    
    try:
        response = _openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query,
            dimensions=EMBEDDING_DIMENSIONS,
        )
        return response.data[0].embedding
    except Exception:
        return None


# --- Basic tools ---

@mcp.tool
def add(a: float, b: float) -> float:
    """
    Add two numbers to verify tool execution.

    Args:
        a: First number.
        b: Second number.
    Returns:
        Sum of a and b.
    """
    return a + b


@mcp.tool
def echo(message: str) -> str:
    """
    Echo a message to confirm connectivity.

    Args:
        message: Text to echo back.
    Returns:
        The same message.
    """
    return message


@mcp.tool
def search_db_map(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Match a natural language query to the most relevant DB map segments.
    Returns top_k segments with id, title, score, and snippet.

    Args:
        query: Free-text search string.
        top_k: Number of results to return (minimum 1).
    Returns:
        List of segment dicts with id, title, score, and snippet.
    """
    q_tokens = set(_normalize(query))
    candidate_ids: Set[str] = set()

    # Retrieve candidate segment ids via inverted index for efficiency.
    for token in q_tokens:
        candidate_ids |= INDEX.get(token, set())

    # Fallback: if no candidates, consider all segments.
    if not candidate_ids:
        candidate_ids = {seg["id"] for seg in DB_SEGMENTS}

    scored = []
    for seg in DB_SEGMENTS:
        if seg["id"] not in candidate_ids:
            continue
        text_parts = [
            seg.get("id", ""),
            seg.get("title", ""),
            seg.get("summary", ""),
            " ".join(col["name"] for col in seg.get("columns", [])),
        ]
        seg_tokens = set(_normalize(" ".join(text_parts)))
        score = len(q_tokens & seg_tokens)
        scored.append(
            {
                "id": seg["id"],
                "title": seg["title"],
                "score": score,
                "snippet": seg["summary"],
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[: max(1, top_k)]


# --- Search Tools ---

@mcp.tool
def search_fts(
    query: str,
    database: str = "",
    domain: str = "",
    doc_type: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """
    Full-text search using FTS5 with BM25 ranking.
    Searches document content, summary, and keywords.

    Args:
        query: Search text (supports FTS5 query syntax like AND, OR, NOT, quotes).
        database: Optional database filter.
        domain: Optional domain filter.
        doc_type: Optional document type filter (table, column, relationship, domain).
        limit: Max results (1-50).
    Returns:
        Dict with results list, each containing id, table_name, doc_type, summary, rank, and tokens_used.
    """
    limit = max(1, min(limit, 50))
    
    db = _get_db_connection()
    if not db:
        return {
            "error": "Database not found. Run setup_db.py first.",
            "results": [],
            "tokens_used": 0,
        }
    
    try:
        # Build the FTS query - escape special characters for safety
        # FTS5 supports: AND, OR, NOT, quotes, prefix*, NEAR()
        fts_query = query
        
        # Build WHERE clause for filters
        filters = []
        params: List[Any] = [fts_query, limit]
        
        if database:
            filters.append("d.database_name = ?")
            params.insert(-1, database)
        if domain:
            filters.append("d.domain = ?")
            params.insert(-1, domain)
        if doc_type:
            filters.append("d.doc_type = ?")
            params.insert(-1, doc_type)
        
        filter_clause = ""
        if filters:
            filter_clause = "AND " + " AND ".join(filters)
        
        # Execute FTS5 search with BM25 ranking
        sql = f"""
            SELECT 
                d.id,
                d.doc_type,
                d.database_name,
                d.table_name,
                d.column_name,
                d.domain,
                d.summary,
                d.content,
                d.file_path,
                bm25(documents_fts) as rank
            FROM documents_fts fts
            JOIN documents d ON d.id = fts.rowid
            WHERE documents_fts MATCH ?
            {filter_clause}
            ORDER BY rank
            LIMIT ?
        """
        
        cursor = db.execute(sql, params)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            # Convert DB path to actual file path
            file_path = row["file_path"]
            actual_path = str(_db_path_to_file_path(file_path)) if file_path else None
            
            result = {
                "id": row["id"],
                "doc_type": row["doc_type"],
                "database": row["database_name"],
                "table_name": row["table_name"],
                "column_name": row["column_name"],
                "domain": row["domain"],
                "summary": row["summary"],
                "content_preview": row["content"][:200] + "..." if len(row["content"]) > 200 else row["content"],
                "file_path": actual_path,
                "bm25_rank": round(row["rank"], 4),
            }
            results.append(result)
        
        db.close()
        
        return {
            "results": results,
            "total_matches": len(results),
            "query": query,
            "tokens_used": _estimate_tokens(query + str(results)),
        }
        
    except sqlite3.OperationalError as e:
        db.close()
        error_msg = str(e)
        if "no such table" in error_msg:
            return {
                "error": "FTS5 index not found. Run setup_db.py to create the database.",
                "results": [],
                "tokens_used": 0,
            }
        elif "fts5: syntax error" in error_msg.lower():
            return {
                "error": f"Invalid FTS5 query syntax: {error_msg}. Try simpler terms or quote exact phrases.",
                "results": [],
                "tokens_used": 0,
            }
        else:
            return {
                "error": f"Database error: {error_msg}",
                "results": [],
                "tokens_used": 0,
            }


@mcp.tool
def search_vector(
    query: str,
    database: str = "",
    domain: str = "",
    doc_type: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """
    Semantic vector search using OpenAI embeddings and sqlite-vec.
    Finds documents with similar meaning to the query.

    Args:
        query: Natural language search query.
        database: Optional database filter.
        domain: Optional domain filter.
        doc_type: Optional document type filter (table, column, relationship, domain).
        limit: Max results (1-50).
    Returns:
        Dict with results list, each containing id, table_name, doc_type, summary, distance, and tokens_used.
    """
    limit = max(1, min(limit, 50))
    
    # Check prerequisites
    if not HAS_SQLITE_VEC:
        return {
            "error": "sqlite-vec not installed. Install with: pip install sqlite-vec",
            "results": [],
            "tokens_used": 0,
        }
    
    if not _openai_client:
        return {
            "error": "OpenAI client not available. Set OPENAI_API_KEY environment variable.",
            "results": [],
            "tokens_used": 0,
        }
    
    db = _get_db_connection()
    if not db:
        return {
            "error": "Database not found. Run setup_db.py first.",
            "results": [],
            "tokens_used": 0,
        }
    
    try:
        # Generate embedding for query
        query_embedding = _generate_query_embedding(query)
        if not query_embedding:
            db.close()
            return {
                "error": "Failed to generate query embedding.",
                "results": [],
                "tokens_used": 0,
            }
        
        # Convert embedding to JSON for sqlite-vec
        embedding_json = json.dumps(query_embedding)
        
        # Build WHERE clause for filters on the joined documents table
        filters = []
        params: List[Any] = []
        
        if database:
            filters.append("d.database_name = ?")
            params.append(database)
        if domain:
            filters.append("d.domain = ?")
            params.append(domain)
        if doc_type:
            filters.append("d.doc_type = ?")
            params.append(doc_type)
        
        # For vec0, we need k = ? in WHERE clause for KNN queries
        # First get vector matches, then filter
        if filters:
            filter_clause = "WHERE " + " AND ".join(filters)
            
            sql = f"""
                WITH vec_matches AS (
                    SELECT 
                        document_id,
                        distance
                    FROM documents_vec
                    WHERE embedding MATCH ? AND k = ?
                )
                SELECT 
                    d.id,
                    d.doc_type,
                    d.database_name,
                    d.table_name,
                    d.column_name,
                    d.domain,
                    d.summary,
                    d.content,
                    d.file_path,
                    vm.distance
                FROM vec_matches vm
                JOIN documents d ON d.id = vm.document_id
                {filter_clause}
                ORDER BY vm.distance
            """
            params = [embedding_json, limit * 2] + params  # Fetch more to account for filtering
        else:
            sql = """
                SELECT 
                    d.id,
                    d.doc_type,
                    d.database_name,
                    d.table_name,
                    d.column_name,
                    d.domain,
                    d.summary,
                    d.content,
                    d.file_path,
                    v.distance
                FROM documents_vec v
                JOIN documents d ON d.id = v.document_id
                WHERE v.embedding MATCH ? AND k = ?
                ORDER BY v.distance
            """
            params = [embedding_json, limit]
        
        cursor = db.execute(sql, params)
        rows = cursor.fetchall()
        
        results = []
        for row in rows[:limit]:  # Ensure we respect limit after filtering
            # Convert DB path to actual file path
            file_path = row["file_path"]
            actual_path = str(_db_path_to_file_path(file_path)) if file_path else None
            
            result = {
                "id": row["id"],
                "doc_type": row["doc_type"],
                "database": row["database_name"],
                "table_name": row["table_name"],
                "column_name": row["column_name"],
                "domain": row["domain"],
                "summary": row["summary"],
                "content_preview": row["content"][:200] + "..." if len(row["content"]) > 200 else row["content"],
                "file_path": actual_path,
                "distance": round(row["distance"], 4),
            }
            results.append(result)
        
        db.close()
        
        return {
            "results": results,
            "total_matches": len(results),
            "query": query,
            "embedding_model": EMBEDDING_MODEL,
            "tokens_used": _estimate_tokens(query + str(results)),
        }
        
    except sqlite3.OperationalError as e:
        db.close()
        error_msg = str(e)
        if "no such table" in error_msg:
            return {
                "error": "Vector index not found. Run setup_db.py with OPENAI_API_KEY set to create embeddings.",
                "results": [],
                "tokens_used": 0,
            }
        else:
            return {
                "error": f"Database error: {error_msg}",
                "results": [],
                "tokens_used": 0,
            }


# --- PRD2 tools based on planning spec ---


@mcp.tool
def list_tables(database: str = "", domain: str = "") -> List[Dict[str, Any]]:
    """
    List available tables, optionally filtered by database or domain.

    Args:
        database: Optional database filter.
        domain: Optional domain filter.
    Returns:
        List of table metadata dicts.
    """
    # Try database first, fall back to in-memory segments
    db = _get_db_connection()
    if db:
        try:
            filters = ["doc_type = 'table'", "file_path LIKE '%.json'"]
            params: List[Any] = []
            
            if database:
                filters.append("database_name = ?")
                params.append(database)
            if domain:
                filters.append("domain = ?")
                params.append(domain)
            
            filter_clause = " AND ".join(filters)
            
            cursor = db.execute(f"""
                SELECT id, table_name, database_name, schema_name, domain, summary, file_path
                FROM documents
                WHERE {filter_clause}
            """, params)
            
            results = []
            for row in cursor.fetchall():
                # Strip .json suffix from table name
                table_name = row["table_name"]
                if table_name.endswith(".json"):
                    table_name = table_name[:-5]
                
                results.append({
                    "name": table_name,
                    "title": f"{table_name} table",
                    "database": row["database_name"],
                    "schema": row["schema_name"],
                    "domain": row["domain"],
                    "summary": row["summary"],
                    "file_path": str(_db_path_to_file_path(row["file_path"])),
                })
            
            db.close()
            return results
        except Exception:
            db.close()
    
    # Fallback to in-memory segments
    results = []
    for seg in DB_SEGMENTS:
        if database and seg.get("database", "") != database:
            continue
        if domain and seg.get("domain", "") != domain:
            continue
        results.append(
            {
                "name": seg["id"],
                "title": seg.get("title", seg["id"]),
                "database": seg.get("database", "default"),
                "domain": seg.get("domain", "default"),
                "summary": seg.get("summary", ""),
                "key_columns": seg.get("keys", {}).get("primary", []),
            }
        )
    return results


@mcp.tool
def list_columns(table: str, database: str = "") -> Dict[str, Any]:
    """
    List columns for a given table, with their types and descriptions.

    Args:
        table: Table name (e.g., 'merchants', 'DABSTEP_PAYMENTS').
        database: Optional database filter (e.g., 'postgres_production', 'snowflake_production').
    Returns:
        Dict with table name, columns list [{name, type, nullable, description}], and file_path.
    """
    # Try to load from actual JSON file first
    db = _get_db_connection()
    if db:
        try:
            # Find the table's JSON file, optionally filtered by database
            if database:
                cursor = db.execute("""
                    SELECT file_path, table_name
                    FROM documents 
                    WHERE doc_type = 'table' 
                    AND (table_name = ? OR table_name LIKE ? OR LOWER(table_name) = LOWER(?))
                    AND database_name = ?
                    AND file_path LIKE '%.json'
                    LIMIT 1
                """, (table, f"%{table}%", table, database))
            else:
                cursor = db.execute("""
                    SELECT file_path, table_name
                    FROM documents 
                    WHERE doc_type = 'table' 
                    AND (table_name = ? OR table_name LIKE ? OR LOWER(table_name) = LOWER(?))
                    AND file_path LIKE '%.json'
                    LIMIT 1
                """, (table, f"%{table}%", table))
            row = cursor.fetchone()
            db.close()
            
            if row:
                json_content = _load_map_file(row["file_path"])
                if json_content and "columns" in json_content:
                    columns = []
                    for col in json_content["columns"]:
                        columns.append({
                            "name": col.get("name"),
                            "type": col.get("type"),
                            "nullable": col.get("nullable", True),
                            "description": col.get("description", ""),
                        })
                    # Strip .json suffix from table name
                    table_name = row["table_name"]
                    if table_name.endswith(".json"):
                        table_name = table_name[:-5]
                    
                    return {
                        "table": table_name,
                        "columns": columns,
                        "file_path": str(_db_path_to_file_path(row["file_path"])),
                    }
        except Exception:
            if db:
                db.close()
    
    # Fallback to in-memory segments
    seg = _find_table(table, database)
    if not seg:
        return {"error": f"table '{table}' not found"}
    columns = []
    for col in seg.get("columns", []):
        columns.append(
            {
                "name": col.get("name"),
                "type": col.get("type"),
                "nullable": "not null" not in (col.get("notes", "") or "").lower(),
                "description": col.get("notes", ""),
            }
        )
    return {"table": seg["id"], "columns": columns}


@mcp.tool
def search_tables(
    query: str, database: str = "", domain: str = "", limit: int = 5
) -> Dict[str, Any]:
    """
    Find tables relevant to a natural language query.
    Simplified implementation using token overlap on the curated map.

    Args:
        query: Search text.
        database: Optional database filter.
        domain: Optional domain filter.
        limit: Max results (1-20).
    Returns:
        Dict with table list, tokens used, and total matches.
    """
    limit = max(1, min(limit, 20))
    q_tokens = set(_normalize(query))
    scored = []
    for seg in DB_SEGMENTS:
        if database and seg.get("database", "") != database:
            continue
        if domain and seg.get("domain", "") != domain:
            continue
        seg_tokens = _segment_tokens(seg)
        overlap = len(q_tokens & seg_tokens)
        # Light boost for substring matches in id/title/summary.
        text_blob = " ".join(
            [seg.get("id", ""), seg.get("title", ""), seg.get("summary", "")]
        ).lower()
        if any(tok in text_blob for tok in q_tokens):
            overlap += 0.5
        scored.append(
            {
                "name": seg["id"],
                "database": seg.get("database", "default"),
                "domain": seg.get("domain", "default"),
                "summary": seg.get("summary", ""),
                "key_columns": seg.get("keys", {}).get("primary", []),
                "relevance_score": round(overlap, 3),
            }
        )

    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    results = scored[:limit]
    return {
        "tables": results,
        "tokens_used": _estimate_tokens(query),
        "total_matches": len(scored),
    }


@mcp.tool
def get_table_schema(table: str, database: str = "", include_samples: bool = False) -> Dict[str, Any]:
    """
    Retrieve full schema details for a specific table from the source JSON file.

    Args:
        table: Table name (e.g., 'payments', 'DABSTEP_PAYMENTS').
        database: Optional database filter (e.g., 'postgres_production', 'snowflake_production').
        include_samples: Include sample values from the JSON if available.
    Returns:
        Complete schema with name, database, schema, description, row_count, columns,
        primary_key, foreign_keys, indexes, related_tables, and file_path.
    """
    # First, try to get the file path from the database and load the actual JSON
    db = _get_db_connection()
    if db:
        try:
            # Search for the table by name (case-insensitive)
            # Optionally filter by database
            if database:
                cursor = db.execute("""
                    SELECT file_path, content, database_name, schema_name, domain, summary
                    FROM documents 
                    WHERE doc_type = 'table' 
                    AND (table_name = ? OR table_name LIKE ? OR LOWER(table_name) = LOWER(?))
                    AND database_name = ?
                    AND file_path LIKE '%.json'
                    LIMIT 1
                """, (table, f"%{table}%", table, database))
            else:
                cursor = db.execute("""
                    SELECT file_path, content, database_name, schema_name, domain, summary
                    FROM documents 
                    WHERE doc_type = 'table' 
                    AND (table_name = ? OR table_name LIKE ? OR LOWER(table_name) = LOWER(?))
                    AND file_path LIKE '%.json'
                    LIMIT 1
                """, (table, f"%{table}%", table))
            row = cursor.fetchone()
            db.close()
            
            if row:
                # Try to load the actual JSON file for full content
                json_content = _load_map_file(row["file_path"])
                if json_content:
                    columns = []
                    for col in json_content.get("columns", []):
                        col_entry = {
                            "name": col.get("name"),
                            "type": col.get("type"),
                            "nullable": col.get("nullable", True),
                            "description": col.get("description", ""),
                        }
                        if include_samples:
                            col_entry["samples"] = col.get("sample_values", [])
                        columns.append(col_entry)
                    
                    return {
                        "name": json_content.get("table", table),
                        "database": json_content.get("database", row["database_name"]),
                        "schema": json_content.get("schema", row["schema_name"]),
                        "description": json_content.get("description", row["summary"]),
                        "row_count": json_content.get("row_count"),
                        "columns": columns,
                        "primary_key": json_content.get("primary_key", []),
                        "foreign_keys": json_content.get("foreign_keys", []),
                        "indexes": json_content.get("indexes", []),
                        "related_tables": json_content.get("relationships", {}),
                        "file_path": str(_db_path_to_file_path(row["file_path"])),
                        "tokens_used": _estimate_tokens(json_content.get("description", "")),
                    }
        except Exception:
            if db:
                db.close()
    
    # Fallback to in-memory segments
    seg = _find_table(table, database)
    if not seg:
        return {"error": f"table '{table}' not found"}

    columns = []
    for col in seg.get("columns", []):
        col_entry = {
            "name": col.get("name"),
            "type": col.get("type"),
            "nullable": "not null" not in (col.get("notes", "") or "").lower(),
            "description": col.get("notes", ""),
        }
        if include_samples:
            col_entry["samples"] = []
        columns.append(col_entry)

    keys = seg.get("keys", {}) or {}
    foreign_keys = []
    for fk in keys.get("foreign", []) or []:
        ref = fk.get("references", "")
        ref_table = ref.split("(")[0] if "(" in ref else ref
        foreign_keys.append(
            {"columns": fk.get("columns", []), "references": ref, "table": ref_table}
        )

    return {
        "name": seg["id"],
        "database": seg.get("database", "default"),
        "schema": seg.get("schema", "public"),
        "description": seg.get("summary", ""),
        "row_count": seg.get("row_count"),
        "columns": columns,
        "primary_key": keys.get("primary", []),
        "foreign_keys": foreign_keys,
        "indexes": keys.get("indexes", []),
        "related_tables": seg.get("relationships", {}),
        "tokens_used": _estimate_tokens(seg.get("summary", "")),
    }


@mcp.tool
def get_join_path(
    source_table: str, target_table: str, database: str = "", max_hops: int = 3
) -> Dict[str, Any]:
    """
    Find the join path between two tables using foreign key graph traversal.

    Args:
        source_table: Starting table name.
        target_table: Destination table name.
        database: Optional database filter (e.g., 'postgres_production', 'snowflake_production').
        max_hops: Maximum number of joins to traverse (default 3).
    Returns:
        Dict with source, target, found (bool), hop_count, path steps, and sql_snippet.
        Note: Requires foreign_keys to be defined in the source JSON files.
    """
    src = _find_table(source_table, database).get("id")
    tgt = _find_table(target_table, database).get("id")
    if not src or not tgt:
        return {"error": "source or target table not found"}

    visited = {src}
    queue = deque([(src, [])])
    found_path: List[str] = []

    while queue:
        node, path = queue.popleft()
        if len(path) > max_hops:
            continue
        if node == tgt:
            found_path = path
            break
        for edge in GRAPH.get(node, []):
            nxt = edge["to"]
            if nxt in visited:
                continue
            visited.add(nxt)
            queue.append((nxt, path + [edge]))

    if not found_path:
        return {
            "source": src,
            "target": tgt,
            "found": False,
            "hop_count": None,
            "path": [],
            "sql_snippet": None,
            "tokens_used": _estimate_tokens(source_table + target_table),
        }

    path_steps = []
    joins = []
    prev = src
    for step in found_path:
        nxt = step["to"]
        info = step.get("info", {})
        on_clause = info.get("references", info.get("note", ""))
        join_type = "inner"
        path_steps.append(
            {"from_table": prev, "to_table": nxt, "join_type": join_type, "on_clause": on_clause}
        )
        joins.append(f"JOIN {nxt} ON {on_clause or '/* specify join condition */'}")
        prev = nxt

    sql_snippet = f"SELECT * FROM {src} " + " ".join(joins)
    return {
        "source": src,
        "target": tgt,
        "found": True,
        "hop_count": len(path_steps),
        "path": path_steps,
        "sql_snippet": sql_snippet,
        "tokens_used": _estimate_tokens(sql_snippet),
    }


@mcp.tool
def get_domain_overview(domain: str, database: str = "") -> Dict[str, Any]:
    """
    Get summary of all tables in a business domain.

    Args:
        domain: Domain name filter.
        database: Optional database filter.
    Returns:
        Domain description with tables and databases.
    """
    tables = []
    for seg in DB_SEGMENTS:
        if domain and seg.get("domain", "") != domain:
            continue
        if database and seg.get("database", "") != database:
            continue
        tables.append(
            {
                "name": seg["id"],
                "description": seg.get("summary", ""),
                "row_count": seg.get("row_count"),
            }
        )

    return {
        "domain": domain or "default",
        "description": f"Overview for domain '{domain or 'default'}'",
        "databases": sorted({seg.get("database", "default") for seg in DB_SEGMENTS}),
        "tables": tables,
        "er_diagram": None,
        "common_joins": [],
        "tokens_used": _estimate_tokens(domain),
    }


@mcp.tool
def list_domains(database: str = "") -> Dict[str, Any]:
    """
    List all available business domains.

    Args:
        database: Optional database filter.
    Returns:
        Domain list with counts and databases.
    """
    domains: DefaultDict[str, Dict[str, Any]] = defaultdict(
        lambda: {"name": "", "description": "", "table_count": 0, "databases": set()}
    )
    for seg in DB_SEGMENTS:
        if database and seg.get("database", "") != database:
            continue
        dom = seg.get("domain", "default")
        domains[dom]["name"] = dom
        domains[dom]["description"] = f"Tables under domain '{dom}'"
        domains[dom]["table_count"] += 1
        domains[dom]["databases"].add(seg.get("database", "default"))

    return {
        "domains": [
            {
                "name": dom["name"],
                "description": dom["description"],
                "table_count": dom["table_count"],
                "databases": sorted(list(dom["databases"])),
            }
            for dom in domains.values()
        ],
        "tokens_used": _estimate_tokens(database),
    }


@mcp.tool
def list_databases() -> Dict[str, Any]:
    """
    List all available databases in the index.
    Use this to discover what databases exist before querying specific tables.

    Returns:
        Dict with list of databases, each containing name, table_count, domains, and schemas.
    """
    databases: DefaultDict[str, Dict[str, Any]] = defaultdict(
        lambda: {"name": "", "table_count": 0, "domains": set(), "schemas": set()}
    )
    
    for seg in DB_SEGMENTS:
        db_name = seg.get("database", "default")
        databases[db_name]["name"] = db_name
        databases[db_name]["table_count"] += 1
        if seg.get("domain"):
            databases[db_name]["domains"].add(seg["domain"])
        if seg.get("schema"):
            databases[db_name]["schemas"].add(seg["schema"])
    
    return {
        "databases": [
            {
                "name": db["name"],
                "table_count": db["table_count"],
                "domains": sorted(list(db["domains"])),
                "schemas": sorted(list(db["schemas"])),
            }
            for db in sorted(databases.values(), key=lambda x: x["name"])
        ],
    }


@mcp.tool
def get_common_relationships(
    database: str = "", domain: str = "", limit: int = 10
) -> Dict[str, Any]:
    """
    Retrieve frequently used join patterns based on foreign keys.

    Args:
        database: Optional database filter.
        domain: Optional domain filter.
        limit: Max relationships to return.
    Returns:
        List of join patterns with SQL templates.
    """
    limit = max(1, limit)
    relationships = []
    for seg in DB_SEGMENTS:
        if database and seg.get("database", "") != database:
            continue
        if domain and seg.get("domain", "") != domain:
            continue
        for fk in seg.get("keys", {}).get("foreign", []) or []:
            ref = fk.get("references", "")
            ref_table = ref.split("(")[0] if "(" in ref else ref
            join_sql = f"{seg['id']} JOIN {ref_table} ON {ref}"
            relationships.append(
                {
                    "source_table": seg["id"],
                    "target_table": ref_table,
                    "join_sql": join_sql,
                    "description": "Foreign key relationship",
                }
            )

    return {"relationships": relationships[:limit], "tokens_used": _estimate_tokens(database + domain)}


# --- SQL Generation and Execution Tools ---

SQL_SERVICE_AVAILABLE = False
SQL_SERVICE_ERROR = None

try:
    from sql_service import generate_and_execute_sql, _sql_generator, _sql_executor
    # Verify the service is actually functional
    if _sql_generator.client is None:
        SQL_SERVICE_AVAILABLE = False
        SQL_SERVICE_ERROR = "OpenRouter API key not configured. Set OPENROUTER_API_KEY environment variable."
        print(f"[MCP Server] SQL service imported but not configured: {SQL_SERVICE_ERROR}")
    else:
        SQL_SERVICE_AVAILABLE = True
        SQL_SERVICE_ERROR = None
        print("[MCP Server] SQL service loaded successfully")
except ImportError as e:
    SQL_SERVICE_AVAILABLE = False
    SQL_SERVICE_ERROR = f"Could not import sql_service: {e}. Make sure sql_service.py exists and dependencies are installed."
    print(f"[MCP Server] SQL service import failed: {e}")
except Exception as e:
    SQL_SERVICE_AVAILABLE = False
    SQL_SERVICE_ERROR = f"SQL service initialization error: {e}"
    print(f"[MCP Server] SQL service initialization error: {e}")


@mcp.tool
def generate_sql(
    query: str,
    database: str = "",
    context_tables: List[str] = []
) -> Dict[str, Any]:
    """
    Generate SQL query from natural language question using schema context.
    
    Args:
        query: Natural language question (e.g., "How many customers do I have?")
        database: Target database (postgres_production or snowflake_production). Auto-detected if not specified.
        context_tables: Optional list of table names to include in schema context.
    
    Returns:
        Dict with generated SQL, schema_context used, and any errors.
        Note: SQL is generated but not executed. Use execute_sql() to run it.
    """
    if not SQL_SERVICE_AVAILABLE:
        error_msg = "SQL service not available. Check dependencies and configuration."
        if SQL_SERVICE_ERROR:
            error_msg += f" Error: {SQL_SERVICE_ERROR}"
        return {
            "error": error_msg,
            "sql": None,
            "schema_context": {}
        }
    
    # Auto-detect database if not specified
    if not database:
        # Try to infer from context_tables or query
        for seg in DB_SEGMENTS:
            if context_tables and seg["id"] in context_tables:
                database = seg.get("database", "")
                break
        if not database:
            # Default to postgres_production if available
            databases = {seg.get("database") for seg in DB_SEGMENTS if seg.get("database")}
            database = "postgres_production" if "postgres_production" in databases else list(databases)[0] if databases else ""
    
    if not database:
        return {
            "error": "Could not determine target database. Please specify database parameter.",
            "sql": None,
            "schema_context": {}
        }
    
    # Build schema context
    schema_context = {"database": database, "tables": []}
    
    # Find relevant tables
    if context_tables:
        for table_name in context_tables:
            seg = _find_table(table_name, database)
            if seg:
                table_info = {
                    "name": seg["id"],
                    "description": seg.get("summary", ""),
                    "columns": seg.get("columns", []),
                    "primary_key": seg.get("keys", {}).get("primary", []),
                    "foreign_keys": seg.get("keys", {}).get("foreign", [])
                }
                schema_context["tables"].append(table_info)
    else:
        # Auto-discover relevant tables from query
        # Use search to find relevant tables
        search_result = search_tables(query, database=database, limit=5)
        for table in search_result.get("tables", [])[:3]:  # Top 3 most relevant
            seg = _find_table(table["name"], database)
            if seg:
                table_info = {
                    "name": seg["id"],
                    "description": seg.get("summary", ""),
                    "columns": seg.get("columns", []),
                    "primary_key": seg.get("keys", {}).get("primary", []),
                    "foreign_keys": seg.get("keys", {}).get("foreign", [])
                }
                schema_context["tables"].append(table_info)
    
    if not schema_context["tables"]:
        return {
            "error": f"No relevant tables found for query. Database: {database}",
            "sql": None,
            "schema_context": schema_context
        }
    
    # Generate SQL
    sql, error = _sql_generator.generate_sql(query, schema_context, database)
    
    if error:
        return {
            "error": error,
            "sql": None,
            "schema_context": schema_context
        }
    
    return {
        "sql": sql,
        "schema_context": {
            "database": database,
            "table_count": len(schema_context["tables"]),
            "tables": [t["name"] for t in schema_context["tables"]]
        },
        "tokens_used": _estimate_tokens(query)
    }


@mcp.tool
def execute_sql(
    sql: str,
    database: str,
    limit: int = 10000
) -> Dict[str, Any]:
    """
    Execute a SQL query against the specified database.
    
    Args:
        sql: SQL query to execute (must be read-only SELECT query)
        database: Target database (postgres_production or snowflake_production)
        limit: Maximum rows to return (default 10000, max 10000)
    
    Returns:
        Dict with success status, data (rows), columns, row_count, and any errors.
    """
    if not SQL_SERVICE_AVAILABLE:
        error_msg = "SQL service not available. Check dependencies and configuration."
        if SQL_SERVICE_ERROR:
            error_msg += f" Error: {SQL_SERVICE_ERROR}"
        return {
            "success": False,
            "error": error_msg,
            "data": [],
            "columns": [],
            "row_count": 0
        }
    
    limit = max(1, min(limit, 10000))
    
    result = _sql_executor.execute_query(sql, database, limit)
    
    return result


@mcp.tool
def answer_question(
    question: str,
    database: str = ""
) -> Dict[str, Any]:
    """
    Answer a natural language question by generating and executing SQL.
    This is a convenience tool that combines generate_sql() and execute_sql().
    
    Args:
        question: Natural language question (e.g., "How many customers do I have?")
        database: Target database (postgres_production or snowflake_production). Auto-detected if not specified.
    
    Returns:
        Dict with success status, answer (formatted text), data (rows), columns, row_count, and any errors.
        Note: The generated SQL is not included in the response (hidden from user).
    """
    if not SQL_SERVICE_AVAILABLE:
        return {
            "success": False,
            "error": "SQL service not available. Check dependencies and configuration.",
            "answer": None,
            "data": [],
            "columns": [],
            "row_count": 0
        }
    
    # Valid database names
    VALID_DATABASES = {"postgres_production", "snowflake_production"}
    
    # Auto-detect database if not specified
    if not database:
        # Use search to find relevant tables
        search_result = search_tables(question, limit=5)
        for table in search_result.get("tables", []):
            seg = _find_table(table["name"])
            if seg and seg.get("database"):
                candidate_db = seg.get("database")
                # Only use if it's a valid database name (not a domain)
                if candidate_db in VALID_DATABASES:
                    database = candidate_db
                    break
        
        if not database:
            databases = {seg.get("database") for seg in DB_SEGMENTS if seg.get("database")}
            # Filter to only valid database names
            valid_found = [db for db in databases if db in VALID_DATABASES]
            database = "postgres_production" if "postgres_production" in valid_found else (valid_found[0] if valid_found else "")
    
    # Validate database name
    if database not in VALID_DATABASES:
        # Try to find the correct database by searching for tables
        search_result = search_tables(question, limit=10)
        for table in search_result.get("tables", []):
            seg = _find_table(table["name"])
            if seg and seg.get("database") in VALID_DATABASES:
                database = seg.get("database")
                break
        
        if database not in VALID_DATABASES:
            # Default to postgres_production if available
            databases = {seg.get("database") for seg in DB_SEGMENTS if seg.get("database")}
            if "postgres_production" in databases:
                database = "postgres_production"
            else:
                return {
                    "success": False,
                    "error": f"Invalid database name '{database}'. Valid databases are: {', '.join(VALID_DATABASES)}. Could not auto-detect correct database.",
                    "answer": None,
                    "data": [],
                    "columns": [],
                    "row_count": 0
                }
    
    if not database:
        return {
            "success": False,
            "error": "Could not determine target database. Please specify database parameter (postgres_production or snowflake_production).",
            "answer": None,
            "data": [],
            "columns": [],
            "row_count": 0
        }
    
    # Build schema context
    schema_context = {"database": database, "tables": []}
    
    # Find relevant tables
    search_result = search_tables(question, database=database, limit=5)
    for table in search_result.get("tables", [])[:3]:  # Top 3 most relevant
        seg = _find_table(table["name"], database)
        if seg:
            table_info = {
                "name": seg["id"],
                "description": seg.get("summary", ""),
                "columns": seg.get("columns", []),
                "primary_key": seg.get("keys", {}).get("primary", []),
                "foreign_keys": seg.get("keys", {}).get("foreign", [])
            }
            schema_context["tables"].append(table_info)
    
    if not schema_context["tables"]:
        return {
            "success": False,
            "error": f"No relevant tables found for question. Database: {database}",
            "answer": None,
            "data": [],
            "columns": [],
            "row_count": 0
        }
    
    # Generate and execute SQL
    result = generate_and_execute_sql(question, schema_context, database)
    
    if not result.get("success"):
        return {
            "success": False,
            "error": result.get("error", "Unknown error"),
            "answer": None,
            "data": [],
            "columns": [],
            "row_count": 0
        }
    
    # Format answer
    answer = _format_query_answer(question, result)
    
    # Get SQL from result (should be added by generate_and_execute_sql)
    sql = result.get("sql")
    
    return {
        "success": True,
        "answer": answer,
        "data": result.get("data", []),
        "columns": result.get("columns", []),
        "row_count": result.get("row_count", 0),
        "execution_time": result.get("execution_time", 0),
        "sql": sql  # Include generated SQL for UI display (may be None if SQL generation failed)
    }


def _format_query_answer(question: str, result: Dict[str, Any]) -> str:
    """Format query results into a natural language answer."""
    data = result.get("data", [])
    row_count = result.get("row_count", 0)
    
    if row_count == 0:
        return "No results found."
    
    # If single row with single column, return simple answer
    if row_count == 1 and len(result.get("columns", [])) == 1:
        value = data[0].get(result["columns"][0])
        return f"The answer is: {value}"
    
    # If single row, format as sentence
    if row_count == 1:
        row = data[0]
        parts = []
        for col in result.get("columns", []):
            value = row.get(col)
            parts.append(f"{col}: {value}")
        return ", ".join(parts)
    
    # Multiple rows - provide summary
    if "count" in question.lower() or "how many" in question.lower():
        # Count queries
        if row_count == 1 and len(result.get("columns", [])) == 1:
            return f"The answer is: {data[0].get(result['columns'][0])}"
        else:
            return f"Found {row_count} results."
    
    # General query with multiple rows
    return f"Found {row_count} results. Showing data below."


if __name__ == "__main__":
    # Bind to 0.0.0.0 for container networking; use HTTP transport for remote access.
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8000)
