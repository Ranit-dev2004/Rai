import speech_recognition as sr
import logging
from rai_voice import speak
from rai_commands import process_command

def passive_listener():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)
                command = recognizer.recognize_google(audio).lower()
                print(f"Passive heard: {command}")

                if command:
                    process_command(command)

            except sr.UnknownValueError:
                continue  
            except Exception as e:
                logging.error(f"Passive listener error: {e}")
