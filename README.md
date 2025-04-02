# Browser Power Efficiency Test Suite

A framework to measure and compare power consumption of different web browsers during typical usage scenarios. Created for Lewis University's Software Architecture class.

## Overview

This suite evaluates browser energy efficiency across multiple test scenarios, providing data that can impact battery life and user experience.

## Key Results

Testing on a Microsoft Surface 7 running Ubuntu showed:
- **Vivaldi**: Best efficiency (78.2/100)
- **Brave**: Second best (68.2/100)
- **Chrome**: Unexpectedly lowest (22.6/100)
- Switching browsers could extend battery life by up to 17%

## Test Scenarios

1. **Video Playback**: Video streaming efficiency
2. **CSS Animation**: Dynamic web content rendering
3. **JavaScript Computation**: CPU-intensive tasks
4. **Static Webpage**: Simple browsing baseline
5. **Multiple Tabs**: Multiple tabs efficiency

## Requirements

- Linux system with battery
- Python 3.9+
- Required libraries: matplotlib, seaborn, numpy, pandas
- Browsers to test

## Installation

1. Clone repository
2. Install requirements: `pip install -r requirements.txt`
3. Update paths in `config.py`

## Usage

Run all tests:
```
python main.py
```

With options:
```
python main.py --duration 60 --browsers firefox chrome --test-types video webpage --iterations 3
```

Options:
- `--duration`: Test duration in seconds
- `--browsers`: Specific browsers to test
- `--test-types`: Test types to run
- `--url`: URL for webpage tests
- `--iterations`: Number of test iterations