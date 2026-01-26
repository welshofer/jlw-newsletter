import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme - Rust/Tauri theme (warm orange tones)
ACCENT = '#C4654A'      # Rust/coral accent
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'        # Dark text
TEXT_SECONDARY = '#5C564D'  # Secondary text
GRID = '#E5E0D8'        # Grid lines

# Data
categories = ['Minimal\nHello World', 'Basic\nTodo App', 'Full\nWorkbench']
tauri_sizes = [0.6, 2.5, 12]  # MB
electron_sizes = [80, 120, 180]  # MB

x = np.arange(len(categories))
width = 0.35

# Create figure
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

# Plot bars
bars1 = ax.bar(x - width/2, tauri_sizes, width, label='Tauri', color=ACCENT, zorder=3)
bars2 = ax.bar(x + width/2, electron_sizes, width, label='Electron', color='#4A7BC4', zorder=3)

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'{height}MB',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='600', color=TEXT)

for bar in bars2:
    height = bar.get_height()
    ax.annotate(f'{height}MB',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='600', color=TEXT)

# Styling
ax.set_ylabel('Application Size (MB)', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
ax.set_title('App Bundle Size: Tauri vs Electron', fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11, color=TEXT)
ax.legend(fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.5, color=GRID, axis='y', zorder=1)
ax.set_ylim(0, 200)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)

# Source attribution
fig.text(0.99, 0.02, 'Source: Various benchmarks (2025)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-bundle-size.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-bundle-size.png")
