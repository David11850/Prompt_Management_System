# init_db.py
import sqlite3

conn=sqlite3.connect('prompt_manager.db')

cursor=conn.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS prompts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        create_at DATETIME DEFAULT CURRENT_TIMESTAMP);
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS prompt_versions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt_id INTEGER NOT NULL,
        version INTEGER NOT NULL,
        content TEXT NOT NULL,
        tags TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(prompt_id) REFERENCES prompts(id),
        UNIQUE(prompt_id,version));
    ''')

conn.commit()
conn.close()