# Habit Tracker App 

Introducing the Habit Tracker App, developed as part of the Object-Oriented and Functional Programming with Python course at IU International University of Applied Sciences.

---

## What is habit tracker application? 
This application is a Command Line Interface (CLI) tool programmed in Python to help users track and maintain habits effectively. It allows users to:
-  Create, complete, and delete habits.
-  Monitor progress and show analytics (longest streak, most missed habit, Average streak).
-  Track daily and weekly habits.
-  View insights such as longest streaks alone without use show analytics.

The interactive CLI menu makes habit tracking simple and accessible.

---

## How to Install It?
1) Clone the Repository
```bash
git clone https://github.com/RaghadIU/Raghad-habit-tracker
```
```bash
cd Raghad-habit-tracker
```
2) Create and activate a virtual environment
```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```
3) Install Python Dependencies 
Make sure you have Python 3.7+ installed. Then, run:
```bash
pip install -r requirements.txt
```
4) To start the app, run:   
```bash
python main.py
```

---

## How to use the application 
 Run the Application
python src/cli.py
Navigate the CLI and select:
- Create a New Habit: Add a habit with a description and frequency (Daily/Weekly).
- Increment Habit: Mark a habit as completed by using its ID for the current period.
- Analyse Habits: View tracking habits, streaks, and performance insights.
- Delete Habit: Remove a habit from tracking.
  
Follow the prompts to enter the habit name and frequency.
1) Add a habit (name, description, frequency)
```bash
python main.py add-habit
```

2) View All Habits
```bash
python main.py list-habits
```
Lists all tracked habits with their details.

3) Mark a Habit as Completed
```bash
python main.py complete-habit --habit_id 1
```
Marks the habit with ID `1` as completed.

4) View Analytics
```bash
python main.py show-analytics
```
Displays the longest streak and most missed habit and average streak.

5) show longest streak
```bash
python main.py longest-streak
```
6) delete habit
```bash
python main.py delete-habit --habit_id 1
```
---

## The features of the application:
- Create and manage habits with descriptions and frequency.   
- Track streaks and analyze progress trends.  
- Interactive CLI for smooth navigation.  
- Filter habits by frequency (Daily/Weekly).
- Advanced analytics to measure habit success.  

---

## Habit Analysis Options
| Feature | Description |
|---------|------------|
| List all habits | Displays all currently tracked habits. |
| Longest streak of all habits | Shows the longest streak achieved overall. |
| Compelet a habit  | complete a habit bt using its ID. |
| most missed habit | by using show analytics |

---

## Example Habits 
When using python src/cli.py, the following test habits are added:
- study (Daily)
- Read (Daily)
- Exercise (Daily)
- Laundry (Weekly)

---

## Running Tests
To validate functionality, automated tests are available:
pytest
For detailed test results:
```bash
python -m pytest tests/ -v
```
## Tests verify:
- test_longest_streak
- test_most_missed_habit 
- test_list_habits 
- test_average_streak 
- test_add_habit
- test_complete_habit 
- test_delete_habit 
---

## Future Enhancements
Graphical User Interface (GUI) using Tkinter or React.  
Mobile App Integration to track habits on the go.  
 Automated Habit Reminders & Notifications.  

---