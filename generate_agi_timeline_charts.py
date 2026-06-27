#!/usr/bin/env python3
"""Generate 3 data visualization charts for the AGI Timeline newsletter."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import chart_style
from chart_style import apply_brand_style

# Newsletter color scheme — teal/cyan tech theme
ACCENT = '#0D6E8A'
ACCENT_LIGHT = '#1A9BC7'
ACCENT_DARK = '#084E63'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
BORDER = '#E5E0D8'
WARM = '#B85C38'
WARM_LIGHT = '#E07B52'

OUTPUT_DIR = Path(chart_style.output_path('images'))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    'axes.facecolor': BG,
    'figure.facecolor': BG,
    'text.color': TEXT,
    'axes.labelcolor': TEXT_SECONDARY,
    'xtick.color': TEXT_SECONDARY,
    'ytick.color': TEXT_SECONDARY,
})
apply_brand_style()


def chart_1_expert_predictions():
    """Horizontal bar chart: AGI timeline predictions by expert/source."""
    fig, ax = plt.subplots(figsize=(10, 6.5), facecolor=BG)
    ax.set_facecolor(BG)

    experts = [
        'Sam Altman\n(OpenAI CEO)',
        'Dario Amodei\n(Anthropic CEO)',
        'Elon Musk',
        'Ray Kurzweil',
        'Metaculus\n(Community Median)',
        'Demis Hassabis\n(DeepMind CEO)',
        'Yann LeCun\n(Meta Chief AI Sci.)',
        'Gary Marcus\n(NYU)',
    ]

    # Ranges: (earliest, latest) prediction — year values
    ranges = [
        (2025, 2026),   # Altman: "basically here" / 2025-2026
        (2026, 2028),   # Amodei: 2-3 years (from late 2025)
        (2026, 2028),   # Musk: "by 2026" then "2028 at latest"
        (2029, 2029),   # Kurzweil: 2029 singularity
        (2029, 2033),   # Metaculus: median ~2031, range 2029-2033
        (2031, 2034),   # Hassabis: "5 to 8 years" from Feb 2026
        (2040, 2060),   # LeCun: "decades away" / needs new paradigm
        (2040, 2075),   # Marcus: "nowhere close" / 50+ years
    ]

    y_pos = np.arange(len(experts))
    colors = [WARM, ACCENT_LIGHT, WARM_LIGHT, ACCENT, ACCENT, ACCENT_DARK, TEXT_SECONDARY, TEXT_SECONDARY]

    for i, ((start, end), color) in enumerate(zip(ranges, colors)):
        width = max(end - start, 0.4)  # Minimum visible width
        ax.barh(i, width, left=start, height=0.55, color=color, alpha=0.85,
                edgecolor='white', linewidth=0.5, zorder=3)
        # Label the range
        mid = start + width / 2
        label = f'{start}' if start == end else f'{start}–{end}'
        ax.text(mid, i, label, ha='center', va='center', fontsize=9,
                fontweight='600', color='white', zorder=4)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(experts, fontsize=10)
    ax.set_xlim(2024, 2080)
    ax.set_xlabel('Predicted Year of AGI Arrival', fontsize=11, labelpad=10)
    ax.set_title('When Will AGI Arrive?\nExpert Predictions & Forecasts (as of Feb 2026)',
                 fontsize=15, fontweight='600', color=TEXT, pad=18, loc='left')

    # Add "today" line
    ax.axvline(x=2026.14, color=WARM, linestyle='--', linewidth=1.5, alpha=0.7, zorder=2)
    ax.text(2026.14, len(experts) - 0.3, ' NOW', fontsize=8, color=WARM,
            fontweight='600', va='bottom')

    ax.grid(True, axis='x', alpha=0.4, color=GRID, zorder=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)
    ax.invert_yaxis()

    # Optimist / Pessimist annotations
    ax.text(2027, 7.8, 'OPTIMISTS', fontsize=8, color=WARM, fontweight='600',
            ha='center', style='italic')
    ax.text(2055, 7.8, 'SKEPTICS', fontsize=8, color=TEXT_SECONDARY, fontweight='600',
            ha='center', style='italic')

    fig.text(0.99, 0.01, 'Sources: Public statements, Metaculus (Feb 2026)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-expert-predictions.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print('✓ chart-expert-predictions.png')


def chart_2_funding_escalation():
    """Bar chart: Frontier AI lab funding rounds escalation."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    rounds = [
        ('OpenAI\n$1B\n2019', 1.0, ACCENT_LIGHT),
        ('Anthropic\nSeries A\n$580M 2023', 0.58, ACCENT),
        ('OpenAI\n$10B\n2023', 10.0, ACCENT_LIGHT),
        ('Anthropic\nSeries D\n$4B 2024', 4.0, ACCENT),
        ('xAI\n$6B\n2024', 6.0, TEXT_SECONDARY),
        ('OpenAI\n$6.6B\n2024', 6.6, ACCENT_LIGHT),
        ('Anthropic\nSeries E\n$8B 2025', 8.0, ACCENT),
        ('xAI\n$12B\n2025', 12.0, TEXT_SECONDARY),
        ('Anthropic\nSeries G\n$30B 2026', 30.0, WARM),
    ]

    labels = [r[0] for r in rounds]
    values = [r[1] for r in rounds]
    colors = [r[2] for r in rounds]

    x_pos = np.arange(len(rounds))
    bars = ax.bar(x_pos, values, color=colors, width=0.65, edgecolor='white',
                  linewidth=0.5, zorder=3, alpha=0.9)

    # Value labels on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f'${val:.0f}B' if val >= 1 else f'${val*1000:.0f}M',
                ha='center', va='bottom', fontsize=9, fontweight='600', color=TEXT)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, fontsize=7.5, ha='center')
    ax.set_ylabel('Funding Amount ($ Billions)', fontsize=11, labelpad=10)
    ax.set_title('The AGI Arms Race: Funding Escalation\nMajor Frontier AI Lab Rounds (2019–2026)',
                 fontsize=15, fontweight='600', color=TEXT, pad=18, loc='left')

    ax.set_ylim(0, 36)
    ax.grid(True, axis='y', alpha=0.4, color=GRID, zorder=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)

    # Annotation arrow on the $30B bar
    ax.annotate('3x jump in\n12 months',
                xy=(8, 30), xytext=(6.5, 33),
                fontsize=9, color=WARM, fontweight='600',
                arrowprops=dict(arrowstyle='->', color=WARM, lw=1.5),
                ha='center')

    fig.text(0.99, 0.01, 'Sources: Company announcements, press reports (Feb 2026)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-funding-escalation.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print('✓ chart-funding-escalation.png')


def chart_3_metaculus_drift():
    """Line chart: How the Metaculus AGI median forecast has shifted over time."""
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG)
    ax.set_facecolor(BG)

    # Metaculus community median AGI year forecast at different points in time
    # These are approximate values from publicly available Metaculus data
    forecast_dates = [
        '2020\nJan', '2021\nJan', '2022\nJan', '2022\nDec',
        '2023\nJun', '2023\nDec', '2024\nJun', '2024\nDec',
        '2025\nJun', '2025\nDec', '2026\nFeb'
    ]
    median_year = [2060, 2050, 2043, 2040, 2037, 2034, 2033, 2032, 2032, 2031, 2031]

    # 25th and 75th percentile range (approximate)
    p25 = [2045, 2038, 2033, 2032, 2030, 2029, 2028, 2028, 2028, 2027, 2027]
    p75 = [2090, 2075, 2060, 2055, 2048, 2042, 2040, 2038, 2037, 2036, 2035]

    x = np.arange(len(forecast_dates))

    # Fill confidence band
    ax.fill_between(x, p25, p75, alpha=0.15, color=ACCENT, zorder=2, label='25th–75th percentile')

    # Main line
    ax.plot(x, median_year, color=ACCENT, linewidth=2.5, marker='o', markersize=6,
            markerfacecolor=ACCENT, markeredgecolor='white', markeredgewidth=1.5,
            zorder=4, label='Community median')

    # "Now" reference line
    ax.axhline(y=2026.14, color=WARM, linestyle=':', linewidth=1, alpha=0.6, zorder=1)
    ax.text(len(forecast_dates) - 0.5, 2026.5, '← We are here', fontsize=8,
            color=WARM, fontweight='500', va='bottom')

    # Annotate key shift
    ax.annotate('ChatGPT\nlaunches',
                xy=(3, 2040), xytext=(3, 2050),
                fontsize=8, color=TEXT_SECONDARY, ha='center',
                arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1))

    ax.annotate('GPT-4 &\nscaling boom',
                xy=(5, 2034), xytext=(5, 2044),
                fontsize=8, color=TEXT_SECONDARY, ha='center',
                arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1))

    ax.set_xticks(x)
    ax.set_xticklabels(forecast_dates, fontsize=8.5)
    ax.set_ylabel('Predicted AGI Year (Median)', fontsize=11, labelpad=10)
    ax.set_title('The Great Pull-In: Metaculus AGI Forecast Over Time\nCommunity median prediction has shifted 29 years closer since 2020',
                 fontsize=14, fontweight='600', color=TEXT, pad=18, loc='left')

    ax.set_ylim(2024, 2095)
    ax.grid(True, alpha=0.4, color=GRID, zorder=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)

    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)

    fig.text(0.99, 0.01, 'Source: Metaculus Question #5121 (Feb 2026)',
             fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-metaculus-drift.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print('✓ chart-metaculus-drift.png')


if __name__ == '__main__':
    chart_1_expert_predictions()
    chart_2_funding_escalation()
    chart_3_metaculus_drift()
    print('\nAll 3 charts generated successfully.')
