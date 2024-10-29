import os
import time
import logging
from git import Repo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer
import ctypes
import sys


log_file_path = r"D:\Scripts\Logseq Autosync\logseq_realtime_sync.log"

# Function to clear the log file
def clear_log():
    with open(log_file_path, "w") as log_file:
        log_file.write("")

# Clear log at startup
clear_log()

# Hide console window for Python scripts on Windows
if sys.platform == "win32":
    ctypes.windll.kernel32.SetConsoleMode(
        ctypes.windll.kernel32.GetConsoleWindow(), 0
    )

# Configure logging to output to both file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        # logging.StreamHandler()  # This will print to the Python console
    ]
)

class GitSyncHandler(FileSystemEventHandler):
    def __init__(self, repo):
        self.repo = repo
        self.timer = None
        self.buffer_time = 30  # 30-second buffer

    def on_any_event(self, event):
        # Log the detected event
        logging.info(f"File event detected: {event.event_type} on {event.src_path}")

        # Cancel any existing timer and reset it
        if self.timer:
            self.timer.cancel()
        
        # Set up a new timer to delay commit and push
        self.timer = Timer(self.buffer_time, self.commit_and_push)
        self.timer.start()

    def commit_and_push(self):
        try:
            # Set origin at the start
            origin = self.repo.remote(name="origin")
            
            # Check for changes to commit
            if self.repo.is_dirty(untracked_files=True):
                self.repo.git.add(all=True)
                self.repo.index.commit("Auto-sync commit")
                logging.info("Committed changes to repository")

                origin.push()
                logging.info("Pushed changes to remote repository")
            else:
                logging.info("No changes detected, skipping commit")

            # Always pull to keep the repository in sync with remote
            origin.pull()
            logging.info("Pulled latest changes from remote repository")

        except Exception as e:
            logging.error(f"Error during sync operation: {e}")

def start_sync():
    repo_path = r"D:\Logseq"
    repo = Repo(repo_path)

    # Log startup message
    logging.info("Starting Logseq sync script")

    event_handler = GitSyncHandler(repo)
    observer = Observer()
    observer.schedule(event_handler, path=repo_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    # Log script termination
    logging.info("Logseq sync script terminated")

start_sync()
