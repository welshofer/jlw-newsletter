import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#0D6E8A'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
TARGET = '#2E8B57'  # Green for targets

# Data: EU emissions reduction pathway (indexed to 1990 = 100)
years_actual = [1990, 2000, 2010, 2020, 2025]
emissions_actual = [100, 93, 86, 68, 60]

years_target = [2025, 2030, 2040, 2050]
emissions_target = [60, 45, 10, 0]

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Plot actual emissions
ax.plot(years_actual, emissions_actual, color=TEXT, linewidth=3, marker='o',
        markersize=10, label='Actual Emissions', zorder=3)

# Plot target pathway
ax.plot(years_target, emissions_target, color=TARGET, linewidth=3, linestyle='--',
        marker='D', markersize=10, label='Target Pathway', zorder=2)

# Fill areas
ax.fill_between(years_actual, emissions_actual, alpha=0.1, color=TEXT)
ax.fill_between(years_target, emissions_target, alpha=0.15, color=TARGET)

# Annotate key milestones
ax.annotate('2030: -55%', xy=(2030, 45), xytext=(2032, 55),
            fontsize=11, color=TARGET, fontweight='600')
ax.annotate('2040: -90%\n(Just approved)', xy=(2040, 10), xytext=(2035, 25),
            fontsize=11, color=ACCENT, fontweight='700',
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=2))
ax.annotate('2050: Net Zero', xy=(2050, 0), xytext=(2045, 15),
            fontsize=11, color=TARGET, fontweight='600')

# Styling
ax.set_title("EU Emissions Pathway: The Road to Net Zero",
             fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylabel('Emissions (% of 1990 levels)', fontsize=12, color=TEXT_SECONDARY)
ax.set_xlim(1985, 2055)
ax.set_ylim(-5, 110)
ax.axhline(y=0, color=GRID, linestyle='-', linewidth=1)
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.5, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Source attribution
fig.text(0.99, 0.02, 'Source: European Parliament (Jan 2026)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-eu-emissions.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved successfully")
