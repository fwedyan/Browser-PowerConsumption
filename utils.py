#!/usr/bin/env python3
import datetime
from pathlib import Path
from config import OUTPUT_DIR, LOG_FILE

def setup_logging():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(LOG_FILE, 'w') as f:
        f.write(f"Browser Power Test - {datetime.datetime.now()}\n")
        f.write("=" * 50 + "\n")
    
    return LOG_FILE

def log_message(message):
    print(message)
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.datetime.now().strftime('%H:%M:%S')} - {message}\n")