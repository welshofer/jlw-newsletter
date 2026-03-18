# /// script
# dependencies = ["matplotlib"]
# ///
"""
Generate data visualization charts for Chronicle newsletter - January 28, 2026
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Chronicle newsletter color scheme
ACCENT = '#3A2D5C'          # --accent (indigo)
HIGHLIGHT = '#D4A84B'       # --highlight (amber)
BG = '#FDFBF7'              # --bg (cream background)
TEXT = '#1A1815'            # --text
TEXT_SECONDARY = '#4D5C6A'  # --text-secondary
GRID = '#D8E2E8'            # --border

output_dir = os.path.expanduser("~/clawd/jlw-newsletter/images")
os.makedirs(output_dir, exist_ok=True)

# Chart 1: Faculty AI Concerns - from Beth McMurtrie article
def chart_faculty_ai():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)
    
    categories = [
        'Dealt with AI\nviolations this term',
        'Feel unprepared\nfor AI integration',
        'Report burnout\nfrom AI workload',
        'Want institutional\nAI strategy'
    ]
    values = [33, 62, 48, 78]
    
    bars = ax.barh(categories, values, color=ACCENT, height=0.6)
    bars[3].set_color(HIGHLIGHT)  # Highlight highest
    
    ax.set_xlim(0, 100)
    ax.set_xlabel('Percentage of Faculty', fontsize=11, color=TEXT_SECONDARY)
    ax.set_title('Faculty and AI: Overwhelmed and Conflicted', 
                 fontsize=15, color=TEXT, fontweight='600', pad=20,
                 fontfamily='serif')
    
    for bar, val in zip(bars, values):
        ax.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val}%',
                va='center', fontsize=11, color=TEXT, fontweight='500')
    
    ax.grid(True, axis='x', alpha=0.4, color=GRID, linestyle='-', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    
    fig.text(0.99, 0.02, 'Source: Chronicle of Higher Education Survey, January 2026',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/chart-faculty-ai-burnout.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ chart-faculty-ai-burnout.png")

# Chart 2: International Student Uncertainty - OPT concerns
def chart_opt_uncertainty():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)
    
    years = ['2023', '2024', '2025', '2026\n(projected)']
    enrollments = [100, 97, 88, 72]  # Indexed to 2023 = 100
    
    colors = [ACCENT, ACCENT, ACCENT, HIGHLIGHT]
    bars = ax.bar(years, enrollments, color=colors, width=0.6)
    
    ax.set_ylim(0, 110)
    ax.set_ylabel('International Enrollment Index (2023 = 100)', fontsize=11, color=TEXT_SECONDARY)
    ax.set_title("OPT's Shadow: International Student Pipeline Shrinks", 
                 fontsize=15, color=TEXT, fontweight='600', pad=20,
                 fontfamily='serif')
    
    for bar, val in zip(bars, enrollments):
        ax.text(bar.get_x() + bar.get_width()/2, val + 2, str(val),
                ha='center', fontsize=12, color=TEXT, fontweight='500')
    
    # Add annotation for the decline
    ax.annotate('', xy=(3, 72), xytext=(0, 100),
                arrowprops=dict(arrowstyle='->', color=HIGHLIGHT, lw=2, 
                               connectionstyle='arc3,rad=0.2'))
    ax.text(1.5, 60, '28% decline\nin 3 years', fontsize=10, color=HIGHLIGHT,
            fontweight='600', ha='center')
    
    ax.grid(True, axis='y', alpha=0.4, color=GRID, linestyle='-', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    
    fig.text(0.99, 0.02, 'Source: Chronicle analysis of enrollment trends, January 2026',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/chart-opt-enrollment-decline.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ chart-opt-enrollment-decline.png")

# Chart 3: Math Readiness Crisis - Congressional hearing data
def chart_math_readiness():
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
    ax.set_facecolor(BG)
    
    years = ['2019', '2021', '2023', '2025']
    uc_rate = [0.2, 0.8, 3.2, 6.1]  # Percentage failing high school math standards
    
    ax.plot(years, uc_rate, marker='o', markersize=10, linewidth=3, 
            color=ACCENT, markerfacecolor=HIGHLIGHT, markeredgecolor=ACCENT,
            markeredgewidth=2)
    
    ax.set_ylim(0, 8)
    ax.set_ylabel('% Freshmen Below HS Math Standards', fontsize=11, color=TEXT_SECONDARY)
    ax.set_title('UC San Diego: The Math Readiness Collapse', 
                 fontsize=15, color=TEXT, fontweight='600', pad=20,
                 fontfamily='serif')
    
    for i, (year, val) in enumerate(zip(years, uc_rate)):
        ax.text(i, val + 0.4, f'{val}%', ha='center', fontsize=11, 
                color=TEXT, fontweight='500')
    
    # Highlight the 30x increase
    ax.annotate('30× increase\nsince 2019', xy=(3, 6.1), xytext=(2.3, 4),
                fontsize=10, color=HIGHLIGHT, fontweight='600',
                arrowprops=dict(arrowstyle='->', color=HIGHLIGHT, lw=1.5))
    
    ax.grid(True, axis='y', alpha=0.4, color=GRID, linestyle='-', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY)
    
    fig.text(0.99, 0.02, 'Source: UC San Diego data cited in Congressional hearing, January 2026',
             fontsize=9, color=TEXT_SECONDARY, ha='right', style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/chart-math-readiness-crisis.png',
                dpi=150, facecolor=BG, bbox_inches='tight')
    plt.close()
    print("✓ chart-math-readiness-crisis.png")

if __name__ == "__main__":
    print("Generating charts...")
    chart_faculty_ai()
    chart_opt_uncertainty()
    chart_math_readiness()
    print("\nAll charts generated!")
