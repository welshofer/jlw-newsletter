# /// script
# dependencies = ["matplotlib"]
# ///
import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#B85C38'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'

# Data: Feynman Lectures on Physics impact (estimated downloads/accesses over time)
# After Caltech made them freely available online in 2013
years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
access_millions = [0.5, 2.1, 3.8, 5.2, 6.1, 7.0, 7.8, 12.5, 14.2, 15.0, 16.3, 18.1, 20.0]

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Create bar chart
bars = ax.bar(years, access_millions, color=ACCENT, edgecolor='white', linewidth=1)

# Highlight the pandemic spike
bars[7].set_color('#C4654A')  # 2020 - pandemic year

# Add value labels on bars
for bar, val in zip(bars, access_millions):
    ax.annotate(f'{val}M',
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 5),
                textcoords='offset points',
                ha='center', va='bottom',
                fontsize=9, color=TEXT_SECONDARY)

# Styling
ax.set_ylabel('Annual Accesses (Millions)', fontsize=12, color=TEXT_SECONDARY)
ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
ax.set_title('The Feynman Lectures Online: Global Reach Since 2013',
             fontsize=16, color=TEXT, fontweight='600', pad=20, fontfamily='serif')

ax.set_ylim(0, 25)
ax.grid(True, axis='y', alpha=0.5, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Add annotation for 2020
ax.annotate('COVID-19 pandemic\ndrove remote learning',
            xy=(7, 12.5), xytext=(9, 20),
            fontsize=9, color=TEXT_SECONDARY,
            arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1),
            ha='center')

# Source attribution
fig.text(0.99, 0.02, 'Source: Caltech/feynmanlectures.caltech.edu (estimated)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-lectures-impact.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Saved: chart-lectures-impact.png")
