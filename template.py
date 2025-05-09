import os 
from pathlib import Path 
import logging 

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "source-code-analyzer"

list_of_files = [
   "src/__init__.py",
   "src/helper.py",
   "research/trails.ipynb",
   "static/style.css",
   "template/chat.html",
   "store_index.py",
   "app.py",
   ".env"

]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    # Ensure filedir is not empty
    if filedir.strip():  # Only proceed if filedir is not an empty string
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")
    else:
        logging.warning(f"Skipping creation for empty directory path associated with file: {filename}")

    # Create the file if it doesn't exist or is empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} is already exists")