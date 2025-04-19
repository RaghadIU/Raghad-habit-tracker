import sqlite3
import json
from datetime import datetime, timedelta

class Analytics:
    def __init__(self, db_path='data/habits.db'):
        self.db_path = db_path
    
    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _calculate_longest_streak(self, completion_dates):
        """
        Helper function to calculate the longest streak from a list of dates.
        :param completion_dates: List of completion dates as strings.
        :return: Longest consecutive streak.
        """
        dates = sorted([datetime.strptime(date, "%Y-%m-%d") for date in completion_dates])
        if not dates:
            return 0

        longest = current = 1
        for i in range(1, len(dates)):
            if dates[i] - dates[i - 1] == timedelta(days=1):
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        return longest

    def get_longest_streak(self):
        """
        Retrieves the habit with the longest streak based on recorded dates.
        :return: (habit_name, longest_streak)
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name, completion_dates FROM habits")
        habits = cursor.fetchall()
        conn.close()

        longest_streak = 0
        longest_habit = None

        for name, dates_json in habits:
            dates = json.loads(dates_json) if dates_json else []
            streak = self._calculate_longest_streak(dates)
            if streak > longest_streak:
                longest_streak = streak
                longest_habit = name

        return (longest_habit, longest_streak) if longest_habit else (None, 0)

    def get_most_missed_habit(self):
        """
        Finds the habit with the least completions (i.e., most missed).
        :return: (habit_name, completion_count)
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name, completion_dates FROM habits")
        habits = cursor.fetchall()
        conn.close()

        if not habits:
            return (None, 0)

        most_missed = habits[0][0]
        fewest = len(json.loads(habits[0][1]) if habits[0][1] else [])

        for name, dates_json in habits[1:]:
            dates = json.loads(dates_json) if dates_json else []
            if len(dates) < fewest:
                fewest = len(dates)
                most_missed = name

        return (most_missed, fewest)

    def calculate_streak(self, habit_name):
        """
        Calculates the streak (total completions) for a specific habit.
        :param habit_name: The name of the habit.
        :return: Streak count (total completions).
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT completion_dates FROM habits WHERE name = ?", (habit_name,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0]:
            completion_dates = json.loads(result[0])
            return len(completion_dates)
        return 0

    def average_streak(self):
        """
        Calculates the average number of completions across all habits.
        :return: Average completion count.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT completion_dates FROM habits")
        habits = cursor.fetchall()
        conn.close()

        total = 0
        count = 0

        for dates_json in habits:
            if dates_json[0]:
                dates = json.loads(dates_json[0])
                total += len(dates)
                count += 1

        return total / count if count > 0 else 0

    def delete_habit(self, habit_name):
        """
        Deletes a habit by its name.
        :param habit_name: Name of the habit to delete.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM habits WHERE name = ?', (habit_name,))
        conn.commit()
        conn.close()
