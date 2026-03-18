import matplotlib.pyplot as plt
import numpy as np

ACCENT = '#5B6B4A'
ACCENT2 = '#8B4513'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SEC = '#5C564D'
GRID = '#E5E0D8'

categories = ['Troops\n(thousands)', 'Tanks &\nAssault Guns', 'Artillery\nPieces', 'Aircraft\n(available)']

# Initial strengths Dec 16, 1944
german = [200, 600, 1900, 1000]
american = [83, 400, 400, 0]  # 0 aircraft operational (grounded by weather)

# Normalize for display (different scales)
fig, axes = plt.subplots(1, 4, figsize=(14, 5), facecolor=BG)

for i, (ax, cat, g, a) in enumerate(zip(axes, categories, german, american)):
    ax.set_facecolor(BG)

    bars = ax.barh([0.6, -0.1], [g, a], height=0.5,
                   color=[ACCENT2, ACCENT], edgecolor='white', linewidth=0.5)

    ax.set_title(cat, fontsize=11, color=TEXT, fontweight='600', pad=10, fontfamily='serif')
    ax.set_yticks([0.6, -0.1])
    ax.set_yticklabels(['Germany', 'U.S.'], fontsize=10, color=TEXT_SEC)
    ax.set_xlim(0, max(g, a) * 1.35)

    # Value labels
    for bar, val in zip(bars, [g, a]):
        w = bar.get_width()
        label = f'{val:,}' if val > 0 else 'Grounded'
        ax.text(w + max(g, a)*0.03, bar.get_y() + bar.get_height()/2.,
                label, ha='left', va='center', fontsize=10,
                color=TEXT, fontweight='500')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.tick_params(bottom=False, labelbottom=False)
    ax.grid(False)

fig.suptitle('Opening Day Force Comparison — December 16, 1944',
             fontsize=16, color=TEXT, fontweight='600', y=1.02, fontfamily='serif')

fig.text(0.99, -0.02,
         'Source: MacDonald, A Time for Trumpets (1985); Cole, The Ardennes (1965)',
         fontsize=8, color=TEXT_SEC, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-force-comparison.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-force-comparison.png")
