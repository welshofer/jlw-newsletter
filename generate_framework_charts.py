#!/usr/bin/env python3
"""Generate data visualization charts for the desktop frameworks newsletter."""

import matplotlib.pyplot as plt
import numpy as np
from chart_style import output_path, apply_brand_style

# Newsletter color scheme - teal/cyan for tech topics
ACCENT = '#0D6E8A'
ACCENT_LIGHT = '#4A9BB8'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Additional colors for the three frameworks
TAURI_COLOR = '#0D6E8A'      # Teal (primary accent)
ELECTRON_COLOR = '#6B5B95'   # Purple
SWIFTUI_COLOR = '#F28E2B'    # Orange

apply_brand_style()

def chart_bundle_size():
    """Bar chart comparing bundle sizes."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    frameworks = ['Tauri', 'SwiftUI', 'Electron']
    sizes = [6, 5, 115]  # MB - using averages from research
    colors = [TAURI_COLOR, SWIFTUI_COLOR, ELECTRON_COLOR]

    bars = ax.bar(frameworks, sizes, color=colors, width=0.6, edgecolor='none')

    # Add value labels on bars
    for bar, size in zip(bars, sizes):
        height = bar.get_height()
        ax.annotate(f'{size} MB',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 8),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=14, fontweight='600', color=TEXT)

    ax.set_ylabel('Bundle Size (MB)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Application Bundle Size Comparison', fontsize=18, color=TEXT, fontweight='600', pad=20)

    ax.set_ylim(0, 140)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.yaxis.grid(True, alpha=0.3, color=GRID)

    # Source
    fig.text(0.99, 0.02, 'Source: Codeology 2025 Benchmarks', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-bundle-size-compare.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ chart-bundle-size-compare.png")

def chart_memory_usage():
    """Grouped bar chart comparing memory usage."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    frameworks = ['Tauri', 'SwiftUI', 'Electron']
    idle_memory = [40, 22, 225]  # MB - midpoint of ranges
    colors = [TAURI_COLOR, SWIFTUI_COLOR, ELECTRON_COLOR]

    x = np.arange(len(frameworks))
    bars = ax.bar(x, idle_memory, color=colors, width=0.5)

    # Add value labels
    for bar, mem in zip(bars, idle_memory):
        height = bar.get_height()
        ax.annotate(f'{mem} MB',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 8),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=14, fontweight='600', color=TEXT)

    ax.set_xticks(x)
    ax.set_xticklabels(frameworks)
    ax.set_ylabel('Memory Usage (MB)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Idle Memory Consumption', fontsize=18, color=TEXT, fontweight='600', pad=20)

    ax.set_ylim(0, 280)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.yaxis.grid(True, alpha=0.3, color=GRID)

    fig.text(0.99, 0.02, 'Source: OpenReplay 2025 Analysis', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-memory-usage.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ chart-memory-usage.png")

def chart_github_stars():
    """Line chart showing GitHub star growth trajectories."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Approximate star history (2021-2025)
    years = [2021, 2022, 2023, 2024, 2025]

    tauri_stars = [15, 35, 60, 80, 100]  # Rapid growth
    electron_stars = [90, 100, 108, 115, 120]  # Mature, plateauing

    ax.plot(years, tauri_stars, color=TAURI_COLOR, linewidth=3, marker='o',
            markersize=8, label='Tauri')
    ax.plot(years, electron_stars, color=ELECTRON_COLOR, linewidth=3, marker='s',
            markersize=8, label='Electron')

    # Annotate current values
    ax.annotate('100K+', xy=(2025, 100), xytext=(10, 0),
                textcoords='offset points', fontsize=11, fontweight='600',
                color=TAURI_COLOR, va='center')
    ax.annotate('~120K', xy=(2025, 120), xytext=(10, 0),
                textcoords='offset points', fontsize=11, fontweight='600',
                color=ELECTRON_COLOR, va='center')

    ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('GitHub Stars (thousands)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('GitHub Star Growth: Momentum vs Maturity', fontsize=18, color=TEXT, fontweight='600', pad=20)

    ax.legend(loc='upper left', frameon=False, fontsize=11)
    ax.set_xlim(2020.5, 2026)
    ax.set_ylim(0, 140)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.yaxis.grid(True, alpha=0.3, color=GRID)
    ax.xaxis.grid(True, alpha=0.3, color=GRID)

    fig.text(0.99, 0.02, 'Source: GitHub Star History', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-github-stars.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ chart-github-stars.png")

def chart_platform_coverage():
    """Horizontal bar chart showing platform coverage."""
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    ax.set_facecolor(BG)

    platforms = ['macOS', 'Windows', 'Linux', 'iOS', 'Android', 'Web']

    # Coverage: 1 = full support, 0 = no support
    tauri_coverage = [1, 1, 1, 1, 1, 1]  # Full cross-platform with v2
    electron_coverage = [1, 1, 1, 0, 0, 0]  # Desktop only
    swiftui_coverage = [1, 0, 0, 1, 0, 0]  # Apple only

    y = np.arange(len(platforms))
    height = 0.25

    ax.barh(y - height, tauri_coverage, height, label='Tauri 2.0', color=TAURI_COLOR)
    ax.barh(y, electron_coverage, height, label='Electron', color=ELECTRON_COLOR)
    ax.barh(y + height, swiftui_coverage, height, label='SwiftUI', color=SWIFTUI_COLOR)

    ax.set_yticks(y)
    ax.set_yticklabels(platforms)
    ax.set_xlabel('Platform Support', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Cross-Platform Coverage Comparison', fontsize=18, color=TEXT, fontweight='600', pad=20)

    ax.set_xlim(0, 1.2)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Not Supported', 'Supported'])

    ax.legend(loc='lower right', frameon=False, fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)

    fig.text(0.99, 0.02, 'Source: Official Framework Documentation (Jan 2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-platform-coverage.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ chart-platform-coverage.png")

def chart_startup_time():
    """Simple comparison of startup times."""
    fig, ax = plt.subplots(figsize=(10, 4), facecolor=BG)
    ax.set_facecolor(BG)

    frameworks = ['SwiftUI', 'Tauri', 'Electron']
    startup_times = [0.1, 0.4, 2.0]  # seconds
    colors = [SWIFTUI_COLOR, TAURI_COLOR, ELECTRON_COLOR]

    bars = ax.barh(frameworks, startup_times, color=colors, height=0.5)

    # Add value labels
    for bar, time in zip(bars, startup_times):
        width = bar.get_width()
        label = f'{time}s' if time >= 1 else f'{int(time*1000)}ms'
        ax.annotate(label,
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(8, 0),
                    textcoords="offset points",
                    ha='left', va='center',
                    fontsize=12, fontweight='600', color=TEXT)

    ax.set_xlabel('Startup Time (seconds)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Application Launch Speed', fontsize=18, color=TEXT, fontweight='600', pad=20)

    ax.set_xlim(0, 2.8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.xaxis.grid(True, alpha=0.3, color=GRID)

    fig.text(0.99, 0.02, 'Source: Developer benchmarks, typical cold start', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-startup-time.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ chart-startup-time.png")

if __name__ == '__main__':
    print("Generating framework comparison charts...")
    chart_bundle_size()
    chart_memory_usage()
    chart_github_stars()
    chart_platform_coverage()
    chart_startup_time()
    print("\nAll charts generated successfully!")
