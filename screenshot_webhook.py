import os
import time
import random
import requests
import logging
from datetime import datetime
from PIL import ImageGrab, Image, ImageDraw, ImageFont
from logging.handlers import RotatingFileHandler
import tkinter as tk
from tkinter import messagebox, ttk
import pystray
from pystray import MenuItem as item
from threading import Thread
from PIL import Image as PILImage

# Configuration
WEBHOOK_URL = 'WEBHOOK_URL_HERE'  # Replace with your Discord webhook URL
DELETE_AFTER_SEND = True  # Whether to delete the screenshot file after sending

# Configure logging with rotation
log_handler = RotatingFileHandler('screenshot_tool.log', maxBytes=5e6, backupCount=5)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(log_handler)
logging.getLogger().setLevel(logging.INFO)

ICON_PATH = "icon.png"

class ScreenshotTool:
    def __init__(self):
        self.min_interval = 60
        self.max_interval = 600
        self.add_timestamp = False
        self.is_running = True
        self.icon = None

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Screenshot Tool")

        # Interval setting
        tk.Label(self.root, text="Min Interval (seconds):").grid(row=0, column=0, padx=10, pady=5)
        self.min_interval_entry = tk.Entry(self.root)
        self.min_interval_entry.grid(row=0, column=1)
        self.min_interval_entry.insert(0, str(self.min_interval))

        tk.Label(self.root, text="Max Interval (seconds):").grid(row=1, column=0, padx=10, pady=5)
        self.max_interval_entry = tk.Entry(self.root)
        self.max_interval_entry.grid(row=1, column=1)
        self.max_interval_entry.insert(0, str(self.max_interval))

        # Timestamp toggle
        self.timestamp_var = tk.BooleanVar()
        self.timestamp_check = tk.Checkbutton(self.root, text="Add Timestamp", variable=self.timestamp_var)
        self.timestamp_check.grid(row=2, columnspan=2, pady=5)

        # Apply and Quit buttons
        self.apply_button = tk.Button(self.root, text="Apply", command=self.apply_settings)
        self.apply_button.grid(row=3, column=0, pady=10)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit)
        self.quit_button.grid(row=3, column=1, pady=10)

        # Start the screenshot process in a separate thread
        self.thread = Thread(target=self.main_loop)
        self.thread.daemon = True
        self.thread.start()

        # Create the icon
        self.create_icon()

        # Minimize to tray
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.create_tray_icon()

    def create_icon(self):
        """Create a simple icon with a line."""
        image = PILImage.new('RGB', (64, 64), color=(73, 109, 137))
        draw = ImageDraw.Draw(image)
        draw.line((0, 32, 64, 32), fill="white", width=5)
        image.save(ICON_PATH)

    def create_tray_icon(self):
        image = PILImage.open(ICON_PATH)
        menu = (item('Open', self.show_window), item('Quit', self.quit))
        self.icon = pystray.Icon("Screenshot Tool", image, "Screenshot Tool", menu)

    def minimize_to_tray(self):
        self.root.withdraw()
        if not self.icon.visible:
            Thread(target=self.icon.run).start()

    def show_window(self, icon=None, item=None):
        if self.icon:
            self.icon.stop()
        self.root.deiconify()

    def apply_settings(self):
        self.min_interval = int(self.min_interval_entry.get())
        self.max_interval = int(self.max_interval_entry.get())
        self.add_timestamp = self.timestamp_var.get()
        messagebox.showinfo("Settings", "Settings applied successfully!")

    def quit(self, icon=None, item=None):
        self.is_running = False
        self.root.quit()
        if self.icon:
            self.icon.stop()

    def take_screenshot(self):
        screenshot = ImageGrab.grab()
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        if self.add_timestamp:
            draw = ImageDraw.Draw(screenshot)
            font = ImageFont.load_default()
            text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            draw.text((10, 10), text, font=font, fill="white")
        screenshot.save(filename)
        logging.info(f"Screenshot taken and saved as {filename}")
        return filename

    def send_to_discord(self, filename):
        with open(filename, 'rb') as file:
            response = requests.post(WEBHOOK_URL, files={'file': file})
        if response.status_code == 200:
            logging.info(f"Successfully sent {filename} to Discord")
        else:
            logging.error(f"Failed to send {filename} to Discord: {response.status_code} - {response.text}")
        logging.info(f"Screenshot {filename} processed.")
        if DELETE_AFTER_SEND:
            os.remove(filename)
            logging.info(f"Deleted screenshot file {filename}")

    def get_dynamic_interval(self):
        return random.randint(self.min_interval, self.max_interval)

    def main_loop(self):
        while self.is_running:
            try:
                filename = self.take_screenshot()
                self.send_to_discord(filename)
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            sleep_time = self.get_dynamic_interval()
            logging.info(f"Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ScreenshotTool()
    app.run()
