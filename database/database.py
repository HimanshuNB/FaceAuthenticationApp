import sqlite3

def setup_database():
    conn = sqlite3.connect("database/face_auth.db")
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        face_data BLOB NOT NULL,
        password_hash BLOB NOT NULL
    )''')

    # Create passwords table
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password BLOB NOT NULL
    )''')

    conn.commit()
    conn.close()

setup_database()