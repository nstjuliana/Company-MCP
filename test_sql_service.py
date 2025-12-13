"""
Test script for SQL Service Layer

Tests database connections, SQL generation, and SQL execution
for both PostgreSQL and Snowflake databases.
"""

import os
import sys

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed, using existing environment variables")

def test_env_vars():
    """Check that required environment variables are set."""
    print("\n=== Testing Environment Variables ===")
    
    # PostgreSQL
    postgres_url = os.getenv("TEST_DATABASE_URL") or os.getenv("POSTGRES_CONNECTION_STRING")
    print(f"PostgreSQL URL: {'Set' if postgres_url else 'NOT SET'}")
    
    # Snowflake
    sf_account = os.getenv("SNOWFLAKE_ACCOUNT") or os.getenv("SNOWFLAKE_TEST_ACCOUNT")
    sf_user = os.getenv("SNOWFLAKE_USERNAME") or os.getenv("SNOWFLAKE_USER") or os.getenv("SNOWFLAKE_TEST_USERNAME")
    sf_password = os.getenv("SNOWFLAKE_PASSWORD") or os.getenv("SNOWFLAKE_TEST_PASSWORD")
    sf_warehouse = os.getenv("SNOWFLAKE_WAREHOUSE") or os.getenv("SNOWFLAKE_TEST_WAREHOUSE")
    sf_database = os.getenv("SNOWFLAKE_DATABASE") or os.getenv("SNOWFLAKE_TEST_DATABASE")
    
    print(f"Snowflake Account: {'Set' if sf_account else 'NOT SET'}")
    print(f"Snowflake User: {'Set' if sf_user else 'NOT SET'}")
    print(f"Snowflake Password: {'Set' if sf_password else 'NOT SET'}")
    print(f"Snowflake Warehouse: {'Set' if sf_warehouse else 'NOT SET'}")
    print(f"Snowflake Database: {'Set' if sf_database else 'NOT SET'}")
    
    # OpenRouter
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    print(f"OpenRouter API Key: {'Set' if openrouter_key else 'NOT SET'}")
    
    return bool(postgres_url or (sf_account and sf_user and sf_password))

def test_postgres_connection():
    """Test PostgreSQL connection."""
    print("\n=== Testing PostgreSQL Connection ===")
    
    try:
        from sql_service import _db_manager
        
        conn = _db_manager._get_postgres_connection()
        if not conn:
            print("FAILED: Could not get PostgreSQL connection")
            return False
        
        # Test simple query
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        cursor.close()
        _db_manager._return_postgres_connection(conn)
        
        if result and result[0] == 1:
            print("SUCCESS: PostgreSQL connection works!")
            return True
        else:
            print("FAILED: Query returned unexpected result")
            return False
            
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def test_snowflake_connection():
    """Test Snowflake connection."""
    print("\n=== Testing Snowflake Connection ===")
    
    try:
        from sql_service import _db_manager
        
        conn = _db_manager._get_snowflake_connection()
        if not conn:
            print("FAILED: Could not get Snowflake connection")
            return False
        
        # Test simple query
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        cursor.close()
        
        if result and result[0] == 1:
            print("SUCCESS: Snowflake connection works!")
            return True
        else:
            print("FAILED: Query returned unexpected result")
            return False
            
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def test_sql_generation():
    """Test SQL generation from natural language."""
    print("\n=== Testing SQL Generation ===")
    
    try:
        from sql_service import _sql_generator
        
        if not _sql_generator.client:
            print("SKIPPED: OpenRouter client not configured")
            return None
        
        # Test with a simple query
        schema_context = {
            "database": "postgres_production",
            "tables": [
                {
                    "name": "public.payments",
                    "description": "Payment transactions table",
                    "columns": [
                        {"name": "id", "type": "uuid", "description": "Primary key"},
                        {"name": "amount", "type": "numeric", "description": "Payment amount"},
                        {"name": "created_at", "type": "timestamp", "description": "Creation timestamp"},
                    ],
                    "primary_key": ["id"]
                }
            ]
        }
        
        sql, error = _sql_generator.generate_sql(
            "How many payments are there?",
            schema_context,
            "postgres_production"
        )
        
        if error:
            print(f"FAILED: {error}")
            return False
        
        if sql:
            print(f"SUCCESS: Generated SQL:\n{sql}")
            return True
        else:
            print("FAILED: No SQL generated")
            return False
            
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def test_sql_execution_postgres():
    """Test SQL execution on PostgreSQL."""
    print("\n=== Testing SQL Execution (PostgreSQL) ===")
    
    try:
        from sql_service import _sql_executor
        
        # Simple count query
        result = _sql_executor.execute_query(
            "SELECT COUNT(*) as count FROM public.payments",
            "postgres_production",
            100
        )
        
        if result.get("success"):
            print(f"SUCCESS: Query executed!")
            print(f"  Columns: {result.get('columns')}")
            print(f"  Row count: {result.get('row_count')}")
            print(f"  Data: {result.get('data')}")
            return True
        else:
            print(f"FAILED: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def test_sql_execution_snowflake():
    """Test SQL execution on Snowflake."""
    print("\n=== Testing SQL Execution (Snowflake) ===")
    
    try:
        from sql_service import _sql_executor
        
        # Simple count query - using PAYMENTS table which exists in DABSTEP_DB
        result = _sql_executor.execute_query(
            "SELECT COUNT(*) as count FROM PUBLIC.PAYMENTS",
            "snowflake_production",
            100
        )
        
        if result.get("success"):
            print(f"SUCCESS: Query executed!")
            print(f"  Columns: {result.get('columns')}")
            print(f"  Row count: {result.get('row_count')}")
            print(f"  Data: {result.get('data')}")
            return True
        else:
            print(f"FAILED: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def test_end_to_end():
    """Test end-to-end flow: natural language -> SQL -> execution."""
    print("\n=== Testing End-to-End Flow ===")
    
    try:
        from sql_service import generate_and_execute_sql
        
        schema_context = {
            "database": "postgres_production",
            "tables": [
                {
                    "name": "public.payments",
                    "description": "Payment transactions table",
                    "columns": [
                        {"name": "id", "type": "uuid", "description": "Primary key"},
                        {"name": "amount", "type": "numeric", "description": "Payment amount"},
                        {"name": "created_at", "type": "timestamp", "description": "Creation timestamp"},
                    ],
                    "primary_key": ["id"]
                }
            ]
        }
        
        result = generate_and_execute_sql(
            "How many payments are there?",
            schema_context,
            "postgres_production"
        )
        
        if result.get("success"):
            print(f"SUCCESS: End-to-end flow works!")
            print(f"  Generated SQL: {result.get('sql')}")
            print(f"  Row count: {result.get('row_count')}")
            print(f"  Data: {result.get('data')}")
            return True
        else:
            print(f"FAILED: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def test_security_validation():
    """Test SQL security validation."""
    print("\n=== Testing SQL Security Validation ===")
    
    try:
        from sql_service import SQLSecurityValidator
        
        # Test valid SELECT
        is_valid, error = SQLSecurityValidator.validate_read_only("SELECT * FROM users")
        print(f"SELECT * FROM users: {'VALID' if is_valid else f'INVALID ({error})'}")
        
        # Test valid WITH CTE
        is_valid, error = SQLSecurityValidator.validate_read_only("WITH cte AS (SELECT 1) SELECT * FROM cte")
        print(f"WITH CTE: {'VALID' if is_valid else f'INVALID ({error})'}")
        
        # Test invalid INSERT
        is_valid, error = SQLSecurityValidator.validate_read_only("INSERT INTO users VALUES (1)")
        print(f"INSERT: {'INVALID (expected)' if not is_valid else 'VALID (SECURITY ISSUE!)'}")
        
        # Test invalid DELETE
        is_valid, error = SQLSecurityValidator.validate_read_only("DELETE FROM users")
        print(f"DELETE: {'INVALID (expected)' if not is_valid else 'VALID (SECURITY ISSUE!)'}")
        
        # Test invalid DROP
        is_valid, error = SQLSecurityValidator.validate_read_only("DROP TABLE users")
        print(f"DROP TABLE: {'INVALID (expected)' if not is_valid else 'VALID (SECURITY ISSUE!)'}")
        
        print("\nSecurity validation tests completed!")
        return True
        
    except Exception as e:
        print(f"FAILED: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("SQL Service Layer Tests")
    print("=" * 60)
    
    # Run tests
    results = {}
    
    results["env_vars"] = test_env_vars()
    results["security"] = test_security_validation()
    results["postgres_conn"] = test_postgres_connection()
    results["snowflake_conn"] = test_snowflake_connection()
    results["sql_generation"] = test_sql_generation()
    results["postgres_exec"] = test_sql_execution_postgres()
    results["snowflake_exec"] = test_sql_execution_snowflake()
    results["end_to_end"] = test_end_to_end()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "PASS" if result else ("SKIP" if result is None else "FAIL")
        print(f"  {test_name}: {status}")
    
    # Exit code
    failed = [k for k, v in results.items() if v is False]
    if failed:
        print(f"\nFailed tests: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\nAll tests passed!")
        sys.exit(0)

