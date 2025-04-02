#!/usr/bin/env python3
import csv
import statistics
from config import OUTPUT_DIR, SAMPLE_INTERVAL, TIMESTAMP
from utils import log_message

def save_results_to_csv(results, test_type, iteration=None):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    iter_suffix = f"_iter{iteration}" if iteration is not None else ""
    
    detail_file = OUTPUT_DIR / f"{test_type}_power_details{iter_suffix}_{TIMESTAMP}.csv"
    log_message(f"Saving detailed results to {detail_file}")
    
    with open(detail_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        browsers = [result["browser"] for result in results if result]
        header = ["Time (s)"] + browsers
        writer.writerow(header)
        
        max_length = max([len(result["timestamps"]) for result in results if result], default=0)
        
        for i in range(max_length):
            row = [i * SAMPLE_INTERVAL]
            
            for result in results:
                if result and i < len(result["timestamps"]):
                    row.append(result["power_readings"][i])
                else:
                    row.append("")
            
            writer.writerow(row)
    
    summary_file = OUTPUT_DIR / f"{test_type}_power_summary{iter_suffix}_{TIMESTAMP}.csv"
    log_message(f"Saving summary results to {summary_file}")
    
    with open(summary_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Browser", "Avg Power (W)", "Max Power (W)", "Min Power (W)", "Total Energy (Wh)"])
        
        for result in results:
            if result:
                writer.writerow([
                    result["browser"],
                    result["avg_power"],
                    result["max_power"],
                    result["min_power"],
                    result["total_energy"]
                ])
    
    return detail_file, summary_file

def save_aggregate_results(all_iterations, test_type):
    browsers = {}
    
    for iteration_results in all_iterations:
        for result in iteration_results:
            if result:
                browser_name = result["browser"]
                if browser_name not in browsers:
                    browsers[browser_name] = {
                        "avg_power": [],
                        "max_power": [],
                        "min_power": [],
                        "total_energy": []
                    }
                
                browsers[browser_name]["avg_power"].append(result["avg_power"])
                browsers[browser_name]["max_power"].append(result["max_power"])
                browsers[browser_name]["min_power"].append(result["min_power"])
                browsers[browser_name]["total_energy"].append(result["total_energy"])
    
    aggregate_results = []
    for browser_name, data in browsers.items():
        avg_power_mean = statistics.mean(data["avg_power"])
        max_power_mean = statistics.mean(data["max_power"])
        min_power_mean = statistics.mean(data["min_power"])
        total_energy_mean = statistics.mean(data["total_energy"])
        
        if len(data["avg_power"]) > 1:
            avg_power_stdev = statistics.stdev(data["avg_power"])
            max_power_stdev = statistics.stdev(data["max_power"])
            min_power_stdev = statistics.stdev(data["min_power"])
            total_energy_stdev = statistics.stdev(data["total_energy"])
        else:
            avg_power_stdev = max_power_stdev = min_power_stdev = total_energy_stdev = 0
        
        aggregate_results.append({
            "browser": browser_name,
            "avg_power_mean": avg_power_mean,
            "avg_power_stdev": avg_power_stdev,
            "max_power_mean": max_power_mean,
            "max_power_stdev": max_power_stdev,
            "min_power_mean": min_power_mean,
            "min_power_stdev": min_power_stdev,
            "total_energy_mean": total_energy_mean,
            "total_energy_stdev": total_energy_stdev
        })
    
    aggregate_file = OUTPUT_DIR / f"{test_type}_aggregate_results_{TIMESTAMP}.csv"
    log_message(f"Saving aggregate results to {aggregate_file}")
    
    with open(aggregate_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Browser", 
            "Avg Power Mean (W)", 
            "Avg Power StdDev (W)",
            "Max Power Mean (W)", 
            "Max Power StdDev (W)",
            "Min Power Mean (W)", 
            "Min Power StdDev (W)",
            "Total Energy Mean (Wh)", 
            "Total Energy StdDev (Wh)"
        ])
        
        for result in aggregate_results:
            writer.writerow([
                result["browser"],
                f"{result['avg_power_mean']:.2f}",
                f"{result['avg_power_stdev']:.2f}",
                f"{result['max_power_mean']:.2f}",
                f"{result['max_power_stdev']:.2f}",
                f"{result['min_power_mean']:.2f}",
                f"{result['min_power_stdev']:.2f}",
                f"{result['total_energy_mean']:.4f}",
                f"{result['total_energy_stdev']:.4f}"
            ])
    
    return aggregate_file