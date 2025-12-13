#!/usr/bin/env python3
"""
Test script for the Database Context MCP Chatbot UI.

This script tests that the chatbot can process natural language queries
and route them to the appropriate MCP tools.
"""

import sys
import os
# Add parent directory to path to access server.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from chatbot.web_app import process_natural_language_query

def test_chatbot_queries():
    """Test various natural language queries."""

    test_queries = [
        "What databases are available?",
        "Show me all tables in the payments domain",
        "Find tables related to user authentication",
        "Get schema for the payments table",
        "List all domains",
        "What tables are in postgres_production?",
    ]

    print("🧪 Testing Database Context MCP Chatbot Queries\n")
    print("=" * 60)

    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 40)

        try:
            result = process_natural_language_query(query)
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                response = result.get('response', 'No response')
                print(f"✅ Response: {response[:200]}{'...' if len(response) > 200 else ''}")
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

        print()

if __name__ == "__main__":
    test_chatbot_queries()
