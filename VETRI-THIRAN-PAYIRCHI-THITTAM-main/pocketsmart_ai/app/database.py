import sqlite3
from pathlib import Path
from typing import Generator

# Database file location
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"


# Database connection
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Database connection for FastAPI
def db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


# Create database tables
def init_db():
    conn = get_connection()

    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    # Recommendations table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            planner_type TEXT,
            budget REAL,
            request_json TEXT,
            response_json TEXT
        )
    """)

    conn.commit()
    conn.close()