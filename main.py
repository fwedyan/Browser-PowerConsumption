#!/usr/bin/env python3
import sys
import argparse
from config import WATCH_DURATION, TEST_URL, NUM_TEST_ITERATIONS
from run_tests import run_all_tests

def parse_arguments():
    parser = argparse.ArgumentParser(description='Browser power efficiency test')
    parser.add_argument('--duration', type=int, default=WATCH_DURATION,
                      help=f'Duration of each test in seconds (default: {WATCH_DURATION})')
    parser.add_argument('--browsers', type=str, nargs='+',
                      help='List of browsers to test (default: all available)')
    parser.add_argument('--test-types', type=str, nargs='+', 
                      choices=['video', 'animation', 'js_computation', 'webpage', 'multiple_tabs', 'all'],
                      default=['all'], help='Types of tests to run')
    parser.add_argument('--url', type=str, default=TEST_URL,
                      help=f'URL to test (default: {TEST_URL})')
    parser.add_argument('--iterations', type=int, default=NUM_TEST_ITERATIONS,
                      help=f'Number of test iterations to run (default: {NUM_TEST_ITERATIONS})')
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    from config import WATCH_DURATION, TEST_URL, NUM_TEST_ITERATIONS, WATCH_DURATION, TEST_URL, NUM_TEST_ITERATIONS
    
    if args.duration:
        WATCH_DURATION = args.duration
    
    if args.url:
        TEST_URL = args.url
    
    if args.iterations:
        NUM_TEST_ITERATIONS = args.iterations
    
    results = run_all_tests()
    
    if results:
        print(f"\nTests completed successfully!")
        print(f"Summary report: {results['report_file']}")
        print(f"Log file: {results['log_file']}")
        print(f"Results directory: {results['output_dir']}")
        sys.exit(0)
    else:
        print(f"\nTests failed. Check log for details.")
        sys.exit(1)