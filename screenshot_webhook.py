import os
import time
import random
import requests
import logging
from datetime import datetime
from PIL import ImageGrab  # For macOS, use the 'Pillow' package for screen capture

# Configuration
WEBHOOK_URL = 'your_discord_webhook_url'  # Replace with your Discord webhook URL
MIN_INTERVAL = 60  # Minimum interval in seconds
MAX_INTERVAL = 600  # Maximum interval in seconds
DELETE_AFTER_SEND = True  # Whether to delete the screenshot file after sending

logging.basicConfig(level=logging.INFO)

def take_screenshot():
    screenshot = ImageGrab.grab()
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot.save(filename)
    return filename

def send_to_discord(filename):
    with open(filename, 'rb') as file:
        response = requests.post(WEBHOOK_URL, files={'file': file})
    if response.status_code == 200:
        logging.info(f"Successfully sent {filename} to Discord")
    else:
        logging.error(f"Failed to send {filename} to Discord: {response.status_code} - {response.text}")

def main():
    while True:
        try:
            filename = take_screenshot()
            send_to_discord(filename)
            if DELETE_AFTER_SEND:
                os.remove(filename)  # Optionally remove the screenshot file after sending
                logging.info(f"Deleted screenshot file {filename}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        sleep_time = random.randint(MIN_INTERVAL, MAX_INTERVAL)
        logging.info(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()