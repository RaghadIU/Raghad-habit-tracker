import pytest
from datetime import datetime, timedelta
from src.habit import Habit

def test_habit_initialization():
    """Test Habit initialization with all parameters."""
    habit = Habit(
        id=1,
        name="Exercise",
        description="Daily workout",
        frequency="daily",
        created_at="2023-01-01 00:00:00",
        streak=5,
        completion_dates=["2023-01-01", "2023-01-02"]
    )
    assert habit.id == 1
    assert habit.name == "Exercise"
    assert habit.frequency == "daily"
    assert habit.streak == 5
    assert len(habit.completion_dates) == 2

def test_complete_daily_habit():
    """Test completing a daily habit."""
    habit = Habit(1, "Read", "Daily reading", "daily", created_at="2023-01-01 00:00:00")
    habit.complete_habit()
    assert habit.streak == 1
    assert datetime.now().strftime("%Y-%m-%d") in habit.completion_dates

def test_complete_weekly_habit():
    """Test completing a weekly habit."""
    habit = Habit(1, "Clean", "Weekly cleaning", "weekly", created_at="2023-01-01 00:00:00")
    habit.complete_habit()
    assert habit.streak == 1
    assert datetime.now().strftime("%A") in habit.completion_dates

def test_reset_streak():
    """Test resetting a habit streak."""
    habit = Habit(1, "Meditate", "Daily meditation", "daily", 
                 created_at="2023-01-01 00:00:00", streak=10)
    habit.reset_streak()
    assert habit.streak == 0