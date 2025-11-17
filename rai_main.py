import threading  # <-- THE MISSING IMPORT IS NOW ADDED
import time
import random
import datetime
from rai_voice import speak, get_greeting
from rai_listener import passive_listener
from rai_tray import start_tray_icon

MORNING_MESSAGES = [
    "Good morning, sir! You have a full day ahead. Shall I open your work folder to get started?",
    "Rise and shine! Don’t forget your morning meeting — want me to remind you?",
    "Morning, sir! A perfect time to plan your day. Shall I go through your to-do list with you?"
]

AFTERNOON_MESSAGES = [
    "Good afternoon, sir! How’s your progress so far? Shall I help track your tasks?",
    "Feeling a bit tired, sir? I can play some music for a short refreshing break!",
    "Afternoon check, sir — want me to look at your emails for any new messages?"
]

EVENING_MESSAGES = [
    "Good evening, sir! Shall I summarize today’s work for you?",
    "Evening prep, sir — do you want me to organize your schedule for tomorrow?",
    "Sir, would you like me to back up your important files before you wrap up?"
]

NIGHT_MESSAGES = [
    "It’s getting late, sir. Don’t forget to rest! Shall I switch the system to night mode?",
    "Sir, want me to log off unnecessary apps so your system can rest peacefully overnight?",
    "Night check, sir — ready to help you wrap up or prepare for tomorrow?"
]


def dynamic_practical_greeting():
    now = datetime.datetime.now()
    hour = now.hour
    weekday = now.strftime("%A")
    greeting = get_greeting()

    if 5 <= hour < 12:
        message = random.choice(MORNING_MESSAGES)
    elif 12 <= hour < 17:
        message = random.choice(AFTERNOON_MESSAGES)
    elif 17 <= hour < 22:
        message = random.choice(EVENING_MESSAGES)
    else:
        message = random.choice(NIGHT_MESSAGES)
    
    return f"{greeting}, sir. It's {weekday}. {message}"

def main():
    # Speak greeting
    message = dynamic_practical_greeting()
    threading.Thread(target=speak, args=(message,), daemon=True).start()

    # Start background threads
    threading.Thread(target=start_tray_icon, daemon=True).start()
    threading.Thread(target=passive_listener, daemon=True).start()

    # Keep main thread alive efficiently
    try:
        while True:
            time.sleep(1)  # ✅ sleep instead of busy-waiting
    except KeyboardInterrupt:
        print("Exiting Rai...")

if __name__ == "__main__":
    main()