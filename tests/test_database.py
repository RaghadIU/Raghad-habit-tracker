import pytest
import sqlite3
import os
import json
from src.database import Database
from datetime import datetime

@pytest.fixture
def test_db(tmp_path):
    """Fixture to create a test database."""
    db_path = tmp_path / "test.db"
    db = Database(db_path)
    db.create_tables()
    yield db
    db._connect().close()
    os.remove(db_path)

def test_add_habit(test_db):
    """Test adding a habit to the database."""
    test_db.add_habit("Exercise", "Daily workout", "daily")
    habits = test_db.get_habits()
    assert len(habits) == 1
    assert habits[0][1] == "Exercise"  # name is at index 1

def test_complete_habit(test_db):
    """Test completing a habit."""
    test_db.add_habit("Read", "Daily reading", "daily")
    test_db.complete_habit(1)

    habits = test_db.get_habits()
    # Get the habit with ID = 1
    for habit in habits:
        if habit[0] == 1:
            completion_dates = json.loads(habit[6]) if habit[6] else []
            break

    today = datetime.now().strftime("%Y-%m-%d")
    assert today in completion_dates
    assert len(completion_dates) == 1

def test_delete_habit(test_db):
    """Test deleting a habit."""
    test_db.add_habit("Temp", "Test habit", "daily")
    test_db.delete_habit(1)
    habits = test_db.get_habits()
    assert len(habits) == 0
