import sqlite3
import logging

DB_FILE = "responses.db"

def setup_database():
    """Initialize the SQLite database and create the responses table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                tool TEXT,
                response_text TEXT,
                reference_link TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def store_response(topic, tool, response_text, reference_link=None):
    """Store the AI-generated response in the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO responses (topic, tool, response_text, reference_link)
            VALUES (?, ?, ?, ?)
        ''', (topic, tool, response_text, reference_link))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Error storing response: {e}")
