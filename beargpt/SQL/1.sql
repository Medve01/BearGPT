CREATE TABLE sessions
                  (id TEXT PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE history ( session_id TEXT NOT NULL, role TEXT NOT_NULL, content TEXT NOT NULL, message_id TEXT UNIQUE NOT NULL, remembered INTEGER DEFAULT 0);