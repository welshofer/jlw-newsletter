import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#B85C38'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'
THIRD_PARTY = '#4A7C59'

# Lens data: weight (g), max aperture (as f-number), sharpness score, price
# Sharpness is relative score (100 = APO-Summicron reference)
lenses = {
    'APO-Summicron 50/2': {'weight': 300, 'aperture': 2.0, 'sharpness': 100, 'price': 8995, 'brand': 'Leica'},
    'Summilux 50/1.4 ASPH': {'weight': 335, 'aperture': 1.4, 'sharpness': 92, 'price': 5095, 'brand': 'Leica'},
    'Noctilux 50/0.95': {'weight': 700, 'aperture': 0.95, 'sharpness': 85, 'price': 13095, 'brand': 'Leica'},
    'APO-Lanthar 50/3.5 II': {'weight': 162, 'aperture': 3.5, 'sharpness': 98, 'price': 699, 'brand': 'Third-Party'},
    'Voigtlander 50/1.5 II': {'weight': 216, 'aperture': 1.5, 'sharpness': 78, 'price': 999, 'brand': 'Third-Party'},
    'Light Lens Lab 50/1.2': {'weight': 450, 'aperture': 1.2, 'sharpness': 82, 'price': 2999, 'brand': 'Third-Party'},
}

# Create figure
fig, ax = plt.subplots(figsize=(11, 8), facecolor=BG)
ax.set_facecolor(BG)

# Plot each lens
for name, data in lenses.items():
    color = ACCENT if data['brand'] == 'Leica' else THIRD_PARTY
    # Size proportional to price (normalized)
    size = 100 + (data['price'] / 13095) * 400

    scatter = ax.scatter(data['weight'], data['sharpness'],
                         s=size, c=color, alpha=0.7,
                         edgecolors='white', linewidth=2, zorder=5)

    # Label positioning
    offset_x = 15 if data['weight'] < 500 else -15
    ha = 'left' if data['weight'] < 500 else 'right'
    offset_y = 5 if data['sharpness'] > 90 else -8

    # Aperture in label
    short_name = name.split('/')[0].replace('APO-', '').replace(' II', '')
    label = f'{short_name}\nf/{data["aperture"]}'

    ax.annotate(label, (data['weight'], data['sharpness']),
                xytext=(offset_x, offset_y), textcoords='offset points',
                fontsize=9, color=TEXT, ha=ha, fontweight='500',
                bbox=dict(boxstyle='round,pad=0.2', facecolor=BG, edgecolor=GRID, alpha=0.9))

# Styling
ax.set_xlabel('Weight (grams)', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
ax.set_ylabel('Optical Performance Score', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
ax.set_title('The 50mm Paradox: Smaller Isn\'t Always Sharper\n(but sometimes it is)',
             fontsize=15, color=TEXT, fontweight='600', pad=20,
             fontfamily='serif')

# Grid
ax.grid(True, alpha=0.5, color=GRID)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Axis limits
ax.set_xlim(100, 800)
ax.set_ylim(70, 105)

# Add annotation for APO-Lanthar
ax.annotate('', xy=(162, 98), xytext=(250, 75),
            arrowprops=dict(arrowstyle='->', color=THIRD_PARTY, lw=1.5))
ax.text(255, 74, 'Best performance-to-weight\nratio in the segment',
        fontsize=9, color=THIRD_PARTY, style='italic')

# Legend with size reference
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [
    Patch(facecolor=ACCENT, label='Leica', edgecolor='white'),
    Patch(facecolor=THIRD_PARTY, label='Third-Party', edgecolor='white'),
    Line2D([0], [0], marker='o', color=BG, markerfacecolor='gray',
           markersize=8, label='Bubble size = Price'),
]
ax.legend(handles=legend_elements, loc='lower right', frameon=True,
          facecolor=BG, edgecolor=GRID, fontsize=10)

# Source
fig.text(0.99, 0.02, 'Source: Manufacturer specs, Lenstip resolution tests (Jan 2026)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-50mm-size-performance.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved to: /Users/welshofer/clawd/jlw-newsletter/images/chart-50mm-size-performance.png")
