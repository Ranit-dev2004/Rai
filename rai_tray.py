import pystray
from PIL import Image, ImageDraw
from rai_voice import speak
import os

def create_image():
    image = Image.new('RGB', (64, 64), color=(73, 109, 137))
    d = ImageDraw.Draw(image)
    d.text((10, 25), "RAI", fill=(255, 255, 0))
    return image

def on_quit(icon, item):
    speak("Shutting down. Goodbye!")
    icon.stop()
    os._exit(0)

def start_tray_icon():
    icon = pystray.Icon("RAI", create_image(), "RAI - Personal AI", menu=pystray.Menu(
        pystray.MenuItem("Quit", on_quit)
    ))
    icon.run()