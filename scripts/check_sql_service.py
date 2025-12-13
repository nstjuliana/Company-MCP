#!/usr/bin/env python3
"""
Diagnostic script to check SQL service availability and configuration.
"""

import os
import sys

print("=== SQL Service Diagnostic ===\n")

# Check imports
print("1. Checking dependencies...")
try:
    import psycopg2
    print("   ✓ psycopg2 (PostgreSQL) - Available")
except ImportError:
    print("   ✗ psycopg2 (PostgreSQL) - NOT AVAILABLE")

try:
    import snowflake.connector
    print("   ✓ snowflake-connector-python - Available")
except ImportError:
    print("   ✗ snowflake-connector-python - NOT AVAILABLE")

try:
    from openai import OpenAI
    print("   ✓ openai - Available")
except ImportError:
    print("   ✗ openai - NOT AVAILABLE")

# Check SQL service import
print("\n2. Checking SQL service import...")
try:
    from sql_service import generate_and_execute_sql, _sql_generator, _sql_executor
    print("   ✓ sql_service - Import successful")
    SQL_SERVICE_IMPORTED = True
except ImportError as e:
    print(f"   ✗ sql_service - Import failed: {e}")
    SQL_SERVICE_IMPORTED = False
except Exception as e:
    print(f"   ✗ sql_service - Error: {e}")
    SQL_SERVICE_IMPORTED = False

# Check environment variables
print("\n3. Checking environment variables...")

# Load .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("   ✓ .env file loaded")
except ImportError:
    print("   ⚠ python-dotenv not installed (optional)")
except Exception as e:
    print(f"   ⚠ Could not load .env: {e}")

# OpenRouter
openrouter_key = os.getenv("OPENROUTER_API_KEY")
if openrouter_key:
    print(f"   ✓ OPENROUTER_API_KEY - Set (length: {len(openrouter_key)})")
else:
    print("   ✗ OPENROUTER_API_KEY - NOT SET (required for SQL generation)")

# PostgreSQL
postgres_url = os.getenv("TEST_DATABASE_URL") or os.getenv("POSTGRES_CONNECTION_STRING")
if postgres_url:
    print("   ✓ PostgreSQL connection string - Set")
else:
    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    if postgres_host and postgres_user and postgres_password:
        print("   ✓ PostgreSQL credentials - Set (individual vars)")
    else:
        print("   ✗ PostgreSQL credentials - NOT SET")

# Snowflake
sf_account = os.getenv("SNOWFLAKE_ACCOUNT") or os.getenv("SNOWFLAKE_TEST_ACCOUNT")
sf_user = os.getenv("SNOWFLAKE_USERNAME") or os.getenv("SNOWFLAKE_USER") or os.getenv("SNOWFLAKE_TEST_USERNAME")
sf_password = os.getenv("SNOWFLAKE_PASSWORD") or os.getenv("SNOWFLAKE_TEST_PASSWORD")
if sf_account and sf_user and sf_password:
    print("   ✓ Snowflake credentials - Set")
else:
    print("   ✗ Snowflake credentials - NOT SET")

# Check SQL service initialization
print("\n4. Checking SQL service initialization...")
if SQL_SERVICE_IMPORTED:
    try:
        # Check if SQL generator has API key
        if _sql_generator.client:
            print("   ✓ SQL Generator - Initialized with API key")
        else:
            print("   ✗ SQL Generator - No API key configured")
        
        # Check database manager
        print("   ✓ Database Connection Manager - Initialized")
        print("   ✓ SQL Executor - Initialized")
    except Exception as e:
        print(f"   ✗ Error checking initialization: {e}")

# Summary
print("\n=== Summary ===")
if SQL_SERVICE_IMPORTED and openrouter_key:
    print("✓ SQL service should be available")
    print("  - You can generate SQL queries")
    if postgres_url or (sf_account and sf_user and sf_password):
        print("  - You can execute SQL queries")
    else:
        print("  ⚠ Database credentials not set - SQL execution will fail")
else:
    print("✗ SQL service is NOT available")
    if not SQL_SERVICE_IMPORTED:
        print("  - Fix: Install missing dependencies or fix import errors")
    if not openrouter_key:
        print("  - Fix: Set OPENROUTER_API_KEY environment variable")

print("\nTo fix issues:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Set OPENROUTER_API_KEY in your environment or .env file")
print("3. Set database credentials (PostgreSQL or Snowflake) if you want to execute queries")

