#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import datetime
import shutil
from pathlib import Path

from config import (
    WATCH_DURATION, OUTPUT_DIR, LOG_FILE, SAMPLE_INTERVAL, 
    TEST_URL, VIDEO_SERVER_PORT, NUM_TEST_ITERATIONS
)
from utils import setup_logging, log_message
from power_measurement import check_battery_available, has_powertop, read_power_file
from server import start_local_test_server
from reporting import save_results_to_csv, save_aggregate_results

def get_available_browsers():
    from config import BROWSERS
    
    available_browsers = {}
    for browser_cmd, browser_name in BROWSERS.items():
        try:
            subprocess.run(["which", browser_cmd], check=True, capture_output=True)
            available_browsers[browser_cmd] = browser_name
            log_message(f"Found browser: {browser_name}")
        except subprocess.CalledProcessError:
            log_message(f"Browser not available: {browser_name}")
    
    return available_browsers

def run_browser_test(browser_cmd, browser_name, test_type, url, power_file=None, duration=WATCH_DURATION):
    log_message(f"Starting {test_type} test for {browser_name}...")
    
    if test_type == "video":
        if browser_cmd == "firefox":
            cmd = [browser_cmd, "--kiosk", "--autoplay-policy=no-user-gesture-required", 
                  f"http://localhost:{VIDEO_SERVER_PORT}/video.html"]
        elif browser_cmd in ["google-chrome", "chromium-browser", "brave-browser", "microsoft-edge"]:
            cmd = [browser_cmd, "--autoplay-policy=no-user-gesture-required", "--start-maximized",
                  f"http://localhost:{VIDEO_SERVER_PORT}/video.html"]
        elif browser_cmd in ["opera", "vivaldi"]:
            cmd = [browser_cmd, "--autoplay-policy=no-user-gesture-required", 
                  f"http://localhost:{VIDEO_SERVER_PORT}/video.html"]
        else:
            cmd = [browser_cmd, f"http://localhost:{VIDEO_SERVER_PORT}/video.html"]
    elif test_type == "animation":
        if browser_cmd in ["google-chrome", "chromium-browser", "brave-browser", "microsoft-edge"]:
            cmd = [browser_cmd, "--start-maximized",
                  f"http://localhost:{VIDEO_SERVER_PORT}/animation.html"]
        else:
            cmd = [browser_cmd, f"http://localhost:{VIDEO_SERVER_PORT}/animation.html"]
    elif test_type == "js_computation":
        if browser_cmd in ["google-chrome", "chromium-browser", "brave-browser", "microsoft-edge"]:
            cmd = [browser_cmd, "--start-maximized",
                  f"http://localhost:{VIDEO_SERVER_PORT}/jscomputation.html"]
        else:
            cmd = [browser_cmd, f"http://localhost:{VIDEO_SERVER_PORT}/jscomputation.html"]
    elif test_type == "webpage":
        cmd = [browser_cmd, url]
    elif test_type == "multiple_tabs":
        cmd = [browser_cmd]
    else:
        log_message(f"Unknown test type: {test_type}")
        return None
    
    try:
        browser_process = subprocess.Popen(cmd)
        log_message(f"Started {browser_name} with PID {browser_process.pid}")
        
        time.sleep(5)
        
        if test_type == "video":
            try:
                subprocess.run(["which", "xdotool"], check=True, capture_output=True)
                log_message("Using xdotool to help trigger video autoplay...")
                subprocess.run(["xdotool", "mousemove", "50%", "50%"], capture_output=True)
                subprocess.run(["xdotool", "click", "1"], capture_output=True)
                time.sleep(2)
            except subprocess.CalledProcessError:
                log_message("xdotool not available, relying on JavaScript for autoplay")
                pass
        
        if test_type == "multiple_tabs":
            for _ in range(10):
                subprocess.run([browser_cmd, url])
                time.sleep(1)
        
        start_time = time.time()
        end_time = start_time + duration
        
        power_readings = []
        timestamps = []
        
        if power_file:
            log_message(f"Collecting power data from {power_file} for {duration} seconds...")
            while time.time() < end_time:
                current_time = time.time() - start_time
                power = read_power_file(power_file)
                
                if power is not None:
                    power_readings.append(power)
                    timestamps.append(current_time)
                    log_message(f"Time: {current_time:.1f}s, Power: {power:.2f}W")
                
                time.sleep(SAMPLE_INTERVAL)
        else:
            log_message(f"No direct power readings available. Using powertop...")
            time.sleep(duration)
            
            try:
                powertop_output = subprocess.run(
                    ["sudo", "powertop", "--csv=/tmp/powertop.csv", "--time=5"],
                    capture_output=True,
                    text=True
                )
                
                log_message("Powertop data collected.")
                
                power_readings = [0]
                timestamps = [0]
            except Exception as e:
                log_message(f"Error running powertop: {e}")
        
        log_message(f"Test complete. Terminating {browser_name}...")
        
        browser_process.terminate()
        try:
            browser_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            browser_process.kill()
            browser_process.wait()
        
        if test_type == "multiple_tabs":
            subprocess.run(["killall", browser_cmd], stderr=subprocess.DEVNULL)
        
        log_message(f"{browser_name} terminated.")
        
        if power_readings:
            avg_power = sum(power_readings) / len(power_readings)
            max_power = max(power_readings)
            min_power = min(power_readings)
            total_energy = sum(power_readings) * SAMPLE_INTERVAL / 3600
            
            log_message(f"Average Power: {avg_power:.2f}W")
            log_message(f"Max Power: {max_power:.2f}W")
            log_message(f"Min Power: {min_power:.2f}W")
            log_message(f"Total Energy: {total_energy:.4f}Wh")
            
            return {
                "browser": browser_name,
                "test_type": test_type,
                "timestamps": timestamps,
                "power_readings": power_readings,
                "avg_power": avg_power,
                "max_power": max_power,
                "min_power": min_power,
                "total_energy": total_energy
            }
        else:
            log_message("No power readings collected.")
            return None
    
    except Exception as e:
        log_message(f"Error during test: {e}")
        try:
            browser_process.kill()
        except:
            pass
        subprocess.run(["killall", browser_cmd], stderr=subprocess.DEVNULL)
        return None