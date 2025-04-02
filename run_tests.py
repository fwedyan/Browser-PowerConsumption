#!/usr/bin/env python3
import time
import datetime
import shutil
from pathlib import Path

from config import (
    OUTPUT_DIR, LOG_FILE, NUM_TEST_ITERATIONS, TEST_URL
)
from utils import setup_logging, log_message
from power_measurement import check_battery_available, has_powertop
from server import start_local_test_server
from browser_test import get_available_browsers, run_browser_test
from reporting import save_results_to_csv, save_aggregate_results

def run_all_tests():
    log_file = setup_logging()
    log_message("Starting browser power efficiency tests")
    log_message(f"Number of test iterations: {NUM_TEST_ITERATIONS}")
    
    power_file = check_battery_available()
    if power_file:
        log_message(f"Using power measurements from: {power_file}")
    elif has_powertop():
        log_message("No direct power readings available. Will use powertop.")
    else:
        log_message("ERROR: No method available to measure power. Please install powertop or run on a laptop with battery.")
        return
    
    available_browsers = get_available_browsers()
    if not available_browsers:
        log_message("No browsers available for testing!")
        return
    
    httpd = None
    temp_dir = None
    
    try:
        httpd, temp_dir = start_local_test_server()
        log_message("Local test server started")
        
        all_iterations = {
            "video": [],
            "animation": [],
            "js_computation": [],
            "webpage": [],
            "multiple_tabs": []
        }
        
        for iteration in range(1, NUM_TEST_ITERATIONS + 1):
            log_message(f"\n{'='*20} Starting test iteration {iteration}/{NUM_TEST_ITERATIONS} {'='*20}")
            
            iteration_results = {
                "video": [],
                "animation": [],
                "js_computation": [],
                "webpage": [],
                "multiple_tabs": []
            }
            
            for browser_cmd, browser_name in available_browsers.items():
                log_message(f"\n{'='*20} Testing {browser_name} {'='*20}")
                
                if httpd:
                    video_result = run_browser_test(
                        browser_cmd, 
                        browser_name, 
                        "video", 
                        "", 
                        power_file
                    )
                    iteration_results["video"].append(video_result)
                    
                    if video_result:
                        save_results_to_csv([video_result], f"video_{browser_name.lower()}", iteration)
                    
                    time.sleep(5)
                    
                    animation_result = run_browser_test(
                        browser_cmd, 
                        browser_name, 
                        "animation", 
                        "", 
                        power_file
                    )
                    iteration_results["animation"].append(animation_result)
                    
                    if animation_result:
                        save_results_to_csv([animation_result], f"animation_{browser_name.lower()}", iteration)
                    
                    time.sleep(5)
                    
                    js_result = run_browser_test(
                        browser_cmd, 
                        browser_name, 
                        "js_computation", 
                        "", 
                        power_file
                    )
                    iteration_results["js_computation"].append(js_result)
                    
                    if js_result:
                        save_results_to_csv([js_result], f"js_computation_{browser_name.lower()}", iteration)
                    
                    time.sleep(5)
                
                webpage_result = run_browser_test(
                    browser_cmd, 
                    browser_name, 
                    "webpage", 
                    TEST_URL, 
                    power_file
                )
                iteration_results["webpage"].append(webpage_result)
                
                if webpage_result:
                    save_results_to_csv([webpage_result], f"webpage_{browser_name.lower()}", iteration)
                
                time.sleep(5)
                
                multiple_tabs_result = run_browser_test(
                    browser_cmd, 
                    browser_name, 
                    "multiple_tabs", 
                    TEST_URL, 
                    power_file
                )
                iteration_results["multiple_tabs"].append(multiple_tabs_result)
                
                if multiple_tabs_result:
                    save_results_to_csv([multiple_tabs_result], f"multiple_tabs_{browser_name.lower()}", iteration)
                
                time.sleep(5)
            
            for test_type, results in iteration_results.items():
                if results and any(results):
                    save_results_to_csv(results, test_type, iteration)
                    all_iterations[test_type].append(results)
        
        aggregate_files = []
        if NUM_TEST_ITERATIONS > 1:
            log_message("\nCalculating aggregate results across all iterations...")
            for test_type, iterations in all_iterations.items():
                if iterations:
                    aggregate_file = save_aggregate_results(iterations, test_type)
                    aggregate_files.append(aggregate_file)
        
        log_message("\nCreating summary report...")
        report_file = OUTPUT_DIR / f"summary_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w') as f:
            f.write(f"Browser Power Efficiency Test Results\n")
            f.write(f"=====================================\n")
            f.write(f"Test conducted on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Number of test iterations: {NUM_TEST_ITERATIONS}\n\n")
            
            f.write(f"Test Results Directory: {OUTPUT_DIR}\n")
            f.write(f"Log File: {LOG_FILE}\n\n")
            
            if NUM_TEST_ITERATIONS > 1:
                f.write(f"Aggregate Result Files:\n")
                for agg_file in aggregate_files:
                    f.write(f"- {agg_file.name}\n")
        
        log_message(f"\nSummary report created: {report_file}")
        log_message(f"All test results saved to: {OUTPUT_DIR}")
        
        return {
            "log_file": log_file,
            "report_file": report_file,
            "output_dir": OUTPUT_DIR
        }
    
    finally:
        if httpd:
            log_message("Shutting down HTTP server")
            httpd.shutdown()
        
        if temp_dir:
            log_message("Cleaning up temporary files")
            shutil.rmtree(temp_dir, ignore_errors=True)