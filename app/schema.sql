CREATE TABLE IF NOT EXISTS todos (
     id INTEGER PRIMARY KEY,
     user_email TEXT NOT NULL,
     title TEXT NOT NULL,
     decription TEXT NOT NULL
)