"""
AI Agent for Database Context Chatbot

This module implements an AI-driven agent that orchestrates MCP tools
to answer user questions. The AI decides which tools to call, executes
them, and generates natural language responses from the results.

Architecture:
- MCP provides schema context only (no SQL generation/execution)
- Agent uses sql_service directly for SQL operations
- Schema context is filtered and lightweight to avoid token overflow

Flow:
User Question → AI (with context) → AI decides tools → Execute tools →
AI receives results → AI generates response → Return
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime

# OpenRouter/OpenAI client
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# SQL Service - direct import for SQL generation and execution
# Note: ai_agent.py is in chatbot/ subdirectory, sql_service.py is in parent directory
# Add parent directory to sys.path before importing
try:
    _current_dir = os.path.dirname(os.path.abspath(__file__))
    _parent_dir = os.path.dirname(_current_dir)
    if _parent_dir not in sys.path:
        sys.path.insert(0, _parent_dir)
    from sql_service import _sql_generator, _sql_executor
    HAS_SQL_SERVICE = True
except ImportError as e:
    HAS_SQL_SERVICE = False
    _sql_generator = None
    _sql_executor = None
    # Log the import error for debugging
    print(f"Warning: Could not import sql_service in ai_agent.py: {e}")

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


class AIAgent:
    """
    AI agent that uses MCP tools to answer questions.
    
    The agent receives user questions, decides which tools to call,
    executes them, and generates natural language responses.
    
    Architecture:
    - MCP: Schema context only (search_tables, list_columns, etc.)
    - SQL Service: Direct calls for SQL generation and execution
    - Lightweight schema: Only table+column names+types (no descriptions)
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        # Using GPT-4o-mini for fast, cost-effective function calling
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        
        if HAS_OPENAI and self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = None
        
        # Define available tools for AI
        self.tool_definitions = self._define_tools()
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """
        Define tools as function schemas for AI function calling.
        
        Note: 'data_question' is handled internally by the agent (not via MCP).
        Other tools are MCP calls.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "data_question",
                    "description": "Answer a data question by generating and executing SQL. Use this for ANY question about actual data values including: counts ('how many'), lists ('name all', 'show me all', 'list all'), aggregations (sum, average, max, min), or any question asking about what's in the database. This is the primary tool for data questions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The natural language question to answer. IMPORTANT: Expand the question with context from conversation history. For example, if user previously asked 'how many merchants' and got 30, and now asks 'name all 30', expand to 'list all 30 merchant names'."
                            },
                            "database": {
                                "type": "string",
                                "description": "Target database. Leave empty for auto-detection.",
                                "enum": ["", "postgres_production", "snowflake_production"]
                            }
                        },
                        "required": ["question"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_tables",
                    "description": "Search for tables by topic/keyword. Use ONLY when user explicitly asks to find or search for tables, or asks what tables exist for a topic. Do NOT use for data questions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query for finding relevant tables"
                            },
                            "database": {
                                "type": "string",
                                "description": "Filter by database",
                                "enum": ["", "postgres_production", "snowflake_production"]
                            },
                            "domain": {
                                "type": "string",
                                "description": "Filter by business domain",
                                "enum": ["", "authentication", "payments", "realtime", "security", "storage", "workflow"]
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results (default: 5)",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_columns",
                    "description": "Get column names and types for a specific table. Use when user asks about table columns or fields. This is a lightweight call.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "table": {
                                "type": "string",
                                "description": "Name of the table to get columns for"
                            },
                            "database": {
                                "type": "string",
                                "description": "Database containing the table",
                                "enum": ["", "postgres_production", "snowflake_production"]
                            }
                        },
                        "required": ["table"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "paginate_query",
                    "description": "Get a specific page of results from a previous large query. Use when user wants to see more data or navigate to different pages.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "integer",
                                "description": "Page number to retrieve (1-based)",
                                "minimum": 1
                            },
                            "page_size": {
                                "type": "integer",
                                "description": "Number of rows per page (default: 50, max: 100)",
                                "default": 50,
                                "minimum": 10,
                                "maximum": 100
                            },
                            "sql": {
                                "type": "string",
                                "description": "The SQL query to paginate (from previous query result)"
                            },
                            "database": {
                                "type": "string",
                                "description": "Target database",
                                "enum": ["postgres_production", "snowflake_production"]
                            }
                        },
                        "required": ["page", "sql", "database"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_table_schema",
                    "description": "Get full schema details for a table. Use only when user asks for complete schema information including relationships, indexes, and constraints. For basic column info, use list_columns instead.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "table": {
                                "type": "string",
                                "description": "Name of the table to get schema for"
                            },
                            "database": {
                                "type": "string",
                                "description": "Database containing the table",
                                "enum": ["", "postgres_production", "snowflake_production"]
                            }
                        },
                        "required": ["table"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_databases",
                    "description": "List all available databases. Use when user asks what databases are available.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_domains",
                    "description": "List business domains (e.g., payments, authentication). Use when user asks about domains or business areas.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "database": {
                                "type": "string",
                                "description": "Filter by database",
                                "enum": ["", "postgres_production", "snowflake_production"]
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tables",
                    "description": "List tables in a database or domain. Use when user asks to list or show tables.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "database": {
                                "type": "string",
                                "description": "Filter by database",
                                "enum": ["", "postgres_production", "snowflake_production"]
                            },
                            "domain": {
                                "type": "string",
                                "description": "Filter by business domain",
                                "enum": ["", "authentication", "payments", "realtime", "security", "storage", "workflow"]
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_domain_overview",
                    "description": "Get overview of a business domain including all tables and their purposes. Use when user asks for domain overview or summary.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "domain": {
                                "type": "string",
                                "description": "Domain name to get overview for",
                                "enum": ["authentication", "payments", "realtime", "security", "storage", "workflow"]
                            },
                            "database": {
                                "type": "string",
                                "description": "Filter by database",
                                "enum": ["", "postgres_production", "snowflake_production"]
                            }
                        },
                        "required": ["domain"]
                    }
                }
            }
        ]
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI agent."""
        return """You are a helpful database assistant that answers questions about data and database schemas.

CRITICAL RULES FOR TOOL USAGE:

1. DATA QUESTIONS → Use data_question tool
   - "How many merchants?" → data_question
   - "Name all 30" (after asking how many merchants) → data_question with expanded query "list all merchant names"
   - "Show me all payments" → data_question
   - "What is the total revenue?" → data_question
   - "List all users" → data_question
   - Any question asking for actual data values → data_question

2. SCHEMA QUESTIONS → Use appropriate schema tools
   - "What tables exist?" → list_tables
   - "Find tables about payments" → search_tables
   - "What columns are in the merchants table?" → list_columns (lightweight)
   - "Show me the full schema for merchants" → get_table_schema (detailed)
   - "What databases are available?" → list_databases

3. CONTEXT HANDLING:
   - Always consider conversation history when interpreting questions
   - Expand ambiguous queries using context (e.g., "all 30" → "all 30 merchants")
   - If the user refers to something from a previous message, include that context
   - For follow-up questions like "more details", "tell me about that", use stored data entities
   - Reference specific values from previous queries when generating SQL

4. RESPONSE FORMATTING:
   - Provide clear, natural language answers
   - For data results, present them in a readable format
   - For lists, use bullet points or tables as appropriate
   - Keep responses concise but complete

5. ERROR HANDLING:
   - If a tool fails, explain what went wrong clearly
   - Suggest alternative approaches if possible
   - Don't show raw error messages to users

Remember: Your goal is to ANSWER the user's question, not just show them where to find information."""
    
    def _build_lightweight_schema(
        self,
        tables: List[Dict[str, Any]],
        mcp_tool_caller: Callable,
        database: str
    ) -> Dict[str, Any]:
        """
        Build lightweight schema context with only table names, column names, and types.
        This dramatically reduces token usage compared to full schema.
        
        Args:
            tables: List of table info from search_tables
            mcp_tool_caller: Function to call MCP tools
            database: Target database
            
        Returns:
            Lightweight schema context dict
        """
        schema_context = {
            "database": database,
            "tables": []
        }
        
        # Limit to top 3 most relevant tables
        for table_info in tables[:3]:
            table_name = table_info.get("name", "")
            if not table_name:
                continue
            
            # Get columns using list_columns (lightweight MCP call)
            try:
                columns_result = mcp_tool_caller("list_columns", table=table_name, database=database)
                columns = columns_result.get("columns", [])
            except Exception as e:
                logger.warning(f"Failed to get columns for {table_name}: {e}")
                columns = []
            
            # Build minimal column list: just name and type
            minimal_columns = []
            for col in columns:
                minimal_columns.append({
                    "name": col.get("name", ""),
                    "type": col.get("type", "")
                })
            
            schema_context["tables"].append({
                "name": table_name,
                "columns": minimal_columns
            })
        
        return schema_context
    
    def _handle_data_question(
        self,
        question: str,
        database: str,
        mcp_tool_caller: Callable,
        step_updater: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """
        Handle data questions by:
        1. Finding relevant tables via MCP (search_tables)
        2. Getting lightweight column info via MCP (list_columns)
        3. Generating SQL via sql_service
        4. Executing SQL via sql_service
        
        Args:
            question: Natural language question
            database: Target database (may be empty for auto-detect)
            mcp_tool_caller: Function to call MCP tools
            step_updater: Optional callback for UI status updates
            
        Returns:
            Dict with success, data, columns, row_count, sql, error
        """
        if not HAS_SQL_SERVICE or not _sql_generator or not _sql_executor:
            logger.error(f"SQL service not available: HAS_SQL_SERVICE={HAS_SQL_SERVICE}, "
                        f"_sql_generator={_sql_generator is not None}, "
                        f"_sql_executor={_sql_executor is not None}")
            return {
                "success": False,
                "error": "SQL service not available. Check sql_service.py and dependencies.",
                "data": [],
                "columns": [],
                "row_count": 0,
                "sql": None
            }
        
        # Step 1: Find relevant tables using MCP
        if step_updater:
            step_updater("Finding relevant tables...")
        
        # Auto-detect database if not specified
        if not database:
            database = "postgres_production"  # Default
        
        logger.info(f"Data question: {question[:100]}... | Database: {database}")
        
        try:
            search_result = mcp_tool_caller("search_tables", query=question, database=database, limit=5)
            tables = search_result.get("tables", [])
            
            if not tables:
                # Try without database filter
                search_result = mcp_tool_caller("search_tables", query=question, limit=5)
                tables = search_result.get("tables", [])
                if tables:
                    # Use database from first result
                    database = tables[0].get("database", "postgres_production")
            
            logger.info(f"Found {len(tables)} relevant tables")
        except Exception as e:
            logger.error(f"Error searching tables: {e}")
            return {
                "success": False,
                "error": f"Failed to find relevant tables: {str(e)}",
                "data": [],
                "columns": [],
                "row_count": 0,
                "sql": None
            }
        
        if not tables:
            return {
                "success": False,
                "error": f"No relevant tables found for your question. Database: {database}",
                "data": [],
                "columns": [],
                "row_count": 0,
                "sql": None
            }
        
        # Step 2: Build lightweight schema context
        if step_updater:
            step_updater("Building schema context...")
        
        schema_context = self._build_lightweight_schema(tables, mcp_tool_caller, database)
        
        if not schema_context["tables"]:
            return {
                "success": False,
                "error": "Failed to build schema context for relevant tables.",
                "data": [],
                "columns": [],
                "row_count": 0,
                "sql": None
            }
        
        logger.info(f"Schema context: {len(schema_context['tables'])} tables, "
                   f"{sum(len(t['columns']) for t in schema_context['tables'])} columns")
        
        # Step 3: Generate SQL using sql_service
        if step_updater:
            step_updater("Generating SQL...")
        
        try:
            sql, error = _sql_generator.generate_sql(question, schema_context, database)
            
            if error or not sql:
                logger.error(f"SQL generation failed: {error}")
                return {
                    "success": False,
                    "error": error or "Failed to generate SQL query.",
                    "data": [],
                    "columns": [],
                    "row_count": 0,
                    "sql": None
                }
            
            logger.info(f"Generated SQL: {sql[:100]}...")
        except Exception as e:
            logger.error(f"Exception during SQL generation: {e}")
            return {
                "success": False,
                "error": f"SQL generation error: {str(e)}",
                "data": [],
                "columns": [],
                "row_count": 0,
                "sql": None
            }
        
        # Step 4: Execute SQL using sql_service
        if step_updater:
            step_updater("Executing query...")

        try:
            # Smart result limiting based on query intent and data size
            result = self._execute_query_with_smart_limits(sql, database, question)
            result["sql"] = sql  # Include SQL in result

            if result.get("success"):
                logger.info(f"Query executed: {result.get('row_count', 0)} rows returned")
            else:
                logger.error(f"Query execution failed: {result.get('error')}")

            return result
        except Exception as e:
            logger.error(f"Exception during SQL execution: {e}")
            return {
                "success": False,
                "error": f"SQL execution error: {str(e)}",
                "data": [],
                "columns": [],
                "row_count": 0,
                "sql": sql
            }

    def _execute_query_with_smart_limits(self, sql: str, database: str, question: str) -> Dict[str, Any]:
        """
        Execute query with intelligent limits and summarization to avoid token overflow.

        Strategy:
        - For aggregate/summary queries: Full results (unlimited)
        - For detailed queries: Smart sampling when > 50 rows
        - For count queries: Full results (typically 1 row)
        - For "all" queries: Summary + sample, not full dataset

        Args:
            sql: SQL query to execute
            database: Target database
            question: Original user question for intent analysis

        Returns:
            Query result with smart limiting applied
        """
        question_lower = question.lower()

        # Always allow full results for aggregate queries
        aggregate_keywords = ['count', 'sum', 'avg', 'average', 'total', 'max', 'min', 'group by']
        if any(keyword in question_lower for keyword in aggregate_keywords):
            logger.info("Detected aggregate query - allowing full results")
            return _sql_executor.execute_query(sql, database, limit=MAX_QUERY_ROWS)

        # For count-only queries, always allow full results
        if 'select count' in sql.lower() and 'from' in sql.lower():
            logger.info("Detected count query - allowing full results")
            return _sql_executor.execute_query(sql, database, limit=MAX_QUERY_ROWS)

        # Execute with reasonable initial limit to check result size
        initial_limit = 100  # Quick check for data size
        initial_result = _sql_executor.execute_query(sql, database, limit=initial_limit)

        if not initial_result.get("success"):
            return initial_result

        row_count = initial_result.get("row_count", 0)

        # If small result set, return all data
        if row_count <= 50:
            logger.info(f"Small result set ({row_count} rows) - returning all data")
            return initial_result

        # Medium result set (51-500 rows): Return all but warn about size
        if row_count <= 500:
            logger.info(f"Medium result set ({row_count} rows) - returning all with size warning")
            full_result = _sql_executor.execute_query(sql, database, limit=MAX_QUERY_ROWS)
            if full_result.get("success"):
                full_result["size_warning"] = f"This query returned {row_count} rows. For large datasets, consider using summary queries."
            return full_result

        # Large result set (>500 rows): Offer pagination or summary
        logger.warning(f"Large result set ({row_count} rows) - offering pagination/summary options")

        # Get basic stats about the data
        columns = initial_result.get("columns", [])
        data_sample = initial_result.get("data", [])

        # Check if user specifically asked for "all" data
        if "all" in question_lower and ("transaction" in question_lower or "record" in question_lower):
            # User explicitly wants all data - provide paginated access
            logger.info("User requested 'all' data - providing paginated access")
            paginated_result = _sql_executor.execute_query(sql, database, limit=50, offset=0)  # First page
            paginated_result["data_truncated"] = True
            paginated_result["total_rows_available"] = row_count
            paginated_result["pagination_info"] = {
                "current_page": 1,
                "page_size": 50,
                "total_pages": (row_count + 49) // 50,  # Ceiling division
                "has_more": paginated_result.get("has_more", False)
            }
            paginated_result["message"] = f"This query returned {row_count} rows. Showing first 50 rows. Use pagination tools to navigate."
            return paginated_result
        else:
            # Provide summary with option to paginate
            summary_result = {
                "success": True,
                "data": [],  # Will be populated with summary
                "columns": ["metric", "value"],
                "row_count": 1,  # Summary is 1 row
                "sql": sql,
                "data_truncated": True,
                "total_rows_available": row_count,
                "sample_size": len(data_sample),
                "summary": self._create_data_summary(data_sample, columns, question),
                "pagination_available": True,
                "pagination_info": {
                    "page_size": 50,
                    "total_pages": (row_count + 49) // 50,
                    "message": f"Data too large to display fully. Use pagination to browse {row_count} rows in pages of 50."
                }
            }

            # Add sample data (first 5 rows) for user reference
            if data_sample:
                sample_data = data_sample[:5]
                summary_result["sample_data"] = sample_data
                summary_result["sample_columns"] = columns

            return summary_result

    def _create_data_summary(self, data_sample: List[Dict], columns: List[str], question: str) -> Dict[str, Any]:
        """
        Create intelligent summary of large datasets based on data types and user intent.

        Args:
            data_sample: Sample of the data (first 100 rows)
            columns: Column names
            question: Original user question

        Returns:
            Summary statistics and insights
        """
        if not data_sample or not columns:
            return {"error": "No data available for summarization"}

        summary = {
            "total_sample_rows": len(data_sample),
            "columns_analyzed": len(columns),
            "column_types": {},
            "numeric_columns": [],
            "date_columns": [],
            "insights": []
        }

        # Analyze column types and collect statistics
        for col in columns:
            values = [row.get(col) for row in data_sample if row.get(col) is not None]
            if not values:
                summary["column_types"][col] = "empty"
                continue

            # Detect column type
            sample_value = values[0]
            if isinstance(sample_value, (int, float)):
                summary["column_types"][col] = "numeric"
                summary["numeric_columns"].append(col)

                # Calculate basic stats for numeric columns
                numeric_values = [v for v in values if isinstance(v, (int, float))]
                if numeric_values:
                    summary[col] = {
                        "min": min(numeric_values),
                        "max": max(numeric_values),
                        "avg": round(sum(numeric_values) / len(numeric_values), 2),
                        "count": len(numeric_values)
                    }

            elif isinstance(sample_value, str) and self._looks_like_date(sample_value):
                summary["column_types"][col] = "date"
                summary["date_columns"].append(col)
            else:
                summary["column_types"][col] = "text"
                # For text columns, show unique value count
                unique_values = len(set(str(v) for v in values))
                summary[col] = {
                    "unique_values": unique_values,
                    "total_values": len(values)
                }

        # Generate insights based on question intent
        question_lower = question.lower()
        if "transaction" in question_lower:
            summary["insights"].append("💰 This appears to be transaction data")
            if summary["numeric_columns"]:
                summary["insights"].append(f"📊 Found {len(summary['numeric_columns'])} numeric columns that may contain amounts or quantities")
        elif "payment" in question_lower:
            summary["insights"].append("💳 This appears to be payment data")
        elif "user" in question_lower or "customer" in question_lower:
            summary["insights"].append("👥 This appears to be user/customer data")

        # Add general insights
        if summary["numeric_columns"]:
            summary["insights"].append(f"🔢 Numeric columns available: {', '.join(summary['numeric_columns'][:3])}{'...' if len(summary['numeric_columns']) > 3 else ''}")

        if summary["date_columns"]:
            summary["insights"].append(f"📅 Date columns available: {', '.join(summary['date_columns'][:3])}{'...' if len(summary['date_columns']) > 3 else ''}")

        return summary

    def _looks_like_date(self, value: str) -> bool:
        """Simple heuristic to detect date-like strings."""
        if not isinstance(value, str):
            return False

        # Common date patterns
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        ]

        return any(re.match(pattern, value) for pattern in date_patterns)

    def _create_compact_context_for_ai(self, tool_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a compact version of large query results for AI context to avoid token overflow.

        Args:
            tool_result: Original tool result with truncated data

        Returns:
            Compact version suitable for AI context
        """
        compact = {
            "success": tool_result.get("success", False),
            "row_count": tool_result.get("row_count", 0),
            "data_truncated": True,
            "total_rows_available": tool_result.get("total_rows_available", 0),
            "sample_size": tool_result.get("sample_size", 0),
        }

        # Include SQL if available
        if tool_result.get("sql"):
            compact["sql"] = tool_result["sql"]

        # Include summary statistics
        if tool_result.get("summary"):
            compact["summary"] = tool_result["summary"]

        # Include a small sample (max 3 rows) for AI to understand structure
        if tool_result.get("sample_data") and tool_result.get("sample_columns"):
            compact["sample_columns"] = tool_result["sample_columns"]
            compact["sample_data"] = tool_result["sample_data"][:3]  # Max 3 sample rows

        # Include error if present
        if tool_result.get("error"):
            compact["error"] = tool_result["error"]

        return compact

    def _handle_paginate_query(self, page: int, page_size: int, sql: str, database: str, step_updater=None) -> Dict[str, Any]:
        """
        Handle pagination requests for large datasets.

        Args:
            page: Page number (1-based)
            page_size: Rows per page (max 100)
            sql: SQL query to paginate
            database: Target database
            step_updater: Optional callback for UI status updates

        Returns:
            Paginated query results
        """
        if not HAS_SQL_SERVICE or not _sql_executor:
            return {
                "success": False,
                "error": "SQL service not available for pagination.",
                "data": [],
                "columns": [],
                "row_count": 0
            }

        # Validate inputs
        page = max(1, page)
        page_size = min(max(10, page_size), 100)  # Clamp between 10-100

        # Calculate offset
        offset = (page - 1) * page_size

        try:
            logger.info(f"Executing paginated query: page {page}, size {page_size}, offset {offset}")

            result = _sql_executor.execute_query(sql, database, limit=page_size, offset=offset)
            result["pagination_info"] = {
                "current_page": page,
                "page_size": page_size,
                "has_more": result.get("has_more", False)
            }

            if result.get("success"):
                logger.info(f"Pagination successful: returned {result.get('row_count', 0)} rows for page {page}")
            else:
                logger.error(f"Pagination failed: {result.get('error')}")

            return result

        except Exception as e:
            logger.error(f"Exception during pagination: {e}")
            return {
                "success": False,
                "error": f"Pagination error: {str(e)}",
                "data": [],
                "columns": [],
                "row_count": 0
            }

    def process_query(
        self,
        user_query: str,
        conversation_history: List[Dict[str, str]],
        mcp_tool_caller: Callable,
        context_manager: Optional[any] = None,
        step_updater: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """
        Process user query using AI agent with function calling.

        Args:
            user_query: User's question
            conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
            mcp_tool_caller: Function to call MCP tools
            context_manager: Conversation context manager for storing/retrieving data entities
            step_updater: Optional callback for UI status updates

        Returns:
            Dict with 'response' (str) and 'sql_queries' (list of executed SQL)
        """
        if not self.client:
            logger.error("AI agent not available. OPENROUTER_API_KEY not configured.")
            return {"response": "AI agent not available. Please configure OPENROUTER_API_KEY.", "sql_queries": []}

        # Track SQL queries executed during this request
        sql_queries = []

        # Build messages for AI
        messages = [
            {"role": "system", "content": self._get_system_prompt()}
        ]

        # Add conversation history (excluding current message)
        for msg in conversation_history:
            messages.append(msg)

        # Add context about stored data entities if available
        if context_manager:
            data_entities = context_manager.get_all_data_entities()
            if data_entities:
                context_prompt = "Available context from previous queries:\n"
                for entity_type, entity_data in data_entities.items():
                    context_prompt += f"- {entity_type}: {entity_data}\n"
                messages.append({"role": "system", "content": context_prompt})

        # Add current user query
        messages.append({"role": "user", "content": user_query})
        
        # Agentic loop - let AI call tools until it has final answer
        max_iterations = 10  # Safety limit
        iteration = 0
        
        logger.info(f"Processing user query: {user_query[:100]}...")
        logger.debug(f"Conversation history: {len(conversation_history)} messages")
        
        while iteration < max_iterations:
            iteration += 1
            logger.debug(f"AI agent iteration {iteration}/{max_iterations}")
            
            try:
                # Call AI with function calling
                logger.debug("Calling OpenRouter API for AI completion")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tool_definitions,
                    tool_choice="auto",
                    temperature=0.3,
                    max_tokens=4000
                )
                
                message = response.choices[0].message
                
                # Check if AI wants to call functions
                if message.tool_calls:
                    logger.info(f"AI requested {len(message.tool_calls)} tool call(s)")
                    # Add assistant message with tool calls to history
                    messages.append({
                        "role": "assistant",
                        "content": message.content or "",
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in message.tool_calls
                        ]
                    })
                    
                    # Execute each tool call
                    for tool_call in message.tool_calls:
                        function_name = tool_call.function.name
                        
                        try:
                            function_args = json.loads(tool_call.function.arguments)
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse tool arguments for {function_name}: {e}")
                            function_args = {}
                        
                        # Handle data_question and paginate_query internally (not via MCP)
                        if function_name == "data_question":
                            if step_updater:
                                step_updater("Processing data question...")
                            
                            logger.info(f"Handling data_question internally: {function_args}")
                            tool_result = self._handle_data_question(
                                question=function_args.get("question", user_query),
                                database=function_args.get("database", ""),
                                mcp_tool_caller=mcp_tool_caller,
                                step_updater=step_updater
                            )
                            
                            # Capture SQL
                            if tool_result.get("sql"):
                                sql_queries.append(tool_result["sql"])
                                logger.info(f"✓ Captured SQL query from data_question")
                            
                            # Store data entities for follow-up queries
                            if context_manager and tool_result.get("success"):
                                self._store_data_entities_from_result(tool_result, context_manager)

                        elif function_name == "paginate_query":
                            if step_updater:
                                step_updater("Getting paginated results...")

                            logger.info(f"Handling paginate_query internally: {function_args}")
                            tool_result = self._handle_paginate_query(
                                page=function_args.get("page", 1),
                                page_size=function_args.get("page_size", 50),
                                sql=function_args.get("sql", ""),
                                database=function_args.get("database", ""),
                                step_updater=step_updater
                            )
                        else:
                            # Call MCP tool
                            if step_updater:
                                tool_display_name = function_name.replace('_', ' ').title()
                                step_updater(f"Calling MCP...")
                            
                            logger.info(f"Calling MCP tool: {function_name} with args: {function_args}")
                            try:
                                tool_result = mcp_tool_caller(function_name, **function_args)
                                logger.debug(f"Tool {function_name} returned: success={tool_result.get('success', 'N/A')}")
                                
                                # Log errors from tool results
                                if isinstance(tool_result, dict) and not tool_result.get("success", True):
                                    error_msg = tool_result.get("error", "Unknown error")
                                    logger.error(f"Tool {function_name} failed: {error_msg}")
                            except Exception as tool_error:
                                logger.error(f"Exception calling tool {function_name}: {tool_error}", exc_info=True)
                                tool_result = {
                                    "success": False,
                                    "error": f"Exception calling tool: {str(tool_error)}"
                                }

                        # Handle large datasets intelligently for token management
                        if isinstance(tool_result, dict) and tool_result.get("data_truncated", False):
                            # For truncated results, create a compact summary for AI context
                            ai_context = self._create_compact_context_for_ai(tool_result)
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(ai_context, default=str, indent=2)
                            })
                        else:
                            # Normal handling for smaller results
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(tool_result, default=str, indent=2)
                            })
                    
                    # Continue loop to let AI process tool results
                    continue
                
                else:
                    # AI has final answer (no more tool calls)
                    response_text = message.content or "I couldn't generate a response."
                    logger.info(f"AI generated final response (length: {len(response_text)})")
                    return {"response": response_text, "sql_queries": sql_queries}
                    
            except Exception as e:
                logger.error(f"Error in AI agentic loop: {e}", exc_info=True)
                return {"response": f"I encountered an error while processing your request: {str(e)}", "sql_queries": sql_queries}
        
        # If we hit max iterations
        logger.warning(f"AI agent hit max iterations ({max_iterations}) without final answer")
        return {"response": "I'm having trouble processing that request. Please try rephrasing your question.", "sql_queries": sql_queries}
    
    def _store_data_entities_from_result(self, result: Dict[str, Any], context_manager):
        """
        Extract and store specific data entities from query results for follow-up queries.

        Args:
            result: Result from data question
            context_manager: Context manager to store entities
        """
        if not result.get("success") or not result.get("data"):
            return

        data = result.get("data", [])
        columns = result.get("columns", [])

        # Store different types of entities based on the data
        if len(data) == 1 and len(columns) == 1:
            # Single value result (like MAX(created_at))
            value = data[0].get(columns[0])
            if value:
                # Try to determine entity type from column name
                col_name = columns[0].lower()
                if "payment" in col_name or "amount" in col_name:
                    context_manager.store_data_entity("payment_value", value)
                elif "date" in col_name or "time" in col_name or "created" in col_name:
                    context_manager.store_data_entity("timestamp", value)
                elif "count" in col_name or "total" in col_name:
                    context_manager.store_data_entity("count", value)
        elif len(data) == 1:
            # Single row result - store the entire row
            row = data[0]
            # Try to determine entity type from data
            if "payment_id" in row:
                context_manager.store_data_entity("payment", row)
            elif "merchant_id" in row:
                context_manager.store_data_entity("merchant", row)
            elif "user_id" in row or "id" in row:
                context_manager.store_data_entity("record", row)

        # Always store the most recent query result for "that" references
        context_manager.store_data_entity("last_query_result", {
            "data": data,
            "columns": columns,
            "row_count": len(data)
        })

    def is_available(self) -> bool:
        """Check if AI agent is properly configured."""
        return self.client is not None


# Global AI agent instance
ai_agent = AIAgent()
