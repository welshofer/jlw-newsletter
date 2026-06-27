#!/usr/bin/env python3
"""Generate charts for the Home NAS newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from chart_style import output_path, apply_brand_style

# Newsletter color scheme - teal accent for tech
ACCENT = '#0D6E8A'      # --accent (teal)
ACCENT_LIGHT = '#2A8BA3'
BG = '#FDFBF7'          # --bg (cream background)
TEXT = '#1A1815'        # --text
TEXT_SECONDARY = '#5C564D'  # --text-secondary
GRID = '#E5E0D8'        # --border

apply_brand_style()

def chart_1_market_share():
    """NAS Market Share - Pie chart showing major players."""
    fig, ax = plt.subplots(figsize=(10, 8), facecolor=BG)
    ax.set_facecolor(BG)

    # Market share data (approximate based on Gartner and industry reports)
    labels = ['Synology', 'QNAP', 'ASUSTOR', 'TerraMaster', 'UGREEN', 'Others']
    sizes = [42, 28, 10, 8, 5, 7]
    colors = [ACCENT, '#2A8BA3', '#4DA3B8', '#70B7C8', '#93CBD8', '#B6DFE8']
    explode = (0.05, 0, 0, 0, 0, 0)  # Highlight Synology

    wedges, texts, autotexts = ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct='%1.0f%%',
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(width=0.6, edgecolor=BG, linewidth=2)
    )

    # Style the percentage labels
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('600')

    # Style the labels
    for text in texts:
        text.set_color(TEXT)
        text.set_fontsize(12)

    ax.set_title('Home NAS Market Share (2025-2026)',
                 fontsize=18, color=TEXT, fontweight='600', pad=20)

    # Add source
    fig.text(0.95, 0.02, 'Source: Industry estimates, Gartner Peer Insights (2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-nas-market-share.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 1 saved: chart-nas-market-share.png")

def chart_2_cloud_vs_nas_cost():
    """5-Year Cost Comparison: Cloud vs NAS."""
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
    ax.set_facecolor(BG)

    years = np.array([0, 1, 2, 3, 4, 5])

    # Cloud storage costs (10TB plan)
    # Assuming $10/month for 2TB, scaling to ~$50/month for 10TB
    cloud_monthly = 50
    cloud_cumulative = years * 12 * cloud_monthly

    # NAS costs (upfront hardware + drives, minimal ongoing)
    nas_hardware = 550  # e.g., Synology DS423+ or QNAP TS-464
    nas_drives = 400    # 2x8TB drives @ ~$200 each
    nas_electricity = 40 * 12  # ~$40/year in power
    nas_initial = nas_hardware + nas_drives
    nas_cumulative = np.array([nas_initial] + [nas_initial + (y * nas_electricity) for y in years[1:]])

    # Hybrid approach (NAS + cloud backup)
    hybrid_nas = nas_initial
    hybrid_cloud = 5 * 12  # $5/month for backup service
    hybrid_cumulative = np.array([hybrid_nas] + [hybrid_nas + (y * (nas_electricity + hybrid_cloud)) for y in years[1:]])

    ax.plot(years, cloud_cumulative, 'o-', color='#C4654A', linewidth=3,
            markersize=8, label='Cloud Only (10TB)')
    ax.plot(years, nas_cumulative, 's-', color=ACCENT, linewidth=3,
            markersize=8, label='NAS Only (16TB capacity)')
    ax.plot(years, hybrid_cumulative, '^-', color='#5B4B8A', linewidth=3,
            markersize=8, label='Hybrid (NAS + Cloud Backup)')

    # Add breakeven annotation
    breakeven_year = 2
    breakeven_cost = nas_cumulative[breakeven_year]
    ax.annotate('Breakeven\nPoint',
                xy=(breakeven_year, breakeven_cost),
                xytext=(breakeven_year + 0.5, breakeven_cost + 300),
                fontsize=11, color=TEXT,
                arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1.5),
                ha='left')

    ax.set_xlabel('Years', fontsize=13, color=TEXT, labelpad=10)
    ax.set_ylabel('Cumulative Cost (USD)', fontsize=13, color=TEXT, labelpad=10)
    ax.set_title('5-Year Storage Cost Comparison',
                 fontsize=18, color=TEXT, fontweight='600', pad=20)

    ax.set_xlim(-0.2, 5.2)
    ax.set_ylim(0, 3500)
    ax.set_xticks(years)
    ax.set_xticklabels(['Year 0', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'])

    ax.grid(True, alpha=0.4, color=GRID, linestyle='-', linewidth=0.8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    ax.tick_params(colors=TEXT_SECONDARY)
    ax.legend(loc='upper left', fontsize=11, frameon=True, facecolor=BG, edgecolor=GRID)

    # Add cost labels at year 5
    for y_val, label, color in [
        (cloud_cumulative[-1], f'${cloud_cumulative[-1]:,.0f}', '#C4654A'),
        (nas_cumulative[-1], f'${nas_cumulative[-1]:,.0f}', ACCENT),
        (hybrid_cumulative[-1], f'${hybrid_cumulative[-1]:,.0f}', '#5B4B8A')
    ]:
        ax.annotate(label, xy=(5, y_val), xytext=(5.15, y_val),
                   fontsize=11, color=color, fontweight='600', va='center')

    fig.text(0.95, 0.02, 'Source: Cloudwards, Android Authority cost analysis (2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-nas-vs-cloud-cost.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 2 saved: chart-nas-vs-cloud-cost.png")

def chart_3_nas_performance():
    """Performance comparison of popular NAS models."""
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=BG)
    ax.set_facecolor(BG)

    # NAS models and specs
    models = [
        'Synology\nDS423+',
        'QNAP\nTS-464',
        'ASUSTOR\nLockerstor 4\nGen3',
        'TerraMaster\nF4-425',
        'UGREEN\nDXP4800+'
    ]

    # Normalized performance scores (0-100 scale)
    # Based on: CPU power, RAM, network speed, expandability
    categories = ['CPU\nPerformance', 'Max RAM', 'Network\nSpeed', 'M.2 Slots', 'Price\nValue']

    # Data: [CPU, RAM, Network, M.2, Value]
    synology = [60, 50, 60, 40, 70]      # J4125, 6GB max, 1GbE, 0 M.2
    qnap = [75, 100, 80, 60, 85]         # N5105, 16GB, 2.5GbE, 2 M.2
    asustor = [95, 100, 90, 80, 60]      # Ryzen, 64GB, 2.5GbE, 4 M.2
    terramaster = [70, 75, 80, 60, 95]   # N95, 8GB, 2.5GbE, 2 M.2
    ugreen = [80, 75, 80, 80, 80]        # N100, 8GB, 2.5GbE, 2 M.2

    data = np.array([synology, qnap, asustor, terramaster, ugreen])

    x = np.arange(len(categories))
    width = 0.15

    colors = [ACCENT, '#2A8BA3', '#4DA3B8', '#70B7C8', '#93CBD8']

    for i, (model, color) in enumerate(zip(models, colors)):
        offset = (i - 2) * width
        bars = ax.bar(x + offset, data[i], width, label=model, color=color, edgecolor=BG, linewidth=1)

    ax.set_xlabel('Specification Category', fontsize=13, color=TEXT, labelpad=15)
    ax.set_ylabel('Score (Normalized 0-100)', fontsize=13, color=TEXT, labelpad=10)
    ax.set_title('4-Bay NAS Performance Comparison',
                 fontsize=18, color=TEXT, fontweight='600', pad=20)

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 110)

    ax.grid(True, alpha=0.4, color=GRID, linestyle='-', linewidth=0.8, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    ax.tick_params(colors=TEXT_SECONDARY)
    ax.legend(loc='upper right', fontsize=10, frameon=True, facecolor=BG,
              edgecolor=GRID, ncol=2)

    fig.text(0.95, 0.02, 'Source: NAS Compares, StorageReview, manufacturer specs (2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-nas-performance.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 3 saved: chart-nas-performance.png")

if __name__ == '__main__':
    chart_1_market_share()
    chart_2_cloud_vs_nas_cost()
    chart_3_nas_performance()
    print("\nAll charts generated successfully!")
