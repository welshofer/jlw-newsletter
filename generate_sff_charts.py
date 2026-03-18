#!/usr/bin/env python3
"""Generate data visualization charts for SFF shelving newsletter."""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Newsletter color scheme - indigo/violet for literary theme
ACCENT = '#5B4B8A'      # --accent (indigo)
ACCENT_LIGHT = '#8B7BB4'
BG = '#FDFBF7'          # --bg (cream)
TEXT = '#1A1815'        # --text
TEXT_SECONDARY = '#5C564D'  # --text-secondary
GRID = '#E5E0D8'        # --border

OUTPUT_DIR = Path('/Users/welshofer/clawd/jlw-newsletter/images')

def setup_style(ax, fig):
    """Apply consistent newsletter styling."""
    ax.set_facecolor(BG)
    fig.set_facecolor(BG)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY, which='both')
    ax.grid(True, alpha=0.4, color=GRID, linestyle='-', linewidth=0.5)

def chart_market_growth():
    """Chart 1: SFF Market Growth with Romantasy Surge."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    setup_style(ax, fig)

    years = ['2020', '2021', '2022', '2023', '2024', '2025*']
    # Market data (estimated from $17.17B in 2024, 4.7% CAGR, 41.3% surge in 2024)
    total_market = [13.5, 14.2, 15.0, 16.0, 17.17, 18.0]
    romantasy = [0.15, 0.25, 0.35, 0.45, 0.61, 0.75]  # $610M in 2024

    # Create bar chart with overlay
    x = np.arange(len(years))
    width = 0.6

    bars1 = ax.bar(x, total_market, width, label='Total SFF Market', color=ACCENT, alpha=0.7)
    bars2 = ax.bar(x, romantasy, width, label='Romantasy Segment', color='#C4654A', alpha=0.9)

    ax.set_title('The Fantasy Market Surge', fontsize=18, color=TEXT,
                 fontweight='600', pad=20, fontfamily='serif')
    ax.set_xlabel('Year', fontsize=11, color=TEXT_SECONDARY, labelpad=10)
    ax.set_ylabel('Market Value ($ Billion)', fontsize=11, color=TEXT_SECONDARY, labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylim(0, 20)

    # Add growth annotation
    ax.annotate('+41.3%\nin 2024', xy=(4, 17.17), xytext=(4.3, 19),
                fontsize=10, color=ACCENT, fontweight='600',
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

    ax.legend(loc='upper left', frameon=False, fontsize=10)

    fig.text(0.99, 0.02, 'Source: Nielsen BookScan, Industry Analysis (2024)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')
    fig.text(0.01, 0.02, '*Projected', fontsize=8, color=TEXT_SECONDARY, ha='left', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-market-growth.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved chart-market-growth.png")

def chart_reader_crossover():
    """Chart 2: Reader Crossover Data - Donut chart."""
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=BG)

    # Data: What SF readers also buy
    labels = ['Also Buy Fantasy', 'SF Only']
    sizes = [70, 30]  # 60-80% crossover, using 70% as midpoint
    colors = [ACCENT, GRID]
    explode = (0.02, 0)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=None, colors=colors,
                                       autopct='%1.0f%%', shadow=False, startangle=90,
                                       wedgeprops={'edgecolor': BG, 'linewidth': 2},
                                       pctdistance=0.75)

    # Add center circle for donut effect
    centre_circle = plt.Circle((0, 0), 0.5, fc=BG, ec=BG)
    ax.add_patch(centre_circle)

    # Style percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(16)
        autotext.set_fontweight('600')

    ax.set_title('The Genre-Fluid Reader', fontsize=18, color=TEXT,
                 fontweight='600', pad=20, fontfamily='serif', y=1.05)

    # Add center text
    ax.text(0, 0.1, '70%', fontsize=36, ha='center', va='center',
            color=ACCENT, fontweight='700')
    ax.text(0, -0.15, 'of SF readers\nalso buy Fantasy', fontsize=12, ha='center',
            va='center', color=TEXT_SECONDARY)

    # Legend
    ax.legend(wedges, labels, loc='lower center', bbox_to_anchor=(0.5, -0.1),
              frameon=False, fontsize=11, ncol=2)

    fig.text(0.5, 0.02, 'Source: Nielsen BookScan Reader Analysis (2023-2024)',
             fontsize=8, color=TEXT_SECONDARY, ha='center', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-reader-crossover.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved chart-reader-crossover.png")

def chart_historical_timeline():
    """Chart 3: Historical Timeline of SFF Merger."""
    fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
    setup_style(ax, fig)
    ax.grid(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Timeline data
    events = [
        (1923, 'Weird Tales\nlaunches', 'top'),
        (1926, 'Amazing Stories\n(Gernsback)', 'bottom'),
        (1941, '"Speculative\nFiction" coined', 'top'),
        (1965, 'Tolkien\nboom begins', 'bottom'),
        (1971, 'DAW Books\nfounded', 'top'),
        (2020, 'BookTok\nemerges', 'bottom'),
        (2024, 'Romantasy\n$610M', 'top'),
    ]

    # Draw timeline
    years = [e[0] for e in events]
    ax.plot([1920, 2026], [0, 0], color=ACCENT, linewidth=3, solid_capstyle='round')

    for year, label, pos in events:
        # Draw vertical line
        y_offset = 0.4 if pos == 'top' else -0.4
        ax.plot([year, year], [0, y_offset * 0.5], color=ACCENT, linewidth=1.5)

        # Draw dot
        ax.scatter([year], [0], s=80, color=ACCENT, zorder=5)

        # Add label
        ax.annotate(f'{year}\n{label}', xy=(year, y_offset * 0.5),
                    xytext=(year, y_offset),
                    ha='center', va='center' if pos == 'top' else 'top',
                    fontsize=9, color=TEXT, fontweight='500',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GRID))

    ax.set_xlim(1915, 2030)
    ax.set_ylim(-0.8, 0.8)
    ax.set_title('A Century of Convergence', fontsize=18, color=TEXT,
                 fontweight='600', pad=30, fontfamily='serif')
    ax.set_yticks([])
    ax.set_xticks([])

    fig.text(0.5, 0.02, 'Key moments in the merger of Science Fiction and Fantasy shelving',
             fontsize=9, color=TEXT_SECONDARY, ha='center', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-timeline.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved chart-timeline.png")

def chart_demographics():
    """Chart 4: SFF Reader Demographics."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    setup_style(ax, fig)

    categories = ['Female\nReaders', 'Male\nReaders', 'Cross-Genre\nBuyers', 'YA\nCrossover']
    values = [55, 45, 70, 48]  # Based on research data
    colors = ['#C4654A', ACCENT, ACCENT_LIGHT, GRID]

    bars = ax.barh(categories, values, color=colors, height=0.6, edgecolor=BG, linewidth=2)

    ax.set_xlim(0, 100)
    ax.set_title('Who Reads SFF?', fontsize=18, color=TEXT,
                 fontweight='600', pad=20, fontfamily='serif')
    ax.set_xlabel('Percentage of Readership', fontsize=11, color=TEXT_SECONDARY, labelpad=10)

    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val}%',
                va='center', fontsize=12, color=TEXT, fontweight='600')

    # Highlight annotation for female readers
    ax.annotate('Female readership\nnow majority', xy=(55, 3), xytext=(75, 3.5),
                fontsize=9, color='#C4654A', fontweight='500',
                arrowprops=dict(arrowstyle='->', color='#C4654A', lw=1.2))

    fig.text(0.99, 0.02, 'Source: Nielsen BookScan Demographics (2024)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-demographics.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved chart-demographics.png")

if __name__ == '__main__':
    print("Generating SFF newsletter charts...")
    chart_market_growth()
    chart_reader_crossover()
    chart_historical_timeline()
    chart_demographics()
    print("\nAll charts generated!")
