import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#B85C38'      # terracotta
BG = '#FDFBF7'          # cream background
TEXT = '#1A1815'        # dark text
TEXT_SECONDARY = '#5C564D'  # secondary text
GRID = '#E5E0D8'        # border/grid
ACCENT_BLUE = '#2C3E50' # slate blue

# Data: Canary Islands irregular arrivals
years = ['2020', '2021', '2022', '2023', '2024', '2025']
arrivals = [23023, 22316, 15682, 39910, 47000, 17788]  # actual data from research

# Create figure
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Create bars with conditional coloring
colors = [ACCENT_BLUE if a < 30000 else ACCENT for a in arrivals]
colors[-1] = '#2E7D32'  # Green for 2025 success

bars = ax.bar(years, arrivals, color=colors, width=0.6, edgecolor='white', linewidth=1)

# Add value labels on bars
for bar, arrival in zip(bars, arrivals):
    height = bar.get_height()
    label = f'{arrival:,}'
    ax.annotate(label,
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=10, fontweight='500', color=TEXT)

# Add percentage drop annotation
ax.annotate('−62%', xy=(5, 20000), fontsize=24, fontweight='700', color='#2E7D32',
            ha='center', va='bottom')
ax.annotate('from 2024 peak', xy=(5, 16000), fontsize=10, color=TEXT_SECONDARY,
            ha='center', va='top')

# Styling
ax.set_title('Canary Islands: Atlantic Route Arrivals Plummet', fontsize=16,
             color=TEXT, fontweight='600', pad=20, fontfamily='serif')
ax.set_ylabel('Irregular arrivals', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylim(0, 55000)

# Grid styling
ax.grid(True, alpha=0.5, color=GRID, linestyle='-', linewidth=0.5, axis='y')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=TEXT_SECONDARY)

# Source attribution
fig.text(0.99, 0.02, 'Source: Spanish Ministry of Interior (January 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-canary-drop.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved successfully")
