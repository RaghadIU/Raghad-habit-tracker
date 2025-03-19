import unittest
from datetime import datetime
from habits.database import Database
from habits.habit import Habit


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.habit = Habit("Test Habit", "daily")

    def test_add_habit(self):
        self.db.add_habit(self.habit)
        habits = self.db.get_habits()
        self.assertEqual(len(habits), 1)

    def test_add_completion(self):
        self.db.add_habit(self.habit)
        self.db.add_completion(1, datetime.now())
        # You can add more assertions here to test the completions table.


if __name__ == "__main__":
    unittest.main()
