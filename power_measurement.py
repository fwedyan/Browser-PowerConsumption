#!/usr/bin/env python3
import subprocess
from pathlib import Path
from utils import log_message

def check_battery_available():
    if Path("/sys/class/power_supply/BAT1/power_now").exists():
        return "/sys/class/power_supply/BAT1/power_now"
    elif Path("/sys/class/power_supply/BAT0/power_now").exists():
        return "/sys/class/power_supply/BAT0/power_now"
    return None

def has_powertop():
    try:
        subprocess.run(["which", "powertop"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def read_power_file(power_file):
    try:
        with open(power_file, 'r') as f:
            power_now = int(f.read().strip())
            return power_now / 1000000.0
    except Exception as e:
        log_message(f"Error reading power: {e}")
        return None