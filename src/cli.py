import click
from src.database import Database
from src.analytics import Analytics
import json

# Initialize database and analytics
db = Database()
analytics = Analytics()

@click.group()
def cli():
    """
    Command-line interface for the Habit Tracking Application.
    """
    pass

@cli.command()
@click.option('--name', prompt='Habit name', help='The name of the habit')
@click.option('--description', prompt='Habit description', help='A brief description of the habit')
@click.option('--frequency', type=click.Choice(['daily', 'weekly']), prompt='Frequency (daily/weekly)', help='The frequency of the habit')
def add_habit(name, description, frequency):
    """
    Adds a new habit to the database.
    """
    db.add_habit(name, description, frequency)
    click.echo(f"Habit '{name}' added successfully with description '{description}'!")

@cli.command()
def list_habits():
    """
    Lists all habits in the database, including completion history.
    """
    habits = db.get_habits()
    if not habits:
        click.echo("No habits found.")
        return

    click.echo("\nTracked Habits:")
    for habit in habits:
        habit_id = habit[0]
        name = habit[1]
        frequency = habit[2]
        description = habit[3]
        created_at = habit[4]
        streak = habit[5]

        # Get completion dates from habit_logs
        logs = db.get_habit_logs(habit_id)
        completion_dates = [log[2][:10] for log in logs]  # Extract date only (YYYY-MM-DD)

        click.echo(f"ID: {habit_id}, Name: {name}, Frequency: {frequency}, Created At: {created_at}")
        click.echo(f"  → Description: {description}")
        click.echo(f"  → Streak: {streak}, Completed Dates: {completion_dates}")


@cli.command()
@click.option('--habit_id', type=int, prompt='Habit ID', help='ID of the habit to mark as completed')
def complete_habit(habit_id):
    """
    Marks a habit as completed for today.
    """
    db.complete_habit(habit_id)
    click.echo(f"Habit ID {habit_id} marked as completed!")

@cli.command()
def longest_streak():
    """
    Displays the longest streak across all habits.
    """
    longest_streak = analytics.get_longest_streak()
    if longest_streak:
        click.echo(f"Longest Streak: {longest_streak[0]} ({longest_streak[1]} days)")
    else:
        click.echo("No data available for longest streak.")

@cli.command()
def show_analytics():
    """
    Displays analytics about habit tracking.
    """
    longest_streak = analytics.get_longest_streak()
    most_missed = analytics.get_most_missed_habit()
    avg_streak = analytics.average_streak()

    click.echo("\nHabit Analytics:")

    if longest_streak:
        click.echo(f"Longest Streak: {longest_streak[0]} ({longest_streak[1]} days)")
    else:
        click.echo("Longest Streak: No data")

    if most_missed:
        click.echo(f"Most Missed Habit: {most_missed[0]} ({most_missed[1]} missed)")
    else:
        click.echo("Most Missed Habit: No data")

    if avg_streak is not None:
        click.echo(f"Average Streak: {avg_streak:.2f} days")
    else:
        click.echo("Average Streak: No data")

@cli.command()
@click.option('--habit_id', type=int, prompt='Habit ID', help='ID of the habit to delete')
def delete_habit(habit_id):
    """
    Deletes a habit from the database.
    """
    db.delete_habit(habit_id)
    click.echo(f"Habit ID {habit_id} deleted successfully!")

@cli.command()
@click.option('--habit_name', prompt='Habit name', help='Name of the habit to check the streak for')
def streak_for_habit(habit_name):
    """
    Displays the current streak for a given habit.
    """
    streak = analytics.calculate_streak(habit_name)
    click.echo(f"The current streak for {habit_name} is {streak} days.")

# Optional: preload sample data
@cli.command()
def preload_data():
    """
    Loads sample habits into the database for demo/testing.
    """
    sample_habits = [
        ("Drink Water", "Drink 8 glasses of water", "daily"),
        ("Exercise", "30 minutes workout", "daily"),
        ("Read Book", "Read 10 pages", "daily")
    ]
    for name, desc, freq in sample_habits:
        db.add_habit(name, desc, freq)
    click.echo("Sample habits loaded successfully.")

@cli.command()
def preload_4weeks():
    """
    Preloads 4 weeks of habit completion data for testing analytics.
    """
    from datetime import datetime, timedelta

    habits = db.get_habits()
    if not habits:
        click.echo("No habits found to populate. Please add habits first.")
        return

    today = datetime.now()

    for habit in habits:
        habit_id = habit[0]
        
        for days_ago in range(28):
            date = today - timedelta(days=days_ago)
            formatted = date.strftime('%Y-%m-%d %H:%M:%S')

            conn = db._connect()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO habit_logs (habit_id, completed_at) VALUES (?, ?)
            ''', (habit_id, formatted))
            conn.commit()
            conn.close()

    click.echo("Preloaded 4 weeks of completion data for all habits.")


if __name__ == '__main__':
    cli()
