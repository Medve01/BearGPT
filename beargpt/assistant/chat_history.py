import sqlite3
from uuid import uuid4
from flask import current_app as app

# Initialize the SQLite database
db_file = 'chat_history.db'

def create_connection():
    conn = sqlite3.connect(db_file)
    return conn

# Create tables if they don't exist
# conn = create_connection()
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS sessions
#                   (id TEXT PRIMARY KEY, name TEXT NOT NULL)''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS history (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     session_id TEXT NOT NULL,
#                     role TEXT NOT NULL,
#                     content TEXT NOT NULL,
#                     message_id TEXT UNIQUE NOT NULL
#                 );''')
# conn.commit()


def create_chat_session(name):
    conn = create_connection()
    cursor = conn.cursor()
    session_id = str(uuid4())
    cursor.execute("INSERT INTO sessions VALUES (?, ?)", (session_id, name))
    conn.commit()
    return session_id

def delete_chat_session(session_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE id=?", (session_id,))
    conn.commit()

def get_chat_sessions():
    app.logger.debug("Getting chat sessions")
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions")
    result = cursor.fetchall()
    conn.close()
    sessions = [{"id": row[0], "name": row[1]} for row in result]
    return sessions

def get_chat_history(session_id, raw=False, skip_remembered=False):
    conn = create_connection()
    cursor = conn.cursor()

    if raw:
        SQL = "SELECT * FROM history WHERE session_id=?"
    else:
        SQL = "SELECT role, content FROM history WHERE session_id=?"
    if skip_remembered:
        SQL += " AND remembered = 0"
    cursor.execute(SQL, (session_id,))
    result = cursor.fetchall()
    conn.close()

    if raw:
        history = [{"session_id": row[0], "role": row[1], "content": row[2], "message_id": row[3], "remembered": row[4]} for row in result]
    else:
        history = [{"role": row[0], "content": row[1]} for row in result]

    return history


def store_message(session_id, sender, message):
    conn = create_connection()
    cursor = conn.cursor()
    message_id = str(uuid4())
    cursor.execute("INSERT INTO history (message_id, session_id, role, content) VALUES (?, ?, ?, ?)", (message_id, session_id, sender, message))
    conn.commit()
    cursor.close()
    conn.close()

def remember_message(message_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE history SET role='remembered' WHERE message_id=?", (message_id,))
    conn.commit()
    cursor.close()
    conn.close()

def flush_chat_history(session_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history WHERE session_id=?", (session_id,))
    conn.commit()

def rename_chat_session(session_id, new_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE sessions SET name=? WHERE id=?", (new_name, session_id))
    conn.commit()

def delete_message(session_id, message_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history WHERE session_id=? AND message_id=?", (session_id, message_id))
    conn.commit()

def update_remembered(session_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE history SET role='remembered' WHERE session_id=?", (session_id,))
    conn.commit()