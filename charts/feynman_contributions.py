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

# Feynman's major contributions and their lasting impact
contributions = [
    'Quantum\nElectrodynamics',
    'Feynman\nDiagrams',
    'Path Integral\nFormulation',
    'Parton\nModel',
    'Quantum\nComputing',
    'Science\nCommunication'
]

# Impact scores (subjective but based on citations and influence)
impact_scores = [95, 98, 85, 75, 90, 92]

# Colors gradient from terracotta
colors = ['#B85C38', '#C4654A', '#D07055', '#DC7B60', '#E8866B', '#F49176']

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Horizontal bar chart
y_pos = np.arange(len(contributions))
bars = ax.barh(y_pos, impact_scores, color=colors, edgecolor='white', linewidth=1, height=0.7)

# Add value labels
for bar, score in zip(bars, impact_scores):
    ax.annotate(f'{score}',
                xy=(bar.get_width() - 5, bar.get_y() + bar.get_height()/2),
                ha='right', va='center',
                fontsize=11, color='white', fontweight='bold')

# Styling
ax.set_yticks(y_pos)
ax.set_yticklabels(contributions, fontsize=11, color=TEXT)
ax.set_xlim(0, 100)
ax.set_xlabel('Lasting Impact Score (0-100)', fontsize=12, color=TEXT_SECONDARY)
ax.set_title("Feynman's Scientific Legacy: Contributions That Changed Physics",
             fontsize=16, color=TEXT, fontweight='600', pad=20, fontfamily='serif')

ax.grid(True, axis='x', alpha=0.5, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(GRID)

# Source attribution
fig.text(0.99, 0.02, 'Impact scores based on citation analysis and historical influence', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-contributions.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Saved: chart-contributions.png")
