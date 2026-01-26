import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme
ACCENT = '#C4654A'      # Rust/coral accent
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'        # Dark text
TEXT_SECONDARY = '#5C564D'  # Secondary text
GRID = '#E5E0D8'        # Grid lines

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=BG)

# Memory Usage Chart
frameworks = ['Tauri', 'Electron']
memory_idle = [28, 250]  # MB RAM
colors = [ACCENT, '#4A7BC4']

ax1.set_facecolor(BG)
bars1 = ax1.barh(frameworks, memory_idle, color=colors, height=0.5, zorder=3)
ax1.set_xlabel('Memory Usage (MB RAM)', fontsize=11, color=TEXT_SECONDARY)
ax1.set_title('Idle Memory Consumption', fontsize=14, color=TEXT, fontweight='600', pad=15)
ax1.set_xlim(0, 300)
ax1.grid(True, alpha=0.5, color=GRID, axis='x', zorder=1)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color(GRID)
ax1.spines['bottom'].set_color(GRID)

for bar, val in zip(bars1, memory_idle):
    ax1.annotate(f'{val}MB', xy=(val + 5, bar.get_y() + bar.get_height()/2),
                 va='center', fontsize=11, fontweight='600', color=TEXT)

# Add "8.9x less" annotation
ax1.annotate('8.9x less RAM', xy=(140, 0.75), fontsize=12, 
             color=ACCENT, fontweight='700', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ACCENT, alpha=0.9))

# Startup Time Chart
startup_times = [0.4, 1.5]  # seconds

ax2.set_facecolor(BG)
bars2 = ax2.barh(frameworks, startup_times, color=colors, height=0.5, zorder=3)
ax2.set_xlabel('Startup Time (seconds)', fontsize=11, color=TEXT_SECONDARY)
ax2.set_title('Application Launch Speed', fontsize=14, color=TEXT, fontweight='600', pad=15)
ax2.set_xlim(0, 2)
ax2.grid(True, alpha=0.5, color=GRID, axis='x', zorder=1)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color(GRID)
ax2.spines['bottom'].set_color(GRID)

for bar, val in zip(bars2, startup_times):
    ax2.annotate(f'{val}s', xy=(val + 0.05, bar.get_y() + bar.get_height()/2),
                 va='center', fontsize=11, fontweight='600', color=TEXT)

# Add "3.75x faster" annotation
ax2.annotate('3.75x faster', xy=(0.95, 0.75), fontsize=12, 
             color=ACCENT, fontweight='700', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ACCENT, alpha=0.9))

# Source attribution
fig.text(0.99, 0.02, 'Source: Side-by-side benchmarks on mid-range laptop (2025)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-memory-startup.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-memory-startup.png")
