import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme - teal/tech theme
ACCENT = '#0D6E8A'
ACCENT_LIGHT = '#1A8FB0'
BG = '#FDFBF7'
TEXT = '#1A1815'
TEXT_SECONDARY = '#4D5C6A'
GRID = '#D8E2E8'

# Data: AI Coding Tools by Est. Active Users (millions) - Jan 2026
tools = ['GitHub\nCopilot', 'Cursor', 'Claude\nCode', 'Codeium', 'Tabnine', 'Replit\nGhostwriter']
users = [15.0, 4.2, 2.8, 2.1, 1.8, 1.2]
colors = [ACCENT, ACCENT_LIGHT, '#2CA58D', '#5B8A72', '#7A9E7E', '#98B089']

fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
ax.set_facecolor(BG)

bars = ax.barh(tools, users, color=colors, height=0.6)

# Add value labels
for bar, val in zip(bars, users):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2, f'{val}M',
            va='center', fontsize=11, color=TEXT, fontweight='500')

ax.set_xlabel('Estimated Active Users (Millions)', fontsize=12, color=TEXT_SECONDARY, labelpad=10)
ax.set_title('AI Coding Assistant Landscape — January 2026', fontsize=16, color=TEXT, fontweight='600', pad=20)
ax.set_xlim(0, 18)

# Styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color(GRID)
ax.spines['left'].set_color(GRID)
ax.tick_params(colors=TEXT_SECONDARY, labelsize=10)
ax.xaxis.grid(True, alpha=0.4, color=GRID)
ax.set_axisbelow(True)

# Source
fig.text(0.99, 0.02, 'Source: Industry estimates, company announcements (Jan 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-ai-coding-ecosystem.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("Chart saved: chart-ai-coding-ecosystem.png")
