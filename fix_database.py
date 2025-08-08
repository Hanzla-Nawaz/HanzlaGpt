#!/usr/bin/env python3
"""
Fix database schema issues for HanzlaGPT.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.database import get_connection_pool, create_tables
from loguru import logger

def fix_database():
    """Fix database schema issues."""
    
    print("🔧 Fixing database schema...")
    
    try:
        # Recreate tables with correct schema
        create_tables()
        
        # Check if intent column exists, if not add it
        pool = get_connection_pool()
        if pool:
            with pool.getconn() as conn:
                with conn.cursor() as cur:
                    # Check if intent column exists
                    cur.execute("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'chat_history' 
                        AND column_name = 'intent';
                    """)
                    
                    if not cur.fetchone():
                        print("➕ Adding missing 'intent' column...")
                        cur.execute("""
                            ALTER TABLE chat_history 
                            ADD COLUMN intent VARCHAR(100);
                        """)
                        print("✅ Intent column added successfully!")
                    else:
                        print("✅ Intent column already exists!")
                        
        print("✅ Database schema fixed successfully!")
        
    except Exception as e:
        print(f"❌ Error fixing database: {str(e)}")
        logger.error(f"Failed to fix database: {str(e)}")

if __name__ == "__main__":
    fix_database()
