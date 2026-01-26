import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#0D6E8A'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
COAL = '#5C4033'  # Dark brown for coal/thermal
PEAK = '#B85C38'  # Highlight for peak

# Data: China thermal power generation (TWh)
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
thermal_twh = [4100, 4250, 4450, 4850, 5050, 4900, 5200, 5450, 5600, 5650, 5580]

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Color bars - highlight the peak and decline
colors = [COAL if y < 5650 else (PEAK if y == 5650 else ACCENT) for y in thermal_twh]
colors[-1] = ACCENT  # 2025 decline in teal

bars = ax.bar(years, thermal_twh, color=colors, width=0.7, edgecolor='white', linewidth=0.5)

# Mark the peak
ax.annotate('PEAK', xy=(2024, 5650), xytext=(2024, 5850),
            fontsize=12, color=PEAK, fontweight='700', ha='center',
            arrowprops=dict(arrowstyle='->', color=PEAK, lw=2))

# Mark the decline
ax.annotate('First decline\nin 10 years', xy=(2025, 5580), xytext=(2022, 5200),
            fontsize=11, color=ACCENT, fontweight='600',
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

# Styling
ax.set_title("China's Thermal Power Generation Peaks in 2024",
             fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylabel('Thermal Power Generation (TWh)', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylim(0, 6500)
ax.grid(True, alpha=0.5, color=GRID, axis='y')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Source attribution
fig.text(0.99, 0.02, 'Source: Carbon Pulse / Ember (Jan 2026)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-china-thermal.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved successfully")
