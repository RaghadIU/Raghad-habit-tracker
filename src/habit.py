from datetime import datetime
from typing import List


class Habit:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        frequency: str,
        created_at: str,
        streak: int = 0,
        completion_dates: List[str] = None
    ):
        """
        Represents a habit that the user wants to track.

        :param id: Unique identifier for the habit
        :param name: Name of the habit
        :param frequency: Frequency of the habit (daily or weekly)
        :param description: Optional description of the habit
        :param created_at: Creation date of the habit
        :param streak: Consecutive success count
        :param completion_dates: List of dates when the habit was completed
        """
        self.id = id
        self.name = name
        self.frequency = frequency
        self.description = description
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.streak = streak
        self.completion_dates = completion_dates if completion_dates is not None else []

    def complete_habit(self):
        """
        Mark the habit as completed today and update the streak.
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # Prevent duplicate completion for the same day
        if today in self.completion_dates:
            print("Habit already completed today.")
            return

        self.completion_dates.append(today)

        # Simple streak increment logic (custom logic can be applied if needed)
        if self.frequency == "daily":
            self.streak += 1
        elif self.frequency == "weekly":
            self.streak += 1  # Weekly logic can be refined further

    def __repr__(self):
        return (
            f"Habit(id={self.id}, name={self.name}, frequency={self.frequency}, "
            f"description={self.description}, created_at={self.created_at}, streak={self.streak}, "
            f"completion_dates={self.completion_dates})"
        )

