#!/usr/bin/env python3
"""Generate data visualizations for AI Manga Market newsletter."""

import matplotlib.pyplot as plt
import numpy as np
import os
import chart_style
from chart_style import apply_brand_style

# Newsletter color scheme - violet/creative theme
ACCENT = '#7C5C8A'      # --accent (violet)
ACCENT_DARK = '#5B4B8A'
BG = '#FDFBF7'          # --bg (cream background)
TEXT = '#1A1815'        # --text
TEXT_SECONDARY = '#4D5C6A'  # --text-secondary
GRID = '#D8E2E8'        # --border

OUTPUT_DIR = chart_style.output_path('images', 'ai-manga-market')
os.makedirs(OUTPUT_DIR, exist_ok=True)

apply_brand_style()

def chart_1_market_growth():
    """AI Manga Tools Market Growth Projection"""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    years = ['2023', '2024', '2025', '2026 (Est)', '2027 (Proj)']
    market_size = [45, 85, 180, 320, 550]  # millions USD

    bars = ax.bar(years, market_size, color=ACCENT, width=0.65, edgecolor='white', linewidth=1)

    # Add value labels on bars
    for bar, val in zip(bars, market_size):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 12,
                f'${val}M', ha='center', va='bottom', fontsize=11,
                fontweight='600', color=TEXT)

    # Growth rate annotations
    growth_rates = [None, '+89%', '+112%', '+78%', '+72%']
    for i, (bar, rate) in enumerate(zip(bars, growth_rates)):
        if rate:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                    rate, ha='center', va='center', fontsize=10,
                    color='white', fontweight='600')

    ax.set_title('AI Manga Creation Tools Market Size', fontsize=16,
                 color=TEXT, fontweight='600', pad=20)
    ax.set_ylabel('Market Size (USD Millions)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylim(0, 650)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.yaxis.grid(True, alpha=0.5, color=GRID, linestyle='--')
    ax.set_axisbelow(True)

    fig.text(0.99, 0.02, 'Source: Industry estimates based on Anifusion, Skywork, NovelAI market data (2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/chart-market-growth.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Saved: chart-market-growth.png")


def chart_2_institutional_divide():
    """East vs West: Institutional Response to AI Manga"""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    categories = ['Japan\n(Shueisha/Jump)', 'Japan\n(Gov\'t Funding)', 'South Korea\n(Webtoon)',
                  'US Publishers', 'US Conventions\n(SDCC)', 'EU Regulators']

    # Positive = embracing AI, Negative = restricting/banning
    stance = [85, 70, 60, -30, -90, -50]  # percentage scale
    colors = [ACCENT if s > 0 else '#C45C5C' for s in stance]

    bars = ax.barh(categories, stance, color=colors, height=0.65, edgecolor='white', linewidth=1)

    # Add labels
    for bar, val in zip(bars, stance):
        offset = 5 if val > 0 else -5
        ha = 'left' if val > 0 else 'right'
        label = f'+{val}%' if val > 0 else f'{val}%'
        ax.text(val + offset, bar.get_y() + bar.get_height()/2,
                label, ha=ha, va='center', fontsize=10,
                fontweight='600', color=TEXT)

    ax.axvline(x=0, color=GRID, linewidth=2)
    ax.set_xlim(-110, 110)

    ax.set_title('Institutional AI Manga Adoption Spectrum', fontsize=16,
                 color=TEXT, fontweight='600', pad=20)
    ax.set_xlabel('← Restricting / Banning    |    Embracing / Investing →',
                  fontsize=11, color=TEXT_SECONDARY)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(left=False, colors=TEXT_SECONDARY)
    ax.xaxis.grid(True, alpha=0.3, color=GRID, linestyle='--')
    ax.set_axisbelow(True)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=ACCENT, label='Embracing AI'),
                       Patch(facecolor='#C45C5C', label='Restricting AI')]
    ax.legend(handles=legend_elements, loc='upper right', frameon=False)

    fig.text(0.99, 0.02, 'Source: Policy analysis of Shueisha, SDCC, EU AI Act positions (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/chart-institutional-divide.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Saved: chart-institutional-divide.png")


def chart_3_job_displacement():
    """AI Displacement Risk: Illustrators vs Manga Artists (NBER Study)"""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    categories = ['Single-Image\nIllustrators', 'Manga/Comic\nArtists']

    # Data from Pixiv study - upload rate changes
    upload_change = [-42, -8]  # percentage change in uploads after AI models released
    colors = ['#C45C5C', ACCENT]

    bars = ax.bar(categories, upload_change, color=colors, width=0.5, edgecolor='white', linewidth=2)

    ax.axhline(y=0, color=GRID, linewidth=2)

    for bar, val in zip(bars, upload_change):
        offset = -3 if val < 0 else 3
        va = 'top' if val < 0 else 'bottom'
        ax.text(bar.get_x() + bar.get_width()/2, val + offset,
                f'{val}%', ha='center', va=va, fontsize=16,
                fontweight='700', color=TEXT)

    ax.set_ylim(-55, 10)
    ax.set_title('Upload Rate Changes Post-AI (Pixiv Analysis)', fontsize=16,
                 color=TEXT, fontweight='600', pad=20)
    ax.set_ylabel('Change in Upload Volume (%)', fontsize=12, color=TEXT_SECONDARY)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(colors=TEXT_SECONDARY, bottom=False)
    ax.yaxis.grid(True, alpha=0.5, color=GRID, linestyle='--')
    ax.set_axisbelow(True)

    # Insight callout
    ax.text(0.5, -45, '"Sequential art\'s complexity acts as a moat against AI displacement"',
            ha='center', fontsize=10, style='italic', color=TEXT_SECONDARY,
            transform=ax.get_xaxis_transform())

    fig.text(0.99, 0.02, 'Source: NBER/Pixiv Data Analysis (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/chart-job-displacement.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Saved: chart-job-displacement.png")


def chart_4_tool_capabilities():
    """AI Manga Tool Capabilities Comparison"""
    fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
    ax.set_facecolor(BG)

    tools = ['Anifusion', 'Skywork AI', 'NovelAI', 'ComicAI', 'Midjourney\n(+ manual)']

    capabilities = {
        'Character Consistency': [85, 92, 75, 70, 40],
        'Panel Layout': [90, 88, 60, 80, 20],
        'Text Bubbles': [95, 85, 50, 85, 10],
        'Full Workflow': [95, 70, 45, 65, 15],
        'Style Control': [80, 90, 95, 75, 98]
    }

    x = np.arange(len(tools))
    width = 0.15
    multiplier = 0

    colors = [ACCENT, ACCENT_DARK, '#6B8E8A', '#8A7C6B', '#6B7C8A']

    for i, (cap, scores) in enumerate(capabilities.items()):
        offset = width * multiplier
        ax.bar(x + offset, scores, width, label=cap, color=colors[i],
                      edgecolor='white', linewidth=0.5)
        multiplier += 1

    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(tools)
    ax.set_ylim(0, 110)

    ax.set_title('AI Manga Tool Capability Scores', fontsize=16,
                 color=TEXT, fontweight='600', pad=20)
    ax.set_ylabel('Capability Score (0-100)', fontsize=12, color=TEXT_SECONDARY)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.yaxis.grid(True, alpha=0.5, color=GRID, linestyle='--')
    ax.set_axisbelow(True)

    ax.legend(loc='upper right', frameon=True, facecolor=BG, edgecolor=GRID,
              fontsize=9, ncol=2)

    fig.text(0.99, 0.02, 'Source: Feature analysis based on tool documentation (Jan 2026)',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/chart-tool-capabilities.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Saved: chart-tool-capabilities.png")


if __name__ == '__main__':
    print("Generating AI Manga Market charts...")
    chart_1_market_growth()
    chart_2_institutional_divide()
    chart_3_job_displacement()
    chart_4_tool_capabilities()
    print("All charts generated!")
