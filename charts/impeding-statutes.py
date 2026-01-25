import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme - deep slate blue
ACCENT = '#3D5A73'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Federal statutes used for "impeding" charges
statutes = [
    '18 U.S.C. § 111\n(Assault/Impede\nFed Officer)',
    '18 U.S.C. § 231\n(Civil Disorder)',
    '18 U.S.C. § 241\n(KKK Act -\nDeprive Rights)',
    '18 U.S.C. § 1509\n(Obstruct\nCourt Order)',
    'FACE Act\n(Interfere w/\nReligious Worship)'
]

# Maximum penalties (years)
max_penalties = [8, 5, 10, 5, 1]  # years imprisonment

# Key requirements
requirements = [
    '"Forcible" act\nrequired',
    'Any act during\n"civil disorder"',
    'Conspiracy to\ndeprive rights',
    'Court order\nmust exist',
    'Physical\nobstruction'
]

# Create figure
fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
ax.set_facecolor(BG)

# Colors - gradient based on severity
colors = ['#5A7A96', '#4A6A86', ACCENT, '#2D4A63', '#6A8AA6']

# Horizontal bar chart
y_pos = np.arange(len(statutes))
bars = ax.barh(y_pos, max_penalties, color=colors, edgecolor='white', linewidth=2, height=0.6)

# Add requirement labels inside bars
for i, (bar, req, penalty) in enumerate(zip(bars, requirements, max_penalties)):
    # Penalty text at end of bar
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f'{penalty} yrs', va='center', ha='left', fontsize=11, fontweight='600', color=TEXT)
    # Requirement text inside bar (if bar is wide enough)
    if penalty >= 3:
        ax.text(bar.get_width()/2, bar.get_y() + bar.get_height()/2,
                req, va='center', ha='center', fontsize=8, color='white', fontweight='500')

# Formatting
ax.set_yticks(y_pos)
ax.set_yticklabels(statutes, fontsize=10, color=TEXT)
ax.set_xlabel('Maximum Imprisonment (Years)', fontsize=11, color=TEXT_SECONDARY)
ax.set_title('Federal Statutes for Charging "Impeding" Protesters', fontsize=15, color=TEXT, fontweight='700', pad=20)

ax.set_xlim(0, 12)
ax.xaxis.grid(True, linestyle='--', alpha=0.5, color=GRID)
ax.set_axisbelow(True)

# Highlight KKK Act bar
bars[2].set_edgecolor('#C62828')
bars[2].set_linewidth(3)
ax.annotate('Novel application\nto protesters', xy=(10, 2), xytext=(10.5, 3.5),
            fontsize=9, color='#C62828', fontweight='600',
            arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.5))

# Remove spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Source
fig.text(0.99, 0.02, 'Source: U.S. Code, Cornell Law (Jan 2026)', fontsize=8,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/impeding-protest/chart-statutes.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Saved chart-statutes.png")
