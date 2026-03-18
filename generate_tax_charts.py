#!/usr/bin/env python3
"""Generate data visualizations for the US Tax Rates newsletter."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

# Newsletter color scheme — indigo/gold for fiscal gravitas
ACCENT = '#3D3B8A'       # Deep indigo
ACCENT2 = '#C49B3A'      # Warm gold
BG = '#FDFBF7'           # Cream background
TEXT = '#1A1815'          # Dark text
TEXT_SEC = '#4D5C6A'      # Secondary text
GRID = '#D8E2E8'         # Grid lines
RED = '#B85C38'          # Terracotta for deficit
GREEN = '#4A8C5C'        # Green for surplus

OUTPUT_DIR = os.path.expanduser('~/clawd/jlw-newsletter/images')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def chart1_top_marginal_rate_timeline():
    """Chart 1: Top marginal income tax rate, 1975-2026."""
    years = [1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984,
             1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994,
             1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004,
             2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
             2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024,
             2025, 2026]
    rates = [70, 70, 70, 70, 70, 70, 70, 50, 50, 50,
             50, 50, 38.5, 28, 28, 28, 31, 31, 39.6, 39.6,
             39.6, 39.6, 39.6, 39.6, 39.6, 39.6, 39.1, 38.6, 35, 35,
             35, 35, 35, 35, 35, 35, 35, 35, 39.6, 39.6,
             39.6, 39.6, 39.6, 37, 37, 37, 37, 37, 37, 37,
             37, 37]

    fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Fill area under line
    ax.fill_between(years, rates, alpha=0.15, color=ACCENT)
    ax.plot(years, rates, color=ACCENT, linewidth=2.5, zorder=5)

    # Annotate key legislation
    annotations = [
        (1981, 70, 'ERTA 1981\n70% → 50%', (-60, 15)),
        (1988, 28, 'TRA 1986\n→ 28%', (-50, -35)),
        (1993, 39.6, 'OBRA 1993\n→ 39.6%', (10, 15)),
        (2003, 35, 'JGTRRA 2003\n→ 35%', (10, -30)),
        (2013, 39.6, 'ATRA 2012\n→ 39.6%', (10, 15)),
        (2018, 37, 'TCJA 2017\n→ 37%', (10, -30)),
        (2025, 37, 'OBBBA 2025\nPermanent', (-80, -30)),
    ]

    for yr, rate, label, offset in annotations:
        ax.annotate(label, (yr, rate),
                    xytext=offset, textcoords='offset points',
                    fontsize=8, color=ACCENT, fontweight='500',
                    ha='left',
                    arrowprops=dict(arrowstyle='->', color=ACCENT, lw=0.8),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor=GRID, alpha=0.9))

    ax.set_title('Top Marginal Federal Income Tax Rate (1975–2026)',
                 fontsize=16, color=TEXT, fontweight='600', pad=20,
                 fontfamily='serif')
    ax.set_xlabel('Year', fontsize=11, color=TEXT_SEC)
    ax.set_ylabel('Top Marginal Rate (%)', fontsize=11, color=TEXT_SEC)
    ax.set_ylim(20, 80)
    ax.set_xlim(1975, 2026)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.grid(True, alpha=0.4, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SEC)

    fig.text(0.99, 0.02, 'Source: IRS, Tax Policy Center, Tax Foundation',
             fontsize=8, color=TEXT_SEC, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/chart-top-marginal-rate-timeline.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print('✓ Chart 1: Top marginal rate timeline')


def chart2_bracket_comparison():
    """Chart 2: Compare all tax brackets across key years."""
    # Key years and their bracket structures (married filing jointly thresholds simplified)
    eras = {
        '1980\n(Pre-Reagan)': [14, 16, 18, 20, 22, 25, 28, 32, 36, 39, 42, 45, 48, 50, 53, 55, 58, 60, 62, 64, 66, 68, 70],
        '1988\n(Post-TRA)': [15, 28],
        '1993\n(Pre-Clinton)': [15, 28, 31],
        '2000\n(Clinton)': [15, 28, 31, 36, 39.6],
        '2008\n(Bush)': [10, 15, 25, 28, 33, 35],
        '2016\n(Obama)': [10, 15, 25, 28, 33, 35, 39.6],
        '2024\n(TCJA)': [10, 12, 22, 24, 32, 35, 37],
    }

    fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
    ax.set_facecolor(BG)

    x_positions = np.arange(len(eras))
    bar_width = 0.7
    cmap = plt.cm.RdYlGn_r  # Red for high rates, green for low

    for i, (era, brackets) in enumerate(eras.items()):
        bottom = 0
        for j, rate in enumerate(brackets):
            height = rate / len(brackets)  # Equal visual height per bracket
            color_val = rate / 70.0  # Normalize to 0-1
            color = cmap(color_val)
            ax.bar(i, height, bottom=bottom, width=bar_width,
                   color=color, edgecolor='white', linewidth=0.5, alpha=0.85)
            if len(brackets) <= 7:  # Only label if not too many brackets
                ax.text(i, bottom + height/2, f'{rate}%',
                        ha='center', va='center', fontsize=7, color='white',
                        fontweight='bold')
            bottom += height

        # Label top rate
        ax.text(i, bottom + 0.3, f'Top: {brackets[-1]}%',
                ha='center', va='bottom', fontsize=9, color=ACCENT,
                fontweight='600')

    # Number of brackets annotation
    for i, (era, brackets) in enumerate(eras.items()):
        ax.text(i, -0.8, f'{len(brackets)} brackets',
                ha='center', va='top', fontsize=8, color=TEXT_SEC)

    ax.set_xticks(x_positions)
    ax.set_xticklabels(eras.keys(), fontsize=9, color=TEXT)
    ax.set_title('Federal Income Tax Bracket Structures Across Eras',
                 fontsize=16, color=TEXT, fontweight='600', pad=20,
                 fontfamily='serif')
    ax.set_ylabel('Relative Bracket Distribution', fontsize=11, color=TEXT_SEC)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(left=False, labelleft=False, colors=TEXT_SEC)
    ax.set_ylim(-1.2, max(sum(r/len(b) for r in b) for b in eras.values()) + 2)

    fig.text(0.99, 0.02, 'Source: IRS Historical Data, Tax Foundation',
             fontsize=8, color=TEXT_SEC, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/chart-bracket-structures.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print('✓ Chart 2: Bracket structure comparison')


def chart3_effective_vs_marginal():
    """Chart 3: Top marginal rate vs effective rate for top 1%."""
    years = [1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]
    marginal = [70, 70, 50, 28, 39.6, 39.6, 35, 35, 39.6, 37, 37]
    # Effective rates for top 1% (approximate, from CBO/TPC data)
    effective = [35.0, 34.5, 24.4, 23.3, 28.9, 27.5, 23.1, 23.4, 27.1, 25.6, 26.1]

    fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
    ax.set_facecolor(BG)

    ax.fill_between(years, marginal, effective, alpha=0.12, color=ACCENT,
                    label='Gap (deductions, credits, capital gains)')
    ax.plot(years, marginal, color=ACCENT, linewidth=2.5, marker='o',
            markersize=6, label='Top Marginal Rate', zorder=5)
    ax.plot(years, effective, color=ACCENT2, linewidth=2.5, marker='s',
            markersize=6, label='Effective Rate (Top 1%)', zorder=5)

    # Annotate the gap
    for i, yr in enumerate(years):
        gap = marginal[i] - effective[i]
        if i % 2 == 0:
            mid = (marginal[i] + effective[i]) / 2
            ax.annotate(f'{gap:.0f}pp gap', (yr, mid),
                        fontsize=7, color=TEXT_SEC, ha='center',
                        style='italic')

    ax.set_title('The Tax Rate Illusion: Marginal vs. Effective Rates',
                 fontsize=16, color=TEXT, fontweight='600', pad=20,
                 fontfamily='serif')
    ax.set_xlabel('Year', fontsize=11, color=TEXT_SEC)
    ax.set_ylabel('Tax Rate (%)', fontsize=11, color=TEXT_SEC)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.set_ylim(15, 75)
    ax.legend(fontsize=10, frameon=True, facecolor=BG, edgecolor=GRID,
              loc='upper right')
    ax.grid(True, alpha=0.4, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SEC)

    fig.text(0.99, 0.02, 'Source: CBO, Tax Policy Center (effective rates approximate)',
             fontsize=8, color=TEXT_SEC, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/chart-effective-vs-marginal.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print('✓ Chart 3: Effective vs marginal rates')


def chart4_revenue_pct_gdp():
    """Chart 4: Federal revenue as % of GDP — the Hauser's Law stability."""
    years = [1975, 1977, 1979, 1981, 1983, 1985, 1987, 1989, 1991, 1993,
             1995, 1997, 1999, 2000, 2001, 2003, 2005, 2007, 2009, 2010,
             2012, 2014, 2016, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    # Federal receipts as % of GDP (from OMB/CBO historical tables)
    revenue = [17.3, 17.5, 18.5, 19.6, 17.4, 17.7, 18.4, 18.3, 17.8, 17.5,
               18.4, 19.2, 19.8, 20.0, 19.1, 16.2, 17.3, 18.0, 14.6, 15.1,
               15.2, 17.5, 17.6, 16.4, 16.3, 16.3, 18.1, 19.6, 18.1, 17.5]
    # Budget surplus/deficit as % of GDP
    balance = [-3.3, -2.7, -1.6, -2.5, -5.9, -5.0, -3.1, -2.8, -4.5, -3.8,
               -2.2, -0.3, 0.9, 1.2, -1.3, -3.4, -2.5, -1.1, -9.8, -8.7,
               -6.8, -2.8, -3.1, -3.8, -4.6, -14.7, -12.1, -5.5, -6.3, -6.4]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), facecolor=BG,
                                     height_ratios=[1, 1], sharex=True)

    for ax in [ax1, ax2]:
        ax.set_facecolor(BG)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(GRID)
        ax.spines['bottom'].set_color(GRID)
        ax.tick_params(colors=TEXT_SEC)
        ax.grid(True, alpha=0.4, color=GRID)

    # Top: Revenue as % of GDP
    ax1.fill_between(years, revenue, alpha=0.15, color=ACCENT)
    ax1.plot(years, revenue, color=ACCENT, linewidth=2.5, zorder=5)
    ax1.axhline(y=17.8, color=ACCENT2, linestyle='--', linewidth=1, alpha=0.7)
    ax1.text(2024.5, 18.0, '50-year avg: 17.8%', fontsize=8, color=ACCENT2,
             ha='right', style='italic')
    ax1.set_ylabel('Federal Revenue (% of GDP)', fontsize=11, color=TEXT_SEC)
    ax1.set_title('Federal Revenue & Budget Balance as % of GDP (1975–2024)',
                  fontsize=16, color=TEXT, fontweight='600', pad=20,
                  fontfamily='serif')
    ax1.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax1.set_ylim(13, 22)

    # Bottom: Budget balance
    colors = [GREEN if b >= 0 else RED for b in balance]
    ax2.bar(years, balance, color=colors, alpha=0.7, width=1.5)
    ax2.axhline(y=0, color=TEXT, linewidth=0.8)
    ax2.set_ylabel('Budget Balance (% of GDP)', fontsize=11, color=TEXT_SEC)
    ax2.set_xlabel('Year', fontsize=11, color=TEXT_SEC)
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))

    # Annotate key moments
    ax2.annotate('Clinton\nsurpluses', (2000, 1.2), fontsize=8, color=GREEN,
                 ha='center', fontweight='500')
    ax2.annotate('COVID\n-14.7%', (2020, -14.7), xytext=(2017, -13),
                 fontsize=8, color=RED, fontweight='500',
                 arrowprops=dict(arrowstyle='->', color=RED, lw=0.8))

    fig.text(0.99, 0.02, 'Source: OMB Historical Tables, CBO',
             fontsize=8, color=TEXT_SEC, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/chart-revenue-and-balance-gdp.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print('✓ Chart 4: Revenue and balance as % of GDP')


def chart5_2026_brackets():
    """Chart 5: Current 2026 tax brackets (OBBBA permanent rates)."""
    brackets_single = [
        ('$0 – $11,925', 10),
        ('$11,926 – $48,475', 12),
        ('$48,476 – $103,350', 22),
        ('$103,351 – $197,300', 24),
        ('$197,301 – $250,525', 32),
        ('$250,526 – $626,350', 35),
        ('$626,351+', 37),
    ]

    fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
    ax.set_facecolor(BG)

    # Use indigo gradient
    colors = plt.cm.Purples(np.linspace(0.2, 0.85, len(brackets_single)))

    y_pos = np.arange(len(brackets_single))
    rates = [b[1] for b in brackets_single]
    labels = [b[0] for b in brackets_single]

    bars = ax.barh(y_pos, rates, color=colors, edgecolor='white', linewidth=1,
                   height=0.7)

    # Add rate labels on bars
    for i, (bar, rate) in enumerate(zip(bars, rates)):
        ax.text(bar.get_width() - 1, bar.get_y() + bar.get_height()/2,
                f'{rate}%', ha='right', va='center', fontsize=14,
                color='white', fontweight='bold')

    # Add income range labels
    for i, label in enumerate(labels):
        ax.text(0.5, i, label, ha='left', va='center', fontsize=10,
                color='white', fontweight='500')

    ax.set_yticks([])
    ax.set_xlabel('Tax Rate (%)', fontsize=11, color=TEXT_SEC)
    ax.set_title('2026 Federal Income Tax Brackets (Single Filer)',
                 fontsize=16, color=TEXT, fontweight='600', pad=20,
                 fontfamily='serif')
    ax.set_xlim(0, 42)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SEC, left=False)

    # Subtitle
    ax.text(0.5, -0.08, 'Rates made permanent by the One Big Beautiful Bill Act (July 2025)',
            transform=ax.transAxes, fontsize=10, color=TEXT_SEC, ha='center',
            style='italic')

    fig.text(0.99, 0.02, 'Source: IRS Revenue Procedure 2025-11, Tax Foundation',
             fontsize=8, color=TEXT_SEC, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/chart-2026-brackets.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print('✓ Chart 5: 2026 tax brackets')


if __name__ == '__main__':
    print('Generating tax rate newsletter charts...')
    chart1_top_marginal_rate_timeline()
    chart2_bracket_comparison()
    chart3_effective_vs_marginal()
    chart4_revenue_pct_gdp()
    chart5_2026_brackets()
    print('\nAll charts generated successfully!')
