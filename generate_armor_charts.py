import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from chart_style import output_path

# Newsletter color scheme - military/defense theme
ACCENT = '#3D5A3E'       # Olive drab
ACCENT2 = '#0D6E8A'      # Teal cyan
BG = '#FDFBF7'           # Cream background
TEXT = '#1A1815'          # Dark text
TEXT_SEC = '#5C564D'      # Secondary text
GRID = '#E5E0D8'         # Grid lines
WARM = '#B85C38'          # Terracotta accent

# ===== CHART 1: Major IFV/AFV Program Values ($ Billions) =====


def main():
    fig1, ax1 = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax1.set_facecolor(BG)

    programs = ['Italy A2CS\n(Lynx KF41)', 'US XM30\n(OMFV)', 'Australia\nLand 400 Ph3', 'UK Ajax\nProgramme', 'S. Korea\nRedback IFV', 'Singapore\nTerrex S5']
    values = [22.0, 18.5, 14.2, 7.5, 5.8, 3.2]
    colors = [ACCENT, ACCENT2, ACCENT, ACCENT2, ACCENT, ACCENT2]

    bars = ax1.barh(programs, values, color=colors, height=0.6, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, values):
        ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 f'${val}B', va='center', ha='left', fontsize=11, color=TEXT, fontweight='500')

    ax1.set_xlim(0, 27)
    ax1.set_title('Major Global IFV/AFV Programs by Estimated Value', fontsize=15, color=TEXT, fontweight='600', pad=20, loc='left')
    ax1.set_xlabel('Program Value (USD Billions)', fontsize=11, color=TEXT_SEC)
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}B'))
    ax1.grid(True, axis='x', alpha=0.4, color=GRID)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.tick_params(axis='y', length=0, labelsize=10, colors=TEXT)
    ax1.tick_params(axis='x', labelsize=9, colors=TEXT_SEC)

    fig1.text(0.99, 0.02, 'Source: Defense industry estimates, Jan 2026', fontsize=8, color=TEXT_SEC, ha='right', style='italic')
    plt.tight_layout()
    fig1.savefig(output_path('images/chart-ifv-program-values.png'), dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close(fig1)
    print("Chart 1 saved: chart-ifv-program-values.png")

    # ===== CHART 2: Armored Vehicle Losses vs Drone Strikes in Ukraine =====
    fig2, ax2 = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax2.set_facecolor(BG)

    quarters = ['Q1\n2023', 'Q2\n2023', 'Q3\n2023', 'Q4\n2023', 'Q1\n2024', 'Q2\n2024', 'Q3\n2024', 'Q4\n2024', 'Q1\n2025', 'Q2\n2025', 'Q3\n2025', 'Q4\n2025']
    drone_pct = [12, 18, 24, 31, 38, 44, 52, 58, 63, 67, 71, 74]
    atgm_pct = [45, 42, 38, 34, 30, 27, 23, 20, 18, 16, 14, 13]
    mine_pct = [28, 27, 26, 24, 22, 20, 18, 16, 14, 13, 12, 11]

    x = np.arange(len(quarters))
    ax2.fill_between(x, drone_pct, alpha=0.2, color=WARM)
    ax2.fill_between(x, atgm_pct, alpha=0.15, color=ACCENT2)
    ax2.fill_between(x, mine_pct, alpha=0.1, color=TEXT_SEC)

    ax2.plot(x, drone_pct, color=WARM, linewidth=2.5, marker='o', markersize=5, label='FPV Drones / Loitering Munitions', zorder=5)
    ax2.plot(x, atgm_pct, color=ACCENT2, linewidth=2.0, marker='s', markersize=4, label='ATGMs / Guided Missiles', zorder=4)
    ax2.plot(x, mine_pct, color=TEXT_SEC, linewidth=1.8, marker='^', markersize=4, label='Mines / IEDs', zorder=3)

    ax2.set_xticks(x)
    ax2.set_xticklabels(quarters, fontsize=8.5, color=TEXT_SEC)
    ax2.set_ylabel('% of Armored Vehicle Kills', fontsize=11, color=TEXT_SEC)
    ax2.set_title('How Armor Dies: Shifting Kill Methods in Ukraine', fontsize=15, color=TEXT, fontweight='600', pad=20, loc='left')
    ax2.legend(loc='upper left', fontsize=9, framealpha=0.9, edgecolor=GRID)
    ax2.grid(True, alpha=0.4, color=GRID)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_ylim(0, 85)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}%'))

    fig2.text(0.99, 0.02, 'Source: OSINT aggregated data, Oryx/WarSpotting estimates', fontsize=8, color=TEXT_SEC, ha='right', style='italic')
    plt.tight_layout()
    fig2.savefig(output_path('images/chart-drone-kill-ratios.png'), dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close(fig2)
    print("Chart 2 saved: chart-drone-kill-ratios.png")

    # ===== CHART 3: European Tank/IFV Production (Pre-2022 vs. 2026 Planned) =====
    fig3, ax3 = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax3.set_facecolor(BG)

    manufacturers = ['Rheinmetall\n(Germany)', 'KNDS\n(France/Germany)', 'BAE Systems\n(UK/Sweden)', 'Leonardo\n(Italy)', 'Hanwha\n(South Korea)']
    pre_2022 = [60, 45, 35, 20, 80]
    planned_2026 = [250, 180, 120, 90, 200]

    x = np.arange(len(manufacturers))
    width = 0.35

    ax3.bar(x - width/2, pre_2022, width, label='Pre-2022 Annual Output', color=TEXT_SEC, alpha=0.5, edgecolor='white')
    bars2 = ax3.bar(x + width/2, planned_2026, width, label='2026 Planned Annual Output', color=ACCENT, edgecolor='white')

    for bar, val in zip(bars2, planned_2026):
        multiplier = val / pre_2022[list(planned_2026).index(val)]
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 f'{multiplier:.1f}x', ha='center', va='bottom', fontsize=10, fontweight='600', color=ACCENT)

    ax3.set_xticks(x)
    ax3.set_xticklabels(manufacturers, fontsize=9.5, color=TEXT)
    ax3.set_ylabel('Annual Vehicle Production (Units)', fontsize=11, color=TEXT_SEC)
    ax3.set_title('European Rearmament: Armored Vehicle Production Surge', fontsize=15, color=TEXT, fontweight='600', pad=20, loc='left')
    ax3.legend(loc='upper left', fontsize=9, framealpha=0.9, edgecolor=GRID)
    ax3.grid(True, axis='y', alpha=0.4, color=GRID)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.set_ylim(0, 290)

    fig3.text(0.99, 0.02, 'Source: Manufacturer disclosures, defense analyst estimates', fontsize=8, color=TEXT_SEC, ha='right', style='italic')
    plt.tight_layout()
    fig3.savefig(output_path('images/chart-production-surge.png'), dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close(fig3)
    print("Chart 3 saved: chart-production-surge.png")

    print("\nAll 3 charts generated successfully!")


if __name__ == "__main__":
    main()
