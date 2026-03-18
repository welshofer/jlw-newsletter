import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

ACCENT = '#5B6B4A'
ACCENT2 = '#8B4513'
ACCENT3 = '#4A6B8A'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SEC = '#5C564D'
GRID = '#E5E0D8'

# Key events timeline
events = [
    (datetime(1944, 12, 16), "German offensive\nbegins", -1),
    (datetime(1944, 12, 17), "Malmedy\nMassacre", 1),
    (datetime(1944, 12, 19), "106th Div.\nsurrenders\n(~9,000 POWs)", -1),
    (datetime(1944, 12, 19), "Eisenhower's\nVerdun meeting", 1),
    (datetime(1944, 12, 21), "Bastogne\nencircled", -1),
    (datetime(1944, 12, 22), 'McAuliffe:\n"NUTS!"', 1),
    (datetime(1944, 12, 23), "Skies clear —\nAllied air power\nunleashed", -1),
    (datetime(1944, 12, 26), "Patton's 4th\nArmored relieves\nBastogne", 1),
    (datetime(1945, 1, 1), "Operation\nBodenplatte", -1),
    (datetime(1945, 1, 3), "Allied\ncounteroffensive\nbegins", 1),
    (datetime(1945, 1, 25), "Bulge\neliminated", -1),
]

# German max penetration depth over time (miles from start line)
dates_pen = [
    datetime(1944, 12, 16), datetime(1944, 12, 18), datetime(1944, 12, 20),
    datetime(1944, 12, 22), datetime(1944, 12, 24), datetime(1944, 12, 26),
    datetime(1944, 12, 28), datetime(1944, 12, 31), datetime(1945, 1, 3),
    datetime(1945, 1, 8), datetime(1945, 1, 16), datetime(1945, 1, 25)
]
penetration = [5, 20, 35, 45, 50, 50, 48, 42, 35, 25, 12, 0]

fig, ax = plt.subplots(figsize=(14, 7), facecolor=BG)
ax.set_facecolor(BG)

# Plot penetration depth
ax.fill_between(dates_pen, penetration, alpha=0.15, color=ACCENT2)
ax.plot(dates_pen, penetration, color=ACCENT2, linewidth=2.5, marker='o',
        markersize=5, label='German max penetration (miles)')

# Add event markers
for date, label, side in events:
    color = ACCENT2 if side < 0 else ACCENT
    y_pos = 55 + (side * 3) if side > 0 else -8
    ax.axvline(x=date, color=color, alpha=0.2, linewidth=1, linestyle='--')

    # Alternate text above and below
    if side > 0:
        ax.annotate(label, xy=(date, 52), fontsize=7.5,
                    color=color, ha='center', va='bottom', fontweight='500',
                    fontfamily='sans-serif')
    else:
        ax.annotate(label, xy=(date, -3), fontsize=7.5,
                    color=color, ha='center', va='top', fontweight='500',
                    fontfamily='sans-serif')

# Formatting
ax.set_title('The Battle of the Bulge: Timeline & German Penetration Depth',
             fontsize=16, color=TEXT, fontweight='600', pad=20, fontfamily='serif')
ax.set_ylabel('Miles from start line', fontsize=12, color=TEXT_SEC)
ax.set_ylim(-25, 72)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
ax.grid(True, axis='y', alpha=0.4, color=GRID)
ax.grid(True, axis='x', alpha=0.2, color=GRID)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(GRID)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=TEXT_SEC)

# Add "Meuse River (objective)" line
ax.axhline(y=60, color=ACCENT3, linestyle=':', linewidth=1.5, alpha=0.6)
ax.text(datetime(1945, 1, 20), 61, 'Meuse River (German objective — never reached)',
        fontsize=9, color=ACCENT3, style='italic', ha='right')

ax.legend(fontsize=10, frameon=False, loc='upper right')

fig.text(0.99, 0.01,
         'Source: Cole, The Ardennes: Battle of the Bulge (1965); MacDonald, A Time for Trumpets (1985)',
         fontsize=8, color=TEXT_SEC, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-timeline.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-timeline.png")
