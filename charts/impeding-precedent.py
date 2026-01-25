import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Newsletter color scheme - deep slate blue
ACCENT = '#3D5A73'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Key precedents establishing "impeding" boundaries
cases = [
    {
        'year': 1968,
        'name': 'Cameron v. Johnson',
        'holding': 'Blocking access to\npublic buildings is\nNOT protected speech',
        'outcome': 'against'
    },
    {
        'year': 1968,
        'name': 'United States v.\nO\'Brien',
        'holding': '"O\'Brien Test":\nGovt can regulate\nexpressive conduct',
        'outcome': 'against'
    },
    {
        'year': 1983,
        'name': 'Perry Education\nv. Perry Local',
        'holding': 'Time, place, manner\nrestrictions allowed\nin public forums',
        'outcome': 'neutral'
    },
    {
        'year': 2000,
        'name': 'Hill v. Colorado',
        'holding': 'Buffer zones around\nclinics are\nconstitutional',
        'outcome': 'against'
    },
    {
        'year': 2026,
        'name': 'Menendez TRO\n(8th Circuit pending)',
        'holding': '"Following at distance"\nis NOT obstruction\n(under appeal)',
        'outcome': 'for'
    }
]

# Create figure
fig, ax = plt.subplots(figsize=(14, 6), facecolor=BG)
ax.set_facecolor(BG)

# Timeline
years = [c['year'] for c in cases]
min_year, max_year = 1965, 2030

# Draw main timeline
ax.axhline(y=0, color=ACCENT, linewidth=3, zorder=1)

# Color mapping
color_map = {
    'for': '#2E7D32',      # green - favors protesters
    'against': '#C62828',  # red - favors government
    'neutral': '#F57C00'   # orange - balanced
}

# Plot cases
for i, case in enumerate(cases):
    x = case['year']
    y = 0.5 if i % 2 == 0 else -0.5
    color = color_map[case['outcome']]

    # Marker
    ax.scatter([x], [0], s=200, c=[color], zorder=3, edgecolors='white', linewidths=2)

    # Vertical line to text
    ax.plot([x, x], [0, y*0.8], color=GRID, linewidth=1.5, zorder=2)

    # Case name box
    va = 'bottom' if y > 0 else 'top'
    ax.annotate(f"{case['name']}\n({case['year']})",
                xy=(x, y*0.8), xytext=(0, 10 if y > 0 else -10),
                textcoords='offset points', ha='center', va=va,
                fontsize=10, fontweight='600', color=TEXT,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=color, linewidth=2))

    # Holding text
    holding_y = y * 1.5
    ax.text(x, holding_y, case['holding'], ha='center', va='center' if y > 0 else 'center',
            fontsize=8, color=TEXT_SECONDARY, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GRID, alpha=0.9))

# Formatting
ax.set_xlim(min_year, max_year)
ax.set_ylim(-1.8, 1.8)
ax.set_title('The Legal Boundaries of "Impeding": Key Precedents', fontsize=15, color=TEXT, fontweight='700', pad=25)

# X-axis
ax.set_xticks([1970, 1980, 1990, 2000, 2010, 2020])
ax.set_xticklabels(['1970', '1980', '1990', '2000', '2010', '2020'], fontsize=10, color=TEXT_SECONDARY)

# Hide y-axis
ax.yaxis.set_visible(False)

# Remove spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='#C62828', edgecolor='white', label='Favors Government'),
    mpatches.Patch(facecolor='#F57C00', edgecolor='white', label='Balanced'),
    mpatches.Patch(facecolor='#2E7D32', edgecolor='white', label='Favors Protesters'),
]
ax.legend(handles=legend_elements, loc='lower right', framealpha=0.9, fontsize=9)

# Annotation for recent case
ax.annotate('First ruling defining\n"appropriate distance"', xy=(2026, 0.5), xytext=(2020, 1.4),
            fontsize=9, color='#2E7D32', fontweight='500',
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.5))

# Source
fig.text(0.99, 0.02, 'Source: SCOTUS, Justia, Oyez (1968-2026)', fontsize=8,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/impeding-protest/chart-precedent.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Saved chart-precedent.png")
