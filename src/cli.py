import click
from src.database import Database
from src.analytics import Analytics

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
    db.complete_habit(habit_id)
    click.echo(f"Habit ID {habit_id} marked as completed!")

@cli.command()
def longest_streak():
    """
    Displays the longest streak across all habits.
    """
    longest_streak = analytics.get_longest_streak()
    click.echo(f"Longest Streak: {longest_streak[0]} ({longest_streak[1]} days)")


@cli.command()
def show_analytics():
    """
    Displays analytics about habit tracking.
    """
    longest_streak = analytics.get_longest_streak()
    most_missed = analytics.get_most_missed_habit()
    avg_streak = analytics.average_streak()
    
    click.echo("\nHabit Analytics:")
    click.echo(f"Longest Streak: {longest_streak[0]} ({longest_streak[1]} days)")
    click.echo(f"Most Missed Habit: {most_missed[0]} ({most_missed[1]} completions)")
    click.echo(f"Average Streak: {avg_streak:.2f} days")

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

if __name__ == '__main__':
        cli() 