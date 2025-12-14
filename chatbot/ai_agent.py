"""
AI Agent for Database Context Chatbot

This module implements an AI-driven agent that orchestrates MCP tools
to answer user questions. The AI decides which tools to call, executes
them, and generates natural language responses from the results.

Flow:
User Question → AI (with context) → AI decides tools → Execute tools →
AI receives results → AI generates response → Return
"""

import os
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
        
        # Define available MCP tools as functions for AI
        self.tool_definitions = self._define_tools()
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define MCP tools as function schemas for AI function calling."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "answer_question",
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
                    "name": "get_table_schema",
                    "description": "Get detailed schema information for a specific table including columns, types, and relationships. Use when user asks about table structure, columns, fields, or schema.",
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
                            },
                            "include_samples": {
                                "type": "boolean",
                                "description": "Include sample data values",
                                "default": False
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

1. DATA QUESTIONS → Use answer_question tool
   - "How many merchants?" → answer_question
   - "Name all 30" (after asking how many merchants) → answer_question with expanded query "list all merchant names"
   - "Show me all payments" → answer_question
   - "What is the total revenue?" → answer_question
   - "List all users" → answer_question
   - Any question asking for actual data values → answer_question

2. SCHEMA QUESTIONS → Use appropriate schema tools
   - "What tables exist?" → list_tables
   - "Find tables about payments" → search_tables
   - "What are the columns in the merchants table?" → get_table_schema
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
                        
                        # Call the MCP tool
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

                        # Store data entities for follow-up queries if this is answer_question
                        if function_name == "answer_question" and context_manager and tool_result.get("success"):
                            self._store_data_entities_from_result(tool_result, context_manager)
                        
                        # Capture SQL from answer_question tool results
                        if function_name == "answer_question":
                            # Check if tool_result is a dict
                            if isinstance(tool_result, dict):
                                sql = tool_result.get("sql")
                                # Check if SQL exists and is not empty
                                if sql and isinstance(sql, str) and sql.strip():
                                    sql_queries.append(sql)
                                    logger.info(f"✓ Captured SQL query ({len(sql)} chars) from answer_question")
                                else:
                                    # Log the actual keys to debug
                                    logger.warning(f"✗ answer_question returned no SQL. SQL value: {repr(sql)}")
                                    logger.warning(f"  Result keys: {list(tool_result.keys())}")
                                    logger.debug(f"  Full result (first 500 chars): {str(tool_result)[:500]}")
                            else:
                                logger.warning(f"✗ answer_question returned non-dict result: {type(tool_result)}")

                        # Add tool result to messages
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
            result: Result from answer_question tool
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

