import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#0066CC'
ACCENT_LIGHT = '#66B2FF'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
WARNING = '#CC3300'  # Red for US

# Data
countries = ['United States', 'European Union', 'Canada\n(Old Policy)', 'Canada\n(New Deal)']
tariffs = [100, 35, 100, 6.1]
colors = [WARNING, ACCENT_LIGHT, WARNING, ACCENT]

# Create figure
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Create horizontal bars
y_pos = np.arange(len(countries))
bars = ax.barh(y_pos, tariffs, color=colors, height=0.6, edgecolor='white', linewidth=0.5)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, tariffs)):
    label = f'{val}%'
    if i == 3:  # Canada new deal - highlight the reduction
        label = f'{val}%  ↓'
    ax.text(val + 2, bar.get_y() + bar.get_height()/2,
            label, ha='left', va='center', fontsize=13, fontweight='600',
            color=colors[i])

# Styling
ax.set_title('Tariffs on Chinese EV Imports by Region', fontsize=18, color=TEXT, fontweight='700', pad=20)
ax.set_xlabel('Import Tariff Rate (%)', fontsize=12, color=TEXT_SECONDARY)
ax.set_yticks(y_pos)
ax.set_yticklabels(countries, fontsize=11, color=TEXT)

# X-axis
ax.set_xlim(0, 120)
ax.xaxis.set_major_locator(plt.MultipleLocator(25))

# Grid
ax.grid(True, axis='x', alpha=0.5, color=GRID, linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)

# Remove spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Tick colors
ax.tick_params(colors=TEXT_SECONDARY)

# Add annotation box
bbox_props = dict(boxstyle="round,pad=0.5", facecolor=ACCENT, alpha=0.1, edgecolor=ACCENT)
ax.text(75, 0.5, '94% reduction\nin tariff rate', fontsize=10, ha='center', va='center',
        bbox=bbox_props, color=ACCENT, fontweight='600')

# Source attribution
fig.text(0.99, 0.02, 'Source: BNN Bloomberg (Jan 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/ev-market-2026/chart-tariff-comparison.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved successfully!")
