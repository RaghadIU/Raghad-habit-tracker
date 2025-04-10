import sqlite3
from datetime import datetime 
import json

class Database:
    def __init__(self, db_path='data/habits.db'):
        """
        Initializes the database connection and ensures tables are created.
        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path 
        self._create_tables()
          

    def _connect(self):
        """
        Establishes a connection to the database.
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _create_tables(self):
        """
        Creates necessary tables if they do not already exist.
        Also ensures all required columns exist (e.g., 'description').
        """
        conn = self._connect()
        cursor = conn.cursor()

         # Create 'habits' table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           frequency TEXT CHECK(frequency IN ('daily', 'weekly')) NOT NULL,
           streak INTEGER DEFAULT 0,
           complete_habit TEXT DEFAULT '[]',
           created_at TEXT NOT NULL
        ) 
        ''')

        cursor.execute("PRAGMA table_info(habits)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'description' not in columns:
            cursor.execute("ALTER TABLE habits ADD COLUMN description TEXT")
        if 'streak' not in columns:
            cursor.execute("ALTER TABLE habits ADD COLUMN streak INTEGER DEFAULT 0")

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
        """
        Logs the completion of a habit without storing completion dates.
        :param habit_id: ID of the habit being completed.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habits WHERE id = ?', (habit_id,))
        habit = cursor.fetchone()

        if habit:
            current_streak = habit[3] 
            streak = current_streak + 1

           
            cursor.execute('''
            UPDATE habits
            SET streak = ?
            WHERE id = ?
            ''', (streak, habit_id))

        
            cursor.execute('''INSERT INTO habit_logs (habit_id, completed_at) VALUES (?, ?)
            ''', (habit_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        else:
            print(f"Habit with ID {habit_id} not found.") 
        
        conn.commit()
        conn.close()

    def get_habits(self):
         """
         Retrieves all habits from the database.
         :return: List of habits.
         """
         conn = self._connect()
         cursor = conn.cursor()
         cursor.execute('SELECT * FROM habits')
         habits = cursor.fetchall()
         conn.close()
         return habits
     
    def get_habit_logs(self, habit_id: int):
         """
         Retrieves all logs for a specific habit.
         :param habit_id: ID of the habit.
         :return: List of log entries.
         """
         conn = self._connect()
         cursor = conn.cursor()
         cursor.execute('SELECT * FROM habit_logs WHERE habit_id = ?', (habit_id,))
         logs = cursor.fetchall()
         conn.close()
         return logs

    def delete_habit(self, habit_id: int):
        """
        Deletes a habit and all its associated logs from the database.
        :param habit_id: ID of the habit to be deleted.
        """
        conn = self._connect()
        cursor = conn.cursor()

        
        cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    
        conn.commit()
        conn.close()

    def create_tables(self):
       """Public method to create tables for testing."""
       self._create_tables()
