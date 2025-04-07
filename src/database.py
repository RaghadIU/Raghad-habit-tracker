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
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        """
        Creates necessary tables if they do not already exist.
        """
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            frequency TEXT CHECK(frequency IN ('daily', 'weekly')) NOT NULL,
            streak INTEGER DEFAULT 0,
            complete_habit TEXT DEFAULT '[]',  -- Stored as JSON string
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
        """
        Logs the completion of a habit without storing completion dates.
        :param habit_id: ID of the habit being completed.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habits WHERE id = ?', (habit_id,))
        habit = cursor.fetchone()

        if habit:
            try:
                streak = int(habit_id) + 1  # Increment streak
            except ValueError:  # If value is invalid, reset to 0
                streak = 0

            # Update the habit with the new streak (no completion dates)
            cursor.execute('''
            UPDATE habits
            SET streak = ?
            WHERE id = ?
            ''', (streak, habit_id))

            # Log the completion (no completion date storage)
            cursor.execute('''INSERT INTO habit_logs (habit_id, completed_at) VALUES (?, ?)
            ''', (habit_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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

        # Delete the logs associated with the habit first (optional, depends on foreign key constraints)
        cursor.execute('DELETE FROM habit_logs WHERE habit_id = ?', (habit_id,))

        # Then delete the habit
        cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    
        conn.commit()
        conn.close()

    def create_tables(self):
       """Public method to create tables for testing."""
       self._create_tables()
