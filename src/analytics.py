import sqlite3
from datetime import datetime, timedelta

class Analytics:
    def __init__(self, db_path='data/habits.db'):
        self.db_path = db_path
    
    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_longest_streak(self):
        """
        Retrieves the habit with the longest streak based on continuous dates in habit_logs.
        """
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM habits")
        habits = cursor.fetchall()
        max_streak = 0
        max_habit = None

        for habit_id, habit_name in habits:
            cursor.execute("SELECT completed_at FROM habit_logs WHERE habit_id = ? ORDER BY completed_at", (habit_id,))
            dates = [datetime.strptime(row[0][:10], "%Y-%m-%d") for row in cursor.fetchall()]
        
            streak = 1
            longest = 1
            for i in range(1, len(dates)):
                if (dates[i] - dates[i - 1]).days == 1:
                    streak += 1
                    longest = max(longest, streak)
                else:
                    streak = 1
        
            if longest > max_streak:
                max_streak = longest
                max_habit = habit_name

        conn.close()
        return (max_habit, max_streak) if max_habit else (None, 0)

    def get_most_missed_habit(self):
        """
        Identifies the habit with the most missed completions based on 28 days (4 weeks).
        Only checks daily habits.
        """
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM habits WHERE frequency = 'daily'")
        habits = cursor.fetchall()
        
        max_missed = 0
        missed_habit = None

        for habit_id, habit_name in habits:
            cursor.execute("SELECT COUNT(*) FROM habit_logs WHERE habit_id = ?", (habit_id,))
            completed = cursor.fetchone()[0]
            missed = 28 - completed

            if missed > max_missed:
                max_missed = missed
                missed_habit = habit_name

        conn.close()
        return (missed_habit, max_missed) if missed_habit else (None, 0)

    def average_streak(self):
        """
        Calculates the average number of completions (over 28 days) across all habits.
        """
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM habits")
        habits = cursor.fetchall()
        
        total_streaks = 0
        total_habits = 0

        for (habit_id,) in habits:
            cursor.execute("SELECT COUNT(*) FROM habit_logs WHERE habit_id = ?", (habit_id,))
            count = cursor.fetchone()[0]
            total_streaks += count
            total_habits += 1

        conn.close()
        return total_streaks / total_habits if total_habits > 0 else 0

    def calculate_streak(self, habit_name):
        """
        Calculates total completions for a specific habit from habit_logs.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
        result = cursor.fetchone()

        if result:
            habit_id = result[0]
            cursor.execute("SELECT COUNT(*) FROM habit_logs WHERE habit_id = ?", (habit_id,))
            count = cursor.fetchone()[0]
        else:
            count = 0

        conn.close()
        return count

    def delete_habit(self, habit_name):
        """
        Deletes a habit by its name.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM habits WHERE name = ?', (habit_name,))
        conn.commit()
        conn.close()
