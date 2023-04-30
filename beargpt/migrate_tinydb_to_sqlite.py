from tinydb import TinyDB, Query
import sqlite3

db_file = 'chat_history.db'
json_file = 'chat_history.json'

def create_connection():
    conn = sqlite3.connect(db_file)
    return conn

# Create tables if they don't exist
conn = create_connection()
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS sessions
                    (id TEXT PRIMARY KEY, name TEXT NOT NULL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    message_id TEXT UNIQUE NOT NULL
                );''')
conn.commit()

def create_chat_session(session_id, name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions VALUES (?, ?)", (session_id, name))
    conn.commit()
    return session_id

def store_chat_history(session_id, role, content, message_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (session_id, role, content, message_id) VALUES (?, ?, ?, ?)", (session_id, role, content, message_id))
    conn.commit()

# fetch sessions from tinydb
db = TinyDB(json_file)
sessions = db.table('sessions')
history = db.table('history')
for session in sessions.all():
    session_id = session['id']
    name = session['name']
    create_chat_session(session_id, name)
    for message in history.search(Query().session_id == session_id):
        role = message['role']
        content = message['content']
        message_id = message['message_id']
        store_chat_history(session_id, role, content, message_id)

conn.close()
