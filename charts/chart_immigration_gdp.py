#!/usr/bin/env python3
"""
Data visualizations for Immigration & GDP Newsletter
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Newsletter color scheme
ACCENT = '#0D6E8A'      # Deep teal
ACCENT_LIGHT = '#4A9DB8'
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
POSITIVE = '#2E8B57'    # Sea green for positive
NEGATIVE = '#C04040'    # Muted red for negative
AMBER = '#B85C38'       # Warm amber

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SF Pro Display', 'Helvetica Neue', 'Arial']

def chart_tax_contributions():
    """Stacked bar showing $96.7B in tax contributions breakdown"""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Data from ITEP (2022 figures)
    categories = ['Federal\nTaxes', 'State & Local\nTaxes']
    values = [59.4, 37.3]  # billions

    # Breakdown
    ss_medicare = 33.9  # Part of federal
    other_federal = 59.4 - 33.9

    # Create stacked bar for federal
    bars1 = ax.bar(['Tax Contributions'], [other_federal],
                   color=ACCENT, label='Other Federal Taxes', width=0.4)
    bars2 = ax.bar(['Tax Contributions'], [ss_medicare],
                   bottom=[other_federal], color=ACCENT_LIGHT,
                   label='Social Security & Medicare', width=0.4)
    bars3 = ax.bar(['Tax Contributions'], [37.3],
                   bottom=[59.4], color=AMBER,
                   label='State & Local Taxes', width=0.4)

    # Add value labels
    ax.text(0, other_federal/2, f'${other_federal:.1f}B',
            ha='center', va='center', color='white', fontsize=14, fontweight='600')
    ax.text(0, other_federal + ss_medicare/2, f'${ss_medicare:.1f}B',
            ha='center', va='center', color='white', fontsize=14, fontweight='600')
    ax.text(0, 59.4 + 37.3/2, f'${37.3:.1f}B',
            ha='center', va='center', color='white', fontsize=14, fontweight='600')

    # Total annotation
    ax.annotate(f'Total: $96.7B', xy=(0, 96.7), xytext=(0.25, 85),
                fontsize=16, fontweight='bold', color=TEXT,
                arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY))

    ax.set_ylabel('Billions USD', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Annual Tax Contributions by Undocumented Immigrants',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_ylim(0, 110)
    ax.legend(loc='upper right', framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)

    # Note about SS/Medicare
    fig.text(0.5, 0.02, 'Note: $33.9B funds Social Security & Medicare—programs undocumented immigrants cannot access',
             fontsize=9, color=TEXT_SECONDARY, ha='center', style='italic')

    fig.text(0.99, 0.02, 'Source: ITEP (2025)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-tax-contributions.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-tax-contributions.png")


def chart_gdp_scenarios():
    """Bar chart comparing GDP impact under different scenarios"""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Data from various sources
    scenarios = [
        'Mass Deportation\n(Low Est.)',
        'Mass Deportation\n(High Est.)',
        'Restrictive Policy\n(NFAP)',
        'Baseline Growth\n(With Immigration)',
    ]

    # GDP impact as percentage points or cumulative
    gdp_impact = [-2.6, -6.8, -1.9, 0.2]  # Negative = contraction, positive = growth contribution
    colors = [NEGATIVE, NEGATIVE, NEGATIVE, POSITIVE]

    bars = ax.barh(scenarios, gdp_impact, color=colors, height=0.6)

    # Add value labels
    for bar, val in zip(bars, gdp_impact):
        x_pos = bar.get_width()
        label = f'{val:+.1f}%' if abs(val) < 10 else f'${abs(val):.1f}T'
        ha = 'left' if val > 0 else 'right'
        offset = 0.1 if val > 0 else -0.1
        ax.text(x_pos + offset, bar.get_y() + bar.get_height()/2,
                label, ha=ha, va='center', fontsize=12, fontweight='600', color=TEXT)

    ax.axvline(x=0, color=TEXT_SECONDARY, linewidth=0.5)
    ax.set_xlabel('GDP Impact', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('GDP Impact Under Different Immigration Scenarios',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.set_xlim(-8, 1)

    fig.text(0.99, 0.02, 'Sources: Econlib, NFAP, CBO (2024-2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-gdp-scenarios.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-gdp-scenarios.png")


def chart_fiscal_debate():
    """Dual chart showing both perspectives on fiscal impact"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=BG)

    for ax in [ax1, ax2]:
        ax.set_facecolor(BG)

    # LEFT: Net Positive Perspective (CBO/ITEP)
    categories1 = ['Tax Revenue\n(Annual)', 'Deficit Reduction\n(10-Year)', 'GDP Contribution\n(Annual)']
    values1 = [96.7, 900, 0.2]  # billions for first two, percentage points for last
    colors1 = [POSITIVE, POSITIVE, ACCENT]

    bars1 = ax1.bar(categories1, [96.7, 90, 100], color=colors1, width=0.6)  # Normalized for display
    ax1.set_title('Net Positive View\n(CBO, ITEP)', fontsize=14, color=POSITIVE, fontweight='600', pad=15)
    ax1.set_ylabel('Impact (normalized scale)', fontsize=10, color=TEXT_SECONDARY)

    # Labels
    ax1.text(0, 96.7 + 3, '$96.7B', ha='center', fontsize=11, fontweight='600', color=TEXT)
    ax1.text(1, 90 + 3, '$0.9T', ha='center', fontsize=11, fontweight='600', color=TEXT)
    ax1.text(2, 100 + 3, '+0.2%/yr', ha='center', fontsize=11, fontweight='600', color=TEXT)

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(GRID)
    ax1.spines['bottom'].set_color(GRID)
    ax1.tick_params(colors=TEXT_SECONDARY)
    ax1.set_ylim(0, 120)

    # RIGHT: Net Negative Perspective (Manhattan Institute, CIS)
    categories2 = ['Lifetime Cost\n(Per Person)', 'Annual Federal\nDeficit', 'Services Gap']
    values2 = [68.4, 10, 80]  # thousands for first, billions for second
    colors2 = [NEGATIVE, NEGATIVE, AMBER]

    bars2 = ax2.bar(categories2, [68.4, 100, 80], color=colors2, width=0.6)
    ax2.set_title('Net Negative View\n(CIS, Manhattan Inst.)', fontsize=14, color=NEGATIVE, fontweight='600', pad=15)

    # Labels
    ax2.text(0, 68.4 + 3, '$68K', ha='center', fontsize=11, fontweight='600', color=TEXT)
    ax2.text(1, 100 + 3, '$10B+', ha='center', fontsize=11, fontweight='600', color=TEXT)
    ax2.text(2, 80 + 3, '$80K', ha='center', fontsize=11, fontweight='600', color=TEXT)

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(GRID)
    ax2.spines['bottom'].set_color(GRID)
    ax2.tick_params(colors=TEXT_SECONDARY)
    ax2.set_ylim(0, 120)

    fig.suptitle('The Fiscal Impact Debate: Two Perspectives',
                 fontsize=16, color=TEXT, fontweight='600', y=1.02)

    fig.text(0.5, -0.02, 'Note: Methodological differences explain divergent conclusions—see analysis',
             fontsize=9, color=TEXT_SECONDARY, ha='center', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-fiscal-debate.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-fiscal-debate.png")


def chart_labor_sectors():
    """Horizontal bar showing immigrant workforce share by sector"""
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    ax.set_facecolor(BG)

    sectors = ['Construction', 'Agriculture', 'Hospitality', 'Manufacturing', 'Healthcare Support']
    immigrant_share = [25, 45, 22, 18, 24]  # Approximate percentages

    colors = [ACCENT if s >= 25 else ACCENT_LIGHT for s in immigrant_share]

    bars = ax.barh(sectors, immigrant_share, color=colors, height=0.6)

    for bar, val in zip(bars, immigrant_share):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{val}%', ha='left', va='center', fontsize=12, fontweight='600', color=TEXT)

    ax.set_xlabel('Immigrant Share of Workforce (%)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Immigrant Labor Concentration by Sector',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xlim(0, 55)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)

    # Construction shortage callout
    ax.annotate('500,000 worker\nshortfall projected', xy=(25, 4), xytext=(40, 3.5),
                fontsize=10, color=NEGATIVE, fontweight='500',
                arrowprops=dict(arrowstyle='->', color=NEGATIVE, lw=1.5))

    fig.text(0.99, 0.02, 'Source: Center for Migration Studies (2024)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-labor-sectors.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-labor-sectors.png")


if __name__ == "__main__":
    chart_tax_contributions()
    chart_gdp_scenarios()
    chart_fiscal_debate()
    chart_labor_sectors()
    print("\nAll charts generated successfully!")
