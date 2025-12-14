#!/usr/bin/env python3
"""
Test script to verify the merchant count query works with the actual database.
"""

import sys
import os
sys.path.append('.')

from chatbot.ai_agent import AIAgent

def test_merchant_query():
    """Test the merchant count query."""
    print("Testing merchant count query...")

    # Mock MCP tool caller (since MCP server should be running)
    def mock_mcp_tool_caller(tool_name, **kwargs):
        print(f"MCP Tool Call: {tool_name} with args: {kwargs}")
        # For this test, we'll simulate MCP responses
        if tool_name == "search_tables":
            return {
                "tables": [
                    {
                        "name": "merchants",
                        "database": "postgres_production",
                        "schema": "public",
                        "description": "Merchant entities"
                    }
                ]
            }
        elif tool_name == "list_columns":
            return {
                "columns": [
                    {"name": "merchant_id", "type": "character varying"},
                    {"name": "created_at", "type": "timestamp"}
                ]
            }
        return {}

    try:
        agent = AIAgent()
        result = agent._handle_data_question(
            question="how many merchants",
            database="postgres_production",
            mcp_tool_caller=mock_mcp_tool_caller
        )

        print(f"Query result: {result}")

        if result.get("success"):
            print("✅ Query succeeded!")
            print(f"SQL: {result.get('sql')}")
            print(f"Row count: {result.get('row_count')}")
            if result.get("data"):
                print(f"Data: {result['data']}")
        else:
            print("❌ Query failed!")
            print(f"Error: {result.get('error')}")

    except Exception as e:
        print(f"❌ Exception during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_merchant_query()