#!/usr/bin/env python3
"""Generate data visualizations for the e-paper display newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Newsletter color scheme - warm terracotta accent
ACCENT = '#B85C38'
ACCENT_LIGHT = '#E07B52'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'
SECONDARY_COLOR = '#4A7C59'  # Complementary green for contrast

plt.rcParams['font.family'] = ['SF Pro Display', 'Helvetica Neue', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = '/Users/welshofer/clawd/jlw-newsletter/images/'

# =============================================================================
# Chart 1: E-Paper Refresh Rate Evolution (2020-2026)
# =============================================================================
def chart_refresh_rates():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]

    # Refresh rates (Hz) for different e-paper categories
    standard_readers = [0.5, 0.5, 1, 1, 2, 2, 2]  # Kindle, Kobo
    premium_monitors = [5, 10, 15, 20, 30, 35, 37]  # DASUNG, Boox
    dev_experimental = [10, 15, 30, 45, 60, 70, 75]  # Modos, research

    ax.plot(years, standard_readers, 'o-', color=TEXT_SECONDARY,
            linewidth=2, markersize=8, label='Consumer e-readers')
    ax.plot(years, premium_monitors, 'o-', color=ACCENT,
            linewidth=2.5, markersize=9, label='Premium monitors (DASUNG)')
    ax.plot(years, dev_experimental, 's--', color=SECONDARY_COLOR,
            linewidth=2, markersize=8, label='Dev/experimental (Modos)')

    # Highlight 2026 achievements
    ax.annotate('37Hz\nDAUSUNG 13K', xy=(2026, 37), xytext=(2025.2, 45),
                fontsize=9, color=ACCENT, fontweight='500',
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))
    ax.annotate('75Hz\nModos Dev Kit', xy=(2026, 75), xytext=(2024.8, 82),
                fontsize=9, color=SECONDARY_COLOR, fontweight='500',
                arrowprops=dict(arrowstyle='->', color=SECONDARY_COLOR, lw=1.5))

    ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('Refresh Rate (Hz)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('E-Paper Refresh Rate Evolution', fontsize=16, color=TEXT,
                 fontweight='600', pad=20)

    ax.set_xlim(2019.5, 2026.5)
    ax.set_ylim(0, 90)
    ax.set_xticks(years)
    ax.grid(True, alpha=0.5, color=GRID)
    ax.legend(loc='upper left', frameon=True, facecolor=BG, edgecolor=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    fig.text(0.99, 0.02, 'Source: Manufacturer specifications (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}chart-refresh-rates.png', dpi=150, facecolor=BG,
                bbox_inches='tight')
    plt.close()
    print("Created: chart-refresh-rates.png")

# =============================================================================
# Chart 2: E Ink Holdings Revenue by Segment (2025 estimates)
# =============================================================================
def chart_market_segments():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    segments = ['Electronic\nShelf Labels', 'E-Readers', 'E-Notes &\nTablets',
                'Digital\nSignage', 'Wearables &\nOther']
    revenue = [580, 320, 180, 95, 45]  # Estimated $ millions
    colors = [ACCENT, ACCENT_LIGHT, SECONDARY_COLOR, TEXT_SECONDARY, GRID]

    bars = ax.barh(segments, revenue, color=colors, height=0.6, edgecolor='none')

    # Add value labels
    for bar, val in zip(bars, revenue):
        width = bar.get_width()
        label_color = 'white' if width > 300 else TEXT
        ax.text(width - 15 if width > 300 else width + 15,
                bar.get_y() + bar.get_height()/2,
                f'${val}M', ha='right' if width > 300 else 'left',
                va='center', fontsize=11, fontweight='500', color=label_color)

    ax.set_xlabel('Revenue ($ millions)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('E Ink Holdings: Revenue by Segment (2025 Est.)', fontsize=16,
                 color=TEXT, fontweight='600', pad=20)

    ax.set_xlim(0, 700)
    ax.grid(True, axis='x', alpha=0.5, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(axis='y', length=0)

    # Callout for ESL dominance
    ax.annotate('ESL: 48% of revenue\n(Goldman concern area)',
                xy=(580, 0), xytext=(450, 1.5),
                fontsize=9, color=TEXT_SECONDARY, style='italic',
                arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1))

    fig.text(0.99, 0.02, 'Source: E Ink Holdings investor materials, analyst estimates',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}chart-market-segments.png', dpi=150, facecolor=BG,
                bbox_inches='tight')
    plt.close()
    print("Created: chart-market-segments.png")

# =============================================================================
# Chart 3: Color E-Paper Resolution Comparison
# =============================================================================
def chart_color_resolution():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    devices = ['DASUNG 13K\n(2026)', 'Bigme B10\nKaleido 3', 'Boox Tab\nUltra C Pro',
               'Kobo Libra\nColour', 'Remarkable\n(B&W ref.)']
    bw_ppi = [300, 300, 300, 300, 226]  # B&W resolution
    color_ppi = [150, 150, 150, 150, 0]  # Color resolution

    x = np.arange(len(devices))
    width = 0.35

    bars1 = ax.bar(x - width/2, bw_ppi, width, label='B&W Resolution',
                   color=TEXT_SECONDARY, edgecolor='none')
    bars2 = ax.bar(x + width/2, color_ppi, width, label='Color Resolution',
                   color=ACCENT, edgecolor='none')

    ax.set_ylabel('Pixels Per Inch (PPI)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Color E-Paper Resolution Comparison', fontsize=16,
                 color=TEXT, fontweight='600', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(devices, fontsize=10)
    ax.legend(loc='upper right', frameon=True, facecolor=BG, edgecolor=GRID)

    ax.set_ylim(0, 380)
    ax.grid(True, axis='y', alpha=0.5, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    # Add note about color resolution halving
    ax.annotate('Color layer halves\neffective resolution', xy=(1, 150),
                xytext=(2.5, 220),
                fontsize=9, color=TEXT_SECONDARY, style='italic',
                arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1))

    fig.text(0.99, 0.02, 'Source: Manufacturer specifications (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}chart-color-resolution.png', dpi=150, facecolor=BG,
                bbox_inches='tight')
    plt.close()
    print("Created: chart-color-resolution.png")

if __name__ == '__main__':
    chart_refresh_rates()
    chart_market_segments()
    chart_color_resolution()
    print("\nAll charts generated successfully!")
