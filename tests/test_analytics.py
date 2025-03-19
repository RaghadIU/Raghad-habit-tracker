import unittest
from analytics import Analytics
from database import Database

class TestAnalytics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Initialize the database and analytics module for testing.
        """
        cls.db = Database(db_path=':memory:')  # Use in-memory database for testing
        cls.analytics = Analytics(db_path=':memory:')
        cls.db.add_habit("Exercise", "daily")
        cls.db.add_habit("Reading", "weekly")
        
        # Log some completions
        cls.db.log_completion(1)
        cls.db.log_completion(1)
        cls.db.log_completion(2)
    
    def test_get_longest_streak(self):
        """
        Test retrieving the longest streak.
        """
        longest_streak = self.analytics.get_longest_streak()
        self.assertEqual(longest_streak[0], "Exercise")  # Exercise should have the longest streak
    
    def test_get_habits_by_frequency(self):
        """
        Test retrieving habits by frequency.
        """
        daily_habits = self.analytics.get_habits_by_frequency("daily")
        weekly_habits = self.analytics.get_habits_by_frequency("weekly")
        
        self.assertEqual(len(daily_habits), 1)
        self.assertEqual(len(weekly_habits), 1)
    
    def test_get_most_missed_habit(self):
        """
        Test retrieving the most missed habit.
        """
        most_missed = self.analytics.get_most_missed_habit()
        self.assertEqual(most_missed[0], "Reading")  # Reading has the least completions

if __name__ == "__main__":
    unittest.main()

