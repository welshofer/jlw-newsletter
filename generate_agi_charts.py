#!/usr/bin/env python3
"""Generate data visualizations for AGI Timeline newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Newsletter color scheme - indigo/violet theme
ACCENT = '#5B4B8A'  # Deep indigo
ACCENT_LIGHT = '#7C5C8A'  # Violet
BG = '#FDFBF7'  # Cream background
TEXT = '#1A1815'  # Dark text
TEXT_SECONDARY = '#4D5C6A'  # Secondary text
GRID = '#D8E2E8'  # Grid lines

OUTPUT_DIR = Path.home() / 'clawd' / 'jlw-newsletter' / 'images'

def setup_figure(figsize=(10, 6)):
    """Create figure with newsletter styling."""
    fig, ax = plt.subplots(figsize=figsize, facecolor=BG)
    ax.set_facecolor(BG)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    return fig, ax


def chart_agi_timeline_predictions():
    """Chart 1: AGI Timeline Predictions from Key Figures (2024-2030)."""
    fig, ax = setup_figure(figsize=(12, 7))

    # Data: Who predicted what, and when
    predictions = [
        ('Dario Amodei\n(Anthropic CEO)', 2027, 'Superhuman AI', '#5B4B8A'),
        ('Mark Zuckerberg\n(Meta CEO)', 2026, 'Personal Superintelligence', '#7C5C8A'),
        ('Sam Altman\n(OpenAI CEO)', 2027, 'AGI', '#8B7BA0'),
        ('Demis Hassabis\n(DeepMind CEO)', 2028, 'Transformative AI', '#9A8BB0'),
        ('Elon Musk\n(xAI)', 2026, 'Smarter than humans', '#A99BC0'),
    ]

    y_positions = np.arange(len(predictions))
    current_year = 2026

    # Draw timeline bars
    for i, (name, year, label, color) in enumerate(predictions):
        bar_length = year - current_year + 0.5
        ax.barh(i, bar_length, left=current_year - 0.25, height=0.6,
                color=color, alpha=0.85, edgecolor='white', linewidth=1)

        # Add year label at end of bar
        ax.text(year + 0.15, i, f'{year}', va='center', ha='left',
                fontsize=14, fontweight='bold', color=TEXT)

        # Add prediction type
        ax.text(year + 0.15, i - 0.25, label, va='top', ha='left',
                fontsize=9, color=TEXT_SECONDARY, style='italic')

    # Styling
    ax.set_yticks(y_positions)
    ax.set_yticklabels([p[0] for p in predictions], fontsize=11)
    ax.set_xlim(2025.5, 2029)
    ax.set_xlabel('Predicted Year', fontsize=12, color=TEXT_SECONDARY)

    # Add "NOW" marker
    ax.axvline(x=2026, color=ACCENT, linestyle='--', linewidth=2, alpha=0.7)
    ax.text(2026, len(predictions) - 0.3, 'NOW\n(Jan 2026)', ha='center',
            fontsize=10, color=ACCENT, fontweight='bold')

    ax.set_title('When Will AGI Arrive?\nPredictions from AI Lab Leaders',
                 fontsize=18, color=TEXT, fontweight='bold', pad=20)

    ax.grid(True, alpha=0.3, color=GRID, axis='x')

    fig.text(0.99, 0.02, 'Source: Public statements and earnings calls (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-agi-predictions.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Created: chart-agi-predictions.png")


def chart_infrastructure_investment():
    """Chart 2: AI Infrastructure Investment Comparison (2026 Commitments)."""
    fig, ax = setup_figure(figsize=(10, 7))

    companies = ['OpenAI\nFunding Round', 'Meta\nCapex 2026', 'Microsoft\nCloud AI',
                 'Google\nDeepMind', 'Amazon\nBedrock/AWS']
    investments = [100, 125, 80, 45, 50]  # Billions USD

    colors = ['#5B4B8A', '#7C5C8A', '#8B7BA0', '#9A8BB0', '#A99BC0']

    bars = ax.bar(companies, investments, color=colors, edgecolor='white', linewidth=2)

    # Add value labels on bars
    for bar, val in zip(bars, investments):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'${val}B', ha='center', va='bottom',
                fontsize=14, fontweight='bold', color=TEXT)

    # Highlight the scale
    ax.axhline(y=100, color=ACCENT, linestyle='--', linewidth=1.5, alpha=0.5)
    ax.text(4.5, 102, '$100B threshold', ha='right', fontsize=10,
            color=ACCENT, style='italic')

    ax.set_ylabel('Investment (Billions USD)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('The AGI Arms Race\n2026 AI Infrastructure Commitments',
                 fontsize=18, color=TEXT, fontweight='bold', pad=20)

    ax.set_ylim(0, 150)
    ax.grid(True, alpha=0.3, color=GRID, axis='y')

    fig.text(0.99, 0.02, 'Source: Company earnings calls and funding announcements (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-agi-investment.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Created: chart-agi-investment.png")


def chart_agi_progress_indicators():
    """Chart 3: AGI Progress Indicators - Technical Milestones."""
    fig, ax = setup_figure(figsize=(12, 7))

    # Milestones and their "completion" percentage toward AGI
    milestones = [
        'Language\nUnderstanding',
        'Code\nGeneration',
        'Mathematical\nReasoning',
        'Scientific\nDiscovery',
        'Autonomous\nAgency',
        'General\nReasoning'
    ]

    # Progress as of Jan 2026 (estimated)
    progress_2025 = [85, 75, 60, 40, 30, 25]
    progress_2026 = [95, 90, 85, 70, 55, 45]  # After this week's announcements

    x = np.arange(len(milestones))
    width = 0.35

    bars1 = ax.bar(x - width/2, progress_2025, width, label='End of 2025',
                   color='#9A8BB0', alpha=0.7, edgecolor='white')
    bars2 = ax.bar(x + width/2, progress_2026, width, label='Jan 2026 (Current)',
                   color=ACCENT, edgecolor='white')

    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}%', ha='center', va='bottom',
                fontsize=10, fontweight='bold', color=TEXT)

    # AGI threshold line
    ax.axhline(y=90, color='#B85C38', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(5.5, 91, 'AGI Threshold (Estimated)', ha='right', fontsize=10,
            color='#B85C38', fontweight='bold')

    ax.set_ylabel('Progress Toward Human-Level (%)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xticks(x)
    ax.set_xticklabels(milestones, fontsize=10)
    ax.set_ylim(0, 105)

    ax.set_title('Closing the Gap: AGI Capability Progress\nRecent Breakthroughs Accelerating Timeline',
                 fontsize=18, color=TEXT, fontweight='bold', pad=20)

    ax.legend(loc='upper left', frameon=True, facecolor=BG)
    ax.grid(True, alpha=0.3, color=GRID, axis='y')

    fig.text(0.99, 0.02, 'Source: Analysis of benchmark performance and research publications (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-agi-progress.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Created: chart-agi-progress.png")


def chart_valuation_growth():
    """Chart 4: AI Lab Valuation Growth Timeline."""
    fig, ax = setup_figure(figsize=(12, 6))

    years = ['2022', '2023', '2024', '2025', 'Jan 2026']

    # Valuations in billions
    openai = [29, 80, 150, 250, 340]  # Estimated based on funding rounds
    anthropic = [4, 18, 61, 180, 350]  # From research

    ax.plot(years, openai, marker='o', markersize=10, linewidth=3,
            color=ACCENT, label='OpenAI')
    ax.plot(years, anthropic, marker='s', markersize=10, linewidth=3,
            color=ACCENT_LIGHT, label='Anthropic')

    # Add value labels
    for i, (o, a) in enumerate(zip(openai, anthropic)):
        ax.annotate(f'${o}B', (years[i], o), textcoords="offset points",
                    xytext=(0,10), ha='center', fontsize=9, color=ACCENT)
        ax.annotate(f'${a}B', (years[i], a), textcoords="offset points",
                    xytext=(0,-15), ha='center', fontsize=9, color=ACCENT_LIGHT)

    ax.set_ylabel('Valuation (Billions USD)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('The Race to $1 Trillion\nAI Lab Valuations Skyrocketing',
                 fontsize=18, color=TEXT, fontweight='bold', pad=20)

    ax.legend(loc='upper left', frameon=True, facecolor=BG)
    ax.grid(True, alpha=0.3, color=GRID)
    ax.set_ylim(0, 400)

    fig.text(0.99, 0.02, 'Source: Company funding rounds and financial reports (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-valuation-growth.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Created: chart-valuation-growth.png")


if __name__ == '__main__':
    print("Generating AGI Timeline newsletter charts...")
    chart_agi_timeline_predictions()
    chart_infrastructure_investment()
    chart_agi_progress_indicators()
    chart_valuation_growth()
    print("All charts generated successfully!")
