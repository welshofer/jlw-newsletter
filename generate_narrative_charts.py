"""
Data visualizations for Narrative Arcs Newsletter
Color scheme: Deep Indigo (#5B4B8A) with warm amber accents
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Newsletter color scheme - Indigo/Violet theme
ACCENT = '#5B4B8A'      # Deep indigo
ACCENT_LIGHT = '#8B7CB8'  # Lighter indigo
AMBER = '#D4A84B'       # Warm amber for contrast
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'        # Near-black text
TEXT_SECONDARY = '#4D5C6A'  # Secondary gray
GRID = '#D8E2E8'        # Subtle grid

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica Neue', 'Arial', 'sans-serif']

# ============================================
# CHART 1: Timeline of Narrative Frameworks
# ============================================

frameworks_timeline = [
    ("Aristotle's Rhetoric", -350, "Academic"),
    ("Freytag's Pyramid", 1863, "Classic"),
    ("Monroe's Motivated Sequence", 1935, "Academic"),
    ("Hero's Journey", 1949, "Classic"),
    ("Three-Act Structure (Field)", 1979, "Classic"),
    ("Pyramid Principle (Minto)", 1987, "Business"),
    ("Dan Roam's Visual Thinking", 2008, "Modern"),
    ("Golden Circle (Sinek)", 2009, "Modern"),
    ("Duarte Sparkline", 2010, "TED-Style"),
    ("Pixar's Story Spine", 2011, "Modern"),
    ("Oren Klaff's STRONG", 2011, "Startup"),
    ("Andy Raskin's Strategic Narrative", 2016, "Startup"),
    ("StoryBrand (Miller)", 2017, "Business"),
    ("Amazon Working Backwards", 2021, "Startup"),  # Book publication
]

fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
ax.set_facecolor(BG)

# Create color mapping for categories
category_colors = {
    "Classic": ACCENT,
    "Academic": '#6B8E8A',  # Teal
    "Business": AMBER,
    "Modern": '#C4654A',  # Coral
    "TED-Style": '#7C5C8A',  # Violet
    "Startup": '#2E7D5A',  # Green
}

# Filter to recent frameworks for readability (1900+)
recent = [(n, y, c) for n, y, c in frameworks_timeline if y >= 1900]

# Plot timeline
y_positions = range(len(recent))
years = [y for _, y, _ in recent]
names = [n for n, _, _ in recent]
colors = [category_colors[c] for _, _, c in recent]

ax.barh(y_positions, [2025 - y for y in years], left=years, color=colors, alpha=0.7, height=0.6)

# Add year labels
for i, (name, year, cat) in enumerate(recent):
    ax.text(year - 3, i, str(year), ha='right', va='center', fontsize=9,
            color=TEXT_SECONDARY, fontweight='500')
    ax.text(2027, i, name, ha='left', va='center', fontsize=10,
            color=TEXT, fontweight='500')

# Add Aristotle as a special callout
ax.annotate('Aristotle\'s Rhetoric\n(350 BC)', xy=(1930, -0.8), xytext=(1930, -1.5),
            fontsize=9, color=TEXT_SECONDARY, ha='center',
            arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1))

ax.set_xlim(1920, 2090)
ax.set_ylim(-2, len(recent))
ax.set_yticks([])
ax.set_xlabel('', fontsize=12, color=TEXT_SECONDARY)

# Legend
legend_patches = [mpatches.Patch(color=c, label=l, alpha=0.7)
                  for l, c in category_colors.items()]
ax.legend(handles=legend_patches, loc='lower right', frameon=False,
          fontsize=9, ncol=2)

ax.set_title('The Evolution of Presentation Storytelling',
             fontsize=16, color=TEXT, fontweight='600', pad=20, loc='left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

fig.text(0.99, 0.02, 'Source: Various academic and business publications',
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-framework-timeline.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()

print("Chart 1: Timeline saved")

# ============================================
# CHART 2: Framework Use Case Matrix
# ============================================

fig, ax = plt.subplots(figsize=(10, 8), facecolor=BG)
ax.set_facecolor(BG)

# Use cases (columns) and frameworks (rows)
use_cases = ['Sales\nPitch', 'Keynote', 'Board\nMeeting', 'Team\nUpdate', 'Product\nLaunch', 'Fundraising']
frameworks = ['Hero\'s Journey', 'Three-Act', 'Pyramid Principle', 'Sparkline',
              'Story Spine', 'StoryBrand', 'Monroe\'s Sequence', 'Strategic Narrative',
              'Working Backwards']

# Effectiveness scores (0-10 scale)
effectiveness = np.array([
    [6, 10, 4, 5, 8, 7],   # Hero's Journey
    [7, 8, 5, 7, 8, 6],    # Three-Act
    [5, 4, 10, 9, 5, 6],   # Pyramid Principle
    [8, 10, 5, 5, 9, 8],   # Sparkline
    [6, 7, 4, 8, 7, 5],    # Story Spine
    [10, 6, 5, 4, 9, 7],   # StoryBrand
    [9, 8, 6, 5, 8, 9],    # Monroe's Sequence
    [10, 7, 7, 4, 9, 10],  # Strategic Narrative
    [5, 6, 9, 7, 10, 8],   # Working Backwards
])

# Create heatmap
cmap = plt.cm.RdYlGn
im = ax.imshow(effectiveness, cmap=cmap, aspect='auto', vmin=0, vmax=10)

# Add text annotations
for i in range(len(frameworks)):
    for j in range(len(use_cases)):
        val = effectiveness[i, j]
        color = 'white' if val > 7 or val < 3 else TEXT
        ax.text(j, i, str(val), ha='center', va='center', fontsize=11,
                color=color, fontweight='600')

ax.set_xticks(range(len(use_cases)))
ax.set_xticklabels(use_cases, fontsize=10, color=TEXT)
ax.set_yticks(range(len(frameworks)))
ax.set_yticklabels(frameworks, fontsize=10, color=TEXT)

ax.set_title('Framework Effectiveness by Use Case',
             fontsize=16, color=TEXT, fontweight='600', pad=20, loc='left')

# Add colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.8, aspect=30)
cbar.set_label('Effectiveness (0-10)', fontsize=10, color=TEXT_SECONDARY)
cbar.ax.tick_params(labelsize=9)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

fig.text(0.99, 0.02, 'Effectiveness ratings based on framework design intent and common usage patterns',
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-framework-matrix.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()

print("Chart 2: Matrix saved")

# ============================================
# CHART 3: Framework Complexity vs Memorability
# ============================================

fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
ax.set_facecolor(BG)

# Data: (name, complexity 1-10, memorability 1-10, bubble_size, category)
framework_scatter = [
    ("Hero's Journey", 9, 9, 800, "Classic"),
    ("Three-Act", 4, 8, 700, "Classic"),
    ("Freytag's Pyramid", 6, 6, 500, "Classic"),
    ("Pyramid Principle", 3, 7, 650, "Business"),
    ("SCR", 2, 6, 400, "Business"),
    ("Sparkline", 5, 9, 750, "TED-Style"),
    ("Story Spine", 3, 10, 700, "Modern"),
    ("StoryBrand SB7", 5, 8, 700, "Business"),
    ("Monroe's Sequence", 5, 7, 600, "Academic"),
    ("Strategic Narrative", 4, 8, 650, "Startup"),
    ("Golden Circle", 2, 10, 800, "Modern"),
    ("Working Backwards", 4, 6, 500, "Startup"),
    ("STRONG Method", 7, 5, 400, "Startup"),
]

for name, complexity, memorability, size, cat in framework_scatter:
    color = category_colors.get(cat, ACCENT)
    ax.scatter(complexity, memorability, s=size, c=color, alpha=0.65,
               edgecolors='white', linewidth=2)

    # Position labels to avoid overlap
    x_offset = 0.15
    y_offset = 0.15 if memorability < 9 else -0.3
    if name == "Golden Circle":
        x_offset = 0.2
        y_offset = -0.4
    elif name == "Story Spine":
        y_offset = 0.3
    elif name == "Three-Act":
        x_offset = -0.8
        y_offset = 0.3

    ax.annotate(name, (complexity + x_offset, memorability + y_offset),
                fontsize=9, color=TEXT, fontweight='500')

# Quadrant labels
ax.text(1.5, 9.5, 'Sweet Spot:\nSimple & Memorable', fontsize=9, color='#2E7D5A',
        fontweight='600', alpha=0.7)
ax.text(7.5, 9.5, 'Powerful but\nDemanding', fontsize=9, color=AMBER,
        fontweight='600', alpha=0.7)
ax.text(1.5, 1.5, 'Too Simple?', fontsize=9, color=TEXT_SECONDARY,
        fontweight='600', alpha=0.5)
ax.text(7.5, 1.5, 'Avoid', fontsize=9, color='#C4654A',
        fontweight='600', alpha=0.5)

# Quadrant dividers
ax.axhline(y=5.5, color=GRID, linestyle='--', alpha=0.5)
ax.axvline(x=5.5, color=GRID, linestyle='--', alpha=0.5)

ax.set_xlim(0.5, 10.5)
ax.set_ylim(0.5, 10.5)
ax.set_xlabel('Complexity (Steps/Concepts to Master)', fontsize=11, color=TEXT_SECONDARY)
ax.set_ylabel('Memorability (How Sticky Is It?)', fontsize=11, color=TEXT_SECONDARY)
ax.set_title('The Simplicity-Impact Tradeoff',
             fontsize=16, color=TEXT, fontweight='600', pad=20, loc='left')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Legend
legend_patches = [mpatches.Patch(color=c, label=l, alpha=0.65)
                  for l, c in list(category_colors.items())[:4]]
ax.legend(handles=legend_patches, loc='lower right', frameon=False, fontsize=9)

fig.text(0.99, 0.02, 'Bubble size reflects mainstream adoption',
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-complexity-memorability.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()

print("Chart 3: Scatter saved")

print("\n✅ All charts generated successfully!")
