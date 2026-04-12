import sqlite3
import os
import time
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv('DATABASE')

class DB_service():
    def __init__(self, DATABASE):
        self.database = DATABASE

    def create_tables(self):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute(""" CREATE TABLE IF NOT EXISTS users (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    chat_id INTEGER NOT NULL,
                    username TEXT NOT NULL) """)
            
            cur.execute(""" CREATE TABLE IF NOT EXISTS prompts (
                        user_id INTEGER,
                        user_prompt TEXT NOT NULL,
                        AI_answer TEXT NOT NULL) """)
            
            cur.execute(""" CREATE TABLE IF NOT EXISTS leonardo_prompts (
                            user_id INTEGER,
                            prompt TEXT NOT NULL,
                            username TEXT) """)
            
            cur.execute('''CREATE TABLE IF NOT EXISTS active_games (
                        chat_id INTEGER PRIMARY KEY, 
                        bot_choice INTEGER, 
                        attempts INTEGER DEFAULT 0, 
                        created_at REAL DEFAULT 0
                    )''')
            
            cur.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                        username TEXT PRIMARY KEY, 
                        best_score INTEGER, 
                        last_play TEXT
                    )''')
            conn.commit()
    
    def start_game(self, chat_id, bot_choice):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("INSERT OR REPLACE INTO active_games VALUES (?, ?, 0, ?)", 
                       (chat_id, bot_choice, time.time()))
        conn.commit()
    
    def get_game(self, chat_id):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM active_games WHERE chat_id=? AND ? - created_at < 300", 
                       (chat_id, time.time()))
        row = cur.fetchone()
        if not row:
            cur.execute("DELETE FROM active_games WHERE chat_id=?", (chat_id,))
            conn.commit()
        return row
    
    def save_attempt(self, chat_id, attempts):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE active_games SET attempts=?, created_at=? WHERE chat_id=?", 
                       (attempts, time.time(), chat_id))
        conn.commit()
    
    def end_game(self, chat_id, username, attempts):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM active_games WHERE chat_id=?", (chat_id,))
            
            cur.execute("SELECT best_score FROM leaderboard WHERE username=?", (username,))
            current = cur.fetchone()
            
            if current is None or attempts < current[0]:
                cur.execute("INSERT OR REPLACE INTO leaderboard VALUES (?, ?, datetime('now'))", (username, attempts))
            conn.commit()
    
    def get_leaderboard(self, limit=5):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("SELECT username, best_score FROM leaderboard ORDER BY best_score ASC LIMIT ?", (limit,))
            return cur.fetchall()
            
    def create_user(self, user_id, chat_id, username):
        with sqlite3.connect(self.database) as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO users (user_id, chat_id, username) 
                            VALUES (?, ?, ?)''', (user_id, chat_id, username))
                conn.commit()
            except sqlite3.IntegrityError:
                cur.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))

    def add_to_prompts(self, user_id, user_prompt, AI_answer):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute('''INSERT INTO prompts (user_id, user_prompt, AI_answer) 
                         VALUES (?, ?, ?)''', (user_id, user_prompt, AI_answer))
            conn.commit()
            
    def leonardo_AI(self, user_id, prompt, username):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute('''INSERT INTO leonardo_prompts (user_id, prompt, username)
                        VALUES (?, ?, ?)''', (user_id, prompt, username))
            conn.commit()
            
if __name__ == '__main__':
    manager = DB_service(DATABASE)
    manager.create_tables()