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

        # --- FTS5 and Vector Search tests ---
        print("\n" + "="*60)
        print("FTS5 FULL-TEXT SEARCH TESTS")
        print("="*60)

        # Test FTS5 search for "payment"
        fts_result1 = await client.call_tool(
            "search_fts", {"query": "payment", "limit": 3}
        )
        print("\nsearch_fts('payment') =", _pretty(fts_result1))

        # Test FTS5 search for "fraud"
        fts_result2 = await client.call_tool(
            "search_fts", {"query": "fraud", "doc_type": "table", "limit": 3}
        )
        print("\nsearch_fts('fraud', doc_type='table') =", _pretty(fts_result2))

        # Test FTS5 search for "submission task"
        fts_result3 = await client.call_tool(
            "search_fts", {"query": "submission task", "limit": 5}
        )
        print("\nsearch_fts('submission task') =", _pretty(fts_result3))

        print("\n" + "="*60)
        print("VECTOR SIMILARITY SEARCH TESTS")
        print("="*60)

        # Test vector search - semantic query about money
        vec_result1 = await client.call_tool(
            "search_vector", {"query": "tables related to financial transactions", "limit": 3}
        )
        print("\nsearch_vector('tables related to financial transactions') =", _pretty(vec_result1))

        # Test vector search - semantic query about fraud
        vec_result2 = await client.call_tool(
            "search_vector", {"query": "how to detect suspicious activity", "limit": 3}
        )
        print("\nsearch_vector('how to detect suspicious activity') =", _pretty(vec_result2))

        # Test vector search - semantic query about task tracking
        vec_result3 = await client.call_tool(
            "search_vector", {"query": "tracking user submissions and scores", "limit": 3}
        )
        print("\nsearch_vector('tracking user submissions and scores') =", _pretty(vec_result3))

        # Test vector search with domain filter
        vec_result4 = await client.call_tool(
            "search_vector", {"query": "credit card details", "domain": "payments", "limit": 3}
        )
        print("\nsearch_vector('credit card details', domain='payments') =", _pretty(vec_result4))


if __name__ == "__main__":
    asyncio.run(main())

