from datetime import datetime
from typing import List


class Habit:
    def __init__(self, id: int, name: str, description: str, frequency: str, created_at: str, streak: int = 0, completion_dates: List[str] = None):
        """
        Represents a habit that the user wants to track.

        :param id: Unique identifier for the habit
        :param name: Name of the habit
        :param frequency: Frequency of the habit (daily or weekly)
        :param description: Optional description of the habit
        :param created_at: Creation date of the habit (default: current time)
        :param streak: Consecutive success count
        :param completion_dates: List of dates when habit was marked completed
        """
        self.id = id
        self.name = name
        self.frequency = frequency
        self.description = description
        self.created_at =created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.streak = streak
        self.completion_dates = completion_dates if completion_dates else[]

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
        return f"Habit(id={self.id}, name={self.name}, frequency={self.frequency}, description={self.description}, created_at={self.created_at}, streak={self.streak}, completion_dates={self.completion_dates})"
