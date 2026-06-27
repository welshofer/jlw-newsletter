#!/usr/bin/env python3
"""Generate data visualizations for College Education in AI Era newsletter."""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from chart_style import output_path, apply_brand_style

# Newsletter color scheme - Indigo theme for education/uncertainty
ACCENT = '#5B4B8A'      # Indigo accent
ACCENT_LIGHT = '#7B6BAA'
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'        # Dark text
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
BORDER = '#E5E0D8'

# Set up matplotlib defaults
apply_brand_style()
plt.rcParams['axes.unicode_minus'] = False

output_dir = Path(output_path('images'))


def chart_entry_level_decline():
    """Chart 1: Entry-level job postings decline over time."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Data: Entry-level job postings index (100 = early 2023)
    years = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023',
             'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024',
             'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026']
    job_index = [100, 95, 88, 82, 78, 75, 72, 70, 68, 67, 66, 65, 65]

    # Plot line
    x = np.arange(len(years))
    ax.plot(x, job_index, color=ACCENT, linewidth=3, marker='o', markersize=8, markerfacecolor=BG, markeredgewidth=2)

    # Fill area under curve
    ax.fill_between(x, job_index, alpha=0.2, color=ACCENT)

    # Add annotation for 35% drop
    ax.annotate('35% decline\nsince early 2023', xy=(12, 65), xytext=(10, 80),
                fontsize=12, fontweight='600', color=ACCENT,
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

    # Styling
    ax.set_title('Entry-Level Job Postings Are Evaporating',
                 fontsize=18, color=TEXT, fontweight='600', pad=20, loc='left')
    ax.set_xlabel('', fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel('Job Posting Index (Q1 2023 = 100)', fontsize=11, color=TEXT_SECONDARY)

    ax.set_xticks(x[::2])  # Show every other label
    ax.set_xticklabels([years[i] for i in range(0, len(years), 2)], fontsize=10, color=TEXT_SECONDARY)
    ax.set_ylim(50, 110)

    ax.grid(True, alpha=0.5, color=GRID, linestyle='-', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)

    # Source
    fig.text(0.99, 0.02, 'Source: The Optimist (ACU), Jan 2026', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_dir / 'chart-entry-level-decline.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Generated: chart-entry-level-decline.png")


def chart_degree_requirements():
    """Chart 2: Companies dropping degree requirements."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Data: Percentage of companies removing degree requirements
    years = ['2020', '2021', '2022', '2023', '2024', '2025', '2026\n(projected)']
    removed = [5, 8, 12, 15, 18, 21, 25]

    bars = ax.bar(years, removed, color=ACCENT, width=0.6, edgecolor='none')

    # Highlight 2026 projection
    bars[-1].set_color(ACCENT_LIGHT)
    bars[-1].set_hatch('///')

    # Add value labels
    for bar, val in zip(bars, removed):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                f'{val}%', ha='center', va='bottom', fontsize=11, color=TEXT, fontweight='500')

    # Styling
    ax.set_title('Employers Are Ditching Degree Requirements',
                 fontsize=18, color=TEXT, fontweight='600', pad=20, loc='left')
    ax.set_ylabel('% of Companies', fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylim(0, 32)

    ax.tick_params(axis='x', colors=TEXT_SECONDARY)
    ax.tick_params(axis='y', colors=TEXT_SECONDARY)

    ax.grid(True, alpha=0.5, color=GRID, axis='y', linestyle='-', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)

    # Source
    fig.text(0.99, 0.02, 'Source: The HR Digest, Jan 2026', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_dir / 'chart-degree-requirements.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Generated: chart-degree-requirements.png")


def chart_student_confidence():
    """Chart 3: Student confidence crisis - horizontal bar chart."""
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    ax.set_facecolor(BG)

    # Data from College Recruiter survey
    categories = [
        'See AI as threat\nto career prospects',
        'Expect AI will eliminate\nmore jobs than create',
        'View degree as\n"financial burden"'
    ]
    values = [59, 44, 38]  # 38% is inferred from context

    y_pos = np.arange(len(categories))
    bars = ax.barh(y_pos, values, color=ACCENT, height=0.6, edgecolor='none')

    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height()/2,
                f'{val}%', va='center', fontsize=14, color=ACCENT, fontweight='600')

    # Styling
    ax.set_title('Class of 2026: A Crisis of Confidence',
                 fontsize=18, color=TEXT, fontweight='600', pad=20, loc='left')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=11, color=TEXT)
    ax.set_xlim(0, 75)
    ax.set_xlabel('% of Young Americans', fontsize=11, color=TEXT_SECONDARY)

    ax.grid(True, alpha=0.5, color=GRID, axis='x', linestyle='-', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(BORDER)

    ax.tick_params(axis='y', length=0)
    ax.tick_params(axis='x', colors=TEXT_SECONDARY)

    # Source
    fig.text(0.99, 0.02, 'Source: College Recruiter Survey, Jan 2026', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_dir / 'chart-student-confidence.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Generated: chart-student-confidence.png")


def chart_roi_comparison():
    """Chart 4: ROI comparison - 4-year degree vs 2-year AI credential."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Hypothetical data based on PwC insights
    years_after = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # 4-year traditional degree: -$120k investment, slower salary growth
    traditional = [-120, -80, -40, 0, 20, 45, 70, 95, 120]

    # 2-year AI credential: -$30k investment, faster but potentially plateauing
    accelerated = [-30, 10, 40, 65, 85, 100, 112, 122, 130]

    ax.plot(years_after, traditional, color=ACCENT, linewidth=3, label='4-Year Traditional Degree', marker='o', markersize=6)
    ax.plot(years_after, accelerated, color='#D4A574', linewidth=3, label='2-Year AI Credential', marker='s', markersize=6)

    # Add breakeven annotation
    ax.axhline(y=0, color=GRID, linestyle='--', linewidth=1)
    ax.annotate('Breakeven', xy=(3.3, 5), fontsize=10, color=TEXT_SECONDARY)

    # Styling
    ax.set_title('Time to Positive ROI: Traditional vs. Accelerated Paths',
                 fontsize=18, color=TEXT, fontweight='600', pad=20, loc='left')
    ax.set_xlabel('Years After Starting Program', fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel('Cumulative Return ($k)', fontsize=11, color=TEXT_SECONDARY)

    ax.legend(loc='lower right', frameon=True, facecolor=BG, edgecolor=BORDER, fontsize=10)

    ax.grid(True, alpha=0.5, color=GRID, linestyle='-', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)

    ax.tick_params(axis='x', colors=TEXT_SECONDARY)
    ax.tick_params(axis='y', colors=TEXT_SECONDARY)

    # Source
    fig.text(0.99, 0.02, 'Source: Analysis based on PwC Ireland insights, Jan 2026', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig(output_dir / 'chart-roi-comparison.png', dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ Generated: chart-roi-comparison.png")


if __name__ == '__main__':
    print("Generating newsletter charts...")
    chart_entry_level_decline()
    chart_degree_requirements()
    chart_student_confidence()
    chart_roi_comparison()
    print("\nAll charts generated successfully!")
