import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = "#7C5C8A"
BG = "#FDFBF7"
TEXT = "#1A1815"
TEXT_SECONDARY = "#4D5C6A"
GRID = "#D8E2E8"

# Picasso auction records (approximate, well-documented sales)
years = [2004, 2006, 2010, 2013, 2015, 2018, 2021, 2024, 2025]
prices = [104, 95, 106, 155, 179, 115, 103, 139, 125]  # in millions USD

fig, ax = plt.subplots(figsize=(11, 6), facecolor=BG)
ax.set_facecolor(BG)

# Create bar chart
bars = ax.bar(range(len(years)), prices, color=ACCENT, alpha=0.85, edgecolor="white", linewidth=1, width=0.7)

# Add price labels on bars
for i, (bar, price) in enumerate(zip(bars, prices)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
            f"${price}M", ha="center", va="bottom", fontsize=9, color=TEXT, fontweight="500")

# Styling
ax.set_xticks(range(len(years)))
ax.set_xticklabels(years, fontsize=10, color=TEXT_SECONDARY)
ax.set_ylabel("Sale Price (Millions USD)", fontsize=11, color=TEXT_SECONDARY, labelpad=10)
ax.set_title("Picasso Auction Records: Top Sales 2004-2025", fontsize=16, color=TEXT, fontweight="600", pad=20)
ax.set_ylim(0, 200)

# Add gridlines
ax.yaxis.grid(True, alpha=0.4, color=GRID, linestyle="-")
ax.set_axisbelow(True)

# Remove spines except bottom
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color(GRID)

ax.tick_params(colors=TEXT_SECONDARY, labelsize=10, left=False)

# Add $179M highlight annotation
max_idx = prices.index(max(prices))
ax.annotate("Record: Les femmes d'Alger\n(Christie's 2015)",
            xy=(max_idx, prices[max_idx]),
            xytext=(max_idx + 1.5, prices[max_idx] + 10),
            fontsize=9, color=ACCENT, fontweight="500",
            arrowprops=dict(arrowstyle="->", color=ACCENT, alpha=0.7))

# Source attribution
fig.text(0.99, 0.02, "Source: Christie's, Sotheby's auction records",
         fontsize=8, color=TEXT_SECONDARY, ha="right", style="italic")

plt.tight_layout()
plt.savefig("/Users/welshofer/clawd/jlw-newsletter/images/chart-picasso-auctions.png",
            dpi=150, facecolor=BG, bbox_inches="tight")
print("Chart saved: chart-picasso-auctions.png")
