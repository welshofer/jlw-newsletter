import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#3D4F7C'      # Deep indigo
ACCENT2 = '#B85C38'     # Terracotta
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Economic costs of low literacy (estimates)
categories = ['Lost\nProductivity', 'Healthcare\nCosts', 'Criminal\nJustice', 'Welfare &\nSupport']
costs = [1200, 480, 320, 200]  # Billions
colors = [ACCENT, ACCENT, ACCENT2, ACCENT2]

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Bars
bars = ax.bar(categories, costs, color=colors, edgecolor=colors, width=0.6)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'${height}B', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 8), textcoords="offset points",
                ha='center', va='bottom', fontsize=14, color=TEXT, fontweight='700')

# Total annotation
total_cost = sum(costs)
ax.text(0.95, 0.9, f'TOTAL:\n${total_cost/1000:.1f} Trillion',
        transform=ax.transAxes, fontsize=18, color=ACCENT2,
        ha='right', va='top', fontweight='700',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=BG, edgecolor=ACCENT2, linewidth=2))

# Styling
ax.set_title('The $2.2 Trillion Cost of Low Literacy', fontsize=18,
             color=TEXT, fontweight='700', pad=25, fontfamily='serif')
ax.set_ylabel('Annual Cost (Billions USD)', fontsize=12, color=TEXT_SECONDARY, fontweight='500')

ax.set_ylim(0, 1500)
ax.grid(True, alpha=0.4, color=GRID, axis='y')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Context line
ax.axhline(y=800, color=TEXT_SECONDARY, linestyle=':', linewidth=1, alpha=0.5)
ax.text(3.5, 830, 'US Defense Budget (~$850B)', fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

# Source
fig.text(0.99, 0.02, 'Source: National Literacy Institute / ProLiteracy (2024 estimates)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-economic-cost.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("Chart saved: chart-economic-cost.png")
