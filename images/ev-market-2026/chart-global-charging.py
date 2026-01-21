import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#0066CC'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Data: Global EV charging infrastructure (end of 2025, approximate)
regions = ['China', 'Europe', 'United States', 'Rest of World']
chargers = [20.09, 0.73, 0.19, 0.35]  # in millions
colors = [ACCENT, '#4DA6CC', '#80C4E0', '#B3DCF0']

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=BG)

# PIE CHART (left)
ax1.set_facecolor(BG)
wedges, texts, autotexts = ax1.pie(chargers, labels=regions, autopct='%1.1f%%',
                                    colors=colors, startangle=90,
                                    explode=(0.05, 0, 0, 0),  # Explode China slice
                                    textprops={'color': TEXT, 'fontsize': 11})
autotexts[0].set_fontweight('bold')
autotexts[0].set_fontsize(14)
ax1.set_title('Global EV Charging Share', fontsize=14, color=TEXT, fontweight='600', pad=15)

# BAR CHART (right) - more dramatic visual
ax2.set_facecolor(BG)
y_pos = np.arange(len(regions))
bars = ax2.barh(y_pos, chargers, color=colors, height=0.6, edgecolor='white', linewidth=0.5)

# Add value labels
for bar, val in zip(bars, chargers):
    ax2.text(val + 0.2, bar.get_y() + bar.get_height()/2,
            f'{val}M', ha='left', va='center', fontsize=12, fontweight='600', color=TEXT)

ax2.set_yticks(y_pos)
ax2.set_yticklabels(regions, fontsize=11, color=TEXT)
ax2.set_xlabel('Charging Points (Millions)', fontsize=11, color=TEXT_SECONDARY)
ax2.set_title('Charging Points by Region', fontsize=14, color=TEXT, fontweight='600', pad=15)
ax2.set_xlim(0, 24)

# Grid
ax2.grid(True, axis='x', alpha=0.5, color=GRID, linestyle='-', linewidth=0.5)
ax2.set_axisbelow(True)

# Remove spines
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color(GRID)
ax2.spines['bottom'].set_color(GRID)
ax2.tick_params(colors=TEXT_SECONDARY)

# Main title
fig.suptitle("China Dominates Global EV Charging Infrastructure (2025)",
             fontsize=18, color=TEXT, fontweight='700', y=1.02)

# Source attribution
fig.text(0.99, 0.02, 'Source: Metal.com / National Energy Administration (Jan 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/ev-market-2026/chart-global-charging.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved successfully!")
