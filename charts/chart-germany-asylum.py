import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#B85C38'      # terracotta
BG = '#FDFBF7'          # cream background
TEXT = '#1A1815'        # dark text
TEXT_SECONDARY = '#5C564D'  # secondary text
GRID = '#E5E0D8'        # border/grid
ACCENT_BLUE = '#2C3E50' # slate blue

# Data: Germany asylum applications (thousands)
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
applications = [476, 745, 222, 186, 166, 122, 190, 244, 352, 230, 115]  # in thousands

# Create figure
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Plot area chart
ax.fill_between(years, applications, alpha=0.3, color=ACCENT_BLUE)
ax.plot(years, applications, color=ACCENT_BLUE, linewidth=2.5, marker='o', markersize=6)

# Highlight key moments
ax.annotate('2015-16\nMigration crisis', xy=(2015.5, 600), fontsize=9, color=TEXT,
            ha='center', fontweight='500',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GRID))

ax.annotate('2025: Decade low\n(115K applications)', xy=(2025, 115), xytext=(2022, 80),
            fontsize=10, color='#2E7D32', fontweight='500',
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor='#2E7D32'))

# Styling
ax.set_title('Germany: Asylum Applications Hit 10-Year Low', fontsize=16,
             color=TEXT, fontweight='600', pad=20, fontfamily='serif')
ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylabel('Applications (thousands)', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylim(0, 800)
ax.set_xlim(2014, 2026)

# Grid styling
ax.grid(True, alpha=0.5, color=GRID, linestyle='-', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=TEXT_SECONDARY)

# Source attribution
fig.text(0.99, 0.02, 'Source: German Federal Ministry of Interior (January 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-germany-asylum.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved successfully")
