Habit Tracker App

Introducing the Habit Tracker App, developed as part of the Object-Oriented and Functional Programming with Python course at IU International University of Applied Sciences.

---

What is habit tracker application?
This application is a Command Line Interface (CLI) tool programmed in Python to help users track and maintain habits effectively. It allows users to:
-  Create, complete, reset, and delete habits.
-  Monitor progress and analyze habit completion.
-  Track daily and weekly habits.
-  View insights such as longest streaks and completion trends.

The interactive CLI menu makes habit tracking simple and accessible.

---

 How to Install It?
1) Clone the Repository
git clone https://github.com/RaghadIU/Raghad-habit-tracker
cd habit-tracker
2) Install Python Dependencies
Make sure you have Python 3.7+ installed. Then, run:
pip install -r requirements.txt
3) Load the Database with Test Data (Optional)
To preload the database with 1 month of test data, run:
python preload_db.py

---

 How to use the application 
 Run the Application
python src/cli.py
Navigate the CLI using arrow keys and select:
- Create a New Habit: Add a habit with a description and frequency (Daily/Weekly).
- Increment Habit: Mark a habit as completed for the current period.
- Reset Habit: Reset the progress of a habit to zero.
- Analyse Habits: View tracking data, streaks, and performance insights.
- Delete Habit: Remove a habit from tracking.
- Exit: Close the application.

Follow the prompts to enter the habit name and frequency.
1) Add a habit 
```bash
python src/cli.py add-habit
```

2) View All Habits
```bash
python src/cli.py list-habits
```
Lists all tracked habits with their details.

3) Mark a Habit as Completed
```bash
python src/cli.py complete-habit --habit_id 1
```
Marks the habit with ID `1` as completed.

4) View Analytics
```bash
python src/cli.py show-analytics
```
Displays the longest streak and most missed habit.

---

The features of the application:
- Create and manage habits with descriptions.  
- Preloaded test data for immediate use.  
- Track streaks and analyze progress trends.  
- Interactive CLI for smooth navigation.  
- Filter habits by frequency (Daily/Weekly).
- Advanced analytics to measure habit success.  

---

 Habit Analysis Options
| Feature | Description |
|---------|------------|
| List all habits | Displays all currently tracked habits. |
| List habits by periodicity | Filters habits as daily or weekly. |
| Longest streak of all habits | Shows the longest streak achieved overall. |
| Longest streak for a habit | Shows the longest streak for a specific habit. |
| Completion Rate Analysis | Calculates habit success percentage. |

---

 Example Habits (Preloaded Data)
When using preload_db.py, the following test habits are added:
- study (Daily)
- Read (Daily)
- Exercise (Daily)
- Laundry (Weekly)

---

 Running Tests
To validate functionality, automated tests are available:
pytest
For detailed test results:
pytest -v
Tests verify:
- Habit creation, completion, and deletion.
- Streak tracking and reset functionality.
- Database operations and analytics calculations.

---

Future Enhancements
Graphical User Interface (GUI) using Tkinter or React.  
Mobile App Integration to track habits on the go.  
 Automated Habit Reminders & Notifications.  

---
 License
This project is licensed under the MIT License.

---

 Contact
For any issues, reach out via GitHub issues or email: your-email@example.com.