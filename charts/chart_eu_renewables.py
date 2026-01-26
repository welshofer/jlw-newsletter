import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme - teal climate theme
ACCENT = '#0D6E8A'
ACCENT_DARK = '#095A70'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
FOSSIL = '#8B7355'  # Brown for fossil fuels

# Data: EU electricity generation share (%)
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
wind_solar = [13, 14, 15, 17, 19, 22, 23, 25, 27, 29, 30]
fossil = [43, 41, 40, 38, 35, 33, 34, 33, 30, 27, 25]

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Plot both lines
ax.plot(years, wind_solar, color=ACCENT, linewidth=3, marker='o', markersize=8, label='Wind & Solar')
ax.plot(years, fossil, color=FOSSIL, linewidth=3, marker='s', markersize=8, label='Fossil Fuels')

# Fill areas for visual impact
ax.fill_between(years, wind_solar, alpha=0.2, color=ACCENT)
ax.fill_between(years, fossil, alpha=0.15, color=FOSSIL)

# Mark the crossover point in 2025
ax.annotate('Historic\nCrossover', xy=(2025, 27.5), xytext=(2023.5, 35),
            fontsize=11, color=ACCENT_DARK, fontweight='600',
            arrowprops=dict(arrowstyle='->', color=ACCENT_DARK, lw=1.5))

# Styling
ax.set_title('EU Electricity: Wind & Solar Surpass Fossil Fuels',
             fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylabel('Share of EU Electricity (%)', fontsize=12, color=TEXT_SECONDARY)
ax.set_xlim(2015, 2025.5)
ax.set_ylim(0, 50)
ax.legend(loc='upper left', framealpha=0.9)
ax.grid(True, alpha=0.5, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Source attribution
fig.text(0.99, 0.02, 'Source: Ember European Electricity Review (Jan 2026)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-eu-renewables.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved successfully")
