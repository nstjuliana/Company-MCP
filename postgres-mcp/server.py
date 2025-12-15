"""
PostgreSQL MCP Server - Read-only database access via SSE/HTTP transport.
Lightweight implementation compatible with FastMCP pattern.
"""
from fastmcp import FastMCP
import os
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

# PostgreSQL driver
try:
    import psycopg2
    import psycopg2.extras
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# MCP Server instance
mcp = FastMCP("PostgreSQL Database Server")

# Database configuration from environment
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "database": os.getenv("POSTGRES_DATABASE", "postgres"),
}


@contextmanager
def get_connection():
    """Get a database connection with automatic cleanup."""
    if not HAS_PSYCOPG2:
        raise RuntimeError("psycopg2 not installed. Install with: pip install psycopg2-binary")
    
    conn = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        dbname=DB_CONFIG["database"],
    )
    try:
        yield conn
    finally:
        conn.close()


def _is_read_only_query(sql: str) -> bool:
    """Check if a SQL query is read-only (SELECT only)."""
    # Normalize whitespace and convert to uppercase for checking
    normalized = " ".join(sql.upper().split())
    
    # List of forbidden keywords that indicate write operations
    forbidden = [
        "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE",
        "GRANT", "REVOKE", "COPY", "VACUUM", "REINDEX", "CLUSTER",
        "COMMENT", "SECURITY", "OWNER", "SET ROLE", "RESET ROLE",
    ]
    
    # Check for forbidden keywords at word boundaries
    for keyword in forbidden:
        if keyword in normalized.split():
            return False
    
    # Must start with SELECT, WITH, EXPLAIN, or SHOW
    allowed_starts = ["SELECT", "WITH", "EXPLAIN", "SHOW", "TABLE"]
    first_word = normalized.split()[0] if normalized.split() else ""
    
    return first_word in allowed_starts


# --- MCP Tools ---

@mcp.tool
def list_schemas() -> Dict[str, Any]:
    """
    List all schemas in the database.
    
    Returns:
        Dict with schemas list containing name and table_count.
    """
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        schema_name,
                        (SELECT COUNT(*) FROM information_schema.tables t 
                         WHERE t.table_schema = s.schema_name) as table_count
                    FROM information_schema.schemata s
                    WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
                    ORDER BY schema_name
                """)
                schemas = [dict(row) for row in cur.fetchall()]
                return {"schemas": schemas, "count": len(schemas)}
    except Exception as e:
        return {"error": str(e), "schemas": []}


@mcp.tool
def list_tables(schema: str = "synthetic") -> Dict[str, Any]:
    """
    List all tables in a schema.
    
    Args:
        schema: Schema name (default: synthetic).
    Returns:
        Dict with tables list containing name, type, and row estimate.
    """
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        t.table_name as name,
                        t.table_type as type,
                        COALESCE(s.n_live_tup, 0) as row_estimate
                    FROM information_schema.tables t
                    LEFT JOIN pg_stat_user_tables s 
                        ON s.schemaname = t.table_schema AND s.relname = t.table_name
                    WHERE t.table_schema = %s
                    ORDER BY t.table_name
                """, (schema,))
                tables = [dict(row) for row in cur.fetchall()]
                return {"schema": schema, "tables": tables, "count": len(tables)}
    except Exception as e:
        return {"error": str(e), "tables": []}


@mcp.tool
def describe_table(table: str, schema: str = "synthetic") -> Dict[str, Any]:
    """
    Get detailed schema information for a table.
    
    Args:
        table: Table name.
        schema: Schema name (default: synthetic).
    Returns:
        Dict with columns, primary_key, foreign_keys, and indexes.
    """
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # Get columns
                cur.execute("""
                    SELECT 
                        column_name as name,
                        data_type as type,
                        is_nullable = 'YES' as nullable,
                        column_default as default_value,
                        character_maximum_length as max_length
                    FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s
                    ORDER BY ordinal_position
                """, (schema, table))
                columns = [dict(row) for row in cur.fetchall()]
                
                # Get primary key
                cur.execute("""
                    SELECT a.attname as column_name
                    FROM pg_index i
                    JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                    JOIN pg_class c ON c.oid = i.indrelid
                    JOIN pg_namespace n ON n.oid = c.relnamespace
                    WHERE i.indisprimary AND n.nspname = %s AND c.relname = %s
                """, (schema, table))
                primary_key = [row["column_name"] for row in cur.fetchall()]
                
                # Get foreign keys
                cur.execute("""
                    SELECT
                        kcu.column_name,
                        ccu.table_schema AS foreign_schema,
                        ccu.table_name AS foreign_table,
                        ccu.column_name AS foreign_column
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                        AND ccu.table_schema = tc.table_schema
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                        AND tc.table_schema = %s
                        AND tc.table_name = %s
                """, (schema, table))
                foreign_keys = [dict(row) for row in cur.fetchall()]
                
                # Get indexes
                cur.execute("""
                    SELECT
                        i.relname as index_name,
                        array_agg(a.attname ORDER BY array_position(ix.indkey, a.attnum)) as columns,
                        ix.indisunique as is_unique
                    FROM pg_class t
                    JOIN pg_namespace n ON n.oid = t.relnamespace
                    JOIN pg_index ix ON t.oid = ix.indrelid
                    JOIN pg_class i ON i.oid = ix.indexrelid
                    JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
                    WHERE n.nspname = %s AND t.relname = %s
                    GROUP BY i.relname, ix.indisunique
                """, (schema, table))
                indexes = [dict(row) for row in cur.fetchall()]
                
                return {
                    "table": table,
                    "schema": schema,
                    "columns": columns,
                    "primary_key": primary_key,
                    "foreign_keys": foreign_keys,
                    "indexes": indexes,
                }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def execute_query(sql: str, limit: int = 100) -> Dict[str, Any]:
    """
    Execute a read-only SQL query against the database.
    Only SELECT, WITH, EXPLAIN, SHOW, and TABLE statements are allowed.
    
    Args:
        sql: SQL query to execute (read-only).
        limit: Maximum rows to return (default: 100, max: 1000).
    Returns:
        Dict with columns, rows, row_count, and limited flag.
    """
    # Validate read-only
    if not _is_read_only_query(sql):
        return {
            "error": "Only read-only queries are allowed (SELECT, WITH, EXPLAIN, SHOW, TABLE).",
            "rows": [],
            "row_count": 0,
        }
    
    # Enforce limit
    limit = max(1, min(limit, 1000))
    
    try:
        with get_connection() as conn:
            # Set statement timeout for safety (30 seconds)
            with conn.cursor() as timeout_cur:
                timeout_cur.execute("SET statement_timeout = '30s'")
            
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql)
                
                # Get column names
                columns = [desc[0] for desc in cur.description] if cur.description else []
                
                # Fetch limited rows
                rows = []
                for i, row in enumerate(cur):
                    if i >= limit:
                        break
                    # Convert row to serializable dict
                    rows.append({k: _serialize_value(v) for k, v in dict(row).items()})
                
                # Check if there are more rows
                has_more = cur.fetchone() is not None if len(rows) == limit else False
                
                return {
                    "columns": columns,
                    "rows": rows,
                    "row_count": len(rows),
                    "limited": has_more,
                    "limit_applied": limit,
                }
    except psycopg2.Error as e:
        return {"error": f"Database error: {e.pgerror or str(e)}", "rows": [], "row_count": 0}
    except Exception as e:
        return {"error": str(e), "rows": [], "row_count": 0}


def _serialize_value(value) -> Any:
    """Convert database values to JSON-serializable types."""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [_serialize_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _serialize_value(v) for k, v in value.items()}
    # Convert other types to string
    return str(value)


@mcp.tool
def search_tables(query: str, schema: str = "") -> Dict[str, Any]:
    """
    Search for tables by name pattern.
    
    Args:
        query: Search pattern (supports % wildcard).
        schema: Optional schema filter.
    Returns:
        Dict with matching tables.
    """
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                search_pattern = f"%{query}%"
                
                if schema:
                    cur.execute("""
                        SELECT 
                            table_schema as schema,
                            table_name as name,
                            table_type as type
                        FROM information_schema.tables
                        WHERE table_name ILIKE %s
                            AND table_schema = %s
                            AND table_schema NOT IN ('pg_catalog', 'information_schema')
                        ORDER BY table_schema, table_name
                        LIMIT 50
                    """, (search_pattern, schema))
                else:
                    cur.execute("""
                        SELECT 
                            table_schema as schema,
                            table_name as name,
                            table_type as type
                        FROM information_schema.tables
                        WHERE table_name ILIKE %s
                            AND table_schema NOT IN ('pg_catalog', 'information_schema')
                        ORDER BY table_schema, table_name
                        LIMIT 50
                    """, (search_pattern,))
                
                tables = [dict(row) for row in cur.fetchall()]
                return {"query": query, "tables": tables, "count": len(tables)}
    except Exception as e:
        return {"error": str(e), "tables": []}


@mcp.tool
def get_sample_data(table: str, schema: str = "synthetic", limit: int = 5) -> Dict[str, Any]:
    """
    Get sample rows from a table.
    
    Args:
        table: Table name.
        schema: Schema name (default: synthetic).
        limit: Number of sample rows (default: 5, max: 20).
    Returns:
        Dict with columns and sample rows.
    """
    limit = max(1, min(limit, 20))
    
    # Use identifier quoting to prevent SQL injection
    sql = f'SELECT * FROM "{schema}"."{table}" LIMIT %s'
    
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql, (limit,))
                columns = [desc[0] for desc in cur.description] if cur.description else []
                rows = [{k: _serialize_value(v) for k, v in dict(row).items()} for row in cur.fetchall()]
                
                return {
                    "table": table,
                    "schema": schema,
                    "columns": columns,
                    "rows": rows,
                    "row_count": len(rows),
                }
    except Exception as e:
        return {"error": str(e), "rows": []}


@mcp.tool
def get_table_stats(table: str, schema: str = "synthetic") -> Dict[str, Any]:
    """
    Get statistics for a table (row count, size, etc.).
    
    Args:
        table: Table name.
        schema: Schema name (default: synthetic).
    Returns:
        Dict with row_count, table_size, index_size, and last_vacuum.
    """
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT
                        COALESCE(s.n_live_tup, 0) as row_count,
                        pg_size_pretty(pg_total_relation_size(c.oid)) as total_size,
                        pg_size_pretty(pg_relation_size(c.oid)) as table_size,
                        pg_size_pretty(pg_indexes_size(c.oid)) as index_size,
                        s.last_vacuum,
                        s.last_autovacuum,
                        s.last_analyze
                    FROM pg_class c
                    JOIN pg_namespace n ON n.oid = c.relnamespace
                    LEFT JOIN pg_stat_user_tables s 
                        ON s.schemaname = n.nspname AND s.relname = c.relname
                    WHERE n.nspname = %s AND c.relname = %s
                """, (schema, table))
                
                row = cur.fetchone()
                if row:
                    result = dict(row)
                    # Convert timestamps to strings
                    for key in ["last_vacuum", "last_autovacuum", "last_analyze"]:
                        if result.get(key):
                            result[key] = str(result[key])
                    return {"table": table, "schema": schema, **result}
                else:
                    return {"error": f"Table {schema}.{table} not found"}
    except Exception as e:
        return {"error": str(e)}


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
def test_connection() -> Dict[str, Any]:
    """
    Test the database connection.
    
    Returns:
        Dict with connection status and database info.
    """
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT version(), current_database(), current_user")
                row = cur.fetchone()
                return {
                    "connected": True,
                    "version": row["version"],
                    "database": row["current_database"],
                    "user": row["current_user"],
                    "host": DB_CONFIG["host"],
                }
    except Exception as e:
        return {"connected": False, "error": str(e)}


if __name__ == "__main__":
    port = int(os.getenv("MCP_PORT", "8000"))
    print(f"Starting PostgreSQL MCP server on port {port}...")
    print(f"Database: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    print(f"User: {DB_CONFIG['user']}")
    mcp.run(transport="http", host="0.0.0.0", port=port)

