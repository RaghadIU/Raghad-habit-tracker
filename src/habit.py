from datetime import datetime

class Habit:
    def __init__(self, name: str, frequency: str, created_at: str = None):
        """
       Class represents the habit that a user can add and track.
        :param name: Habit Name
        :param frequency: frequent the habit ('daily' or 'weekly')
        :param created_at: Custom creation date (by default is current time)
        """
        self.name = name
        self.frequency = frequency
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.streak = 0 # Consecutive success series

    def complete_habit(self):
        """
This function is called when the habit is completed, which increases the success chain.
"""
        self.streak += 1

    def reset_streak(self):
       """
Reset the success chain when the user fails to complete the habit in the specified period.
"""
        self.streak = 0

    def __repr__(self):
        return f"Habit(name={self.name}, frequency={self.frequency}, created_at={self.created_at}, streak={self.streak})"
