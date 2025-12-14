"""
Database Context MCP Chatbot Web Interface

A Flask web application that provides a chatbot interface for interacting
with the Database Context MCP server.
"""

import json
import os
import asyncio
import logging
from flask import Flask, render_template_string, request, jsonify, session
from flask_cors import CORS
from typing import Dict, Any, List, Optional
import re
import sys
import uuid

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Import AI agent and context manager
try:
    # Add chatbot directory to path if needed
    chatbot_dir = os.path.dirname(os.path.abspath(__file__))
    if chatbot_dir not in sys.path:
        sys.path.insert(0, chatbot_dir)
    
    from ai_agent import ai_agent
    from context_manager import conversation_manager
    AI_AGENT_AVAILABLE = True
    logger.info("AI agent and context manager loaded successfully")
except ImportError as e:
    logger.warning(f"AI agent not available: {e}")
    import traceback
    traceback.print_exc()
    AI_AGENT_AVAILABLE = False
    ai_agent = None
    conversation_manager = None

# Global variable to store import error message
MCP_IMPORT_ERROR = None

# Placeholder functions that will be overridden if MCP loads successfully
def list_databases():
    """Placeholder function - will be overridden."""
    return {"error": "Database functions not initialized"}

def list_domains(database: str = ""):
    """Placeholder function - will be overridden."""
    return {"error": "Database functions not initialized"}

def list_tables(database: str = "", domain: str = ""):
    """Placeholder function - will be overridden."""
    return {"error": "Database functions not initialized"}

def search_tables(query: str, database: str = "", domain: str = "", limit: int = 5):
    """Placeholder function - will be overridden."""
    return {"error": "Database functions not initialized"}

def get_table_schema(table: str, database: str = "", include_samples: bool = False):
    """Placeholder function - will be overridden."""
    return {"error": "Database functions not initialized"}

def add(a: float, b: float) -> float:
    """Add two numbers. Will be overridden if MCP loads successfully."""
    return a + b

def echo(message: str) -> str:
    """Echo a message. Will be overridden if MCP loads successfully."""
    return message

# Import MCP server data and functions directly for local execution
try:
    # Import the MCP server data and helper functions directly
    # Try Docker path first, then current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if '/app' not in sys.path:
        sys.path.insert(0, '/app')  # Docker path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)  # Local path
    
    from server import (
        DB_SEGMENTS, INDEX, SEGMENT_BY_ID, GRAPH,
        _find_table, _estimate_tokens, _foreign_key_edges,
        _build_graph, _normalize, _segment_tokens, _build_index,
        _safe_load_map, _safe_load_index, _get_db_connection,
        _load_map_file, _db_path_to_file_path
    )
    
    # Try to import SQL functions directly from sql_service (bypasses server.py dependency on fastmcp)
    # First try from server (if available), then try direct import from sql_service
    try:
        from server import answer_question, generate_sql, execute_sql
        print("Successfully imported SQL functions from server")
    except (ImportError, AttributeError) as server_error:
        # If server import fails, try importing directly from sql_service
        # Add parent directory to path since web_app.py is in chatbot/ subdirectory
        try:
            import sys
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            from sql_service import generate_and_execute_sql, _sql_generator, _sql_executor
            from pathlib import Path
            import json
            import re
            
            # We need to implement the MCP tool wrappers ourselves
            def _normalize_sql(text: str) -> list:
                return re.findall(r"[a-z0-9]+", text.lower())
            
            def answer_question(question: str, database: str = ""):
                """Answer a natural language question by generating and executing SQL."""
                # Valid database names
                VALID_DATABASES = {"postgres_production", "snowflake_production"}
                
                if not database:
                    # Auto-detect database from question
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
                    logger.error(f"Invalid database name detected: '{database}'. Valid databases: {VALID_DATABASES}")
                    # Try to find the correct database by searching for tables
                    search_result = search_tables(question, limit=10)
                    for table in search_result.get("tables", []):
                        seg = _find_table(table["name"])
                        if seg and seg.get("database") in VALID_DATABASES:
                            database = seg.get("database")
                            logger.info(f"Corrected database to: {database}")
                            break
                    
                    if database not in VALID_DATABASES:
                        # Default to postgres_production if available
                        databases = {seg.get("database") for seg in DB_SEGMENTS if seg.get("database")}
                        if "postgres_production" in databases:
                            database = "postgres_production"
                            logger.info(f"Defaulting to postgres_production")
                        else:
                            return {
                                "success": False,
                                "error": f"Invalid database name '{database}'. Valid databases are: {', '.join(VALID_DATABASES)}. Could not auto-detect correct database.",
                                "answer": None,
                                "data": [],
                                "columns": [],
                                "row_count": 0,
                                "sql": None
                            }
                
                if not database:
                    return {
                        "success": False,
                        "error": "Could not determine target database. Please specify database parameter (postgres_production or snowflake_production).",
                        "answer": None,
                        "data": [],
                        "columns": [],
                        "row_count": 0,
                        "sql": None
                    }
                
                # Build schema context
                schema_context = {"database": database, "tables": []}
                logger.info(f"Searching for tables matching question: '{question}' in database: '{database}'")
                search_result = search_tables(question, database=database, limit=5)
                logger.debug(f"Search result: {len(search_result.get('tables', []))} tables found")
                
                # If no results with database filter, try without filter to see what's available
                if not search_result.get("tables"):
                    logger.warning(f"No tables found with database filter '{database}'. Trying search without database filter...")
                    search_result_no_filter = search_tables(question, limit=10)
                    logger.info(f"Found {len(search_result_no_filter.get('tables', []))} tables without database filter")
                    for table in search_result_no_filter.get("tables", [])[:5]:
                        logger.debug(f"  - Table: {table.get('name')}, Database: {table.get('database')}, Domain: {table.get('domain')}")
                
                for table in search_result.get("tables", [])[:3]:
                    logger.debug(f"Processing table: {table.get('name')} from database: {table.get('database')}")
                    seg = _find_table(table["name"], database)
                    if seg:
                        logger.debug(f"Found segment for table: {seg.get('id')}, database: {seg.get('database')}")
                        table_info = {
                            "name": seg["id"],
                            "description": seg.get("summary", ""),
                            "columns": seg.get("columns", []),
                            "primary_key": seg.get("keys", {}).get("primary", []),
                            "foreign_keys": seg.get("keys", {}).get("foreign", [])
                        }
                        schema_context["tables"].append(table_info)
                    else:
                        logger.warning(f"Could not find segment for table: {table.get('name')} in database: {database}")
                
                if not schema_context["tables"]:
                    # Try a more direct search for "merchants" table
                    logger.warning(f"No relevant tables found. Attempting direct search for 'merchants' table...")
                    merchants_seg = _find_table("merchants", database)
                    if merchants_seg:
                        logger.info(f"Found merchants table directly: {merchants_seg.get('id')}, database: {merchants_seg.get('database')}")
                        schema_context["tables"].append({
                            "name": merchants_seg["id"],
                            "description": merchants_seg.get("summary", ""),
                            "columns": merchants_seg.get("columns", []),
                            "primary_key": merchants_seg.get("keys", {}).get("primary", []),
                            "foreign_keys": merchants_seg.get("keys", {}).get("foreign", [])
                        })
                    else:
                        # List all available tables in this database for debugging
                        all_tables = [seg for seg in DB_SEGMENTS if seg.get("database") == database]
                        logger.error(f"No tables found. Available tables in database '{database}': {[t.get('id') for t in all_tables[:10]]}")
                        return {
                            "success": False,
                            "error": f"No relevant tables found for question in database '{database}'. Available tables: {', '.join([t.get('id') for t in all_tables[:5]])}",
                            "answer": None,
                            "data": [],
                            "columns": [],
                            "row_count": 0,
                            "sql": None
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
                        "row_count": 0,
                        "sql": result.get("sql")
                    }
                
                # Format answer
                data = result.get("data", [])
                row_count = result.get("row_count", 0)
                columns = result.get("columns", [])
                
                if row_count == 0:
                    answer = "No results found."
                elif row_count == 1 and len(columns) == 1:
                    answer = f"The answer is: {data[0].get(columns[0])}"
                elif row_count == 1:
                    row = data[0]
                    parts = [f"{col}: {row.get(col)}" for col in columns]
                    answer = ", ".join(parts)
                elif "count" in question.lower() or "how many" in question.lower():
                    answer = f"Found {row_count} results."
                else:
                    answer = f"Found {row_count} results. Showing data below."
                
                return {
                    "success": True,
                    "answer": answer,
                    "data": data,
                    "columns": columns,
                    "row_count": row_count,
                    "execution_time": result.get("execution_time", 0),
                    "sql": result.get("sql")
                }
            
            def generate_sql(query: str, database: str = "", context_tables: List[str] = []):
                """Generate SQL query from natural language question."""
                if not database:
                    for seg in DB_SEGMENTS:
                        if context_tables and seg["id"] in context_tables:
                            database = seg.get("database", "")
                            break
                    if not database:
                        databases = {seg.get("database") for seg in DB_SEGMENTS if seg.get("database")}
                        database = "postgres_production" if "postgres_production" in databases else list(databases)[0] if databases else ""
                
                if not database:
                    return {
                        "error": "Could not determine target database. Please specify database parameter.",
                        "sql": None,
                        "schema_context": {}
                    }
                
                schema_context = {"database": database, "tables": []}
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
                    search_result = search_tables(query, database=database, limit=5)
                    for table in search_result.get("tables", [])[:3]:
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
            
            def execute_sql(sql: str, database: str, limit: int = 10000):
                """Execute a SQL query against the specified database."""
                limit = max(1, min(limit, 10000))
                result = _sql_executor.execute_query(sql, database, limit)
                return result
            
            print("Successfully imported SQL functions directly from sql_service")
        except (ImportError, AttributeError) as sql_error:
            # Final fallback - provide error-returning functions
            print(f"Warning: Could not import SQL functions (server: {server_error}, sql_service: {sql_error})")
            def answer_question(question: str, database: str = ""):
                return {
                    "success": False,
                    "error": "SQL service not available. Check dependencies and configuration.",
                    "answer": None,
                    "data": [],
                    "columns": [],
                    "row_count": 0,
                    "sql": None
                }
            
            def generate_sql(query: str, database: str = "", context_tables: List[str] = []):
                return {
                    "error": "SQL service not available. Check dependencies and configuration.",
                    "sql": None,
                    "schema_context": {}
                }
            
            def execute_sql(sql: str, database: str, limit: int = 10000):
                return {
                    "success": False,
                    "error": "SQL service not available. Check dependencies and configuration.",
                    "data": [],
                    "columns": [],
                    "row_count": 0
                }
        
        # Explicitly assign to module namespace to ensure they're available
        import sys
        current_module = sys.modules[__name__]
        current_module.answer_question = answer_question
        current_module.generate_sql = generate_sql
        current_module.execute_sql = execute_sql

    # Full functionality available with MCP server
    def list_databases():
        """List all available databases in the index."""
        databases = {}
        for seg in DB_SEGMENTS:
            db_name = seg.get("database", "default")
            if db_name not in databases:
                databases[db_name] = {"name": db_name, "table_count": 0, "domains": set(), "schemas": set()}
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

    def list_domains(database: str = ""):
        """List all available business domains."""
        domains = {}
        for seg in DB_SEGMENTS:
            if database and seg.get("database", "") != database:
                continue
            dom = seg.get("domain", "default")
            if dom not in domains:
                domains[dom] = {"name": "", "description": "", "table_count": 0, "databases": set()}
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

    def list_tables(database: str = "", domain: str = ""):
        """List available tables, optionally filtered by database or domain."""
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
                    "key_columns": [],
                }
            )
        return results

    def search_tables(query: str, database: str = "", domain: str = "", limit: int = 5):
        """Find tables relevant to a natural language query."""
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
            # Light boost for substring matches
            text_blob = " ".join([seg.get("id", ""), seg.get("title", ""), seg.get("summary", "")]).lower()
            if any(tok in text_blob for tok in q_tokens):
                overlap += 0.5
            scored.append(
                {
                    "name": seg["id"],
                    "database": seg.get("database", "default"),
                    "domain": seg.get("domain", "default"),
                    "summary": seg.get("summary", ""),
                    "key_columns": [],
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

    def get_table_schema(table: str, database: str = "", include_samples: bool = False):
        """Retrieve full schema details for a specific table."""
        seg = _find_table(table, database)
        if not seg:
            return {"error": f"table '{table}' not found"}

        columns = []
        for col in seg.get("columns", []):
            col_entry = {
                "name": col.get("name"),
                "type": col.get("type"),
                "nullable": col.get("nullable", True),
                "description": col.get("description", ""),
            }
            if include_samples:
                col_entry["samples"] = col.get("sample_values", [])
            columns.append(col_entry)

        keys = seg.get("keys", {})
        foreign_keys = []
        for fk in keys.get("foreign", []):
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


    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    def echo(message: str) -> str:
        """Echo a message."""
        return message

    MCP_AVAILABLE = True
    print("Successfully loaded MCP server functions")

except ImportError as e:
    import traceback
    error_msg = str(e)
    error_details = traceback.format_exc()

    print("MCP server functions not available, loading data directly from JSON files...")

    # Load data directly from JSON files when MCP is not available
    try:
        from pathlib import Path

        # Load data directly from JSON files
        DATA_DIR = Path(__file__).parent.parent / "data" / "map"
        DB_SEGMENTS = []

        if DATA_DIR.exists():
            for json_file in DATA_DIR.rglob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Create segment from JSON data
                    table_name = json_file.stem
                    
                    # Path structure: data/map/{database}/domains/{domain}/tables/{table}.json
                    # So we need to extract database from the path correctly
                    rel_path = json_file.relative_to(DATA_DIR)
                    parts = rel_path.parts
                    
                    # First part is database (postgres_production, snowflake_production)
                    database = parts[0] if len(parts) > 0 else data.get("database", "default")
                    
                    # Find domain - should be after "domains" folder
                    domain = "default"
                    for i, part in enumerate(parts):
                        if part == "domains" and i + 1 < len(parts):
                            domain = parts[i + 1]
                            break
                    
                    # Prefer database from JSON if available
                    if data.get("database"):
                        database = data.get("database")

                    segment = {
                        "id": table_name,
                        "title": f"{table_name} table",
                        "summary": data.get("description", ""),
                        "database": database,
                        "domain": domain,
                        "schema": data.get("schema", "public"),
                        "columns": data.get("columns", []),
                        "keys": {
                            "primary": data.get("primary_key", []),
                            "foreign": data.get("foreign_keys", []),
                        },
                        "relationships": data.get("relationships", {}),
                        "row_count": data.get("row_count"),
                    }
                    DB_SEGMENTS.append(segment)
                    logger.debug(f"Loaded table {table_name} from database={database}, domain={domain}")
                except Exception as json_error:
                    print(f"Warning: Could not load {json_file}: {json_error}")
                    continue

        print(f"Successfully loaded {len(DB_SEGMENTS)} tables directly from JSON files!")

        # Define helper functions for direct data access
        def _normalize(text: str) -> list:
            return re.findall(r"[a-z0-9]+", text.lower())

        def _segment_tokens(seg: dict) -> set:
            text_parts = [
                seg.get("id", ""),
                seg.get("title", ""),
                seg.get("summary", ""),
                seg.get("database", ""),
                seg.get("domain", ""),
                " ".join(col.get("name", "") for col in seg.get("columns", [])),
            ]
            return set(_normalize(" ".join(text_parts)))

        def _estimate_tokens(text: str) -> int:
            return max(1, len(text) // 4)

        def _find_table(table: str, database: str = "") -> dict:
            table_clean = table
            if table_clean.endswith(".json"):
                table_clean = table_clean[:-5]
            table_norm = table_clean.lower()

            segments = DB_SEGMENTS
            if database:
                segments = [s for s in DB_SEGMENTS if s.get("database") == database]

            # Try exact match first
            for seg in segments:
                if seg["id"].lower() == table_norm:
                    return seg

            # Try partial match
            for seg in segments:
                if table_norm in seg["id"].lower():
                    return seg

            return {}

        # Define MCP tool functions using direct data access
        def list_databases():
            """List all available databases in the index."""
            databases = {}
            for seg in DB_SEGMENTS:
                db_name = seg.get("database", "default")
                if db_name not in databases:
                    databases[db_name] = {"name": db_name, "table_count": 0, "domains": set(), "schemas": set()}
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

        def list_domains(database: str = ""):
            """List all available business domains."""
            domains = {}
            for seg in DB_SEGMENTS:
                if database and seg.get("database", "") != database:
                    continue
                dom = seg.get("domain", "default")
                if dom not in domains:
                    domains[dom] = {"name": "", "description": "", "table_count": 0, "databases": set()}
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

        def list_tables(database: str = "", domain: str = ""):
            """List available tables, optionally filtered by database or domain."""
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
                        "key_columns": [],
                    }
                )
            return results

        def search_tables(query: str, database: str = "", domain: str = "", limit: int = 5):
            """Find tables relevant to a natural language query."""
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
                # Light boost for substring matches
                text_blob = " ".join([seg.get("id", ""), seg.get("title", ""), seg.get("summary", "")]).lower()
                if any(tok in text_blob for tok in q_tokens):
                    overlap += 0.5
                scored.append(
                    {
                        "name": seg["id"],
                        "database": seg.get("database", "default"),
                        "domain": seg.get("domain", "default"),
                        "summary": seg.get("summary", ""),
                        "key_columns": [],
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

        def get_table_schema(table: str, database: str = "", include_samples: bool = False):
            """Retrieve full schema details for a specific table."""
            seg = _find_table(table, database)
            if not seg:
                return {"error": f"table '{table}' not found"}

            columns = []
            for col in seg.get("columns", []):
                col_entry = {
                    "name": col.get("name"),
                    "type": col.get("type"),
                    "nullable": col.get("nullable", True),
                    "description": col.get("description", ""),
                }
                if include_samples:
                    col_entry["samples"] = col.get("sample_values", [])
                columns.append(col_entry)

            keys = seg.get("keys", {})
            foreign_keys = []
            for fk in keys.get("foreign", []):
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

        # Define add and echo functions - ensure they're module-level
        # These will override the placeholder functions defined earlier
        def _add_impl(a: float, b: float) -> float:
            """Add two numbers."""
            return a + b

        def _echo_impl(message: str) -> str:
            """Echo a message."""
            return message
        
        # Assign to module-level names to override placeholders
        import sys
        current_module = sys.modules[__name__]
        current_module.add = _add_impl
        current_module.echo = _echo_impl
        
        # Try to import SQL functions directly from sql_service (bypasses server.py)
        # Add parent directory to path since web_app.py is in chatbot/ subdirectory
        try:
            import sys
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            from sql_service import generate_and_execute_sql, _sql_generator, _sql_executor
            
            # Implement MCP tool wrappers
            def answer_question(question: str, database: str = ""):
                """Answer a natural language question by generating and executing SQL."""
                # Valid database names
                VALID_DATABASES = {"postgres_production", "snowflake_production"}
                
                if not database:
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
                    logger.error(f"Invalid database name detected: '{database}'. Valid databases: {VALID_DATABASES}")
                    # Try to find the correct database by searching for tables
                    search_result = search_tables(question, limit=10)
                    for table in search_result.get("tables", []):
                        seg = _find_table(table["name"])
                        if seg and seg.get("database") in VALID_DATABASES:
                            database = seg.get("database")
                            logger.info(f"Corrected database to: {database}")
                            break
                    
                    if database not in VALID_DATABASES:
                        # Default to postgres_production if available
                        databases = {seg.get("database") for seg in DB_SEGMENTS if seg.get("database")}
                        if "postgres_production" in databases:
                            database = "postgres_production"
                            logger.info(f"Defaulting to postgres_production")
                        else:
                            return {
                                "success": False,
                                "error": f"Invalid database name '{database}'. Valid databases are: {', '.join(VALID_DATABASES)}. Could not auto-detect correct database.",
                                "answer": None,
                                "data": [],
                                "columns": [],
                                "row_count": 0,
                                "sql": None
                            }
                
                if not database:
                    return {
                        "success": False,
                        "error": "Could not determine target database. Please specify database parameter (postgres_production or snowflake_production).",
                        "answer": None,
                        "data": [],
                        "columns": [],
                        "row_count": 0,
                        "sql": None
                    }
                
                schema_context = {"database": database, "tables": []}
                search_result = search_tables(question, database=database, limit=5)
                for table in search_result.get("tables", [])[:3]:
                    seg = _find_table(table["name"], database)
                    if seg:
                        schema_context["tables"].append({
                            "name": seg["id"],
                            "description": seg.get("summary", ""),
                            "columns": seg.get("columns", []),
                            "primary_key": seg.get("keys", {}).get("primary", []),
                            "foreign_keys": seg.get("keys", {}).get("foreign", [])
                        })
                
                if not schema_context["tables"]:
                    return {
                        "success": False,
                        "error": f"No relevant tables found. Database: {database}",
                        "answer": None,
                        "data": [],
                        "columns": [],
                        "row_count": 0,
                        "sql": None
                    }
                
                result = generate_and_execute_sql(question, schema_context, database)
                if not result.get("success"):
                    return {
                        "success": False,
                        "error": result.get("error", "Unknown error"),
                        "answer": None,
                        "data": [],
                        "columns": [],
                        "row_count": 0,
                        "sql": result.get("sql")
                    }
                
                # Format answer
                data = result.get("data", [])
                row_count = result.get("row_count", 0)
                columns = result.get("columns", [])
                
                if row_count == 0:
                    answer = "No results found."
                elif row_count == 1 and len(columns) == 1:
                    answer = f"The answer is: {data[0].get(columns[0])}"
                elif row_count == 1:
                    answer = ", ".join([f"{col}: {data[0].get(col)}" for col in columns])
                elif "count" in question.lower() or "how many" in question.lower():
                    answer = f"Found {row_count} results."
                else:
                    answer = f"Found {row_count} results."
                
                return {
                    "success": True,
                    "answer": answer,
                    "data": data,
                    "columns": columns,
                    "row_count": row_count,
                    "execution_time": result.get("execution_time", 0),
                    "sql": result.get("sql")
                }
            
            def generate_sql(query: str, database: str = "", context_tables: List[str] = []):
                """Generate SQL query from natural language question."""
                if not database:
                    databases = {seg.get("database") for seg in DB_SEGMENTS if seg.get("database")}
                    database = "postgres_production" if "postgres_production" in databases else list(databases)[0] if databases else ""
                
                if not database:
                    return {"error": "Could not determine database.", "sql": None, "schema_context": {}}
                
                schema_context = {"database": database, "tables": []}
                if context_tables:
                    for table_name in context_tables:
                        seg = _find_table(table_name, database)
                        if seg:
                            schema_context["tables"].append({
                                "name": seg["id"],
                                "description": seg.get("summary", ""),
                                "columns": seg.get("columns", []),
                                "primary_key": seg.get("keys", {}).get("primary", []),
                                "foreign_keys": seg.get("keys", {}).get("foreign", [])
                            })
                else:
                    search_result = search_tables(query, database=database, limit=5)
                    for table in search_result.get("tables", [])[:3]:
                        seg = _find_table(table["name"], database)
                        if seg:
                            schema_context["tables"].append({
                                "name": seg["id"],
                                "description": seg.get("summary", ""),
                                "columns": seg.get("columns", []),
                                "primary_key": seg.get("keys", {}).get("primary", []),
                                "foreign_keys": seg.get("keys", {}).get("foreign", [])
                            })
                
                if not schema_context["tables"]:
                    return {"error": f"No relevant tables found. Database: {database}", "sql": None, "schema_context": schema_context}
                
                sql, error = _sql_generator.generate_sql(query, schema_context, database)
                if error:
                    return {"error": error, "sql": None, "schema_context": schema_context}
                
                return {
                    "sql": sql,
                    "schema_context": {"database": database, "table_count": len(schema_context["tables"]), "tables": [t["name"] for t in schema_context["tables"]]},
                    "tokens_used": _estimate_tokens(query)
                }
            
            def execute_sql(sql: str, database: str, limit: int = 10000):
                """Execute a SQL query."""
                limit = max(1, min(limit, 10000))
                return _sql_executor.execute_query(sql, database, limit)
            
            print("SQL functions loaded directly from sql_service (fallback mode)")
        except Exception as sql_error:
            # Final fallback - error-returning functions
            print(f"Warning: Could not load SQL functions: {sql_error}")
            def answer_question(question: str, database: str = ""):
                return {
                    "success": False,
                    "error": "SQL service not available. Check dependencies and configuration.",
                    "answer": None,
                    "data": [],
                    "columns": [],
                    "row_count": 0,
                    "sql": None
                }
            
            def generate_sql(query: str, database: str = "", context_tables: List[str] = []):
                return {
                    "error": "SQL service not available. Check dependencies and configuration.",
                    "sql": None,
                    "schema_context": {}
                }
            
            def execute_sql(sql: str, database: str, limit: int = 10000):
                return {
                    "success": False,
                    "error": "SQL service not available. Check dependencies and configuration.",
                    "data": [],
                    "columns": [],
                    "row_count": 0
                }
        
        # Make SQL functions available at module level
        current_module.answer_question = answer_question
        current_module.generate_sql = generate_sql
        current_module.execute_sql = execute_sql

        MCP_AVAILABLE = True
        MCP_IMPORT_ERROR = None
        print("Basic database functionality is now available! (without MCP server)")

    except Exception as fallback_error:
        print(f"Warning: Could not load data directly from JSON files: {fallback_error}")

        # Provide helpful error messages for common issues
        if "fastmcp" in error_msg.lower():
            user_message = "Missing dependency 'fastmcp'. Your Python version (3.9.6) is too old. Consider upgrading to Python 3.10+ or using Docker. Basic functionality loaded from JSON files."
        elif "No module named" in error_msg:
            missing_module = error_msg.split("'")[1] if "'" in error_msg else "unknown"
            user_message = f"Missing Python module '{missing_module}'. Basic functionality loaded from JSON files instead."
        else:
            user_message = f"Could not import MCP server functions: {error_msg}. Basic functionality loaded from JSON files."

        print(f"INFO: {user_message}")
        MCP_IMPORT_ERROR = user_message
        MCP_AVAILABLE = True  # We have basic functionality

except Exception as e:
    import traceback
    error_details = traceback.format_exc()
    user_message = f"Error loading MCP server functions: {str(e)}"
    print(f"Warning: {user_message}")
    print(f"Error details: {error_details}")
    MCP_IMPORT_ERROR = user_message
    MCP_AVAILABLE = False
    
    # Define fallback SQL functions so they're always available
    def answer_question(question: str, database: str = ""):
        return {
            "success": False,
            "error": "SQL service not available. Check dependencies and configuration.",
            "answer": None,
            "data": [],
            "columns": [],
            "row_count": 0,
            "sql": None
        }
    
    def generate_sql(query: str, database: str = "", context_tables: List[str] = []):
        return {
            "error": "SQL service not available. Check dependencies and configuration.",
            "sql": None,
            "schema_context": {}
        }
    
    def execute_sql(sql: str, database: str, limit: int = 10000):
        return {
            "success": False,
            "error": "SQL service not available. Check dependencies and configuration.",
            "data": [],
            "columns": [],
            "row_count": 0
        }

# HTML template for the chatbot interface - ChatGPT-style design
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Context Assistant</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f4f4f5;
            --bg-tertiary: #e5e5e5;
            --text-primary: #0d0d0d;
            --text-secondary: #666666;
            --text-tertiary: #999999;
            --border-color: #e5e5e5;
            --user-bubble: #f4f4f4;
            --button-primary: #000000;
            --button-hover: #2d2d2d;
            --action-hover: #f4f4f5;
            --max-width: 768px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            height: 100%;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            display: flex;
            flex-direction: column;
            line-height: 1.5;
            font-size: 16px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* Header */
        .header {
            height: 52px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            background: var(--bg-primary);
            flex-shrink: 0;
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 4px;
            cursor: pointer;
            padding: 6px 8px;
            border-radius: 8px;
            transition: background 0.15s;
        }

        .header-left:hover {
            background: var(--action-hover);
        }

        .header-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-primary);
        }

        .header-dropdown {
            width: 16px;
            height: 16px;
            color: var(--text-secondary);
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .header-btn {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 12px;
            border: 1px solid var(--border-color);
            border-radius: 20px;
            background: var(--bg-primary);
            font-size: 14px;
            font-weight: 500;
            color: var(--text-primary);
            cursor: pointer;
            transition: background 0.15s;
        }

        .header-btn:hover {
            background: var(--action-hover);
        }

        .header-btn svg {
            width: 16px;
            height: 16px;
        }

        .header-icon-btn {
            width: 36px;
            height: 36px;
            border: none;
            background: transparent;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.15s;
            color: var(--text-secondary);
        }

        .header-icon-btn:hover {
            background: var(--action-hover);
        }

        .header-icon-btn svg {
            width: 20px;
            height: 20px;
        }

        /* Main Container */
        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Chat Area */
        .chat-area {
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
        }

        .chat-content {
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 24px 16px;
            min-height: 100%;
            display: flex;
            flex-direction: column;
        }

        /* Empty State */
        .empty-state {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 40px 20px;
        }

        .empty-state-title {
            font-size: 32px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 8px;
        }

        .empty-state-subtitle {
            font-size: 16px;
            color: var(--text-secondary);
        }

        /* Messages */
        .messages-container {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .message-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .message-group.user {
            align-items: flex-end;
        }

        .message-group.assistant {
            align-items: flex-start;
        }

        .message {
            max-width: 85%;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }

        .message.user {
            background: var(--user-bubble);
            padding: 12px 18px;
            border-radius: 24px;
            color: var(--text-primary);
        }

        .message.assistant {
            padding: 0;
            color: var(--text-primary);
        }

        .message-content {
            font-size: 16px;
            line-height: 1.6;
        }

        .message-content p {
            margin-bottom: 12px;
        }

        .message-content p:last-child {
            margin-bottom: 0;
        }

        .message-content strong {
            font-weight: 600;
        }

        .message-content ul, .message-content ol {
            margin: 8px 0;
            padding-left: 24px;
        }

        .message-content li {
            margin-bottom: 4px;
        }

        .message-content code {
            background: var(--bg-secondary);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'SF Mono', 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
        }

        .message-content h3 {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
            margin: 16px 0 8px 0;
            line-height: 1.3;
        }

        .message-content .table-container {
            overflow-x: auto;
            margin: 16px -16px;
            border-radius: 8px;
        }

        .message-content table {
            width: auto;
            min-width: 100%;
            border-collapse: collapse;
            margin: 0;
            font-size: 12px;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            display: table;
            max-width: none;
        }

        .message-content th,
        .message-content td {
            padding: 6px 8px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }

        .message-content th {
            background: var(--bg-secondary);
            font-weight: 600;
            color: var(--text-primary);
            border-bottom: 2px solid var(--border-color);
        }

        .message-content tbody tr:hover {
            background: var(--action-hover);
        }

        .message-content tbody tr:last-child td {
            border-bottom: none;
        }

        /* Message Actions */
        .message-actions {
            display: flex;
            align-items: center;
            gap: 2px;
            margin-top: 8px;
            opacity: 1;
            transition: opacity 0.15s;
        }

        .action-btn {
            width: 32px;
            height: 32px;
            border: none;
            background: transparent;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-tertiary);
            transition: all 0.15s;
        }

        .action-btn:hover {
            background: var(--action-hover);
            color: var(--text-secondary);
        }

        .action-btn svg {
            width: 18px;
            height: 18px;
        }

        .action-btn.has-sql {
            color: var(--text-tertiary);
        }

        .action-btn.has-sql:hover {
            background: var(--action-hover);
            color: var(--text-secondary);
        }

        /* SQL Popup */
        .sql-popup-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(4px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.2s, visibility 0.2s;
        }

        .sql-popup-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .sql-popup {
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            max-width: 700px;
            width: 90%;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
            transform: scale(0.95);
            transition: transform 0.2s;
        }

        .sql-popup-overlay.active .sql-popup {
            transform: scale(1);
        }

        .sql-popup-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-color);
        }

        .sql-popup-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .sql-popup-title svg {
            width: 20px;
            height: 20px;
            color: #10b981;
        }

        .sql-popup-close {
            width: 32px;
            height: 32px;
            border: none;
            background: transparent;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-tertiary);
            transition: all 0.15s;
        }

        .sql-popup-close:hover {
            background: var(--action-hover);
            color: var(--text-primary);
        }

        .sql-popup-close svg {
            width: 20px;
            height: 20px;
        }

        .sql-popup-content {
            padding: 20px;
            overflow-y: auto;
            flex: 1;
        }

        .sql-query-block {
            background: #1e1e1e;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 16px;
        }

        .sql-query-block:last-child {
            margin-bottom: 0;
        }

        .sql-query-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 16px;
            background: #2d2d2d;
            border-bottom: 1px solid #3d3d3d;
        }

        .sql-query-label {
            font-size: 12px;
            font-weight: 500;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .sql-copy-btn {
            padding: 4px 10px;
            font-size: 12px;
            background: transparent;
            border: 1px solid #4d4d4d;
            border-radius: 6px;
            color: #aaa;
            cursor: pointer;
            transition: all 0.15s;
        }

        .sql-copy-btn:hover {
            background: #3d3d3d;
            border-color: #5d5d5d;
            color: #fff;
        }

        .sql-query-code {
            padding: 16px;
            font-family: 'SF Mono', 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            line-height: 1.6;
            color: #d4d4d4;
            white-space: pre-wrap;
            word-break: break-word;
            margin: 0;
        }

        /* SQL Syntax Highlighting */
        .sql-keyword {
            color: #569cd6;
            font-weight: 500;
        }

        .sql-function {
            color: #dcdcaa;
        }

        .sql-string {
            color: #ce9178;
        }

        .sql-number {
            color: #b5cea8;
        }

        .sql-comment {
            color: #6a9955;
            font-style: italic;
        }

        .no-sql-message {
            text-align: center;
            color: var(--text-tertiary);
            padding: 40px 20px;
        }

        .no-sql-message svg {
            width: 48px;
            height: 48px;
            margin-bottom: 12px;
            opacity: 0.5;
        }

        /* JSON/Code Response */
        .json-response {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 16px;
            border-radius: 12px;
            font-family: 'SF Mono', 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            overflow-x: auto;
            margin-top: 12px;
            white-space: pre-wrap;
            word-break: break-word;
            line-height: 1.5;
        }

        /* Tables */
        .message-content .table-container {
            overflow-x: auto;
            margin: 12px -16px;
            border-radius: 8px;
        }

        .message-content table {
            border-collapse: collapse;
            margin: 0;
            font-size: 12px;
            width: auto;
            min-width: 100%;
            display: table;
            max-width: none;
        }

        .message-content th, .message-content td {
            border: 1px solid var(--border-color);
            padding: 6px 8px;
            text-align: left;
            white-space: nowrap;
        }

        .message-content th {
            background: var(--bg-secondary);
            font-weight: 600;
        }

        /* Input Area */
        .input-area {
            padding: 16px;
            background: var(--bg-primary);
            flex-shrink: 0;
        }

        .input-container {
            max-width: var(--max-width);
            margin: 0 auto;
        }

        .input-wrapper {
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 26px;
            padding: 8px 8px 8px 16px;
            transition: border-color 0.15s, box-shadow 0.15s;
        }

        .input-wrapper:focus-within {
            border-color: var(--text-tertiary);
            box-shadow: 0 0 0 1px var(--text-tertiary);
        }

        .input-left-btn {
            width: 32px;
            height: 32px;
            border: none;
            background: transparent;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
            flex-shrink: 0;
            transition: background 0.15s;
        }

        .input-left-btn:hover {
            background: var(--action-hover);
        }

        .input-left-btn svg {
            width: 20px;
            height: 20px;
        }

        .input-field-container {
            flex: 1;
            display: flex;
            align-items: flex-start;
            min-height: 36px;
            padding-top: 8px;
        }

        #message-input {
            width: 100%;
            border: none;
            outline: none;
            font-size: 16px;
            font-family: inherit;
            line-height: 20px;
            resize: none;
            max-height: 400px;
            overflow-y: hidden;
            background: transparent;
            color: var(--text-primary);
            padding: 0;
            margin: 0;
            vertical-align: top;
            min-height: 20px;
        }

        #message-input::placeholder {
            color: var(--text-tertiary);
        }

        .input-right-actions {
            display: flex;
            align-items: center;
            gap: 4px;
            flex-shrink: 0;
        }

        .input-icon-btn {
            width: 32px;
            height: 32px;
            border: none;
            background: transparent;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
            transition: background 0.15s;
        }

        .input-icon-btn:hover {
            background: var(--action-hover);
        }

        .input-icon-btn svg {
            width: 20px;
            height: 20px;
        }

        .send-button {
            width: 36px;
            height: 36px;
            border: none;
            background: var(--button-primary);
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.15s, opacity 0.15s;
            position: relative;
        }

        .send-button:hover:not(:disabled) {
            background: var(--button-hover);
        }

        .send-button:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .send-button #send-icon,
        .send-button .btn-loading,
        .send-button svg,
        .send-button span {
            pointer-events: none;
        }

        .send-button #send-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
        }

        .send-button svg {
            width: 18px;
            height: 18px;
            color: white;
            display: block;
            margin: 0 auto;
            padding: 0;
        }

        /* Loading Indicator */
        .loading-dots {
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 12px 0;
        }

        .loading-dot {
            width: 8px;
            height: 8px;
            background: var(--text-tertiary);
            border-radius: 50%;
            animation: loadingPulse 1.4s ease-in-out infinite;
        }

        .loading-dot:nth-child(1) { animation-delay: 0s; }
        .loading-dot:nth-child(2) { animation-delay: 0.2s; }
        .loading-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes loadingPulse {
            0%, 80%, 100% {
                opacity: 0.4;
                transform: scale(0.8);
            }
            40% {
                opacity: 1;
                transform: scale(1);
            }
        }

        /* Button loading spinner */
        .btn-loading {
            width: 18px;
            height: 18px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Message animations */
        @keyframes fadeSlideIn {
            from {
                opacity: 0;
                transform: translateY(8px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message-group {
            animation: fadeSlideIn 0.25s ease-out;
        }

        /* Scrollbar styling */
        .chat-area::-webkit-scrollbar {
            width: 8px;
        }

        .chat-area::-webkit-scrollbar-track {
            background: transparent;
        }

        .chat-area::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }

        .chat-area::-webkit-scrollbar-thumb:hover {
            background: var(--text-tertiary);
        }

        /* Disclaimer */
        .disclaimer {
            text-align: center;
            font-size: 12px;
            color: var(--text-tertiary);
            padding: 8px 16px 16px;
        }

        /* Responsive */
        @media (max-width: 640px) {
            .header-btn span {
                display: none;
            }
            
            .header-btn {
                padding: 8px;
            }

            .empty-state-title {
                font-size: 24px;
            }

            .message {
                max-width: 90%;
            }

            .chat-content {
                padding: 16px 12px;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-left">
            <span class="header-title">DB Assistant</span>
            <svg class="header-dropdown" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
        </div>
        <div class="header-right">
            <button class="header-btn" type="button" id="new-chat-btn" title="New chat">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 5v14M5 12h14"/>
                </svg>
                <span>New chat</span>
            </button>
            <button class="header-icon-btn" type="button" title="Menu">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="1"/>
                    <circle cx="12" cy="5" r="1"/>
                    <circle cx="12" cy="19" r="1"/>
                </svg>
            </button>
        </div>
    </header>

    <!-- Main Container -->
    <main class="main-container">
        <!-- Chat Area -->
        <div class="chat-area" id="chat-area">
            <div class="chat-content" id="chat-content">
                <!-- Empty State (shown when no messages) -->
                <div class="empty-state" id="empty-state">
                    <h1 class="empty-state-title">What can I help with?</h1>
                    <p class="empty-state-subtitle">Ask about databases, tables, schemas, or query your data</p>
                </div>
                <!-- Messages Container (hidden initially) -->
                <div class="messages-container" id="messages-container" style="display: none;"></div>
            </div>
        </div>

        <!-- Input Area -->
        <div class="input-area">
            <div class="input-container">
                <div class="input-wrapper">
                    <button class="input-left-btn" type="button" title="Attach">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 5v14M5 12h14"/>
                        </svg>
                    </button>
                    <div class="input-field-container">
                        <textarea 
                            id="message-input" 
                            placeholder="Ask anything" 
                            rows="1"
                        ></textarea>
                    </div>
                    <div class="input-right-actions">
                        <button class="send-button" id="send-button" type="button" title="Send" onclick="window.handleSend && window.handleSend()">
                            <span id="send-icon">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M22 2L11 13"/>
                                    <path d="M22 2L15 22L11 13L2 9L22 2Z"/>
                                </svg>
                            </span>
                            <div class="btn-loading" id="loading" style="display: none;"></div>
                        </button>
                    </div>
                </div>
            </div>
            <p class="disclaimer">DB Assistant can make mistakes. Verify important information.</p>
        </div>
    </main>

    <!-- SQL Popup -->
    <div class="sql-popup-overlay" id="sql-popup-overlay">
        <div class="sql-popup">
            <div class="sql-popup-header">
                <div class="sql-popup-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M4 7V4a2 2 0 0 1 2-2h8.5L20 7.5V20a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-3"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <path d="M8 13h3"/>
                        <path d="M8 17h5"/>
                    </svg>
                    Executed SQL Queries
                </div>
                <button class="sql-popup-close" onclick="closeSqlPopup()">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>
            <div class="sql-popup-content" id="sql-popup-content">
                <!-- SQL queries will be injected here -->
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            let isLoading = false;
            let hasMessages = false;
            let messageCounter = 0;
            const messageSqlMap = new Map(); // Store SQL queries per message ID

            const chatArea = document.getElementById('chat-area');
            const chatContent = document.getElementById('chat-content');
            const emptyState = document.getElementById('empty-state');
            const messagesContainer = document.getElementById('messages-container');
            const messageInput = document.getElementById('message-input');
            const sendButton = document.getElementById('send-button');
            const sendIcon = document.getElementById('send-icon');
            const loading = document.getElementById('loading');
            const newChatBtn = document.getElementById('new-chat-btn');

            // Validate elements
            if (!chatArea || !messagesContainer || !messageInput || !sendButton || !sendIcon || !loading) {
                console.error('Missing required DOM elements');
                return;
            }

            // Auto-resize textarea
            function autoResize() {
                messageInput.style.height = 'auto';
                messageInput.style.height = Math.min(messageInput.scrollHeight, 400) + 'px';
            }

            messageInput.addEventListener('input', autoResize);

            // Handle key press
            function handleKeyPress(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    sendMessage();
                }
            }

            // Send message
            function sendMessage() {
                console.log('sendMessage called');
                const message = messageInput.value.trim();
                console.log('Message:', message, 'isLoading:', isLoading);
                if (!message || isLoading) return;

                // Show messages container, hide empty state
                if (!hasMessages) {
                    emptyState.style.display = 'none';
                    messagesContainer.style.display = 'flex';
                    hasMessages = true;
                }

                addMessage(message, 'user');
                messageInput.value = '';
                messageInput.style.height = 'auto';
                messageInput.focus();

                setLoading(true);
                addLoadingIndicator();
                sendToBackend(message);
            }

            // Expose globally for onclick fallback
            window.handleSend = sendMessage;

            // Process markdown tables
            function processTables(text) {
                // Split text into lines
                const lines = text.split('\\n');
                let result = [];
                let inTable = false;
                let tableRows = [];

                for (let i = 0; i < lines.length; i++) {
                    const line = lines[i].trim();

                    // Check if this line is a table row (starts and ends with |)
                    if (line.startsWith('|') && line.endsWith('|')) {
                        const cells = line.split('|').slice(1, -1).map(cell => cell.trim());
                        tableRows.push(cells);
                        inTable = true;
                    } else {
                        // If we were in a table, process it
                        if (inTable && tableRows.length > 0) {
                            result.push(generateTableHTML(tableRows));
                            tableRows = [];
                            inTable = false;
                        }
                        result.push(line);
                    }
                }

                // Handle table at end of text
                if (inTable && tableRows.length > 0) {
                    result.push(generateTableHTML(tableRows));
                }

                return result.join('\\n');
            }

            function generateTableHTML(rows) {
                if (rows.length < 2) return rows.map(row => '|' + row.join('|') + '|').join('\\n');

                // First row is headers, second row is separator, rest are data
                const headers = rows[0];
                const dataRows = rows.slice(2); // Skip header and separator rows

                let html = '<table><thead><tr>';
                headers.forEach(header => {
                    html += '<th>' + header + '</th>';
                });
                html += '</tr></thead><tbody>';

                dataRows.forEach(row => {
                    html += '<tr>';
                    row.forEach(cell => {
                        html += '<td>' + cell + '</td>';
                    });
                    html += '</tr>';
                });

                html += '</tbody></table>';
                return '<div class="table-container">' + html + '</div>';
            }

            // Process markdown
            function processMarkdown(text) {
                if (!text) return '';
                // Tables - convert markdown tables to HTML tables
                text = processTables(text);
                // Headers (### Header Text -> <h3>Header Text</h3>)
                text = text.replace(/^### (.+)$/gm, '<h3>$1</h3>');
                // Bold - using string replace to avoid regex escaping issues
                text = text.split('**').map(function(part, i) {
                    return i % 2 === 1 ? '<strong>' + part + '</strong>' : part;
                }).join('');
                // Inline code
                text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
                // Newlines to <br>
                text = text.replace(/\\n/g, '<br>');
                return text;
            }

            // Add message
            function addMessage(content, type, isJson = false, sqlQueries = []) {
                const messageId = `msg-${++messageCounter}`;
                const group = document.createElement('div');
                group.className = `message-group ${type}`;
                group.id = messageId;

                const message = document.createElement('div');
                message.className = `message ${type}`;

                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';

                if (isJson) {
                    const jsonDiv = document.createElement('div');
                    jsonDiv.className = 'json-response';
                    jsonDiv.textContent = content;
                    contentDiv.appendChild(jsonDiv);
                } else {
                    contentDiv.innerHTML = processMarkdown(content);
                }

                message.appendChild(contentDiv);
                group.appendChild(message);

                // Add action buttons for assistant messages
                if (type === 'assistant') {
                    // Store SQL queries for this message
                    if (sqlQueries && sqlQueries.length > 0) {
                        messageSqlMap.set(messageId, sqlQueries);
                    }
                    
                    const hasSql = sqlQueries && sqlQueries.length > 0;
                    const sqlBtnClass = hasSql ? 'action-btn has-sql' : 'action-btn';
                    const sqlBtnTitle = hasSql ? `View SQL (${sqlQueries.length})` : 'No SQL executed';
                    
                    const actions = document.createElement('div');
                    actions.className = 'message-actions';
                    actions.innerHTML = `
                        <button class="action-btn" type="button" title="Copy" onclick="copyMessage(this)">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="9" y="9" width="13" height="13" rx="2"/>
                                <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
                            </svg>
                        </button>
                        <button class="action-btn" type="button" title="Good response">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M14 9V5a3 3 0 00-3-3l-4 9v11h11.28a2 2 0 002-1.7l1.38-9a2 2 0 00-2-2.3H14z"/>
                                <path d="M7 22H4a2 2 0 01-2-2v-7a2 2 0 012-2h3"/>
                            </svg>
                        </button>
                        <button class="action-btn" type="button" title="Bad response">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M10 15v4a3 3 0 003 3l4-9V2H5.72a2 2 0 00-2 1.7l-1.38 9a2 2 0 002 2.3H10z"/>
                                <path d="M17 2h3a2 2 0 012 2v7a2 2 0 01-2 2h-3"/>
                            </svg>
                        </button>
                        <button class="${sqlBtnClass}" type="button" title="${sqlBtnTitle}" onclick="showSqlPopup('${messageId}')">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M4 7V4a2 2 0 0 1 2-2h8.5L20 7.5V20a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-3"/>
                                <polyline points="14 2 14 8 20 8"/>
                                <path d="M8 13h3"/>
                                <path d="M8 17h5"/>
                            </svg>
                        </button>
                    `;
                    group.appendChild(actions);
                }

                messagesContainer.appendChild(group);
                scrollToBottom();
            }

            // Loading indicator
            function addLoadingIndicator() {
                const loadingGroup = document.createElement('div');
                loadingGroup.className = 'message-group assistant';
                loadingGroup.id = 'loading-indicator';

                const loadingContent = document.createElement('div');
                loadingContent.className = 'loading-dots';
                loadingContent.innerHTML = `
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                `;

                loadingGroup.appendChild(loadingContent);
                messagesContainer.appendChild(loadingGroup);
                scrollToBottom();
            }

            function removeLoadingIndicator() {
                const indicator = document.getElementById('loading-indicator');
                if (indicator) indicator.remove();
            }

            // Scroll to bottom
            function scrollToBottom() {
                chatArea.scrollTop = chatArea.scrollHeight;
            }

            // Set loading state
            function setLoading(loadingState) {
                isLoading = loadingState;
                sendIcon.style.display = loadingState ? 'none' : 'flex';
                loading.style.display = loadingState ? 'block' : 'none';
                sendButton.disabled = loadingState;
            }

            // Send to backend
            async function sendToBackend(message) {
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.json();
                    removeLoadingIndicator();

                    // Extract SQL queries from response
                    const sqlQueries = data.sql_queries || [];

                    if (data.error) {
                        addMessage('Error: ' + data.error, 'assistant', false, []);
                    } else if (data.response) {
                        addMessage(data.response, 'assistant', data.is_json, sqlQueries);
                    } else {
                        addMessage('Sorry, I couldn\\'t process your request.', 'assistant', false, []);
                    }
                } catch (error) {
                    console.error('Error sending message:', error);
                    removeLoadingIndicator();
                    addMessage('Sorry, there was an error connecting to the server: ' + error.message, 'assistant', false, []);
                } finally {
                    setLoading(false);
                }
            }

            // Copy message function (global)
            window.copyMessage = function(btn) {
                const messageContent = btn.closest('.message-group').querySelector('.message-content');
                const text = messageContent.innerText;
                navigator.clipboard.writeText(text).then(() => {
                    // Show feedback
                    const originalHTML = btn.innerHTML;
                    btn.innerHTML = `
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="20 6 9 17 4 12"/>
                        </svg>
                    `;
                    setTimeout(() => { btn.innerHTML = originalHTML; }, 2000);
                });
            };

            // SQL Popup functions (global)
            window.showSqlPopup = function(messageId) {
                const sqlQueries = messageSqlMap.get(messageId) || [];
                const popupContent = document.getElementById('sql-popup-content');
                const overlay = document.getElementById('sql-popup-overlay');
                
                if (sqlQueries.length === 0) {
                    popupContent.innerHTML = `
                        <div class="no-sql-message">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"/>
                                <line x1="12" y1="8" x2="12" y2="12"/>
                                <line x1="12" y1="16" x2="12.01" y2="16"/>
                            </svg>
                            <p>No SQL queries were executed for this response.</p>
                        </div>
                    `;
                } else {
                    popupContent.innerHTML = sqlQueries.map((sql, index) => `
                        <div class="sql-query-block">
                            <div class="sql-query-header">
                                <span class="sql-query-label">Query ${sqlQueries.length > 1 ? index + 1 : ''}</span>
                                <button class="sql-copy-btn" onclick="copySql(this, ${index})">Copy</button>
                            </div>
                            <pre class="sql-query-code">${highlightSql(sql)}</pre>
                        </div>
                    `).join('');
                    
                    // Store queries for copy function
                    window._currentSqlQueries = sqlQueries;
                }
                
                overlay.classList.add('active');
                document.body.style.overflow = 'hidden';
            };

            window.closeSqlPopup = function() {
                const overlay = document.getElementById('sql-popup-overlay');
                overlay.classList.remove('active');
                document.body.style.overflow = '';
            };

            window.copySql = function(btn, index) {
                const sql = window._currentSqlQueries[index];
                navigator.clipboard.writeText(sql).then(() => {
                    const originalText = btn.textContent;
                    btn.textContent = 'Copied!';
                    setTimeout(() => { btn.textContent = originalText; }, 2000);
                });
            };

            // Close popup on overlay click
            document.getElementById('sql-popup-overlay').addEventListener('click', function(e) {
                if (e.target === this) {
                    closeSqlPopup();
                }
            });

            // Close popup on Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeSqlPopup();
                }
            });

            // SQL syntax highlighting
            function highlightSql(sql) {
                // Escape HTML first
                let escaped = sql
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');
                
                // Keywords (case-insensitive)
                const keywords = [
                    'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'IN', 'LIKE', 'BETWEEN',
                    'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'FULL', 'CROSS', 'ON',
                    'GROUP', 'BY', 'ORDER', 'HAVING', 'LIMIT', 'OFFSET', 'AS', 'DISTINCT',
                    'UNION', 'ALL', 'EXCEPT', 'INTERSECT', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
                    'NULL', 'IS', 'TRUE', 'FALSE', 'ASC', 'DESC', 'WITH', 'OVER', 'PARTITION'
                ];
                
                // Functions
                const functions = [
                    'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'COALESCE', 'NULLIF', 'CAST',
                    'CONCAT', 'SUBSTRING', 'TRIM', 'UPPER', 'LOWER', 'LENGTH', 'REPLACE',
                    'DATE', 'NOW', 'CURRENT_DATE', 'CURRENT_TIMESTAMP', 'EXTRACT',
                    'ROUND', 'FLOOR', 'CEIL', 'ABS', 'ROW_NUMBER', 'RANK', 'DENSE_RANK'
                ];
                
                // Highlight keywords
                keywords.forEach(kw => {
                    const regex = new RegExp('\\\\b(' + kw + ')\\\\b', 'gi');
                    escaped = escaped.replace(regex, '<span class="sql-keyword">$1</span>');
                });
                
                // Highlight functions
                functions.forEach(fn => {
                    const regex = new RegExp('\\\\b(' + fn + ')\\\\s*\\\\(', 'gi');
                    escaped = escaped.replace(regex, '<span class="sql-function">$1</span>(');
                });
                
                // Highlight strings (single quotes)
                escaped = escaped.replace(/'([^']*)'/g, '<span class="sql-string">\\'$1\\'</span>');
                
                // Highlight numbers
                escaped = escaped.replace(/\\b(\\d+\\.?\\d*)\\b/g, '<span class="sql-number">$1</span>');
                
                // Highlight comments
                escaped = escaped.replace(/--(.*)$/gm, '<span class="sql-comment">--$1</span>');
                
                return escaped;
            }

            // Event listeners - attach these FIRST before anything else
            console.log('Attaching event listeners...');
            messageInput.addEventListener('keydown', handleKeyPress);
            sendButton.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Send button clicked');
                sendMessage();
            });
            console.log('Main event listeners attached');

            // New chat button (optional - check if exists)
            if (newChatBtn) {
                newChatBtn.addEventListener('click', async function() {
                    try {
                        await fetch('/clear-context', { method: 'POST' });
                    } catch (e) {
                        console.error('Error clearing context:', e);
                    }
                    messagesContainer.innerHTML = '';
                    emptyState.style.display = 'flex';
                    messagesContainer.style.display = 'none';
                    hasMessages = false;
                    messageInput.focus();
                });
            }

            // Focus input
            messageInput.focus();
            console.log('UI initialized successfully');
        });
    </script>
</body>
</html>
"""

def call_mcp_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """
    Call an MCP tool by importing and running the server functions directly.

    Args:
        tool_name: Name of the MCP tool to call
        **kwargs: Arguments to pass to the tool

    Returns:
        Tool response as dictionary
    """
    logger.debug(f"Calling MCP tool: {tool_name} with kwargs: {kwargs}")
    if not MCP_AVAILABLE:
        error_msg = "MCP server functions not available"
        if MCP_IMPORT_ERROR:
            error_msg += f". {MCP_IMPORT_ERROR}"
        logger.error(error_msg)
        return {"error": error_msg}

    try:
        # Map tool names to imported functions - use globals() to safely check
        tool_functions = {}
        func_names = ["list_databases", "list_domains", "list_tables", "search_tables", 
                     "get_table_schema", "answer_question", "generate_sql", "execute_sql", "add", "echo"]
        
        missing_funcs = []
        module_globals = globals()
        for name in func_names:
            try:
                if name in module_globals:
                    func = module_globals[name]
                    if callable(func):
                        tool_functions[name] = func
                    else:
                        missing_funcs.append(f"{name}(not callable)")
                else:
                    missing_funcs.append(name)
            except Exception as e:
                missing_funcs.append(f"{name}(error: {e})")
        
        if missing_funcs:
            available = list(tool_functions.keys())
            return {"error": f"Functions not available: {', '.join(missing_funcs)}. Available: {available}. MCP_AVAILABLE={MCP_AVAILABLE}"}

        if tool_name not in tool_functions:
            return {"error": f"Unknown tool: {tool_name}. Available: {list(tool_functions.keys())}"}

        # Call the function directly
        logger.debug(f"Executing tool function: {tool_name}")
        result = tool_functions[tool_name](**kwargs)

        # Some functions return dicts, others return values - handle appropriately
        if isinstance(result, dict) and "error" in result:
            logger.warning(f"Tool {tool_name} returned error: {result.get('error')}")
            return result
        elif tool_name in ["add", "echo"]:
            # Simple functions return values directly
            logger.debug(f"Tool {tool_name} returned value: {result}")
            return result
        else:
            # Complex functions return structured data
            logger.debug(f"Tool {tool_name} returned structured data: success={result.get('success', 'N/A')}")
            return result

    except NameError as e:
        # Handle case where functions aren't defined
        missing_name = str(e).split("'")[1] if "'" in str(e) else "unknown"
        error_msg = f"Function '{missing_name}' is not defined. This may indicate the module wasn't loaded correctly. Please restart the server."
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        error_msg = f"Error calling tool {tool_name}: {str(e)}"
        logger.error(f"{error_msg}\nDetails: {error_details[:200]}", exc_info=True)
        return {"error": f"{error_msg}\nDetails: {error_details[:200]}"}

def process_natural_language_query(query: str) -> Dict[str, Any]:
    """
    Process a natural language query and determine which MCP tool(s) to call.

    Args:
        query: Natural language query from user

    Returns:
        Response dictionary with formatted result
    """
    query_lower = query.lower().strip()

    # Route queries to appropriate MCP tools
    try:
        # Detect data questions (questions that need SQL execution)
        # These are questions that ask about data, not schema
        data_question_indicators = [
            "how many", "how much", "count", "total", "sum", "average", "avg",
            "what is", "what are", "show me", "list all", "find all", "get all",
            "who", "when", "where", "which", "give me", "tell me"
        ]
        
        is_schema_question = any(phrase in query_lower for phrase in [
            "what databases", "list databases", "show databases", "available databases",
            "what domains", "list domains", "show domains", "business domains",
            "list tables", "show tables", "what tables", "all tables",
            "schema", "structure", "columns", "fields", "table schema",
            "search", "find", "look for", "related to"
        ])
        
        # If it's a data question (not a schema question), use answer_question tool
        if not is_schema_question and any(indicator in query_lower for indicator in data_question_indicators):
            result = call_mcp_tool("answer_question", question=query)
            
            if "error" in result or not result.get("success"):
                error_msg = result.get("error", "Failed to answer question")
                return {"response": f"Error: {error_msg}", "is_json": False}
            
            # Format response with answer and table if applicable
            response = ""
            
            # Add natural language answer
            if result.get("answer"):
                response += f"{result['answer']}\n\n"
            
            # Add table if there's data
            data = result.get("data", [])
            columns = result.get("columns", [])
            row_count = result.get("row_count", 0)
            
            if row_count > 0 and data:
                # Format as table
                response += "**Results:**\n\n"
                
                # Create markdown table
                if row_count <= 100:  # Only show table for reasonable number of rows
                    # Header
                    response += "| " + " | ".join(columns) + " |\n"
                    response += "| " + " | ".join(["---"] * len(columns)) + " |\n"
                    
                    # Rows
                    for row in data:
                        values = [str(row.get(col, "")) for col in columns]
                        response += "| " + " | ".join(values) + " |\n"
                else:
                    # Too many rows, just show summary
                    response += f"*Showing {row_count} rows. First few results:*\n\n"
                    response += "| " + " | ".join(columns) + " |\n"
                    response += "| " + " | ".join(["---"] * len(columns)) + " |\n"
                    for row in data[:10]:  # Show first 10
                        values = [str(row.get(col, "")) for col in columns]
                        response += "| " + " | ".join(values) + " |\n"
                    response += f"\n*... and {row_count - 10} more rows*"
            
            if result.get("execution_time"):
                response += f"\n\n*Query executed in {result['execution_time']}s*"
            
            return {"response": response, "is_json": False}
        
        # List databases
        if any(phrase in query_lower for phrase in ["what databases", "list databases", "show databases", "available databases"]):
            result = call_mcp_tool("list_databases")
            if "error" in result:
                return {"response": f"Error: {result['error']}", "is_json": False}

            databases = result.get("databases", [])
            if not databases:
                return {"response": "No databases found in the index.", "is_json": False}

            response = "**Available Databases:**\n\n"
            for db in databases:
                response += f"• **{db['name']}**: {db['table_count']} tables\n"
                if db.get('domains'):
                    response += f"  Domains: {', '.join(db['domains'])}\n"
                if db.get('schemas'):
                    response += f"  Schemas: {', '.join(db['schemas'])}\n"
                response += "\n"

            return {"response": response, "is_json": False}

        # List domains
        elif any(phrase in query_lower for phrase in ["what domains", "list domains", "show domains", "business domains"]):
            database = None
            # Extract database name if specified
            if "postgres" in query_lower:
                database = "postgres_production"
            elif "snowflake" in query_lower:
                database = "snowflake_production"

            result = call_mcp_tool("list_domains", database=database or "")
            if "error" in result:
                return {"response": f"Error: {result['error']}", "is_json": False}

            domains = result.get("domains", [])
            if not domains:
                db_msg = f" in {database}" if database else ""
                return {"response": f"No domains found{db_msg}.", "is_json": False}

            response = f"**Business Domains{' (' + database + ')' if database else ''}:**\n\n"
            for domain in domains:
                response += f"• **{domain['name']}**: {domain['table_count']} tables\n"
                response += f"  {domain['description']}\n"
                if domain.get('databases'):
                    response += f"  Databases: {', '.join(domain['databases'])}\n"
                response += "\n"

            return {"response": response, "is_json": False}

        # List tables
        elif any(phrase in query_lower for phrase in ["list tables", "show tables", "what tables", "all tables"]):
            database = domain = None

            # Extract filters from query
            if "postgres" in query_lower:
                database = "postgres_production"
            elif "snowflake" in query_lower:
                database = "snowflake_production"

            # Extract domain
            domain_keywords = ["authentication", "payments", "realtime", "security", "storage", "workflow"]
            for keyword in domain_keywords:
                if keyword in query_lower:
                    domain = keyword
                    break

            result = call_mcp_tool("list_tables", database=database or "", domain=domain or "")
            if "error" in result:
                return {"response": f"Error: {result['error']}", "is_json": False}

            tables = result
            if not tables:
                filters = []
                if database: filters.append(f"database: {database}")
                if domain: filters.append(f"domain: {domain}")
                filter_msg = f" ({', '.join(filters)})" if filters else ""
                return {"response": f"No tables found{filter_msg}.", "is_json": False}

            response = f"**Tables{' (' + database + ')' if database else ''}{' in ' + domain if domain else ''}:**\n\n"
            for table in tables[:20]:  # Limit to 20 for readability
                response += f"• **{table['name']}** ({table.get('database', 'unknown')})\n"
                if table.get('summary'):
                    response += f"  {table['summary']}\n"
                response += "\n"

            if len(tables) > 20:
                response += f"\n*Showing first 20 of {len(tables)} tables*"

            return {"response": response, "is_json": False}

        # Search tables
        elif any(phrase in query_lower for phrase in ["search", "find", "look for"]) and ("table" in query_lower or "related to" in query_lower):
            # Extract search terms
            search_terms = []
            if "related to" in query_lower:
                parts = query_lower.split("related to")
                if len(parts) > 1:
                    search_terms = [parts[1].strip()]
            elif "find" in query_lower and "table" in query_lower:
                # Extract everything after "find tables" or similar
                patterns = [r"find tables? (.*)", r"find (.*) tables?", r"search for (.*)"]
                for pattern in patterns:
                    match = re.search(pattern, query_lower)
                    if match:
                        search_terms = [match.group(1).strip()]
                        break

            if not search_terms:
                # Use the whole query minus common words
                stop_words = ["find", "search", "for", "tables", "table", "related", "to", "show", "me", "about"]
                words = [w for w in query_lower.split() if w not in stop_words]
                search_terms = [" ".join(words)]

            if search_terms:
                result = call_mcp_tool("search_tables", query=search_terms[0], limit=10)
                if "error" in result:
                    return {"response": f"Error: {result['error']}", "is_json": False}

                tables = result.get("tables", [])
                if not tables:
                    return {"response": f"No tables found matching '{search_terms[0]}'.", "is_json": False}

                response = f"**Search Results for '{search_terms[0]}':**\n\n"
                for table in tables:
                    response += f"• **{table['name']}** (relevance: {table['relevance_score']:.2f})\n"
                    if table.get('summary'):
                        response += f"  {table['summary']}\n"
                    response += f"  Database: {table['database']}, Domain: {table['domain']}\n\n"

                response += f"*Found {result.get('total_matches', 0)} total matches*"
                return {"response": response, "is_json": False}

        # Get table schema
        elif any(phrase in query_lower for phrase in ["schema", "structure", "columns", "fields"]) and ("table" in query_lower or "for" in query_lower):
            # Extract table name
            table_name = None

            # Look for quoted table names
            quoted_match = re.search(r'["\']([^"\']+)["\']', query)
            if quoted_match:
                table_name = quoted_match.group(1)
            else:
                # Look for common patterns
                patterns = [
                    r"schema for (.*)",
                    r"columns for (.*)",
                    r"structure of (.*)",
                    r"(.*) table schema",
                    r"(.*) columns"
                ]
                for pattern in patterns:
                    match = re.search(pattern, query_lower)
                    if match:
                        table_name = match.group(1).strip()
                        break

            if table_name:
                result = call_mcp_tool("get_table_schema", table=table_name)
                if "error" in result:
                    return {"response": f"Error: {result['error']}", "is_json": False}

                # Format the schema response nicely
                response = f"**Schema for table '{table_name}':**\n\n"
                response += f"**Database:** {result.get('database', 'unknown')}\n"
                response += f"**Schema:** {result.get('schema', 'unknown')}\n"

                if result.get('description'):
                    response += f"**Description:** {result['description']}\n"

                if result.get('row_count'):
                    response += f"**Row Count:** {result['row_count']:,}\n"

                response += "\n**Columns:**\n"
                for col in result.get('columns', []):
                    nullable = " (nullable)" if col.get('nullable') else ""
                    response += f"• `{col['name']}`: {col['type']}{nullable}\n"
                    if col.get('description'):
                        response += f"  {col['description']}\n"

                if result.get('primary_key'):
                    response += f"\n**Primary Key:** {', '.join(result['primary_key'])}\n"

                if result.get('foreign_keys'):
                    response += "\n**Foreign Keys:**\n"
                    for fk in result['foreign_keys']:
                        response += f"• {fk.get('columns', [])} → {fk.get('references', '')}\n"

                return {"response": response, "is_json": False}

        # Get domain overview
        elif "domain" in query_lower and ("overview" in query_lower or "summary" in query_lower):
            # Extract domain name
            domain = None
            domain_keywords = ["authentication", "payments", "realtime", "security", "storage", "workflow"]
            for keyword in domain_keywords:
                if keyword in query_lower:
                    domain = keyword
                    break

            if domain:
                result = call_mcp_tool("get_domain_overview", domain=domain)
                if "error" in result:
                    return {"response": f"Error: {result['error']}", "is_json": False}

                response = f"**Domain Overview: {domain}**\n\n"
                response += f"**Description:** {result.get('description', '')}\n"
                response += f"**Databases:** {', '.join(result.get('databases', []))}\n\n"

                response += "**Tables:**\n"
                for table in result.get('tables', []):
                    response += f"• **{table['name']}**\n"
                    if table.get('description'):
                        response += f"  {table['description']}\n"
                    if table.get('row_count'):
                        response += f"  Rows: {table['row_count']:,}\n"
                    response += "\n"

                return {"response": response, "is_json": False}

        # Default: use search_tables as fallback
        result = call_mcp_tool("search_tables", query=query, limit=5)
        if "error" not in result and result.get("tables"):
            tables = result.get("tables", [])
            response = f"**Search Results:**\n\n"
            for table in tables:
                response += f"• **{table['name']}** (relevance: {table['relevance_score']:.2f})\n"
                if table.get('summary'):
                    response += f"  {table['summary']}\n"
                response += "\n"
            return {"response": response, "is_json": False}

        # If all else fails, provide help
        return {
            "response": "I'm not sure how to help with that query. Try asking about:\n\n• Available databases\n• Tables in specific domains\n• Schema information for tables\n• Search for tables by topic\n\nFor example: 'What databases are available?' or 'Show me payment-related tables'",
            "is_json": False
        }

    except Exception as e:
        return {"response": f"An error occurred while processing your query: {str(e)}", "is_json": False}

@app.route('/')
def index():
    """Serve the main chatbot interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/favicon.ico')
def favicon():
    """Return empty favicon to prevent 404 errors."""
    return '', 204

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages using AI agent with fallback to pattern matching."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            logger.warning("Chat request missing message parameter")
            return jsonify({"error": "Missing message parameter"}), 400

        message = data['message'].strip()
        if not message:
            logger.warning("Chat request with empty message")
            return jsonify({"error": "Empty message"}), 400

        # Initialize session if needed
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            logger.info(f"Created new session: {session['session_id']}")

        session_id = session['session_id']
        logger.info(f"Processing chat message from session {session_id}: {message[:100]}...")

        # Try AI agent first if available
        if AI_AGENT_AVAILABLE and ai_agent and ai_agent.is_available():
            try:
                logger.debug("Using AI agent for query processing")
                # Get or create conversation context
                context = conversation_manager.get_or_create(session_id)
                
                # Get conversation history
                history = context.get_history()
                logger.debug(f"Conversation history: {len(history)} messages")
                
                # Process query with AI agent
                result = ai_agent.process_query(
                    user_query=message,
                    conversation_history=history,
                    mcp_tool_caller=call_mcp_tool,
                    context_manager=context
                )
                
                # Extract response and SQL queries from result
                response_text = result.get("response", "")
                sql_queries = result.get("sql_queries", [])
                
                # Add messages to context
                context.add_message("user", message)
                context.add_message("assistant", response_text)
                
                logger.info(f"AI agent response generated (length: {len(response_text)}), SQL queries: {len(sql_queries)}")
                return jsonify({
                    "response": response_text,
                    "is_json": False,
                    "sql_queries": sql_queries
                })
            except Exception as ai_error:
                logger.error(f"AI agent error: {ai_error}", exc_info=True)
                # Fall through to pattern matching fallback
                pass

        # Fallback to pattern matching
        logger.debug("Using pattern matching fallback for query processing")
        result = process_natural_language_query(message)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Server error in /chat endpoint: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/clear-context', methods=['POST'])
def clear_context():
    """Clear conversation context for current session."""
    if 'session_id' in session:
        session_id = session['session_id']
        if conversation_manager:
            conversation_manager.delete(session_id)
        session.pop('session_id', None)
    return jsonify({"status": "context cleared"})

@app.route('/health')
def health():
    """Health check endpoint."""
    ai_available = AI_AGENT_AVAILABLE and ai_agent and ai_agent.is_available() if AI_AGENT_AVAILABLE else False
    return jsonify({
        "status": "healthy",
        "service": "database-context-chatbot",
        "ai_agent_available": ai_available
    })

if __name__ == '__main__':
    port = int(os.getenv('WEB_PORT', 3000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
