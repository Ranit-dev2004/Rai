from rai_voice import speak, recognize_speech_or_manual_input
from rai_llm import send_to_llm
from rai_apps import open_software
import pywhatkit
import wikipedia
import datetime
import os
import random
import platform

# Global flag to control active / standby state
rai_active = True

def process_command(command):
    global rai_active
    command = command.lower()

    # Wake up commands
    if ("hey rai" in command or "oy rai" in command or "oi rai" in command 
        or "oa rai" in command or "orai " in command) and (
        "need you" in command or "come back" in command or "wake up" in command):
        rai_active = True
        speak("At your command, sir! Back online and ready for action!")

    # Standby commands
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
            speak(f"Right away, sir! The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
        elif "date" in command:
            speak(f"As you wish, sir. Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}")
        elif "play" in command:
            query = command.replace("play", "").strip()
            pywhatkit.playonyt(query)
            speak(f"Playing {query} for you, sir. Enjoy!")
        elif "search" in command or "tell me about" in command:
            query = command.replace("search", "").replace("tell me about", "").strip()
            try:
                summary = wikipedia.summary(query, sentences=2)
                speak(f"Here’s what I found, sir: {summary}")
            except:
                speak("Oops, sir! I couldn't find information about that. Shall I try again?")
        elif "joke" in command:
            tell_joke()
        elif "fact" in command:
            tell_fact()
        elif "system info" in command:
            system_info()
        elif "write code" in command or "generate code" in command:
            speak("As you wish, sir! Generating code now...")
            send_to_llm("Write code for: " + command)
        elif "i feel" in command or "my mood" in command:
            speak("I’m all ears, sir! Let me give you some friendly suggestions...")
            send_to_llm("Friendly suggestion: " + command)
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            speak(f"Opening {app_name} immediately, sir!")
            open_software(app_name)
        elif "how are you" in command:
            speak(random.choice([
                "At your service and feeling fantastic, sir!",
                "Always ready to serve, sir! No complaints here.",
                "I’m humming along smoothly, sir. How can I assist you today?"
            ]))
        elif "what can you do" in command:
            speak("Sir, I can tell time, play music, search the web, tell jokes, give facts, show system info, open apps, generate code, or just make your day easier. All for you!")
        elif "who are you" in command:
            speak("I am Rai, your devoted AI companion. I obey your commands and make your life easier, sir.")
        elif "exit" in command or "quit" in command:
            speak("Understood, sir. Shutting down… until you summon me again!")
            os._exit(0)
        else:
            speak("Consider it done, sir!")
            send_to_llm(command)

    else:
        print("Rai in standby mode — ignoring command.")

def tell_joke():
    speak(random.choice([
        "Why did the AI cross the road, sir? To serve you on the other side!",
        "Why don’t scientists trust atoms, sir? Because they make up everything — unlike me, I only serve truthfully!",
        "Why did the computer go to sleep? It was waiting for your next command, sir!"
    ]))

def tell_fact():
    speak(random.choice([
        "Sir, did you know honey never spoils? Just like my loyalty to you!",
        "Bananas are berries, sir, but strawberries are not. Interesting, isn’t it?",
        "Octopuses have three hearts, sir. I have one for you… metaphorically!"
    ]))

def system_info():
    info = f"Running on {platform.system()} {platform.release()}, Node: {platform.node()}, Arch: {platform.machine()}. All systems nominal, sir!"
    speak(info)
