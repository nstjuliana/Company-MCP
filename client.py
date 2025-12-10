import asyncio
import json

from fastmcp import Client


def _pretty(response) -> str:
    """Best-effort formatting for tool responses."""
    if not getattr(response, "content", None):
        return ""
    msg = response.content[0]
    text = getattr(msg, "text", None) or str(msg)
    try:
        return json.dumps(json.loads(text), indent=2)
    except Exception:
        return text


async def main() -> None:
    # Point to the MCP HTTP endpoint exposed by server.py (default path /mcp).
    # async with Client("http://129.158.231.129/mcp") as client:
    async with Client("http://localhost:8000/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        print("Tools:", [t.name for t in tools])

        # Call the sample tools
        add_result = await client.call_tool("add", {"a": 2, "b": 3})
        print("add(2,3) =", _pretty(add_result))

        echo_result = await client.call_tool("echo", {"message": "hello"})
        print("echo =", _pretty(echo_result))

        search_db_map_result = await client.call_tool("search_db_map", {"query": "payment 123"})
        print("search_db_map =", _pretty(search_db_map_result))

        # --- PRD2 tool smoke tests ---
        list_tables_result = await client.call_tool("list_tables", {})
        print("list_tables =", _pretty(list_tables_result))

        list_columns_result = await client.call_tool("list_columns", {"table": "dabstep_tasks"})
        print("list_columns(dabstep_tasks) =", _pretty(list_columns_result))

        search_tables_result = await client.call_tool(
            "search_tables", {"query": "payments fraud", "domain": "payments", "limit": 5}
        )
        print("search_tables(payments fraud) =", _pretty(search_tables_result))

        schema_result = await client.call_tool("get_table_schema", {"table": "dabstep_payments"})
        print("get_table_schema(dabstep_payments) =", _pretty(schema_result))

        join_result = await client.call_tool(
            "get_join_path", {"source_table": "dabstep_submissions", "target_table": "dabstep_tasks"}
        )
        print("get_join_path(submissions -> tasks) =", _pretty(join_result))

        domain_overview_result = await client.call_tool(
            "get_domain_overview", {"domain": "tasks", "database": "default"}
        )
        print("get_domain_overview(tasks) =", _pretty(domain_overview_result))

        list_domains_result = await client.call_tool("list_domains", {})
        print("list_domains =", _pretty(list_domains_result))

        common_rels_result = await client.call_tool(
            "get_common_relationships", {"domain": "tasks", "limit": 5}
        )
        print("get_common_relationships(tasks) =", _pretty(common_rels_result))


if __name__ == "__main__":
    asyncio.run(main())

