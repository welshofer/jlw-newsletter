#!/usr/bin/env python3
"""Generate data visualization charts for European Demographics newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Newsletter color scheme - Indigo theme for demographics
ACCENT = '#2E3A59'      # Deep indigo
ACCENT_LIGHT = '#4A5A7A'
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'        # Dark text
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'

OUTPUT_DIR = Path.home() / 'clawd' / 'jlw-newsletter' / 'images'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def setup_style(ax, fig):
    """Apply newsletter styling to axes."""
    ax.set_facecolor(BG)
    fig.set_facecolor(BG)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=10)
    ax.grid(True, alpha=0.4, color=GRID, linestyle='-', linewidth=0.5)

def chart_fertility_rates():
    """Chart 1: European Fertility Rates 2024 vs Replacement Rate"""
    countries = ['Italy', 'Spain', 'Finland', 'Austria', 'Germany', 'France', 'Sweden', 'EU Avg']
    rates_2024 = [1.18, 1.21, 1.25, 1.32, 1.35, 1.44, 1.43, 1.38]

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    setup_style(ax, fig)

    x = np.arange(len(countries))
    bars = ax.bar(x, rates_2024, color=ACCENT, width=0.6, alpha=0.85)

    # Replacement rate line
    ax.axhline(y=2.1, color='#C4654A', linestyle='--', linewidth=2, label='Replacement rate (2.1)')

    # Add value labels on bars
    for bar, rate in zip(bars, rates_2024):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                f'{rate}', ha='center', va='bottom', fontsize=10, color=TEXT, fontweight='500')

    ax.set_xticks(x)
    ax.set_xticklabels(countries, rotation=45, ha='right', fontsize=10)
    ax.set_ylabel('Total Fertility Rate', fontsize=11, color=TEXT_SECONDARY, labelpad=10)
    ax.set_title('European Fertility Rates Hit Record Lows (2024)',
                 fontsize=14, color=TEXT, fontweight='600', pad=15)
    ax.set_ylim(0, 2.4)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)

    fig.text(0.99, 0.02, 'Sources: Eurostat, National Statistics Offices (2024)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-fertility-rates-2024.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Saved: chart-fertility-rates-2024.png")

def chart_foreign_born_growth():
    """Chart 2: Foreign-Born Population Growth in EU"""
    years = [2010, 2015, 2020, 2022, 2023, 2024]
    percentage = [10.0, 11.2, 12.5, 13.1, 13.6, 14.1]
    millions = [44.5, 50.2, 56.3, 59.0, 61.0, 63.3]

    fig, ax1 = plt.subplots(figsize=(10, 6), facecolor=BG)
    setup_style(ax1, fig)

    # Percentage line
    line1 = ax1.plot(years, percentage, color=ACCENT, linewidth=2.5, marker='o',
                     markersize=8, label='Share of Population (%)', zorder=3)
    ax1.fill_between(years, percentage, alpha=0.15, color=ACCENT)

    ax1.set_xlabel('Year', fontsize=11, color=TEXT_SECONDARY, labelpad=10)
    ax1.set_ylabel('Foreign-Born Share (%)', fontsize=11, color=ACCENT, labelpad=10)
    ax1.tick_params(axis='y', labelcolor=ACCENT)
    ax1.set_ylim(8, 16)

    # Second y-axis for absolute numbers
    ax2 = ax1.twinx()
    ax2.set_facecolor('none')
    line2 = ax2.plot(years, millions, color='#C4654A', linewidth=2.5, marker='s',
                     markersize=8, linestyle='--', label='Total (millions)', zorder=2)
    ax2.set_ylabel('Total Foreign-Born (millions)', fontsize=11, color='#C4654A', labelpad=10)
    ax2.tick_params(axis='y', labelcolor='#C4654A')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_color('#C4654A')
    ax2.set_ylim(40, 70)

    # Combined legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=9, framealpha=0.9)

    ax1.set_title('EU Foreign-Born Population: From 10% to 14.1% in 14 Years',
                  fontsize=14, color=TEXT, fontweight='600', pad=15)

    fig.text(0.99, 0.02, 'Source: Eurostat (2024)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-foreign-born-growth.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Saved: chart-foreign-born-growth.png")

def chart_eastern_europe_decline():
    """Chart 3: Eastern European Population Decline Projections"""
    countries = ['Bulgaria', 'Romania', 'Poland', 'Lithuania', 'Croatia']
    decline_pct = [-22.5, -18.0, -14.8, -20.0, -17.5]  # Projected decline by 2050

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    setup_style(ax, fig)

    y = np.arange(len(countries))
    colors = [ACCENT if d > -20 else '#8B3A3A' for d in decline_pct]

    bars = ax.barh(y, decline_pct, color=colors, height=0.6, alpha=0.85)

    ax.axvline(x=0, color=TEXT_SECONDARY, linewidth=1)

    # Add value labels
    for bar, pct in zip(bars, decline_pct):
        ax.text(bar.get_width() - 1.5, bar.get_y() + bar.get_height()/2,
                f'{pct}%', ha='right', va='center', fontsize=11, color='white', fontweight='500')

    ax.set_yticks(y)
    ax.set_yticklabels(countries, fontsize=11)
    ax.set_xlabel('Projected Population Change by 2050 (%)', fontsize=11, color=TEXT_SECONDARY, labelpad=10)
    ax.set_title('Eastern Europe\'s Demographic Exodus',
                 fontsize=14, color=TEXT, fontweight='600', pad=15)
    ax.set_xlim(-28, 2)

    fig.text(0.99, 0.02, 'Source: UN World Population Prospects 2024',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-eastern-europe-decline.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Saved: chart-eastern-europe-decline.png")

def chart_religious_composition():
    """Chart 4: Europe Religious Demographic Shift"""
    years = ['2010', '2030', '2050']

    # Data from Pew Research
    christians = [75, 70, 65]
    muslims = [6, 8, 10]
    unaffiliated = [17, 19, 22]
    other = [2, 3, 3]

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    setup_style(ax, fig)

    x = np.arange(len(years))
    width = 0.2

    bars1 = ax.bar(x - 1.5*width, christians, width, label='Christians', color=ACCENT, alpha=0.85)
    bars2 = ax.bar(x - 0.5*width, muslims, width, label='Muslims', color='#5B8A5C', alpha=0.85)
    bars3 = ax.bar(x + 0.5*width, unaffiliated, width, label='Unaffiliated', color='#7A6A8A', alpha=0.85)
    bars4 = ax.bar(x + 1.5*width, other, width, label='Other', color='#9A8A6A', alpha=0.85)

    # Add value labels
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 1,
                    f'{int(height)}%', ha='center', va='bottom', fontsize=9, color=TEXT)

    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=12)
    ax.set_ylabel('Share of Population (%)', fontsize=11, color=TEXT_SECONDARY, labelpad=10)
    ax.set_title('Europe\'s Shifting Religious Landscape',
                 fontsize=14, color=TEXT, fontweight='600', pad=15)
    ax.set_ylim(0, 85)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9, ncol=2)

    fig.text(0.99, 0.02, 'Source: Pew Research Center (2015, 2017)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-religious-composition.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Saved: chart-religious-composition.png")

def chart_dependency_ratio():
    """Chart 5: Old-Age Dependency Ratio Projection"""
    years = [2022, 2035, 2050, 2070, 2100]
    ratio = [33.9, 42.0, 50.0, 55.0, 60.0]

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    setup_style(ax, fig)

    ax.plot(years, ratio, color=ACCENT, linewidth=3, marker='o', markersize=10, zorder=3)
    ax.fill_between(years, ratio, alpha=0.2, color=ACCENT)

    # Add annotations
    for i, (year, r) in enumerate(zip(years, ratio)):
        ax.annotate(f'{r}%', (year, r), textcoords="offset points", xytext=(0,12),
                    ha='center', fontsize=11, fontweight='500', color=TEXT)

    # Add warning zone
    ax.axhspan(50, 65, alpha=0.1, color='#C4654A', label='Critical pressure zone')

    ax.set_xlabel('Year', fontsize=11, color=TEXT_SECONDARY, labelpad=10)
    ax.set_ylabel('Old-Age Dependency Ratio (%)', fontsize=11, color=TEXT_SECONDARY, labelpad=10)
    ax.set_title('The Looming Pension Crisis: Dependency Ratio Nearly Doubles',
                 fontsize=14, color=TEXT, fontweight='600', pad=15)
    ax.set_ylim(25, 68)
    ax.set_xlim(2018, 2105)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)

    # Add context annotation
    ax.text(2060, 38, 'By 2100: <2 workers\nper retiree', fontsize=9,
            color=TEXT_SECONDARY, style='italic', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=BG, edgecolor=GRID))

    fig.text(0.99, 0.02, 'Source: Eurostat Population Projections (2024)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-dependency-ratio.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Saved: chart-dependency-ratio.png")

if __name__ == '__main__':
    print("Generating demographic charts...")
    chart_fertility_rates()
    chart_foreign_born_growth()
    chart_eastern_europe_decline()
    chart_religious_composition()
    chart_dependency_ratio()
    print("All charts generated successfully!")
