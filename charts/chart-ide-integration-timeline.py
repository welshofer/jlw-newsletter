import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Newsletter color scheme
ACCENT = '#0D6E8A'
ACCENT_LIGHT = '#1A8FB0'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Timeline data: Major IDE AI integration milestones
events = [
    (datetime(2021, 6, 1), 'GitHub Copilot Preview', 'VSCode'),
    (datetime(2022, 6, 1), 'Copilot GA', 'VSCode, JetBrains'),
    (datetime(2023, 3, 1), 'Cursor Launch', 'Native IDE'),
    (datetime(2024, 3, 1), 'Claude Code Beta', 'Terminal'),
    (datetime(2024, 10, 1), 'Windsurf Launch', 'Native IDE'),
    (datetime(2025, 11, 1), 'Claude Code GA', 'Terminal + VSCode'),
    (datetime(2026, 1, 22), 'JetBrains + Codex', 'All JetBrains IDEs'),
    (datetime(2026, 1, 22), 'Copilot SDK', 'Embeddable'),
]

fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
ax.set_facecolor(BG)

dates = [e[0] for e in events]
y_positions = [1 if i % 2 == 0 else -1 for i in range(len(events))]

# Plot timeline
ax.axhline(0, color=ACCENT, linewidth=2, alpha=0.3)
ax.scatter(dates, [0]*len(dates), s=100, c=ACCENT, zorder=5)

# Add labels
for i, (date, event, platform) in enumerate(events):
    y = y_positions[i] * 0.5
    va = 'bottom' if y > 0 else 'top'
    ax.annotate(f'{event}\n({platform})', (date, 0), xytext=(date, y),
                ha='center', va=va, fontsize=9, color=TEXT,
                arrowprops=dict(arrowstyle='-', color=GRID, lw=0.8))

ax.set_xlim(datetime(2021, 1, 1), datetime(2026, 6, 1))
ax.set_ylim(-1.2, 1.2)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))

ax.set_title('AI in IDEs: From Plugin to Platform (2021–2026)', fontsize=16, color=TEXT, fontweight='600', pad=20)

# Hide y-axis
ax.yaxis.set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=TEXT_SECONDARY, labelsize=9)

# Highlight "This Week"
ax.axvspan(datetime(2026, 1, 19), datetime(2026, 1, 26), alpha=0.15, color=ACCENT)
ax.text(datetime(2026, 1, 22), 1.05, 'This Week', ha='center', fontsize=9,
        color=ACCENT, fontweight='600')

fig.text(0.99, 0.02, 'Source: Company announcements, press releases', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-ide-timeline.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-ide-timeline.png")
