import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = "#7C5C8A"
BG = "#FDFBF7"
TEXT = "#1A1815"
TEXT_SECONDARY = "#4D5C6A"

# Picasso's estimated output by medium (approximate)
mediums = ["Paintings", "Drawings/\nSketches", "Prints", "Sculptures", "Ceramics"]
counts = [1885, 12000, 2880, 1228, 2200]
colors = ["#7C5C8A", "#B85C38", "#5B7B6A", "#8B6B4A", "#6A7B8A"]

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Horizontal bar chart
bars = ax.barh(mediums, counts, color=colors, alpha=0.85, edgecolor="white", linewidth=1, height=0.65)

# Add count labels
for bar, count in zip(bars, counts):
    width = bar.get_width()
    ax.text(width + 200, bar.get_y() + bar.get_height()/2,
            f"{count:,}", ha="left", va="center", fontsize=11, color=TEXT, fontweight="500")

# Styling
ax.set_xlim(0, 14500)
ax.set_xlabel("Estimated Number of Works", fontsize=11, color=TEXT_SECONDARY, labelpad=10)
ax.set_title("Picasso's Prolific Output: ~50,000 Total Works", fontsize=16, color=TEXT, fontweight="600", pad=20)

# Add vertical gridlines
ax.xaxis.grid(True, alpha=0.4, color="#D8E2E8", linestyle="-")
ax.set_axisbelow(True)

# Remove spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_color("#D8E2E8")
ax.spines["left"].set_visible(False)

ax.tick_params(colors=TEXT_SECONDARY, labelsize=10, left=False)

# Add total annotation
ax.text(0.98, 0.05, "Total lifetime output:\n~50,000 works", transform=ax.transAxes,
        fontsize=10, color=ACCENT, ha="right", va="bottom", fontweight="500",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=BG, edgecolor=ACCENT, alpha=0.9))

# Source attribution
fig.text(0.99, 0.02, "Source: Picasso Museum estimates",
         fontsize=8, color=TEXT_SECONDARY, ha="right", style="italic")

plt.tight_layout()
plt.savefig("/Users/welshofer/clawd/jlw-newsletter/images/chart-picasso-output.png",
            dpi=150, facecolor=BG, bbox_inches="tight")
print("Chart saved: chart-picasso-output.png")
