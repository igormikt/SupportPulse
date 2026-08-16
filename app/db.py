import sqlite3
import os
from app.config import DB_PATH

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            channel TEXT NOT NULL,
            client_id TEXT NOT NULL,
            category TEXT,
            draft_reply TEXT,
            confidence TEXT,
            escalate BOOLEAN,
            error TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn
