#!/usr/bin/env python3
"""Generate charts for Native vs Web Apps in AI Era newsletter."""

import matplotlib.pyplot as plt
import numpy as np

# Newsletter color scheme - teal/tech focused
ACCENT = '#0D6E8A'      # --accent (teal)
ACCENT_LIGHT = '#1A8FB4'
ACCENT_DARK = '#095570'
BG = '#FDFBF7'          # --bg (cream background)
TEXT = '#1A1815'        # --text
TEXT_SECONDARY = '#4D5C6A'  # --text-secondary
GRID = '#D8E2E8'        # --border
GOLD = '#C4A35A'        # For contrast

plt.rcParams['font.family'] = ['SF Pro Display', 'Helvetica Neue', 'sans-serif']

# Chart 1: Development Cost Comparison
fig1, ax1 = plt.subplots(figsize=(10, 6), facecolor=BG)
ax1.set_facecolor(BG)

categories = ['PWA / Web', 'Cross-Platform\n(Flutter/RN)', 'Native\n(iOS + Android)']
low_costs = [15, 40, 100]
high_costs = [50, 120, 300]

x = np.arange(len(categories))
width = 0.35

bars1 = ax1.bar(x - width/2, low_costs, width, label='Low End', color=ACCENT, alpha=0.7)
bars2 = ax1.bar(x + width/2, high_costs, width, label='High End', color=ACCENT_DARK, alpha=0.9)

ax1.set_ylabel('Development Cost ($K)', fontsize=12, color=TEXT_SECONDARY)
ax1.set_title('Development Cost by Platform (2026)', fontsize=16, color=TEXT, fontweight='600', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontsize=11, color=TEXT)
ax1.legend(fontsize=10)
ax1.set_ylim(0, 350)

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax1.annotate(f'${int(height)}K',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9, color=TEXT_SECONDARY)

for bar in bars2:
    height = bar.get_height()
    ax1.annotate(f'${int(height)}K',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9, color=TEXT_SECONDARY)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color(GRID)
ax1.spines['bottom'].set_color(GRID)
ax1.tick_params(colors=TEXT_SECONDARY)

fig1.text(0.99, 0.02, 'Source: AoxApps Cost Analysis (Jan 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-dev-costs.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()


# Chart 2: AI Productivity Boost by Framework
fig2, ax2 = plt.subplots(figsize=(10, 6), facecolor=BG)
ax2.set_facecolor(BG)

frameworks = ['Cross-Platform\n(Bridge Code)', 'Web\n(React/Vue)', 'Native iOS\n(Swift)', 'Native Android\n(Kotlin)']
productivity_boost = [60, 50, 40, 35]
colors = [ACCENT_DARK, ACCENT, ACCENT_LIGHT, '#5BA3B8']

bars = ax2.barh(frameworks, productivity_boost, color=colors, height=0.6)

ax2.set_xlabel('AI Productivity Boost (%)', fontsize=12, color=TEXT_SECONDARY)
ax2.set_title('Where AI Helps Most: Productivity Gains by Platform', fontsize=16, color=TEXT, fontweight='600', pad=20)
ax2.set_xlim(0, 75)

# Add value labels
for bar in bars:
    width = bar.get_width()
    ax2.annotate(f'{int(width)}%',
                xy=(width, bar.get_y() + bar.get_height()/2),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center', fontsize=11, fontweight='500', color=TEXT)

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color(GRID)
ax2.spines['bottom'].set_color(GRID)
ax2.tick_params(colors=TEXT_SECONDARY)

# Add insight annotation
ax2.annotate('AI excels at "bridge" code\nbetween native modules',
            xy=(60, 3.3), fontsize=9, color=TEXT_SECONDARY, style='italic',
            ha='left', va='top')

fig2.text(0.99, 0.02, 'Source: Builder.io / Dev.to Analysis (Jan 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-ai-productivity.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()


# Chart 3: Time to Market Comparison
fig3, ax3 = plt.subplots(figsize=(10, 6), facecolor=BG)
ax3.set_facecolor(BG)

approaches = ['Native\n(No AI)', 'Native\n(AI-Assisted)', 'Cross-Platform\n(No AI)', 'Cross-Platform\n(AI-Assisted)']
months = [8, 5.5, 5, 3]
colors = ['#A0A0A0', ACCENT_LIGHT, '#A0A0A0', ACCENT_DARK]

bars = ax3.bar(approaches, months, color=colors, width=0.6, edgecolor='white', linewidth=1)

ax3.set_ylabel('Time to Market (Months)', fontsize=12, color=TEXT_SECONDARY)
ax3.set_title('Speed to Market: AI Cuts Development Time by 30-40%', fontsize=16, color=TEXT, fontweight='600', pad=20)
ax3.set_ylim(0, 10)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax3.annotate(f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=12, fontweight='600', color=TEXT)

# Add percentage reduction annotations
ax3.annotate('−31%', xy=(1, 5.5), xytext=(1.3, 7),
            fontsize=10, color=ACCENT, fontweight='600',
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))
ax3.annotate('−40%', xy=(3, 3), xytext=(3.3, 4.5),
            fontsize=10, color=ACCENT_DARK, fontweight='600',
            arrowprops=dict(arrowstyle='->', color=ACCENT_DARK, lw=1.5))

ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_color(GRID)
ax3.spines['bottom'].set_color(GRID)
ax3.tick_params(colors=TEXT_SECONDARY)

fig3.text(0.99, 0.02, 'Source: Natively.dev Analysis (Jan 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-time-to-market.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()


# Chart 4: PWA vs Native Capability Gap
fig4, ax4 = plt.subplots(figsize=(10, 6), facecolor=BG)
ax4.set_facecolor(BG)

capabilities = ['Basic UI/UX', 'Camera Access', 'Push Notifications', 'Offline Mode',
                'Biometrics', 'Background Sync', 'LiDAR/AR', 'Complex Bluetooth']
pwa_scores = [100, 95, 90, 95, 85, 80, 20, 25]
native_scores = [100, 100, 100, 100, 100, 100, 100, 100]

x = np.arange(len(capabilities))
width = 0.35

bars1 = ax4.barh(x - width/2, pwa_scores, width, label='PWA (2026)', color=ACCENT, alpha=0.85)
bars2 = ax4.barh(x + width/2, native_scores, width, label='Native', color='#B8B8B8', alpha=0.5)

ax4.set_xlabel('Capability Score (%)', fontsize=12, color=TEXT_SECONDARY)
ax4.set_title('PWA vs Native: The Capability Gap in 2026', fontsize=16, color=TEXT, fontweight='600', pad=20)
ax4.set_yticks(x)
ax4.set_yticklabels(capabilities, fontsize=10, color=TEXT)
ax4.set_xlim(0, 115)
ax4.legend(loc='lower right', fontsize=10)

# Highlight the gap zone
ax4.axvspan(80, 100, alpha=0.1, color=GOLD, zorder=0)
ax4.text(90, 7.5, 'Native\nAdvantage\nZone', fontsize=8, color=TEXT_SECONDARY,
        ha='center', va='center', style='italic')

ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.spines['left'].set_color(GRID)
ax4.spines['bottom'].set_color(GRID)
ax4.tick_params(colors=TEXT_SECONDARY)

fig4.text(0.99, 0.02, 'Source: Progressier PWA Analysis (Jan 2026)', fontsize=9,
         color=TEXT_SECONDARY, ha='right', style='italic')

plt.tight_layout()
plt.savefig('/Users/welshofer/clawd/jlw-newsletter/images/chart-pwa-capabilities.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()

print("✅ Generated 4 charts:")
print("  - chart-dev-costs.png")
print("  - chart-ai-productivity.png")
print("  - chart-time-to-market.png")
print("  - chart-pwa-capabilities.png")
