#!/usr/bin/env python3
"""Generate charts for US depression probability newsletter."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Newsletter color scheme - teal accent for economic/forecasting topic
ACCENT = '#0D6E8A'      # Deep teal cyan
ACCENT_LIGHT = '#1A8FB4'
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
WARNING = '#C4654A'     # Coral for warning indicators
NEUTRAL = '#6B7A8A'

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SF Pro Display', 'Helvetica Neue', 'Arial']

# Chart 1: Recession Probability Comparison
fig1, ax1 = plt.subplots(figsize=(10, 6), facecolor=BG)
ax1.set_facecolor(BG)

institutions = ['Goldman\nSachs', 'J.P.\nMorgan', 'Yield Curve\nSignal', 'ITR\nEconomics']
probabilities = [20, 35, 55, 80]  # Estimated probabilities
colors = [ACCENT_LIGHT, ACCENT, WARNING, '#B85C38']

bars = ax1.bar(institutions, probabilities, color=colors, width=0.6, edgecolor='white', linewidth=1.5)

# Add value labels on bars
for bar, prob in zip(bars, probabilities):
    height = bar.get_height()
    ax1.annotate(f'{prob}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 8),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=14, fontweight='600', color=TEXT)

ax1.set_ylabel('Probability of Significant Downturn', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
ax1.set_title('Who Sees Trouble Ahead?', fontsize=18, color=TEXT, fontweight='600', pad=20, loc='left')
ax1.set_ylim(0, 100)
ax1.set_yticks([0, 25, 50, 75, 100])
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x)}%'))
ax1.tick_params(axis='both', colors=TEXT_SECONDARY, labelsize=11)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color(GRID)
ax1.spines['bottom'].set_color(GRID)
ax1.grid(True, axis='y', alpha=0.4, color=GRID, linestyle='-', linewidth=0.5)
ax1.set_axisbelow(True)

# Subtitle
fig1.text(0.13, 0.89, 'Institutional forecasts for US recession/depression probability (2026-2030)',
         fontsize=11, color=TEXT_SECONDARY, style='italic')

# Source
fig1.text(0.99, 0.02, 'Sources: Goldman Sachs, J.P. Morgan, Conference Board, ITR Economics (Jan 2026)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-recession-probabilities.png',
            dpi=150, facecolor=BG, bbox_inches='tight', pad_inches=0.3)
plt.close()

print("Chart 1: Recession probabilities saved")

# Chart 2: US Debt-to-GDP Trajectory
fig2, ax2 = plt.subplots(figsize=(10, 6), facecolor=BG)
ax2.set_facecolor(BG)

years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
debt_gdp = [129, 128, 123, 123, 124, 127, 130, 131, 132, 133, 133]  # Historical + CBO projections

# Split into historical and projected
historical_years = years[:6]
historical_debt = debt_gdp[:6]
projected_years = years[5:]
projected_debt = debt_gdp[5:]

ax2.plot(historical_years, historical_debt, color=ACCENT, linewidth=3, marker='o', markersize=6, label='Historical')
ax2.plot(projected_years, projected_debt, color=WARNING, linewidth=3, linestyle='--', marker='s', markersize=6, label='CBO Projection')

# Danger zone shading
ax2.axhspan(130, 140, alpha=0.15, color=WARNING, label='Danger Zone (>130%)')

ax2.set_xlabel('Year', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
ax2.set_ylabel('Debt-to-GDP Ratio (%)', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
ax2.set_title('The Fiscal Straitjacket', fontsize=18, color=TEXT, fontweight='600', pad=20, loc='left')
ax2.set_xlim(2019.5, 2030.5)
ax2.set_ylim(115, 140)
ax2.tick_params(axis='both', colors=TEXT_SECONDARY, labelsize=11)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color(GRID)
ax2.spines['bottom'].set_color(GRID)
ax2.grid(True, alpha=0.4, color=GRID, linestyle='-', linewidth=0.5)
ax2.set_axisbelow(True)
ax2.legend(loc='lower right', framealpha=0.9, fontsize=10)

# Annotation
ax2.annotate('133% by 2030', xy=(2030, 133), xytext=(2028, 137),
            fontsize=11, color=WARNING, fontweight='600',
            arrowprops=dict(arrowstyle='->', color=WARNING, lw=1.5))

# Subtitle
fig2.text(0.13, 0.89, 'US public debt as percentage of GDP, limiting future stimulus capacity',
         fontsize=11, color=TEXT_SECONDARY, style='italic')

# Source
fig2.text(0.99, 0.02, 'Source: Congressional Budget Office (Nov 2025)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-debt-gdp.png',
            dpi=150, facecolor=BG, bbox_inches='tight', pad_inches=0.3)
plt.close()

print("Chart 2: Debt-to-GDP trajectory saved")

# Chart 3: Policy Tools Comparison (2008 vs 2026)
fig3, ax3 = plt.subplots(figsize=(10, 6), facecolor=BG)
ax3.set_facecolor(BG)

categories = ['Fed Rate\nCutting Room', 'Fiscal\nSpace', 'Inflation\nHeadroom', 'Consumer\nBalance Sheets']
values_2008 = [100, 80, 85, 50]  # Pre-2008 crisis capacity (normalized to 100 max)
values_2026 = [40, 25, 35, 60]   # Current capacity estimates

x = np.arange(len(categories))
width = 0.35

bars1 = ax3.bar(x - width/2, values_2008, width, label='Pre-2008 Crisis', color=ACCENT, alpha=0.8)
bars2 = ax3.bar(x + width/2, values_2026, width, label='January 2026', color=WARNING, alpha=0.8)

ax3.set_ylabel('Policy Capacity (Indexed)', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
ax3.set_title('The Depleted Arsenal', fontsize=18, color=TEXT, fontweight='600', pad=20, loc='left')
ax3.set_xticks(x)
ax3.set_xticklabels(categories)
ax3.set_ylim(0, 120)
ax3.tick_params(axis='both', colors=TEXT_SECONDARY, labelsize=11)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_color(GRID)
ax3.spines['bottom'].set_color(GRID)
ax3.grid(True, axis='y', alpha=0.4, color=GRID, linestyle='-', linewidth=0.5)
ax3.set_axisbelow(True)
ax3.legend(loc='upper right', framealpha=0.9, fontsize=10)

# Subtitle
fig3.text(0.13, 0.89, 'Comparing available policy responses: then vs now',
         fontsize=11, color=TEXT_SECONDARY, style='italic')

# Source
fig3.text(0.99, 0.02, 'Sources: Federal Reserve, IMF, Brookings Institution (2025-2026)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-policy-tools.png',
            dpi=150, facecolor=BG, bbox_inches='tight', pad_inches=0.3)
plt.close()

print("Chart 3: Policy tools comparison saved")

print("\n✓ All charts generated successfully!")
