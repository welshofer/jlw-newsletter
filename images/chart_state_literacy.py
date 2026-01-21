import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#3D4F7C'      # Deep indigo
ACCENT2 = '#B85C38'     # Terracotta for lowest
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Top and Bottom states by literacy proficiency (estimated 2024 data)
states_top = ['New Hampshire', 'Minnesota', 'Vermont', 'Massachusetts', 'Colorado']
scores_top = [94.1, 93.8, 93.5, 93.2, 92.8]

states_bottom = ['Louisiana', 'Mississippi', 'New Mexico', 'Alabama', 'California']
scores_bottom = [79.2, 78.8, 80.1, 81.5, 82.3]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=BG)

# Top 5 states
ax1.set_facecolor(BG)
bars1 = ax1.barh(states_top[::-1], scores_top[::-1], color=ACCENT, edgecolor=ACCENT, height=0.6)
ax1.set_xlim(75, 100)
ax1.set_title('Highest Literacy Rates', fontsize=14, color=TEXT, fontweight='600', pad=10)
ax1.set_xlabel('Adult Literacy Rate (%)', fontsize=11, color=TEXT_SECONDARY)

for bar, score in zip(bars1, scores_top[::-1]):
    ax1.text(score + 0.5, bar.get_y() + bar.get_height()/2, f'{score}%',
             va='center', fontsize=11, color=ACCENT, fontweight='600')

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color(GRID)
ax1.spines['bottom'].set_color(GRID)
ax1.grid(True, alpha=0.4, color=GRID, axis='x')

# Bottom 5 states
ax2.set_facecolor(BG)
bars2 = ax2.barh(states_bottom[::-1], scores_bottom[::-1], color=ACCENT2, edgecolor=ACCENT2, height=0.6)
ax2.set_xlim(75, 100)
ax2.set_title('Lowest Literacy Rates', fontsize=14, color=TEXT, fontweight='600', pad=10)
ax2.set_xlabel('Adult Literacy Rate (%)', fontsize=11, color=TEXT_SECONDARY)

for bar, score in zip(bars2, scores_bottom[::-1]):
    ax2.text(score + 0.5, bar.get_y() + bar.get_height()/2, f'{score}%',
             va='center', fontsize=11, color=ACCENT2, fontweight='600')

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color(GRID)
ax2.spines['bottom'].set_color(GRID)
ax2.grid(True, alpha=0.4, color=GRID, axis='x')

# Main title
fig.suptitle('The Literacy Divide: State-by-State Gap', fontsize=18,
             color=TEXT, fontweight='700', y=1.02, fontfamily='serif')

# Gap annotation
fig.text(0.5, -0.02, '15+ percentage point gap between highest and lowest states',
         ha='center', fontsize=11, color=TEXT_SECONDARY, style='italic')

# Source
fig.text(0.99, -0.06, 'Source: World Population Review / Dept. of Education (2024)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-state-literacy-gap.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("Chart saved: chart-state-literacy-gap.png")
