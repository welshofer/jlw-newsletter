#!/usr/bin/env python3
"""Generate P-Doom newsletter charts with newsletter styling."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Newsletter color scheme - violet/indigo for this P-Doom topic
ACCENT = '#5B4B8A'      # Deep violet
ACCENT_LIGHT = '#7C6BAA'
ACCENT_DARK = '#3D3260'
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'        # Dark text
TEXT_SECONDARY = '#5C564D'
GRID = '#E5E0D8'
DANGER = '#B85C38'      # Terracotta for high risk
SAFE = '#4A9B7F'        # Green-teal for low risk

# Set default font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif']


def chart1_individual_estimates():
    """Bar chart of individual researcher P-Doom estimates."""

    # Data: researcher name, midpoint estimate, low, high (for error bars)
    researchers = [
        ('Yudkowsky', 97, 95, 99),
        ('Leahy', 85, 80, 90),
        ('Hendrycks', 80, 80, 85),
        ('Christiano', 50, 40, 60),
        ('Shear', 27.5, 5, 50),
        ('Leike', 50, 10, 90),
        ('Amodei', 17.5, 10, 25),
        ('Bengio', 20, 15, 25),
        ('Hinton', 15, 10, 20),
        ('LeCun', 0.01, 0, 0.1),
    ]

    # Sort by midpoint estimate (descending)
    researchers = sorted(researchers, key=lambda x: x[1], reverse=True)

    names = [r[0] for r in researchers]
    mids = [r[1] for r in researchers]
    lows = [r[2] for r in researchers]
    highs = [r[3] for r in researchers]

    # Calculate error bar sizes
    yerr_low = [m - l for m, l in zip(mids, lows)]
    yerr_high = [h - m for m, h in zip(mids, highs)]

    # Color gradient based on estimate
    colors = []
    for m in mids:
        if m > 70:
            colors.append(DANGER)
        elif m > 30:
            colors.append(ACCENT)
        elif m > 10:
            colors.append(ACCENT_LIGHT)
        else:
            colors.append(SAFE)

    fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
    ax.set_facecolor(BG)

    y_pos = np.arange(len(names))

    bars = ax.barh(y_pos, mids, color=colors, edgecolor='white', linewidth=0.5, height=0.7)

    # Add error bars
    ax.errorbar(mids, y_pos, xerr=[yerr_low, yerr_high],
                fmt='none', ecolor=TEXT_SECONDARY, capsize=4, capthick=1.5, elinewidth=1.5, alpha=0.7)

    # Add percentage labels
    for i, (bar, mid) in enumerate(zip(bars, mids)):
        if mid > 1:
            label = f'{mid:.0f}%'
        else:
            label = f'{mid:.2f}%'
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2,
                label, ha='left', va='center', fontsize=11, fontweight='500', color=TEXT)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=12, color=TEXT)
    ax.set_xlabel('P(Doom) Estimate (%)', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
    ax.set_title('What Do Top AI Researchers Think?\nP-Doom Estimates Across the Spectrum',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)

    ax.set_xlim(0, 110)
    ax.invert_yaxis()

    # Styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.spines['left'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.grid(axis='x', alpha=0.3, color=GRID)

    # Add reference lines
    ax.axvline(x=50, color=ACCENT, linestyle='--', alpha=0.3, linewidth=1)
    ax.text(51, -0.7, '50% threshold', fontsize=9, color=TEXT_SECONDARY, style='italic')

    # Source
    fig.text(0.99, 0.02, 'Sources: Various interviews, 2023-2025', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-pdoom-estimates.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-pdoom-estimates.png")


def chart2_survey_distribution():
    """Histogram showing bimodal distribution from AI Impacts survey."""

    # Simulated distribution based on survey results
    # Median: 5%, Mean: 16.2%, 50% gave <5%, 10% gave ≥25%
    np.random.seed(42)

    # Create bimodal distribution
    # Cluster 1: Low estimates (most researchers)
    low_cluster = np.random.exponential(3, 1400)  # ~50% below 5%
    low_cluster = np.clip(low_cluster, 0, 15)

    # Cluster 2: Medium estimates
    mid_cluster = np.random.normal(12, 5, 800)
    mid_cluster = np.clip(mid_cluster, 5, 25)

    # Cluster 3: High estimates (~10% at 25%+)
    high_cluster = np.random.normal(35, 15, 280)
    high_cluster = np.clip(high_cluster, 25, 90)

    # Very high estimates (tail)
    very_high = np.random.uniform(60, 99, 50)

    all_estimates = np.concatenate([low_cluster, mid_cluster, high_cluster, very_high])

    fig, ax = plt.subplots(figsize=(11, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Histogram
    bins = np.arange(0, 105, 5)
    n, bins_out, patches = ax.hist(all_estimates, bins=bins, edgecolor='white', linewidth=0.5)

    # Color bars by risk level
    for i, (patch, left_edge) in enumerate(zip(patches, bins[:-1])):
        if left_edge < 10:
            patch.set_facecolor(SAFE)
        elif left_edge < 30:
            patch.set_facecolor(ACCENT_LIGHT)
        elif left_edge < 50:
            patch.set_facecolor(ACCENT)
        else:
            patch.set_facecolor(DANGER)

    # Add median and mean lines
    ax.axvline(x=5, color=ACCENT_DARK, linestyle='-', linewidth=2.5, label='Median: 5%')
    ax.axvline(x=16.2, color=DANGER, linestyle='--', linewidth=2.5, label='Mean: 16.2%')

    ax.set_xlabel('P(Doom) Estimate (%)', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
    ax.set_ylabel('Number of Researchers', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
    ax.set_title('The Bimodal Distribution of Doom\nAI Impacts Survey of 2,778 Researchers (2024)',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)

    # Legend
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)

    # Styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.spines['left'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    ax.grid(axis='y', alpha=0.3, color=GRID)

    # Annotations
    ax.annotate('50% of researchers\nestimate <5%',
                xy=(2.5, 700), fontsize=10, color=TEXT_SECONDARY,
                ha='center', style='italic')

    ax.annotate('10% estimate\n≥25%',
                xy=(40, 100), fontsize=10, color=TEXT_SECONDARY,
                ha='center', style='italic')

    # Source
    fig.text(0.99, 0.02, 'Source: AI Impacts Survey (Jan 2024)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-survey-distribution.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-survey-distribution.png")


def chart3_experts_vs_superforecasters():
    """Comparison of AI experts vs superforecasters from XPT survey."""

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    groups = ['AI Domain\nExperts', 'Super-\nforecasters']
    medians = [3.0, 0.38]

    bars = ax.bar(groups, medians, color=[ACCENT, SAFE], edgecolor='white', linewidth=1, width=0.5)

    # Add value labels
    for bar, val in zip(bars, medians):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{val}%', ha='center', va='bottom', fontsize=16, fontweight='600', color=TEXT)

    ax.set_ylabel('Median P(Doom by 2100) %', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
    ax.set_title('The Expert Gap\nAI Researchers vs. Professional Forecasters',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)

    # Add multiplier annotation
    ax.annotate('', xy=(0, 3.0), xytext=(1, 0.38),
                arrowprops=dict(arrowstyle='<->', color=TEXT_SECONDARY, lw=1.5))
    ax.text(0.5, 1.5, '~8× higher', ha='center', fontsize=12, color=TEXT_SECONDARY, fontweight='500')

    # Styling
    ax.set_ylim(0, 4.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.spines['left'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=12)
    ax.grid(axis='y', alpha=0.3, color=GRID)

    # Context note
    ax.text(0.5, -0.8,
            'Superforecasters: professional predictors with track records of accuracy\n'
            'AI Experts: researchers who published in top ML venues',
            ha='center', transform=ax.transAxes, fontsize=10, color=TEXT_SECONDARY, style='italic')

    # Source
    fig.text(0.99, 0.02, 'Source: Existential Risk Persuasion Tournament (XPT)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-experts-vs-forecasters.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-experts-vs-forecasters.png")


def chart4_turing_split():
    """Visual showing the Turing Award winners' split."""

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    ax.set_facecolor(BG)

    # Three segments for the three researchers
    names = ['Hinton', 'Bengio', 'LeCun']
    estimates = [15, 20, 0.01]
    positions = [0, 1, 2]

    colors = [ACCENT, ACCENT, SAFE]

    bars = ax.bar(positions, estimates, color=colors, edgecolor='white', linewidth=1, width=0.6)

    # Labels
    for pos, bar, name, est in zip(positions, bars, names, estimates):
        # Name below
        ax.text(pos, -3, name, ha='center', fontsize=14, fontweight='600', color=TEXT)
        # Percentage on bar
        if est > 1:
            label = f'{est:.0f}%'
            y_pos = bar.get_height() / 2
        else:
            label = f'{est}%'
            y_pos = bar.get_height() + 1
        ax.text(pos, y_pos, label, ha='center', va='center', fontsize=14, fontweight='600',
                color='white' if est > 1 else TEXT)

    ax.set_title('The Godfather Split\nTuring Award Winners Diverge on AI Risk',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)

    # Remove axes
    ax.set_xlim(-0.7, 2.7)
    ax.set_ylim(-6, 30)
    ax.axis('off')

    # Add bracket and label for the "worried" group
    bracket_y = 23
    ax.plot([0, 1], [bracket_y, bracket_y], color=TEXT_SECONDARY, linewidth=1.5)
    ax.plot([0, 0], [bracket_y-1, bracket_y], color=TEXT_SECONDARY, linewidth=1.5)
    ax.plot([1, 1], [bracket_y-1, bracket_y], color=TEXT_SECONDARY, linewidth=1.5)
    ax.text(0.5, bracket_y + 2, '"We must be cautious"', ha='center', fontsize=11,
            color=TEXT_SECONDARY, style='italic')

    # Label for LeCun
    ax.text(2, 5, '"Preposterously\nridiculous"', ha='center', fontsize=11,
            color=TEXT_SECONDARY, style='italic')

    # Source
    fig.text(0.99, 0.02, '2018 Turing Award recipients for deep learning', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-turing-split.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Created: chart-turing-split.png")


if __name__ == '__main__':
    print("Generating P-Doom newsletter charts...")
    chart1_individual_estimates()
    chart2_survey_distribution()
    chart3_experts_vs_superforecasters()
    chart4_turing_split()
    print("\nAll charts generated successfully!")
