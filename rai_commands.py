import os
import random
import datetime
import platform
import json
import pywhatkit
import wikipedia
from rai_voice import speak, recognize_speech_or_manual_input
from rai_llm import send_to_llm
from rai_apps import open_software

CONFIG_FILE = 'rai_config.json'

def load_config():
    """Loads the configuration file, or returns an empty dict if it doesn't exist."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} 
    return {}

def save_config(config):
    """Saves the configuration dictionary to the JSON file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
rai_active = True

def process_command(command):
    global rai_active
    command = command.lower()

    if ("hey rai" in command or "oy rai" in command or "oi rai" in command 
        or "oa rai" in command or "orai " in command) and (
        "need you" in command or "come back" in command or "wake up" in command):
        rai_active = True
        speak("At your command, sir! Back online and ready for action!")

    elif "stop for now" in command or "standby" in command or "quiet now" in command or "no need of you right now" in command:
        rai_active = False
        standby_responses = [
        "Alright, sir. I’ll stay on standby, ready to spring into action when called.",
        "Got it, sir! I’ll be resting my circuits until you summon me.",
        "As you wish, sir. I’ll wait patiently until you call for me.",
        "Very well, sir. Silent mode activated — but always alert for your next command!"
    ]
        speak(random.choice(standby_responses))

    elif rai_active:
        
        if "time" in command:
            speak(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}, sir.")
        
        elif "date" in command:
            speak(f"Certainly, sir. Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}.")
        
        elif "play" in command:
            query = command.replace("play", "").strip()
            speak(f"Excellent choice, sir. Cueing up {query} on YouTube now.")
            pywhatkit.playonyt(query)
        
        elif "search" in command or "tell me about" in command:
            query = command.replace("search", "").replace("tell me about", "").strip()
            speak(f"One moment, sir. Looking up '{query}' for you...")
            try:
                summary = wikipedia.summary(query, sentences=2)
                speak(f"I've found a summary, sir: {summary}")
            except Exception as e:
                speak(f"My apologies, sir. I'm having trouble finding a clear summary for '{query}'. Perhaps we could try a different search term?")
        
        elif "joke" in command:
            tell_joke()
        
        elif "fact" in command:
            tell_fact()
        
        elif "system info" in command:
            system_info()

        elif "file manager" in command or "explorer" in command or "my files" in command:
            speak("Opening File Manager, sir.")
            os.system("explorer")

        elif "work folder" in command:
            config = load_config()
            work_folder_path = config.get('work_folder')

            if work_folder_path and os.path.exists(work_folder_path):
                speak("Opening your work folder, sir.")
                os.startfile(work_folder_path)
            else:
                speak("I don't have your work folder path set. Please use your keyboard to type the full path, and I'll save it for you.")
                new_path = recognize_speech_or_manual_input()
                
                if new_path and os.path.exists(new_path):
                    config['work_folder'] = new_path
                    save_config(config)
                    speak(f"Excellent. I have saved {new_path} as your work folder. I will remember this for next time.")
                else:
                    speak("My apologies, that path doesn't seem to exist or was invalid. Let's try again later.")
        
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            speak(f"Understood, sir. Launching {app_name}.")
            open_software(app_name)
        
        elif "exit" in command or "quit" in command:
            speak("Understood, sir. Shutting down… until you summon me again!")
            os._exit(0)
        
        elif "how are you" in command:
            speak(random.choice([
                "At your service and feeling fantastic, sir!",
                "Always ready to serve, sir! All circuits are nominal.",
                "I’m humming along smoothly, sir. How can I assist you today?"
            ]))
        
        elif "what can you do" in command:
            speak("Sir, I can manage your tasks, play media, find information, and control your system. Think of me as your personal command center.")
        
        elif "who are you" in command:
            speak("I am Rai, your devoted AI companion, designed to make your workflow more efficient.")
        
        elif "write code" in command or "generate code" in command:
            speak("As you wish, sir! Let me draft that code for you...")
            send_to_llm("Write Python code for: " + command)
            
        elif "i feel" in command or "my mood" in command:
            speak("I’m all ears, sir. Please tell me what's on your mind.")
            send_to_llm("User said: " + command + ". Respond with a friendly, supportive suggestion.")
            
        else:
            speak(f"That's an interesting request, sir. Processing it now...")
            send_to_llm(command)

    else:
        print("Rai in standby mode — ignoring command.")

def tell_joke():
    speak(random.choice([
        "Sir, why don't scientists trust atoms? Because they make up everything.",
        "I told my computer I needed a break, sir... and now it won’t stop sending me vacation ads.",
        "What do you call a fish with no eyes, sir? A fsh.",
        "Why don't skeletons fight each other? They just don't have the guts, sir."
    ]))

def tell_fact():
    speak(random.choice([
        "Sir, did you know the Eiffel Tower can be 15 cm taller during the summer due to thermal expansion?",
        "A single day on Venus is longer than an entire year on Venus. It rotates very slowly, sir.",
        "Did you know, sir, that a group of flamingos is called a 'flamboyance'?",
        "Honey never spoils, sir. Archaeologists have found pots of honey in ancient Egyptian tombs that are still perfectly edible."
    ]))

def system_info():
    info = f"All systems are online, sir. I'm running on a {platform.system()} {platform.machine()} architecture. Let me know if you need a deeper diagnostic."
    speak(info)