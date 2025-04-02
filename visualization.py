#!/usr/bin/env python3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import datetime
from config import ANALYSIS_OUTPUT_DIR, TEST_TYPES, BROWSER_COLORS

plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.style.use('ggplot')

def create_average_power_comparison(aggregate_data):
    if not aggregate_data:
        print("No aggregate data available for average power comparison")
        return
    
    fig, axes = plt.subplots(len(aggregate_data), 1, figsize=(14, 4 * len(aggregate_data)), sharex=True)
    
    if len(aggregate_data) == 1:
        axes = [axes]
    
    for i, (test_type, df) in enumerate(aggregate_data.items()):
        ax = axes[i]
        
        df_sorted = df.sort_values('Avg Power Mean (W)')
        
        colors = [BROWSER_COLORS.get(b.lower(), '#333333') for b in df_sorted['Browser'].str.lower()]
        
        bars = ax.bar(df_sorted['Browser'], df_sorted['Avg Power Mean (W)'], color=colors)
        
        ax.errorbar(
            df_sorted['Browser'], 
            df_sorted['Avg Power Mean (W)'], 
            yerr=df_sorted['Avg Power StdDev (W)'],
            fmt='none', 
            ecolor='black', 
            capsize=5
        )
        
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height + 0.1,
                f'{height:.2f}W',
                ha='center', 
                va='bottom',
                fontsize=10
            )
        
        ax.set_title(f'Average Power Consumption - {test_type.replace("_", " ").title()} Test', fontsize=14)
        ax.set_ylabel('Average Power (Watts)', fontsize=12)
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        min_power = df_sorted['Avg Power Mean (W)'].min() * 0.98
        max_power = df_sorted['Avg Power Mean (W)'].max() * 1.02
        ax.set_ylim(min_power, max_power)
        
        min_power_data = df_sorted['Avg Power Mean (W)'].min()
        ax.axhline(y=min_power_data, color='green', linestyle='--', alpha=0.6)
        ax.text(len(df_sorted) - 0.5, min_power_data, 'More Efficient', 
                color='green', ha='right', va='bottom', fontsize=10)
    
    plt.xlabel('Browser', fontsize=12)
    plt.tight_layout()
    
    output_file = ANALYSIS_OUTPUT_DIR / "average_power_comparison.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved average power comparison chart to {output_file}")
    plt.close()

def create_energy_consumption_comparison(aggregate_data):
    if not aggregate_data:
        print("No aggregate data available for energy consumption comparison")
        return
    
    fig, axes = plt.subplots(len(aggregate_data), 1, figsize=(14, 4 * len(aggregate_data)), sharex=True)
    
    if len(aggregate_data) == 1:
        axes = [axes]
    
    for i, (test_type, df) in enumerate(aggregate_data.items()):
        ax = axes[i]
        
        df_sorted = df.sort_values('Total Energy Mean (Wh)')
        
        colors = [BROWSER_COLORS.get(b.lower(), '#333333') for b in df_sorted['Browser'].str.lower()]
        
        bars = ax.bar(df_sorted['Browser'], df_sorted['Total Energy Mean (Wh)'], color=colors)
        
        ax.errorbar(
            df_sorted['Browser'], 
            df_sorted['Total Energy Mean (Wh)'], 
            yerr=df_sorted['Total Energy StdDev (Wh)'],
            fmt='none', 
            ecolor='black', 
            capsize=5
        )
        
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height + 0.001,
                f'{height:.4f}Wh',
                ha='center', 
                va='bottom',
                fontsize=10
            )
        
        ax.set_title(f'Total Energy Consumption - {test_type.replace("_", " ").title()} Test', fontsize=14)
        ax.set_ylabel('Total Energy (Watt-hours)', fontsize=12)
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        min_energy = df_sorted['Total Energy Mean (Wh)'].min()
        ax.axhline(y=min_energy, color='green', linestyle='--', alpha=0.6)
        ax.text(len(df_sorted) - 0.5, min_energy, 'More Efficient', 
                color='green', ha='right', va='bottom', fontsize=10)
    
    plt.xlabel('Browser', fontsize=12)
    plt.tight_layout()
    
    output_file = ANALYSIS_OUTPUT_DIR / "total_energy_comparison.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved total energy comparison chart to {output_file}")
    plt.close()

def create_browser_ranking_heatmap(aggregate_data):
    if not aggregate_data:
        print("No aggregate data available for browser ranking heatmap")
        return
    
    power_rankings = {}
    energy_rankings = {}
    
    for test_type, df in aggregate_data.items():
        power_sorted = df.sort_values('Avg Power Mean (W)')
        power_ranks = {row['Browser'].lower(): rank + 1 for rank, (_, row) in enumerate(power_sorted.iterrows())}
        power_rankings[test_type] = power_ranks
        
        energy_sorted = df.sort_values('Total Energy Mean (Wh)')
        energy_ranks = {row['Browser'].lower(): rank + 1 for rank, (_, row) in enumerate(energy_sorted.iterrows())}
        energy_rankings[test_type] = energy_ranks
    
    all_browsers = sorted(set(sum([list(ranks.keys()) for ranks in power_rankings.values()], [])))
    
    power_matrix = pd.DataFrame(index=TEST_TYPES, columns=all_browsers)
    energy_matrix = pd.DataFrame(index=TEST_TYPES, columns=all_browsers)
    
    for test_type in TEST_TYPES:
        if test_type in power_rankings:
            for browser in all_browsers:
                power_matrix.at[test_type, browser] = power_rankings[test_type].get(browser, np.nan)
                energy_matrix.at[test_type, browser] = energy_rankings[test_type].get(browser, np.nan)
    
    power_matrix = power_matrix.apply(pd.to_numeric, errors='coerce')
    energy_matrix = energy_matrix.apply(pd.to_numeric, errors='coerce')
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    sns.heatmap(power_matrix, annot=True, cmap="RdYlGn_r", ax=ax1, cbar_kws={'label': 'Ranking'})
    ax1.set_title("Browser Rankings by Average Power Consumption\n(1 = Best/Lowest Power)", fontsize=14)
    ax1.set_ylabel("Test Type", fontsize=12)
    
    sns.heatmap(energy_matrix, annot=True, cmap="RdYlGn_r", ax=ax2, cbar_kws={'label': 'Ranking'})
    ax2.set_title("Browser Rankings by Total Energy Consumption\n(1 = Best/Lowest Energy)", fontsize=14)
    ax2.set_ylabel("Test Type", fontsize=12)
    ax2.set_xlabel("Browser", fontsize=12)
    
    plt.tight_layout()
    
    output_file = ANALYSIS_OUTPUT_DIR / "browser_ranking_heatmap.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved browser ranking heatmap to {output_file}")
    plt.close()

def create_radar_chart(aggregate_data):
    if not aggregate_data:
        print("No aggregate data available for radar chart")
        return
    
    common_browsers = set()
    first = True
    
    for test_type, df in aggregate_data.items():
        browsers = set(df['Browser'].str.lower())
        if first:
            common_browsers = browsers
            first = False
        else:
            common_browsers &= browsers
    
    common_browsers = sorted(common_browsers)
    
    if not common_browsers:
        print("No common browsers found across all test types for radar chart")
        return
    
    radar_data = {}
    
    for browser in common_browsers:
        browser_data = []
        
        for test_type in TEST_TYPES:
            if test_type in aggregate_data:
                df = aggregate_data[test_type]
                browser_row = df[df['Browser'].str.lower() == browser]
                
                if not browser_row.empty:
                    avg_power = browser_row['Avg Power Mean (W)'].values[0]
                    browser_data.append(avg_power)
                else:
                    browser_data.append(np.nan)
            else:
                browser_data.append(np.nan)
        
        radar_data[browser] = browser_data
    
    normalized_data = {}
    
    for i, test_type in enumerate(TEST_TYPES):
        if test_type in aggregate_data:
            values = [data[i] for data in radar_data.values() if not np.isnan(data[i])]
            
            if values:
                min_val = min(values)
                max_val = max(values)
                
                for browser in radar_data:
                    if i < len(radar_data[browser]) and not np.isnan(radar_data[browser][i]):
                        if min_val == max_val:
                            if browser not in normalized_data:
                                normalized_data[browser] = [0] * len(TEST_TYPES)
                            normalized_data[browser][i] = 1
                        else:
                            val = radar_data[browser][i]
                            norm_val = (max_val - val) / (max_val - min_val)
                            
                            if browser not in normalized_data:
                                normalized_data[browser] = [0] * len(TEST_TYPES)
                            normalized_data[browser][i] = norm_val
    
    test_labels = [test_type.replace("_", " ").title() for test_type in TEST_TYPES]
    
    N = len(test_labels)
    
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    plt.xticks(angles[:-1], test_labels, size=12)
    
    ax.set_rlabel_position(0)
    plt.yticks([0.25, 0.5, 0.75, 1], ["0.25", "0.50", "0.75", "1.00"], color="grey", size=10)
    plt.ylim(0, 1)
    
    for browser in common_browsers:
        if browser in normalized_data:
            values = normalized_data[browser]
            values += values[:1]
            
            ax.plot(angles, values, linewidth=2, label=browser.capitalize(), 
                    color=BROWSER_COLORS.get(browser, '#333333'))
            ax.fill(angles, values, alpha=0.1, color=BROWSER_COLORS.get(browser, '#333333'))
    
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.title("Browser Efficiency Across Test Types\n(Higher is Better - Normalized)", size=15)
    
    output_file = ANALYSIS_OUTPUT_DIR / "browser_radar_chart.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved browser radar chart to {output_file}")
    plt.close()

def create_browser_efficiency_index(aggregate_data):
    if not aggregate_data:
        print("No aggregate data available for efficiency index")
        return
    
    efficiency_scores = {}
    
    for test_type, df in aggregate_data.items():
        min_power = df['Avg Power Mean (W)'].min()
        max_power = df['Avg Power Mean (W)'].max()
        power_range = max_power - min_power
        
        for _, row in df.iterrows():
            browser = row['Browser'].lower()
            
            if browser not in efficiency_scores:
                efficiency_scores[browser] = {
                    'scores': {},
                    'total_score': 0,
                    'test_count': 0
                }
            
            if power_range > 0:
                score = 100 * (max_power - row['Avg Power Mean (W)']) / power_range
            else:
                score = 100
            
            efficiency_scores[browser]['scores'][test_type] = score
            efficiency_scores[browser]['total_score'] += score
            efficiency_scores[browser]['test_count'] += 1
    
    browser_scores = []
    for browser, data in efficiency_scores.items():
        if data['test_count'] > 0:
            avg_score = data['total_score'] / data['test_count']
            
            test_scores = {}
            for test_type in TEST_TYPES:
                test_scores[test_type] = data['scores'].get(test_type, np.nan)
            
            browser_scores.append({
                'Browser': browser.capitalize(),
                'Average Score': avg_score,
                **test_scores
            })
    
    browser_scores.sort(key=lambda x: x['Average Score'], reverse=True)
    
    df_scores = pd.DataFrame(browser_scores)
    
    plt.figure(figsize=(12, 8))
    
    colors = [BROWSER_COLORS.get(b.lower(), '#333333') for b in df_scores['Browser'].str.lower()]
    
    bars = plt.bar(df_scores['Browser'], df_scores['Average Score'], color=colors)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height + 1,
            f'{height:.1f}',
            ha='center', 
            va='bottom',
            fontsize=10
        )
    
    plt.title('Browser Power Efficiency Index\n(Higher Score = Better Efficiency)', fontsize=16)
    plt.ylabel('Efficiency Score (0-100)', fontsize=14)
    plt.xlabel('Browser', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylim(0, 105)
    
    output_file = ANALYSIS_OUTPUT_DIR / "browser_efficiency_index.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved browser efficiency index to {output_file}")
    plt.close()