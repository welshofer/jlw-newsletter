import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Newsletter color scheme - indigo theme for AGI/forecasting
ACCENT = '#5B4B8A'      # Deep indigo
ACCENT_LIGHT = '#7C6BA8'
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
AMBER = '#D4A84B'       # For contrast

# Data: AGI predictions from various sources
predictions = {
    'Amodei\n(Anthropic)': {'optimistic': 2026, 'pessimistic': 2027, 'note': 'Coding in 6-12mo'},
    'Hassabis\n(DeepMind)': {'optimistic': 2028, 'pessimistic': 2032, 'note': '50% by 2030'},
    'AI 2027\nReport': {'optimistic': 2027, 'pessimistic': 2033, 'note': 'Median ~2030'},
    'LeCun\n(Meta)': {'optimistic': 2035, 'pessimistic': 2045, 'note': '"Not soon"'},
    'Chollet\n(ARC-AGI)': {'optimistic': 2030, 'pessimistic': 2040, 'note': 'Scaling not enough'},
}

fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
ax.set_facecolor(BG)

names = list(predictions.keys())
y_pos = np.arange(len(names))

# Create horizontal bar ranges
for i, (name, data) in enumerate(predictions.items()):
    opt = data['optimistic']
    pess = data['pessimistic']
    midpoint = (opt + pess) / 2

    # Range bar
    ax.barh(i, pess - opt, left=opt, height=0.5, color=ACCENT, alpha=0.3, edgecolor=ACCENT, linewidth=1)

    # Optimistic marker
    ax.scatter(opt, i, color=ACCENT, s=120, zorder=5, marker='o')

    # Pessimistic marker
    ax.scatter(pess, i, color=ACCENT_LIGHT, s=120, zorder=5, marker='o')

    # Midpoint marker (filled)
    ax.scatter(midpoint, i, color=AMBER, s=80, zorder=6, marker='D')

ax.set_yticks(y_pos)
ax.set_yticklabels(names, fontsize=11, color=TEXT, fontweight='500')

ax.set_xlabel('Predicted Year of AGI Arrival', fontsize=12, color=TEXT_SECONDARY, labelpad=15)
ax.set_title('AGI Timeline Predictions: The Great Divide\n', fontsize=18, color=TEXT, fontweight='600', pad=20)

# Set x-axis range
ax.set_xlim(2024, 2048)
ax.set_xticks([2025, 2030, 2035, 2040, 2045])

# Grid
ax.xaxis.grid(True, alpha=0.5, color=GRID, linestyle='-')
ax.set_axisbelow(True)

# Remove spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Add vertical line for "now"
ax.axvline(x=2026, color=TEXT_SECONDARY, linestyle='--', alpha=0.5, linewidth=1.5)
ax.annotate('Now\n(Jan 2026)', xy=(2026, len(names)-0.5), fontsize=9, color=TEXT_SECONDARY, ha='center')

# Legend
opt_patch = mpatches.Patch(color=ACCENT, label='Optimistic estimate')
pess_patch = mpatches.Patch(color=ACCENT_LIGHT, label='Pessimistic estimate', alpha=0.6)
mid_marker = plt.Line2D([0], [0], marker='D', color='w', markerfacecolor=AMBER, markersize=10, label='Midpoint')
ax.legend(handles=[opt_patch, pess_patch, mid_marker], loc='lower right', frameon=True,
          facecolor=BG, edgecolor=GRID, fontsize=10)

# Source attribution
fig.text(0.99, 0.02, 'Source: WEF 2026, Investing.com, AI-2027.com, Time, Uncharted Territories (Jan 2026)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-agi-predictions.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-agi-predictions.png")
