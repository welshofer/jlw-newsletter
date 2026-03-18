import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Newsletter color scheme — military olive/khaki
ACCENT = '#4A5D4F'
ACCENT2 = '#8B7355'  # khaki secondary
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'
OLIVE_DARK = '#3A4A3F'
STEEL_BLUE = '#4A6680'

OUT = '/Users/welshofer/clawd/jlw-newsletter/images/'

# ─────────────────────────────────────────────
# CHART 1: Troops landed by beach on D-Day
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

beaches = ['Utah\n(US)', 'Omaha\n(US)', 'Gold\n(UK)', 'Juno\n(CAN)', 'Sword\n(UK)']
troops = [23250, 34250, 24970, 21400, 28845]
casualties = [197, 2400, 1000, 961, 683]

colors = [ACCENT, '#8B4513', STEEL_BLUE, '#C41E3A', STEEL_BLUE]

bars = ax.bar(beaches, troops, color=colors, edgecolor='white', linewidth=0.5, width=0.65)

# Add casualty annotations
for i, (bar, cas) in enumerate(zip(bars, casualties)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 400,
            f'{troops[i]:,}', ha='center', va='bottom',
            fontsize=11, fontweight='600', color=TEXT)
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
            f'~{cas:,}\ncasualties', ha='center', va='center',
            fontsize=9, color='white', fontweight='500')

ax.set_title('Troops Landed & Casualties by Beach — June 6, 1944',
             fontsize=15, color=TEXT, fontweight='600', pad=20,
             fontfamily='serif')
ax.set_ylabel('Troops Landed', fontsize=11, color=TEXT_SECONDARY)
ax.set_ylim(0, 42000)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.grid(True, alpha=0.3, color=GRID, axis='y')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

fig.text(0.99, 0.02, 'Sources: National WWII Museum, Antony Beevor "D-Day"',
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig(f'{OUT}chart-troops-by-beach.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("✓ chart-troops-by-beach.png")


# ─────────────────────────────────────────────
# CHART 2: Operation Overlord Force Composition
# ─────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), facecolor=BG)

# Left: Naval forces breakdown
labels_nav = ['Landing Craft\n4,126', 'Combat Ships\n1,213', 'Ancillary\n1,600']
sizes_nav = [4126, 1213, 1600]
colors_nav = [ACCENT, STEEL_BLUE, ACCENT2]
explode_nav = (0.03, 0.03, 0.03)

wedges1, texts1, autotexts1 = ax1.pie(sizes_nav, labels=labels_nav, colors=colors_nav,
    autopct='%1.0f%%', startangle=140, explode=explode_nav,
    textprops={'fontsize': 10, 'color': TEXT})
for t in autotexts1:
    t.set_fontsize(11)
    t.set_fontweight('600')
    t.set_color('white')
ax1.set_title('Naval Fleet: 6,939 Vessels', fontsize=13, color=TEXT,
              fontweight='600', pad=15, fontfamily='serif')
ax1.set_facecolor(BG)

# Right: Air sorties comparison
categories = ['Allied\nSorties', 'German\nSorties']
sorties = [14674, 319]
colors_air = [ACCENT, '#8B4513']

bars2 = ax2.barh(categories, sorties, color=colors_air, height=0.5, edgecolor='white')
ax2.set_facecolor(BG)
for bar, val in zip(bars2, sorties):
    ax2.text(bar.get_width() + 200, bar.get_y() + bar.get_height()/2,
             f'{val:,}', ha='left', va='center', fontsize=13, fontweight='600', color=TEXT)

ax2.set_title('Air Superiority on D-Day', fontsize=13, color=TEXT,
              fontweight='600', pad=15, fontfamily='serif')
ax2.set_xlim(0, 18000)
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax2.grid(True, alpha=0.3, color=GRID, axis='x')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color(GRID)
ax2.spines['bottom'].set_color(GRID)

fig.suptitle('Operation Overlord Force Composition', fontsize=16, color=TEXT,
             fontweight='700', y=1.02, fontfamily='serif')
fig.text(0.99, 0.01, 'Source: National WWII Museum statistics archives',
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig(f'{OUT}chart-force-composition.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("✓ chart-force-composition.png")


# ─────────────────────────────────────────────
# CHART 3: Comparative Amphibious Operations
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG)
ax.set_facecolor(BG)

operations = ['Gallipoli\n1915', 'Dieppe\n1942', 'Sicily\n1943', 'D-Day\n1944', 'Iwo Jima\n1945', 'Inchon\n1950']
troops_count = [70000, 6086, 160000, 156000, 110000, 40000]
ships_count = [200, 237, 3200, 6939, 880, 261]

x = np.arange(len(operations))
width = 0.35

bars1 = ax.bar(x - width/2, troops_count, width, label='Troops (initial landing)',
               color=ACCENT, edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x + width/2, ships_count, width, label='Ships/Vessels',
               color=STEEL_BLUE, edgecolor='white', linewidth=0.5)

# Highlight D-Day
bars1[3].set_edgecolor('#FFD700')
bars1[3].set_linewidth(2.5)
bars2[3].set_edgecolor('#FFD700')
bars2[3].set_linewidth(2.5)

ax.set_xticks(x)
ax.set_xticklabels(operations, fontsize=10)
ax.set_title("History's Great Amphibious Operations — D-Day in Context",
             fontsize=14, color=TEXT, fontweight='600', pad=20, fontfamily='serif')
ax.set_ylabel('Count', fontsize=11, color=TEXT_SECONDARY)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.legend(fontsize=10, frameon=True, facecolor=BG, edgecolor=GRID)
ax.grid(True, alpha=0.3, color=GRID, axis='y')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Annotate D-Day
ax.annotate('Largest ever', xy=(3, 156000), xytext=(4.2, 145000),
            fontsize=10, color=ACCENT, fontweight='600',
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

fig.text(0.99, 0.02, 'Sources: Various military histories; troop numbers are initial landing day estimates',
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig(f'{OUT}chart-amphibious-comparison.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("✓ chart-amphibious-comparison.png")


# ─────────────────────────────────────────────
# CHART 4: WWII Veterans Still Living (decline)
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG)
ax.set_facecolor(BG)

years = [2000, 2005, 2010, 2015, 2020, 2024, 2025]
veterans_alive = [5720000, 3600000, 1711000, 855070, 325574, 100000, 65000]

ax.fill_between(years, veterans_alive, alpha=0.15, color=ACCENT)
ax.plot(years, veterans_alive, color=ACCENT, linewidth=3, marker='o',
        markersize=8, markerfacecolor='white', markeredgecolor=ACCENT, markeredgewidth=2.5)

for yr, vet in zip(years, veterans_alive):
    label = f'{vet/1000000:.1f}M' if vet >= 1000000 else f'{vet/1000:.0f}K'
    offset = 15 if vet > 200000 else -25
    ax.annotate(label, (yr, vet), textcoords="offset points",
                xytext=(0, offset), ha='center', fontsize=10,
                fontweight='600', color=TEXT)

ax.set_title('The Vanishing Generation: Living US WWII Veterans',
             fontsize=15, color=TEXT, fontweight='600', pad=20, fontfamily='serif')
ax.set_xlabel('Year', fontsize=11, color=TEXT_SECONDARY)
ax.set_ylabel('Living Veterans', fontsize=11, color=TEXT_SECONDARY)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1000000:.1f}M' if x >= 1000000 else f'{int(x/1000)}K'))
ax.set_xlim(1999, 2026)
ax.set_ylim(0, 6500000)
ax.grid(True, alpha=0.3, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Add annotation about rate
ax.annotate('~130 veterans\npassing per day', xy=(2024, 100000),
            xytext=(2019, 900000),
            fontsize=10, color='#8B4513', fontweight='500',
            arrowprops=dict(arrowstyle='->', color='#8B4513', lw=1.5))

fig.text(0.99, 0.02, 'Source: US Department of Veterans Affairs (estimates)',
         fontsize=8, color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig(f'{OUT}chart-veterans-decline.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("✓ chart-veterans-decline.png")

print("\n✅ All 4 charts generated successfully")
