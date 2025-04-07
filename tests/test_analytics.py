import os  
import pytest
import sqlite3
from src.analytics import Analytics
from datetime import datetime, timedelta

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
    
    # Insert test data
    cursor.execute('''
    INSERT INTO habits VALUES 
        (1, 'Exercise', 'Daily workout', 'daily', 5, '[]', '2023-01-01'),
        (2, 'Read', 'Weekly reading', 'weekly', 2, '[]', '2023-01-01')
    ''')
    
    # Add completion logs
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

def test_calculate_streak(test_db_with_data):
    """Test streak calculation."""
    analytics = Analytics(test_db_with_data)
    streak = analytics.calculate_streak("Exercise")
    assert streak == 5