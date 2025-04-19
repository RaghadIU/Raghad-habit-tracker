import os
import gc
import pytest
import sqlite3
import json
from src.analytics import Analytics
from datetime import datetime, timedelta
from src.database import Database

@pytest.fixture
def test_db_with_data(tmp_path):
    """Fixture with test data for analytics using completion_dates."""
    db_path = tmp_path / "analytics.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create updated habits table with completion_dates
    cursor.execute('''
    CREATE TABLE habits (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        frequency TEXT,
        streak INTEGER,
        completion_dates TEXT,
        created_at TEXT
    )
    ''')

   
    exercise_dates = ["2025-04-15", "2025-04-16", "2025-04-17", "2025-04-18", "2025-04-19"]
    read_dates = ["2025-04-15", "2025-04-17"]

    
    cursor.execute('''
        INSERT INTO habits VALUES
        (1, 'Exercise', 'Daily workout', 'daily', 5, ?, '2025-04-10'),
        (2, 'Read', 'Weekly reading', 'weekly', 2, ?, '2025-04-10')
    ''', (json.dumps(exercise_dates), json.dumps(read_dates)))

    conn.commit()
    conn.close()
    yield str(db_path)

   
    gc.collect()
    os.remove(db_path)

def test_longest_streak(test_db_with_data):
    """Test getting the longest streak."""
    analytics = Analytics(test_db_with_data)
    name, streak = analytics.get_longest_streak()
    assert name == "Exercise"
    assert streak == 5 

def test_most_missed_habit(test_db_with_data):
    """Test identifying most missed habit."""
    analytics = Analytics(test_db_with_data)
    name, missed = analytics.get_most_missed_habit()
    assert name == "Read"
    assert missed == 2  

def test_average_streak(test_db_with_data):
    """Test calculating the average streak."""
    analytics = Analytics(test_db_with_data)
    avg = analytics.average_streak()
    assert avg == 3.5  # (5 + 2) / 2

def test_list_habits():
    """Test creating and listing habits with the real database logic."""
    db = Database("data/test.db")
    db.create_tables()

    with db._connect() as conn:
        conn.execute("DELETE FROM habits")

    db.add_habit("Read", "Read for 30 mins", "daily")
    db.add_habit("Workout", "Gym session", "weekly")

    habits = db.get_habits()

    assert len(habits) == 2
    assert habits[0][1] == "Read"
    assert habits[1][1] == "Workout"
