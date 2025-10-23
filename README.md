# An Empirical Evaluation of Energy Consumption Across Web Browsers

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
## How to Cite?
A. DiBenedetto and F. Wedyan, "An Empirical Evaluation of Energy Consumption Across Web Browsers," 2025 10th International Conference on Fog and Mobile Edge Computing (FMEC), Tampa, FL, USA, 2025, pp. 39-48, doi: 10.1109/FMEC65595.2025.11119363.
### BibTex:
@INPROCEEDINGS{11119363,
  author={DiBenedetto, Anthony and Wedyan, Fadi},
  booktitle={2025 10th International Conference on Fog and Mobile Edge Computing (FMEC)}, 
  title={An Empirical Evaluation of Energy Consumption Across Web Browsers}, 
  year={2025},
  pages={39-48},
  keywords={Energy consumption;Power demand;Multi-access edge computing;Green products;Software quality;Rendering (computer graphics);Energy efficiency;User experience;Browsers;Videos;Web browsers;Energy efficiency;Power consumption;Green computing;Empirical study;Software Quality},
  doi={10.1109/FMEC65595.2025.11119363}}
