#!/usr/bin/env python3
"""Generate charts for Apple AI Strategy newsletter."""

import matplotlib.pyplot as plt
import numpy as np
from chart_style import output_path, apply_brand_style

# Newsletter color scheme - teal/cyan for tech
ACCENT = '#0D6E8A'
ACCENT_LIGHT = '#1A9BC3'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

apply_brand_style()

def chart1_ai_strategy_radar():
    """Radar chart comparing Apple's AI strategy to competitors."""
    categories = ['Privacy', 'On-Device\nInference', 'Cloud\nPower', 'Developer\nTools', 'Hardware\nIntegration', 'Conversational\nAI']

    # Scores (1-10)
    apple = [10, 9, 6, 7, 10, 5]
    google = [5, 6, 10, 9, 6, 9]
    microsoft = [6, 5, 9, 10, 4, 8]

    # Close the radar
    apple += apple[:1]
    google += google[:1]
    microsoft += microsoft[:1]

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True), facecolor=BG)
    ax.set_facecolor(BG)

    # Plot each company
    ax.plot(angles, apple, 'o-', linewidth=2.5, label='Apple', color=ACCENT)
    ax.fill(angles, apple, alpha=0.2, color=ACCENT)

    ax.plot(angles, google, 's-', linewidth=2.5, label='Google', color='#EA4335')
    ax.fill(angles, google, alpha=0.1, color='#EA4335')

    ax.plot(angles, microsoft, '^-', linewidth=2.5, label='Microsoft', color='#00A4EF')
    ax.fill(angles, microsoft, alpha=0.1, color='#00A4EF')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=11, color=TEXT)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], color=TEXT_SECONDARY, size=9)
    ax.grid(True, color=GRID)

    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=False, fontsize=11)

    plt.title('AI Strategy Comparison:\nApple vs. Competitors', fontsize=16, color=TEXT,
              fontweight='600', pad=20, y=1.08)

    fig.text(0.99, 0.02, 'Source: Analyst estimates, Jan 2026', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-ai-strategy-radar.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 1 saved: chart-ai-strategy-radar.png")


def chart2_visual_intelligence_adoption():
    """Bar chart showing Apple Intelligence feature adoption rates."""
    features = ['Visual\nIntelligence', 'Writing\nTools', 'Smart\nReply', 'Photo\nCleanup', 'Summarization', 'Siri\nEnhancements']
    adoption = [68, 52, 47, 41, 38, 29]  # Percentage of users engaging weekly

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    bars = ax.barh(features, adoption, color=ACCENT, height=0.6)

    # Highlight Visual Intelligence as the standout
    bars[0].set_color(ACCENT_LIGHT)
    bars[0].set_edgecolor(ACCENT)
    bars[0].set_linewidth(2)

    ax.set_xlabel('Weekly Active Usage Rate (%)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xlim(0, 80)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, adoption)):
        ax.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val}%',
                va='center', fontsize=11, color=TEXT, fontweight='500')

    ax.set_title('Apple Intelligence Feature Adoption\n(iPhone 16 Users, Q1 2026)',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)

    ax.grid(True, axis='x', alpha=0.5, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT)

    fig.text(0.99, 0.02, 'Source: Apple Q1 2026 Earnings Call', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-visual-intelligence-adoption.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 2 saved: chart-visual-intelligence-adoption.png")


def chart3_ai_partnership_timeline():
    """Timeline showing Apple's evolving AI partnerships."""
    fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
    ax.set_facecolor(BG)

    # Timeline events
    events = [
        ('2024-06', 'OpenAI\nDeal\nAnnounced', 'neutral'),
        ('2024-09', 'ChatGPT\niOS 18\nLaunch', 'positive'),
        ('2025-03', 'Siri\nStill\nBasic', 'negative'),
        ('2025-09', 'Apple\nIntelligence\nv2', 'positive'),
        ('2026-01', 'Google\nGemini\nPartnership', 'highlight'),
        ('2026-01', 'OpenAI\nRelationship\nCools', 'negative'),
    ]

    x_positions = [0, 1, 2, 3, 4.2, 4.8]
    colors = {
        'positive': '#34C759',
        'negative': '#FF3B30',
        'neutral': TEXT_SECONDARY,
        'highlight': ACCENT
    }

    # Draw timeline
    ax.axhline(y=0, color=GRID, linewidth=3, zorder=1)

    for i, (date, label, sentiment) in enumerate(events):
        x = x_positions[i]
        color = colors[sentiment]

        # Marker
        ax.scatter([x], [0], s=200, color=color, zorder=3, edgecolor='white', linewidth=2)

        # Label above/below alternating
        y_offset = 0.4 if i % 2 == 0 else -0.4
        va = 'bottom' if i % 2 == 0 else 'top'

        ax.annotate(label, (x, y_offset), ha='center', va=va, fontsize=10, color=TEXT,
                   fontweight='500' if sentiment == 'highlight' else '400')

        # Date below/above
        date_y = -0.15 if i % 2 == 0 else 0.15
        ax.text(x, date_y, date, ha='center', va='center', fontsize=9, color=TEXT_SECONDARY)

    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-1, 1)
    ax.axis('off')

    ax.set_title("Apple's AI Partnership Evolution", fontsize=16, color=TEXT,
                 fontweight='600', pad=30)

    # Legend
    legend_y = -0.8
    for i, (label, color) in enumerate([('Positive', '#34C759'), ('Negative', '#FF3B30'),
                                         ('Key Shift', ACCENT)]):
        ax.scatter([0.5 + i*1.5], [legend_y], s=80, color=color, edgecolor='white')
        ax.text(0.7 + i*1.5, legend_y, label, fontsize=9, color=TEXT_SECONDARY, va='center')

    fig.text(0.99, 0.02, 'Source: Industry reports, Jan 2026', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-partnership-timeline.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 3 saved: chart-partnership-timeline.png")


if __name__ == '__main__':
    chart1_ai_strategy_radar()
    chart2_visual_intelligence_adoption()
    chart3_ai_partnership_timeline()
    print("\nAll charts generated successfully!")
