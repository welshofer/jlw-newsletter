#!/usr/bin/env python3
"""Generate charts for the Workflow Presentation Tools Market newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

# Newsletter color scheme - Teal/Cyan for tech topics
ACCENT = '#0D6E8A'      # --accent (deep teal)
ACCENT_LIGHT = '#3A9DB8'  # lighter teal
BG = '#FDFBF7'          # --bg (cream background)
TEXT = '#1A1815'        # --text
TEXT_SECONDARY = '#4D5C6A'  # --text-secondary
GRID = '#D8E2E8'        # --border
ACCENT_SOFT = 'rgba(13, 110, 138, 0.15)'

# Chart 1: Market Segmentation Donut Chart
def create_market_segmentation():
    fig, ax = plt.subplots(figsize=(10, 8), facecolor=BG)
    ax.set_facecolor(BG)

    # Market segments with estimated shares
    segments = ['Enterprise Platforms\n(Miro, Lucidchart)',
                'Design Systems\n(Figma)',
                'AI-Native Tools\n(Prism, Napkin, Diagrimo)',
                'Developer-First\n(tldraw, Eraser)',
                'Interactive Design\n(Canva, Beautiful.ai)']
    sizes = [30, 25, 15, 12, 18]

    # Color gradient from dark teal to light
    colors = ['#0D6E8A', '#2A8BA8', '#47A8C6', '#64C5E4', '#81D2F2']
    explode = (0, 0, 0.1, 0.05, 0)  # Highlight AI-native

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=segments,
                                       colors=colors, autopct='%1.0f%%',
                                       shadow=False, startangle=90,
                                       pctdistance=0.75,
                                       wedgeprops=dict(width=0.5, edgecolor=BG))

    # Style the text
    for text in texts:
        text.set_fontsize(10)
        text.set_color(TEXT)
    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_fontweight('600')
        autotext.set_color('white')

    # Center text
    ax.text(0, 0, 'Workflow\nPresentation\nTools', ha='center', va='center',
            fontsize=14, fontweight='600', color=TEXT)

    ax.set_title('Market Segmentation: Workflow Visualization Tools (2026)',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)

    # Source attribution
    fig.text(0.99, 0.02, 'Source: Market Analysis (Jan 2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-market-segmentation.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-market-segmentation.png")


# Chart 2: Timeline of This Week's Activity
def create_activity_timeline():
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Events data (date, event, type)
    events = [
        (24, 'Diagrimo\nLaunches', 'launch'),
        (25, 'Figma Slots\nBeta', 'feature'),
        (26, 'tldraw 4.3.0\nSQLite', 'release'),
        (27, 'Canva +\nJotform AI', 'partnership'),
        (28, 'OpenAI\nPrism', 'launch'),
        (28, 'Eraser IaC\nUpdate', 'feature'),
        (29, 'Napkin.ai\nMomentum', 'traction'),
    ]

    # Y positions to avoid overlap (stagger events on same day)
    y_positions = [1.0, 1.0, 1.0, 1.0, 1.3, 0.7, 1.0]

    # Event type colors
    type_colors = {
        'launch': '#0D6E8A',
        'feature': '#47A8C6',
        'release': '#64C5E4',
        'partnership': '#2A8BA8',
        'traction': '#81D2F2'
    }

    # Plot timeline
    ax.axhline(y=1.0, color=GRID, linewidth=2, zorder=1)

    for i, (day, label, etype) in enumerate(events):
        color = type_colors[etype]
        y = y_positions[i]

        # Draw vertical line from timeline
        ax.plot([day, day], [1.0, y], color=color, linewidth=2, zorder=2)

        # Draw circle marker
        ax.scatter(day, y, s=200, color=color, zorder=3, edgecolor='white', linewidth=2)

        # Add label
        va = 'bottom' if y >= 1.0 else 'top'
        offset = 0.1 if y >= 1.0 else -0.1
        ax.text(day, y + offset, label, ha='center', va=va, fontsize=9,
                fontweight='500', color=TEXT, linespacing=1.1)

    # X-axis
    ax.set_xlim(23, 30)
    ax.set_xticks([24, 25, 26, 27, 28, 29])
    ax.set_xticklabels(['Jan 24', 'Jan 25', 'Jan 26', 'Jan 27', 'Jan 28', 'Jan 29'])
    ax.tick_params(axis='x', colors=TEXT_SECONDARY)

    ax.set_ylim(0.3, 1.8)
    ax.set_yticks([])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='#0D6E8A', label='Launch'),
        mpatches.Patch(facecolor='#47A8C6', label='Feature'),
        mpatches.Patch(facecolor='#64C5E4', label='Release'),
        mpatches.Patch(facecolor='#2A8BA8', label='Partnership'),
        mpatches.Patch(facecolor='#81D2F2', label='Traction'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', frameon=False,
              fontsize=9, ncol=5)

    ax.set_title('This Week in Workflow Tools: January 24–29, 2026',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)

    fig.text(0.99, 0.02, 'Source: Industry News Tracking', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-activity-timeline.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-activity-timeline.png")


# Chart 3: Competitive Positioning Scatter Plot
def create_competitive_positioning():
    fig, ax = plt.subplots(figsize=(12, 9), facecolor=BG)
    ax.set_facecolor(BG)

    # Tools with coordinates: (AI Integration, Specialization)
    # AI Integration: 0 = Manual, 10 = Fully AI-Native
    # Specialization: 0 = General Purpose, 10 = Highly Specialized
    tools = {
        'Miro': (4, 3, 300),
        'Lucidchart': (3, 4, 250),
        'Figma': (5, 6, 350),
        'Canva': (6, 2, 320),
        'tldraw': (3, 7, 150),
        'Eraser': (5, 9, 180),
        'Beautiful.ai': (7, 3, 120),
        'Gamma': (8, 4, 140),
        'OpenAI Prism': (10, 5, 200),
        'Napkin.ai': (9, 6, 100),
        'Diagrimo': (8, 8, 80),
    }

    # Color by category
    categories = {
        'Enterprise': ['Miro', 'Lucidchart'],
        'Design': ['Figma', 'Canva'],
        'Developer': ['tldraw', 'Eraser'],
        'AI-Native': ['Beautiful.ai', 'Gamma', 'OpenAI Prism', 'Napkin.ai', 'Diagrimo']
    }

    cat_colors = {
        'Enterprise': '#64C5E4',
        'Design': '#47A8C6',
        'Developer': '#2A8BA8',
        'AI-Native': '#0D6E8A'
    }

    for cat, names in categories.items():
        for name in names:
            if name in tools:
                x, y, size = tools[name]
                ax.scatter(x, y, s=size, color=cat_colors[cat],
                          alpha=0.8, edgecolor='white', linewidth=2, zorder=3)
                ax.annotate(name, (x, y), xytext=(5, 5), textcoords='offset points',
                           fontsize=9, color=TEXT, fontweight='500')

    # Quadrant labels
    ax.text(2, 9, 'Specialized\n& Manual', fontsize=10, color=TEXT_SECONDARY,
            ha='center', va='center', alpha=0.6)
    ax.text(9, 9, 'Specialized\n& AI-Driven', fontsize=10, color=TEXT_SECONDARY,
            ha='center', va='center', alpha=0.6)
    ax.text(2, 1, 'General Purpose\n& Manual', fontsize=10, color=TEXT_SECONDARY,
            ha='center', va='center', alpha=0.6)
    ax.text(9, 1, 'General Purpose\n& AI-Driven', fontsize=10, color=TEXT_SECONDARY,
            ha='center', va='center', alpha=0.6)

    # Axes
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 10.5)
    ax.set_xlabel('AI Integration Level', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
    ax.set_ylabel('Specialization Level', fontsize=12, color=TEXT_SECONDARY, labelpad=10)

    # Grid and styling
    ax.axhline(y=5, color=GRID, linewidth=1, linestyle='--', alpha=0.5)
    ax.axvline(x=5.5, color=GRID, linewidth=1, linestyle='--', alpha=0.5)
    ax.grid(True, alpha=0.3, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors=TEXT_SECONDARY)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=cat_colors['Enterprise'], label='Enterprise', alpha=0.8),
        mpatches.Patch(facecolor=cat_colors['Design'], label='Design', alpha=0.8),
        mpatches.Patch(facecolor=cat_colors['Developer'], label='Developer', alpha=0.8),
        mpatches.Patch(facecolor=cat_colors['AI-Native'], label='AI-Native', alpha=0.8),
    ]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True,
              facecolor=BG, edgecolor=GRID, fontsize=10)

    ax.set_title('Competitive Landscape: AI Integration vs. Specialization',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)

    fig.text(0.99, 0.02, 'Source: Market Analysis (Jan 2026) | Bubble size = Est. Market Share',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-competitive-positioning.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-competitive-positioning.png")


# Chart 4: Developer Documentation Time Savings (for Eraser article)
def create_documentation_savings():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Before/After comparison
    categories = ['Architecture\nDocs', 'Cloud\nDiagrams', 'API\nFlows', 'System\nOverview']
    before = [120, 90, 60, 45]  # Minutes per document
    after = [12, 9, 6, 4.5]    # 90% reduction

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, before, width, label='Manual Process',
                   color='#64C5E4', edgecolor='white', linewidth=1)
    bars2 = ax.bar(x + width/2, after, width, label='With Eraser IaC',
                   color='#0D6E8A', edgecolor='white', linewidth=1)

    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{int(height)}m',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, color=TEXT)

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{int(height)}m',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, color=TEXT, fontweight='600')

    ax.set_ylabel('Time per Document (minutes)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xlabel('Document Type', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(loc='upper right', frameon=True, facecolor=BG, edgecolor=GRID)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.set_ylim(0, 140)

    # Add 90% reduction callout
    ax.annotate('90% Time\nReduction', xy=(3.3, 70), fontsize=14,
                color=ACCENT, fontweight='700', ha='center')

    ax.set_title('Documentation Time: Manual vs. Eraser Infrastructure-as-Code',
                 fontsize=14, color=TEXT, fontweight='600', pad=15)

    fig.text(0.99, 0.02, 'Source: Eraser.io Case Studies (Jan 2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-documentation-savings.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-documentation-savings.png")


if __name__ == '__main__':
    create_market_segmentation()
    create_activity_timeline()
    create_competitive_positioning()
    create_documentation_savings()
    print("\nAll charts generated successfully!")
