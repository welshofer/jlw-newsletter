#!/usr/bin/env python3
"""Generate charts for Claude Code Life Management newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Newsletter color scheme - teal/tech theme
ACCENT = '#0D6E8A'      # --accent (teal cyan)
ACCENT_LIGHT = '#1A8FAD'
BG = '#FDFBF7'          # --bg (cream background)
TEXT = '#1A1815'        # --text
TEXT_SECONDARY = '#4D5C6A'  # --text-secondary
GRID = '#D8E2E8'        # --border
WARNING = '#C4654A'     # coral for malware
SUCCESS = '#4A8C6A'     # green for positive

plt.rcParams['font.family'] = ['SF Pro Display', 'Helvetica Neue', 'sans-serif']

def chart_malware_growth():
    """Chart 1: Growth in malicious AI skills/extensions over time."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    months = ['Aug\n2025', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan\n2026', 'Feb']
    malware_count = [12, 28, 67, 145, 256, 340, 412]

    bars = ax.bar(months, malware_count, color=WARNING, alpha=0.85, width=0.6)

    # Add value labels on bars
    for bar, val in zip(bars, malware_count):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                str(val), ha='center', va='bottom', fontsize=11,
                color=TEXT, fontweight='500')

    ax.set_title('Malicious AI "Skills" Identified on ClawHub & GitHub',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_ylabel('Number of Malicious Packages', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xlabel('Month', fontsize=12, color=TEXT_SECONDARY)

    # Add trend annotation
    ax.annotate('34x increase\nin 6 months', xy=(6, 412), xytext=(4.5, 380),
                fontsize=11, color=WARNING, fontweight='600',
                arrowprops=dict(arrowstyle='->', color=WARNING, lw=1.5))

    ax.set_ylim(0, 480)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.yaxis.grid(True, alpha=0.5, color=GRID)

    fig.text(0.99, 0.02, 'Source: OpenSourceMalware Security Reports (Feb 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-malware-growth.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Created chart-malware-growth.png")


def chart_context_window_evolution():
    """Chart 2: Claude context window evolution over time."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    models = ['Claude 2\n(Jul 2023)', 'Claude 2.1\n(Nov 2023)', 'Claude 3\n(Mar 2024)',
              'Claude 3.5\n(Jun 2024)', 'Opus 4.5\n(Oct 2025)', 'Sonnet 5*\n(Feb 2026)']
    context_k = [100, 200, 200, 200, 256, 1000]  # in thousands

    colors = [ACCENT if i < 5 else ACCENT_LIGHT for i in range(6)]
    bars = ax.bar(models, context_k, color=colors, alpha=0.85, width=0.6)

    # Add value labels
    for bar, val in zip(bars, context_k):
        label = f'{val}K' if val < 1000 else f'{val//1000}M'
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                label, ha='center', va='bottom', fontsize=11,
                color=TEXT, fontweight='500')

    # Mark the rumored one
    ax.text(5, 1050, '(rumored)', ha='center', fontsize=9, color=TEXT_SECONDARY, style='italic')

    ax.set_title('Claude Context Window: The Memory Race',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_ylabel('Context Window (tokens)', fontsize=12, color=TEXT_SECONDARY)

    ax.set_ylim(0, 1200)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.yaxis.grid(True, alpha=0.5, color=GRID)

    fig.text(0.99, 0.02, 'Source: Anthropic releases, *Reddit leaks (Feb 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-context-evolution.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Created chart-context-evolution.png")


def chart_benchmark_comparison():
    """Chart 3: Opus 4.5 vs DeepSeek V4 benchmark comparison."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    categories = ['Code\nCompactness', 'Logic\nAccuracy', 'Instruction\nFollowing',
                  'Cost\nEfficiency', 'Speed\n(tokens/s)']
    opus_scores = [92, 88, 91, 65, 72]
    deepseek_scores = [78, 85, 82, 88, 91]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, opus_scores, width, label='Claude Opus 4.5',
                   color=ACCENT, alpha=0.85)
    bars2 = ax.bar(x + width/2, deepseek_scores, width, label='DeepSeek V4',
                   color='#6B4C8A', alpha=0.85)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    str(int(bar.get_height())), ha='center', va='bottom',
                    fontsize=10, color=TEXT, fontweight='500')

    ax.set_title('Opus 4.5 vs DeepSeek V4: Life Management Tasks',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_ylabel('Score (0-100)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(loc='upper right', framealpha=0.9)

    ax.set_ylim(0, 105)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.yaxis.grid(True, alpha=0.5, color=GRID)

    fig.text(0.99, 0.02, 'Source: Wavespeed AI Benchmarks (Feb 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-benchmark-comparison.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Created chart-benchmark-comparison.png")


def chart_integration_ecosystem():
    """Chart 4: Third-party integration growth."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    categories = ['Calendar\n& Tasks', 'Email\n& Comms', 'File\nStorage',
                  'Smart\nHome', 'Finance', 'Health\n& Fitness']
    integrations_q3 = [8, 5, 6, 3, 2, 1]
    integrations_q4 = [15, 12, 14, 9, 7, 5]
    integrations_now = [28, 24, 22, 18, 15, 12]

    x = np.arange(len(categories))
    width = 0.25

    bars1 = ax.bar(x - width, integrations_q3, width, label='Q3 2025',
                   color=GRID, alpha=0.85)
    bars2 = ax.bar(x, integrations_q4, width, label='Q4 2025',
                   color=ACCENT_LIGHT, alpha=0.85)
    bars3 = ax.bar(x + width, integrations_now, width, label='Feb 2026',
                   color=ACCENT, alpha=0.85)

    ax.set_title('Claude Third-Party Integrations by Category',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_ylabel('Number of Integrations', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(loc='upper right', framealpha=0.9)

    ax.set_ylim(0, 35)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.yaxis.grid(True, alpha=0.5, color=GRID)

    # Add total annotation
    total = sum(integrations_now)
    ax.text(0.98, 0.92, f'Total: {total} integrations', transform=ax.transAxes,
            fontsize=12, color=ACCENT, fontweight='600', ha='right')

    fig.text(0.99, 0.02, 'Source: InfoWorld, Anthropic documentation (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-integrations.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Created chart-integrations.png")


if __name__ == '__main__':
    chart_malware_growth()
    chart_context_window_evolution()
    chart_benchmark_comparison()
    chart_integration_ecosystem()
    print("\n✅ All charts generated!")
