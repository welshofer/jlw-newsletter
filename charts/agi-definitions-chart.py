import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#5B4B8A'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
AMBER = '#D4A84B'
TEAL = '#0D6E8A'

# Different AGI definitions and who holds them
definitions = {
    'Amodei': {
        'coding': 95,
        'science': 80,
        'autonomy': 70,
        'reasoning': 85,
        'learning': 60,
    },
    'Hassabis': {
        'coding': 60,
        'science': 90,
        'autonomy': 85,
        'reasoning': 95,
        'learning': 90,
    },
    'LeCun': {
        'coding': 40,
        'science': 70,
        'autonomy': 90,
        'reasoning': 95,
        'learning': 95,
    },
    'Chollet': {
        'coding': 50,
        'science': 60,
        'autonomy': 80,
        'reasoning': 100,
        'learning': 95,
    },
}

categories = ['Coding\nProficiency', 'Scientific\nDiscovery', 'Autonomous\nAgency', 'Novel\nReasoning', 'Continuous\nLearning']
N = len(categories)

# Angle for each category
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # Complete the loop

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True), facecolor=BG)
ax.set_facecolor(BG)

colors = [ACCENT, TEAL, AMBER, '#C4654A']
fills = [0.15, 0.12, 0.1, 0.08]

for idx, (name, values) in enumerate(definitions.items()):
    vals = list(values.values())
    vals += vals[:1]  # Complete the loop

    ax.plot(angles, vals, 'o-', linewidth=2.5, label=name, color=colors[idx], markersize=6)
    ax.fill(angles, vals, alpha=fills[idx], color=colors[idx])

# Fix axis labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11, color=TEXT, fontweight='500')

# Y-axis
ax.set_ylim(0, 100)
ax.set_yticks([25, 50, 75, 100])
ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=9, color=TEXT_SECONDARY)

ax.set_title('What Counts as AGI?\nImportance of Each Capability by Expert\n', fontsize=16, color=TEXT, fontweight='600', pad=30)

# Legend
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), frameon=True,
          facecolor=BG, edgecolor=GRID, fontsize=11)

# Source
fig.text(0.5, 0.02, 'Interpretation based on public statements (Jan 2026) • Illustrative, not exact survey data',
         fontsize=9, color=TEXT_SECONDARY, ha='center', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-agi-definitions.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-agi-definitions.png")
