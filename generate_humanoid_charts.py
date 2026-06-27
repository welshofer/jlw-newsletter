#!/usr/bin/env python3
"""Generate charts for the humanoid robots newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
import chart_style

# Newsletter color scheme - teal/cyan tech theme
ACCENT = '#0D6E8A'
ACCENT_LIGHT = '#1A8CAA'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Chart 1: Humanoid Robot Pricing Comparison
def create_pricing_chart():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    robots = ['Unitree G1', 'Tesla Optimus\n(projected)', 'Figure 02', 'Boston Dynamics\nAtlas', 'Sanctuary AI\nPhoenix']
    prices = [13500, 25000, 60000, 150000, 200000]
    colors = [ACCENT if p < 30000 else TEXT_SECONDARY for p in prices]

    bars = ax.barh(robots, prices, color=colors, height=0.6)

    # Add price labels
    for bar, price in zip(bars, prices):
        width = bar.get_width()
        label = f'${price:,}'
        ax.text(width + 5000, bar.get_y() + bar.get_height()/2,
                label, va='center', fontsize=11, color=TEXT, fontweight='500')

    ax.set_xlabel('Estimated Price (USD)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Humanoid Robot Pricing Landscape (2026)', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xlim(0, 250000)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))

    # Styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.spines['left'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.grid(axis='x', alpha=0.3, color=GRID)

    # Annotation
    ax.annotate('Unitree disrupts\nat $13.5k', xy=(13500, 0), xytext=(60000, -0.3),
                fontsize=10, color=ACCENT, fontweight='500',
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

    fig.text(0.99, 0.02, 'Source: Company announcements (Jan 2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(Path(chart_style.output_path('images', 'chart-robot-pricing.png')),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-robot-pricing.png")


# Chart 2: Commercial Deployment Timeline
def create_deployment_timeline():
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    ax.set_facecolor(BG)

    companies = ['Agility\n(Digit)', 'Boston Dynamics\n(Atlas)', 'Figure AI', 'Tesla\n(Optimus)', '1X\n(NEO)']
    pilot_start = [2023.5, 2024.0, 2024.5, 2025.0, 2025.5]
    production_start = [2025.0, 2026.0, 2026.5, 2026.75, 2026.75]

    y_pos = np.arange(len(companies))

    # Pilot phase (lighter)
    for i, (company, ps, prd) in enumerate(zip(companies, pilot_start, production_start)):
        ax.barh(i, prd - ps, left=ps, color=ACCENT, alpha=0.4, height=0.4, label='Pilot' if i == 0 else '')
        ax.barh(i, 2027 - prd, left=prd, color=ACCENT, alpha=0.9, height=0.4, label='Production' if i == 0 else '')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(companies, fontsize=11)
    ax.set_xlim(2023, 2027.5)
    ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Humanoid Robot Deployment Timeline', fontsize=16, color=TEXT, fontweight='600', pad=20)

    # Add vertical line for "now"
    ax.axvline(x=2026.08, color='#E74C3C', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(2026.15, 4.5, 'Now', fontsize=10, color='#E74C3C', fontweight='500')

    # Legend
    pilot_patch = mpatches.Patch(color=ACCENT, alpha=0.4, label='Pilot/Testing')
    prod_patch = mpatches.Patch(color=ACCENT, alpha=0.9, label='Production')
    ax.legend(handles=[pilot_patch, prod_patch], loc='lower right', frameon=False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.spines['left'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.grid(axis='x', alpha=0.3, color=GRID)

    fig.text(0.99, 0.02, 'Source: Company announcements, analyst estimates', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(Path(chart_style.output_path('images', 'chart-deployment-timeline.png')),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-deployment-timeline.png")


# Chart 3: Autonomous Task Complexity (Figure AI benchmark)
def create_task_complexity_chart():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    demos = ['Early teleoperated\ndemos (2023)', 'First autonomous\npick-and-place', 'Multi-step\nassembly tasks', 'Unitree G1\nmimicry demo', 'Figure Helix 02\ndishwasher cycle']
    actions = [1, 5, 12, 25, 61]

    colors = [TEXT_SECONDARY if a < 61 else ACCENT for a in actions]
    bars = ax.bar(demos, actions, color=colors, width=0.6)

    # Highlight the 61 actions bar
    bars[-1].set_edgecolor('#074D62')
    bars[-1].set_linewidth(2)

    for bar, action in zip(bars, actions):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{action}', ha='center', fontsize=12, fontweight='600', color=TEXT)

    ax.set_ylabel('Sequential Autonomous Actions', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Humanoid Robot Task Complexity Over Time', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_ylim(0, 75)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.spines['left'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY, axis='x', labelsize=9)
    ax.tick_params(colors=TEXT_SECONDARY, axis='y')
    ax.grid(axis='y', alpha=0.3, color=GRID)

    # Annotation
    ax.annotate('Figure AI: 61 actions\nwithout intervention', xy=(4, 61), xytext=(2.5, 55),
                fontsize=10, color=ACCENT, fontweight='500',
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

    fig.text(0.99, 0.02, 'Source: Company demos, Figure AI (Jan 2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(Path(chart_style.output_path('images', 'chart-task-complexity.png')),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-task-complexity.png")


# Chart 4: Tesla Production Shift
def create_tesla_shift_chart():
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    ax.set_facecolor(BG)

    years = ['2024', '2025', '2026', '2027 (proj)', '2028 (proj)']
    model_sx = [100, 80, 30, 0, 0]  # Percentage of capacity
    optimus = [0, 20, 70, 100, 100]

    x = np.arange(len(years))
    width = 0.35

    ax.bar(x - width/2, model_sx, width, label='Model S/X Production', color=TEXT_SECONDARY, alpha=0.7)
    ax.bar(x + width/2, optimus, width, label='Optimus Production', color=ACCENT)

    ax.set_ylabel('% of Factory Capacity', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Tesla: From Cars to Robots', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylim(0, 120)
    ax.legend(loc='upper right', frameon=False)

    # Add vertical line showing the pivot
    ax.axvline(x=1.5, color='#E74C3C', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.text(1.55, 105, 'Production halt\nannounced', fontsize=9, color='#E74C3C')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.spines['left'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.grid(axis='y', alpha=0.3, color=GRID)

    fig.text(0.99, 0.02, 'Source: Tesla announcements, analyst estimates (Jan 2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(Path(chart_style.output_path('images', 'chart-tesla-shift.png')),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-tesla-shift.png")


if __name__ == '__main__':
    create_pricing_chart()
    create_deployment_timeline()
    create_task_complexity_chart()
    create_tesla_shift_chart()
    print("\nAll charts generated!")
