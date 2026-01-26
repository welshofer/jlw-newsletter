import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#5B4B8A'
ACCENT_LIGHT = '#7C6BA8'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
AMBER = '#D4A84B'

# AI 2027 report forecast evolution
years = ['Early 2024', 'Mid 2024', 'Late 2024', 'Early 2025', 'Jan 2026']
median_forecast = [2027, 2027, 2028, 2029, 2030]
optimistic_10 = [2025, 2025, 2026, 2026, 2027]
pessimistic_90 = [2032, 2033, 2035, 2036, 2038]

fig, ax = plt.subplots(figsize=(11, 6), facecolor=BG)
ax.set_facecolor(BG)

x = np.arange(len(years))

# Fill the confidence interval
ax.fill_between(x, optimistic_10, pessimistic_90, color=ACCENT, alpha=0.15, label='10th-90th percentile')

# Plot lines
ax.plot(x, median_forecast, 'o-', color=ACCENT, linewidth=3, markersize=10, label='Median forecast', zorder=5)
ax.plot(x, optimistic_10, 's--', color=AMBER, linewidth=2, markersize=7, alpha=0.8, label='10th percentile (optimistic)')
ax.plot(x, pessimistic_90, '^--', color=ACCENT_LIGHT, linewidth=2, markersize=7, alpha=0.8, label='90th percentile (pessimistic)')

# Annotate the shift
ax.annotate('', xy=(4, 2030), xytext=(0, 2027),
            arrowprops=dict(arrowstyle='->', color=TEXT_SECONDARY, lw=1.5, ls='--'))
ax.annotate('+3 years\nin 2 years', xy=(2.5, 2028.2), fontsize=10, color=TEXT_SECONDARY,
            ha='center', style='italic')

ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=11, color=TEXT)

ax.set_ylabel('Predicted AGI Arrival Year', fontsize=12, color=TEXT_SECONDARY)
ax.set_title('The Shifting Horizon: AGI Forecast Evolution\nAI 2027 Report Median Estimates Over Time\n',
             fontsize=16, color=TEXT, fontweight='600', pad=20)

# Y-axis
ax.set_ylim(2024, 2040)
ax.set_yticks([2025, 2027, 2030, 2033, 2036, 2039])

# Grid
ax.yaxis.grid(True, alpha=0.5, color=GRID)
ax.set_axisbelow(True)

# Spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Legend
ax.legend(loc='upper left', frameon=True, facecolor=BG, edgecolor=GRID, fontsize=10)

# Source
fig.text(0.99, 0.02, 'Source: AI-2027.com forecast updates (2024-2026)',
         fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-forecast-shift.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-forecast-shift.png")
