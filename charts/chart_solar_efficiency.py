import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#0D6E8A'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Data: Solar cell efficiency records by technology
technologies = ['Antimony\nChalcogenide\n(UNSW 2026)', 'Organic PV', 'CZTS', 'CdTe\n(First Solar)',
                'CIGS', 'Perovskite', 'Mono-Si', 'Multi-junction']
efficiencies = [10.7, 18.2, 13.0, 22.1, 23.4, 26.1, 26.7, 47.6]
colors = [ACCENT, TEXT_SECONDARY, TEXT_SECONDARY, TEXT_SECONDARY,
          TEXT_SECONDARY, TEXT_SECONDARY, TEXT_SECONDARY, TEXT_SECONDARY]

fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
ax.set_facecolor(BG)

# Horizontal bar chart
bars = ax.barh(technologies, efficiencies, color=colors, height=0.6, edgecolor='white')

# Highlight the UNSW breakthrough
bars[0].set_color(ACCENT)
bars[0].set_edgecolor(ACCENT)
bars[0].set_linewidth(3)

# Add value labels
for i, (bar, eff) in enumerate(zip(bars, efficiencies)):
    width = bar.get_width()
    label_color = 'white' if i == 0 else TEXT
    ha = 'right' if width > 5 else 'left'
    offset = -1 if width > 5 else 0.5
    ax.text(width + offset, bar.get_y() + bar.get_height()/2,
            f'{eff}%', va='center', ha=ha, fontsize=11,
            fontweight='600', color=label_color if ha == 'right' else TEXT)

# Add annotation for UNSW
ax.annotate('NEW RECORD\nNon-toxic, Earth-abundant', xy=(10.7, 0), xytext=(20, 0.5),
            fontsize=10, color=ACCENT, fontweight='600',
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

# Styling
ax.set_title('Solar Cell Efficiency Records by Technology',
             fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_xlabel('Certified Efficiency (%)', fontsize=12, color=TEXT_SECONDARY)
ax.set_xlim(0, 52)
ax.grid(True, alpha=0.5, color=GRID, axis='x')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Source attribution
fig.text(0.99, 0.02, 'Source: UNSW / Solar Cell Efficiency Tables (Jan 2026)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-solar-efficiency.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved successfully")
