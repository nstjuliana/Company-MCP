"""
Company MCP Frontend - FastAPI Backend
Provides web UI for MCP interaction, SFTP browsing, and GPT-4o powered AI chat.
"""
import os
import json
import paramiko
import sqlite3
import re
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any, Set
from contextlib import asynccontextmanager
from collections import defaultdict
from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

# Configuration
SFTP_HOST = os.getenv("SFTP_HOST", "sftp-server")
SFTP_PORT = int(os.getenv("SFTP_PORT", "22"))
SFTP_USER = os.getenv("SFTP_USER", "datauser")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD", "changeme")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# MCP Server URL - connects to MCP server within Docker network
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://mcp-dabstep:8000")

# Database paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "index" / "index.db"
DATA_MAP_PATH = DATA_DIR / "map"
MCP_CONFIG_PATH = BASE_DIR / "mcp_servers.json"

# HTTP client
http_client: Optional[httpx.AsyncClient] = None
openai_client: Optional[AsyncOpenAI] = None

# In-memory MCP server registry
mcp_servers: Dict[str, Dict[str, Any]] = {}

# Known internal MCP server mappings (external path -> internal URL)
INTERNAL_MCP_SERVERS = {
    "/mcp/dabstep": "http://mcp-dabstep:8000",
    "/mcp/synth": "http://mcp-synth:8000",
    "/mcp/postgres": "http://mcp-postgres:8000",
}


def normalize_mcp_url(url: str) -> str:
    """
    Normalize MCP server URL to use internal Docker URLs when running locally.
    
    Only converts localhost URLs (http://localhost/mcp/dabstep) to internal
    Docker URLs (http://mcp-dabstep:8000).
    
    Production URLs (https://company-mcp.com/mcp/synth) are left unchanged.
    """
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    
    # Only convert localhost URLs to internal Docker URLs
    if parsed.hostname in ('localhost', '127.0.0.1'):
        for path, internal_url in INTERNAL_MCP_SERVERS.items():
            if path in url:
                print(f"[normalize_mcp_url] Converting localhost URL {url} -> {internal_url}")
                return internal_url
    
    # Return original URL for production/external servers
    print(f"[normalize_mcp_url] Keeping external URL as-is: {url}")
    return url


def load_mcp_servers():
    """Load MCP server configurations from file."""
    global mcp_servers
    mcp_servers = {}  # Always start with empty dict
    if MCP_CONFIG_PATH.exists():
        try:
            with open(MCP_CONFIG_PATH, "r") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    mcp_servers = loaded
        except Exception as e:
            print(f"[load_mcp_servers] Error loading config: {e}")
            mcp_servers = {}


def save_mcp_servers():
    """Save MCP server configurations to file."""
    with open(MCP_CONFIG_PATH, "w") as f:
        json.dump(mcp_servers, f, indent=2)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage HTTP client lifecycle."""
    global http_client, openai_client
    http_client = httpx.AsyncClient(timeout=60.0)
    if OPENAI_API_KEY:
        openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    load_mcp_servers()
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
    role: str  # "user", "assistant", or "system"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []


class ToolCall(BaseModel):
    tool: str
    params: Dict[str, Any] = {}


class MCPServerConfig(BaseModel):
    name: str
    url: str
    enabled: bool = True
    description: str = ""


class MCPServerUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    enabled: Optional[bool] = None
    description: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────────────
# Page Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main SPA page."""
    return templates.TemplateResponse("index.html", {"request": request})


# ─────────────────────────────────────────────────────────────────────────────
# API Routes - MCP Server Management
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/mcp/servers")
async def list_mcp_servers():
    """List all configured MCP servers."""
    # Ensure we always return a valid dict
    return {"servers": mcp_servers if isinstance(mcp_servers, dict) else {}}


@app.post("/api/mcp/servers/{server_id}")
async def add_mcp_server(server_id: str, config: MCPServerConfig):
    """Add a new MCP server configuration."""
    if server_id in mcp_servers:
        raise HTTPException(status_code=400, detail=f"Server '{server_id}' already exists")
    
    mcp_servers[server_id] = {
        "name": config.name,
        "url": config.url,
        "enabled": config.enabled,
        "description": config.description
    }
    save_mcp_servers()
    return {"status": "created", "server_id": server_id}


@app.put("/api/mcp/servers/{server_id}")
async def update_mcp_server(server_id: str, update: MCPServerUpdate):
    """Update an existing MCP server configuration."""
    if server_id not in mcp_servers:
        raise HTTPException(status_code=404, detail=f"Server '{server_id}' not found")
    
    if update.name is not None:
        mcp_servers[server_id]["name"] = update.name
    if update.url is not None:
        mcp_servers[server_id]["url"] = update.url
    if update.enabled is not None:
        mcp_servers[server_id]["enabled"] = update.enabled
    if update.description is not None:
        mcp_servers[server_id]["description"] = update.description
    
    save_mcp_servers()
    return {"status": "updated", "server": mcp_servers[server_id]}


@app.delete("/api/mcp/servers/{server_id}")
async def delete_mcp_server(server_id: str):
    """Delete an MCP server configuration."""
    if server_id not in mcp_servers:
        raise HTTPException(status_code=404, detail=f"Server '{server_id}' not found")
    
    del mcp_servers[server_id]
    save_mcp_servers()
    return {"status": "deleted"}


@app.get("/api/mcp/servers/{server_id}/health")
async def check_mcp_server_health(server_id: str):
    """Check health of a specific MCP server by attempting to initialize a session."""
    if server_id not in mcp_servers:
        raise HTTPException(status_code=404, detail=f"Server '{server_id}' not found")

    server = mcp_servers[server_id]
    # Normalize URL to use internal Docker URLs when possible
    server_url = normalize_mcp_url(server['url'])
    mcp_endpoint = get_mcp_endpoint(server_url)
    
    try:
        # Try to initialize an MCP session to verify the server is working
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "CompanyMCP-HealthCheck", "version": "1.0.0"}
            }
        }
        
        response = await http_client.post(
            mcp_endpoint,
            json=init_payload,
            headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
            timeout=10.0
        )
        
        # Check if we got a session ID back
        session_id = response.headers.get("mcp-session-id")
        if session_id and response.status_code == 200:
            return {"status": "connected", "server_id": server_id, "session_id": session_id[:8] + "..."}
        else:
            return {"status": "disconnected", "server_id": server_id, "error": f"No session (HTTP {response.status_code})"}
    except Exception as e:
        return {"status": "disconnected", "server_id": server_id, "error": str(e)}


def parse_sse_response(content: str) -> Dict[str, Any]:
    """Parse SSE event stream response to extract JSON data."""
    for line in content.split('\n'):
        if line.startswith('data: '):
            try:
                return json.loads(line[6:])
            except json.JSONDecodeError:
                continue
    return {}


def get_mcp_endpoint(server_url: str) -> str:
    """
    Get the MCP endpoint URL for a server.
    
    For local Docker URLs (http://mcp-synth:8000), append /mcp.
    For production URLs that already contain /mcp/ path, use as-is.
    """
    # If the URL already has /mcp/ in the path (production), don't append /mcp
    if "/mcp/" in server_url or server_url.endswith("/mcp"):
        return server_url
    # For local Docker URLs, append /mcp
    return f"{server_url}/mcp"


async def fetch_tools_from_server(server_id: str, server_url: str) -> List[Dict[str, Any]]:
    """Fetch tools from a single MCP server using session-based protocol."""
    try:
        # Normalize URL to use internal Docker URLs when possible
        server_url = normalize_mcp_url(server_url)
        mcp_endpoint = get_mcp_endpoint(server_url)
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        # Step 1: Initialize session
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "CompanyMCP-Frontend", "version": "1.0.0"}
            }
        }
        
        print(f"[fetch_tools_from_server] Connecting to {mcp_endpoint}")
        init_response = await http_client.post(
            mcp_endpoint,
            json=init_payload,
            headers=headers
        )
        
        # Get session ID from response headers
        session_id = init_response.headers.get("mcp-session-id")
        if not session_id:
            print(f"[fetch_tools_from_server] No session ID from {server_id}")
            return []
        
        print(f"[fetch_tools_from_server] Got session {session_id[:8]}... from {server_id}")
        
        # Step 2: List tools with session
        tools_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        headers["mcp-session-id"] = session_id
        
        tools_response = await http_client.post(
            mcp_endpoint,
            json=tools_payload,
            headers=headers
        )
        
        # Parse SSE response
        content = tools_response.text
        result = parse_sse_response(content)
        tools = result.get("result", {}).get("tools", [])
        
        print(f"[fetch_tools_from_server] Got {len(tools)} tools from {server_id}")
        return tools
        
    except Exception as e:
        import traceback
        print(f"[fetch_tools_from_server] Error from {server_id}: {e}")
        traceback.print_exc()
        return []


@app.get("/api/mcp/servers/{server_id}/tools")
async def get_mcp_server_tools(server_id: str):
    """Get available tools from a specific MCP server."""
    if server_id not in mcp_servers:
        raise HTTPException(status_code=404, detail=f"Server '{server_id}' not found")
    
    server = mcp_servers[server_id]
    tools = await fetch_tools_from_server(server_id, server['url'])
    return {"server_id": server_id, "tools": tools}


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
# API Routes - Chat (GPT-4o Powered)
# ─────────────────────────────────────────────────────────────────────────────

async def get_all_mcp_tools() -> List[Dict[str, Any]]:
    """Fetch tools from all enabled MCP servers."""
    all_tools = []

    print(f"[get_all_mcp_tools] Checking {len(mcp_servers)} servers: {list(mcp_servers.keys())}")

    for server_id, server in mcp_servers.items():
        if not server.get("enabled", True):
            print(f"[get_all_mcp_tools] Skipping disabled server: {server_id}")
            continue

        server_url = server['url']
        # Normalize URL for internal use
        normalized_url = normalize_mcp_url(server_url)
        tools = await fetch_tools_from_server(server_id, server_url)
        print(f"[get_all_mcp_tools] Got {len(tools)} tools from {server_id}")

        # Tag each tool with its server (use normalized URL for actual calls)
        for tool in tools:
            tool["_server_id"] = server_id
            tool["_server_url"] = normalized_url
            all_tools.append(tool)
    
    print(f"[get_all_mcp_tools] Total tools found: {len(all_tools)}")
    return all_tools


def convert_mcp_tools_to_openai_format(mcp_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert MCP tool definitions to OpenAI function calling format."""
    openai_tools = []
    
    for tool in mcp_tools:
        # Build the parameters schema
        input_schema = tool.get("inputSchema", {})
        
        openai_tool = {
            "type": "function",
            "function": {
                "name": f"{tool.get('_server_id', 'default')}__{tool['name']}",
                "description": tool.get("description", f"Tool: {tool['name']}"),
                "parameters": input_schema if input_schema else {"type": "object", "properties": {}}
            }
        }
        openai_tools.append(openai_tool)
    
    return openai_tools


async def call_mcp_tool_on_server(server_url: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Call a specific tool on an MCP server using session-based protocol."""
    try:
        # Normalize URL to use internal Docker URLs when possible
        server_url = normalize_mcp_url(server_url)
        mcp_endpoint = get_mcp_endpoint(server_url)
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }

        # Step 1: Initialize session
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "CompanyMCP-Frontend", "version": "1.0.0"}
            }
        }
        
        init_response = await http_client.post(
            mcp_endpoint,
            json=init_payload,
            headers=headers
        )
        
        session_id = init_response.headers.get("mcp-session-id")
        if not session_id:
            return {"error": "Failed to establish MCP session"}
        
        # Step 2: Call tool with session
        tool_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        headers["mcp-session-id"] = session_id
        
        response = await http_client.post(
            mcp_endpoint,
            json=tool_payload,
            headers=headers
        )
        
        # Parse SSE response
        content = response.text
        result = parse_sse_response(content)
        
        if "error" in result:
            return {"error": result["error"]}
        
        return result.get("result", result)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


@app.get("/api/chat/status")
async def chat_status():
    """Check if GPT-4o chat is available."""
    return {
        "openai_configured": bool(OPENAI_API_KEY),
        "mcp_servers_count": len(mcp_servers),
        "enabled_servers": sum(1 for s in mcp_servers.values() if s.get("enabled", True))
    }


def build_system_prompt(server_list: str, tool_names: List[str]) -> str:
    """Build the system prompt for the chat assistant."""
    tool_list = ", ".join(tool_names[:20])
    if len(tool_names) > 20:
        tool_list += f" (and {len(tool_names) - 20} more)"
    
    return f"""You are a helpful AI assistant with access to MCP (Model Context Protocol) servers and their tools.

IMPORTANT: You MUST use the available tools to answer questions. Do NOT just say "let me check" - actually call the tools!

Available MCP Servers: {server_list}

Available Tools ({len(tool_names)} total): {tool_list}

Tool naming convention: Tools are named as "server_id__tool_name". For example:
- "synth-mcp__search_tables" calls the search_tables tool on the synth-mcp server
- "postgres-mcp__execute_query" calls execute_query on the postgres-mcp server

=== DATABASE QUERY WORKFLOW ===
When answering questions that require database information, follow this workflow:

1. **FIRST: Use synth-mcp to understand the schema**
   - Use synth-mcp tools (search_tables, list_tables, get_table_schema, search_fts, search_vector) to discover relevant tables and columns
   - Understand table relationships, column types, and data structure before writing SQL
   - synth-mcp has pre-indexed documentation about the database schema

2. **THEN: Write SQL based on what you learned**
   - Use the schema knowledge from synth-mcp to write accurate SQL
   - Reference the correct table names, column names, and relationships
   - Tables are in the "synthetic" schema (e.g., synthetic.accounts, synthetic.transactions)

3. **FINALLY: Use postgres-mcp to execute the SQL**
   - Use postgres-mcp__execute_query to run your SQL against the live database
   - postgres-mcp provides read-only access (SELECT, WITH, EXPLAIN only)
   - Results are limited to 1000 rows by default

=== GENERAL GUIDELINES ===
1. ALWAYS use the available tools to get real data - don't make up information
2. If asked about a specific server, use tools from that server (look for the server_id prefix)
3. Provide clear, well-formatted responses with the actual data returned
4. If a tool returns an error, explain what went wrong
5. Format data results using markdown (tables, lists, code blocks)

Remember: Call the tools, don't just describe what you would do!"""


async def stream_sse_event(event_type: str, data: Any) -> str:
    """Format a Server-Sent Event."""
    json_data = json.dumps(data, default=str)
    return f"event: {event_type}\ndata: {json_data}\n\n"


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream chat responses using Server-Sent Events.
    Events: thinking, tool_start, tool_result, content_delta, content_done, error
    """
    async def generate():
        if not openai_client:
            yield await stream_sse_event("error", {
                "message": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            })
            return
        
        try:
            # Fetch all available MCP tools
            mcp_tools = await get_all_mcp_tools()
            openai_tools = convert_mcp_tools_to_openai_format(mcp_tools)
            
            # Build tool lookup for quick access
            tool_lookup = {
                f"{tool.get('_server_id', 'default')}__{tool['name']}": tool 
                for tool in mcp_tools
            }
            
            # Build list of available servers for the prompt
            enabled_servers = [(k, v) for k, v in mcp_servers.items() if v.get("enabled", True)]
            server_list = ", ".join(f"{k} ({v['name']})" for k, v in enabled_servers)
            
            # Build list of tool names for the prompt
            tool_names = [f"{t.get('_server_id', 'default')}__{t['name']}" for t in mcp_tools]
            
            # Build messages for OpenAI
            messages = [
                {
                    "role": "system",
                    "content": build_system_prompt(server_list, tool_names)
                }
            ]
            
            # Add conversation history
            for msg in request.history[-10:]:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            # Add the current user message
            messages.append({
                "role": "user",
                "content": request.message
            })
            
            tools_used = []
            max_tool_calls = 10
            tool_call_count = 0
            
            while tool_call_count < max_tool_calls:
                # Call GPT-4o (non-streaming for tool calls phase)
                completion_params = {
                    "model": "gpt-4o",
                    "messages": messages,
                }
                
                if openai_tools:
                    completion_params["tools"] = openai_tools
                    completion_params["tool_choice"] = "auto"
                
                response = await openai_client.chat.completions.create(**completion_params)
                assistant_message = response.choices[0].message
                
                # Check if the model wants to call tools
                if assistant_message.tool_calls:
                    # Send thinking event if there's content
                    if assistant_message.content:
                        yield await stream_sse_event("thinking", {
                            "content": assistant_message.content
                        })
                    
                    # Add the assistant's message with tool calls
                    messages.append({
                        "role": "assistant",
                        "content": assistant_message.content or "",
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in assistant_message.tool_calls
                        ]
                    })
                    
                    # Execute each tool call
                    for tool_call in assistant_message.tool_calls:
                        full_tool_name = tool_call.function.name
                        
                        # Parse the tool name to get server_id and actual tool name
                        if "__" in full_tool_name:
                            server_id, tool_name = full_tool_name.split("__", 1)
                        else:
                            server_id = "default"
                            tool_name = full_tool_name
                        
                        # Get tool info
                        tool_info = tool_lookup.get(full_tool_name, {})
                        server_url = tool_info.get("_server_url", mcp_servers.get(server_id, {}).get("url", MCP_SERVER_URL))
                        
                        # Parse arguments
                        try:
                            arguments = json.loads(tool_call.function.arguments)
                        except json.JSONDecodeError:
                            arguments = {}
                        
                        # Send tool_start event
                        yield await stream_sse_event("tool_start", {
                            "server": server_id,
                            "tool": tool_name,
                            "arguments": arguments
                        })
                        
                        # Execute the tool
                        tool_result = await call_mcp_tool_on_server(server_url, tool_name, arguments)
                        
                        # Send tool_result event
                        yield await stream_sse_event("tool_result", {
                            "server": server_id,
                            "tool": tool_name,
                            "arguments": arguments,
                            "result": tool_result
                        })
                        
                        tools_used.append({
                            "server": server_id,
                            "tool": tool_name,
                            "arguments": arguments
                        })
                        
                        # Add tool result to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(tool_result, default=str)
                        })
                    
                    tool_call_count += 1
                else:
                    # No more tool calls - stream the final response
                    # Re-call with streaming enabled for the final response
                    final_stream = await openai_client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages,
                        stream=True
                    )
                    
                    full_content = ""
                    async for chunk in final_stream:
                        if chunk.choices and chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            full_content += content
                            yield await stream_sse_event("content_delta", {
                                "content": content
                            })
                    
                    # Send completion event
                    yield await stream_sse_event("content_done", {
                        "full_content": full_content,
                        "tools_used": tools_used
                    })
                    return
            
            # Max tool calls reached, stream final response
            final_stream = await openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                stream=True
            )
            
            full_content = ""
            async for chunk in final_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_content += content
                    yield await stream_sse_event("content_delta", {
                        "content": content
                    })
            
            yield await stream_sse_event("content_done", {
                "full_content": full_content,
                "tools_used": tools_used
            })
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield await stream_sse_event("error", {
                "message": str(e)
            })
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Process a chat message using GPT-4o with MCP tool integration.
    The AI can use tools from all connected MCP servers.
    Note: For streaming responses, use /api/chat/stream instead.
    """
    if not openai_client:
        return {
            "response": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.",
            "tools_used": [],
            "error": True
        }
    
    try:
        # Fetch all available MCP tools
        mcp_tools = await get_all_mcp_tools()
        openai_tools = convert_mcp_tools_to_openai_format(mcp_tools)
        
        # Log tool count for debugging
        print(f"[Chat] Found {len(mcp_tools)} MCP tools from {len([s for s in mcp_servers.values() if s.get('enabled', True)])} servers")
        
        # Build tool lookup for quick access
        tool_lookup = {
            f"{tool.get('_server_id', 'default')}__{tool['name']}": tool 
            for tool in mcp_tools
        }
        
        # Build list of available servers for the prompt
        enabled_servers = [(k, v) for k, v in mcp_servers.items() if v.get("enabled", True)]
        server_list = ", ".join(f"{k} ({v['name']})" for k, v in enabled_servers)
        
        # Build list of tool names for the prompt
        tool_names = [f"{t.get('_server_id', 'default')}__{t['name']}" for t in mcp_tools]
        
        # Build messages for OpenAI
        messages = [
            {
                "role": "system",
                "content": build_system_prompt(server_list, tool_names)
            }
        ]
        
        # Add conversation history
        for msg in request.history[-10:]:  # Last 10 messages for context
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add the current user message
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        tools_used = []
        thinking_steps = []  # Track detailed steps for display
        max_tool_calls = 10  # Prevent infinite loops
        tool_call_count = 0
        
        while tool_call_count < max_tool_calls:
            # Call GPT-4o
            completion_params = {
                "model": "gpt-4o",
                "messages": messages,
            }
            
            if openai_tools:
                completion_params["tools"] = openai_tools
                completion_params["tool_choice"] = "auto"
            
            response = await openai_client.chat.completions.create(**completion_params)
            
            assistant_message = response.choices[0].message
            
            # Log for debugging
            print(f"[Chat] Response: content={bool(assistant_message.content)}, tool_calls={len(assistant_message.tool_calls) if assistant_message.tool_calls else 0}")
            
            # Check if the model wants to call tools
            if assistant_message.tool_calls:
                # Capture any thinking/reasoning the assistant provided
                if assistant_message.content:
                    thinking_steps.append({
                        "type": "thinking",
                        "content": assistant_message.content
                    })
                
                # Add the assistant's message with tool calls
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })
                
                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    full_tool_name = tool_call.function.name
                    
                    # Parse the tool name to get server_id and actual tool name
                    if "__" in full_tool_name:
                        server_id, tool_name = full_tool_name.split("__", 1)
                    else:
                        server_id = "default"
                        tool_name = full_tool_name
                    
                    # Get tool info
                    tool_info = tool_lookup.get(full_tool_name, {})
                    server_url = tool_info.get("_server_url", mcp_servers.get(server_id, {}).get("url", MCP_SERVER_URL))
                    
                    # Parse arguments
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        arguments = {}
                    
                    # Execute the tool
                    print(f"[Chat] Executing tool: {server_id}/{tool_name} with args: {arguments}")
                    tool_result = await call_mcp_tool_on_server(server_url, tool_name, arguments)
                    print(f"[Chat] Tool result: {str(tool_result)[:200]}...")
                    
                    tools_used.append({
                        "server": server_id,
                        "tool": tool_name,
                        "arguments": arguments
                    })
                    
                    # Track detailed step for display
                    thinking_steps.append({
                        "type": "tool_call",
                        "server": server_id,
                        "tool": tool_name,
                        "arguments": arguments,
                        "result": tool_result
                    })
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result, default=str)
                    })
                
                tool_call_count += 1
            else:
                # No more tool calls, return the response
                return {
                    "response": assistant_message.content or "I processed your request but have no response.",
                    "tools_used": tools_used,
                    "thinking_steps": thinking_steps,
                    "error": False
                }
        
        # Max tool calls reached, get final response
        final_response = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        
        return {
            "response": final_response.choices[0].message.content or "Request completed.",
            "tools_used": tools_used,
            "thinking_steps": thinking_steps,
            "error": False
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "response": f"I encountered an error: {str(e)}",
            "tools_used": [],
            "error": True
        }


@app.post("/api/chat/simple")
async def chat_simple(request: ChatRequest):
    """
    Simple chat endpoint that falls back to rule-based routing when OpenAI is unavailable.
    """
    message = request.message.lower()
    
    try:
        # Route based on message content
        if any(word in message for word in ["list", "show", "all"]) and "database" in message:
            result = await call_tool("list_databases", {})
            return format_chat_response("list_databases", result)
        
        elif any(word in message for word in ["list", "show", "all"]) and "table" in message:
            db = extract_database(message)
            result = await call_tool("list_tables", {"database": db} if db else {})
            return format_chat_response("list_tables", result)
        
        elif any(word in message for word in ["list", "show"]) and "domain" in message:
            result = await call_tool("list_domains", {})
            return format_chat_response("list_domains", result)
        
        elif "schema" in message or "column" in message:
            table = extract_table_name(message)
            if table:
                result = await call_tool("get_table_schema", {"table": table})
                return format_chat_response("get_table_schema", result)
            else:
                return {
                    "response": "Please specify a table name to get its schema.",
                    "tool_used": None
                }
        
        elif "join" in message and ("path" in message or "between" in message):
            tables = extract_table_names(message)
            if len(tables) >= 2:
                result = await call_tool("get_join_path", {
                    "source_table": tables[0],
                    "target_table": tables[1]
                })
                return format_chat_response("get_join_path", result)
            else:
                return {
                    "response": "Please specify two table names for join path.",
                    "tool_used": None
                }
        
        else:
            result = await call_tool("search_tables", {"query": request.message, "limit": 5})
            return format_chat_response("search_tables", result)
    
    except Exception as e:
        return {
            "response": f"Error: {str(e)}",
            "tool_used": None,
            "error": True
        }


def get_db_connection() -> Optional[sqlite3.Connection]:
    """Get a connection to the SQLite database."""
    if not DB_PATH.exists():
        return None
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    return db


def load_json(path: Path) -> Any:
    """Load JSON from a file path."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


async def call_tool(tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute MCP tool by directly querying the database."""
    try:
        if tool == "list_databases":
            return await tool_list_databases()
        elif tool == "list_tables":
            return await tool_list_tables(params.get("database", ""), params.get("domain", ""))
        elif tool == "list_domains":
            return await tool_list_domains(params.get("database", ""))
        elif tool == "get_table_schema":
            return await tool_get_table_schema(params.get("table", ""), params.get("database", ""))
        elif tool == "search_tables":
            return await tool_search_tables(params.get("query", ""), params.get("limit", 5))
        elif tool == "search_fts":
            return await tool_search_fts(params.get("query", ""), params.get("limit", 10))
        else:
            return {"error": f"Unknown tool: {tool}"}
    except Exception as e:
        return {"error": str(e)}


async def tool_list_databases() -> Dict[str, Any]:
    """List all databases in the index."""
    db = get_db_connection()
    if not db:
        return {"databases": [], "error": "Database not found"}
    
    try:
        cursor = db.execute("""
            SELECT database_name, COUNT(DISTINCT table_name) as table_count,
                   GROUP_CONCAT(DISTINCT domain) as domains,
                   GROUP_CONCAT(DISTINCT schema_name) as schemas
            FROM documents 
            WHERE doc_type = 'table'
            GROUP BY database_name
        """)
        
        databases = []
        for row in cursor.fetchall():
            databases.append({
                "name": row["database_name"],
                "table_count": row["table_count"],
                "domains": [d for d in (row["domains"] or "").split(",") if d],
                "schemas": [s for s in (row["schemas"] or "").split(",") if s],
            })
        
        db.close()
        return {"databases": databases}
    except Exception as e:
        db.close()
        return {"databases": [], "error": str(e)}


async def tool_list_tables(database: str = "", domain: str = "") -> List[Dict[str, Any]]:
    """List tables, optionally filtered."""
    db = get_db_connection()
    if not db:
        return []
    
    try:
        filters = ["doc_type = 'table'", "file_path LIKE '%.json'"]
        params = []
        
        if database:
            filters.append("database_name = ?")
            params.append(database)
        if domain:
            filters.append("domain = ?")
            params.append(domain)
        
        cursor = db.execute(f"""
            SELECT DISTINCT table_name, database_name, schema_name, domain, summary
            FROM documents
            WHERE {' AND '.join(filters)}
        """, params)
        
        tables = []
        for row in cursor.fetchall():
            name = row["table_name"]
            if name.endswith(".json"):
                name = name[:-5]
            tables.append({
                "name": name,
                "database": row["database_name"],
                "schema": row["schema_name"],
                "domain": row["domain"],
                "summary": row["summary"] or "",
            })
        
        db.close()
        return tables
    except Exception as e:
        db.close()
        return []


async def tool_list_domains(database: str = "") -> Dict[str, Any]:
    """List all domains."""
    db = get_db_connection()
    if not db:
        return {"domains": []}
    
    try:
        if database:
            cursor = db.execute("""
                SELECT domain, COUNT(DISTINCT table_name) as table_count
                FROM documents 
                WHERE doc_type = 'table' AND database_name = ?
                GROUP BY domain
            """, [database])
        else:
            cursor = db.execute("""
                SELECT domain, COUNT(DISTINCT table_name) as table_count
                FROM documents 
                WHERE doc_type = 'table'
                GROUP BY domain
            """)
        
        domains = []
        for row in cursor.fetchall():
            domains.append({
                "name": row["domain"] or "default",
                "table_count": row["table_count"],
            })
        
        db.close()
        return {"domains": domains}
    except Exception as e:
        db.close()
        return {"domains": [], "error": str(e)}


async def tool_get_table_schema(table: str, database: str = "") -> Dict[str, Any]:
    """Get full schema for a table."""
    db = get_db_connection()
    if not db:
        return {"error": "Database not found"}
    
    try:
        # Find the table
        if database:
            cursor = db.execute("""
                SELECT file_path, database_name, schema_name, domain, summary
                FROM documents 
                WHERE doc_type = 'table' 
                AND (table_name = ? OR table_name LIKE ? OR LOWER(table_name) = LOWER(?))
                AND database_name = ?
                AND file_path LIKE '%.json'
                LIMIT 1
            """, (table, f"%{table}%", table, database))
        else:
            cursor = db.execute("""
                SELECT file_path, database_name, schema_name, domain, summary
                FROM documents 
                WHERE doc_type = 'table' 
                AND (table_name = ? OR table_name LIKE ? OR LOWER(table_name) = LOWER(?))
                AND file_path LIKE '%.json'
                LIMIT 1
            """, (table, f"%{table}%", table))
        
        row = cursor.fetchone()
        db.close()
        
        if not row:
            return {"error": f"Table '{table}' not found"}
        
        # Load the JSON file
        file_path = row["file_path"]
        if file_path.startswith("databases/"):
            file_path = file_path[len("databases/"):]
        
        json_path = DATA_MAP_PATH / file_path
        if not json_path.exists():
            return {"error": f"Schema file not found"}
        
        schema = load_json(json_path)
        
        return {
            "name": schema.get("table", table),
            "database": schema.get("database", row["database_name"]),
            "schema": schema.get("schema", row["schema_name"]),
            "description": schema.get("description", row["summary"]),
            "columns": schema.get("columns", []),
            "primary_key": schema.get("primary_key", []),
            "foreign_keys": schema.get("foreign_keys", []),
        }
    except Exception as e:
        return {"error": str(e)}


async def tool_search_tables(query: str, limit: int = 5) -> Dict[str, Any]:
    """Search tables by query."""
    db = get_db_connection()
    if not db:
        return {"tables": [], "total_matches": 0}
    
    try:
        # Simple keyword search
        keywords = re.findall(r"[a-z0-9]+", query.lower())
        
        cursor = db.execute("""
            SELECT DISTINCT table_name, database_name, domain, summary
            FROM documents 
            WHERE doc_type = 'table' AND file_path LIKE '%.json'
        """)
        
        results = []
        for row in cursor.fetchall():
            name = row["table_name"]
            if name.endswith(".json"):
                name = name[:-5]
            
            text = f"{name} {row['summary'] or ''}".lower()
            score = sum(1 for kw in keywords if kw in text)
            
            if score > 0:
                results.append({
                    "name": name,
                    "database": row["database_name"],
                    "domain": row["domain"],
                    "summary": row["summary"] or "",
                    "relevance_score": score,
                })
        
        db.close()
        
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return {"tables": results[:limit], "total_matches": len(results)}
    except Exception as e:
        db.close()
        return {"tables": [], "total_matches": 0, "error": str(e)}


async def tool_search_fts(query: str, limit: int = 10) -> Dict[str, Any]:
    """Full-text search using FTS5."""
    db = get_db_connection()
    if not db:
        return {"results": [], "total_matches": 0}
    
    try:
        cursor = db.execute("""
            SELECT d.table_name, d.database_name, d.domain, d.summary,
                   bm25(documents_fts) as rank
            FROM documents_fts fts
            JOIN documents d ON d.id = fts.rowid
            WHERE documents_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, [query, limit])
        
        results = []
        for row in cursor.fetchall():
            name = row["table_name"]
            if name and name.endswith(".json"):
                name = name[:-5]
            results.append({
                "name": name,
                "database": row["database_name"],
                "domain": row["domain"],
                "summary": row["summary"] or "",
            })
        
        db.close()
        return {"results": results, "total_matches": len(results)}
    except Exception as e:
        db.close()
        # Fall back to simple search
        return await tool_search_tables(query, limit)


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
# API Routes - Wiki (Database Documentation)
# ─────────────────────────────────────────────────────────────────────────────

# Wiki markdown files base path - reading from local folder for now
WIKI_BASE_PATH = BASE_DIR.parent / "sftp-markdown-files"


def get_wiki_structure() -> Dict[str, Any]:
    """Build hierarchical structure from the markdown files directory."""
    structure = {"databases": []}
    
    if not WIKI_BASE_PATH.exists():
        return structure
    
    # Iterate through databases
    for db_path in sorted(WIKI_BASE_PATH.iterdir()):
        if not db_path.is_dir():
            continue
        
        db_info = {
            "name": db_path.name,
            "path": str(db_path.relative_to(WIKI_BASE_PATH)),
            "domains": []
        }
        
        # Look for domains directory
        domains_path = db_path / "domains"
        if domains_path.exists() and domains_path.is_dir():
            for domain_path in sorted(domains_path.iterdir()):
                if not domain_path.is_dir():
                    continue
                
                domain_info = {
                    "name": domain_path.name,
                    "path": str(domain_path.relative_to(WIKI_BASE_PATH)),
                    "tables": []
                }
                
                # Look for tables directory
                tables_path = domain_path / "tables"
                if tables_path.exists() and tables_path.is_dir():
                    for table_file in sorted(tables_path.iterdir()):
                        if table_file.is_file() and table_file.suffix.lower() in ['.md', '.markdown']:
                            table_name = table_file.stem
                            domain_info["tables"].append({
                                "name": table_name,
                                "path": str(table_file.relative_to(WIKI_BASE_PATH)),
                                "file": table_file.name
                            })
                
                db_info["domains"].append(domain_info)
        
        structure["databases"].append(db_info)
    
    return structure


def search_wiki_tables(query: str) -> List[Dict[str, Any]]:
    """Search tables in wiki by name or content."""
    results = []
    query_lower = query.lower()
    
    if not WIKI_BASE_PATH.exists():
        return results
    
    # Search through all markdown files
    for md_file in WIKI_BASE_PATH.rglob("*.md"):
        table_name = md_file.stem
        relative_path = str(md_file.relative_to(WIKI_BASE_PATH))
        
        # Parse path to get database and domain
        parts = relative_path.split("/")
        database = parts[0] if len(parts) > 0 else ""
        domain = parts[2] if len(parts) > 2 else ""  # skip "domains" folder
        
        # Check if query matches table name
        name_match = query_lower in table_name.lower()
        
        # Check content for matches
        content_match = False
        snippet = ""
        try:
            content = md_file.read_text(encoding='utf-8')
            if query_lower in content.lower():
                content_match = True
                # Extract snippet around match
                idx = content.lower().find(query_lower)
                start = max(0, idx - 50)
                end = min(len(content), idx + len(query) + 100)
                snippet = "..." + content[start:end].replace("\n", " ").strip() + "..."
        except Exception:
            pass
        
        if name_match or content_match:
            results.append({
                "name": table_name,
                "path": relative_path,
                "database": database,
                "domain": domain,
                "name_match": name_match,
                "snippet": snippet if content_match else ""
            })
    
    # Sort by relevance (name matches first)
    results.sort(key=lambda x: (not x["name_match"], x["name"].lower()))
    
    return results[:50]  # Limit to 50 results


@app.get("/api/wiki/structure")
async def get_wiki_structure_endpoint():
    """Get the hierarchical structure of wiki databases, domains, and tables."""
    try:
        structure = get_wiki_structure()
        return structure
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/wiki/table")
async def get_wiki_table(path: str):
    """Get the markdown content for a specific table."""
    try:
        # Validate path doesn't escape wiki directory
        file_path = WIKI_BASE_PATH / path
        if not file_path.resolve().is_relative_to(WIKI_BASE_PATH.resolve()):
            raise HTTPException(status_code=403, detail="Invalid path")
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Table documentation not found")
        
        content = file_path.read_text(encoding='utf-8')
        
        # Parse path to get metadata
        parts = path.split("/")
        database = parts[0] if len(parts) > 0 else ""
        domain = parts[2] if len(parts) > 2 else ""
        table_name = file_path.stem
        
        return {
            "path": path,
            "name": table_name,
            "database": database,
            "domain": domain,
            "content": content
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/wiki/search")
async def search_wiki(q: str):
    """Search for tables in the wiki."""
    try:
        if not q or len(q) < 2:
            return {"results": [], "query": q}
        
        results = search_wiki_tables(q)
        return {"results": results, "query": q}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
                # Skip markdown files (only filter files, not directories)
                if not is_dir and item.filename.endswith('.md'):
                    continue
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


def find_markdown_files_recursive(sftp, path: str, base_path: str = "/data"):
    """Recursively find all markdown files in SFTP directory."""
    markdown_files = []
    
    try:
        # Ensure path starts with /data
        if not path.startswith("/data"):
            path = f"/data{path}" if path.startswith("/") else f"/data/{path}"
        
        for item in sftp.listdir_attr(path):
            item_path = f"{path}/{item.filename}".replace("//", "/")
            is_dir = item.st_mode is not None and (item.st_mode & 0o40000)
            
            if is_dir:
                # Recursively search subdirectories
                try:
                    markdown_files.extend(find_markdown_files_recursive(sftp, item_path, base_path))
                except Exception:
                    # Skip directories we can't access
                    pass
            else:
                # Check if it's a markdown file
                if item.filename.lower().endswith(('.md', '.markdown')):
                    markdown_files.append({
                        "name": item.filename,
                        "path": item_path,
                        "size": item.st_size,
                        "modified": item.st_mtime,
                        "relative_path": item_path.replace(base_path, "").lstrip("/")
                    })
    except Exception:
        # Skip paths we can't access
        pass
    
    return markdown_files


@app.get("/api/files/markdown")
async def get_all_markdown_files(root_path: str = "/data"):
    """Get all markdown files recursively from SFTP directory."""
    try:
        sftp, transport = get_sftp_client()
        try:
            # Ensure path starts with /data
            if not root_path.startswith("/data"):
                root_path = f"/data{root_path}" if root_path.startswith("/") else f"/data/{root_path}"
            
            markdown_files = find_markdown_files_recursive(sftp, root_path, root_path)
            
            # Sort by path
            markdown_files.sort(key=lambda x: x["path"].lower())
            
            return {
                "count": len(markdown_files),
                "files": markdown_files,
                "root_path": root_path
            }
        finally:
            sftp.close()
            transport.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SFTP error: {str(e)}")


# ─────────────────────────────────────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)

