import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv('DATABASE')

class DB_service():
    def __init__(self, DATABASE):
        self.database = DATABASE

    def create_tables(self):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS AI_users (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    chat_id TEXT NOT NULL,
                    username TEXT) """)
            
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS prompts (
                        prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_prompt TEXT NOT NULL,
                        AI_answer TEXT NOT NULL) """)
            
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS leonardo_prompts (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            prompt TEXT NOT NULL,
                            username TEXT) """)
            
            conn.commit()
    
    def create_user(self, user_id, chat_id, username):
        with sqlite3.connect(self.database) as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO AI_users (user_id, chat_id, username) 
                            VALUES (?, ?, ?)''', (user_id, chat_id, username))
                conn.commit()
            except sqlite3.IntegrityError:
                cur.execute('UPDATE AI_users SET username = ? WHERE user_id = ?', (username, user_id))
            
    def add_to_prompts(self, user_prompt, AI_answer):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute('''INSERT INTO prompts (user_prompt, AI_answer) 
                         VALUES (?, ?)''', (user_prompt, AI_answer))
            
    def leonardo_AI(self, prompt, username):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute('''INSERT INTO leonardo_prompts (prompt, username)
                        VALUES (?, ?)''', (prompt, username))
            
if __name__ == '__main__':
    manager = DB_service(DATABASE)
    manager.create_tables()