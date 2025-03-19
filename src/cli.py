import click
from database import Database
from analytics import Analytics

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
@click.option('--frequency', type=click.Choice(['daily', 'weekly']), prompt='Frequency (daily/weekly)', help='The frequency of the habit')
def add_habit(name, frequency):
    """
    Adds a new habit to the database.
    """
    db.add_habit(name, frequency)
    click.echo(f"Habit '{name}' added successfully!")

@cli.command()
def list_habits():
    """
    Lists all habits in the database.
    """
    habits = db.get_habits()
    if not habits:
        click.echo("No habits found.")
        return
    
    click.echo("\nTracked Habits:")
    for habit in habits:
        click.echo(f"ID: {habit[0]}, Name: {habit[1]}, Frequency: {habit[2]}, Created At: {habit[3]}")

@cli.command()
@click.option('--habit_id', type=int, prompt='Habit ID', help='ID of the habit to mark as completed')
def complete_habit(habit_id):
    """
    Marks a habit as completed for today.
    """
    db.log_completion(habit_id)
    click.echo(f"Habit ID {habit_id} marked as completed!")

@cli.command()
def show_analytics():
    """
    Displays analytics about habit tracking.
    """
    longest_streak = analytics.get_longest_streak()
    most_missed = analytics.get_most_missed_habit()
    
    click.echo("\nHabit Analytics:")
    click.echo(f"Longest Streak: {longest_streak[0]} ({longest_streak[1]} days)")
    click.echo(f"Most Missed Habit: {most_missed[0]} ({most_missed[1]} completions)")

if __name__ == '__main__':
    cli()

