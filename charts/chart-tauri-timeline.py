import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Newsletter color scheme
ACCENT = '#C4654A'      # Rust/coral accent
BG = '#FDFBF7'          # Cream background
TEXT = '#1A1815'        # Dark text
TEXT_SECONDARY = '#5C564D'  # Secondary text
GRID = '#E5E0D8'        # Grid lines

# Timeline data
events = [
    (datetime(2022, 6, 1), '1.0 Stable', 'Major release'),
    (datetime(2022, 12, 1), '2.0 Alpha', 'Mobile preview'),
    (datetime(2024, 2, 1), '2.0 Beta', 'iOS/Android support'),
    (datetime(2024, 8, 1), '2.0 RC', 'Final testing'),
    (datetime(2024, 10, 2), '2.0 Stable', 'Full mobile + plugins'),
    (datetime(2024, 12, 9), '2.9.5', 'Latest stable'),
    (datetime(2025, 3, 17), 'Verso', 'Servo integration'),
    (datetime(2025, 6, 30), 'Elections', '4 years governance'),
]

fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
ax.set_facecolor(BG)

dates = [e[0] for e in events]
labels = [e[1] for e in events]
details = [e[2] for e in events]

# Plot the timeline
ax.plot(dates, [1]*len(dates), color=ACCENT, linewidth=3, marker='o', markersize=12, 
        markerfacecolor=ACCENT, markeredgecolor='white', markeredgewidth=2, zorder=3)

# Add labels
for i, (date, label, detail) in enumerate(events):
    y_offset = 0.15 if i % 2 == 0 else -0.15
    va = 'bottom' if i % 2 == 0 else 'top'
    
    ax.annotate(f'{label}\n{detail}', xy=(date, 1), xytext=(date, 1 + y_offset),
                ha='center', va=va, fontsize=9, fontweight='500', color=TEXT,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor=GRID, alpha=0.95))
    
    # Add connecting line
    ax.plot([date, date], [1, 1 + y_offset*0.7], color=GRID, linewidth=1, zorder=2)

ax.set_ylim(0.6, 1.4)
ax.set_xlim(datetime(2022, 4, 1), datetime(2025, 9, 1))

# Format x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))

ax.set_title('Tauri Framework: Journey to Cross-Platform Excellence', 
             fontsize=14, color=TEXT, fontweight='600', pad=20)

# Remove y-axis and top/right spines
ax.yaxis.set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(GRID)

# Source
fig.text(0.99, 0.02, 'Source: Tauri Blog & GitHub (2022-2025)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-timeline.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-timeline.png")
