import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Newsletter color scheme - deep slate blue
ACCENT = '#3D5A73'
ACCENT_LIGHT = '#5A7A96'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Timeline events - January 2026 Minneapolis
events = [
    ('2026-01-20', 'Judge Menendez issues TRO\nlimiting federal agents', 'judicial'),
    ('2026-01-22', 'Anti-ICE protest at\nSt. Paul church', 'protest'),
    ('2026-01-23', 'DOJ opens investigation\ninto Gov. Walz & Mayor Frey', 'doj'),
    ('2026-01-23', 'Renee Good fatally\nshot by agents', 'shooting'),
    ('2026-01-24', 'Alex Pretti fatally\nshot at protest', 'shooting'),
    ('2026-01-24', 'KKK Act charges filed\nagainst 3 organizers', 'doj'),
    ('2026-01-24', 'ACLU files lawsuits\n(Hussen v. Noem)', 'judicial'),
]

# Parse dates
dates = [datetime.strptime(e[0], '%Y-%m-%d') for e in events]
labels = [e[1] for e in events]
types = [e[2] for e in events]

# Color mapping
color_map = {
    'judicial': '#2E7D32',   # green - courts
    'protest': '#F57C00',    # orange - protests
    'doj': ACCENT,           # slate blue - DOJ
    'shooting': '#C62828',   # red - violence
}
colors = [color_map[t] for t in types]

# Create figure
fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
ax.set_facecolor(BG)

# Plot timeline
levels = np.array([1, -1.2, 1.3, -1, 1.1, -1.3, 1.2])  # Alternate above/below
markerline, stemline, baseline = ax.stem(dates, levels, basefmt=' ')
plt.setp(stemline, color=GRID, linewidth=1.5)

# Plot colored markers separately since stem doesn't support per-marker colors
for i, (d, level, c) in enumerate(zip(dates, levels, colors)):
    ax.plot(d, level, 'o', markersize=10, markerfacecolor=c, markeredgecolor='white', markeredgewidth=2)

# Hide the default markers from stem
plt.setp(markerline, markersize=0)

# Add labels
for i, (d, label, level) in enumerate(zip(dates, labels, levels)):
    va = 'bottom' if level > 0 else 'top'
    y_offset = 0.15 if level > 0 else -0.15
    ax.annotate(label, xy=(d, level), xytext=(0, 25 if level > 0 else -25),
                textcoords='offset points', ha='center', va=va,
                fontsize=9, color=TEXT, fontweight='500',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=GRID, alpha=0.9))

# Formatting
ax.set_title('Five Days That Redefined "Impeding"', fontsize=16, color=TEXT, fontweight='700', pad=30)
ax.set_xlabel('January 2026', fontsize=11, color=TEXT_SECONDARY)
ax.axhline(0, color=ACCENT, linewidth=2)
ax.set_ylim(-2, 2)
ax.yaxis.set_visible(False)

# Format x-axis
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.xticks(rotation=0, fontsize=10, color=TEXT_SECONDARY)

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#2E7D32', markersize=10, label='Judicial'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#F57C00', markersize=10, label='Protest'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=ACCENT, markersize=10, label='DOJ Action'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#C62828', markersize=10, label='Fatal Shooting'),
]
ax.legend(handles=legend_elements, loc='upper right', framealpha=0.9, fontsize=9)

# Remove spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Source
fig.text(0.99, 0.02, 'Source: CBS, MPR, Star Tribune (Jan 2026)', fontsize=8,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/impeding-protest/chart-timeline.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Saved chart-timeline.png")
