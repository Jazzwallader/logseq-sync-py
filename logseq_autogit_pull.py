import os
import time
from git import Repo
import logging
import ctypes
import sys

log_file_path = r"D:\Scripts\Logseq Autosync\logseq_sync_pull.log"

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

def pull_from_remote():
    repo_path = r"D:\Logseq"
    repo = Repo(repo_path)

    while True:
        try:
            origin = repo.remote(name='origin')
            origin.pull()
            logging.info("Pulled latest changes from remote repository")
        except Exception as e:
            logging.error(f"Error during pull operation: {e}")
        
        time.sleep(300)  # Sleep for 5 minutes

if __name__ == "__main__":
    logging.info("Starting Logseq remote pull script")
    pull_from_remote()
