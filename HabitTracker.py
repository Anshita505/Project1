from datetime import datetime, date, timedelta
import json
import os

class HabitTracker:
    def __init__(self):
        self.habits = {
            'exercise': {'type': 'duration', 'unit': 'minutes', 'daily_goal': 30},
            'water': {'type': 'quantity', 'unit': 'glasses', 'daily_goal': 8},
            'sleep': {'type': 'duration', 'unit': 'hours', 'daily_goal': 8},
            'meditation': {'type': 'duration', 'unit': 'minutes', 'daily_goal': 10},
            'reading': {'type': 'duration', 'unit': 'minutes', 'daily_goal': 20},
            'journaling': {'type': 'boolean', 'unit': None, 'daily_goal': 1}
        }
        self.data_file = 'habit_data.json'
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.habit_data = json.load(f)
        else:
            self.habit_data = {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.habit_data, f)

    def log_habit(self, habit_name, value):
        today = date.today().isoformat()
        if today not in self.habit_data:
            self.habit_data[today] = {}
        self.habit_data[today][habit_name] = value
        self.save_data()

    def get_streak(self, habit_name):
        streak = 0
        today = date.today()
        
        for i in range(len(self.habit_data)):
            check_date = (today - timedelta(days=i)).isoformat()
            if check_date not in self.habit_data or habit_name not in self.habit_data[check_date]:
                break
            if self.habit_data[check_date][habit_name] >= self.habits[habit_name]['daily_goal']:
                streak += 1
            else:
                break
        return streak

    def show_menu(self):
        while True:
            print("\n=== Habit Tracker ===")
            print("1. Log a habit")
            print("2. View today's progress")
            print("3. View streaks")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.log_habit_menu()
            elif choice == '2':
                self.show_today_progress()
            elif choice == '3':
                self.show_streaks()
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def log_habit_menu(self):
        print("\nAvailable habits:")
        for i, habit in enumerate(self.habits.keys(), 1):
            print(f"{i}. {habit}")
        
        try:
            choice = int(input("\nSelect habit number: ")) - 1
            habit_name = list(self.habits.keys())[choice]
            
            if self.habits[habit_name]['type'] == 'boolean':
                value = 1 if input(f"Did you complete {habit_name} today? (y/n): ").lower() == 'y' else 0
            else:
                value = float(input(f"Enter {habit_name} value ({self.habits[habit_name]['unit']}): "))
            
            self.log_habit(habit_name, value)
            print(f"\n{habit_name} logged successfully!")
        except (IndexError, ValueError):
            print("Invalid input. Please try again.")

    def show_today_progress(self):
        today = date.today().isoformat()
        print("\nToday's Progress:")
        print("-" * 40)
        
        if today in self.habit_data:
            for habit, value in self.habit_data[today].items():
                goal = self.habits[habit]['daily_goal']
                unit = self.habits[habit]['unit'] or 'completion'
                status = "✓" if value >= goal else "✗"
                print(f"{habit}: {value} {unit} / {goal} {unit} {status}")
        else:
            print("No habits logged today.")

    def show_streaks(self):
        print("\nCurrent Streaks:")
        print("-" * 40)
        for habit in self.habits:
            streak = self.get_streak(habit)
            print(f"{habit}: {streak} days")

if __name__ == "__main__":
    tracker = HabitTracker()
    tracker.show_menu()
