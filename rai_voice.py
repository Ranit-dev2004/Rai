import datetime
import speech_recognition as sr
import asyncio
import edge_tts
import tempfile
import threading
from playsound import playsound  # ✅ replace pydub playback

ASSISTANT_NAME = "Rai"

# --- Global loop for async TTS ---
loop = asyncio.new_event_loop()

def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_loop, daemon=True).start()

# --- Async TTS with Edge voices ---
async def speak_async(text: str):
    try:
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
        mp3_bytes = b""

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                mp3_bytes += chunk["data"]

        # Save to temp file and play
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(mp3_bytes)
            temp_path = f.name

        playsound(temp_path)  # ✅ much more reliable on Windows

    except Exception as e:
        print(f"Error in speak_async: {e}")

# --- Public speak function ---
def speak(text: str):
    print(f"{ASSISTANT_NAME}: {text}")
    try:
        asyncio.run_coroutine_threadsafe(speak_async(text), loop)
    except Exception as e:
        print(f"Error scheduling speak: {e}")

# --- Greeting based on time ---
def get_greeting() -> str:
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning! I'm ready to help you."
    elif hour < 18:
        return "Good afternoon! How can I assist?"
    else:
        return "Good evening! Ready to serve you."

# --- Voice recognition ---
def recognize_speech_or_manual_input() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please type your command.")
            return input("Type your command: ").strip().lower()
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech service. Please type your command.")
            return input("Type your command: ").strip().lower()
        except Exception as e:
            speak("An error occurred. Please type your command.")
            print(f"Error: {e}")
            return input("Type your command: ").strip().lower()
