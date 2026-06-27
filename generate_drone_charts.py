#!/usr/bin/env python3
"""Generate charts for drone warfare newsletter."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from chart_style import output_path, apply_brand_style

# Newsletter color scheme — teal/military tech
ACCENT = '#0D6E8A'
ACCENT2 = '#E07B52'  # warm contrast
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SEC = '#4D5C6A'
GRID = '#D8E2E8'
DARK_TEAL = '#0A5A72'
LIGHT_TEAL = '#5BA3B5'

apply_brand_style()

# ============================================================
# CHART 1: Cost Asymmetry — FPV Drone vs Target Value
# ============================================================


def main():
    fig1, ax1 = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax1.set_facecolor(BG)

    targets = [
        'FPV Drone\n(attacker cost)',
        'Armored\nVehicle',
        'Main Battle\nTank',
        'Knyaz Recon\nDrone',
        'S-300VM\nLauncher',
    ]
    costs = [0.0005, 1.5, 4.5, 8.0, 100.0]  # in $M
    colors = [ACCENT2] + [ACCENT] * 4

    bars = ax1.barh(targets, costs, color=colors, height=0.55, edgecolor='none')

    # Add value labels
    for bar, cost in zip(bars, costs):
        if cost < 1:
            label = f'${int(cost * 1000000):,}'
        else:
            label = f'${cost:.0f}M' if cost >= 1 else f'${cost*1000:.0f}K'
        ax1.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height()/2,
                 label, va='center', ha='left', fontsize=11, fontweight='600',
                 color=TEXT)

    # The ratio callout
    ax1.text(75, -0.15, '200,000:1\ncost ratio', fontsize=14, fontweight='700',
             color=ACCENT2, ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=ACCENT2, alpha=0.12))

    ax1.set_title('The $500 Weapon vs. Multi-Million Dollar Targets',
                  fontsize=16, color=TEXT, fontweight='600', pad=20,
                  fontfamily='serif')
    ax1.set_xlabel('Estimated Value (USD Millions)', fontsize=11, color=TEXT_SEC)
    ax1.set_xlim(0, 120)
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:.0f}M'))
    ax1.grid(True, axis='x', alpha=0.4, color=GRID)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(GRID)
    ax1.spines['bottom'].set_color(GRID)
    ax1.tick_params(colors=TEXT_SEC, labelsize=10)
    ax1.invert_yaxis()

    fig1.text(0.99, 0.02, 'Source: RUSI, United24 Media (Feb 2026)',
              fontsize=8, color=TEXT_SEC, ha='right', style='italic')

    plt.tight_layout()
    fig1.savefig(output_path('images/chart-cost-asymmetry.png'),
                 dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close(fig1)
    print("Chart 1 saved: chart-cost-asymmetry.png")


    # ============================================================
    # CHART 2: Manufacturing Timeline — Traditional vs. Rapid
    # ============================================================
    fig2, ax2 = plt.subplots(figsize=(10, 5.5), facecolor=BG)
    ax2.set_facecolor(BG)

    programs = [
        'MQ-9 Reaper\n(General Atomics)',
        'TB2 Bayraktar\n(Baykar)',
        'XQ-58A Valkyrie\n(Kratos)',
        'CCA / YFQ-42A\n(General Atomics)',
        'Venom\n(Divergent × Mach)',
    ]
    # Development timeline in months (approximate from concept to first flight)
    months = [84, 48, 36, 30, 2.4]  # 71 days ≈ 2.4 months
    bar_colors = [LIGHT_TEAL, LIGHT_TEAL, ACCENT, ACCENT, ACCENT2]

    bars2 = ax2.barh(programs, months, color=bar_colors, height=0.55, edgecolor='none')

    for bar, m in zip(bars2, months):
        if m < 12:
            label = f'{int(m * 30)} days'
        else:
            label = f'{m/12:.1f} yr' if m >= 12 else f'{m:.0f} mo'
        ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                 label, va='center', ha='left', fontsize=11, fontweight='600',
                 color=TEXT)

    # Highlight the 71-day bar
    ax2.annotate('71 DAYS', xy=(2.4, 4), xytext=(25, 4),
                 fontsize=13, fontweight='700', color=ACCENT2,
                 arrowprops=dict(arrowstyle='->', color=ACCENT2, lw=2))

    ax2.set_title('From Years to Days: The Drone Manufacturing Revolution',
                  fontsize=16, color=TEXT, fontweight='600', pad=20,
                  fontfamily='serif')
    ax2.set_xlabel('Design-to-First-Flight (Months)', fontsize=11, color=TEXT_SEC)
    ax2.set_xlim(0, 100)
    ax2.grid(True, axis='x', alpha=0.4, color=GRID)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(GRID)
    ax2.spines['bottom'].set_color(GRID)
    ax2.tick_params(colors=TEXT_SEC, labelsize=10)
    ax2.invert_yaxis()

    fig2.text(0.99, 0.02, 'Source: Divergent Technologies, Defense Scoop (Feb 2026)',
              fontsize=8, color=TEXT_SEC, ha='right', style='italic')

    plt.tight_layout()
    fig2.savefig(output_path('images/chart-manufacturing-speed.png'),
                 dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close(fig2)
    print("Chart 2 saved: chart-manufacturing-speed.png")


    # ============================================================
    # CHART 3: Counter-Drone Methods — Cost Per Intercept
    # ============================================================
    fig3, ax3 = plt.subplots(figsize=(10, 5.5), facecolor=BG)
    ax3.set_facecolor(BG)

    methods = [
        'Patriot Missile',
        'Stinger\nMANPADS',
        'Electronic\nWarfare Jammer',
        'Directed Energy\n(Laser)',
        'DroneHunter\nNet Capture',
    ]
    # Cost per intercept in thousands of dollars
    costs_intercept = [3000, 120, 30, 10, 15]
    method_colors = ['#C44E52', '#C44E52', LIGHT_TEAL, ACCENT, ACCENT2]

    bars3 = ax3.barh(methods, costs_intercept, color=method_colors, height=0.55, edgecolor='none')

    for bar, c in zip(bars3, costs_intercept):
        if c >= 1000:
            label = f'${c/1000:.0f}M'
        else:
            label = f'${c}K'
        ax3.text(bar.get_width() + 40, bar.get_y() + bar.get_height()/2,
                 label, va='center', ha='left', fontsize=11, fontweight='600',
                 color=TEXT)

    # Add "Replicator 2" badge
    ax3.text(2000, 4.3, 'Replicator 2\nSelection', fontsize=10, fontweight='600',
             color=ACCENT2, ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=ACCENT2, alpha=0.12))
    ax3.annotate('', xy=(15, 4.3), xytext=(1800, 4.3),
                 arrowprops=dict(arrowstyle='->', color=ACCENT2, lw=1.5))

    ax3.set_title('Counter-Drone Cost Per Intercept',
                  fontsize=16, color=TEXT, fontweight='600', pad=20,
                  fontfamily='serif')
    ax3.set_xlabel('Cost Per Intercept (USD Thousands)', fontsize=11, color=TEXT_SEC)
    ax3.set_xlim(0, 3500)
    ax3.xaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, _: f'${x/1000:.0f}M' if x >= 1000 else f'${x:.0f}K'))
    ax3.grid(True, axis='x', alpha=0.4, color=GRID)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color(GRID)
    ax3.spines['bottom'].set_color(GRID)
    ax3.tick_params(colors=TEXT_SEC, labelsize=10)
    ax3.invert_yaxis()

    fig3.text(0.99, 0.02, 'Source: CSIS, Hudson Institute, Fortem Technologies (Feb 2026)',
              fontsize=8, color=TEXT_SEC, ha='right', style='italic')

    plt.tight_layout()
    fig3.savefig(output_path('images/chart-counter-drone-costs.png'),
                 dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close(fig3)
    print("Chart 3 saved: chart-counter-drone-costs.png")

    print("\nAll 3 charts generated successfully!")


if __name__ == "__main__":
    main()
