#!/usr/bin/env python3
import os
import sys
import glob
import re
import pandas as pd
import numpy as np
from pathlib import Path

from config import RESULTS_DIR, ANALYSIS_OUTPUT_DIR, TEST_TYPES, BROWSER_COLORS

def setup_output_directory():
    ANALYSIS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Analysis results will be saved to: {ANALYSIS_OUTPUT_DIR}")

def find_aggregate_files():
    aggregate_files = {}
    for test_type in TEST_TYPES:
        pattern = RESULTS_DIR / f"{test_type}_aggregate_results_*.csv"
        files = list(glob.glob(str(pattern)))
        if files:
            files.sort(reverse=True)
            aggregate_files[test_type] = files[0]
    
    return aggregate_files

def load_aggregate_data(aggregate_files):
    data = {}
    for test_type, filepath in aggregate_files.items():
        try:
            df = pd.read_csv(filepath)
            data[test_type] = df
            print(f"Loaded {test_type} data with {len(df)} entries")
        except Exception as e:
            print(f"Error loading {test_type} data: {e}")
    
    return data

def load_all_individual_browser_files():
    all_data = {}
    
    for test_type in TEST_TYPES:
        browser_data = {}
        
        for browser in BROWSER_COLORS.keys():
            pattern = RESULTS_DIR / f"{test_type}_{browser}_power_summary_iter*.csv"
            files = list(glob.glob(str(pattern)))
            
            if files:
                dfs = []
                for file in files:
                    try:
                        iter_match = re.search(r'iter(\d+)', file)
                        if iter_match:
                            iteration = int(iter_match.group(1))
                            df = pd.read_csv(file)
                            
                            df['Iteration'] = iteration
                            
                            if 'Browser' not in df.columns:
                                df['Browser'] = browser.capitalize()
                                
                            dfs.append(df)
                    except Exception as e:
                        print(f"Error loading {file}: {e}")
                
                if dfs:
                    browser_data[browser] = pd.concat(dfs, ignore_index=True)
        
        if browser_data:
            combined_data = pd.concat(list(browser_data.values()), ignore_index=True)
            all_data[test_type] = combined_data
            print(f"Loaded detailed {test_type} data across {len(browser_data)} browsers")
    
    return all_data

def main():
    print("Browser Power Efficiency Analysis")
    print("=" * 50)
    
    setup_output_directory()
    
    aggregate_files = find_aggregate_files()
    if not aggregate_files:
        print("No aggregate result files found. Please run the browser power tests first.")
        return
    
    print(f"Found {len(aggregate_files)} aggregate files for analysis")
    
    aggregate_data = load_aggregate_data(aggregate_files)
    
    detailed_data = load_all_individual_browser_files()
    
    from visualization import (
        create_average_power_comparison,
        create_energy_consumption_comparison,
        create_browser_ranking_heatmap,
        create_radar_chart,
        create_browser_efficiency_index
    )
    
    print("\nGenerating analysis charts...")
    
    create_average_power_comparison(aggregate_data)
    
    create_energy_consumption_comparison(aggregate_data)
    
    create_browser_ranking_heatmap(aggregate_data)
    
    create_radar_chart(aggregate_data)
    
    create_browser_efficiency_index(aggregate_data)
    
    print("\nAnalysis complete!")
    print(f"All results saved to: {ANALYSIS_OUTPUT_DIR}")

if __name__ == "__main__":
    main()