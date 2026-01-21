import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#3D4F7C'      # Deep indigo
ACCENT2 = '#B85C38'     # Terracotta for contrast
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Functional literacy levels data (2003 NAAL and 2017 PIAAC comparison)
categories = ['Below Basic', 'Basic', 'Intermediate', 'Proficient']
naal_2003 = [14, 29, 44, 13]
piaac_2017 = [19, 34, 34, 13]

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Bars
bars1 = ax.bar(x - width/2, naal_2003, width, label='2003 (NAAL)', color=ACCENT,
               edgecolor=ACCENT, linewidth=1)
bars2 = ax.bar(x + width/2, piaac_2017, width, label='2017 (PIAAC)', color=ACCENT2,
               edgecolor=ACCENT2, linewidth=1)

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'{height}%', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=11, color=ACCENT, fontweight='600')

for bar in bars2:
    height = bar.get_height()
    ax.annotate(f'{height}%', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=11, color=ACCENT2, fontweight='600')

# Styling
ax.set_title('Adult Literacy Levels: Then vs Now', fontsize=18,
             color=TEXT, fontweight='700', pad=20, fontfamily='serif')
ax.set_ylabel('Percentage of Adults', fontsize=12, color=TEXT_SECONDARY, fontweight='500')
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11, color=TEXT)
ax.legend(loc='upper right', frameon=False)

ax.set_ylim(0, 55)
ax.grid(True, alpha=0.4, color=GRID, axis='y')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Callout box
ax.text(0.98, 0.85, '54% of adults\nread below\n6th-grade level',
        transform=ax.transAxes, fontsize=11, color=ACCENT2,
        ha='right', va='top', fontweight='600',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=BG, edgecolor=ACCENT2, alpha=0.9))

# Source
fig.text(0.99, 0.02, 'Source: NAAL 2003, PIAAC 2017', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-functional-literacy.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("Chart saved: chart-functional-literacy.png")
