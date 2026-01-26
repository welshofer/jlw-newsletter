import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#0D6E8A'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'

# Cursor v2.4 feature categories
categories = ['Parallel\nExecution', 'Custom\nSkills', 'Image\nGeneration', 'AI\nAttribution', 'Clarifying\nQuestions']
impact_scores = [9, 8, 7, 8, 7]  # Developer impact (1-10)
novelty_scores = [9, 8, 9, 10, 6]  # Novelty/uniqueness (1-10)

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

x = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x - width/2, impact_scores, width, label='Developer Impact', color=ACCENT, alpha=0.9)
bars2 = ax.bar(x + width/2, novelty_scores, width, label='Market Novelty', color='#2CA58D', alpha=0.9)

ax.set_ylabel('Score (1-10)', fontsize=12, color=TEXT_SECONDARY)
ax.set_title('Cursor v2.4: Feature Analysis', fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=10, color=TEXT)
ax.legend(loc='upper right', frameon=False)
ax.set_ylim(0, 11)

# Add value labels
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{int(bar.get_height())}', ha='center', fontsize=9, color=TEXT)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{int(bar.get_height())}', ha='center', fontsize=9, color=TEXT)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(colors=TEXT_SECONDARY)
ax.yaxis.grid(True, alpha=0.3, color='#D8E2E8')
ax.set_axisbelow(True)

# Note about Cursor Blame
ax.annotate('"Cursor Blame" for AI attribution\nscores highest for novelty—\nno competitor offers this.',
            xy=(3, 10), xytext=(4.2, 9),
            fontsize=9, color=TEXT_SECONDARY, style='italic',
            arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=0.8))

fig.text(0.99, 0.02, 'Source: Cursor v2.4 release notes (Jan 22, 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-cursor-features.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-cursor-features.png")
