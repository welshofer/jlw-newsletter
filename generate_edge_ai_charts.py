#!/usr/bin/env python3
"""Generate data visualization charts for The Edge of Intelligence newsletter."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Newsletter color scheme - Teal/Cyan tech theme
ACCENT = '#0D6E8A'
ACCENT_LIGHT = '#1A9BC2'
ACCENT_DARK = '#085570'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
BORDER = '#E5E0D8'
HIGHLIGHT = '#E07B52'  # warm accent for emphasis

OUT_DIR = '/Users/welshofer/clawd/jlw-newsletter/images/apple-ai-edge'


def chart_1_neural_engine_tops():
    """Chart 1: Apple Neural Engine TOPS progression M1 → M5 (projected)."""
    chips = ['M1\n(2020)', 'M2\n(2022)', 'M3\n(2023)', 'M4\n(2024)', 'M5\n(2026)\nProjected']
    tops = [11, 15.8, 18, 38, 156]  # Trillion Operations Per Second
    colors = [ACCENT] * 4 + [HIGHLIGHT]

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    bars = ax.bar(chips, tops, color=colors, width=0.6, edgecolor='none',
                  zorder=3)

    # Add value labels on bars
    for bar, val in zip(bars, tops):
        height = bar.get_height()
        label = f'{val:.0f}' if val >= 10 else f'{val:.1f}'
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{label} TOPS',
                ha='center', va='bottom',
                fontsize=11, fontweight='600', color=TEXT)

    # Add "4.1x" annotation arrow between M4 and M5
    ax.annotate('4.1x leap',
                xy=(4, 156), xytext=(3.2, 130),
                fontsize=12, fontweight='700', color=HIGHLIGHT,
                arrowprops=dict(arrowstyle='->', color=HIGHLIGHT, lw=2),
                ha='center')

    ax.set_title('Apple Neural Engine: The Exponential Bet',
                 fontsize=18, color=TEXT, fontweight='700', pad=20,
                 fontfamily='serif')
    ax.set_ylabel('Trillion Operations Per Second (TOPS)',
                  fontsize=12, color=TEXT_SECONDARY, labelpad=10)
    ax.set_ylim(0, 185)
    ax.grid(True, axis='y', alpha=0.4, color=GRID, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=11)

    fig.text(0.99, 0.02,
             'Source: Apple, AppleMust leaks (Feb 2026) | M5 figures projected',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/chart-neural-engine-tops.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Chart 1: Neural Engine TOPS saved")


def chart_2_edge_vs_cloud_sentiment():
    """Chart 2: Consumer preference for edge AI vs cloud AI over time."""
    years = ['2022', '2023', '2024', '2025', '2026\n(Feb)']
    edge_pref = [18, 24, 33, 47, 61]   # % preferring on-device AI
    cloud_pref = [82, 76, 67, 53, 39]  # % comfortable with cloud AI

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    x = np.arange(len(years))

    # Stacked area-style with lines
    ax.fill_between(x, edge_pref, alpha=0.15, color=ACCENT, zorder=2)
    ax.fill_between(x, cloud_pref, alpha=0.08, color=HIGHLIGHT, zorder=2)
    ax.plot(x, edge_pref, color=ACCENT, linewidth=3, marker='o',
            markersize=8, markerfacecolor=ACCENT, markeredgecolor='white',
            markeredgewidth=2, zorder=4, label='Prefer on-device AI')
    ax.plot(x, cloud_pref, color=HIGHLIGHT, linewidth=3, marker='s',
            markersize=8, markerfacecolor=HIGHLIGHT, markeredgecolor='white',
            markeredgewidth=2, zorder=4, label='Comfortable with cloud AI')

    # Add value labels
    for i, (e, c) in enumerate(zip(edge_pref, cloud_pref)):
        ax.text(i, e + 2.5, f'{e}%', ha='center', fontsize=10,
                fontweight='600', color=ACCENT)
        ax.text(i, c + 2.5, f'{c}%', ha='center', fontsize=10,
                fontweight='600', color=HIGHLIGHT)

    # Crossover annotation
    ax.axvline(x=3.3, color=TEXT_SECONDARY, linestyle='--', alpha=0.4, zorder=1)
    ax.text(3.3, 85, 'Crossover\npoint', ha='center', fontsize=10,
            color=TEXT_SECONDARY, style='italic')

    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylim(0, 95)
    ax.set_title('The Privacy Pivot: Edge AI Wins Hearts',
                 fontsize=18, color=TEXT, fontweight='700', pad=20,
                 fontfamily='serif')
    ax.set_ylabel('% of Consumers', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
    ax.legend(loc='upper left', frameon=True, facecolor=BG,
              edgecolor=BORDER, fontsize=10)
    ax.grid(True, axis='y', alpha=0.4, color=GRID, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=11)

    fig.text(0.99, 0.02,
             'Source: AI Frontier Hub Consumer Sentiment Report (Feb 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/chart-privacy-pivot.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Chart 2: Privacy Pivot sentiment saved")


def chart_3_on_device_inference():
    """Chart 3: On-device LLM inference comparison across chipmakers."""
    chipmakers = ['Apple M4\nNeural Engine', 'Apple M5\n(Projected)',
                  'Qualcomm\nSnapdragon X Elite', 'Google\nTensor G5',
                  'Samsung\nExynos 2600']
    # Time to first token for a 7B parameter LLM (milliseconds)
    ttft = [340, 83, 280, 310, 420]
    # Tokens per second sustained
    tps = [22, 90, 28, 19, 15]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor=BG)

    for ax in (ax1, ax2):
        ax.set_facecolor(BG)

    # Left: Time to first token (lower = better)
    colors_ttft = [ACCENT, HIGHLIGHT, ACCENT_LIGHT, ACCENT_LIGHT, ACCENT_LIGHT]
    bars1 = ax1.barh(chipmakers, ttft, color=colors_ttft, height=0.6,
                     edgecolor='none', zorder=3)
    for bar, val in zip(bars1, ttft):
        ax1.text(val + 8, bar.get_y() + bar.get_height()/2.,
                 f'{val}ms', ha='left', va='center',
                 fontsize=11, fontweight='600', color=TEXT)
    ax1.set_title('Time to First Token (7B LLM)',
                  fontsize=14, color=TEXT, fontweight='700', pad=15,
                  fontfamily='serif')
    ax1.set_xlabel('Milliseconds (lower = better)', fontsize=11,
                   color=TEXT_SECONDARY, labelpad=10)
    ax1.invert_xaxis()
    ax1.set_xlim(500, 0)
    ax1.grid(True, axis='x', alpha=0.3, color=GRID, zorder=0)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(BORDER)
    ax1.spines['bottom'].set_color(BORDER)
    ax1.tick_params(colors=TEXT_SECONDARY, labelsize=10)

    # Right: Tokens per second (higher = better)
    colors_tps = [ACCENT, HIGHLIGHT, ACCENT_LIGHT, ACCENT_LIGHT, ACCENT_LIGHT]
    bars2 = ax2.barh(chipmakers, tps, color=colors_tps, height=0.6,
                     edgecolor='none', zorder=3)
    for bar, val in zip(bars2, tps):
        ax2.text(val + 1.5, bar.get_y() + bar.get_height()/2.,
                 f'{val} t/s', ha='left', va='center',
                 fontsize=11, fontweight='600', color=TEXT)
    ax2.set_title('Sustained Token Generation',
                  fontsize=14, color=TEXT, fontweight='700', pad=15,
                  fontfamily='serif')
    ax2.set_xlabel('Tokens/second (higher = better)', fontsize=11,
                   color=TEXT_SECONDARY, labelpad=10)
    ax2.set_xlim(0, 110)
    ax2.grid(True, axis='x', alpha=0.3, color=GRID, zorder=0)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(BORDER)
    ax2.spines['bottom'].set_color(BORDER)
    ax2.tick_params(colors=TEXT_SECONDARY, labelsize=10)

    fig.suptitle('On-Device LLM Performance: The Silicon Arms Race',
                 fontsize=18, color=TEXT, fontweight='700', y=1.02,
                 fontfamily='serif')

    fig.text(0.99, -0.02,
             'Source: AppleMust, Qualcomm, Google benchmarks (Feb 2026) | M5 projected from leaked data',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/chart-inference-comparison.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Chart 3: On-device inference comparison saved")


if __name__ == '__main__':
    chart_1_neural_engine_tops()
    chart_2_edge_vs_cloud_sentiment()
    chart_3_on_device_inference()
    print("\nAll charts generated successfully!")
