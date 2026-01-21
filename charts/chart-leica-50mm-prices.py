import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme - terracotta warm palette
ACCENT = '#B85C38'
ACCENT_LIGHT = '#D4856A'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'
THIRD_PARTY = '#4A7C59'  # Green for third-party

# Data: 50mm M-mount lenses and their prices (USD)
lenses = [
    'Noctilux 50/0.95\n(Leica)',
    'APO-Summicron\n50/2 (Leica)',
    'Summilux 50/1.4\nASPH (Leica)',
    'Summicron 50/2\n(Leica)',
    'Light Lens Lab\n50/1.2 "1966"',
    'Voigtlander\n50/1.5 II',
    'Voigtlander\nAPO-Lanthar 50/3.5',
    '7Artisans\n50/1.1'
]

prices = [13095, 8995, 5095, 2795, 2999, 999, 699, 299]
colors = [ACCENT, ACCENT, ACCENT, ACCENT, THIRD_PARTY, THIRD_PARTY, THIRD_PARTY, THIRD_PARTY]

# Create figure
fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
ax.set_facecolor(BG)

# Create horizontal bar chart
y_pos = np.arange(len(lenses))
bars = ax.barh(y_pos, prices, color=colors, height=0.65, edgecolor='white', linewidth=0.5)

# Add price labels on bars
for i, (bar, price) in enumerate(zip(bars, prices)):
    width = bar.get_width()
    label_x = width - 200 if width > 2000 else width + 100
    color = 'white' if width > 2000 else TEXT
    ha = 'right' if width > 2000 else 'left'
    ax.text(label_x, bar.get_y() + bar.get_height()/2, f'${price:,}',
            va='center', ha=ha, fontsize=11, fontweight='600', color=color)

# Styling
ax.set_yticks(y_pos)
ax.set_yticklabels(lenses, fontsize=10, color=TEXT)
ax.set_xlabel('Price (USD)', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
ax.set_title('50mm M-Mount Lens Prices: Leica vs Third-Party',
             fontsize=16, color=TEXT, fontweight='600', pad=20,
             fontfamily='serif')

# Grid and spines
ax.xaxis.grid(True, alpha=0.5, color=GRID, linestyle='-')
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Format x-axis
ax.set_xlim(0, 14500)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k' if x >= 1000 else f'${x:.0f}'))
ax.tick_params(axis='x', colors=TEXT_SECONDARY)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=ACCENT, label='Leica Branded'),
                   Patch(facecolor=THIRD_PARTY, label='Third-Party')]
ax.legend(handles=legend_elements, loc='lower right', frameon=True,
          facecolor=BG, edgecolor=GRID, fontsize=10)

# Source attribution
fig.text(0.99, 0.02, 'Source: Leica Camera AG, manufacturer websites (Jan 2026)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-50mm-prices.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved to: /Users/welshofer/clawd/jlw-newsletter/images/chart-50mm-prices.png")
