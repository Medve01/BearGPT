from tinydb import TinyDB, Query
from uuid import uuid4
from assistant import config

# Initialize the TinyDB instance
chat_history_file = config.config("chat_history_file")
db = TinyDB(chat_history_file)

# Table for chat sessions
sessions_table = db.table("sessions")
# Table for chat history
history_table = db.table("history")

def create_chat_session(name):
    session_id = str(uuid4())
    sessions_table.insert({"id": session_id, "name": name})
    return session_id

def delete_chat_session(session_id):
    session_query = Query()
    sessions_table.remove(session_query.id == session_id)
    history_table.remove(session_query.session_id == session_id)

def get_chat_sessions():
    return sessions_table.all()

def get_chat_history(session_id):
    ChatHistory = Query()
    raw_history = history_table.search(ChatHistory.session_id == session_id)
    history = []

    for message in raw_history:
        history.append({"role": message["role"], "content": message["content"]})

    return history


def store_message(session_id, sender, message):
    history_table.insert({"session_id": session_id, "role": sender, "content": message})

def flush_chat_history(session_id):
    history_query = Query()
    history_table.remove(history_query.session_id == session_id)

def rename_chat_session(session_id, new_name):
    session_query = Query()
    sessions_table.update({"name": new_name}, session_query.id == session_id)
