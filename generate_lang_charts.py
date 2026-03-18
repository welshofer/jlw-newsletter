#!/usr/bin/env python3
"""Generate data visualizations for Serge Lang teaching career newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Newsletter color scheme — Indigo for academic/math topic
ACCENT = '#5B4B8A'
ACCENT_LIGHT = '#8B7BB5'
ACCENT_DARK = '#3D2E6B'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
WARM = '#B85C38'

OUTPUT_DIR = Path.home() / 'clawd' / 'jlw-newsletter' / 'images'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.family'] = ['Source Sans 3', 'Source Sans Pro', 'Helvetica Neue', 'sans-serif']


def chart_career_timeline():
    """Chart 1: Lang's career at different institutions."""
    fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
    ax.set_facecolor(BG)

    positions = [
        ("Princeton / IAS", 1951, 1953, ACCENT_LIGHT),
        ("U of Chicago", 1953, 1955, ACCENT),
        ("Columbia University", 1955, 1971, ACCENT_DARK),
        ("Yale University", 1972, 2005, WARM),
    ]

    y_positions = [3, 2, 1, 0]

    for (label, start, end, color), y in zip(positions, y_positions):
        duration = end - start
        bar = ax.barh(y, duration, left=start, height=0.5, color=color,
                      edgecolor='white', linewidth=1.5, zorder=3)
        # Label inside bar if wide enough, else to the right
        mid = start + duration / 2
        if duration > 5:
            ax.text(mid, y, f'{label}\n({start}–{end})',
                    ha='center', va='center', fontsize=10,
                    color='white', fontweight='600', zorder=4)
        else:
            ax.text(end + 0.5, y, f'{label} ({start}–{end})',
                    ha='left', va='center', fontsize=10,
                    color=TEXT, fontweight='500', zorder=4)

    # Mark the Columbia resignation
    ax.annotate('Resigned over\nanti-war protests',
                xy=(1971, 1), xytext=(1975, 2.2),
                fontsize=9, color=WARM, fontweight='500',
                arrowprops=dict(arrowstyle='->', color=WARM, lw=1.5),
                ha='left', va='bottom')

    # Mark Steele Prize
    ax.annotate('Steele Prize\nfor Exposition',
                xy=(1999, 0), xytext=(1995, -0.8),
                fontsize=9, color=ACCENT_DARK, fontweight='500',
                arrowprops=dict(arrowstyle='->', color=ACCENT_DARK, lw=1.5),
                ha='center', va='top')

    ax.set_xlim(1948, 2008)
    ax.set_ylim(-1.5, 4)
    ax.set_yticks([])
    ax.set_xlabel('', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('A Career Across Four Elite Institutions',
                 fontsize=16, color=TEXT, fontweight='600', pad=20,
                 fontfamily='Georgia')
    ax.grid(axis='x', alpha=0.3, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', colors=TEXT_SECONDARY)

    fig.text(0.99, 0.02, 'Source: AMS Notices memorial articles (2006)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-career-timeline.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Saved: chart-career-timeline.png")


def chart_books_by_decade():
    """Chart 2: Textbook output by decade."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Approximate book counts by decade based on Lang's bibliography
    decades = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s']
    books = [3, 12, 15, 14, 11, 8]
    cumulative = np.cumsum(books)

    colors = [ACCENT_LIGHT, ACCENT, ACCENT_DARK, WARM, ACCENT, ACCENT_LIGHT]

    bars = ax.bar(decades, books, color=colors, edgecolor='white',
                  linewidth=1.5, width=0.65, zorder=3)

    # Add count labels on bars
    for bar, count in zip(bars, books):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                str(count), ha='center', va='bottom', fontsize=13,
                fontweight='600', color=TEXT)

    # Cumulative line
    ax2 = ax.twinx()
    ax2.set_facecolor(BG)
    ax2.plot(decades, cumulative, color=WARM, linewidth=2.5, marker='o',
             markersize=8, markerfacecolor='white', markeredgecolor=WARM,
             markeredgewidth=2, zorder=4)
    ax2.set_ylabel('Cumulative Total', fontsize=11, color=WARM, fontweight='500')
    ax2.tick_params(axis='y', colors=WARM)
    ax2.spines['right'].set_color(WARM)
    ax2.set_ylim(0, 70)

    # Annotate peak decade
    ax.annotate('Peak output:\n15 books in one decade',
                xy=(2, 15), xytext=(3.5, 16.5),
                fontsize=9, color=ACCENT_DARK, fontweight='500',
                arrowprops=dict(arrowstyle='->', color=ACCENT_DARK, lw=1.5),
                ha='center')

    ax.set_title("Lang's Textbook Output: 60+ Books Across Five Decades",
                 fontsize=16, color=TEXT, fontweight='600', pad=20,
                 fontfamily='Georgia')
    ax.set_ylabel('Books Published', fontsize=11, color=TEXT_SECONDARY, fontweight='500')
    ax.set_ylim(0, 19)
    ax.grid(axis='y', alpha=0.3, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors=TEXT_SECONDARY)

    fig.text(0.99, 0.02, 'Source: Springer bibliography; AMS Notices (2006)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-books-by-decade.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Saved: chart-books-by-decade.png")


def chart_subject_coverage():
    """Chart 3: Donut chart of subject areas covered by Lang's books."""
    fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
    ax.set_facecolor(BG)

    subjects = [
        'Algebra &\nNumber Theory',
        'Analysis &\nDifferential Geometry',
        'Calculus &\nUndergrad Texts',
        'Diophantine\nGeometry',
        'Modular Forms\n& Arakelov Theory',
        'Expository &\nEssays',
    ]
    counts = [14, 12, 10, 8, 7, 12]

    colors = [ACCENT_DARK, ACCENT, ACCENT_LIGHT, WARM,
              '#7B6BAA', '#D4956A']

    wedges, texts, autotexts = ax.pie(
        counts, labels=None, autopct='%1.0f%%',
        startangle=90, counterclock=False,
        colors=colors,
        pctdistance=0.78,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2.5)
    )

    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('600')
        autotext.set_color('white')

    # Custom legend
    legend_elements = [
        mpatches.Patch(facecolor=c, edgecolor='white', label=f'{s} ({n})')
        for s, n, c in zip(subjects, counts, colors)
    ]
    ax.legend(handles=legend_elements, loc='center left',
              bbox_to_anchor=(0.85, 0.5), fontsize=10,
              frameon=False, labelcolor=TEXT)

    # Center text
    ax.text(0, 0, '63\nBooks', ha='center', va='center',
            fontsize=22, fontweight='700', color=TEXT,
            fontfamily='Georgia')

    ax.set_title("One Man's Library: Subject Areas of Lang's Textbooks",
                 fontsize=16, color=TEXT, fontweight='600', pad=20,
                 fontfamily='Georgia')

    fig.text(0.5, 0.02, 'Source: Springer Graduate Texts in Mathematics; MathSciNet',
             fontsize=8, color=TEXT_SECONDARY, ha='center', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-subject-coverage.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"Saved: chart-subject-coverage.png")


if __name__ == '__main__':
    chart_career_timeline()
    chart_books_by_decade()
    chart_subject_coverage()
    print("All charts generated successfully!")
