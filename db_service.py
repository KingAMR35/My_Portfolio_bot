import os
import time
import psycopg2
from psycopg2 import pool
from psycopg2 import OperationalError, InterfaceError
from dotenv import load_dotenv

load_dotenv()


class DB_service:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL is not set in .env")

        separator = "&" if "?" in self.database_url else "?"
        safe_url = (
            f"{self.database_url}{separator}"
            "keepalives=1&keepalives_idle=30&keepalives_interval=10&keepalives_count=3"
            "&connect_timeout=10&application_name=miniapp"
        )

        self.connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=safe_url
        )

    def get_connection(self):
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
            return conn
        except (OperationalError, InterfaceError):
            self.connection_pool.putconn(conn, close=True)
            conn = self.connection_pool.getconn()
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                return conn
            except (OperationalError, InterfaceError):
                self.connection_pool.putconn(conn, close=True)
                raise

    def release_connection(self, conn):
        try:
            self.connection_pool.putconn(conn)
        except Exception:
            try:
                self.connection_pool.putconn(conn, close=True)
            except Exception:
                pass

    def create_tables(self):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        ID SERIAL PRIMARY KEY,
                        user_id BIGINT UNIQUE NOT NULL,
                        chat_id BIGINT NOT NULL,
                        username TEXT NOT NULL
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS prompts (
                        user_id BIGINT,
                        user_prompt TEXT NOT NULL,
                        AI_answer TEXT NOT NULL
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS leonardo_prompts (
                        user_id BIGINT,
                        prompt TEXT NOT NULL,
                        username TEXT
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS active_games (
                        chat_id BIGINT PRIMARY KEY,
                        bot_choice INTEGER,
                        attempts INTEGER DEFAULT 0,
                        created_at DOUBLE PRECISION DEFAULT 0
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS leaderboard (
                        username TEXT PRIMARY KEY,
                        best_score INTEGER,
                        last_play TIMESTAMP DEFAULT NOW()
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS ADMINS (
                        user_id BIGINT UNIQUE NOT NULL
                    )
                """)
            conn.commit()
        finally:
            self.release_connection(conn)

    def start_game(self, chat_id, bot_choice):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO active_games (chat_id, bot_choice, attempts, created_at)
                    VALUES (%s, %s, 0, %s)
                    ON CONFLICT (chat_id)
                    DO UPDATE SET
                        bot_choice = EXCLUDED.bot_choice,
                        attempts = 0,
                        created_at = EXCLUDED.created_at
                """, (chat_id, bot_choice, time.time()))
            conn.commit()
        finally:
            self.release_connection(conn)

    def get_game(self, chat_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT chat_id, bot_choice, attempts, created_at
                    FROM active_games
                    WHERE chat_id = %s AND %s - created_at < 300
                """, (chat_id, time.time()))
                row = cur.fetchone()

                if not row:
                    cur.execute("DELETE FROM active_games WHERE chat_id = %s", (chat_id,))
                    conn.commit()

                return row
        finally:
            self.release_connection(conn)

    def save_attempt(self, chat_id, attempts):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE active_games
                    SET attempts = %s, created_at = %s
                    WHERE chat_id = %s
                """, (attempts, time.time(), chat_id))
            conn.commit()
        finally:
            self.release_connection(conn)

    def end_game(self, chat_id, username, attempts):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM active_games WHERE chat_id = %s", (chat_id,))

                cur.execute("SELECT best_score FROM leaderboard WHERE username = %s", (username,))
                current = cur.fetchone()

                if current is None or attempts < current[0]:
                    cur.execute("""
                        INSERT INTO leaderboard (username, best_score, last_play)
                        VALUES (%s, %s, NOW())
                        ON CONFLICT (username)
                        DO UPDATE SET
                            best_score = EXCLUDED.best_score,
                            last_play = NOW()
                    """, (username, attempts))
            conn.commit()
        finally:
            self.release_connection(conn)

    def get_leaderboard(self, limit=5):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT username, best_score
                    FROM leaderboard
                    ORDER BY best_score ASC
                    LIMIT %s
                """, (limit,))
                return cur.fetchall()
        finally:
            self.release_connection(conn)

    def create_user(self, user_id, chat_id, username):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (user_id, chat_id, username)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id)
                    DO UPDATE SET
                        chat_id = EXCLUDED.chat_id,
                        username = EXCLUDED.username
                """, (user_id, chat_id, username))
            conn.commit()
        finally:
            self.release_connection(conn)

    def add_to_prompts(self, user_id, user_prompt, AI_answer):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO prompts (user_id, user_prompt, AI_answer)
                    VALUES (%s, %s, %s)
                """, (user_id, user_prompt, AI_answer))
            conn.commit()
        finally:
            self.release_connection(conn)

    def leonardo_AI(self, user_id, prompt, username):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO leonardo_prompts (user_id, prompt, username)
                    VALUES (%s, %s, %s)
                """, (user_id, prompt, username))
            conn.commit()
        finally:
            self.release_connection(conn)

    def select_users(self):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT ID, user_id, username FROM users ORDER BY ID ASC")
                return cur.fetchall()
        finally:
            self.release_connection(conn)

    def add_new_admin(self, user_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO ADMINS (user_id)
                    VALUES (%s)
                    ON CONFLICT (user_id) DO NOTHING
                """, (user_id,))
            conn.commit()
        finally:
            self.release_connection(conn)

    def select_id(self, user_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS(SELECT 1 FROM ADMINS WHERE user_id = %s)", (user_id,))
                return cur.fetchone()[0]
        finally:
            self.release_connection(conn)

    def select_admins(self):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM ADMINS")
                return cur.fetchall()
        finally:
            self.release_connection(conn)

    def delete_admin(self, user_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM ADMINS WHERE user_id = %s", (user_id,))
                deleted = cur.rowcount > 0
            conn.commit()
            return deleted
        finally:
            self.release_connection(conn)


if __name__ == "__main__":
    manager = DB_service()
    manager.create_tables()