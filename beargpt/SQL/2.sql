CREATE TABLE meta (
  id INTEGER PRIMARY KEY,
  key TEXT NOT NULL,
  value TEXT
);
insert into meta (key, value) values ('last_sql', '2');
CREATE TABLE summaries (
  id INTEGER PRIMARY KEY,
  session_id TEXT NOT NULL,
  summary TEXT NOT NULL
);