import sqlite3
from datetime import datetime

DB_NAME = 'resume_parser.db'

def initialize_database():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Users table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Parsed resume data table with timestamp
    c.execute('''
    CREATE TABLE IF NOT EXISTS parsed_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        education TEXT,
        experience TEXT,
        linkedin_url TEXT,
        github_url TEXT,
        parsed_on TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()

def add_user(name, email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        return True, "User added successfully"
    except sqlite3.IntegrityError:
        return False, "User with this email already exists"
    finally:
        conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def save_parsed_data(user_id, data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    parsed_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO parsed_data (
            user_id, name, email, phone, skills, education, experience, linkedin_url, github_url, parsed_on
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        data.get('name', 'N/A'),
        data.get('email', 'N/A'),
        data.get('phone', 'N/A'),
        data.get('skills', 'N/A'),
        data.get('education', 'N/A'),
        data.get('experience', 'N/A'),
        data.get('linkedin_url', 'N/A'),
        data.get('github_url', 'N/A'),
        parsed_on
    ))
    conn.commit()
    conn.close()

def get_user_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT name, email, phone, skills, education, experience, linkedin_url, github_url, parsed_on
        FROM parsed_data
        WHERE user_id=?
        ORDER BY parsed_on DESC
    ''', (user_id,))
    rows = c.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "name": row[0],
            "email": row[1],
            "phone": row[2],
            "skills": row[3],
            "education": row[4],
            "experience": row[5],
            "linkedin_url": row[6],
            "github_url": row[7],
            "parsed_on": row[8]
        })

    return history

def clear_user_history(user_id):
    """
    Delete all parsed resume records for a user.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM parsed_data WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()