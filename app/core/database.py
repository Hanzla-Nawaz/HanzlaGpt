import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings

DSN = (
    f"host={settings.PG_HOST} port={settings.PG_PORT}"
    f" dbname={settings.PG_DATABASE} user={settings.PG_USER}"
    f" password={settings.PG_PASSWORD}"
)

def get_db_connection():
    conn = psycopg2.connect(DSN, cursor_factory=RealDictCursor)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SET search_path TO public;")
    return conn

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            session_id VARCHAR(255) NOT NULL,
            query TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS documents_metadata (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            doc_type VARCHAR(255) NOT NULL,
            file_name TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(user_id, doc_type, file_name)
        );
        """
    )
    cur.close()
    conn.close()

def log_chat(user_id: str, session_id: str, query: str, answer: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO chat_history (user_id, session_id, query, answer)
        VALUES (%s, %s, %s, %s);
        """,
        (user_id, session_id, query, answer)
    )
    cur.close()
    conn.close()