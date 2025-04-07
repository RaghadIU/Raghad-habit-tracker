import pytest
import sqlite3
import os
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
    os.unlink(db_path)

def test_add_habit(test_db):
    """Test adding a habit to the database."""
    test_db.add_habit("Exercise", "Daily workout", "daily")
    habits = test_db.get_habits()
    assert len(habits) == 1
    assert habits[0][1] == "Exercise"  # name is second column

def test_complete_habit(test_db):
    """Test completing a habit."""
    test_db.add_habit("Read", "Daily reading", "daily")
    test_db.complete_habit(1)
    logs = test_db.get_habit_logs(1)
    assert len(logs) == 1
    assert datetime.now().strftime("%Y-%m-%d") in logs[0][2]  # completed_at is third column

def test_delete_habit(test_db):
    """Test deleting a habit."""
    test_db.add_habit("Temp", "Test habit", "daily")
    test_db.delete_habit(1)
    assert len(test_db.get_habits()) == 0