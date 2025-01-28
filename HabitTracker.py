from datetime import datetime, date, timedelta
import json
import os
import random

class HabitTracker:
    def __init__(self):
        self.habits = {
            'exercise': {'type': 'duration', 'unit': 'minutes', 'daily_goal': 30, 'emoji': '💪'},
            'water': {'type': 'quantity', 'unit': 'glasses', 'daily_goal': 8, 'emoji': '💧'},
            'sleep': {'type': 'duration', 'unit': 'hours', 'daily_goal': 8, 'emoji': '😴'},
            'meditation': {'type': 'duration', 'unit': 'minutes', 'daily_goal': 10, 'emoji': '🧘'},
            'reading': {'type': 'duration', 'unit': 'minutes', 'daily_goal': 20, 'emoji': '📚'},
            'journaling': {'type': 'boolean', 'unit': None, 'daily_goal': 1, 'emoji': '✍️'}
        }
        self.data_file = 'habit_data.json'
        self.load_data()
        
        # Motivational messages
        self.milestone_messages = [
            "Amazing work! You're building a better you! 🌟",
            "Look at you go! Your future self thanks you! ⭐",
            "You're on fire! Keep that momentum going! 🔥",
            "Incredible dedication! You're making it happen! 💫",
            "You're crushing it! Every day counts! 💪"
        ]
        
        self.completion_messages = [
            "Great job! One step closer to your goals! ✨",
            "Well done! You're making progress! 🎯",
            "Keep it up! Small steps lead to big changes! 🌱",
            "Awesome work! You're building great habits! 🚀",
            "Excellence is a habit, and you're proving it! 🌟"
        ]

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.habit_data = json.load(f)
        else:
            self.habit_data = {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.habit_data, f)

    def get_motivation_message(self, streak, is_completion=True):
        if is_completion:
            message = random.choice(self.completion_messages)
        elif streak in [7, 14, 21, 30, 60, 90]:  # Milestone streaks
            message = f"\n🎉 {streak} DAY STREAK! 🎉\n{random.choice(self.milestone_messages)}"
        else:
            message = ""
        return message

    def log_habit(self, habit_name, value):
        today = date.today().isoformat()
        if today not in self.habit_data:
            self.habit_data[today] = {}
        self.habit_data[today][habit_name] = value
        self.save_data()
        
        # Get streak and show motivation
        streak = self.get_streak(habit_name)
        if value >= self.habits[habit_name]['daily_goal']:
            print(self.get_motivation_message(streak, is_completion=True))
            if streak in [7, 14, 21, 30, 60, 90]:
                print(self.get_motivation_message(streak, is_completion=False))

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

    def get_progress_bar(self, value, goal, width=20):
        filled = int(width * (value / goal))
        bar = '█' * filled + '░' * (width - filled)
        percentage = (value / goal) * 100
        return f"[{bar}] {percentage:.1f}%"

    def show_menu(self):
        while True:
            print("\n🌟 === Habit Tracker === 🌟")
            print("1. 📝 Log a habit")
            print("2. 📊 View today's progress")
            print("3. 🔥 View streaks")
            print("4. 👋 Exit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.log_habit_menu()
            elif choice == '2':
                self.show_today_progress()
            elif choice == '3':
                self.show_streaks()
            elif choice == '4':
                print("Keep up the great work! See you tomorrow! 👋")
                break
            else:
                print("Invalid choice. Please try again.")

    def log_habit_menu(self):
        print("\n📝 Available habits:")
        for i, (habit, details) in enumerate(self.habits.items(), 1):
            print(f"{i}. {details['emoji']} {habit}")
        
        try:
            choice = int(input("\nSelect habit number: ")) - 1
            habit_name = list(self.habits.keys())[choice]
            
            if self.habits[habit_name]['type'] == 'boolean':
                value = 1 if input(f"Did you complete {habit_name} today? (y/n): ").lower() == 'y' else 0
            else:
                value = float(input(f"Enter {habit_name} value ({self.habits[habit_name]['unit']}): "))
            
            self.log_habit(habit_name, value)
            print(f"\n{self.habits[habit_name]['emoji']} {habit_name} logged successfully!")
        except (IndexError, ValueError):
            print("Invalid input. Please try again.")

    def show_today_progress(self):
        today = date.today().isoformat()
        print("\n📊 Today's Progress:")
        print("-" * 50)
        
        if today in self.habit_data:
            for habit, value in self.habit_data[today].items():
                goal = self.habits[habit]['daily_goal']
                unit = self.habits[habit]['unit'] or 'completion'
                emoji = self.habits[habit]['emoji']
                status = "✅" if value >= goal else "❌"
                
                progress_bar = self.get_progress_bar(value, goal)
                print(f"{emoji} {habit}: {value} {unit} / {goal} {unit} {status}")
                print(f"   {progress_bar}")
        else:
            print("No habits logged today. Start fresh! 🌱")

    def show_streaks(self):
        print("\n🔥 Current Streaks:")
        print("-" * 50)
        for habit in self.habits:
            streak = self.get_streak(habit)
            emoji = self.habits[habit]['emoji']
            fire_level = "🔥" * min(5, (streak // 7) + 1)  # More fire emojis for longer streaks
            print(f"{emoji} {habit}: {streak} days {fire_level}")

if __name__ == "__main__":
    tracker = HabitTracker()
    tracker.show_menu()
