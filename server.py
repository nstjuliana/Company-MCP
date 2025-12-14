from fastmcp import FastMCP
import json
import os
import re
import sqlite3
import sys
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

BASE_DIR = Path(__file__).resolve().parent

# OpenAI embedding configuration
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536

# Initialize OpenAI client if available
_openai_client: Optional["OpenAI"] = None
if HAS_OPENAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        _openai_client = OpenAI(api_key=api_key)


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


class MCPServerInstance:
    """
    Encapsulates all state and helper functions for a single MCP instance.
    Each instance operates on its own data directory with index and map subdirectories.
    """
    
    def __init__(self, name: str, data_dir: Path):
        self.name = name
        self.data_dir = data_dir
        self.map_path = data_dir / "map"
        self.db_path = data_dir / "index" / "index.db"
        
        # Initialize data structures
        self.db_segments: List[Dict[str, Any]] = []
        self.index: Dict[str, Set[str]] = {}
        self.segment_by_id: Dict[str, Dict[str, Any]] = {}
        self.graph: Dict[str, List[Dict[str, Any]]] = {}
        
        # Load data
        self._initialize()
    
    def _get_db_connection(self) -> Optional[sqlite3.Connection]:
        """Get a connection to the SQLite database."""
        if not self.db_path.exists():
            return None
        
        db = sqlite3.connect(str(self.db_path))
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

    def _load_json(self, path: Path) -> Any:
        """Load JSON from a file path."""
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _db_path_to_file_path(self, db_path: str) -> Path:
        """
        Translate a database file_path to an actual filesystem path.
        DB stores: databases/postgres_production/domains/...
        Actual:    data/<mcp>/map/postgres_production/domains/...
        """
        if db_path.startswith("databases/"):
            relative = db_path[len("databases/"):]
        else:
            relative = db_path
        return self.map_path / relative

    def _load_map_file(self, db_path: str) -> Optional[Dict[str, Any]]:
        """Load a JSON file from data/map given a database file_path."""
        try:
            file_path = self._db_path_to_file_path(db_path)
            if file_path.exists() and file_path.suffix == ".json":
                return self._load_json(file_path)
        except Exception:
            pass
        return None

    def _safe_load_map(self) -> List[Dict[str, Any]]:
        """Load table segments from index.db database."""
        db = self._get_db_connection()
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
                    content = json.loads(row["content"]) if row["content"] else {}
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

    def _normalize(self, text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    def _segment_tokens(self, seg: Dict[str, Any]) -> Set[str]:
        text_parts = [
            seg.get("id", ""),
            seg.get("title", ""),
            seg.get("summary", ""),
            seg.get("database", ""),
            seg.get("domain", ""),
            " ".join(col.get("name", "") for col in seg.get("columns", [])),
        ]
        return set(self._normalize(" ".join(text_parts)))

    def _build_index(self, segments: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
        """Build a lightweight inverted index: token -> set(segment_ids)."""
        index: DefaultDict[str, Set[str]] = defaultdict(set)
        for seg in segments:
            for token in self._segment_tokens(seg):
                index[token].add(seg["id"])
        return dict(index)

    def _foreign_key_edges(self, seg: Dict[str, Any]) -> List[Dict[str, Any]]:
        edges = []
        for fk in seg.get("keys", {}).get("foreign", []) or []:
            ref = fk.get("references", "")
            ref_table = ref.split("(")[0] if "(" in ref else ref
            edges.append({
                "from": seg["id"],
                "to": ref_table,
                "columns": fk.get("columns", []),
                "references": ref,
            })
        return edges

    def _build_graph(self) -> Dict[str, List[Dict[str, Any]]]:
        graph: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        for seg in self.db_segments:
            for edge in self._foreign_key_edges(seg):
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

    def _initialize(self):
        """Initialize all data structures."""
        self.db_segments = self._safe_load_map()
        self.index = self._build_index(self.db_segments)
        self.segment_by_id = {seg["id"]: seg for seg in self.db_segments}
        self.graph = self._build_graph()

    def _find_table(self, table: str, database: str = "") -> Dict[str, Any]:
        """Find a table segment by name (flexible matching), optionally filtered by database."""
        table_clean = table
        if table_clean.endswith(".json"):
            table_clean = table_clean[:-5]
        table_norm = table_clean.lower()
        
        segments = self.db_segments
        if database:
            segments = [s for s in self.db_segments if s.get("database") == database]
        
        for seg in segments:
            if seg["id"].lower() == table_norm:
                return seg
        
        for seg in segments:
            if seg.get("title", "").lower() == f"{table_norm} table":
                return seg
        
        for seg in segments:
            if table_norm in seg["id"].lower():
                return seg
        
        return {}

    def _estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4)


def create_mcp_server(instance: MCPServerInstance) -> FastMCP:
    """
    Factory function to create a FastMCP server for a given MCPServerInstance.
    """
    mcp = FastMCP(f"{instance.name} Database Context Server")

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
        q_tokens = set(instance._normalize(query))
        candidate_ids: Set[str] = set()

        for token in q_tokens:
            candidate_ids |= instance.index.get(token, set())

        if not candidate_ids:
            candidate_ids = {seg["id"] for seg in instance.db_segments}

        scored = []
        for seg in instance.db_segments:
            if seg["id"] not in candidate_ids:
                continue
            text_parts = [
                seg.get("id", ""),
                seg.get("title", ""),
                seg.get("summary", ""),
                " ".join(col["name"] for col in seg.get("columns", [])),
            ]
            seg_tokens = set(instance._normalize(" ".join(text_parts)))
            score = len(q_tokens & seg_tokens)
            scored.append({
                "id": seg["id"],
                "title": seg["title"],
                "score": score,
                "snippet": seg["summary"],
            })

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
        
        db = instance._get_db_connection()
        if not db:
            return {
                "error": "Database not found. Run setup_db.py first.",
                "results": [],
                "tokens_used": 0,
            }
        
        try:
            fts_query = query
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
                file_path = row["file_path"]
                actual_path = str(instance._db_path_to_file_path(file_path)) if file_path else None
                
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
                "tokens_used": instance._estimate_tokens(query + str(results)),
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
        
        db = instance._get_db_connection()
        if not db:
            return {
                "error": "Database not found. Run setup_db.py first.",
                "results": [],
                "tokens_used": 0,
            }
        
        try:
            query_embedding = _generate_query_embedding(query)
            if not query_embedding:
                db.close()
                return {
                    "error": "Failed to generate query embedding.",
                    "results": [],
                    "tokens_used": 0,
                }
            
            embedding_json = json.dumps(query_embedding)
            
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
                params = [embedding_json, limit * 2] + params
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
            for row in rows[:limit]:
                file_path = row["file_path"]
                actual_path = str(instance._db_path_to_file_path(file_path)) if file_path else None
                
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
                "tokens_used": instance._estimate_tokens(query + str(results)),
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

    # --- PRD2 tools ---

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
        db = instance._get_db_connection()
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
                        "file_path": str(instance._db_path_to_file_path(row["file_path"])),
                    })
                
                db.close()
                return results
            except Exception:
                db.close()
        
        results = []
        for seg in instance.db_segments:
            if database and seg.get("database", "") != database:
                continue
            if domain and seg.get("domain", "") != domain:
                continue
            results.append({
                "name": seg["id"],
                "title": seg.get("title", seg["id"]),
                "database": seg.get("database", "default"),
                "domain": seg.get("domain", "default"),
                "summary": seg.get("summary", ""),
                "key_columns": seg.get("keys", {}).get("primary", []),
            })
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
        db = instance._get_db_connection()
        if db:
            try:
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
                    json_content = instance._load_map_file(row["file_path"])
                    if json_content and "columns" in json_content:
                        columns = []
                        for col in json_content["columns"]:
                            columns.append({
                                "name": col.get("name"),
                                "type": col.get("type"),
                                "nullable": col.get("nullable", True),
                                "description": col.get("description", ""),
                            })
                        table_name = row["table_name"]
                        if table_name.endswith(".json"):
                            table_name = table_name[:-5]
                        
                        return {
                            "table": table_name,
                            "columns": columns,
                            "file_path": str(instance._db_path_to_file_path(row["file_path"])),
                        }
            except Exception:
                if db:
                    db.close()
        
        seg = instance._find_table(table, database)
        if not seg:
            return {"error": f"table '{table}' not found"}
        columns = []
        for col in seg.get("columns", []):
            columns.append({
                "name": col.get("name"),
                "type": col.get("type"),
                "nullable": "not null" not in (col.get("notes", "") or "").lower(),
                "description": col.get("notes", ""),
            })
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
        q_tokens = set(instance._normalize(query))
        scored = []
        for seg in instance.db_segments:
            if database and seg.get("database", "") != database:
                continue
            if domain and seg.get("domain", "") != domain:
                continue
            seg_tokens = instance._segment_tokens(seg)
            overlap = len(q_tokens & seg_tokens)
            text_blob = " ".join(
                [seg.get("id", ""), seg.get("title", ""), seg.get("summary", "")]
            ).lower()
            if any(tok in text_blob for tok in q_tokens):
                overlap += 0.5
            scored.append({
                "name": seg["id"],
                "database": seg.get("database", "default"),
                "domain": seg.get("domain", "default"),
                "summary": seg.get("summary", ""),
                "key_columns": seg.get("keys", {}).get("primary", []),
                "relevance_score": round(overlap, 3),
            })

        scored.sort(key=lambda x: x["relevance_score"], reverse=True)
        results = scored[:limit]
        return {
            "tables": results,
            "tokens_used": instance._estimate_tokens(query),
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
        db = instance._get_db_connection()
        if db:
            try:
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
                    json_content = instance._load_map_file(row["file_path"])
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
                            "file_path": str(instance._db_path_to_file_path(row["file_path"])),
                            "tokens_used": instance._estimate_tokens(json_content.get("description", "")),
                        }
            except Exception:
                if db:
                    db.close()
        
        seg = instance._find_table(table, database)
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
            "tokens_used": instance._estimate_tokens(seg.get("summary", "")),
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
        src = instance._find_table(source_table, database).get("id")
        tgt = instance._find_table(target_table, database).get("id")
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
            for edge in instance.graph.get(node, []):
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
                "tokens_used": instance._estimate_tokens(source_table + target_table),
            }

        path_steps = []
        joins = []
        prev = src
        for step in found_path:
            nxt = step["to"]
            info = step.get("info", {})
            on_clause = info.get("references", info.get("note", ""))
            join_type = "inner"
            path_steps.append({
                "from_table": prev, "to_table": nxt, "join_type": join_type, "on_clause": on_clause
            })
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
            "tokens_used": instance._estimate_tokens(sql_snippet),
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
        for seg in instance.db_segments:
            if domain and seg.get("domain", "") != domain:
                continue
            if database and seg.get("database", "") != database:
                continue
            tables.append({
                "name": seg["id"],
                "description": seg.get("summary", ""),
                "row_count": seg.get("row_count"),
            })

        return {
            "domain": domain or "default",
            "description": f"Overview for domain '{domain or 'default'}'",
            "databases": sorted({seg.get("database", "default") for seg in instance.db_segments}),
            "tables": tables,
            "er_diagram": None,
            "common_joins": [],
            "tokens_used": instance._estimate_tokens(domain),
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
        for seg in instance.db_segments:
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
            "tokens_used": instance._estimate_tokens(database),
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
        
        for seg in instance.db_segments:
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
        for seg in instance.db_segments:
            if database and seg.get("database", "") != database:
                continue
            if domain and seg.get("domain", "") != domain:
                continue
            for fk in seg.get("keys", {}).get("foreign", []) or []:
                ref = fk.get("references", "")
                ref_table = ref.split("(")[0] if "(" in ref else ref
                join_sql = f"{seg['id']} JOIN {ref_table} ON {ref}"
                relationships.append({
                    "source_table": seg["id"],
                    "target_table": ref_table,
                    "join_sql": join_sql,
                    "description": "Foreign key relationship",
                })

        return {"relationships": relationships[:limit], "tokens_used": instance._estimate_tokens(database + domain)}

    return mcp


def get_available_mcps() -> List[str]:
    """Return list of available MCP names from data directory."""
    data_dir = BASE_DIR / "data"
    mcps = []
    
    if data_dir.exists():
        for item in sorted(data_dir.iterdir()):
            if item.is_dir():
                has_index = (item / "index").exists()
                has_map = (item / "map").exists()
                if has_index or has_map:
                    mcps.append(item.name)
    
    return mcps


def create_mcp_for_name(name: str) -> FastMCP:
    """Create an MCP server for a specific data directory name."""
    data_dir = BASE_DIR / "data" / name
    if not data_dir.exists():
        raise ValueError(f"MCP data directory not found: {data_dir}")
    
    instance = MCPServerInstance(name, data_dir)
    return create_mcp_server(instance)


if __name__ == "__main__":
    # Get MCP name from command line argument or environment variable
    mcp_name = None
    
    if len(sys.argv) > 1:
        mcp_name = sys.argv[1]
    else:
        mcp_name = os.getenv("MCP_NAME")
    
    if not mcp_name:
        available = get_available_mcps()
        print(f"Error: No MCP name specified.")
        print(f"Usage: python server.py <mcp_name>")
        print(f"   or: MCP_NAME=<mcp_name> python server.py")
        print(f"Available MCPs: {available}")
        sys.exit(1)
    
    # Get port from environment variable (default 8000)
    port = int(os.getenv("MCP_PORT", "8000"))
    
    print(f"Starting MCP server '{mcp_name}' on port {port}...")
    mcp = create_mcp_for_name(mcp_name)
    mcp.run(transport="http", host="0.0.0.0", port=port)
