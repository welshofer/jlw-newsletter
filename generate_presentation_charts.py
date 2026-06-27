#!/usr/bin/env python3
"""Generate charts for the Presentation Software Future newsletter."""

import matplotlib.pyplot as plt
import numpy as np
from chart_style import output_path, apply_brand_style

# Newsletter color scheme - indigo/violet for tech/presentations
ACCENT = '#5B4B8A'      # Indigo accent
ACCENT_LIGHT = '#7C5C8A'  # Violet
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'        # Dark text
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

apply_brand_style()

def chart1_market_landscape():
    """Bar chart: AI Presentation Tools vs Traditional - Feature Comparison"""

    categories = ['Content\nGeneration', 'Design\nAutomation', 'Collaboration',
                  'Enterprise\nIntegration', 'Pricing\n(Free tier)']

    traditional = [2, 3, 4, 5, 4]  # PowerPoint, Keynote, Google Slides
    ai_native = [5, 5, 3, 2, 3]    # Gamma, Tome, Beautiful.ai

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    bars1 = ax.bar(x - width/2, traditional, width, label='Traditional (PPT, Keynote, Slides)',
                   color='#6B8BA4', edgecolor='white', linewidth=1)
    bars2 = ax.bar(x + width/2, ai_native, width, label='AI-Native (Gamma, Tome, Beautiful.ai)',
                   color=ACCENT, edgecolor='white', linewidth=1)

    ax.set_ylabel('Capability Score (1-5)', fontsize=11, color=TEXT_SECONDARY)
    ax.set_title('The Presentation Tool Landscape: Traditional vs AI-Native',
                 fontsize=14, color=TEXT, fontweight='600', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10, color=TEXT)
    ax.set_ylim(0, 6)
    ax.legend(loc='upper right', frameon=False, fontsize=9)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.yaxis.grid(True, alpha=0.5, color=GRID)

    # Add value labels on bars
    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, color=TEXT_SECONDARY)

    fig.text(0.99, 0.02, 'Source: Industry analysis, Jan 2026', fontsize=8,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-tool-landscape.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Generated: chart-tool-landscape.png")

def chart2_format_adoption():
    """Pie/donut chart: How knowledge workers share ideas internally"""

    formats = ['Slide Decks', 'Documents/Memos', 'Video (Loom, etc)',
               'Live Whiteboard', 'Chat/Async']
    sizes = [35, 28, 15, 12, 10]
    colors = [ACCENT, ACCENT_LIGHT, '#6B8BA4', '#8BA46B', '#A4826B']
    explode = (0.02, 0, 0, 0, 0)

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=formats,
                                       colors=colors, autopct='%1.0f%%',
                                       startangle=90, pctdistance=0.75,
                                       wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('600')

    for text in texts:
        text.set_color(TEXT)
        text.set_fontsize(10)

    ax.set_title('How Knowledge Workers Share Ideas Internally (2026)',
                 fontsize=14, color=TEXT, fontweight='600', pad=20)

    # Add center text
    ax.text(0, 0, 'Internal\nComms', ha='center', va='center', fontsize=12,
            color=TEXT_SECONDARY, fontweight='500')

    fig.text(0.99, 0.02, 'Source: Enterprise productivity surveys, 2026', fontsize=8,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-format-adoption.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Generated: chart-format-adoption.png")

def chart3_ai_timeline():
    """Timeline: Major AI presentation tool launches and milestones"""

    fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
    ax.set_facecolor(BG)

    # Timeline data
    events = [
        ('2022-09', 'Tome launches\nAI presentations', -1),
        ('2023-03', 'Microsoft Copilot\nin PowerPoint', 1),
        ('2023-06', 'Gamma AI\ngoes viral', -1),
        ('2024-01', 'Beautiful.ai\nenterprise tier', 1),
        ('2024-09', 'Canva Magic\nDesign update', -1),
        ('2025-06', 'Google Slides\nGemini integration', 1),
        ('2026-01', 'Apple Creator Studio\n+ PPT Agent Mode', -1),
    ]

    # Convert dates to positions
    dates = ['Sep\n2022', 'Mar\n2023', 'Jun\n2023', 'Jan\n2024',
             'Sep\n2024', 'Jun\n2025', 'Jan\n2026']
    positions = range(len(events))

    # Draw timeline
    ax.axhline(y=0, color=GRID, linewidth=3, zorder=1)

    for i, (date, event, direction) in enumerate(events):
        # Vertical line
        ax.plot([i, i], [0, direction * 0.4], color=ACCENT if i == len(events)-1 else TEXT_SECONDARY,
                linewidth=2, zorder=2)

        # Event marker
        marker_color = ACCENT if i == len(events)-1 else ACCENT_LIGHT
        ax.scatter([i], [0], s=100, c=[marker_color], zorder=3, edgecolors='white', linewidth=2)

        # Event text
        y_pos = direction * 0.55
        ax.text(i, y_pos, event, ha='center', va='center' if direction > 0 else 'center',
                fontsize=9, color=TEXT, fontweight='500' if i == len(events)-1 else '400',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=BG if i < len(events)-1 else ACCENT + '20',
                          edgecolor=GRID if i < len(events)-1 else ACCENT, linewidth=1))

        # Date below
        ax.text(i, -0.15, dates[i], ha='center', va='top', fontsize=8, color=TEXT_SECONDARY)

    ax.set_xlim(-0.5, len(events) - 0.5)
    ax.set_ylim(-0.8, 1)
    ax.axis('off')

    ax.set_title('The AI Presentation Tool Timeline',
                 fontsize=14, color=TEXT, fontweight='600', pad=20)

    fig.text(0.99, 0.02, 'Source: Product launches and press releases', fontsize=8,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_path('images/chart-ai-timeline.png'),
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Generated: chart-ai-timeline.png")

if __name__ == '__main__':
    chart1_market_landscape()
    chart2_format_adoption()
    chart3_ai_timeline()
    print("\nAll charts generated successfully!")
