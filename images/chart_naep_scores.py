import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#3D4F7C'      # Deep indigo
ACCENT2 = '#B85C38'     # Terracotta
ACCENT3 = '#5C8A5A'     # Sage green
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# NAEP Reading Scores for 4th Grade
years = [2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2022, 2024]
scores_4th = [218, 219, 221, 221, 221, 222, 223, 222, 220, 217, 215]
scores_8th = [263, 262, 263, 264, 265, 268, 265, 267, 263, 260, 258]

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Plot lines
ax.plot(years, scores_4th, color=ACCENT, linewidth=3, marker='o', markersize=7,
        markerfacecolor=BG, markeredgecolor=ACCENT, markeredgewidth=2, label='4th Grade')
ax.plot(years, scores_8th, color=ACCENT2, linewidth=3, marker='s', markersize=7,
        markerfacecolor=BG, markeredgecolor=ACCENT2, markeredgewidth=2, label='8th Grade')

# Highlight the drop
ax.annotate('', xy=(2024, 215), xytext=(2019, 220),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax.annotate('COVID\nSlide', xy=(2021.5, 216), fontsize=10, color='red',
            ha='center', fontweight='600')

# Pre-pandemic baseline
ax.axhline(y=220, color=GRID, linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(2003.5, 220.5, '2019 Pre-pandemic baseline (4th)', fontsize=9,
        color=TEXT_SECONDARY, style='italic')

# Styling
ax.set_title('NAEP Reading Scores: The COVID Cliff', fontsize=18,
             color=TEXT, fontweight='700', pad=20, fontfamily='serif')
ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY, fontweight='500')
ax.set_ylabel('Average Scale Score', fontsize=12, color=TEXT_SECONDARY, fontweight='500')

ax.set_xlim(2002, 2025)
ax.legend(loc='lower left', frameon=False)

ax.grid(True, alpha=0.4, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Callout
ax.text(0.98, 0.25, '2024 scores at\n1971 levels\nfor 13-year-olds',
        transform=ax.transAxes, fontsize=11, color='red',
        ha='right', va='top', fontweight='600',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF5F5', edgecolor='red', alpha=0.9))

# Source
fig.text(0.99, 0.02, 'Source: National Center for Education Statistics (NCES)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-naep-reading-scores.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("Chart saved: chart-naep-reading-scores.png")
