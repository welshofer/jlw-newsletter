import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Newsletter color scheme - violet/art theme
ACCENT = "#7C5C8A"
BG = "#FDFBF7"
TEXT = "#1A1815"
TEXT_SECONDARY = "#4D5C6A"
GRID = "#D8E2E8"

# Picasso periods data
periods = [
    ("Blue Period", 1901, 1904, "#2E5984"),
    ("Rose Period", 1904, 1906, "#C4766E"),
    ("African Period", 1907, 1909, "#8B5A2B"),
    ("Analytic Cubism", 1909, 1912, "#6A6A6A"),
    ("Synthetic Cubism", 1912, 1919, "#4A7B4A"),
    ("Neoclassicism", 1918, 1925, "#D4A574"),
    ("Surrealism", 1925, 1937, "#7C5C8A"),
    ("War Years", 1937, 1945, "#3D3D3D"),
    ("Late Works", 1946, 1973, "#B85C38"),
]

fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
ax.set_facecolor(BG)

# Create horizontal bars for each period
for i, (name, start, end, color) in enumerate(periods):
    ax.barh(i, end - start, left=start, height=0.6, color=color, alpha=0.85, edgecolor="white", linewidth=1)
    # Add period name inside or beside bar
    if end - start > 5:
        ax.text(start + (end-start)/2, i, name, ha="center", va="center",
                color="white", fontweight="600", fontsize=10)
    else:
        ax.text(end + 0.5, i, name, ha="left", va="center",
                color=TEXT, fontsize=10)

# Add key life events
events = [
    (1881, "Born"),
    (1904, "Paris"),
    (1937, "Guernica"),
    (1973, "Dies"),
]

for year, event in events:
    ax.axvline(x=year, color=ACCENT, linestyle="--", alpha=0.5, linewidth=1)
    ax.text(year, len(periods)-0.3, f"{year}", ha="center", va="bottom",
            color=ACCENT, fontsize=8, fontweight="500")

# Styling
ax.set_xlim(1880, 1975)
ax.set_ylim(-0.5, len(periods))
ax.set_yticks([])
ax.set_xlabel("Year", fontsize=11, color=TEXT_SECONDARY, labelpad=10)
ax.set_title("Picasso's Major Artistic Periods", fontsize=16, color=TEXT, fontweight="600", pad=20)

# Remove spines
for spine in ax.spines.values():
    spine.set_visible(False)

ax.tick_params(colors=TEXT_SECONDARY, labelsize=10)

# Source attribution
fig.text(0.99, 0.02, "Source: Art historical consensus",
         fontsize=8, color=TEXT_SECONDARY, ha="right", style="italic")

plt.tight_layout()
plt.savefig("/Users/welshofer/clawd/jlw-newsletter/images/chart-picasso-periods.png",
            dpi=150, facecolor=BG, bbox_inches="tight")
print("Chart saved: chart-picasso-periods.png")
