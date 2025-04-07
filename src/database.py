import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_path='data/habits.db'):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            frequency TEXT CHECK(frequency IN ('daily', 'weekly')) NOT NULL,
            streak INTEGER DEFAULT 0,
            complete_habit TEXT DEFAULT '[]',
            created_at TEXT NOT NULL
        )
        ''')

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

    def add_habit(self, name: str, description : str, frequency: str ):
        """
        Adds a new habit to the database.
        :param name: Name of the habit.
        :param description: Description of the habit.
        :param frequency: Frequency of the habit ('daily' or 'weekly').
        """
        if frequency not in ['daily', 'weekly']:
            raise ValueError("Frequency must be 'daily' or 'weekly'")

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO habits (name, description, frequency, created_at ) VALUES (?, ?, ?, ?)''',
        (name, description, frequency, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        
    def complete_habit(self, habit_id: int):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habits WHERE id = ?', (habit_id,))
        habit = cursor.fetchone()

        if habit:
            try:
                streak = int(habit_id) + 1
            except ValueError:
                streak = 0

            cursor.execute('''
            UPDATE habits
            SET streak = ?
            WHERE id = ?
            ''', (streak, habit_id))

            cursor.execute('INSERT INTO habit_logs (habit_id, completed_at) VALUES (?, ?)',
                           (habit_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

    def get_habits(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habits')
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
        cursor.execute('DELETE FROM habit_logs WHERE habit_id = ?', (habit_id,))
        cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        conn.commit()
        conn.close()

    def create_tables(self):
        self._create_tables()
