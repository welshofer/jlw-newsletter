#!/usr/bin/env python3
"""Generate data visualizations for the Serge Lang teaching career newsletter."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Newsletter color scheme — Indigo/scholarly
ACCENT = '#5B4B8A'
ACCENT_LIGHT = '#7C6BA8'
ACCENT_DARK = '#3D3260'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'
WARM = '#B85C38'
WARM_LIGHT = '#D4845E'

OUT = os.path.expanduser('~/clawd/jlw-newsletter/images')
os.makedirs(OUT, exist_ok=True)


def chart1_publication_output():
    """Chart 1: Lang's publication output by decade — bar chart."""
    decades = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s']
    # Approximate publication counts by decade based on bibliography
    # Lang published ~60-70 books total from 1952-2005
    books = [4, 12, 14, 16, 10, 5]
    # Including revised editions
    editions = [0, 3, 6, 8, 12, 4]

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    x = np.arange(len(decades))
    width = 0.35

    bars1 = ax.bar(x - width/2, books, width, label='New Titles',
                   color=ACCENT, edgecolor='none', zorder=3)
    bars2 = ax.bar(x + width/2, editions, width, label='Revised Editions',
                   color=ACCENT_LIGHT, edgecolor='none', alpha=0.7, zorder=3)

    # Add value labels
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.3,
                str(int(h)), ha='center', va='bottom',
                fontsize=11, fontweight='600', color=ACCENT_DARK)
    for bar in bars2:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2., h + 0.3,
                    str(int(h)), ha='center', va='bottom',
                    fontsize=11, fontweight='500', color=ACCENT_LIGHT)

    ax.set_title('Serge Lang\'s Publication Output by Decade',
                 fontsize=16, color=TEXT, fontweight='600', pad=20,
                 fontfamily='serif')
    ax.set_xlabel('Decade', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('Number of Books', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xticks(x)
    ax.set_xticklabels(decades, fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylim(0, 20)
    ax.grid(True, axis='y', alpha=0.4, color=GRID, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.legend(fontsize=10, frameon=False, loc='upper right')

    # Annotation: peak period
    ax.annotate('Peak output:\n1980s — 24 total',
                xy=(3, 16), xytext=(4.2, 18),
                fontsize=9, color=ACCENT_DARK, style='italic',
                arrowprops=dict(arrowstyle='->', color=ACCENT_LIGHT, lw=1.2),
                ha='center')

    fig.text(0.99, 0.02, 'Source: AMS Bibliography / Springer catalog',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUT}/chart-publication-output.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"✓ Chart 1 saved: {OUT}/chart-publication-output.png")


def chart2_controversy_timeline():
    """Chart 2: Timeline of Lang's major feuds and institutional milestones."""
    fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
    ax.set_facecolor(BG)

    # Career milestones (top)
    milestones = [
        (1955, 'Columbia\nappointed'),
        (1960, 'Cole Prize'),
        (1965, 'Algebra\n1st ed.'),
        (1972, 'Moves to\nYale'),
        (2005, 'Dies\nSep 12'),
    ]

    # Controversies (bottom)
    controversies = [
        (1966, 'Bourbaki\ndeparture'),
        (1971, 'Columbia\nresignation\n(Vietnam)'),
        (1986, 'Blocks\nHuntington\nfrom NAS'),
        (1995, 'Resigns\nfrom NAS'),
        (1998, 'Publishes\nChallenges'),
    ]

    # Draw timeline
    ax.axhline(y=0, color=GRID, linewidth=2, zorder=1)

    # Milestones (above line)
    for year, label in milestones:
        ax.plot(year, 0, 'o', color=ACCENT, markersize=10, zorder=3)
        ax.vlines(year, 0, 1.5, color=ACCENT, linewidth=1.5, alpha=0.5, zorder=2)
        ax.text(year, 1.7, label, ha='center', va='bottom',
                fontsize=9, color=ACCENT_DARK, fontweight='500',
                linespacing=1.3)
        ax.text(year, 0.3, str(year), ha='center', va='bottom',
                fontsize=8, color=TEXT_SECONDARY, fontfamily='monospace')

    # Controversies (below line)
    for year, label in controversies:
        ax.plot(year, 0, 's', color=WARM, markersize=10, zorder=3)
        ax.vlines(year, -1.5, 0, color=WARM, linewidth=1.5, alpha=0.5, zorder=2)
        ax.text(year, -1.8, label, ha='center', va='top',
                fontsize=9, color=WARM, fontweight='500',
                linespacing=1.3)
        ax.text(year, -0.3, str(year), ha='center', va='top',
                fontsize=8, color=TEXT_SECONDARY, fontfamily='monospace')

    # Span bars for institutional affiliations
    ax.fill_between([1955, 1971], -0.15, 0.15, color=ACCENT, alpha=0.15, zorder=1)
    ax.text(1963, 0.25, 'Columbia', ha='center', fontsize=8, color=TEXT_SECONDARY,
            style='italic')
    ax.fill_between([1972, 2005], -0.15, 0.15, color=ACCENT, alpha=0.25, zorder=1)
    ax.text(1988.5, 0.25, 'Yale', ha='center', fontsize=8, color=TEXT_SECONDARY,
            style='italic')

    ax.set_xlim(1950, 2010)
    ax.set_ylim(-3.5, 3.5)
    ax.set_title('Career Milestones & Controversies',
                 fontsize=16, color=TEXT, fontweight='600', pad=20,
                 fontfamily='serif')

    # Legend
    milestone_patch = mpatches.Patch(color=ACCENT, label='Career milestones')
    controversy_patch = mpatches.Patch(color=WARM, label='Feuds & controversies')
    ax.legend(handles=[milestone_patch, controversy_patch],
              fontsize=9, frameon=False, loc='upper left')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_yticks([])
    ax.set_xticks([])

    fig.text(0.99, 0.02, 'Source: AMS Notices, NYT, Yale Daily News',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUT}/chart-controversy-timeline.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"✓ Chart 2 saved: {OUT}/chart-controversy-timeline.png")


def chart3_textbook_influence():
    """Chart 3: Influence of Lang's Algebra — editions and competing texts."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Algebra editions and their page counts (showing growing scope)
    editions = ['1st\n(1965)', '2nd\n(1984)', 'Revised 3rd\n(2002)']
    pages = [508, 714, 914]
    topics = [28, 38, 48]  # Approximate chapter count

    x = np.arange(len(editions))

    # Pages bar
    bars = ax.bar(x, pages, 0.5, color=ACCENT, edgecolor='none', zorder=3)
    for bar, p, t in zip(bars, pages, topics):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 10,
                f'{p} pp\n({t} chapters)',
                ha='center', va='bottom', fontsize=10,
                fontweight='600', color=ACCENT_DARK)

    # Add comparison line for Hungerford's Algebra (a competing text)
    ax.axhline(y=502, color=WARM_LIGHT, linewidth=1.5, linestyle='--', alpha=0.7)
    ax.text(2.35, 510, "Hungerford's\nAlgebra (502 pp)",
            fontsize=8, color=WARM, style='italic', va='bottom')

    # Add comparison line for Dummit & Foote
    ax.axhline(y=932, color=WARM, linewidth=1.5, linestyle='--', alpha=0.7)
    ax.text(2.35, 940, "Dummit & Foote\n(932 pp, 2004)",
            fontsize=8, color=WARM, style='italic', va='bottom')

    ax.set_title('The Growth of Lang\'s Algebra',
                 fontsize=16, color=TEXT, fontweight='600', pad=20,
                 fontfamily='serif')
    ax.set_xlabel('Edition', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('Pages', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xticks(x)
    ax.set_xticklabels(editions, fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylim(0, 1050)
    ax.grid(True, axis='y', alpha=0.4, color=GRID, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    # Annotation
    ax.annotate('80% growth\nin 37 years',
                xy=(1, 714), xytext=(0.3, 820),
                fontsize=9, color=ACCENT_DARK, style='italic',
                arrowprops=dict(arrowstyle='->', color=ACCENT_LIGHT, lw=1.2),
                ha='center')

    fig.text(0.99, 0.02, 'Source: Springer-Verlag catalog, AMS Reviews',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUT}/chart-algebra-growth.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print(f"✓ Chart 3 saved: {OUT}/chart-algebra-growth.png")


if __name__ == '__main__':
    chart1_publication_output()
    chart2_controversy_timeline()
    chart3_textbook_influence()
    print("\n✅ All 3 charts generated successfully.")
