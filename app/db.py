import sqlite3
import os

# Define the path for the database file
DB_FOLDER = "data"
DATABASE_NAME = os.path.join(DB_FOLDER, "url_shortener.db")

def get_db_connection():
    """Establish a connection to the SQLite database."""
    # Ensure the folder exists
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Enable dictionary-style access for rows
    return conn

def initialize_db():
    """Create tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create URLs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_url TEXT UNIQUE NOT NULL,
        creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expiration_time TIMESTAMP
    )
    ''')
    
    # Create analytics table (optional for tracking)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_url_id INTEGER NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address TEXT NOT NULL,
        FOREIGN KEY(short_url_id) REFERENCES urls(id)
    )
    ''')

   
    conn.execute("""
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_url TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                access_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)    
# Call this function when your app starts
    
    conn.commit()
    conn.close()

# Initialize the database when the app starts
if __name__ == "__main__":
    initialize_db()
    print(f"Database initialized successfully! File location: {DATABASE_NAME}")

