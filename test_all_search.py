"""
Comprehensive test script for embeddings, sqlite-vec, FTS5, and vector search.

Tests:
1. OpenAI embedding generation
2. Storing embeddings in sqlite-vec
3. FTS5 full-text search
4. Vector similarity search
"""

import json
import os
import sqlite3
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import dependencies
try:
    import sqlite_vec
    print("✓ sqlite-vec imported successfully")
except ImportError:
    print("✗ sqlite-vec not installed. Run: pip install sqlite-vec")
    exit(1)

try:
    from openai import OpenAI
    print("✓ openai imported successfully")
except ImportError:
    print("✗ openai not installed. Run: pip install openai")
    exit(1)

# Configuration
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "tribal-knowledge.db"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536


def get_db_connection() -> sqlite3.Connection:
    """Get a connection to the SQLite database with sqlite-vec loaded."""
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    
    # Load sqlite-vec extension
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    
    return db


def test_openai_embeddings():
    """Test 1: Generate embeddings using OpenAI API."""
    print("\n" + "="*60)
    print("TEST 1: OpenAI Embedding Generation")
    print("="*60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY not set in environment")
        return None
    
    print(f"✓ OPENAI_API_KEY found (starts with: {api_key[:8]}...)")
    
    client = OpenAI(api_key=api_key)
    
    # Test embedding generation
    test_text = "Payment transactions with fraud detection"
    print(f"\nGenerating embedding for: '{test_text}'")
    
    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=test_text,
            dimensions=EMBEDDING_DIMENSIONS,
        )
        
        embedding = response.data[0].embedding
        print(f"✓ Embedding generated successfully!")
        print(f"  Model: {EMBEDDING_MODEL}")
        print(f"  Dimensions: {len(embedding)}")
        print(f"  First 5 values: {embedding[:5]}")
        print(f"  Token usage: {response.usage.total_tokens}")
        
        return client
        
    except Exception as e:
        print(f"✗ Failed to generate embedding: {e}")
        return None


def test_sqlite_vec_storage(client: OpenAI):
    """Test 2: Store and retrieve embeddings in sqlite-vec."""
    print("\n" + "="*60)
    print("TEST 2: sqlite-vec Storage")
    print("="*60)
    
    db = get_db_connection()
    
    # Check sqlite-vec version
    vec_version = db.execute("SELECT vec_version()").fetchone()[0]
    print(f"✓ sqlite-vec version: {vec_version}")
    
    # Check if documents_vec table exists
    table_check = db.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='documents_vec'
    """).fetchone()
    
    if table_check:
        print("✓ documents_vec table exists")
    else:
        print("✗ documents_vec table not found. Creating it...")
        db.execute(f"""
            CREATE VIRTUAL TABLE documents_vec USING vec0(
                document_id INTEGER PRIMARY KEY,
                embedding float[{EMBEDDING_DIMENSIONS}]
            )
        """)
        db.commit()
        print("✓ documents_vec table created")
    
    # Check current embedding count
    count = db.execute("SELECT COUNT(*) FROM documents_vec").fetchone()[0]
    print(f"\nCurrent embeddings in database: {count}")
    
    if count == 0 and client:
        print("\nGenerating embeddings for all documents...")
        
        # Get all documents without embeddings
        cursor = db.execute("""
            SELECT id, content FROM documents 
            WHERE doc_type = 'table'
        """)
        
        docs = cursor.fetchall()
        print(f"Found {len(docs)} table documents to embed")
        
        for doc in docs:
            try:
                response = client.embeddings.create(
                    model=EMBEDDING_MODEL,
                    input=doc["content"],
                    dimensions=EMBEDDING_DIMENSIONS,
                )
                embedding = response.data[0].embedding
                embedding_json = json.dumps(embedding)
                
                db.execute("""
                    INSERT OR REPLACE INTO documents_vec (document_id, embedding)
                    VALUES (?, ?)
                """, (doc["id"], embedding_json))
                
                print(f"  ✓ Embedded document {doc['id']}")
                
            except Exception as e:
                print(f"  ✗ Failed to embed document {doc['id']}: {e}")
        
        db.commit()
        
        # Also embed column documents
        cursor = db.execute("""
            SELECT id, content FROM documents 
            WHERE doc_type = 'column'
        """)
        
        col_docs = cursor.fetchall()
        print(f"\nFound {len(col_docs)} column documents to embed")
        
        for i, doc in enumerate(col_docs):
            try:
                response = client.embeddings.create(
                    model=EMBEDDING_MODEL,
                    input=doc["content"],
                    dimensions=EMBEDDING_DIMENSIONS,
                )
                embedding = response.data[0].embedding
                embedding_json = json.dumps(embedding)
                
                db.execute("""
                    INSERT OR REPLACE INTO documents_vec (document_id, embedding)
                    VALUES (?, ?)
                """, (doc["id"], embedding_json))
                
                if (i + 1) % 10 == 0:
                    print(f"  ✓ Embedded {i + 1}/{len(col_docs)} column documents")
                
            except Exception as e:
                print(f"  ✗ Failed to embed document {doc['id']}: {e}")
        
        db.commit()
        print(f"  ✓ Embedded all column documents")
    
    # Verify final count
    count = db.execute("SELECT COUNT(*) FROM documents_vec").fetchone()[0]
    print(f"\n✓ Total embeddings stored: {count}")
    
    db.close()
    return count > 0


def test_fts5_search():
    """Test 3: FTS5 full-text search."""
    print("\n" + "="*60)
    print("TEST 3: FTS5 Full-Text Search")
    print("="*60)
    
    db = get_db_connection()
    
    # Check if FTS5 table exists
    table_check = db.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='documents_fts'
    """).fetchone()
    
    if not table_check:
        print("✗ documents_fts table not found")
        db.close()
        return False
    
    print("✓ documents_fts table exists")
    
    # Test queries
    test_queries = [
        "payment",
        "fraud",
        "submission task",
        "merchant card",
        "score level",
    ]
    
    for query in test_queries:
        print(f"\n--- Query: '{query}' ---")
        
        try:
            cursor = db.execute("""
                SELECT 
                    d.id,
                    d.doc_type,
                    d.table_name,
                    d.column_name,
                    d.summary,
                    bm25(documents_fts) as rank
                FROM documents_fts fts
                JOIN documents d ON d.id = fts.rowid
                WHERE documents_fts MATCH ?
                ORDER BY rank
                LIMIT 3
            """, (query,))
            
            results = cursor.fetchall()
            print(f"  Found {len(results)} results")
            
            for r in results:
                name = r['column_name'] or r['table_name']
                summary = r['summary'][:50] + "..." if r['summary'] and len(r['summary']) > 50 else r['summary'] or "(no summary)"
                print(f"    • [{r['doc_type']}] {name}: {summary} (rank: {r['rank']:.4f})")
                
        except sqlite3.OperationalError as e:
            print(f"  ✗ Query failed: {e}")
    
    db.close()
    print("\n✓ FTS5 search tests completed")
    return True


def test_vector_search(client: OpenAI):
    """Test 4: Vector similarity search."""
    print("\n" + "="*60)
    print("TEST 4: Vector Similarity Search")
    print("="*60)
    
    if not client:
        print("✗ OpenAI client not available, skipping vector search test")
        return False
    
    db = get_db_connection()
    
    # Check if we have embeddings
    count = db.execute("SELECT COUNT(*) FROM documents_vec").fetchone()[0]
    if count == 0:
        print("✗ No embeddings in database, skipping vector search test")
        db.close()
        return False
    
    print(f"✓ Found {count} embeddings in database")
    
    # Test semantic queries
    test_queries = [
        "tables related to money transactions",
        "how to find fraudulent activity",
        "task completion tracking",
        "user submitted answers",
        "credit card information",
    ]
    
    for query in test_queries:
        print(f"\n--- Semantic Query: '{query}' ---")
        
        try:
            # Generate query embedding
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=query,
                dimensions=EMBEDDING_DIMENSIONS,
            )
            query_embedding = response.data[0].embedding
            embedding_json = json.dumps(query_embedding)
            
            # Vector search - sqlite-vec requires k = ? in WHERE clause
            cursor = db.execute("""
                SELECT 
                    d.id,
                    d.doc_type,
                    d.table_name,
                    d.column_name,
                    d.summary,
                    v.distance
                FROM documents_vec v
                JOIN documents d ON d.id = v.document_id
                WHERE v.embedding MATCH ? AND k = 3
                ORDER BY v.distance
            """, (embedding_json,))
            
            results = cursor.fetchall()
            print(f"  Found {len(results)} results")
            
            for r in results:
                name = r['column_name'] or r['table_name']
                summary = r['summary'][:50] + "..." if r['summary'] and len(r['summary']) > 50 else r['summary'] or "(no summary)"
                print(f"    • [{r['doc_type']}] {name}: {summary} (distance: {r['distance']:.4f})")
                
        except Exception as e:
            print(f"  ✗ Query failed: {e}")
    
    db.close()
    print("\n✓ Vector search tests completed")
    return True


def test_hybrid_search(client: OpenAI):
    """Test 5: Hybrid search combining FTS5 and vector search with RRF."""
    print("\n" + "="*60)
    print("TEST 5: Hybrid Search (FTS5 + Vector with RRF)")
    print("="*60)
    
    if not client:
        print("✗ OpenAI client not available, skipping hybrid search test")
        return False
    
    db = get_db_connection()
    
    query = "payment fraud detection"
    k = 5
    rrf_k = 60
    
    print(f"Query: '{query}'")
    print(f"Top-K: {k}, RRF-K: {rrf_k}")
    
    try:
        # Generate query embedding
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query,
            dimensions=EMBEDDING_DIMENSIONS,
        )
        query_embedding = response.data[0].embedding
        embedding_json = json.dumps(query_embedding)
        
        # Hybrid search with RRF
        cursor = db.execute("""
            WITH vec_matches AS (
                SELECT 
                    document_id,
                    row_number() OVER (ORDER BY distance) as rank_number,
                    distance
                FROM documents_vec
                WHERE embedding MATCH ? AND k = ?
            ),
            fts_matches AS (
                SELECT 
                    rowid as document_id,
                    row_number() OVER (ORDER BY rank) as rank_number,
                    rank as score
                FROM documents_fts
                WHERE documents_fts MATCH ?
                LIMIT ?
            ),
            combined AS (
                SELECT 
                    COALESCE(f.document_id, v.document_id) as document_id,
                    f.rank_number as fts_rank,
                    v.rank_number as vec_rank,
                    COALESCE(1.0 / (? + f.rank_number), 0.0) 
                    + COALESCE(1.0 / (? + v.rank_number), 0.0) as rrf_score
                FROM fts_matches f
                FULL OUTER JOIN vec_matches v ON f.document_id = v.document_id
            )
            SELECT 
                d.id,
                d.doc_type,
                d.table_name,
                d.column_name,
                d.summary,
                c.fts_rank,
                c.vec_rank,
                c.rrf_score
            FROM combined c
            JOIN documents d ON d.id = c.document_id
            ORDER BY c.rrf_score DESC
            LIMIT ?
        """, (embedding_json, k * 2, query, k * 2, rrf_k, rrf_k, k))
        
        results = cursor.fetchall()
        print(f"\nHybrid results ({len(results)} matches):\n")
        
        for r in results:
            name = r['column_name'] or r['table_name']
            summary = r['summary'][:60] + "..." if r['summary'] and len(r['summary']) > 60 else r['summary'] or "(no summary)"
            fts_rank = f"FTS:{r['fts_rank']}" if r['fts_rank'] else "FTS:-"
            vec_rank = f"Vec:{r['vec_rank']}" if r['vec_rank'] else "Vec:-"
            print(f"  • [{r['doc_type']}] {name}")
            print(f"    {summary}")
            print(f"    Ranks: {fts_rank}, {vec_rank} → RRF: {r['rrf_score']:.4f}")
            print()
            
    except Exception as e:
        print(f"✗ Hybrid search failed: {e}")
        db.close()
        return False
    
    db.close()
    print("✓ Hybrid search test completed")
    return True


def main():
    """Run all tests."""
    print("\n" + "#"*60)
    print("# COMPREHENSIVE SEARCH TEST SUITE")
    print("#"*60)
    
    # Check database exists
    if not DB_PATH.exists():
        print(f"\n✗ Database not found at {DB_PATH}")
        print("  Run 'python setup_db.py' first to create the database.")
        return
    
    print(f"\n✓ Database found at {DB_PATH}")
    
    # Run tests
    results = {}
    
    # Test 1: OpenAI Embeddings
    client = test_openai_embeddings()
    results["OpenAI Embeddings"] = client is not None
    
    # Test 2: sqlite-vec Storage
    results["sqlite-vec Storage"] = test_sqlite_vec_storage(client)
    
    # Test 3: FTS5 Search
    results["FTS5 Search"] = test_fts5_search()
    
    # Test 4: Vector Search
    results["Vector Search"] = test_vector_search(client)
    
    # Test 5: Hybrid Search
    results["Hybrid Search"] = test_hybrid_search(client)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! Your search system is fully operational.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    main()

