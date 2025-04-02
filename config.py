#!/usr/bin/env python3
import datetime
from pathlib import Path

WATCH_DURATION = 60
OUTPUT_DIR = Path.home() / "Desktop/Projects/browser_power_tests"
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = OUTPUT_DIR / f"power_test_{TIMESTAMP}.log"
SAMPLE_INTERVAL = 1
TEST_URL = "https://www.lewisu.edu/"
VIDEO_SERVER_PORT = 8000
AUTOPLAY_RETRY_COUNT = 3
NUM_TEST_ITERATIONS = 5

VIDEO_DIR = Path("/home/anthony/Desktop/Projects/Videos")
VIDEO_FILES = {
    "webm": VIDEO_DIR / "test_VP9.webm",
}

BROWSERS = {
    "firefox": "Firefox",
    "google-chrome": "Chrome",
    "chromium-browser": "Chromium",
    "brave-browser": "Brave", 
    "opera": "Opera",
    "vivaldi": "Vivaldi",
    "microsoft-edge": "Edge"
}

ANALYSIS_OUTPUT_DIR = Path.home() / "Desktop/Projects/output"

TEST_TYPES = ["video", "animation", "js_computation", "webpage", "multiple_tabs"]

BROWSER_COLORS = {
    "firefox": "#FF6F61",
    "chrome": "#5B84B1",
    "chromium": "#42BFDD",
    "brave": "#FC766A",
    "edge": "#5F4B8B",
    "opera": "#E69A8D",
    "vivaldi": "#F7CAC9"
}