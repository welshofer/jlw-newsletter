import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme - deep indigo accent for literacy theme
ACCENT = '#3D4F7C'      # Deep indigo
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'        # Dark text
TEXT_SECONDARY = '#4D5C6A'  # Secondary text
GRID = '#D8E2E8'        # Grid lines

# Historical illiteracy data (percentage who cannot read/write)
years = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1979]
illiteracy_rates = [10.7, 7.7, 6.0, 4.3, 2.9, 2.1, 1.8, 1.0, 0.6]

# Create figure
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Plot line
ax.plot(years, illiteracy_rates, color=ACCENT, linewidth=3, marker='o', markersize=8,
        markerfacecolor=BG, markeredgecolor=ACCENT, markeredgewidth=2)

# Fill under the curve
ax.fill_between(years, illiteracy_rates, alpha=0.15, color=ACCENT)

# Add data labels
for i, (year, rate) in enumerate(zip(years, illiteracy_rates)):
    offset = 0.8 if rate > 2 else 0.3
    ax.annotate(f'{rate}%', (year, rate + offset), ha='center', fontsize=10,
                color=ACCENT, fontweight='600')

# Styling
ax.set_title('The Vanishing of "Basic" Illiteracy: 1900-1979', fontsize=18,
             color=TEXT, fontweight='700', pad=20, fontfamily='serif')
ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY, fontweight='500')
ax.set_ylabel('Illiteracy Rate (%)', fontsize=12, color=TEXT_SECONDARY, fontweight='500')
ax.set_xlim(1895, 1985)
ax.set_ylim(0, 13)

ax.grid(True, alpha=0.5, color=GRID, linestyle='-', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Add annotation
ax.annotate('Census definition: "Cannot sign own name"', xy=(1940, 2.9), xytext=(1955, 6),
            fontsize=10, color=TEXT_SECONDARY, style='italic',
            arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1))

# Source attribution
fig.text(0.99, 0.02, 'Source: U.S. Census Bureau', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-illiteracy-century.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("Chart saved: chart-illiteracy-century.png")
