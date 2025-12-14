"""
Company MCP Frontend - FastAPI Backend
Provides web UI for MCP interaction, SFTP browsing, and documentation.
"""
import os
import json
import paramiko
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

# Configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://mcp-server:8000")
SFTP_HOST = os.getenv("SFTP_HOST", "sftp-server")
SFTP_PORT = int(os.getenv("SFTP_PORT", "22"))
SFTP_USER = os.getenv("SFTP_USER", "datauser")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD", "changeme")

# HTTP client for MCP communication
http_client: Optional[httpx.AsyncClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage HTTP client lifecycle."""
    global http_client
    http_client = httpx.AsyncClient(timeout=60.0)
    yield
    await http_client.aclose()


app = FastAPI(
    title="Company MCP Frontend",
    description="Web interface for Database Context MCP Server",
    lifespan=lifespan
)

# Mount static files
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ─────────────────────────────────────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []


class ToolCall(BaseModel):
    tool: str
    params: Dict[str, Any] = {}


# ─────────────────────────────────────────────────────────────────────────────
# Page Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main SPA page."""
    return templates.TemplateResponse("index.html", {"request": request})


# ─────────────────────────────────────────────────────────────────────────────
# API Routes - MCP Tools
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/mcp/health")
async def mcp_health():
    """Check MCP server connectivity."""
    try:
        response = await http_client.get(f"{MCP_SERVER_URL}/health")
        return {"status": "connected", "mcp_status": response.status_code}
    except Exception as e:
        return {"status": "disconnected", "error": str(e)}


@app.post("/api/mcp/tool")
async def call_mcp_tool(tool_call: ToolCall):
    """Call an MCP tool directly."""
    try:
        # FastMCP HTTP transport expects POST to /mcp with JSON-RPC format
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_call.tool,
                "arguments": tool_call.params
            }
        }
        
        response = await http_client.post(
            f"{MCP_SERVER_URL}/mcp",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        )
        
        result = response.json()
        
        if "error" in result:
            return JSONResponse(
                status_code=400,
                content={"error": result["error"]}
            )
        
        return result.get("result", result)
        
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"MCP server unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/mcp/tools")
async def list_mcp_tools():
    """List available MCP tools."""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        response = await http_client.post(
            f"{MCP_SERVER_URL}/mcp",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        )
        
        result = response.json()
        return result.get("result", result)
        
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# API Routes - Chat
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Process a chat message using MCP tools.
    This provides a simplified chat interface that routes queries to appropriate MCP tools.
    """
    message = request.message.lower()
    
    try:
        # Route based on message content
        if any(word in message for word in ["list", "show", "all"]) and "database" in message:
            result = await call_tool("list_databases", {})
            return format_chat_response("list_databases", result)
        
        elif any(word in message for word in ["list", "show", "all"]) and "table" in message:
            # Extract database if mentioned
            db = extract_database(message)
            result = await call_tool("list_tables", {"database": db} if db else {})
            return format_chat_response("list_tables", result)
        
        elif any(word in message for word in ["list", "show"]) and "domain" in message:
            result = await call_tool("list_domains", {})
            return format_chat_response("list_domains", result)
        
        elif "schema" in message or "column" in message:
            # Try to extract table name
            table = extract_table_name(message)
            if table:
                result = await call_tool("get_table_schema", {"table": table})
                return format_chat_response("get_table_schema", result)
            else:
                return {
                    "response": "Please specify a table name to get its schema. For example: 'Show schema for payments table'",
                    "tool_used": None
                }
        
        elif "join" in message and ("path" in message or "between" in message):
            # Extract table names for join path
            tables = extract_table_names(message)
            if len(tables) >= 2:
                result = await call_tool("get_join_path", {
                    "source_table": tables[0],
                    "target_table": tables[1]
                })
                return format_chat_response("get_join_path", result)
            else:
                return {
                    "response": "Please specify two table names for join path. For example: 'Find join path between merchants and payments'",
                    "tool_used": None
                }
        
        elif any(word in message for word in ["search", "find", "query"]):
            # Default to FTS search
            query = extract_search_query(message)
            if query:
                result = await call_tool("search_fts", {"query": query, "limit": 10})
                return format_chat_response("search_fts", result)
            else:
                result = await call_tool("search_tables", {"query": message, "limit": 5})
                return format_chat_response("search_tables", result)
        
        else:
            # Default: try semantic search
            result = await call_tool("search_tables", {"query": request.message, "limit": 5})
            return format_chat_response("search_tables", result)
    
    except HTTPException:
        raise
    except Exception as e:
        return {
            "response": f"I encountered an error processing your request: {str(e)}",
            "tool_used": None,
            "error": True
        }


async def call_tool(tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Helper to call MCP tool internally (returns dict, not JSONResponse)."""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool,
                "arguments": params
            }
        }
        
        response = await http_client.post(
            f"{MCP_SERVER_URL}/mcp",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        )
        
        result = response.json()
        
        if "error" in result:
            return {"error": str(result["error"])}
        
        # MCP returns result in content array for tool calls
        mcp_result = result.get("result", result)
        if isinstance(mcp_result, dict) and "content" in mcp_result:
            # Parse the text content from MCP response
            content = mcp_result.get("content", [])
            if content and isinstance(content, list) and len(content) > 0:
                text = content[0].get("text", "")
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {"response": text}
        
        return mcp_result
        
    except Exception as e:
        return {"error": str(e)}


def format_chat_response(tool: str, result: Any) -> Dict[str, Any]:
    """Format MCP tool result as a chat response."""
    if isinstance(result, dict) and "error" in result:
        return {
            "response": f"Error: {result['error']}",
            "tool_used": tool,
            "error": True
        }
    
    return {
        "response": format_result_as_markdown(tool, result),
        "tool_used": tool,
        "raw_result": result
    }


def format_result_as_markdown(tool: str, result: Any) -> str:
    """Convert tool result to readable markdown."""
    if tool == "list_databases":
        databases = result.get("databases", [])
        lines = ["### Available Databases\n"]
        for db in databases:
            lines.append(f"**{db['name']}** - {db['table_count']} tables")
            if db.get('domains'):
                lines.append(f"  - Domains: {', '.join(db['domains'])}")
        return "\n".join(lines)
    
    elif tool == "list_tables":
        tables = result if isinstance(result, list) else result.get("tables", [])
        lines = [f"### Tables ({len(tables)} found)\n"]
        for t in tables[:20]:  # Limit display
            name = t.get("name", t.get("id", "Unknown"))
            summary = t.get("summary", "")[:100]
            lines.append(f"- **{name}**: {summary}")
        if len(tables) > 20:
            lines.append(f"\n*...and {len(tables) - 20} more*")
        return "\n".join(lines)
    
    elif tool == "list_domains":
        domains = result.get("domains", [])
        lines = ["### Business Domains\n"]
        for d in domains:
            lines.append(f"- **{d['name']}**: {d['table_count']} tables")
        return "\n".join(lines)
    
    elif tool == "get_table_schema":
        if "error" in result:
            return f"Table not found: {result['error']}"
        lines = [f"### {result.get('name', 'Unknown')} Schema\n"]
        lines.append(f"**Database:** {result.get('database', 'N/A')}")
        lines.append(f"**Schema:** {result.get('schema', 'N/A')}")
        if result.get('description'):
            lines.append(f"\n{result['description']}\n")
        lines.append("\n**Columns:**\n")
        for col in result.get("columns", [])[:30]:
            nullable = "nullable" if col.get("nullable") else "not null"
            lines.append(f"- `{col['name']}` ({col.get('type', 'unknown')}, {nullable})")
            if col.get("description"):
                lines.append(f"  - {col['description'][:100]}")
        return "\n".join(lines)
    
    elif tool == "get_join_path":
        if not result.get("found"):
            return f"No join path found between {result.get('source')} and {result.get('target')}"
        lines = [f"### Join Path: {result['source']} → {result['target']}\n"]
        lines.append(f"**Hops:** {result.get('hop_count', 0)}")
        if result.get("sql_snippet"):
            lines.append(f"\n```sql\n{result['sql_snippet']}\n```")
        return "\n".join(lines)
    
    elif tool in ("search_fts", "search_tables", "search_vector"):
        results = result.get("results", result.get("tables", []))
        lines = [f"### Search Results ({len(results)} found)\n"]
        for r in results[:10]:
            name = r.get("name", r.get("table_name", "Unknown"))
            summary = r.get("summary", "")[:150]
            lines.append(f"- **{name}**: {summary}")
        return "\n".join(lines)
    
    # Default: pretty print JSON
    return f"```json\n{json.dumps(result, indent=2)}\n```"


def extract_database(message: str) -> Optional[str]:
    """Extract database name from message."""
    if "postgres" in message:
        return "postgres_production"
    if "snowflake" in message:
        return "snowflake_production"
    return None


def extract_table_name(message: str) -> Optional[str]:
    """Extract a single table name from message."""
    # Common table names to look for
    known_tables = [
        "payments", "merchants", "users", "sessions", "transactions",
        "dabstep_payments", "dabstep_tasks", "dabstep_submissions",
        "acquirer_countries", "fee_structures", "merchant_category_codes"
    ]
    message_lower = message.lower()
    for table in known_tables:
        if table in message_lower:
            return table
    return None


def extract_table_names(message: str) -> List[str]:
    """Extract multiple table names from message."""
    known_tables = [
        "payments", "merchants", "users", "sessions", "transactions",
        "dabstep_payments", "dabstep_tasks", "dabstep_submissions"
    ]
    found = []
    message_lower = message.lower()
    for table in known_tables:
        if table in message_lower:
            found.append(table)
    return found


def extract_search_query(message: str) -> Optional[str]:
    """Extract search query from message."""
    # Remove common prefixes
    prefixes = ["search for", "find", "query", "look for", "search"]
    result = message.lower()
    for prefix in prefixes:
        if result.startswith(prefix):
            result = result[len(prefix):].strip()
    return result if result else None


# ─────────────────────────────────────────────────────────────────────────────
# API Routes - SFTP File Browser
# ─────────────────────────────────────────────────────────────────────────────

def get_sftp_client():
    """Create SFTP connection."""
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)
    return paramiko.SFTPClient.from_transport(transport), transport


@app.get("/api/files")
async def list_files(path: str = "/data"):
    """List files in SFTP directory."""
    try:
        sftp, transport = get_sftp_client()
        try:
            # Ensure path starts with /data (user's accessible directory)
            if not path.startswith("/data"):
                path = f"/data{path}" if path.startswith("/") else f"/data/{path}"
            
            files = []
            for item in sftp.listdir_attr(path):
                is_dir = item.st_mode is not None and (item.st_mode & 0o40000)
                files.append({
                    "name": item.filename,
                    "path": f"{path}/{item.filename}".replace("//", "/"),
                    "size": item.st_size,
                    "modified": item.st_mtime,
                    "is_directory": bool(is_dir)
                })
            
            # Sort: directories first, then by name
            files.sort(key=lambda x: (not x["is_directory"], x["name"].lower()))
            
            return {
                "path": path,
                "files": files,
                "parent": "/".join(path.rstrip("/").split("/")[:-1]) or "/data"
            }
        finally:
            sftp.close()
            transport.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SFTP error: {str(e)}")


@app.get("/api/files/content")
async def get_file_content(path: str):
    """Get content of a file from SFTP."""
    try:
        sftp, transport = get_sftp_client()
        try:
            # Ensure path is within /data
            if not path.startswith("/data"):
                path = f"/data{path}" if path.startswith("/") else f"/data/{path}"
            
            # Check file size first
            stat = sftp.stat(path)
            if stat.st_size > 1024 * 1024:  # 1MB limit
                return {
                    "path": path,
                    "content": None,
                    "error": "File too large to display (>1MB)",
                    "size": stat.st_size
                }
            
            with sftp.open(path, "r") as f:
                content = f.read()
                # Try to decode as text
                if isinstance(content, bytes):
                    try:
                        content = content.decode("utf-8")
                    except UnicodeDecodeError:
                        return {
                            "path": path,
                            "content": None,
                            "error": "Binary file - cannot display",
                            "size": stat.st_size
                        }
            
            return {
                "path": path,
                "content": content,
                "size": stat.st_size
            }
        finally:
            sftp.close()
            transport.close()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SFTP error: {str(e)}")


# ─────────────────────────────────────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)

