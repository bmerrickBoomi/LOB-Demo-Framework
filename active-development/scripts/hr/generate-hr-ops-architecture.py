#!/usr/bin/env python3
"""
Generate HR Operations Console IT Architecture Walkthrough Diagram
Saves PNG to business-demo/hr-ops-it-architecture.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ─── Canvas setup ────────────────────────────────────────────────────────────
FIG_W, FIG_H = 18, 22
DPI = 150
BG = '#0f172a'

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis('off')

# ─── Color palette ───────────────────────────────────────────────────────────
BLUE   = '#2563eb'
PURPLE = '#7c3aed'
GREEN  = '#16a34a'
ORANGE = '#d97706'
WHITE  = '#ffffff'
MUTED  = '#94a3b8'
LIGHT  = '#cbd5e1'
BORDER_ALPHA = 0.35

BLUE_LIGHT   = '#dbeafe'
PURPLE_LIGHT = '#ede9fe'
GREEN_LIGHT  = '#dcfce7'
ORANGE_LIGHT = '#fef3c7'

# ─── Step definitions ─────────────────────────────────────────────────────────
steps = [
    {
        'num': 1,
        'label': 'IT PREREQUISITE',
        'title': 'Boomi Atom Running',
        'detail': (
            'Local Boomi Atom must be running on localhost:8077\n'
            'Verify: http://localhost:8077 is reachable\n'
            'Auth credentials configured in HTML'
        ),
        'color': PURPLE,
        'icon': '\u2699',   # gear
        'arrow_label': None,
        'arrow_dir': None,
    },
    {
        'num': 2,
        'label': 'OPEN THE SPA',
        'title': 'Open hr-operations-console.html',
        'detail': (
            'Static single-file HTML \u2014 open directly in browser\n'
            'No web server, build step, or install required\n'
            'Loads in-memory mock HR data (15 employees, 8 cases)'
        ),
        'color': BLUE,
        'icon': '\u2609',   # sun / browser symbol
        'arrow_label': None,
        'arrow_dir': None,
    },
    {
        'num': 3,
        'label': 'EXPLORE THE CONSOLE',
        'title': 'Navigate the HR Console',
        'detail': (
            '7 views: Dashboard \u00b7 Employees \u00b7 Cases\n'
            'Compliance \u00b7 Integrations \u00b7 Reports \u00b7 Settings\n'
            'All data is in-memory \u2014 resets on page refresh'
        ),
        'color': BLUE,
        'icon': '\u2609',
        'arrow_label': None,
        'arrow_dir': None,
    },
    {
        'num': 4,
        'label': 'ASK THE AI AGENT',
        'title': 'User Types Question in AI Copilot Panel',
        'detail': (
            'Right-side panel accepts free-text questions\n'
            'Suggested prompts available per view context\n'
            'Hit Send or press Enter to submit'
        ),
        'color': BLUE,
        'icon': '\u2609',
        'arrow_label': None,
        'arrow_dir': None,
    },
    {
        'num': 5,
        'label': 'HTTP POST TO BOOMI',
        'title': 'Browser \u2192 Boomi Atom (HTTP POST)',
        'detail': (
            'POST http://localhost:8077/ws/rest/v1/HR/hrOpsStatus\n'
            'Header: Authorization: Basic <base64 creds>\n'
            'Header: Content-Type: application/json\n'
            'Body: { "question": "<user input>" }'
        ),
        'color': PURPLE,
        'icon': '\u2699',
        'arrow_label': 'Network Request \u2193',
        'arrow_dir': 'down',
    },
    {
        'num': 6,
        'label': 'BOOMI ROUTES TO AGENT',
        'title': 'Boomi Atom Routes to Agent Garden',
        'detail': (
            'Atom receives REST call and triggers process\n'
            'Process invokes Boomi Agent Garden API\n'
            'Agent: HR Operations Console Agent\n'
            'Agent ID: 8cadcf3c-e97e-4f20-aa0d-82153cb2a6af'
        ),
        'color': PURPLE,
        'icon': '\u2699',
        'arrow_label': None,
        'arrow_dir': None,
    },
    {
        'num': 7,
        'label': 'AI AGENT PROCESSES',
        'title': 'HR Ops Console Agent Runs',
        'detail': (
            'Structured-mode agent with 9 OpenAPI tools:\n'
            'Get Dashboard \u00b7 Get Employees \u00b7 Get Cases\n'
            'Create Case \u00b7 Get Compliance \u00b7 Get Integrations\n'
            'Get Tasks \u00b7 Get Notifications \u00b7 Get Audit Log\n'
            '\n'
            'Connected HR Systems:\n'
            'Workday HRIS \u00b7 ADP Payroll \u00b7 Benefitfocus \u00b7 Lattice \u00b7 Glint'
        ),
        'color': GREEN,
        'icon': '\u2605',   # star / agent symbol
        'arrow_label': None,
        'arrow_dir': None,
    },
    {
        'num': 8,
        'label': 'RESPONSE RETURNED',
        'title': 'Agent Response Returns to Browser',
        'detail': (
            'JSON response with two handled variants:\n'
            '{ "data": { "answer": "..." } }  \u2190 primary\n'
            '{ "data": "..." }              \u2190 fallback string\n'
            '\n'
            'Extracted: data.answer or data (string)\n'
            'On failure: falls back to local canned responses'
        ),
        'color': PURPLE,
        'icon': '\u2699',
        'arrow_label': 'HTTP Response \u2191',
        'arrow_dir': 'up',
    },
    {
        'num': 9,
        'label': 'FINAL STEP \u2014 ANSWER DISPLAYED',
        'title': 'Answer Displayed in AI Copilot Panel',
        'detail': (
            'Answer text rendered in chat scrollbar\n'
            'Badge shown: \u2713 Boomi AI Connected\n'
            'On failure badge: \u25cc Boomi AI Offline\n'
            'Response formatted with markdown-style bold'
        ),
        'color': GREEN,
        'icon': '\u2609',
        'arrow_label': None,
        'arrow_dir': None,
    },
]

# ─── Layout constants ─────────────────────────────────────────────────────────
TITLE_Y    = 21.3
SUBTITLE_Y = 20.85
LEGEND_Y   = 0.55
FIRST_BOX_Y = 20.3   # top of first box
BOX_H      = 1.75    # height of each box
BOX_GAP    = 0.32    # gap between boxes
BOX_X      = 0.75
BOX_W      = 14.5
CIRCLE_R   = 0.32
NUM_X      = BOX_X + 0.55
ICON_X     = BOX_X + 1.45
TITLE_X    = BOX_X + 2.15
TIMELINE_X = FIG_W - 1.55   # right-side timeline bar x

def box_y(idx):
    """Return the top-left y of step box at index idx."""
    return FIRST_BOX_Y - idx * (BOX_H + BOX_GAP)

# ─── Title & Subtitle ─────────────────────────────────────────────────────────
ax.text(FIG_W / 2, TITLE_Y,
        'HR Operations Console \u2014 IT Architecture Walkthrough',
        ha='center', va='center', color=WHITE,
        fontsize=22, fontweight='bold', fontfamily='monospace')

ax.text(FIG_W / 2, SUBTITLE_Y,
        'From browser open to AI agent response \u2014 what IT needs to know',
        ha='center', va='center', color=MUTED,
        fontsize=12, fontfamily='sans-serif')

# thin separator line
ax.plot([1.2, FIG_W - 1.2], [20.65, 20.65], color=MUTED, lw=0.6, alpha=0.4)

# ─── Right-side timeline bar ───────────────────────────────────────────────────
# Spans from top of step 1 to bottom of step 9
top_bar  = box_y(0)
bot_bar  = box_y(len(steps) - 1) - BOX_H
bar_h    = top_bar - bot_bar
bar_mid  = (top_bar + bot_bar) / 2

# Draw the bar background
bar_rect = FancyBboxPatch(
    (TIMELINE_X - 0.18, bot_bar), 0.36, bar_h,
    boxstyle='round,pad=0.05',
    linewidth=1, edgecolor='#334155', facecolor='#1e293b', zorder=2
)
ax.add_patch(bar_rect)

# Downward gradient arrow (request)
req_top  = box_y(3) + 0.3   # step 4 area
req_bot  = box_y(5) - 0.05  # step 6 area
ax.annotate('', xy=(TIMELINE_X, req_bot), xytext=(TIMELINE_X, req_top),
            arrowprops=dict(arrowstyle='->', color='#60a5fa', lw=2.2),
            zorder=5)
ax.text(TIMELINE_X + 0.28, (req_top + req_bot) / 2, 'REQUEST',
        ha='left', va='center', color='#60a5fa', fontsize=7,
        fontweight='bold', rotation=90)

# Upward arrow (response)
res_top  = box_y(5) + 0.1
res_bot  = box_y(7) - 0.1
ax.annotate('', xy=(TIMELINE_X, res_top), xytext=(TIMELINE_X, res_bot),
            arrowprops=dict(arrowstyle='->', color='#4ade80', lw=2.2),
            zorder=5)
ax.text(TIMELINE_X + 0.28, (res_top + res_bot) / 2, 'RESPONSE',
        ha='left', va='center', color='#4ade80', fontsize=7,
        fontweight='bold', rotation=90)

# Timeline label
ax.text(TIMELINE_X, top_bar + 0.28, 'DATA\nFLOW',
        ha='center', va='center', color=MUTED,
        fontsize=7, fontweight='bold')

# ─── Draw step boxes ──────────────────────────────────────────────────────────
for i, step in enumerate(steps):
    y_top = box_y(i)
    color = step['color']

    # Subtle colored glow behind box
    glow = FancyBboxPatch(
        (BOX_X - 0.06, y_top - BOX_H - 0.04), BOX_W + 0.12, BOX_H + 0.08,
        boxstyle='round,pad=0.12',
        linewidth=0, facecolor=color, alpha=0.08, zorder=1
    )
    ax.add_patch(glow)

    # Main box
    box = FancyBboxPatch(
        (BOX_X, y_top - BOX_H), BOX_W, BOX_H,
        boxstyle='round,pad=0.10',
        linewidth=1.5, edgecolor=color,
        facecolor='#1e293b', alpha=0.97, zorder=3
    )
    ax.add_patch(box)

    # Left accent strip
    accent = FancyBboxPatch(
        (BOX_X, y_top - BOX_H), 0.28, BOX_H,
        boxstyle='round,pad=0.0',
        linewidth=0, facecolor=color, alpha=0.75, zorder=4
    )
    ax.add_patch(accent)

    # Step number circle
    circle_y = y_top - BOX_H / 2
    circ = plt.Circle((NUM_X, circle_y), CIRCLE_R,
                       color=color, zorder=5, linewidth=0)
    ax.add_patch(circ)
    ax.text(NUM_X, circle_y, str(step['num']),
            ha='center', va='center', color=WHITE,
            fontsize=11, fontweight='bold', zorder=6)

    # Icon
    ax.text(ICON_X, circle_y + 0.02, step['icon'],
            ha='center', va='center', fontsize=16, zorder=6)

    # Step label (small caps style)
    ax.text(TITLE_X, y_top - 0.33, f"STEP {step['num']} \u2014 {step['label']}",
            ha='left', va='center', color=color,
            fontsize=7.5, fontweight='bold',
            fontfamily='monospace', zorder=6)

    # Title
    ax.text(TITLE_X, y_top - 0.68, step['title'],
            ha='left', va='center', color=WHITE,
            fontsize=11.5, fontweight='bold', zorder=6)

    # Detail text
    ax.text(TITLE_X, y_top - 1.18, step['detail'],
            ha='left', va='center', color=LIGHT,
            fontsize=8.5, linespacing=1.6, zorder=6,
            fontfamily='monospace')

    # Arrow label badge (Network Request / HTTP Response)
    if step['arrow_label']:
        badge_x = BOX_X + BOX_W - 0.15
        badge_y = y_top - BOX_H - 0.02 if step['arrow_dir'] == 'down' else y_top + 0.0
        badge_y = y_top - BOX_H / 2
        badge_col = '#60a5fa' if step['arrow_dir'] == 'down' else '#4ade80'
        ax.text(badge_x, badge_y, step['arrow_label'],
                ha='right', va='center', color=badge_col,
                fontsize=8, fontweight='bold',
                fontfamily='monospace', zorder=6)

    # Arrow to next step
    if i < len(steps) - 1:
        arr_x = BOX_X + BOX_W / 2
        arr_y_start = y_top - BOX_H - 0.01
        arr_y_end   = box_y(i + 1) + 0.01
        ax.annotate('', xy=(arr_x, arr_y_end), xytext=(arr_x, arr_y_start),
                    arrowprops=dict(
                        arrowstyle='->', color=WHITE,
                        lw=1.5, alpha=0.45,
                        connectionstyle='arc3,rad=0'
                    ), zorder=7)

# ─── Layer labels on the left ─────────────────────────────────────────────────
def layer_bracket(y_top, y_bot, label, color):
    mid_y = (y_top + y_bot) / 2
    bx = BOX_X - 0.35
    # vertical line
    ax.plot([bx, bx], [y_bot, y_top], color=color, lw=2, alpha=0.7, zorder=2)
    # ticks
    ax.plot([bx, bx + 0.12], [y_top, y_top], color=color, lw=2, alpha=0.7, zorder=2)
    ax.plot([bx, bx + 0.12], [y_bot, y_bot], color=color, lw=2, alpha=0.7, zorder=2)
    ax.text(bx - 0.12, mid_y, label,
            ha='center', va='center', color=color,
            fontsize=7.5, fontweight='bold', rotation=90, zorder=2)

# User / Browser: steps 2-4 (indices 1-3)
layer_bracket(
    box_y(1),
    box_y(3) - BOX_H,
    'USER / BROWSER',
    BLUE
)
# Boomi Atom: steps 1, 5, 6, 8 — shown as two brackets
layer_bracket(
    box_y(0),
    box_y(0) - BOX_H,
    'BOOMI ATOM',
    PURPLE
)
layer_bracket(
    box_y(4),
    box_y(5) - BOX_H,
    'BOOMI ATOM',
    PURPLE
)
layer_bracket(
    box_y(7),
    box_y(7) - BOX_H,
    'BOOMI ATOM',
    PURPLE
)
# Agent Garden: steps 7, 9 (indices 6, 8)
layer_bracket(
    box_y(6),
    box_y(8) - BOX_H,
    'AGENT GARDEN',
    GREEN
)

# ─── Legend ───────────────────────────────────────────────────────────────────
legend_items = [
    (PURPLE, '\u2699  Boomi Atom Layer'),
    (BLUE,   '\u2609  User / Browser Layer'),
    (GREEN,  '\u2605  Boomi Agent Garden Layer'),
    (ORANGE, '\u229e  HR Systems Layer (mock data)'),
]

legend_box = FancyBboxPatch(
    (0.7, LEGEND_Y - 0.22), FIG_W - 1.4, 0.82,
    boxstyle='round,pad=0.12',
    linewidth=1, edgecolor='#334155',
    facecolor='#1e293b', zorder=3
)
ax.add_patch(legend_box)

ax.text(FIG_W / 2, LEGEND_Y + 0.48, 'COLOR LEGEND \u2014 LAYER KEY',
        ha='center', va='center', color=MUTED,
        fontsize=8, fontweight='bold', fontfamily='monospace', zorder=4)

item_w = (FIG_W - 1.4) / len(legend_items)
for j, (col, label) in enumerate(legend_items):
    cx = 1.1 + item_w * j + item_w / 2
    swatch = FancyBboxPatch(
        (cx - item_w / 2 + 0.1, LEGEND_Y - 0.05), 0.22, 0.32,
        boxstyle='round,pad=0.04',
        linewidth=0, facecolor=col, alpha=0.85, zorder=5
    )
    ax.add_patch(swatch)
    ax.text(cx - item_w / 2 + 0.45, LEGEND_Y + 0.10, label,
            ha='left', va='center', color=LIGHT,
            fontsize=9, zorder=5)

# ─── Footer ───────────────────────────────────────────────────────────────────
ax.text(FIG_W / 2, 0.18,
        'HR Operations Console \u00b7 Boomi Integration Demo \u00b7 Generated 2026-03-03',
        ha='center', va='center', color=MUTED,
        fontsize=7.5, fontfamily='monospace')

# ─── Save ─────────────────────────────────────────────────────────────────────
OUT = '/mnt/c/users/BrianMerrick/Documents/Dev/ClaudeCode/boomicompanion_template_workspace/business-demo/hr-ops-it-architecture.png'
plt.tight_layout(pad=0)
plt.savefig(OUT, dpi=DPI, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
plt.close(fig)
print(f'Saved: {OUT}')
