import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Newsletter color scheme - INDIGO theme
ACCENT = '#5B4B8A'
ACCENT_LIGHT = '#7B6BAA'
ACCENT_DARK = '#3B2B6A'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
RED = '#C44A4A'
AMBER = '#B8863C'

plt.rcParams['font.family'] = ['Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif']

# ============================================
# CHART 1: W-Shaped Mortality Curve
# ============================================
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

ages = ['<1', '1-4', '5-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']
x = np.arange(len(ages))

normal_flu = [80, 50, 10, 8, 8, 10, 20, 50, 120, 250]
flu_1918 = [150, 100, 40, 350, 580, 370, 180, 200, 350, 500]

ax.plot(x, normal_flu, 'o-', color=TEXT_SECONDARY, linewidth=2, markersize=6, 
        label='Typical Influenza (U-Shaped)', alpha=0.7)
ax.plot(x, flu_1918, 's-', color=RED, linewidth=2.5, markersize=7, 
        label='1918 Influenza (W-Shaped)')

ax.annotate('Anomalous peak:\nhealthy young adults\nages 25-34', 
            xy=(4, 580), xytext=(6.5, 520),
            fontsize=10, color=RED, fontweight='500',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=RED, alpha=0.9))

ax.set_xticks(x)
ax.set_xticklabels(ages, fontsize=10, color=TEXT_SECONDARY)
ax.set_title('The W-Shaped Mortality Curve of 1918', fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_xlabel('Age Group', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylabel('Deaths per 100,000', fontsize=12, color=TEXT_SECONDARY)
ax.legend(fontsize=10, loc='upper left', framealpha=0.9)
ax.grid(True, alpha=0.3, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=TEXT_SECONDARY)

fig.text(0.99, 0.02, 'Source: Taubenberger & Morens, Emerging Infectious Diseases (2006)', 
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-w-mortality-curve.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("Chart 1 complete: W-shaped mortality curve")

# ============================================
# CHART 2: Philadelphia vs St. Louis Death Rates
# ============================================
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

weeks = list(range(1, 11))
week_labels = ['Sep 21', 'Sep 28', 'Oct 5', 'Oct 12', 'Oct 19', 'Oct 26', 'Nov 2', 'Nov 9', 'Nov 16', 'Nov 23']

philly = [5, 30, 120, 257, 210, 160, 90, 55, 30, 15]
stlouis = [2, 5, 15, 31, 28, 22, 18, 15, 10, 8]

ax.fill_between(weeks, philly, alpha=0.15, color=RED)
ax.fill_between(weeks, stlouis, alpha=0.15, color=ACCENT)

ax.plot(weeks, philly, 'o-', color=RED, linewidth=2.5, markersize=7, label='Philadelphia')
ax.plot(weeks, stlouis, 's-', color=ACCENT, linewidth=2.5, markersize=7, label='St. Louis')

ax.annotate('Liberty Loans Parade\nSep 28: 200,000 gather', 
            xy=(2, 30), xytext=(3.5, 200),
            fontsize=9, color=RED, fontweight='500',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=RED, alpha=0.9))

ax.annotate('St. Louis closes\nschools, theaters,\nchurches (Oct 7)', 
            xy=(3, 15), xytext=(5.5, 120),
            fontsize=9, color=ACCENT, fontweight='500',
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ACCENT, alpha=0.9))

ax.set_xticks(weeks)
ax.set_xticklabels(week_labels, fontsize=9, color=TEXT_SECONDARY, rotation=30, ha='right')
ax.set_title('Two Cities, Two Choices: Death Rates Compared', fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_xlabel('Week (1918)', fontsize=12, color=TEXT_SECONDARY)
ax.set_ylabel('Excess Deaths per 100,000', fontsize=12, color=TEXT_SECONDARY)
ax.legend(fontsize=11, loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=TEXT_SECONDARY)

fig.text(0.99, 0.02, 'Source: Markel et al., JAMA (2007); Hatchett et al., PNAS (2007)', 
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-philly-vs-stlouis.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("Chart 2 complete: Philadelphia vs St. Louis")

# ============================================
# CHART 3: Global Death Toll by Region (Horizontal Bar)
# ============================================
fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
ax.set_facecolor(BG)

countries = ['Western Samoa', 'Iran', 'India', 'Indonesia', 'South Africa', 
             'Japan', 'Brazil', 'United Kingdom', 'United States', 'France']
deaths_millions = [0.0085, 1.65, 18, 1.5, 0.3, 0.39, 0.3, 0.228, 0.675, 0.24]
pop_percent = [22.0, 15.0, 6.0, 3.0, 2.5, 0.7, 1.0, 0.5, 0.65, 0.6]

sorted_indices = np.argsort(pop_percent)
countries = [countries[i] for i in sorted_indices]
pop_percent = [pop_percent[i] for i in sorted_indices]

colors = [ACCENT_LIGHT if p < 2 else ACCENT if p < 5 else RED for p in pop_percent]

bars = ax.barh(countries, pop_percent, color=colors, height=0.6, edgecolor='white', linewidth=0.5)

for bar, pct in zip(bars, pop_percent):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f'{pct}%', va='center', fontsize=10, color=TEXT, fontweight='500')

ax.set_title('Percentage of Population Killed by the 1918 Pandemic', 
             fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_xlabel('% of National Population', fontsize=12, color=TEXT_SECONDARY)
ax.set_xlim(0, 26)
ax.grid(True, axis='x', alpha=0.3, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=TEXT_SECONDARY, axis='both')
ax.tick_params(axis='y', labelsize=11)

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=ACCENT_LIGHT, label='< 2% mortality'),
    Patch(facecolor=ACCENT, label='2-5% mortality'),
    Patch(facecolor=RED, label='> 5% mortality')
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9, framealpha=0.9)

fig.text(0.99, 0.02, 'Source: Johnson & Mueller, Bulletin of the History of Medicine (2002)', 
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-global-death-toll.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("Chart 3 complete: Global death toll")

# ============================================
# CHART 4 (BONUS): Three Waves Timeline
# ============================================
fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
ax.set_facecolor(BG)

months = ['Mar\n1918', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
          'Jan\n1919', 'Feb', 'Mar', 'Apr']
x = np.arange(len(months))

deaths = [2, 3, 2, 1, 0.5, 2, 30, 195, 90, 25, 20, 15, 10, 5]

colors = []
for i, d in enumerate(deaths):
    if i <= 5:
        colors.append(ACCENT_LIGHT)
    elif i <= 9:
        colors.append(RED)
    else:
        colors.append(AMBER)

ax.bar(x, deaths, color=colors, width=0.7, edgecolor='white', linewidth=0.5)

ax.text(2, 12, 'FIRST WAVE\n(Spring 1918)', ha='center', fontsize=9, 
        color=ACCENT_LIGHT, fontweight='600', style='italic')
ax.text(7.5, 210, 'SECOND WAVE\n(Autumn 1918)', ha='center', fontsize=9,
        color=RED, fontweight='600', style='italic')
ax.text(11, 30, 'THIRD WAVE\n(Winter 1919)', ha='center', fontsize=9,
        color=AMBER, fontweight='600', style='italic')

ax.annotate('October 1918:\n~195,000 dead\nin the US alone', 
            xy=(7, 195), xytext=(10, 170),
            fontsize=9, color=RED, fontweight='500',
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=RED, alpha=0.9))

ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=9, color=TEXT_SECONDARY)
ax.set_title('The Three Waves: U.S. Influenza Deaths 1918-1919', 
             fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_ylabel('Deaths (thousands)', fontsize=12, color=TEXT_SECONDARY)
ax.grid(True, axis='y', alpha=0.3, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=TEXT_SECONDARY)

fig.text(0.99, 0.02, 'Source: CDC Historical Records; Barry, The Great Influenza (2004)', 
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-three-waves.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("Chart 4 complete: Three waves timeline")

print("\nAll charts generated successfully!")
