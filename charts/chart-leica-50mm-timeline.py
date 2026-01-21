import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Newsletter color scheme
ACCENT = '#B85C38'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'
THIRD_PARTY = '#4A7C59'

# Lens release timeline data
releases = [
    ('1966', 'Noctilux 50/1.2 AA', 'Leica', 'First aspherical'),
    ('1976', 'Summilux 50/1.4 Pre-ASPH', 'Leica', 'Classic "glow"'),
    ('2004', 'Summilux 50/1.4 ASPH', 'Leica', 'Modern reference'),
    ('2008', 'Noctilux 50/0.95', 'Leica', 'Ultimate fast 50'),
    ('2012', 'APO-Summicron 50/2', 'Leica', 'Sharpest 50mm ever'),
    ('2018', 'Voigtlander 50/1.5 II', 'Third-Party', 'Budget champion'),
    ('2023', 'APO-Lanthar 50/3.5 II', 'Third-Party', 'Compact APO'),
    ('2026', 'Light Lens Lab 50/1.2', 'Third-Party', '"1966" replica'),
]

# Parse years and create positions
years = [int(r[0]) for r in releases]
labels = [r[1] for r in releases]
manufacturers = [r[2] for r in releases]
notes = [r[3] for r in releases]
colors = [ACCENT if m == 'Leica' else THIRD_PARTY for m in manufacturers]

# Create figure
fig, ax = plt.subplots(figsize=(14, 6), facecolor=BG)
ax.set_facecolor(BG)

# Create timeline
y_positions = [1 if i % 2 == 0 else -1 for i in range(len(years))]

# Plot markers
for i, (year, label, y, color, note) in enumerate(zip(years, labels, y_positions, colors, notes)):
    # Marker
    ax.scatter(year, 0, s=120, c=color, zorder=5, edgecolors='white', linewidth=2)

    # Vertical line
    ax.plot([year, year], [0, y * 0.4], color=color, linewidth=2, alpha=0.7)

    # Label box
    bbox_props = dict(boxstyle="round,pad=0.3", facecolor=BG, edgecolor=color, linewidth=1.5)
    ax.annotate(f'{label}\n({note})', xy=(year, y * 0.5),
                fontsize=9, ha='center', va='bottom' if y > 0 else 'top',
                color=TEXT, fontweight='500',
                bbox=bbox_props)

# Timeline base
ax.axhline(y=0, color=GRID, linewidth=3, zorder=1)

# Year labels on timeline
for year in years:
    ax.annotate(str(year), xy=(year, -0.08), fontsize=10, ha='center',
                color=TEXT_SECONDARY, fontweight='600')

# Styling
ax.set_xlim(1960, 2030)
ax.set_ylim(-1.5, 1.5)
ax.axis('off')

ax.set_title('Evolution of the M-Mount 50mm: Six Decades of Excellence',
             fontsize=16, color=TEXT, fontweight='600', pad=30,
             fontfamily='serif', loc='center')

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=ACCENT, label='Leica', edgecolor='white'),
                   Patch(facecolor=THIRD_PARTY, label='Third-Party', edgecolor='white')]
ax.legend(handles=legend_elements, loc='upper left', frameon=True,
          facecolor=BG, edgecolor=GRID, fontsize=10, bbox_to_anchor=(0.02, 0.98))

# Source
fig.text(0.99, 0.02, 'Source: Leica Camera AG historical records',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-50mm-timeline.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved to: /Users/welshofer/clawd/jlw-newsletter/images/chart-50mm-timeline.png")
