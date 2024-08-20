# randomscreenshottool
A multi-platform tool that takes a screenshot of your screen, and sends it to a Discord Webhook. (Personal use only)

By using this software, you agree to not use it for malicious reasons. This program was solely made so you could see what you were doing on a specific day.

# IMPORTANT
Use an IDE and edit the file, replace the place where the Webhook URL goes, with your own URL, if you don't know how to make a Discord Webhook, read this article: https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

Python 3 or higher is required, download Python from https://www.python.org/downloads/release/python-3124/

Make sure that pip is updated, ensure this by typing ```pip install --upgrade pip``` into your Command Prompt/Terminal

# Installation
Unzip the program

Open up a Command Prompt or Terminal window

Install the required dependencies

```pip install pyautogui pillow requests flask```

Next, get into the directory of the tool, if it's in your downloads, you'd do ```cd C:\Users\<user>\Downloads```, or ```cd /users/<user>/downloads``` if you're on macOS.

In order to run it, just type ```python screenshot_webhook.py``` or ```python3 screenshot_webhook.py```

Now, every 1-10 minutes, a screenshot of your screen will appear in the channel you made the Webhook with.




# Features

- Configurable Intervals
- Log File Rotation
- Dynamic Interval
- Status Logging

Just open the file using an IDE, and configure the amount of seconds on line 11, and line 12.

Enjoy!




If you have any ways of optimizing, improving, or adding additional features to this script, just add a commit. I have literally no idea how this code works, because it was made entirely with ChatGPT.
