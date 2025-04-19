import sqlite3
from datetime import datetime 
import json

class Database:
    def __init__(self, db_path='data/habits.db'):
        self.db_path = db_path 
        self._create_tables()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _create_tables(self):
        conn = self._connect()
        cursor = conn.cursor()

        # Create 'habits' table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           frequency TEXT CHECK(frequency IN ('daily', 'weekly')) NOT NULL,
           streak INTEGER DEFAULT 0,
           completion_dates TEXT DEFAULT '[]',
           created_at TEXT NOT NULL
        ) 
        ''')

        cursor.execute("PRAGMA table_info(habits)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'description' not in columns:
            cursor.execute("ALTER TABLE habits ADD COLUMN description TEXT")
        if 'completion_dates' not in columns:
            cursor.execute("ALTER TABLE habits ADD COLUMN completion_dates TEXT DEFAULT '[]'")
        if 'streak' not in columns:
            cursor.execute("ALTER TABLE habits ADD COLUMN streak INTEGER DEFAULT 0")

        # Create logs table (optional, still useful)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_at TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
        )
        ''')

        conn.commit()
        conn.close()

    def add_habit(self, name: str, description: str, frequency: str):
        if frequency not in ['daily', 'weekly']:
            raise ValueError("Frequency must be 'daily' or 'weekly'")

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO habits (name, description, frequency, created_at, completion_dates, streak)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, description, frequency, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), json.dumps([]), 0))
        conn.commit()
        conn.close()

    def complete_habit(self, habit_id: int):
        today = datetime.now().strftime('%Y-%m-%d')
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('SELECT completion_dates, streak FROM habits WHERE id = ?', (habit_id,))
        row = cursor.fetchone()

        if row:
            dates_json, current_streak = row
            completion_dates = json.loads(dates_json) if dates_json else []

            if today in completion_dates:
                print("Habit already completed today.")
            else:
                completion_dates.append(today)
                new_streak = current_streak + 1

                cursor.execute('''
                UPDATE habits
                SET completion_dates = ?, streak = ?
                WHERE id = ?
                ''', (json.dumps(completion_dates), new_streak, habit_id))

                cursor.execute('''
                INSERT INTO habit_logs (habit_id, completed_at)
                VALUES (?, ?)
                ''', (habit_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        else:
            print(f"Habit with ID {habit_id} not found.") 

        conn.commit()
        conn.close()

    def get_habits(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, description, frequency, created_at, streak, completion_dates FROM habits')
        habits = cursor.fetchall()
        conn.close()
        return habits
     
    def get_habit_logs(self, habit_id: int):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habit_logs WHERE habit_id = ?', (habit_id,))
        logs = cursor.fetchall()
        conn.close()
        return logs

    def delete_habit(self, habit_id: int):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        conn.commit()
        conn.close()

    def create_tables(self):
        """Public method to create tables for testing."""
        self._create_tables()
