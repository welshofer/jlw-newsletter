# /// script
# dependencies = ["matplotlib"]
# ///
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# Newsletter color scheme - warm terracotta theme
ACCENT = '#B85C38'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'

# Key events in Feynman's life
events = [
    (1918, "Born in Far Rockaway, NYC", "life"),
    (1939, "MIT undergraduate degree", "education"),
    (1942, "PhD from Princeton", "education"),
    (1943, "Joins Manhattan Project", "career"),
    (1945, "Arline dies; WWII ends", "personal"),
    (1950, "Joins Caltech faculty", "career"),
    (1961, "Feynman Lectures begin", "career"),
    (1965, "Nobel Prize in Physics", "achievement"),
    (1981, "Quantum computing proposal", "achievement"),
    (1986, "Challenger investigation", "achievement"),
    (1988, "Death in Los Angeles", "life"),
]

# Color coding by category
colors = {
    "life": "#B85C38",      # Terracotta
    "education": "#5C8A4D", # Green
    "career": "#4D6B8A",    # Blue
    "personal": "#8A5C7A",  # Purple
    "achievement": "#C4A14A" # Gold
}

fig, ax = plt.subplots(figsize=(12, 8), facecolor=BG)
ax.set_facecolor(BG)

# Create timeline
years = [e[0] for e in events]
y_positions = range(len(events))

# Plot events
for i, (year, desc, cat) in enumerate(events):
    ax.scatter(year, i, s=120, c=colors[cat], zorder=5, edgecolors='white', linewidths=2)
    ax.annotate(f"{year}: {desc}",
                xy=(year, i),
                xytext=(year + 2, i),
                fontsize=10,
                color=TEXT,
                va='center',
                fontfamily='sans-serif')

# Connect with line
ax.plot(years, y_positions, color=GRID, linewidth=2, zorder=1)

# Styling
ax.set_xlim(1910, 1995)
ax.set_ylim(-0.5, len(events) - 0.5)
ax.invert_yaxis()

ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
ax.set_title('Richard Feynman: A Life in Physics', fontsize=18, color=TEXT, fontweight='600', pad=20, fontfamily='serif')

# Remove y-axis
ax.yaxis.set_visible(False)

# Style x-axis
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(GRID)

# Legend
legend_elements = [
    mpatches.Patch(facecolor=colors["life"], label='Life Events'),
    mpatches.Patch(facecolor=colors["education"], label='Education'),
    mpatches.Patch(facecolor=colors["career"], label='Career'),
    mpatches.Patch(facecolor=colors["achievement"], label='Achievements'),
]
ax.legend(handles=legend_elements, loc='lower right', frameon=False, fontsize=9)

# Source attribution
fig.text(0.99, 0.02, 'Compiled from biographical sources', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-feynman-timeline.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Saved: chart-feynman-timeline.png")
