import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from app.core.config import settings
from loguru import logger
from typing import Optional, Dict, Any
import contextlib

# Connection pool
_pool: Optional[SimpleConnectionPool] = None

def get_connection_pool() -> SimpleConnectionPool:
    """Get or create connection pool."""
    global _pool
    if _pool is None:
        try:
            _pool = SimpleConnectionPool(
                minconn=1,
                maxconn=50,  # Increased from 10 to 50 for better concurrency
                host=settings.PG_HOST,
                port=settings.PG_PORT,
                database=settings.PG_DATABASE,
                user=settings.PG_USER,
                password=settings.PG_PASSWORD,
                sslmode=getattr(settings, 'PG_SSLMODE', 'prefer')
            )
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Failed to create connection pool: {str(e)}")
            raise
    return _pool

@contextlib.contextmanager
def get_db_connection():
    """Context manager for database connections."""
    pool = get_connection_pool()
    conn = pool.getconn()
    try:
        conn.autocommit = True
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SET search_path TO public;")
        yield conn
    except Exception as e:
        logger.error(f"Database operation failed: {str(e)}")
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)

def ensure_column_exists(table: str, column: str, coltype: str):
    """Ensure a column exists in a table, add it if missing."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Check if column exists
                cur.execute(f"""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name=%s AND column_name=%s;
                """, (table, column))
                if not cur.fetchone():
                    logger.info(f"Column '{column}' missing in '{table}', adding it...")
                    cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype};")
                    logger.info(f"Column '{column}' added to '{table}'.")
    except Exception as e:
        logger.error(f"Failed to ensure column {column} in {table}: {str(e)}")

# Call this at startup or in create_tables

def create_tables():
    """Create database tables if they don't exist and ensure schema is up to date."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Chat history table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS chat_history (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        session_id VARCHAR(255) NOT NULL,
                        query TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        intent VARCHAR(100),
                        response_time_ms INTEGER,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)
                # Documents metadata table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS documents_metadata (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        doc_type VARCHAR(255) NOT NULL,
                        file_name TEXT NOT NULL,
                        file_size BIGINT,
                        upload_status VARCHAR(50) DEFAULT 'pending',
                        uploaded_at TIMESTAMP DEFAULT NOW(),
                        UNIQUE(user_id, doc_type, file_name)
                    );
                """)
                # Create indexes for better performance
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_chat_history_user_session 
                    ON chat_history(user_id, session_id);
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_chat_history_created_at 
                    ON chat_history(created_at);
                """)
        # Ensure all required columns exist (auto-migrate)
        ensure_column_exists('chat_history', 'response_time_ms', 'INTEGER')
        ensure_column_exists('chat_history', 'intent', 'VARCHAR(100)')
        ensure_column_exists('chat_history', 'created_at', 'TIMESTAMP DEFAULT NOW()')
        logger.info("Database tables and columns ensured successfully")
    except Exception as e:
        logger.error(f"Failed to create tables: {str(e)}")
        raise

def log_chat(user_id: str, session_id: str, query: str, answer: str, 
             intent: str = None, response_time_ms: int = None):
    """Log chat interaction to database."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO chat_history (user_id, session_id, query, answer, intent, response_time_ms)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (user_id, session_id, query, answer, intent, response_time_ms))
        logger.info(f"Chat logged for user {user_id}, session {session_id}")
    except Exception as e:
        logger.error(f"Failed to log chat: {str(e)}", exc_info=True)
        raise  # Raise so the API can warn the user

# Utility for debugging: fetch all chat history (not paginated)
def get_all_chat_history() -> list:
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM chat_history ORDER BY created_at DESC;")
                return cur.fetchall()
    except Exception as e:
        logger.error(f"Failed to fetch all chat history: {str(e)}")
        return []

def get_chat_history(user_id: str, session_id: str, limit: int = 50) -> list:
    """Get chat history for a user session."""
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT query, answer, intent, created_at 
                    FROM chat_history 
                    WHERE user_id = %s AND session_id = %s 
                    ORDER BY created_at DESC 
                    LIMIT %s;
                """, (user_id, session_id, limit))
                results = cur.fetchall()
                # Convert RealDictRow to regular dict for JSON serialization
                return [dict(row) for row in results]
    except Exception as e:
        logger.error(f"Failed to get chat history: {str(e)}")
        return []