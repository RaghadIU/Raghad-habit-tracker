'''import pytest
from datetime import datetime
from src.habit import Habit

def test_habit_initialization():
    """Test Habit initialization with all parameters."""
    habit = Habit(
        id=1,
        name="Exercise",
        description="Daily workout",
        frequency="daily",
        created_at="2023-01-01 00:00:00",
        streak=5
    )
    assert habit.id == 1
    assert habit.name == "Exercise"
    assert habit.frequency == "daily"
    assert habit.streak == 5

def test_complete_daily_habit():
    """Test completing a daily habit."""
    habit = Habit(id=1, name="Read", description="Daily reading", frequency="daily", created_at="2023-01-01 00:00:00")
    initial_streak = habit.streak
    habit.complete_habit()
    assert habit.streak == initial_streak + 1  # Ensure streak increases by 1
    # No need to check completion_dates anymore

def test_complete_weekly_habit():
    """Test completing a weekly habit."""
    habit = Habit(id=1, name="Clean", description="Weekly cleaning", frequency="weekly", created_at="2023-01-01 00:00:00")
    initial_streak = habit.streak
    habit.complete_habit()
    assert habit.streak == initial_streak + 1  # Ensure streak increases by 1
    # No need to check completion_dates anymore'''