import os
import webbrowser
from rai_voice import speak, recognize_speech_or_manual_input

def find_installed_apps():
    start_menu_paths = [
        os.environ["PROGRAMDATA"] + r"\Microsoft\Windows\Start Menu\Programs",
        os.environ["APPDATA"] + r"\Microsoft\Windows\Start Menu\Programs"
    ]
    
    apps = []
    for path in start_menu_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".lnk"):
                    app_name = os.path.splitext(file)[0]
                    app_path = os.path.join(root, file)
                    apps.append( (app_name.lower(), app_path) )
    
    return apps
def open_software(app_name):
    installed_apps = find_installed_apps()
    found = False
    
    for app_name_lower, app_path in installed_apps:
        if app_name.lower() in app_name_lower:
            speak(f"Launching {app_name_lower}...")
            os.startfile(app_path)
            found = True
            break
    
    if not found:
        speak(f"I can't find {app_name}. Do you want me to download it?")
        answer = recognize_speech_or_manual_input()
        if "yes" in answer.lower():
            speak(f"Opening download page for {app_name}.")
            webbrowser.open(f"https://www.google.com/search?q=download+{app_name}")
        else:
            speak("Okay, skipping download.")

def process_user_command(user_command):
    user_command = user_command.lower()
    
    if "file manager" in user_command or "explorer" in user_command or "my files" in user_command:
        speak("Opening File Manager...")
        os.system("explorer")
    
    elif "work folder" in user_command:
        work_folder = r"C:\Users\Niladri\Documents\Work"
        speak("Opening Work Folder...")
        os.startfile(work_folder)
    
    else:
        open_software(user_command)
