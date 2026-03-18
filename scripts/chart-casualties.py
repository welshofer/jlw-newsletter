import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Newsletter color scheme - olive/military themed
ACCENT = '#5B6B4A'
ACCENT2 = '#8B4513'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SEC = '#5C564D'
GRID = '#E5E0D8'

categories = ['Killed', 'Wounded', 'Captured/\nMissing']
us_casualties = [19000, 47500, 23000]
german_casualties = [12000, 38000, 30000]  # conservative estimates from Dept of Defense

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

bars1 = ax.bar(x - width/2, us_casualties, width, label='United States',
               color=ACCENT, edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x + width/2, german_casualties, width, label='Germany',
               color=ACCENT2, edgecolor='white', linewidth=0.5, alpha=0.85)

# Add value labels
for bar in bars1:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 500,
            f'{h:,}', ha='center', va='bottom', fontsize=11,
            color=ACCENT, fontweight='600')

for bar in bars2:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 500,
            f'{h:,}', ha='center', va='bottom', fontsize=11,
            color=ACCENT2, fontweight='600')

ax.set_title('Battle of the Bulge: Casualties by Category',
             fontsize=16, color=TEXT, fontweight='600', pad=20,
             fontfamily='serif')
ax.set_ylabel('Personnel', fontsize=12, color=TEXT_SEC)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12, color=TEXT)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
ax.set_ylim(0, 55000)
ax.legend(fontsize=11, frameon=False)
ax.grid(True, axis='y', alpha=0.4, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=TEXT_SEC)

fig.text(0.99, 0.02, 'Source: U.S. Department of Defense, The Ardennes Campaign (1945)',
         fontsize=8, color=TEXT_SEC, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-casualties.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-casualties.png")
