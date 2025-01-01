import sqlite3

def init_db():
    """Initialize the database and create the keywords table if it doesn’t exist."""
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL UNIQUE,
            business_problem TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

