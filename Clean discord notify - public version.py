import os
import time
import re
import shutil
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import apprise
import signal
import sys

# Folder to watch
FOLDER_TO_WATCH = r"ENTER FOLDER TO WATCH HERE"

# Discord webhook URL
DISCORD_WEBHOOK = "ENTER DISCORD CHANNEL WEBHOOK HERE"

# Supported video file extensions
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov"]


class FolderWatcher(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            file_extension = os.path.splitext(file_name)[1].lower()
            if file_extension in VIDEO_EXTENSIONS:
                cleaned_file_name = clean_file_name(file_name)
                send_discord_notification(cleaned_file_name)

def clean_file_name(file_name):
    # Replace periods with spaces
    cleaned_name = file_name.replace(".", " ").replace("-", " ")

    # Replace the brackets with spaces
    cleaned_name = re.sub(r"\(|\)", " ", cleaned_name).strip()

    # Remove everything from the first 4 digit number to the end
    cleaned_name = re.sub(r"\s\d{4}.*", "", cleaned_name).strip()

    return cleaned_name

def send_discord_notification(file_name):
    apprise_obj = apprise.Apprise()
    apprise_obj.add(DISCORD_WEBHOOK)
    apprise_obj.notify(
        body=f"**{file_name}** added"
    )
    print(f"\033[95mPosted to Discord\033[0m")

def signal_handler(signal, frame):
    print("Stopping the script...")
    observer.stop()
    observer.join()
    move_files_thread.join()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    event_handler = FolderWatcher()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_WATCH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)  # Check the folder every 5 seconds
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)