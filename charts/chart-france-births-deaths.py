import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#B85C38'      # terracotta
BG = '#FDFBF7'          # cream background
TEXT = '#1A1815'        # dark text
TEXT_SECONDARY = '#5C564D'  # secondary text
GRID = '#E5E0D8'        # border/grid
ACCENT_BLUE = '#2C3E50' # slate blue for contrast

# Data: France births vs deaths (millions)
years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
births = [0.753, 0.740, 0.738, 0.723, 0.678, 0.665, 0.640]  # in millions
deaths = [0.613, 0.669, 0.660, 0.667, 0.639, 0.645, 0.655]  # in millions

# Create figure
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Plot lines
ax.plot(years, births, color=ACCENT, linewidth=2.5, marker='o', markersize=8, label='Births')
ax.plot(years, deaths, color=ACCENT_BLUE, linewidth=2.5, marker='s', markersize=8, label='Deaths')

# Fill the area between to show the crossover
ax.fill_between(years, births, deaths, where=[b > d for b, d in zip(births, deaths)],
                alpha=0.2, color=ACCENT, label='Natural increase')
ax.fill_between(years, births, deaths, where=[b <= d for b, d in zip(births, deaths)],
                alpha=0.2, color=ACCENT_BLUE, label='Natural decrease')

# Highlight the crossover point
crossover_x = 2024.8  # approximate
crossover_y = 0.648
ax.annotate('2025: Historic\ncrossover', xy=(2025, 0.647), xytext=(2023.5, 0.580),
            fontsize=10, color=TEXT, fontweight='500',
            arrowprops=dict(arrowstyle='->', color=TEXT, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GRID))

# Styling
ax.set_title('France: When Deaths Overtook Births', fontsize=16, color=TEXT,
             fontweight='600', pad=20, fontfamily='serif')
ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylabel('Population (millions)', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylim(0.55, 0.78)
ax.set_xlim(2018.5, 2025.5)
ax.legend(loc='upper right', frameon=True, facecolor=BG, edgecolor=GRID)

# Grid styling
ax.grid(True, alpha=0.5, color=GRID, linestyle='-', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=TEXT_SECONDARY)

# Source attribution
fig.text(0.99, 0.02, 'Source: INSEE (January 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-france-crossover.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved successfully")
