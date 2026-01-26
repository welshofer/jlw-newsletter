#!/usr/bin/env python3
"""
US Population Demographics Charts for Newsletter
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Newsletter color scheme - terracotta theme
ACCENT = '#B85C38'
ACCENT_LIGHT = '#D4816A'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
TEAL = '#0D6E8A'
INDIGO = '#5B4B8A'

# Set global font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif']

def chart_population_projection():
    """US Population Growth 2024-2054"""
    years = [2024, 2030, 2035, 2040, 2045, 2050, 2054]
    population = [342, 353, 362, 370, 376, 381, 383]  # in millions

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Main line
    ax.plot(years, population, color=ACCENT, linewidth=3, marker='o', markersize=8, markerfacecolor=ACCENT)

    # Fill under curve
    ax.fill_between(years, population, alpha=0.15, color=ACCENT)

    # Annotations
    ax.annotate('342M\n(Today)', xy=(2024, 342), xytext=(2024, 335),
                fontsize=10, color=ACCENT, ha='center', fontweight='600')
    ax.annotate('383M\n(2054)', xy=(2054, 383), xytext=(2054, 390),
                fontsize=10, color=ACCENT, ha='center', fontweight='600')

    # Growth rate annotation
    ax.annotate('Annual growth: 0.4%\n(down from 0.9% historically)',
                xy=(2039, 368), fontsize=9, color=TEXT_SECONDARY, ha='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=BG, edgecolor=GRID))

    ax.set_title('US Population Projection: 2024–2054', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('Population (millions)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylim(330, 400)
    ax.set_xlim(2022, 2056)

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{int(x)}M'))
    ax.grid(True, alpha=0.5, color=GRID, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    fig.text(0.99, 0.02, 'Source: Congressional Budget Office (2024)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-population-projection.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-population-projection.png")


def chart_age_distribution():
    """Age Distribution Shift: 2024 vs 2054"""
    categories = ['Under 18', '18-64', '65+']
    pop_2024 = [22, 62, 16]  # percentages
    pop_2054 = [19, 58, 23]  # percentages

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    bars1 = ax.bar(x - width/2, pop_2024, width, label='2024', color=ACCENT_LIGHT)
    bars2 = ax.bar(x + width/2, pop_2054, width, label='2054', color=ACCENT)

    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height}%', xy=(bar.get_x() + bar.get_width()/2, height),
                   xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                   fontsize=11, color=TEXT_SECONDARY, fontweight='500')

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height}%', xy=(bar.get_x() + bar.get_width()/2, height),
                   xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                   fontsize=11, color=TEXT, fontweight='600')

    ax.set_title('The Graying of America: Age Distribution Shift', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_ylabel('Share of Population (%)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=12)
    ax.legend(loc='upper right', frameon=True, facecolor=BG, edgecolor=GRID)
    ax.set_ylim(0, 75)

    ax.grid(True, alpha=0.5, color=GRID, linestyle='--', axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    # Key insight annotation
    ax.annotate('65+ nearly doubles\nfrom 55M to 84M', xy=(2.2, 23), xytext=(2.2, 45),
                fontsize=10, color=ACCENT, ha='center',
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

    fig.text(0.99, 0.02, 'Source: US Census Bureau', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-age-distribution.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-age-distribution.png")


def chart_racial_composition():
    """Racial/Ethnic Composition: 2024 vs 2060"""
    categories = ['White\n(non-Hispanic)', 'Hispanic', 'Black', 'Asian', 'Other/\nMultiracial']

    # Percentages
    pop_2024 = [58, 19, 12, 6, 5]
    pop_2060 = [44, 27, 13, 9, 7]

    y = np.arange(len(categories))
    height = 0.35

    fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
    ax.set_facecolor(BG)

    bars1 = ax.barh(y + height/2, pop_2024, height, label='2024', color=ACCENT_LIGHT)
    bars2 = ax.barh(y - height/2, pop_2060, height, label='2060', color=ACCENT)

    # Add value labels
    for bar in bars1:
        width = bar.get_width()
        ax.annotate(f'{width}%', xy=(width, bar.get_y() + bar.get_height()/2),
                   xytext=(5, 0), textcoords="offset points", ha='left', va='center',
                   fontsize=10, color=TEXT_SECONDARY)

    for bar in bars2:
        width = bar.get_width()
        ax.annotate(f'{width}%', xy=(width, bar.get_y() + bar.get_height()/2),
                   xytext=(5, 0), textcoords="offset points", ha='left', va='center',
                   fontsize=10, color=TEXT, fontweight='600')

    ax.set_title('Majority-Minority America: Racial/Ethnic Composition', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xlabel('Share of Population (%)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_yticks(y)
    ax.set_yticklabels(categories, fontsize=11)
    ax.legend(loc='upper right', frameon=True, facecolor=BG, edgecolor=GRID)
    ax.set_xlim(0, 70)

    ax.grid(True, alpha=0.5, color=GRID, linestyle='--', axis='x')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    # Add "No majority" annotation
    ax.axvline(x=50, color=INDIGO, linestyle='--', alpha=0.7, linewidth=2)
    ax.annotate('50% threshold', xy=(50, 4.7), fontsize=9, color=INDIGO, ha='center')

    fig.text(0.99, 0.02, 'Source: US Census Bureau, Pew Research Center', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-racial-composition.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-racial-composition.png")


def chart_global_comparison():
    """Global Population Change: 2024 vs 2050"""
    countries = ['United States', 'China', 'Japan', 'European Union']

    # Population in millions
    pop_2024 = [342, 1425, 125, 447]
    pop_2050 = [383, 1313, 100, 419]

    # Calculate change
    change = [p2 - p1 for p1, p2 in zip(pop_2024, pop_2050)]
    colors = [ACCENT if c > 0 else TEAL for c in change]

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    x = np.arange(len(countries))
    bars = ax.bar(x, change, color=colors, width=0.6)

    # Add value labels
    for i, (bar, c) in enumerate(zip(bars, change)):
        height = bar.get_height()
        label = f'+{c}M' if c > 0 else f'{c}M'
        y_pos = height + 3 if c > 0 else height - 8
        ax.annotate(label, xy=(bar.get_x() + bar.get_width()/2, y_pos),
                   ha='center', va='bottom' if c > 0 else 'top',
                   fontsize=12, color=TEXT, fontweight='600')

    ax.axhline(y=0, color=TEXT_SECONDARY, linewidth=1)

    ax.set_title('Global Demographic Advantage: Population Change 2024-2050',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_ylabel('Population Change (millions)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_xticks(x)
    ax.set_xticklabels(countries, fontsize=11)
    ax.set_ylim(-130, 60)

    ax.grid(True, alpha=0.5, color=GRID, linestyle='--', axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=ACCENT, label='Growth'),
                       Patch(facecolor=TEAL, label='Decline')]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True, facecolor=BG, edgecolor=GRID)

    fig.text(0.99, 0.02, 'Source: United Nations, CBO', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-global-comparison.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-global-comparison.png")


def chart_fertility_rate():
    """US Total Fertility Rate: Historical and Projected"""
    years = [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2024, 2030, 2040, 2054]
    tfr = [3.65, 2.48, 1.84, 2.08, 2.06, 1.93, 1.64, 1.62, 1.70, 1.70, 1.70]

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Split into historical and projected
    hist_years = years[:8]
    hist_tfr = tfr[:8]
    proj_years = years[7:]
    proj_tfr = tfr[7:]

    ax.plot(hist_years, hist_tfr, color=ACCENT, linewidth=3, marker='o', markersize=6, label='Historical')
    ax.plot(proj_years, proj_tfr, color=ACCENT, linewidth=3, linestyle='--', marker='s', markersize=6, label='Projected')

    # Replacement rate line
    ax.axhline(y=2.1, color=INDIGO, linestyle='--', linewidth=2, alpha=0.7)
    ax.annotate('Replacement rate (2.1)', xy=(2040, 2.15), fontsize=10, color=INDIGO)

    # Current rate annotation
    ax.annotate('1.62\n(2024)', xy=(2024, 1.62), xytext=(2010, 1.3),
                fontsize=10, color=ACCENT, fontweight='600',
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

    ax.set_title('Fertility Rate: Below Replacement Since 1972', fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('Births per Woman (TFR)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylim(1.0, 4.0)
    ax.set_xlim(1955, 2060)

    ax.legend(loc='upper right', frameon=True, facecolor=BG, edgecolor=GRID)
    ax.grid(True, alpha=0.5, color=GRID, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

    fig.text(0.99, 0.02, 'Source: Congressional Budget Office (2024)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-fertility-rate.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-fertility-rate.png")


if __name__ == '__main__':
    chart_population_projection()
    chart_age_distribution()
    chart_racial_composition()
    chart_global_comparison()
    chart_fertility_rate()
    print("\nAll charts generated successfully!")
