#!/usr/bin/env python3
"""Generate charts for the presentation narrative measurement newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Newsletter color scheme - teal/cyan accent for tech/measurement topic
ACCENT = '#0D6E8A'
ACCENT_LIGHT = '#1A8AAE'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
WARM = '#B85C38'

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SF Pro Display', 'Helvetica Neue', 'Arial']

def chart_1_memory_retention():
    """Chart showing how narrative structure affects memory retention."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    categories = ['Facts Only\n(No Narrative)', 'Basic\nStorytelling', 'Sensory-Heavy\nNarrative', 'Reflective\nNarrative']
    recall_7days = [22, 45, 68, 63]
    recall_30days = [8, 28, 52, 48]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, recall_7days, width, label='7-Day Recall', color=ACCENT, alpha=0.9)
    bars2 = ax.bar(x + width/2, recall_30days, width, label='30-Day Recall', color=WARM, alpha=0.9)

    ax.set_ylabel('Recall Accuracy (%)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Narrative Structure Dramatically Improves Memory Retention',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10, color=TEXT)
    ax.legend(loc='upper left', frameon=False)
    ax.set_ylim(0, 80)

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, color=ACCENT)
    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, color=WARM)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)

    fig.text(0.99, 0.02, 'Source: Journal of Neuroscience (Oct 2025)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-memory-retention.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 1: Memory retention saved")


def chart_2_measurement_framework():
    """Chart showing the 4-part narrative measurement framework."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Funnel-like visualization of the 4 measurement levels
    levels = ['Reach\n(Activities)', 'Message\n(Resonance)', 'People\n(Behavior)', 'Culture\n(Structural)']
    impact = [100, 75, 45, 20]  # What % of organizations measure this well

    colors = [ACCENT, ACCENT_LIGHT, '#3DA7C4', '#5BBCD6']

    bars = ax.barh(levels, impact, color=colors, height=0.6)

    ax.set_xlabel('% of Organizations Measuring Effectively', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('The Narrative Measurement Gap',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xlim(0, 110)

    # Add annotations
    for i, (bar, level) in enumerate(zip(bars, levels)):
        width = bar.get_width()
        ax.annotate(f'{int(width)}%', xy=(width + 2, bar.get_y() + bar.get_height()/2),
                    va='center', ha='left', fontsize=11, color=TEXT, fontweight='500')

    # Add difficulty indicator
    ax.text(95, 3.7, 'Harder to\nmeasure →', fontsize=9, color=TEXT_SECONDARY,
            ha='center', va='center', style='italic')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)

    fig.text(0.99, 0.02, 'Source: Stanford Social Innovation Review (2025)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-measurement-framework.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 2: Measurement framework saved")


def chart_3_roi_metrics():
    """Chart showing storytelling ROI impact on business metrics."""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)

    metrics = ['Audience\nEngagement', 'Story Retention\n(2 weeks)', 'Decision\nSpeed', 'Customer\nLifetime Value']
    baseline = [100, 100, 100, 100]
    with_storytelling = [300, 245, 185, 140]

    x = np.arange(len(metrics))
    width = 0.35

    bars1 = ax.bar(x - width/2, baseline, width, label='Standard Presentation',
                   color=GRID, alpha=0.8, edgecolor=TEXT_SECONDARY)
    bars2 = ax.bar(x + width/2, with_storytelling, width, label='Narrative-Driven',
                   color=ACCENT, alpha=0.9)

    ax.set_ylabel('Performance Index (Baseline = 100)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('Narrative-Driven Presentations Drive Measurable Business Impact',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=10, color=TEXT)
    ax.legend(loc='upper right', frameon=False)
    ax.set_ylim(0, 350)

    # Add improvement percentages
    improvements = ['+200%', '+145%', '+85%', '+40%']
    for i, (bar, imp) in enumerate(zip(bars2, improvements)):
        height = bar.get_height()
        ax.annotate(imp, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, color=ACCENT, fontweight='600')

    ax.axhline(y=100, color=TEXT_SECONDARY, linestyle='--', alpha=0.3, linewidth=1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)

    fig.text(0.99, 0.02, 'Source: Marketing LTB Corporate Storytelling ROI Report (2025)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-storytelling-roi.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 3: Storytelling ROI saved")


def chart_4_ai_tools_comparison():
    """Chart comparing AI presentation analysis tools."""
    fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
    ax.set_facecolor(BG)

    tools = ['Prezent', 'Gamma', 'Beautiful.ai', 'Decktopus', 'Traditional\nFeedback']

    # Capabilities scored 0-10
    categories = ['Predictive\nAnalysis', 'Real-time\nSentiment', 'Audience\nMatching', 'Delivery\nCoaching']

    data = {
        'Prezent': [9, 6, 9, 5],
        'Gamma': [5, 8, 6, 4],
        'Beautiful.ai': [4, 8, 5, 3],
        'Decktopus': [4, 6, 4, 8],
        'Traditional\nFeedback': [1, 2, 2, 6]
    }

    x = np.arange(len(categories))
    width = 0.15

    colors = [ACCENT, ACCENT_LIGHT, '#3DA7C4', '#5BBCD6', GRID]

    for i, (tool, color) in enumerate(zip(tools, colors)):
        offset = (i - 2) * width
        bars = ax.bar(x + offset, data[tool], width, label=tool, color=color, alpha=0.85)

    ax.set_ylabel('Capability Score (0-10)', fontsize=12, color=TEXT_SECONDARY)
    ax.set_title('AI Presentation Tools: Capability Comparison',
                 fontsize=16, color=TEXT, fontweight='600', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10, color=TEXT)
    ax.legend(loc='upper right', frameon=False, ncol=2, fontsize=9)
    ax.set_ylim(0, 11)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)

    fig.text(0.99, 0.02, 'Source: Is4.ai Analysis, Tool Reviews (2025-2026)', fontsize=9,
             color=TEXT_SECONDARY, ha='right', style='italic')

    plt.tight_layout()
    plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-ai-tools.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("Chart 4: AI tools comparison saved")


if __name__ == '__main__':
    chart_1_memory_retention()
    chart_2_measurement_framework()
    chart_3_roi_metrics()
    chart_4_ai_tools_comparison()
    print("\nAll charts generated successfully!")
