import sqlite3

class Analytics:
    def __init__(self, db_path='data/habits.db'):
        """
        Initializes the Analytics module with database access.
        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
    
    def _connect(self):
        """
        Establishes a connection to the database.
        """
        return sqlite3.connect(self.db_path)
    
    def get_longest_streak(self):
        """
        Retrieves the habit with the longest streak.
        :return: Habit with the highest streak count.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT habits.name, COUNT(habit_logs.id) as streak 
            FROM habits 
            LEFT JOIN habit_logs ON habits.id = habit_logs.habit_id 
            GROUP BY habits.id 
            ORDER BY streak DESC 
            LIMIT 1''')
        result = cursor.fetchone()
        conn.close()
        return result if result else (None, 0)
    
    def get_habits_by_frequency(self, frequency):
        """
        Retrieves all habits with a given frequency.
        :param frequency: 'daily' or 'weekly'.
        :return: List of habits with the specified frequency.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habits WHERE frequency = ?', (frequency,))
        habits = cursor.fetchall()
        conn.close()
        return habits
    
    def get_most_missed_habit(self):
        """
        Finds the habit with the least completions.
        :return: Habit with the lowest number of completions.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT habits.name, COUNT(habit_logs.id) as completion_count 
            FROM habits 
            LEFT JOIN habit_logs ON habits.id = habit_logs.habit_id 
            GROUP BY habits.id 
            ORDER BY completion_count ASC 
            LIMIT 1''')
        result = cursor.fetchone()
        conn.close()
        return result if result else (None, 0)
