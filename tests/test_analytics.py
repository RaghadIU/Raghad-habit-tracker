import os  
import pytest
import sqlite3
from src.analytics import Analytics
from datetime import datetime, timedelta
from src.database import Database

@pytest.fixture
def test_db_with_data(tmp_path):
    """Fixture with test data for analytics."""
    db_path = tmp_path / "analytics.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE habits (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        frequency TEXT,
        streak INTEGER,
        complete_habit TEXT,
        created_at TEXT
    )''')
    
    cursor.execute('''
    CREATE TABLE habit_logs (
        id INTEGER PRIMARY KEY,
        habit_id INTEGER,
        completed_at TEXT
    )''')
    

    cursor.execute('''
    INSERT INTO habits VALUES 
        (1, 'Exercise', 'Daily workout', 'daily', 5, '[]', '2023-01-01'),
        (2, 'Read', 'Weekly reading', 'weekly', 2, '[]', '2023-01-01')
    ''')
    
    
    dates = [
        (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
        for i in range(5)
    ]
    for date in dates:
        cursor.execute('INSERT INTO habit_logs (habit_id, completed_at) VALUES (1, ?)', (date,))
    
    conn.commit()
    conn.close()
    
    yield db_path
    os.unlink(db_path)

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
    assert missed == 0

def test_list_habits():
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

def test_average_streak(test_db_with_data):
    """Test calculating the average streak."""
    analytics = Analytics(test_db_with_data)
    
    # Update streaks for testing
    conn = sqlite3.connect(test_db_with_data)
    cursor = conn.cursor()
    cursor.execute("UPDATE habits SET streak = 5 WHERE name = 'Read'")
    cursor.execute("UPDATE habits SET streak = 3 WHERE name = 'Exercise'")
    conn.commit()
    conn.close()

    # Get average streak using Analytics
    avg = analytics.average_streak()
    assert avg == 4  # (5 + 3) / 2
