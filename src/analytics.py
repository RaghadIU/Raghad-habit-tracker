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

    def calculate_streak(self, habit_name):
        """
        Calculates the current streak for a given habit.
        :param habit_name: Name of the habit.
        :return: The streak count for the habit.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT completion_dates FROM habits WHERE name = ?
        ''', (habit_name,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            completion_dates = result[0].split(',')
            streak = 0
            max_streak = 0
            prev_date = None

            for date in completion_dates:
                # Check if the completion dates are consecutive
                if prev_date is None or (self._is_consecutive(prev_date, date)):
                    streak += 1
                    max_streak = max(max_streak, streak)
                else:
                    streak = 1  # Reset streak for non-consecutive dates
                prev_date = date
            return max_streak
        return 0
    
    def get_habits_completion(self):
        """
        Retrieves habits and their completion status.
        :return: List of habits and their completion statuses.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT name, completion_dates FROM habits')
        habits = cursor.fetchall()
        conn.close()

        habits_status = []
        for habit in habits:
            name, completion_dates = habit
            completed = len(completion_dates.split(','))
            habits_status.append((name, completed))
        return habits_status
    
    def average_streak(self):
        """
        Calculates the average streak for all habits.
        :return: The average streak count.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM habits')
        habits = cursor.fetchall()
        
        total_streak = 0
        total_habits = 0
        
        for habit in habits:
            streak = self.calculate_streak(habit[0])  # Calculate streak for each habit
            total_streak += streak
            total_habits += 1
        
        conn.close()

        return total_streak / total_habits if total_habits > 0 else 0       

    def delete_habit(self, habit_name):
        """
        Deletes a habit by its name from the database.
        :param habit_name: Name of the habit to delete.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM habits WHERE name = ?', (habit_name,))
        conn.commit()
        conn.close()


    
