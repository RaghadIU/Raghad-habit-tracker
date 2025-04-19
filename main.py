from src.cli import cli
from src.database import Database
import os

def preload_sample_data_if_empty():
    db = Database()
    db_path = os.path.abspath(db.db_path)
    print(f"\n Database in use: {db_path}\n")

    habits = db.get_habits()
    if not habits:
        sample_habits = [
            ("Drink Water", "Drink 8 glasses of water", "daily"),
            ("Exercise", "30 minutes workout", "daily"),
            ("Read Book", "Read 10 pages", "daily")
        ]
        for name, desc, freq in sample_habits:
            db.add_habit(name, desc, freq)
        print("Sample habits loaded.")

if __name__ == "__main__":
    preload_sample_data_if_empty()
    cli()
