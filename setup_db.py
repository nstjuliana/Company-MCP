"""
Database setup script for Tribal Knowledge SQLite database.

Creates the SQLite database with:
- documents table for storing indexed documentation
- documents_fts FTS5 virtual table for full-text search  
- documents_vec vec0 virtual table for vector similarity search
- relationships table for pre-computed join paths
- keywords table for extracted keywords
- index_weights table for search weight configuration

Populates initial data from context_map.json and context_index.json
"""

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

# Try to import sqlite_vec; install with: pip install sqlite-vec
try:
    import sqlite_vec
    HAS_SQLITE_VEC = True
except ImportError:
    HAS_SQLITE_VEC = False
    print("Warning: sqlite-vec not installed. Vector search will be disabled.")
    print("Install with: pip install sqlite-vec")

# Try to import OpenAI for embeddings
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("Warning: openai not installed. Embeddings will not be generated.")
    print("Install with: pip install openai")

# Load environment variables from .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent
CONTEXT_MAP_PATH = BASE_DIR / "_docs" / "map" / "context_map.json"
CONTEXT_INDEX_PATH = BASE_DIR / "_docs" / "map" / "context_index.json"
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "tribal-knowledge.db"

# OpenAI embedding model configuration
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536


def load_json(path: Path) -> Any:
    """Load JSON file."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def create_tables(db: sqlite3.Connection) -> None:
    """Create all database tables."""
    
    # Main documents table
    db.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_type TEXT NOT NULL,
            database_name TEXT NOT NULL,
            schema_name TEXT,
            table_name TEXT,
            column_name TEXT,
            domain TEXT,
            content TEXT NOT NULL,
            summary TEXT,
            keywords TEXT,
            file_path TEXT,
            content_hash TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Indexes on documents table
    db.execute("CREATE INDEX IF NOT EXISTS idx_documents_database ON documents(database_name)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_documents_table ON documents(database_name, schema_name, table_name)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_documents_domain ON documents(domain)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(doc_type)")
    
    # FTS5 virtual table for full-text search
    db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
            content,
            summary,
            keywords,
            content='documents',
            content_rowid='id',
            tokenize='porter'
        )
    """)
    
    # Triggers to keep FTS5 in sync with documents table
    db.execute("""
        CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
            INSERT INTO documents_fts(rowid, content, summary, keywords)
            VALUES (new.id, new.content, new.summary, new.keywords);
        END
    """)
    
    db.execute("""
        CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
            INSERT INTO documents_fts(documents_fts, rowid, content, summary, keywords)
            VALUES ('delete', old.id, old.content, old.summary, old.keywords);
        END
    """)
    
    db.execute("""
        CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
            INSERT INTO documents_fts(documents_fts, rowid, content, summary, keywords)
            VALUES ('delete', old.id, old.content, old.summary, old.keywords);
            INSERT INTO documents_fts(rowid, content, summary, keywords)
            VALUES (new.id, new.content, new.summary, new.keywords);
        END
    """)
    
    # Relationships table for pre-computed join paths
    db.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            database_name TEXT NOT NULL,
            source_table TEXT NOT NULL,
            target_table TEXT NOT NULL,
            join_path TEXT NOT NULL,
            hop_count INTEGER NOT NULL,
            sql_snippet TEXT,
            confidence REAL,
            UNIQUE(database_name, source_table, target_table)
        )
    """)
    
    db.execute("CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(database_name, source_table)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(database_name, target_table)")
    
    # Keywords table for extracted keywords cache
    db.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT NOT NULL UNIQUE,
            source_type TEXT,
            frequency INTEGER DEFAULT 1
        )
    """)
    
    # Index weights table for search configuration
    db.execute("""
        CREATE TABLE IF NOT EXISTS index_weights (
            doc_type TEXT PRIMARY KEY,
            fts_weight REAL DEFAULT 1.0,
            vec_weight REAL DEFAULT 1.0,
            boost REAL DEFAULT 1.0
        )
    """)
    
    # Insert default weights
    db.executemany("""
        INSERT OR IGNORE INTO index_weights (doc_type, fts_weight, vec_weight, boost)
        VALUES (?, ?, ?, ?)
    """, [
        ('table', 1.0, 1.0, 1.5),
        ('relationship', 1.0, 1.0, 1.2),
        ('column', 0.8, 0.8, 1.0),
        ('domain', 1.0, 1.0, 1.0),
    ])
    
    db.commit()


def create_vector_table(db: sqlite3.Connection) -> None:
    """Create vector table using sqlite-vec."""
    if not HAS_SQLITE_VEC:
        print("Skipping vector table creation (sqlite-vec not available)")
        return
    
    # Load sqlite-vec extension
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    
    # Verify extension loaded
    vec_version = db.execute("SELECT vec_version()").fetchone()[0]
    print(f"sqlite-vec version: {vec_version}")
    
    # Create vec0 virtual table for vector search
    # The document_id column links back to documents.id
    db.execute(f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS documents_vec USING vec0(
            document_id INTEGER PRIMARY KEY,
            embedding float[{EMBEDDING_DIMENSIONS}]
        )
    """)
    
    db.commit()


def generate_embedding(client: "OpenAI", text: str) -> list[float]:
    """Generate embedding for text using OpenAI API."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
        dimensions=EMBEDDING_DIMENSIONS,
    )
    return response.data[0].embedding


def build_document_content(segment: dict[str, Any]) -> str:
    """Build searchable content string from a context map segment."""
    parts = [
        f"Table: {segment.get('id', '')}",
        f"Title: {segment.get('title', '')}",
        f"Summary: {segment.get('summary', '')}",
        f"Database: {segment.get('database', 'default')}",
        f"Domain: {segment.get('domain', 'default')}",
    ]
    
    # Add column information
    columns = segment.get('columns', [])
    if columns:
        col_strs = []
        for col in columns:
            col_str = f"{col.get('name', '')} ({col.get('type', '')})"
            if col.get('notes'):
                col_str += f": {col['notes']}"
            col_strs.append(col_str)
        parts.append(f"Columns: {', '.join(col_strs)}")
    
    # Add key information
    keys = segment.get('keys', {})
    if keys.get('primary'):
        parts.append(f"Primary Key: {', '.join(keys['primary'])}")
    if keys.get('foreign'):
        fk_strs = [f"{fk.get('columns', [])} -> {fk.get('references', '')}" for fk in keys['foreign']]
        parts.append(f"Foreign Keys: {'; '.join(fk_strs)}")
    
    # Add relationship information
    rels = segment.get('relationships', {})
    if rels.get('depends_on'):
        parts.append(f"Depends On: {', '.join(rels['depends_on'])}")
    if rels.get('referenced_by'):
        parts.append(f"Referenced By: {', '.join(rels['referenced_by'])}")
    
    return "\n".join(parts)


def extract_keywords(segment: dict[str, Any]) -> list[str]:
    """Extract keywords from a context map segment."""
    keywords = set()
    
    # Add table name parts
    table_id = segment.get('id', '')
    keywords.update(table_id.lower().split('_'))
    
    # Add column names
    for col in segment.get('columns', []):
        col_name = col.get('name', '')
        keywords.update(col_name.lower().split('_'))
    
    # Add domain
    domain = segment.get('domain', '')
    if domain:
        keywords.add(domain.lower())
    
    # Remove empty strings
    keywords.discard('')
    
    return list(keywords)


def populate_from_context_map(db: sqlite3.Connection, openai_client: "OpenAI | None") -> None:
    """Populate database from context_map.json."""
    
    if not CONTEXT_MAP_PATH.exists():
        print(f"Warning: {CONTEXT_MAP_PATH} not found, skipping population")
        return
    
    context_map = load_json(CONTEXT_MAP_PATH)
    print(f"Loaded {len(context_map)} segments from context_map.json")
    
    for segment in context_map:
        # Build document content
        content = build_document_content(segment)
        summary = segment.get('summary', '')
        keywords = extract_keywords(segment)
        keywords_json = json.dumps(keywords)
        
        # Insert into documents table
        cursor = db.execute("""
            INSERT INTO documents (
                doc_type, database_name, schema_name, table_name, 
                domain, content, summary, keywords
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'table',
            segment.get('database', 'default'),
            segment.get('schema', 'public'),
            segment.get('id', ''),
            segment.get('domain', 'default'),
            content,
            summary,
            keywords_json,
        ))
        
        doc_id = cursor.lastrowid
        
        # Generate and store embedding if OpenAI is available
        if openai_client and HAS_SQLITE_VEC:
            try:
                embedding = generate_embedding(openai_client, content)
                # Insert embedding as JSON array string
                embedding_json = json.dumps(embedding)
                db.execute("""
                    INSERT INTO documents_vec (document_id, embedding)
                    VALUES (?, ?)
                """, (doc_id, embedding_json))
                print(f"  Generated embedding for {segment.get('id', '')}")
            except Exception as e:
                print(f"  Warning: Failed to generate embedding for {segment.get('id', '')}: {e}")
        
        # Also insert individual column documents
        for col in segment.get('columns', []):
            col_content = f"Column: {col.get('name', '')} in table {segment.get('id', '')}\n"
            col_content += f"Type: {col.get('type', '')}\n"
            col_content += f"Notes: {col.get('notes', '')}"
            
            col_keywords = [
                col.get('name', '').lower(),
                col.get('type', '').lower(),
                segment.get('id', '').lower(),
            ]
            
            col_cursor = db.execute("""
                INSERT INTO documents (
                    doc_type, database_name, schema_name, table_name, column_name,
                    domain, content, summary, keywords
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'column',
                segment.get('database', 'default'),
                segment.get('schema', 'public'),
                segment.get('id', ''),
                col.get('name', ''),
                segment.get('domain', 'default'),
                col_content,
                col.get('notes', ''),
                json.dumps(col_keywords),
            ))
            
            # Generate embedding for column document too
            col_doc_id = col_cursor.lastrowid
            if openai_client and HAS_SQLITE_VEC:
                try:
                    col_embedding = generate_embedding(openai_client, col_content)
                    db.execute("""
                        INSERT INTO documents_vec (document_id, embedding)
                        VALUES (?, ?)
                    """, (col_doc_id, json.dumps(col_embedding)))
                except Exception as e:
                    pass  # Silent fail for columns
    
    db.commit()
    print(f"Populated database with table and column documents")


def populate_keywords_from_index(db: sqlite3.Connection) -> None:
    """Populate keywords table from context_index.json."""
    
    if not CONTEXT_INDEX_PATH.exists():
        print(f"Warning: {CONTEXT_INDEX_PATH} not found, skipping keywords population")
        return
    
    context_index = load_json(CONTEXT_INDEX_PATH)
    print(f"Loaded {len(context_index)} keywords from context_index.json")
    
    for term, tables in context_index.items():
        frequency = len(tables) if isinstance(tables, list) else 1
        db.execute("""
            INSERT OR REPLACE INTO keywords (term, source_type, frequency)
            VALUES (?, ?, ?)
        """, (term.lower(), 'index', frequency))
    
    db.commit()
    print(f"Populated keywords table")


def populate_relationships(db: sqlite3.Connection) -> None:
    """Populate relationships table from context_map foreign keys."""
    
    if not CONTEXT_MAP_PATH.exists():
        return
    
    context_map = load_json(CONTEXT_MAP_PATH)
    
    for segment in context_map:
        source_table = segment.get('id', '')
        database = segment.get('database', 'default')
        
        # Extract foreign key relationships
        for fk in segment.get('keys', {}).get('foreign', []) or []:
            ref = fk.get('references', '')
            target_table = ref.split('(')[0] if '(' in ref else ref
            
            if target_table:
                join_path = json.dumps([{
                    'from': source_table,
                    'to': target_table,
                    'on': ref,
                }])
                
                sql_snippet = f"{source_table} JOIN {target_table} ON {ref}"
                
                db.execute("""
                    INSERT OR IGNORE INTO relationships (
                        database_name, source_table, target_table,
                        join_path, hop_count, sql_snippet, confidence
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (database, source_table, target_table, join_path, 1, sql_snippet, 1.0))
    
    db.commit()
    print("Populated relationships table")


def main() -> None:
    """Main setup function."""
    
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Remove existing database to start fresh
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Removed existing database at {DB_PATH}")
    
    # Connect to database
    db = sqlite3.connect(str(DB_PATH))
    print(f"Created database at {DB_PATH}")
    
    # Create tables
    create_tables(db)
    print("Created tables and FTS5 index")
    
    # Create vector table (if sqlite-vec available)
    create_vector_table(db)
    
    # Initialize OpenAI client if available
    openai_client = None
    if HAS_OPENAI:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai_client = OpenAI(api_key=api_key)
            print("OpenAI client initialized for embeddings")
        else:
            print("Warning: OPENAI_API_KEY not set, embeddings will not be generated")
    
    # Populate data
    populate_from_context_map(db, openai_client)
    populate_keywords_from_index(db)
    populate_relationships(db)
    
    # Print summary
    doc_count = db.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    keyword_count = db.execute("SELECT COUNT(*) FROM keywords").fetchone()[0]
    rel_count = db.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
    
    print(f"\n=== Database Summary ===")
    print(f"Documents: {doc_count}")
    print(f"Keywords: {keyword_count}")
    print(f"Relationships: {rel_count}")
    
    if HAS_SQLITE_VEC:
        vec_count = db.execute("SELECT COUNT(*) FROM documents_vec").fetchone()[0]
        print(f"Vector embeddings: {vec_count}")
    
    db.close()
    print(f"\nDatabase setup complete: {DB_PATH}")


if __name__ == "__main__":
    main()

