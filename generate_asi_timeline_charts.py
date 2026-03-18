#!/usr/bin/env python3
"""
Generate charts for ASI Timeline newsletter (January 30, 2026)
Theme: Deep indigo/violet (#5B4B8A) for scientific/forecasting aesthetic
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

# Newsletter color scheme - indigo theme for ASI/forecasting
ACCENT = '#5B4B8A'      # Deep indigo
ACCENT_LIGHT = '#7C6B9A'
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'
BORDER = '#D1C9BC'

# Set up matplotlib style
plt.rcParams['font.family'] = ['Source Sans 3', 'sans-serif']
plt.rcParams['axes.facecolor'] = BG
plt.rcParams['figure.facecolor'] = BG
plt.rcParams['savefig.facecolor'] = BG

def chart_1_expert_predictions():
    """Chart 1: ASI Timeline Predictions by Expert (horizontal bar chart with ranges)"""

    fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
    ax.set_facecolor(BG)

    # Expert predictions (name, earliest_year, latest_year, median_estimate)
    experts = [
        ('Ray Kurzweil', 2029, 2035, 2029),
        ('Sam Altman (OpenAI)', 2027, 2032, 2028),
        ('Dario Amodei (Anthropic)', 2027, 2030, 2027),
        ('Demis Hassabis (DeepMind)', 2030, 2040, 2033),
        ('Elon Musk', 2026, 2030, 2028),
        ('Geoffrey Hinton', 2028, 2040, 2035),
        ('Yann LeCun (Meta)', 2040, 2060, 2050),
        ('Gary Marcus', 2050, 2100, 2075),
    ]

    experts = experts[::-1]  # Reverse for bottom-to-top display

    y_pos = np.arange(len(experts))
    names = [e[0] for e in experts]
    starts = [e[1] for e in experts]
    ends = [e[2] for e in experts]
    medians = [e[3] for e in experts]

    # Draw range bars
    for i, (name, start, end, median) in enumerate(experts):
        # Range bar
        ax.barh(i, end - start, left=start, height=0.5,
                color=ACCENT_LIGHT, alpha=0.4, edgecolor=ACCENT, linewidth=1)
        # Median marker
        ax.scatter([median], [i], color=ACCENT, s=100, zorder=5, marker='|', linewidth=3)

    # Current year line
    ax.axvline(x=2026, color='#C4654A', linestyle='--', linewidth=2, alpha=0.8, label='Current Year (2026)')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=11, color=TEXT)
    ax.set_xlabel('Predicted Year for ASI/Transformative AI', fontsize=12, color=TEXT_SECONDARY, labelpad=15)
    ax.set_xlim(2024, 2105)

    ax.set_title('When Will ASI Arrive? Expert Predictions',
                 fontsize=16, color=TEXT, fontweight='600', pad=20, loc='left')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.grid(axis='x', alpha=0.3, color=GRID)

    # Legend
    range_patch = mpatches.Patch(color=ACCENT_LIGHT, alpha=0.4, label='Prediction Range')
    median_line = plt.Line2D([0], [0], color=ACCENT, marker='|', linestyle='', markersize=10, label='Central Estimate')
    current_line = plt.Line2D([0], [0], color='#C4654A', linestyle='--', linewidth=2, label='Current Year (2026)')
    ax.legend(handles=[range_patch, median_line, current_line], loc='lower right', fontsize=9)

    fig.text(0.99, 0.02, 'Sources: Various interviews, podcasts, and public statements (2024-2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-asi-predictions.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Generated: chart-asi-predictions.png")


def chart_2_ai_lab_valuations():
    """Chart 2: AI Lab Valuations Comparison (Jan 2026)"""

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    companies = ['OpenAI', 'Anthropic', 'xAI', 'Mistral', 'Cohere', 'Inflection*']
    valuations = [300, 350, 50, 6.5, 5.5, 4]  # Billions USD
    colors = [ACCENT if v >= 50 else ACCENT_LIGHT for v in valuations]

    bars = ax.barh(companies[::-1], valuations[::-1], color=colors[::-1], edgecolor=TEXT, linewidth=0.5)

    # Add value labels
    for bar, val in zip(bars, valuations[::-1]):
        width = bar.get_width()
        label_x = width + 5 if width < 200 else width - 40
        color = TEXT if width < 200 else 'white'
        ax.text(label_x, bar.get_y() + bar.get_height()/2, f'${val}B',
                va='center', ha='left' if width < 200 else 'right',
                fontsize=11, color=color, fontweight='500')

    ax.set_xlabel('Valuation (Billions USD)', fontsize=12, color=TEXT_SECONDARY, labelpad=15)
    ax.set_xlim(0, 420)

    ax.set_title('AI Lab Valuations: The Race to ASI',
                 fontsize=16, color=TEXT, fontweight='600', pad=20, loc='left')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.grid(axis='x', alpha=0.3, color=GRID)

    fig.text(0.99, 0.02, '*Inflection assets largely acquired by Microsoft. Sources: Crunchbase, Reuters, TechCrunch (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-ai-valuations.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Generated: chart-ai-valuations.png")


def chart_3_compute_energy_scaling():
    """Chart 3: Compute & Energy Requirements for ASI-Scale Training"""

    fig, ax1 = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax1.set_facecolor(BG)

    # Model generations
    models = ['GPT-3\n(2020)', 'GPT-4\n(2023)', 'GPT-5\n(2025)', 'ASI-Scale\n(Est.)', 'Meta\nPrometheus']

    # Training compute in FLOPs (log scale, approximate)
    compute_pflops_days = [3.6e3, 2.1e6, 2e7, 2e9, 5e9]  # petaFLOP-days equivalent

    # Power consumption for training (MW)
    power_mw = [0.3, 10, 100, 1000, 6600]

    x = np.arange(len(models))

    # Plot compute (log scale)
    color1 = ACCENT
    ax1.bar(x - 0.2, compute_pflops_days, 0.35, label='Training Compute', color=color1, alpha=0.8)
    ax1.set_ylabel('Training Compute (petaFLOP-days, log scale)', color=color1, fontsize=11)
    ax1.set_yscale('log')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(1e2, 1e11)

    # Second y-axis for power
    ax2 = ax1.twinx()
    color2 = '#C4654A'  # Terracotta for energy
    ax2.bar(x + 0.2, power_mw, 0.35, label='Peak Power (MW)', color=color2, alpha=0.8)
    ax2.set_ylabel('Peak Power Consumption (MW)', color=color2, fontsize=11)
    ax2.set_yscale('log')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(0.1, 20000)

    ax1.set_xticks(x)
    ax1.set_xticklabels(models, fontsize=10, color=TEXT)

    ax1.set_title('The Exponential Cost of Intelligence',
                  fontsize=16, color=TEXT, fontweight='600', pad=20, loc='left')

    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_color(BORDER)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)

    fig.text(0.99, 0.02, 'Sources: Epoch AI, SemiAnalysis, Meta press releases (Jan 2026). ASI-Scale estimates are speculative.',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-compute-energy.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Generated: chart-compute-energy.png")


def chart_4_agi_asi_milestones():
    """Chart 4: Timeline of AGI/ASI Milestones"""

    fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
    ax.set_facecolor(BG)

    # Milestones (year, label, category: 'achieved' or 'projected')
    milestones = [
        (2020, 'GPT-3', 'achieved'),
        (2022, 'ChatGPT Launch', 'achieved'),
        (2023, 'GPT-4 / Gemini', 'achieved'),
        (2024, 'Claude 3 / o1', 'achieved'),
        (2025, 'GPT-5 / Agentic AI', 'achieved'),
        (2026, 'Superhuman Coding', 'projected'),
        (2027, 'AGI (Narrow)', 'projected'),
        (2028, 'AGI (Broad)', 'projected'),
        (2030, 'Recursive Self-Improvement?', 'projected'),
        (2035, 'ASI (Optimistic)', 'projected'),
    ]

    years = [m[0] for m in milestones]
    labels = [m[1] for m in milestones]
    categories = [m[2] for m in milestones]

    colors = [ACCENT if c == 'achieved' else ACCENT_LIGHT for c in categories]
    alphas = [1.0 if c == 'achieved' else 0.5 for c in categories]

    # Draw timeline
    ax.axhline(y=0, color=BORDER, linewidth=2, zorder=1)

    # Plot points
    for i, (year, label, cat) in enumerate(milestones):
        color = ACCENT if cat == 'achieved' else ACCENT_LIGHT
        marker = 'o' if cat == 'achieved' else 's'
        alpha = 1.0 if cat == 'achieved' else 0.6

        ax.scatter([year], [0], s=150, color=color, alpha=alpha, marker=marker, zorder=3,
                  edgecolor=TEXT if cat == 'achieved' else BORDER, linewidth=1)

        # Alternating label positions
        y_offset = 0.15 if i % 2 == 0 else -0.25
        va = 'bottom' if i % 2 == 0 else 'top'

        ax.annotate(label, (year, 0), xytext=(year, y_offset),
                   fontsize=9, ha='center', va=va, color=TEXT,
                   fontweight='500' if cat == 'achieved' else '400',
                   arrowprops=dict(arrowstyle='-', color=GRID, lw=0.5))

    # Current year marker
    ax.axvline(x=2026, color='#C4654A', linestyle='--', linewidth=2, alpha=0.8, zorder=2)
    ax.text(2026, 0.35, 'NOW', ha='center', fontsize=10, color='#C4654A', fontweight='600')

    ax.set_xlim(2019, 2037)
    ax.set_ylim(-0.5, 0.5)
    ax.axis('off')

    ax.set_title('The Road to Superintelligence: Key Milestones',
                 fontsize=16, color=TEXT, fontweight='600', pad=20, loc='left')

    # Legend
    achieved_marker = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=ACCENT,
                                  markersize=10, label='Achieved')
    projected_marker = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=ACCENT_LIGHT,
                                   markersize=10, alpha=0.6, label='Projected')
    ax.legend(handles=[achieved_marker, projected_marker], loc='upper right', fontsize=9)

    fig.text(0.99, 0.02, 'Timeline reflects industry consensus as of January 2026. "Projected" milestones are speculative.',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-agi-timeline.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Generated: chart-agi-timeline.png")


if __name__ == '__main__':
    print("Generating ASI timeline charts...")
    chart_1_expert_predictions()
    chart_2_ai_lab_valuations()
    chart_3_compute_energy_scaling()
    chart_4_agi_asi_milestones()
    print("All charts generated successfully!")
