import sqlite3
import os

def getDatabase(create = False, DB_FILE = "main.db"):
    if os.path.exists(DB_FILE):
        if create:
            os.remove(DB_FILE)
    
    con = sqlite3.connect(DB_FILE)
    con.execute('PRAGMA foreign_keys = ON')
    return con

def createDatabase():
    with getDatabase(create = True, DB_FILE = "main.db") as con:
        con.execute('''
CREATE TABLE users (
    user_id         INTEGER PRIMARY KEY,
    username        TEXT NOT NULL
)
''')
        con.execute('''
CREATE TABLE scores (
    score_id        INTEGER PRIMARY KEY,
    user_id         INTEGER,
    time            INTEGER,
    start_time      INTEGER,
    end_time        INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
''')

    print("Database has been successfully created.")
    con.commit()