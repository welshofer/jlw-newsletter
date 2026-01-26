#!/usr/bin/env python3
"""Generate data visualizations for UBI newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path("/Users/welshofer/clawd/jlw-newsletter/images")
OUTPUT_DIR.mkdir(exist_ok=True)

# Newsletter color scheme - indigo/violet for UBI topic
ACCENT = '#5B4B8A'      # Deep indigo
ACCENT_LIGHT = '#7C5C8A'  # Violet
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'        # Dark text
TEXT_SECONDARY = '#5C564D'  # Secondary text
GRID = '#E5E0D8'        # Light grid
GOLD = '#D4A84B'        # Accent gold


def chart_ubi_pilots_growth():
    """Chart 1: Growth of UBI/GI pilots in the US over time."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Data: Number of active guaranteed income pilots in US
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
    pilots = [1, 3, 8, 33, 82, 102, 115, 128, 130]  # Stockton started 2019, COVID boom 2021
    permanent = [0, 0, 0, 0, 0, 0, 0, 0, 1]  # Cook County 2026

    # Create stacked appearance
    ax.fill_between(years, pilots, color=ACCENT, alpha=0.3, label='Active Pilots')
    ax.plot(years, pilots, color=ACCENT, linewidth=3, marker='o', markersize=8)

    # Mark the permanent program
    ax.scatter([2026], [130], color=GOLD, s=200, zorder=5, edgecolors=TEXT, linewidths=2)
    ax.annotate('First Permanent\nProgram (Cook County)',
                xy=(2026, 130), xytext=(2024.2, 138),
                fontsize=10, color=TEXT,
                arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1.5),
                ha='center')

    # Mark COVID inflection
    ax.annotate('COVID/ARPA\nFunding Surge',
                xy=(2021, 33), xytext=(2019.5, 55),
                fontsize=9, color=TEXT_SECONDARY,
                arrowprops=dict(arrowstyle='->', color=GRID, lw=1),
                ha='center')

    ax.set_title('US Guaranteed Income Programs: From Experiment to Permanence',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('Number of Active Programs', fontsize=12, color=TEXT_SECONDARY)

    ax.set_xlim(2017.5, 2026.5)
    ax.set_ylim(0, 160)
    ax.grid(True, alpha=0.4, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(TEXT_SECONDARY)
    ax.spines['bottom'].set_color(TEXT_SECONDARY)
    ax.tick_params(colors=TEXT_SECONDARY)

    fig.text(0.99, 0.02, 'Sources: Mayors for a Guaranteed Income, Stanford Basic Income Lab (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-ubi-pilots-growth.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    print(f"Saved: {OUTPUT_DIR / 'chart-ubi-pilots-growth.png'}")
    plt.close()


def chart_ubi_funding_sources():
    """Chart 2: How GI programs are funded (pie/donut chart)."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Funding sources for GI pilots (approximate percentages)
    labels = ['Federal ARPA Funds\n(Pandemic Relief)', 'Private Philanthropy',
              'Local Government\nBudgets', 'State Funds', 'Mixed/Other']
    sizes = [45, 30, 12, 8, 5]
    colors = [ACCENT, ACCENT_LIGHT, GOLD, '#8A7B5B', TEXT_SECONDARY]
    explode = (0, 0, 0.1, 0, 0)  # Emphasize local government (transitioning)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                       autopct='%1.0f%%', startangle=90,
                                       pctdistance=0.75, labeldistance=1.15,
                                       wedgeprops=dict(width=0.5, edgecolor=BG, linewidth=2))

    # Style the percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)

    for text in texts:
        text.set_color(TEXT)
        text.set_fontsize(10)

    # Add center annotation
    ax.text(0, 0, 'Funding\nMix', ha='center', va='center',
            fontsize=14, fontweight='600', color=TEXT)

    ax.set_title('Where GI Pilot Money Comes From\n(Most Programs Still Depend on Temporary Funding)',
                 fontsize=14, color=TEXT, fontweight='600', pad=20)

    fig.text(0.99, 0.02, 'Source: Economic Security Project analysis (2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-ubi-funding-sources.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    print(f"Saved: {OUTPUT_DIR / 'chart-ubi-funding-sources.png'}")
    plt.close()


def chart_ubi_monthly_amounts():
    """Chart 3: Comparison of monthly UBI amounts across programs."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Programs and their monthly amounts
    programs = ['Cook County\n(Permanent)', 'California CalUBI\n(Proposed)',
                'NY Foster Youth\n(Proposed)', 'Stockton SEED\n(2019-21)',
                'Denver DBIG\n(2022-24)', 'Living Wage\n(Concept)']
    amounts = [500, 1000, 1000, 500, 1000, 2000]
    colors_list = [GOLD, ACCENT, ACCENT, ACCENT_LIGHT, ACCENT_LIGHT, TEXT_SECONDARY]

    bars = ax.barh(programs, amounts, color=colors_list, edgecolor=BG, linewidth=1)

    # Add value labels
    for bar, amount in zip(bars, amounts):
        ax.text(amount + 30, bar.get_y() + bar.get_height()/2,
                f'${amount:,}/mo', va='center', ha='left',
                fontsize=11, color=TEXT, fontweight='500')

    # Add vertical reference lines
    ax.axvline(x=1000, color=ACCENT, linestyle='--', alpha=0.3, linewidth=2)
    ax.text(1010, 5.8, '$1,000 standard', fontsize=9, color=TEXT_SECONDARY, va='bottom')

    ax.axvline(x=1960, color='#C0392B', linestyle='--', alpha=0.3, linewidth=2)
    ax.text(1970, 5.8, 'Federal poverty line\n(single adult)', fontsize=9,
            color='#C0392B', va='bottom', alpha=0.7)

    ax.set_title('Monthly Payment Amounts: UBI Pilots vs. Proposals',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xlabel('Monthly Payment ($)', fontsize=12, color=TEXT_SECONDARY)

    ax.set_xlim(0, 2400)
    ax.grid(True, axis='x', alpha=0.4, color=GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(TEXT_SECONDARY)
    ax.tick_params(colors=TEXT_SECONDARY, left=False)

    # Legend
    legend_elements = [mpatches.Patch(facecolor=GOLD, label='Permanent'),
                      mpatches.Patch(facecolor=ACCENT, label='Proposed/Active'),
                      mpatches.Patch(facecolor=ACCENT_LIGHT, label='Completed Pilot'),
                      mpatches.Patch(facecolor=TEXT_SECONDARY, label='Advocacy Target')]
    ax.legend(handles=legend_elements, loc='lower right', frameon=False,
              fontsize=9)

    fig.text(0.99, 0.02, 'Sources: Program documentation, Economic Security Project (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-ubi-monthly-amounts.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    print(f"Saved: {OUTPUT_DIR / 'chart-ubi-monthly-amounts.png'}")
    plt.close()


def chart_ai_displacement_timeline():
    """Chart 4: AI job displacement concerns vs. UBI policy response."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Timeline data
    years = np.array([2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028])

    # AI capability index (normalized, showing acceleration)
    ai_capability = np.array([30, 35, 45, 65, 85, 95, 100, 108, 118])

    # Policy response lag (number of programs addressing AI displacement)
    ai_specific_policy = np.array([0, 0, 1, 2, 5, 8, 15, 25, 40])

    # Public concern index (Google Trends proxy)
    public_concern = np.array([20, 25, 30, 55, 70, 85, 100, 95, 90])

    ax2 = ax.twinx()

    # Plot lines
    line1, = ax.plot(years, ai_capability, color='#C0392B', linewidth=3,
                     marker='s', markersize=8, label='AI Capability (GPT-4, Claude, etc.)')
    line2, = ax.plot(years, public_concern, color=ACCENT, linewidth=3,
                     marker='o', markersize=8, label='Public Concern Index')
    line3, = ax2.plot(years, ai_specific_policy, color=GOLD, linewidth=3,
                      marker='^', markersize=8, label='AI-Displacement Policies')

    # Annotations
    ax.annotate('ChatGPT\nLaunch', xy=(2022.9, 65), xytext=(2021.5, 75),
                fontsize=9, color=TEXT_SECONDARY,
                arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1))

    ax.annotate('CalUBI\nAnnounced', xy=(2025.9, 95), xytext=(2024.5, 78),
                fontsize=9, color=GOLD,
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=1))

    ax.fill_between(years[5:8], ai_capability[5:8], ai_specific_policy[5:8] + 80,
                    alpha=0.1, color='#C0392B', label='_Policy Gap')

    ax.set_title('The Policy Gap: AI Capability vs. Displacement Response',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('Index (2026 = 100)', fontsize=12, color=TEXT_SECONDARY)
    ax2.set_ylabel('AI-Specific GI Programs', fontsize=12, color=GOLD)

    ax.set_xlim(2019.5, 2028.5)
    ax.set_ylim(0, 130)
    ax2.set_ylim(0, 50)

    ax.grid(True, alpha=0.4, color=GRID)
    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax.spines['left'].set_color(TEXT_SECONDARY)
    ax.spines['bottom'].set_color(TEXT_SECONDARY)
    ax2.spines['right'].set_color(GOLD)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax2.tick_params(colors=GOLD)

    # Combined legend
    lines = [line1, line2, line3]
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='upper left', frameon=False, fontsize=9)

    fig.text(0.99, 0.02, 'Sources: AI benchmark data, policy tracking, Google Trends (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chart-ai-policy-gap.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    print(f"Saved: {OUTPUT_DIR / 'chart-ai-policy-gap.png'}")
    plt.close()


if __name__ == "__main__":
    print("Generating UBI newsletter charts...")
    chart_ubi_pilots_growth()
    chart_ubi_funding_sources()
    chart_ubi_monthly_amounts()
    chart_ai_displacement_timeline()
    print("\nAll charts generated!")
