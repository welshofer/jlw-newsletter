import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import chart_style

# Newsletter color scheme - steel blue war theme
ACCENT = '#2C5F7C'
ACCENT2 = '#C4654A'  # warm contrast for Russia
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'
UKRAINE_BLUE = '#2C5F7C'
UKRAINE_GOLD = '#D4A843'
RUSSIA_RED = '#C4654A'


def main():
    output_dir = chart_style.output_path('images')
    os.makedirs(output_dir, exist_ok=True)

    # ─────────────────────────────────────────────
    # CHART 1: Casualties Comparison - Bar Chart
    # ─────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6.5), facecolor=BG)
    ax.set_facecolor(BG)

    categories = ['Deaths', 'Wounded', 'Total Casualties']
    russia_vals = [325000, 875000, 1200000]
    ukraine_vals = [140000, 410000, 550000]

    x = np.arange(len(categories))
    width = 0.35

    bars_r = ax.bar(x - width/2, russia_vals, width, label='Russia', color=RUSSIA_RED, alpha=0.9, edgecolor='white', linewidth=0.5)
    bars_u = ax.bar(x + width/2, ukraine_vals, width, label='Ukraine', color=UKRAINE_BLUE, alpha=0.9, edgecolor='white', linewidth=0.5)

    # Add value labels on bars
    for bar in bars_r:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 15000,
                f'{height/1000:.0f}K', ha='center', va='bottom',
                fontsize=10, fontweight='600', color=RUSSIA_RED)

    for bar in bars_u:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 15000,
                f'{height/1000:.0f}K', ha='center', va='bottom',
                fontsize=10, fontweight='600', color=UKRAINE_BLUE)

    ax.set_title('Estimated War Casualties (as of Jan 2026)', fontsize=16, color=TEXT, fontweight='600', pad=20, family='serif')
    ax.set_ylabel('Personnel', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11, color=TEXT)
    ax.tick_params(axis='y', colors=TEXT_SECONDARY)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
    ax.grid(True, alpha=0.4, color=GRID, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.legend(fontsize=11, framealpha=0.8, edgecolor=GRID)

    fig.text(0.99, 0.02, 'Source: CSIS Assessment (Jan 2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')
    fig.text(0.01, 0.02, 'Combined total approaching 2 million', fontsize=9,
             color=TEXT_SECONDARY, ha='left', style='italic')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/chart-ukraine-casualties.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 1: Casualties comparison saved")

    # ─────────────────────────────────────────────
    # CHART 2: Feb 2-3 Attack Composition - Donut
    # ─────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=BG)
    ax.set_facecolor(BG)

    sizes = [71, 450]
    labels = ['Missiles\n(71)', 'Drones\n(450)']
    colors = [RUSSIA_RED, '#E8967E']
    explode = (0.03, 0.0)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels,
                                        colors=colors, autopct='%1.0f%%',
                                        startangle=90, pctdistance=0.75,
                                        textprops={'fontsize': 13, 'color': TEXT, 'fontweight': '500'})

    for autotext in autotexts:
        autotext.set_fontsize(14)
        autotext.set_fontweight('600')
        autotext.set_color('white')

    # Draw center circle for donut
    centre_circle = plt.Circle((0, 0), 0.55, fc=BG, linewidth=0)
    ax.add_artist(centre_circle)

    # Center text
    ax.text(0, 0.06, '521', fontsize=36, fontweight='700', color=TEXT, ha='center', va='center', family='serif')
    ax.text(0, -0.1, 'Total Munitions', fontsize=12, color=TEXT_SECONDARY, ha='center', va='center')

    ax.set_title('Russia\'s Feb 2–3 Combined Strike', fontsize=16, color=TEXT, fontweight='600', pad=20, family='serif')

    fig.text(0.5, 0.06, 'Largest attack of 2026 — targeted energy infrastructure during freezing temperatures',
             fontsize=10, color=TEXT_SECONDARY, ha='center', style='italic')
    fig.text(0.5, 0.02, 'Source: Ukrainian Air Force / ISW (Feb 2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='center', style='italic')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/chart-ukraine-strike.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 2: Strike composition saved")

    # ─────────────────────────────────────────────
    # CHART 3: Cost of Advance - Casualties per km²
    # ─────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6.5), facecolor=BG)
    ax.set_facecolor(BG)

    # Estimated Russian advance rate vs casualties per month (2024-2026)
    months = ['Q1\n2024', 'Q2\n2024', 'Q3\n2024', 'Q4\n2024', 'Q1\n2025', 'Q2\n2025', 'Q3\n2025', 'Q4\n2025', 'Jan\n2026']
    advance_km2 = [12, 28, 45, 85, 110, 95, 72, 55, 30]  # approx sq km gained
    casualties_k = [28, 32, 35, 42, 48, 52, 50, 45, 40]  # thousands per period

    ax2 = ax.twinx()

    ax.bar(months, advance_km2, color=UKRAINE_BLUE, alpha=0.7, label='Territory Gained (km²)', width=0.6, edgecolor='white', linewidth=0.5)
    ax2.plot(months, casualties_k, color=RUSSIA_RED, linewidth=2.5, marker='o', markersize=7,
             label='Russian Casualties (thousands)', zorder=5)

    ax.set_title('Russia\'s Diminishing Returns', fontsize=16, color=TEXT, fontweight='600', pad=20, family='serif')
    ax.set_ylabel('Territory Gained (approx. km²)', fontsize=11, color=UKRAINE_BLUE)
    ax2.set_ylabel('Russian Casualties per Period (thousands)', fontsize=11, color=RUSSIA_RED)

    ax.tick_params(axis='y', colors=UKRAINE_BLUE)
    ax2.tick_params(axis='y', colors=RUSSIA_RED)
    ax.tick_params(axis='x', colors=TEXT_SECONDARY)

    ax.grid(True, alpha=0.3, color=GRID, axis='y')
    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax.spines['left'].set_color(UKRAINE_BLUE)
    ax2.spines['right'].set_color(RUSSIA_RED)
    ax.spines['bottom'].set_color(GRID)

    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10, framealpha=0.8, edgecolor=GRID)

    fig.text(0.99, 0.02, 'Source: ISW/CSIS Estimates (2024–2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')
    fig.text(0.01, 0.02, 'Advance rate: 15–70 meters/day in key sectors', fontsize=9,
             color=TEXT_SECONDARY, ha='left', style='italic')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/chart-ukraine-returns.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 3: Diminishing returns saved")

    print("\nAll charts generated successfully!")


if __name__ == "__main__":
    main()
