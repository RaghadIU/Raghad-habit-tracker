from datetime import datetime
from typing import List

class Habit:
    def __init__(self, name: str, description: str, frequency: str, created_at: str = None):
        """
       Class represents the habit that a user can add and track.
        :param id: Unique identifier for the habit
        :param name: Habit Name
        :param description: Optional description of the habit
        :param frequency: frequent the habit ('daily' or 'weekly')
        :param created_at: Custom creation date (by default is current time)
        :param streak: Consecutive success count
        :param completion_dates: List of dates when habit was marked completed
        """
        self.id = id
        self.name = name
        self.description = description
        self.frequency = frequency
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.streak = streak
        self.completion_dates = completion_dates if completion_dates else []

    def complete_habit(self):
        """
        Mark the habit as completed and update streak.
        """
        today = datetime.now().strftime("%Y-%m-%d")

       # Handle daily habit completion
        if self.frequency == "daily":
            if today not in self.completion_dates:
                self.completion_dates.append(today)
                self.streak += 1
        elif self.frequency == "weekly":
            # Handle weekly habit completion (only update streak once per week)
            weekday = datetime.now().strftime("%A")  # Get the current weekday
            if weekday not in self.completion_dates:
                self.completion_dates.append(weekday)
                self.streak += 1


    def __repr__(self):
        return f"Habit(id={self.id}, name={self.name}, description={self.description}, frequency={self.frequency}, created_at={self.created_at}, streak={self.streak}, complete_habit={self.complete_habit})"
