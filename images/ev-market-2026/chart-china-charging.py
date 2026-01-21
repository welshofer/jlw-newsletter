import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme - electric blue/teal for EV theme
ACCENT = '#0066CC'      # Electric blue
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Data: China's charging network growth
years = ['2021', '2022', '2023', '2024', '2025']
total_chargers = [2.62, 5.21, 8.59, 13.42, 20.09]  # in millions

# Create figure
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Create bars
bars = ax.bar(years, total_chargers, color=ACCENT, width=0.6, edgecolor='white', linewidth=0.5)

# Add value labels on bars
for bar, val in zip(bars, total_chargers):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val}M', ha='center', va='bottom', fontsize=12, fontweight='600', color=TEXT)

# Styling
ax.set_title("China's EV Charging Network Explosion", fontsize=18, color=TEXT, fontweight='700', pad=20)
ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylabel('Total Charging Points (Millions)', fontsize=12, color=TEXT_SECONDARY)

# Y-axis
ax.set_ylim(0, 24)
ax.yaxis.set_major_locator(plt.MultipleLocator(5))

# Grid
ax.grid(True, axis='y', alpha=0.5, color=GRID, linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)

# Remove spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Tick colors
ax.tick_params(colors=TEXT_SECONDARY)

# Add annotation for 2025 growth
ax.annotate('+49.7% YoY', xy=(4, 20.09), xytext=(4, 22.5),
            fontsize=11, ha='center', color=ACCENT, fontweight='600',
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

# Source attribution
fig.text(0.99, 0.02, 'Source: National Energy Administration (Jan 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/ev-market-2026/chart-china-charging.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved successfully!")
