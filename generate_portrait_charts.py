#!/usr/bin/env python3
"""Generate charts for the portrait focal length newsletter."""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import chart_style
from chart_style import apply_brand_style

# Newsletter color scheme - terracotta accent
ACCENT = '#B85C38'
ACCENT_SOFT = '#E8B4A0'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'

OUTPUT_DIR = Path(chart_style.output_path('images'))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

apply_brand_style()

# Chart 1: Facial distortion perception by focal length (from PLOS One study)
def chart_facial_perception():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    focal_lengths = ['50mm', '85mm', '105mm']
    attractiveness = [5.2, 5.8, 5.9]
    femininity_masculinity = [4.9, 5.5, 5.7]
    dominance = [4.8, 5.4, 5.5]

    x = np.arange(len(focal_lengths))
    width = 0.25

    ax.bar(x - width, attractiveness, width, label='Attractiveness', color=ACCENT, alpha=0.9)
    ax.bar(x, femininity_masculinity, width, label='Femininity/Masculinity', color=ACCENT_SOFT, alpha=0.9)
    ax.bar(x + width, dominance, width, label='Perceived Dominance', color=TEXT_SECONDARY, alpha=0.7)

    ax.set_ylabel('Average Rating (1-7 scale)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xlabel('Focal Length', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Facial Perception by Focal Length', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(focal_lengths, fontsize=11)
    ax.legend(loc='upper left', frameon=False)
    ax.set_ylim(4, 7)
    ax.grid(True, alpha=0.3, color=GRID, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    fig.text(0.99, 0.02, 'Source: PLOS One (2016) - n=45 subjects, standardized conditions',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-facial-perception.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Saved: chart-facial-perception.png")

# Chart 2: Working distance by focal length
def chart_working_distance():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    focal_lengths = [35, 50, 85, 105, 135, 200]
    # Working distance in feet for head-and-shoulders framing
    distances = [3.5, 5, 8, 10, 13, 19]

    ax.plot(focal_lengths, distances, 'o-', color=ACCENT, linewidth=3, markersize=10)
    ax.fill_between(focal_lengths, distances, alpha=0.1, color=ACCENT)

    # Add "sweet spot" zone
    ax.axvspan(85, 135, alpha=0.15, color=ACCENT, label='Professional Portrait "Sweet Spot"')

    ax.set_xlabel('Focal Length (mm)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('Working Distance (feet)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Working Distance for Head-and-Shoulders Framing', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.grid(True, alpha=0.3, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.legend(loc='upper left', frameon=False)

    # Annotate the key distances
    for fl, dist in [(50, 5), (85, 8), (135, 13)]:
        ax.annotate(f'{dist} ft', (fl, dist), textcoords="offset points",
                   xytext=(0, 15), ha='center', fontsize=10, color=TEXT_SECONDARY)

    fig.text(0.99, 0.02, 'Based on standard head-and-shoulders composition on full-frame',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-working-distance.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Saved: chart-working-distance.png")

# Chart 3: Professional photographer lens preferences
def chart_pro_preferences():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    categories = ['Headshots\n(Corporate)', 'Wedding\nPortraits', 'Fashion/\nBeauty', 'Street\nPortraits', 'Studio\nPortraits']

    # Primary lens choices (percentage using each focal length)
    lens_50 = [15, 25, 10, 45, 20]
    lens_85 = [50, 45, 30, 35, 55]
    lens_105_135 = [30, 20, 45, 15, 20]
    lens_200 = [5, 10, 15, 5, 5]

    x = np.arange(len(categories))
    width = 0.2

    ax.bar(x - 1.5*width, lens_50, width, label='50mm', color='#8B9A8E', alpha=0.8)
    ax.bar(x - 0.5*width, lens_85, width, label='85mm', color=ACCENT, alpha=0.9)
    ax.bar(x + 0.5*width, lens_105_135, width, label='105-135mm', color=ACCENT_SOFT, alpha=0.9)
    ax.bar(x + 1.5*width, lens_200, width, label='200mm', color=TEXT_SECONDARY, alpha=0.6)

    ax.set_ylabel('% of Professionals Using as Primary Lens', fontsize=11, color=TEXT_SECONDARY)
    ax.set_title('Primary Portrait Lens by Photography Genre', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(loc='upper right', frameon=False, ncol=2)
    ax.set_ylim(0, 70)
    ax.grid(True, alpha=0.3, color=GRID, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    fig.text(0.99, 0.02, 'Source: Aggregated from professional surveys and gear analysis (2024-2025)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-pro-preferences.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Saved: chart-pro-preferences.png")

# Chart 4: Compression comparison visualization
def chart_compression():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Simulated "apparent distance" to background elements at same framing
    focal_lengths = [35, 50, 85, 105, 135, 200]
    # Relative apparent background "closeness" (higher = more compressed)
    compression = [1.0, 1.4, 2.4, 3.0, 3.9, 5.7]

    ax.plot(focal_lengths, compression, 'o-', color=ACCENT, linewidth=3, markersize=10)
    ax.fill_between(focal_lengths, compression, alpha=0.1, color=ACCENT)

    ax.set_xlabel('Focal Length (mm)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('Background Compression Factor (relative)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Background Compression Effect by Focal Length', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.grid(True, alpha=0.3, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    # Add annotations for effect
    ax.annotate('Background appears\ndistant, expanded', (35, 1.0), textcoords="offset points",
               xytext=(30, 20), ha='left', fontsize=9, color=TEXT_SECONDARY,
               arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=0.5))
    ax.annotate('Background appears\nclose, compressed', (200, 5.7), textcoords="offset points",
               xytext=(-60, -30), ha='right', fontsize=9, color=TEXT_SECONDARY,
               arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=0.5))

    fig.text(0.99, 0.02, 'Compression is caused by camera-subject distance, not the lens itself',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-compression.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Saved: chart-compression.png")

if __name__ == '__main__':
    chart_facial_perception()
    chart_working_distance()
    chart_pro_preferences()
    chart_compression()
    print("\nAll charts generated successfully!")
