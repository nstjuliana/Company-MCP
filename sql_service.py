"""
SQL Service Layer

Handles SQL generation from natural language queries and SQL execution
against PostgreSQL and Snowflake databases.

Security:
- Read-only queries enforced
- SQL injection prevention
- Query timeouts
- Row limits
- Query validation
"""

import os
import re
import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta

# Database connection imports
try:
    import psycopg2
    from psycopg2 import pool, sql
    from psycopg2.extras import RealDictCursor
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False
    psycopg2 = None

# Lazy import snowflake to avoid startup crashes
HAS_SNOWFLAKE = False
snowflake = None

def _try_import_snowflake():
    global HAS_SNOWFLAKE, snowflake
    if snowflake is not None:
        return HAS_SNOWFLAKE
    try:
        _try_import_snowflake()
        HAS_SNOWFLAKE = True
        return True
    except Exception as e:
        HAS_SNOWFLAKE = False
        snowflake = None
        print(f"Warning: Failed to import snowflake.connector: {e}")
        return False

# OpenRouter for SQL generation
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Configuration
MAX_QUERY_ROWS = 10000  # Maximum rows to return
QUERY_TIMEOUT_SECONDS = 30  # Query execution timeout
MAX_SQL_LENGTH = 50000  # Maximum SQL query length


class DatabaseConnectionManager:
    """Manages database connections for PostgreSQL and Snowflake."""
    
    def __init__(self):
        self.postgres_pool = None
        self.snowflake_connections = {}  # Simple connection cache
        
    def _get_postgres_connection(self) -> Optional[Any]:
        """Get PostgreSQL connection from pool."""
        if not HAS_POSTGRES:
            logger.error("PostgreSQL driver (psycopg2) not available. Install with: pip install psycopg2-binary")
            return None
            
        # Create connection pool if not exists
        if self.postgres_pool is None:
            try:
                # Try connection URL first (TEST_DATABASE_URL or POSTGRES_CONNECTION_STRING)
                conn_string = os.getenv("TEST_DATABASE_URL") or os.getenv("POSTGRES_CONNECTION_STRING")
                if not conn_string:
                    # Build from individual components
                    host = os.getenv("POSTGRES_HOST", "localhost")
                    port = os.getenv("POSTGRES_PORT", "5432")
                    database = os.getenv("POSTGRES_DATABASE", "postgres")
                    user = os.getenv("POSTGRES_USER", "postgres")
                    password = os.getenv("POSTGRES_PASSWORD", "")
                    
                    # Check if credentials are provided
                    if not password:
                        logger.warning("POSTGRES_PASSWORD not set. Connection may fail.")
                    
                    conn_string = f"host={host} port={port} dbname={database} user={user} password={password}"
                    logger.info(f"Creating PostgreSQL connection pool: host={host}, port={port}, database={database}, user={user}")
                else:
                    # Mask password in connection string for logging
                    masked_conn = re.sub(r'password=[^;]+', 'password=***', conn_string)
                    logger.info(f"Creating PostgreSQL connection pool from connection string: {masked_conn}")
                
                self.postgres_pool = psycopg2.pool.SimpleConnectionPool(
                    1, 5, conn_string
                )
                logger.info("PostgreSQL connection pool created successfully")
            except Exception as e:
                error_msg = str(e)
                if HAS_POSTGRES and hasattr(psycopg2, 'OperationalError') and isinstance(e, psycopg2.OperationalError):
                    logger.error(f"PostgreSQL connection failed (OperationalError): {error_msg}")
                    logger.error("Check: 1) Database is running, 2) Host/port are correct, 3) Credentials are valid")
                elif HAS_POSTGRES and hasattr(psycopg2, 'Error') and isinstance(e, psycopg2.Error):
                    logger.error(f"PostgreSQL connection error: {error_msg}")
                else:
                    logger.error(f"Unexpected error creating PostgreSQL connection pool: {error_msg}", exc_info=True)
                return None
        
        try:
            conn = self.postgres_pool.getconn()
            logger.debug("Successfully obtained PostgreSQL connection from pool")
            return conn
        except Exception as e:
            error_msg = str(e)
            if HAS_POSTGRES and hasattr(psycopg2, 'pool') and hasattr(psycopg2.pool, 'PoolError') and isinstance(e, psycopg2.pool.PoolError):
                logger.error(f"PostgreSQL connection pool error: {error_msg}. Pool may be exhausted.")
            else:
                logger.error(f"Error getting PostgreSQL connection from pool: {error_msg}", exc_info=True)
            return None
    
    def _return_postgres_connection(self, conn):
        """Return PostgreSQL connection to pool."""
        if self.postgres_pool and conn:
            try:
                self.postgres_pool.putconn(conn)
            except Exception:
                pass
    
    def _get_snowflake_connection(self) -> Optional[Any]:
        """Get Snowflake connection."""
        if not HAS_SNOWFLAKE:
            logger.error("Snowflake driver not available. Install with: pip install snowflake-connector-python")
            return None
        
        # Use cached connection if available and not expired
        cache_key = "default"
        if cache_key in self.snowflake_connections:
            conn, expiry = self.snowflake_connections[cache_key]
            if datetime.now() < expiry:
                try:
                    # Test connection
                    conn.cursor().execute("SELECT 1")
                    logger.debug("Using cached Snowflake connection")
                    return conn
                except Exception as e:
                    # Connection expired, remove from cache
                    logger.warning(f"Cached Snowflake connection expired: {e}. Creating new connection.")
                    del self.snowflake_connections[cache_key]
        
        try:
            # Try production env vars first, fall back to test env vars
            account = os.getenv("SNOWFLAKE_ACCOUNT") or os.getenv("SNOWFLAKE_TEST_ACCOUNT")
            user = os.getenv("SNOWFLAKE_USERNAME") or os.getenv("SNOWFLAKE_USER") or os.getenv("SNOWFLAKE_TEST_USERNAME")
            password = os.getenv("SNOWFLAKE_PASSWORD") or os.getenv("SNOWFLAKE_TEST_PASSWORD")
            warehouse = os.getenv("SNOWFLAKE_WAREHOUSE") or os.getenv("SNOWFLAKE_TEST_WAREHOUSE") or ""
            database = os.getenv("SNOWFLAKE_DATABASE") or os.getenv("SNOWFLAKE_TEST_DATABASE") or ""
            schema = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
            
            if not all([account, user, password]):
                missing = []
                if not account:
                    missing.append("SNOWFLAKE_ACCOUNT or SNOWFLAKE_TEST_ACCOUNT")
                if not user:
                    missing.append("SNOWFLAKE_USERNAME/USER or SNOWFLAKE_TEST_USERNAME")
                if not password:
                    missing.append("SNOWFLAKE_PASSWORD or SNOWFLAKE_TEST_PASSWORD")
                logger.error(f"Snowflake credentials missing. Required environment variables: {', '.join(missing)}")
                return None
            
            logger.info(f"Creating Snowflake connection: account={account}, user={user}, warehouse={warehouse}, database={database}, schema={schema}")
            if not _try_import_snowflake():
                raise Exception("Snowflake connector not available")
            conn = snowflake.connector.connect(
                account=account,
                user=user,
                password=password,
                warehouse=warehouse,
                database=database,
                schema=schema,
            )
            
            # Cache connection for 30 minutes
            expiry = datetime.now() + timedelta(minutes=30)
            self.snowflake_connections[cache_key] = (conn, expiry)
            logger.info("Snowflake connection created and cached successfully")
            
            return conn
        except Exception as e:
            error_msg = str(e)
            if _try_import_snowflake() and hasattr(snowflake.connector, 'errors'):
                if hasattr(snowflake.connector.errors, 'ProgrammingError') and isinstance(e, snowflake.connector.errors.ProgrammingError):
                    logger.error(f"Snowflake connection failed (ProgrammingError): {error_msg}")
                    logger.error("Check: 1) Account name is correct, 2) User has proper permissions, 3) Warehouse/database exist")
                elif hasattr(snowflake.connector.errors, 'DatabaseError') and isinstance(e, snowflake.connector.errors.DatabaseError):
                    logger.error(f"Snowflake connection failed (DatabaseError): {error_msg}")
                else:
                    logger.error(f"Unexpected error creating Snowflake connection: {error_msg}", exc_info=True)
            else:
                logger.error(f"Unexpected error creating Snowflake connection: {error_msg}", exc_info=True)
            return None
    
    def get_connection(self, database: str) -> Optional[Any]:
        """Get connection for specified database."""
        logger.debug(f"Requesting connection for database: {database}")
        if database == "postgres_production":
            conn = self._get_postgres_connection()
            if conn:
                logger.debug("PostgreSQL connection obtained successfully")
            else:
                logger.error("Failed to obtain PostgreSQL connection")
            return conn
        elif database == "snowflake_production":
            conn = self._get_snowflake_connection()
            if conn:
                logger.debug("Snowflake connection obtained successfully")
            else:
                logger.error("Failed to obtain Snowflake connection")
            return conn
        else:
            logger.error(f"Unsupported database type: {database}. Supported: postgres_production, snowflake_production")
            return None
    
    def close_all(self):
        """Close all connections."""
        if self.postgres_pool:
            self.postgres_pool.closeall()
        for conn, _ in self.snowflake_connections.values():
            try:
                conn.close()
            except Exception:
                pass
        self.snowflake_connections.clear()


# Global connection manager
_db_manager = DatabaseConnectionManager()


class SQLSecurityValidator:
    """Validates SQL queries for security."""
    
    # Dangerous SQL keywords that modify data
    DANGEROUS_KEYWORDS = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
        'TRUNCATE', 'GRANT', 'REVOKE', 'EXEC', 'EXECUTE', 'CALL'
    ]
    
    # Allowed SQL keywords for read-only queries
    ALLOWED_KEYWORDS = [
        'SELECT', 'WITH', 'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'RIGHT',
        'FULL', 'OUTER', 'ON', 'GROUP', 'BY', 'HAVING', 'ORDER', 'LIMIT',
        'OFFSET', 'UNION', 'EXCEPT', 'INTERSECT', 'DISTINCT', 'AS', 'AND',
        'OR', 'NOT', 'IN', 'EXISTS', 'LIKE', 'ILIKE', 'IS', 'NULL', 'CASE',
        'WHEN', 'THEN', 'ELSE', 'END', 'CAST', 'COUNT', 'SUM', 'AVG', 'MAX',
        'MIN', 'COALESCE', 'NULLIF', 'SUBSTRING', 'UPPER', 'LOWER', 'TRIM'
    ]
    
    @staticmethod
    def validate_read_only(sql: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that SQL is read-only.
        Returns (is_valid, error_message)
        """
        sql_upper = sql.upper().strip()
        
        # Check for dangerous keywords
        for keyword in SQLSecurityValidator.DANGEROUS_KEYWORDS:
            # Use word boundaries to avoid false positives
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, sql_upper):
                return False, f"Query contains forbidden keyword: {keyword}. Only read-only queries are allowed."
        
        # Must start with SELECT or WITH (CTE)
        if not (sql_upper.startswith('SELECT') or sql_upper.startswith('WITH')):
            return False, "Query must start with SELECT or WITH (CTE). Only read-only queries are allowed."
        
        # Check length
        if len(sql) > MAX_SQL_LENGTH:
            return False, f"Query exceeds maximum length of {MAX_SQL_LENGTH} characters."
        
        return True, None
    
    @staticmethod
    def sanitize_sql(sql: str) -> str:
        """Basic SQL sanitization (parameterized queries should be used instead)."""
        # Remove comments
        sql = re.sub(r'--.*', '', sql)
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
        
        # Remove multiple spaces
        sql = re.sub(r'\s+', ' ', sql)
        
        return sql.strip()


class SQLGenerator:
    """Generates SQL from natural language queries using OpenRouter with GPT-4o-mini."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        # Using GPT-4o-mini for fast, cost-effective SQL generation
        # Alternative: "anthropic/claude-3-haiku" for slightly higher quality
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        
        if HAS_OPENAI and self.api_key:
            # Use OpenAI client with OpenRouter endpoint
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = None
    
    def generate_sql(
        self,
        natural_language_query: str,
        schema_context: Dict[str, Any],
        database: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate SQL from natural language query.
        
        Args:
            natural_language_query: User's natural language question
            schema_context: Schema information (tables, columns, relationships)
            database: Target database name
            
        Returns:
            (sql_query, error_message)
        """
        if not self.client:
            return None, "OpenRouter API key not configured. Set OPENROUTER_API_KEY environment variable."
        
        # Build schema context string
        schema_text = self._format_schema_context(schema_context)
        
        # Build prompt
        prompt = self._build_sql_generation_prompt(
            natural_language_query,
            schema_text,
            database
        )
        
        try:
            logger.info(f"Generating SQL for query: {natural_language_query[:100]}...")
            logger.debug(f"Schema context: {len(schema_context.get('tables', []))} tables")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a SQL expert. Generate accurate, read-only SQL queries based on natural language questions and database schema information. Only generate SELECT queries. Do not include any explanations or markdown formatting, just the SQL query."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistent SQL
                max_tokens=2000
            )
            
            sql = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            sql = re.sub(r'^```sql\s*', '', sql, flags=re.IGNORECASE)
            sql = re.sub(r'^```\s*', '', sql)
            sql = re.sub(r'```\s*$', '', sql)
            sql = sql.strip()
            
            logger.debug(f"Generated SQL: {sql[:200]}..." if len(sql) > 200 else f"Generated SQL: {sql}")
            
            # Validate SQL
            is_valid, error = SQLSecurityValidator.validate_read_only(sql)
            if not is_valid:
                logger.warning(f"Generated SQL failed validation: {error}")
                return None, error
            
            logger.info("SQL generated and validated successfully")
            return sql, None
            
        except Exception as e:
            error_msg = f"Error generating SQL: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return None, error_msg
    
    def _format_schema_context(self, schema_context: Dict[str, Any]) -> str:
        """Format schema context into readable text."""
        lines = []
        
        # Database info
        if "database" in schema_context:
            lines.append(f"Database: {schema_context['database']}")
        
        # Tables
        if "tables" in schema_context:
            lines.append("\nRelevant Tables:")
            for table in schema_context["tables"]:
                table_name = table.get('name', 'unknown')
                schema = table.get('schema', '')
                database = schema_context.get('database', '')
                
                # Build qualified table name for display
                if schema:
                    if database == "snowflake_production":
                        db_name = os.getenv("SNOWFLAKE_DATABASE", "PRODUCTION")
                        qualified_name = f"{db_name}.{schema.upper()}.{table_name.upper()}"
                    else:
                        qualified_name = f"{schema}.{table_name}"
                else:
                    qualified_name = table_name
                
                lines.append(f"\nTable: {table_name}")
                if schema:
                    lines.append(f"  Schema: {schema}")
                    lines.append(f"  Qualified Name: {qualified_name}")
                if table.get('description'):
                    lines.append(f"  Description: {table['description']}")
                
                # Columns
                if table.get('columns'):
                    lines.append(f"  Columns (ONLY these columns exist in {table_name}):")
                    for col in table['columns']:
                        col_desc = f"    - {col.get('name', 'unknown')} ({col.get('type', 'unknown')})"
                        if col.get('description'):
                            col_desc += f": {col.get('description')}"
                        lines.append(col_desc)
                
                # Primary key
                if table.get('primary_key'):
                    lines.append(f"  Primary Key: {', '.join(table['primary_key'])}")
                
                # Foreign keys
                if table.get('foreign_keys'):
                    lines.append("  Foreign Keys:")
                    for fk in table['foreign_keys']:
                        lines.append(f"    - {fk.get('columns', [])} -> {fk.get('references', '')}")
        
        # Relationships
        if "relationships" in schema_context:
            lines.append("\nRelationships:")
            for rel in schema_context["relationships"]:
                lines.append(f"  - {rel}")
        
        return "\n".join(lines)
    
    def _build_sql_generation_prompt(
        self,
        query: str,
        schema_context: str,
        database: str
    ) -> str:
        """Build prompt for SQL generation."""
        return f"""Generate a SQL query to answer this question: "{query}"

Database: {database}

Schema Information:
{schema_context}

Requirements:
1. Generate a read-only SELECT query
2. CRITICAL: Only use columns that are EXPLICITLY listed under each table in the schema above. Do NOT assume columns exist - if a column is not listed for a table, it does not exist in that table.
3. Use proper table and column names from the schema
4. IMPORTANT: Use schema-qualified table names (e.g., 'public.merchants' for PostgreSQL, 'PRODUCTION.PUBLIC.MERCHANTS' for Snowflake) when schema information is provided
5. Include appropriate JOINs if multiple tables are needed
6. Use proper SQL syntax for {database}
7. Add LIMIT if the query might return many rows (suggested: LIMIT 10000)
8. Return only the SQL query, no explanations

SQL Query:"""


class SQLExecutor:
    """Executes SQL queries against databases."""
    
    def __init__(self, db_manager: DatabaseConnectionManager):
        self.db_manager = db_manager
    
    def execute_query(
        self,
        sql: str,
        database: str,
        limit: int = MAX_QUERY_ROWS,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Execute SQL query and return results.

        Args:
            sql: SQL query to execute
            database: Target database name
            limit: Maximum rows to return
            offset: Number of rows to skip (for pagination)

        Returns:
            Dict with 'success', 'data', 'columns', 'row_count', 'error', 'has_more'
        """
        # Validate SQL
        is_valid, error = SQLSecurityValidator.validate_read_only(sql)
        if not is_valid:
            return {
                "success": False,
                "error": error,
                "data": [],
                "columns": [],
                "row_count": 0
            }
        
        # Sanitize SQL
        sql = SQLSecurityValidator.sanitize_sql(sql)
        
        # Add LIMIT/OFFSET if not present and query might return many rows
        sql_upper = sql.upper()
        if 'LIMIT' not in sql_upper and limit > 0:
            # Simple check - if query has ORDER BY or GROUP BY, add LIMIT and OFFSET
            if 'ORDER BY' in sql_upper or 'GROUP BY' in sql_upper:
                if offset > 0:
                    sql = f"{sql.rstrip(';')} LIMIT {limit} OFFSET {offset}"
                else:
                    sql = f"{sql.rstrip(';')} LIMIT {limit}"
        
        conn = None
        try:
            logger.info(f"Executing query on database: {database}")
            logger.debug(f"SQL query: {sql[:200]}..." if len(sql) > 200 else f"SQL query: {sql}")
            
            conn = self.db_manager.get_connection(database)
            if not conn:
                error_msg = (
                    f"Could not connect to database '{database}'. "
                    "Possible causes: 1) Database credentials not configured (check environment variables like TEST_DATABASE_URL, POSTGRES_HOST, etc.), "
                    "2) Database server is not running or unreachable, "
                    "3) Network connectivity issues or firewall blocking access, "
                    "4) Invalid credentials or database name. "
                    f"For PostgreSQL: check TEST_DATABASE_URL or POSTGRES_* environment variables. "
                    f"For Snowflake: check SNOWFLAKE_* environment variables. "
                    "Check server logs for detailed error information."
                )
                logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg,
                    "data": [],
                    "columns": [],
                    "row_count": 0
                }
            
            # Execute query with timeout
            start_time = time.time()
            
            if database == "postgres_production":
                return self._execute_postgres(conn, sql, limit, offset, start_time)
            elif database == "snowflake_production":
                return self._execute_snowflake(conn, sql, limit, offset, start_time)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported database: {database}",
                    "data": [],
                    "columns": [],
                    "row_count": 0
                }
                
        except Exception as e:
            error_msg = f"Error executing query: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "error": error_msg,
                "data": [],
                "columns": [],
                "row_count": 0
            }
        finally:
            if conn and database == "postgres_production":
                self.db_manager._return_postgres_connection(conn)
            # Snowflake connections are cached, don't close here
    
    def _execute_postgres(
        self,
        conn: Any,
        sql: str,
        limit: int,
        offset: int,
        start_time: float
    ) -> Dict[str, Any]:
        """Execute query on PostgreSQL."""
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Set statement timeout
            cursor.execute(f"SET statement_timeout = {QUERY_TIMEOUT_SECONDS * 1000}")  # milliseconds
            
            # Execute query
            logger.debug("Executing PostgreSQL query")
            cursor.execute(sql)
            
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > QUERY_TIMEOUT_SECONDS:
                cursor.close()
                error_msg = f"Query timeout after {QUERY_TIMEOUT_SECONDS} seconds"
                logger.warning(error_msg)
                return {
                    "success": False,
                    "error": error_msg,
                    "data": [],
                    "columns": [],
                    "row_count": 0
                }
            
            # Fetch results
            rows = cursor.fetchmany(limit)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []

            # Check if there are more rows available (fetch one extra to check)
            has_more = False
            if len(rows) == limit:
                try:
                    extra_row = cursor.fetchone()
                    has_more = extra_row is not None
                except:
                    pass  # Ignore errors when checking for more rows

            # Convert rows to list of dicts
            data = [dict(row) for row in rows]

            cursor.close()
            elapsed = time.time() - start_time

            logger.info(f"PostgreSQL query executed successfully: {len(data)} rows returned in {elapsed:.3f}s")

            return {
                "success": True,
                "data": data,
                "columns": columns,
                "row_count": len(data),
                "execution_time": round(elapsed, 3),
                "has_more": has_more,
                "limit_used": limit,
                "offset_used": offset
            }
            
        except Exception as e:
            error_msg = f"PostgreSQL error: {str(e)}"
            if HAS_POSTGRES and hasattr(psycopg2, 'Error') and isinstance(e, psycopg2.Error):
                logger.error(error_msg, exc_info=True)
            else:
                logger.error(error_msg, exc_info=True)
            if cursor:
                cursor.close()
            return {
                "success": False,
                "error": error_msg,
                "data": [],
                "columns": [],
                "row_count": 0
            }
        except Exception as e:
            error_msg = f"Unexpected error executing PostgreSQL query: {str(e)}"
            logger.error(error_msg, exc_info=True)
            if cursor:
                cursor.close()
            return {
                "success": False,
                "error": error_msg,
                "data": [],
                "columns": [],
                "row_count": 0
            }
    
    def _execute_snowflake(
        self,
        conn: Any,
        sql: str,
        limit: int,
        offset: int,
        start_time: float
    ) -> Dict[str, Any]:
        """Execute query on Snowflake."""
        cursor = None
        try:
            cursor = conn.cursor()
            
            # Execute query
            logger.debug("Executing Snowflake query")
            cursor.execute(sql)
            
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > QUERY_TIMEOUT_SECONDS:
                cursor.close()
                error_msg = f"Query timeout after {QUERY_TIMEOUT_SECONDS} seconds"
                logger.warning(error_msg)
                return {
                    "success": False,
                    "error": error_msg,
                    "data": [],
                    "columns": [],
                    "row_count": 0
                }
            
            # Fetch results
            rows = cursor.fetchmany(limit)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []

            # Check if there are more rows available (fetch one extra to check)
            has_more = False
            if len(rows) == limit:
                try:
                    extra_row = cursor.fetchone()
                    has_more = extra_row is not None
                except:
                    pass  # Ignore errors when checking for more rows

            # Convert rows to list of dicts
            data = []
            for row in rows:
                data.append({col: val for col, val in zip(columns, row)})

            cursor.close()
            elapsed = time.time() - start_time

            logger.info(f"Snowflake query executed successfully: {len(data)} rows returned in {elapsed:.3f}s")

            return {
                "success": True,
                "data": data,
                "columns": columns,
                "row_count": len(data),
                "execution_time": round(elapsed, 3),
                "has_more": has_more,
                "limit_used": limit,
                "offset_used": offset
            }
            
        except Exception as e:
            error_msg = f"Snowflake error: {str(e)}"
            if _try_import_snowflake() and hasattr(snowflake.connector, 'errors'):
                if hasattr(snowflake.connector.errors, 'ProgrammingError') and isinstance(e, snowflake.connector.errors.ProgrammingError):
                    logger.error(f"Snowflake programming error: {error_msg}", exc_info=True)
                elif hasattr(snowflake.connector.errors, 'DatabaseError') and isinstance(e, snowflake.connector.errors.DatabaseError):
                    logger.error(f"Snowflake database error: {error_msg}", exc_info=True)
                else:
                    logger.error(f"Unexpected Snowflake error: {error_msg}", exc_info=True)
            else:
                logger.error(f"Unexpected Snowflake error: {error_msg}", exc_info=True)
            if cursor:
                cursor.close()
            return {
                "success": False,
                "error": error_msg,
                "data": [],
                "columns": [],
                "row_count": 0
            }
        except Exception as e:
            error_msg = f"Unexpected error executing Snowflake query: {str(e)}"
            logger.error(error_msg, exc_info=True)
            if cursor:
                cursor.close()
            return {
                "success": False,
                "error": error_msg,
                "data": [],
                "columns": [],
                "row_count": 0
            }


# Global instances
_sql_generator = SQLGenerator()
_sql_executor = SQLExecutor(_db_manager)


def generate_and_execute_sql(
    natural_language_query: str,
    schema_context: Dict[str, Any],
    database: str
) -> Dict[str, Any]:
    """
    High-level function: Generate SQL and execute it.
    
    Returns dict with:
    - success: bool
    - sql: generated SQL (for debugging, not shown to user)
    - data: query results
    - columns: column names
    - row_count: number of rows
    - error: error message if failed
    - execution_time: query execution time
    """
    # Validate database name - ADD NEW DATABASES HERE
    # To add support for a new database:
    # 1. Add database name to VALID_DATABASES
    # 2. Add connection method to DatabaseConnectionManager
    # 3. Add execution method to SQLExecutor (_execute_<database_name>)
    VALID_DATABASES = {"postgres_production", "snowflake_production"}
    original_database = database
    if database not in VALID_DATABASES:
        error_msg = (
            f"Invalid database name '{database}'. Valid databases are: {', '.join(VALID_DATABASES)}. "
            f"Received database name appears to be a domain name rather than a database name. "
            f"Please use 'postgres_production' or 'snowflake_production'."
        )
        logger.error(error_msg)
        # Try to correct: if it's a domain name, try to find the actual database
        # by checking schema_context or defaulting to postgres_production
        if "database" in schema_context and schema_context["database"] in VALID_DATABASES:
            database = schema_context["database"]
            logger.info(f"Corrected database from schema_context: '{original_database}' -> '{database}'")
        else:
            # Default to postgres_production
            database = "postgres_production"
            logger.warning(f"Invalid database name '{original_database}' detected. Defaulting to 'postgres_production'. "
                         f"Please ensure correct database name is passed.")
        # Update schema_context to reflect the corrected database
        schema_context["database"] = database
    
    # Generate SQL
    sql, error = _sql_generator.generate_sql(
        natural_language_query,
        schema_context,
        database
    )
    
    if error or not sql:
        return {
            "success": False,
            "error": error or "Failed to generate SQL",
            "sql": None,
            "data": [],
            "columns": [],
            "row_count": 0
        }
    
    # Execute SQL
    result = _sql_executor.execute_query(sql, database)
    
    # Add generated SQL to result (for internal use, not shown to user)
    result["sql"] = sql
    
    return result

