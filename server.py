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

# Minimal FastMCP server with database-backed search tools.
mcp = FastMCP("Example Server")

BASE_DIR = Path(__file__).resolve().parent
CONTEXT_MAP_PATH = BASE_DIR / "_docs" / "map" / "context_map.json"
CONTEXT_INDEX_PATH = BASE_DIR / "_docs" / "map" / "context_index.json"
DB_PATH = BASE_DIR / "data" / "tribal-knowledge.db"

# OpenAI embedding configuration
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536

# Initialize OpenAI client if available
_openai_client: Optional["OpenAI"] = None
if HAS_OPENAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        _openai_client = OpenAI(api_key=api_key)


# Fallback context map so the server stays functional if JSON is missing or empty.
DEFAULT_CONTEXT_MAP: List[Dict[str, Any]] = [
    {
        "id": "dabstep_tasks",
        "title": "dabstep_tasks table",
        "summary": "Task definitions with difficulty level and optional question/answer/guidelines.",
        "database": "default",
        "domain": "tasks",
        "columns": [
            {"name": "TASK_ID", "type": "integer", "notes": "primary key"},
            {"name": "QUESTION", "type": "text", "notes": "nullable"},
            {"name": "ANSWER", "type": "text", "notes": "nullable"},
            {"name": "GUIDELINES", "type": "text", "notes": "nullable"},
            {"name": "LEVEL", "type": "text", "notes": "not null, e.g., easy/hard"},
        ],
        "keys": {
            "primary": ["TASK_ID"],
            "checks": ["LEVEL in ('easy','hard') (optional)"],
        },
        "relationships": {"referenced_by": ["dabstep_submissions.TASK_ID", "dabstep_task_scores.TASK_ID"]},
    },
    {
        "id": "dabstep_submissions",
        "title": "dabstep_submissions table",
        "summary": "Stores agent submissions per task with metadata and validation status.",
        "database": "default",
        "domain": "tasks",
        "columns": [
            {"name": "TASK_ID", "type": "integer", "notes": "FK -> dabstep_tasks.TASK_ID"},
            {"name": "AGENT_ANSWER", "type": "text", "notes": "nullable"},
            {"name": "SUBMISSION_ID", "type": "text", "notes": "primary key"},
            {"name": "AGENT_NAME", "type": "text", "notes": "not null"},
            {"name": "MODEL_FAMILY", "type": "integer", "notes": "not null"},
            {"name": "ORGANISATION", "type": "text", "notes": "nullable"},
            {"name": "REPO_URL", "type": "text", "notes": "nullable"},
            {"name": "DATE", "type": "text", "notes": "dd-mm-yyyy in sample"},
            {"name": "VALIDATED", "type": "boolean", "notes": "not null"},
        ],
        "keys": {
            "primary": ["SUBMISSION_ID"],
            "foreign": [{"columns": ["TASK_ID"], "references": "dabstep_tasks(TASK_ID)"}],
            "unique_optional": ["(TASK_ID, AGENT_NAME, ORGANISATION) to prevent duplicates"],
        },
        "relationships": {
            "depends_on": ["dabstep_tasks"],
            "referenced_by": ["dabstep_task_scores.SUBMISSION_ID"],
        },
    },
    {
        "id": "dabstep_task_scores",
        "title": "dabstep_task_scores table",
        "summary": "Scores for submissions per task, with level and optional agent answer copy.",
        "database": "default",
        "domain": "tasks",
        "columns": [
            {"name": "SUBMISSION_ID", "type": "text", "notes": "FK -> dabstep_submissions.SUBMISSION_ID"},
            {"name": "TASK_ID", "type": "integer", "notes": "FK -> dabstep_tasks.TASK_ID"},
            {"name": "SCORE", "type": "boolean", "notes": "not null"},
            {"name": "LEVEL", "type": "text", "notes": "not null, aligns with tasks"},
            {"name": "AGENT_ANSWER", "type": "text", "notes": "nullable"},
        ],
        "keys": {
            "primary": ["SUBMISSION_ID", "TASK_ID"],
            "foreign": [
                {"columns": ["SUBMISSION_ID"], "references": "dabstep_submissions(SUBMISSION_ID)"},
                {"columns": ["TASK_ID"], "references": "dabstep_tasks(TASK_ID)"},
            ],
        },
        "relationships": {"depends_on": ["dabstep_submissions", "dabstep_tasks"]},
    },
    {
        "id": "dabstep_payments",
        "title": "dabstep_payments table",
        "summary": "Payment events with merchant, card, timing, and fraud/refusal indicators.",
        "database": "default",
        "domain": "payments",
        "columns": [
            {"name": "PSP_REFERENCE", "type": "bigint", "notes": "primary key"},
            {"name": "MERCHANT", "type": "text", "notes": "not null"},
            {"name": "CARD_SCHEME", "type": "text", "notes": "not null"},
            {"name": "YEAR", "type": "integer", "notes": "not null"},
            {"name": "HOUR_OF_DAY", "type": "integer", "notes": "0-23"},
            {"name": "MINUTE_OF_HOUR", "type": "integer", "notes": "0-59"},
            {"name": "DAY_OF_YEAR", "type": "integer", "notes": "1-366"},
            {"name": "IS_CREDIT", "type": "boolean", "notes": "not null"},
            {"name": "EUR_AMOUNT", "type": "numeric", "notes": "currency amount"},
            {"name": "IP_COUNTRY", "type": "text", "notes": "2-letter"},
            {"name": "ISSUING_COUNTRY", "type": "text", "notes": "2-letter"},
            {"name": "DEVICE_TYPE", "type": "text", "notes": ""},
            {"name": "IP_ADDRESS", "type": "text", "notes": ""},
            {"name": "EMAIL_ADDRESS", "type": "text", "notes": ""},
            {"name": "CARD_NUMBER", "type": "text", "notes": ""},
            {"name": "SHOPPER_INTERACTION", "type": "text", "notes": "e.g., Ecommerce"},
            {"name": "CARD_BIN", "type": "integer", "notes": ""},
            {"name": "HAS_FRAUDULENT_DISPUTE", "type": "boolean", "notes": "not null"},
            {"name": "IS_REFUSED_BY_ADYEN", "type": "boolean", "notes": "not null"},
            {"name": "ACI", "type": "text", "notes": "single-letter code"},
            {"name": "ACQUIRER_COUNTRY", "type": "text", "notes": "2-letter"},
        ],
        "keys": {
            "primary": ["PSP_REFERENCE"],
            "checks": [
                "HOUR_OF_DAY between 0 and 23",
                "MINUTE_OF_HOUR between 0 and 59",
                "DAY_OF_YEAR between 1 and 366",
            ],
            "pii_columns": ["EMAIL_ADDRESS", "CARD_NUMBER", "IP_ADDRESS"],
        },
        "relationships": {"depends_on": []},
    },
]


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _safe_load_map() -> List[Dict[str, Any]]:
    try:
        data = _load_json(CONTEXT_MAP_PATH)
        if isinstance(data, list) and data:
            return data
    except FileNotFoundError:
        pass
    except Exception:
        pass
    # Fallback to embedded defaults if file missing or empty.
    return DEFAULT_CONTEXT_MAP.copy()


DB_SEGMENTS: List[Dict[str, Any]] = _safe_load_map()


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
    try:
        data = _load_json(CONTEXT_INDEX_PATH)
        if isinstance(data, dict):
            return {token: set(ids) for token, ids in data.items()}
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return _build_index(DB_SEGMENTS)


INDEX = _safe_load_index()
SEGMENT_BY_ID: Dict[str, Dict[str, Any]] = {seg["id"]: seg for seg in DB_SEGMENTS}


def _find_table(table: str) -> Dict[str, Any]:
    table_norm = table.lower()
    for seg in DB_SEGMENTS:
        if seg["id"].lower() == table_norm or seg.get("title", "").lower() == table_norm:
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


GRAPH = _build_graph()


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


@mcp.resource("resource://db-map")
def db_map() -> Dict[str, Any]:
    """Full database context map."""
    return {"segments": DB_SEGMENTS, "index_tokens": sorted(list(INDEX.keys()))}


@mcp.resource("resource://db-map/{segment_id}")
def db_map_segment(segment_id: str) -> Dict[str, Any]:
    """Fetch a single segment by id."""
    for seg in DB_SEGMENTS:
        if seg["id"] == segment_id:
            return seg
    return {"error": f"segment '{segment_id}' not found"}


@mcp.resource("resource://db-map-index")
def db_map_index() -> Dict[str, Any]:
    """
    Expose the inverted index so clients can inspect token->segment mappings.
    Useful for debugging and future smarter retrieval strategies.
    """
    return {"index": {token: sorted(list(ids)) for token, ids in INDEX.items()}}


# --- New FTS5 and Vector Search Tools ---

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
            result = {
                "id": row["id"],
                "doc_type": row["doc_type"],
                "database": row["database_name"],
                "table_name": row["table_name"],
                "column_name": row["column_name"],
                "domain": row["domain"],
                "summary": row["summary"],
                "content_preview": row["content"][:200] + "..." if len(row["content"]) > 200 else row["content"],
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
            result = {
                "id": row["id"],
                "doc_type": row["doc_type"],
                "database": row["database_name"],
                "table_name": row["table_name"],
                "column_name": row["column_name"],
                "domain": row["domain"],
                "summary": row["summary"],
                "content_preview": row["content"][:200] + "..." if len(row["content"]) > 200 else row["content"],
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
            filters = ["doc_type = 'table'"]
            params: List[Any] = []
            
            if database:
                filters.append("database_name = ?")
                params.append(database)
            if domain:
                filters.append("domain = ?")
                params.append(domain)
            
            filter_clause = " AND ".join(filters)
            
            cursor = db.execute(f"""
                SELECT id, table_name, database_name, domain, summary
                FROM documents
                WHERE {filter_clause}
            """, params)
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "name": row["table_name"],
                    "title": f"{row['table_name']} table",
                    "database": row["database_name"],
                    "domain": row["domain"],
                    "summary": row["summary"],
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
def list_columns(table: str) -> Dict[str, Any]:
    """
    List columns for a given table id/title.

    Args:
        table: Table id or title.
    Returns:
        Dict with table id and column metadata or an error.
    """
    # Try database first
    db = _get_db_connection()
    if db:
        try:
            cursor = db.execute("""
                SELECT column_name, summary as description, content
                FROM documents
                WHERE doc_type = 'column' AND table_name = ?
            """, (table,))
            
            rows = cursor.fetchall()
            if rows:
                columns = []
                for row in rows:
                    # Parse type from content if available
                    content = row["content"] or ""
                    type_match = re.search(r"Type:\s*(\w+)", content)
                    col_type = type_match.group(1) if type_match else "unknown"
                    
                    columns.append({
                        "name": row["column_name"],
                        "type": col_type,
                        "description": row["description"],
                    })
                
                db.close()
                return {"table": table, "columns": columns}
            
            db.close()
        except Exception:
            db.close()
    
    # Fallback to in-memory segments
    seg = _find_table(table)
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
def get_table_schema(table: str, include_samples: bool = False) -> Dict[str, Any]:
    """
    Retrieve full schema details for a specific table.

    Args:
        table: Table id or title.
        include_samples: Reserved flag to include sample values.
    Returns:
        Schema details including columns, keys, relationships, or an error.
    """
    seg = _find_table(table)
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
    source_table: str, target_table: str, max_hops: int = 3
) -> Dict[str, Any]:
    """
    Find the join path between two tables using relationship graph traversal.

    Args:
        source_table: Starting table id/title.
        target_table: Destination table id/title.
        max_hops: Maximum graph hops to explore.
    Returns:
        Dict indicating whether a path was found and a SQL join snippet.
    """
    src = _find_table(source_table).get("id")
    tgt = _find_table(target_table).get("id")
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


# --- Placeholder tools for planned data tooling. Implementations are stubs. ---


@mcp.tool
def get_table_samples(table: str, where: str = "", limit: int = 20) -> Dict[str, Any]:
    """
    Placeholder: return sample rows for a table with optional filter.

    Args:
        table: Table id/title.
        where: Optional filter expression.
        limit: Max rows to return.
    Returns:
        Not-implemented message.
    """
    return {"error": "get_table_samples not implemented", "table": table, "limit": limit, "where": where}


@mcp.tool
def get_table_stats(table: str, time_column: str = "", group_by: str = "") -> Dict[str, Any]:
    """
    Placeholder: basic profiling stats for a table.

    Args:
        table: Table id/title.
        time_column: Optional time column for windowed stats.
        group_by: Optional grouping column.
    Returns:
        Not-implemented message.
    """
    return {
        "error": "get_table_stats not implemented",
        "table": table,
        "time_column": time_column,
        "group_by": group_by,
    }


@mcp.tool
def get_column_stats(table: str, column: str) -> Dict[str, Any]:
    """
    Placeholder: distribution/profile stats for a specific column.

    Args:
        table: Table id/title.
        column: Column name to profile.
    Returns:
        Not-implemented message.
    """
    return {"error": "get_column_stats not implemented", "table": table, "column": column}


@mcp.tool
def run_query(query: str, limit: int = 1000, timeout_seconds: int = 30) -> Dict[str, Any]:
    """
    Placeholder: execute a read-only SQL query with safety guards.

    Args:
        query: SQL text.
        limit: Max rows to return.
        timeout_seconds: Query timeout seconds.
    Returns:
        Not-implemented message.
    """
    return {
        "error": "run_query not implemented",
        "limit": limit,
        "timeout_seconds": timeout_seconds,
        "query_preview": query[:200],
    }


@mcp.tool
def explain_query(query: str) -> Dict[str, Any]:
    """
    Placeholder: provide an execution plan for a SQL query.

    Args:
        query: SQL text to explain.
    Returns:
        Not-implemented message.
    """
    return {"error": "explain_query not implemented", "query_preview": query[:200]}


@mcp.tool
def find_relationships(table: str) -> Dict[str, Any]:
    """
    Placeholder: auto-detect FK-like relationships for a table.

    Args:
        table: Table id/title.
    Returns:
        Not-implemented message.
    """
    return {"error": "find_relationships not implemented", "table": table}


@mcp.tool
def time_column_detection(table: str) -> Dict[str, Any]:
    """
    Placeholder: suggest timestamp/date columns and default grains.

    Args:
        table: Table id/title.
    Returns:
        Not-implemented message.
    """
    return {"error": "time_column_detection not implemented", "table": table}


@mcp.tool
def semantic_describe_table(table: str) -> Dict[str, Any]:
    """
    Placeholder: summarize table semantics using metadata and samples.

    Args:
        table: Table id/title.
    Returns:
        Not-implemented message.
    """
    return {"error": "semantic_describe_table not implemented", "table": table}


@mcp.tool
def semantic_describe_column(table: str, column: str) -> Dict[str, Any]:
    """
    Placeholder: summarize column meaning using metadata and samples.

    Args:
        table: Table id/title.
        column: Column name.
    Returns:
        Not-implemented message.
    """
    return {"error": "semantic_describe_column not implemented", "table": table, "column": column}


@mcp.tool
def anomaly_scan(table: str, metric: str, time_column: str = "") -> Dict[str, Any]:
    """
    Placeholder: simple anomaly scan over a metric (optionally over time).

    Args:
        table: Table id/title.
        metric: Metric column to scan.
        time_column: Optional time column.
    Returns:
        Not-implemented message.
    """
    return {
        "error": "anomaly_scan not implemented",
        "table": table,
        "metric": metric,
        "time_column": time_column,
    }


@mcp.tool
def data_freshness(table: str) -> Dict[str, Any]:
    """
    Placeholder: report last ingested timestamp and freshness SLA for a table.

    Args:
        table: Table id/title.
    Returns:
        Not-implemented message.
    """
    return {"error": "data_freshness not implemented", "table": table}


@mcp.tool
def metric_definition_lookup(name: str) -> Dict[str, Any]:
    """
    Placeholder: retrieve canonical metric definition by name.

    Args:
        name: Metric name to look up.
    Returns:
        Not-implemented message.
    """
    return {"error": "metric_definition_lookup not implemented", "name": name}


@mcp.tool
def export_results(format: str = "csv") -> Dict[str, Any]:
    """
    Placeholder: export last query results to a file format.

    Args:
        format: Output format (e.g., csv, parquet).
    Returns:
        Not-implemented message.
    """
    return {"error": "export_results not implemented", "format": format}


@mcp.tool
def paginate_samples(page: int = 1, page_size: int = 50) -> Dict[str, Any]:
    """
    Placeholder: paginate over sample/result sets.

    Args:
        page: Page number (1-based).
        page_size: Number of rows per page.
    Returns:
        Not-implemented message.
    """
    return {"error": "paginate_samples not implemented", "page": page, "page_size": page_size}


if __name__ == "__main__":
    # Bind to 0.0.0.0 for container networking; use HTTP transport for remote access.
    mcp.run(transport="http", host="0.0.0.0", port=8000)
