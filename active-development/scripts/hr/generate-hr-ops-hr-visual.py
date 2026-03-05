#!/usr/bin/env python3.11
"""
HR Professional Flow Diagram — Sarah Reynolds Edition
Non-technical, warm, approachable. Focus: "what does this do FOR ME?"

Run with:  python3.11 generate-hr-ops-hr-visual.py
Requires:  pip3 install matplotlib   (pip3 uses Python 3.11 on this system)
Output:    business-demo/hr-ops-hr-visual.png  (22x16 in, 150 DPI)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

# ─── Palette ──────────────────────────────────────────────────────────────────
BG         = '#f1f5f9'
BLUE       = '#2563eb'
BLUE_LT    = '#dbeafe'
GREEN      = '#16a34a'
GREEN_LT   = '#dcfce7'
PURPLE     = '#7c3aed'
PURPLE_LT  = '#ede9fe'
ORANGE     = '#d97706'
ORANGE_LT  = '#fef3c7'
TEXT_DARK  = '#0f172a'
TEXT_MUTED = '#475569'
WHITE      = '#ffffff'
SHADOW     = '#cbd5e1'
SLATE_DARK = '#0f172a'

# ─── Canvas ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(22, 12.375))  # 16:9 for Google Slides
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, 22)
ax.set_ylim(0, 16)
ax.axis('off')

# ─── Helpers ──────────────────────────────────────────────────────────────────

def rounded_rect(ax, x, y, w, h, color, edge, lw=1.5, zorder=2, pad=0.12, alpha=1.0):
    patch = FancyBboxPatch((x, y), w, h,
                           boxstyle=f"round,pad={pad}",
                           facecolor=color, edgecolor=edge,
                           linewidth=lw, zorder=zorder, alpha=alpha)
    ax.add_patch(patch)
    return patch


def step_circle(ax, cx, cy, r, fill, label, zorder=6):
    c = Circle((cx, cy), r, color=fill, zorder=zorder)
    ax.add_patch(c)
    ax.text(cx, cy, label, ha='center', va='center',
            fontsize=14, fontweight='bold', color=WHITE, zorder=zorder + 1)


def arrow(ax, x1, y1, x2, y2, color, lw=2.5):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->, head_width=0.4, head_length=0.25",
                                color=color, lw=lw),
                zorder=8)


def dashed_arrow(ax, x1, y1, x2, y2, color='#94a3b8', lw=1.5):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->, head_width=0.25, head_length=0.2",
                                color=color, lw=lw,
                                linestyle='dashed',
                                connectionstyle='arc3,rad=0'),
                zorder=5)


# ══════════════════════════════════════════════════════════════════════════════
#  TOP BANNER
# ══════════════════════════════════════════════════════════════════════════════
banner = mpatches.FancyBboxPatch((0, 14.5), 22, 1.5,
                                  boxstyle="square,pad=0",
                                  facecolor=BLUE, edgecolor='none',
                                  linewidth=0, zorder=3)
ax.add_patch(banner)

ax.text(11, 15.25,
        "Your AI-Powered HR Assistant — How It Works For You",
        ha='center', va='center', fontsize=20, fontweight='bold',
        color=WHITE, zorder=4)

ax.text(11, 14.72,
        "No technical knowledge needed. Just ask, and let the technology do the work.",
        ha='center', va='center', fontsize=11, color=WHITE, zorder=4)


# ══════════════════════════════════════════════════════════════════════════════
#  ROW 1 — Sarah's 5-Step Journey
# ══════════════════════════════════════════════════════════════════════════════
CARD_W = 3.8
CARD_H = 3.5
CARD_Y = 10.0
card_xs = [0.4, 4.6, 8.8, 13.0, 17.2]

# ── Card 1: Open Your Console ─────────────────────────────────────────────────
cx1 = card_xs[0]
rounded_rect(ax, cx1, CARD_Y, CARD_W, CARD_H, WHITE, SHADOW, lw=1.5, zorder=3, pad=0.12)
step_circle(ax, 1.5, 13.7, 0.35, BLUE, '1')

# Laptop screen
rounded_rect(ax, 0.9, 11.8, 2.6, 1.7, BLUE_LT, BLUE, lw=2, zorder=4, pad=0.08)
# KPI bars inside screen
for i, (bar_y, bar_c, bar_w) in enumerate([(12.9, BLUE, 0.85), (12.5, GREEN, 0.7), (12.1, PURPLE, 0.55)]):
    ax.add_patch(mpatches.FancyBboxPatch((1.1, bar_y), bar_w, 0.18,
                                          boxstyle="round,pad=0.02",
                                          facecolor=bar_c, edgecolor='none', zorder=5))
# Laptop base (trapezoid)
base = mpatches.FancyBboxPatch((0.7, 11.58), 2.7, 0.22,
                                boxstyle="round,pad=0.04",
                                facecolor='#94a3b8', edgecolor='#64748b', lw=1, zorder=4)
ax.add_patch(base)
# Keyboard dots
for kx in [1.1, 1.4, 1.7, 2.0, 2.3, 2.6, 2.9, 3.2]:
    dot = Circle((kx, 11.69), 0.04, color='#475569', zorder=5)
    ax.add_patch(dot)

ax.text(2.3, 11.3, "Open Your\nConsole",
        ha='center', va='top', fontsize=11, fontweight='bold', color=TEXT_DARK, zorder=5,
        linespacing=1.35)
ax.text(2.3, 10.70, "All your HR data\nin one place —\nno switching tabs",
        ha='center', va='top', fontsize=8.5, color=TEXT_MUTED, zorder=5, linespacing=1.35)

# ── Arrow 1→2 ─────────────────────────────────────────────────────────────────
arrow(ax, 4.22, 12.05, 4.56, 12.05, BLUE)

# ── Card 2: See Everything At A Glance ────────────────────────────────────────
cx2 = card_xs[1]
rounded_rect(ax, cx2, CARD_Y, CARD_W, CARD_H, WHITE, SHADOW, lw=1.5, zorder=3, pad=0.12)
step_circle(ax, 5.7, 13.7, 0.35, PURPLE, '2')

# Dashboard panel
rounded_rect(ax, 5.0, 11.8, 2.6, 1.7, PURPLE_LT, PURPLE, lw=2, zorder=4, pad=0.08)

# 4 mini tiles 2x2
tiles = [
    (5.1, 12.9, '8 Cases', '#dc2626'),
    (6.1, 12.9, '3 Alerts', ORANGE),
    (5.1, 12.32, '15 Staff', BLUE),
    (6.1, 12.32, '5 Systems', GREEN),
]
for tx, ty, txt, tc in tiles:
    rounded_rect(ax, tx, ty, 0.88, 0.48, WHITE, SHADOW, lw=1, zorder=5, pad=0.04)
    ax.text(tx + 0.44, ty + 0.24, txt,
            ha='center', va='center', fontsize=6.5, fontweight='bold', color=tc, zorder=6)

# Mini bar chart at bottom
bar_heights = [0.2, 0.35, 0.25, 0.4, 0.3]
for bi, bh in enumerate(bar_heights):
    bx = 5.15 + bi * 0.47
    ax.add_patch(mpatches.Rectangle((bx, 11.85), 0.35, bh,
                                    facecolor='#c4b5fd', edgecolor='none', zorder=5))

ax.text(6.5, 11.3, "Your Full HR\nPicture",
        ha='center', va='top', fontsize=11, fontweight='bold', color=TEXT_DARK, zorder=5,
        linespacing=1.35)
ax.text(6.5, 10.70, "Cases, compliance,\nemployee data &\nintegration health",
        ha='center', va='top', fontsize=8.5, color=TEXT_MUTED, zorder=5, linespacing=1.35)

# ── Arrow 2→3 ─────────────────────────────────────────────────────────────────
arrow(ax, 8.42, 12.05, 8.76, 12.05, PURPLE)

# ── Card 3: Ask Your AI Copilot ───────────────────────────────────────────────
cx3 = card_xs[2]
rounded_rect(ax, cx3, CARD_Y, CARD_W, CARD_H, WHITE, SHADOW, lw=1.5, zorder=3, pad=0.12)
step_circle(ax, 9.9, 13.7, 0.35, BLUE, '3')

# Chat panel
rounded_rect(ax, 9.2, 11.8, 2.6, 1.7, BLUE_LT, BLUE, lw=2, zorder=4, pad=0.08)

# "AI Copilot" label at top of panel
ax.text(10.5, 13.4, "AI Copilot", ha='center', va='center',
        fontsize=6, fontweight='bold', color=BLUE, zorder=6)

# User bubble (right-aligned)
rounded_rect(ax, 10.35, 13.02, 1.25, 0.35, BLUE, SHADOW, lw=0, zorder=5, pad=0.05)
ax.text(10.975, 13.195, "Who is at risk?",
        ha='center', va='center', fontsize=6, color=WHITE, zorder=6)

# AI bubble (left-aligned)
rounded_rect(ax, 9.3, 12.55, 1.6, 0.35, WHITE, SHADOW, lw=1, zorder=5, pad=0.05)
ax.text(10.1, 12.725, "Searching...",
        ha='center', va='center', fontsize=6, color=TEXT_MUTED, zorder=6)

# Typing dots
for dx in [9.45, 9.65, 9.85]:
    dot = Circle((dx, 12.22), 0.08, color='#94a3b8', zorder=5)
    ax.add_patch(dot)

ax.text(10.7, 11.3, "Just Ask a\nQuestion",
        ha='center', va='top', fontsize=11, fontweight='bold', color=TEXT_DARK, zorder=5,
        linespacing=1.35)
ax.text(10.7, 10.70, 'Type anything —\n"Who needs\nattention today?"',
        ha='center', va='top', fontsize=8.5, color=TEXT_MUTED, zorder=5, linespacing=1.35)

# ── Arrow 3→4 ─────────────────────────────────────────────────────────────────
arrow(ax, 12.62, 12.05, 12.96, 12.05, GREEN)

# ── Card 4: AI Searches For You ───────────────────────────────────────────────
cx4 = card_xs[3]
rounded_rect(ax, cx4, CARD_Y, CARD_W, CARD_H, WHITE, SHADOW, lw=1.5, zorder=3, pad=0.12)
step_circle(ax, 14.1, 13.7, 0.35, GREEN, '4')

# Magnifying glass circle
mag_c = Circle((14.7, 12.65), 0.65, facecolor=GREEN_LT, edgecolor=GREEN, lw=2.5, zorder=4)
ax.add_patch(mag_c)

# Handle
ax.plot([15.18, 15.58], [12.22, 11.88], color=GREEN, lw=4, solid_capstyle='round', zorder=5)

# Dots inside magnifier (5 HR systems)
dot_positions = [
    (15.05, 12.65, '#e05a00'),
    (14.81, 12.98, '#cc0000'),
    (14.38, 12.88, BLUE),
    (14.38, 12.42, PURPLE),
    (14.81, 12.32, GREEN),
]
center_m = (14.7, 12.65)
for dx, dy, dc in dot_positions:
    ax.plot([center_m[0], dx], [center_m[1], dy], color='#86efac', lw=1, zorder=5)
    d = Circle((dx, dy), 0.09, color=dc, zorder=6)
    ax.add_patch(d)

ax.text(14.9, 11.3, "Searches All\nYour Systems",
        ha='center', va='top', fontsize=11, fontweight='bold', color=TEXT_DARK, zorder=5,
        linespacing=1.35)
ax.text(14.9, 10.70, "Workday, ADP, benefits,\nperformance & more —\nautomatically",
        ha='center', va='top', fontsize=8.5, color=TEXT_MUTED, zorder=5, linespacing=1.35)

# ── Arrow 4→5 ─────────────────────────────────────────────────────────────────
arrow(ax, 16.82, 12.05, 17.16, 12.05, GREEN)

# ── Card 5: Get Your Answer ───────────────────────────────────────────────────
cx5 = card_xs[4]
rounded_rect(ax, cx5, CARD_Y, CARD_W, CARD_H, WHITE, SHADOW, lw=1.5, zorder=3, pad=0.12)
step_circle(ax, 18.3, 13.7, 0.35, GREEN, '5')

# FINAL badge
rounded_rect(ax, 18.85, 13.52, 1.3, 0.42, GREEN, GREEN, lw=0, zorder=5, pad=0.04)
ax.text(19.5, 13.73, "FINAL STEP",
        ha='center', va='center', fontsize=7, fontweight='bold', color=WHITE, zorder=6)

# Answer panel
rounded_rect(ax, 17.6, 11.8, 2.6, 1.7, GREEN_LT, GREEN, lw=2.5, zorder=4, pad=0.08)

# Answer bubble
rounded_rect(ax, 17.7, 12.52, 2.3, 0.92, WHITE, SHADOW, lw=1, zorder=5, pad=0.06)
ax.text(18.85, 12.98, "Jordan Williams\nhas high risk.\n2 actions needed.",
        ha='center', va='center', fontsize=6, color=TEXT_DARK, zorder=6, linespacing=1.35)

# Green check badge
check_c = Circle((18.85, 12.3), 0.22, color=GREEN, zorder=6)
ax.add_patch(check_c)
ax.text(18.85, 12.3, "✓", ha='center', va='center',
        fontsize=10, fontweight='bold', color=WHITE, zorder=7)

# "Boomi AI Connected" bottom badge
rounded_rect(ax, 17.7, 11.84, 2.3, 0.28, '#15803d', '#15803d', lw=0, zorder=5, pad=0.03)
ax.text(18.85, 11.98, "✓  Boomi AI Connected",
        ha='center', va='center', fontsize=6, color=WHITE, zorder=6)

ax.text(19.1, 11.3, "Your Answer\nAppears Instantly",
        ha='center', va='top', fontsize=11, fontweight='bold', color=TEXT_DARK, zorder=5,
        linespacing=1.35)
ax.text(19.1, 10.70, "Clear, actionable\nanswer ready —\nno searching needed",
        ha='center', va='top', fontsize=8.5, color=TEXT_MUTED, zorder=5, linespacing=1.35)


# ══════════════════════════════════════════════════════════════════════════════
#  MIDDLE SECTION — "What's Happening Behind The Scenes"
# ══════════════════════════════════════════════════════════════════════════════
rounded_rect(ax, 0.4, 6.6, 21.2, 3.0, WHITE, SHADOW, lw=1.5, zorder=2, pad=0.12)

ax.text(11, 9.55,
        "What's Working Behind The Scenes (So You Don't Have To)",
        ha='center', va='center', fontsize=13, fontweight='bold', color=TEXT_DARK, zorder=4)

# ── Engine 1: Your Console ────────────────────────────────────────────────────
rounded_rect(ax, 0.9, 7.0, 3.6, 2.1, BLUE_LT, BLUE, lw=1.5, zorder=3, pad=0.1)
# Browser icon at top
rounded_rect(ax, 1.4, 8.42, 2.6, 0.52, WHITE, BLUE, lw=1, zorder=4, pad=0.05)
ax.text(2.7, 8.68, "HR Console", ha='center', va='center',
        fontsize=8, fontweight='bold', color=BLUE, zorder=5)
for item, ty in [("Boomi can embed this AI", 8.02), ("into Workday or any existing", 7.72),
                 ("SaaS app — no separate", 7.42), ("tool or login required", 7.15)]:
    ax.text(2.7, ty, item, ha='center', va='center', fontsize=8, color=TEXT_DARK, zorder=4)

# ── Connector 1→2 ─────────────────────────────────────────────────────────────
ax.plot([4.5, 5.3], [8.05, 8.05], color='#94a3b8', lw=1.5,
        linestyle=(0, (5, 3)), zorder=4)
dashed_arrow(ax, 5.2, 8.05, 5.38, 8.05, '#94a3b8')

# ── Engine 2: Boomi Platform ──────────────────────────────────────────────────
rounded_rect(ax, 5.4, 7.0, 3.6, 2.1, PURPLE_LT, PURPLE, lw=1.5, zorder=3, pad=0.1)
# Plug icon: two squares + connecting line
ax.add_patch(mpatches.FancyBboxPatch((6.3, 8.55), 0.4, 0.35,
                                      boxstyle="round,pad=0.03",
                                      facecolor=PURPLE, edgecolor='none', zorder=4))
ax.add_patch(mpatches.FancyBboxPatch((7.3, 8.55), 0.4, 0.35,
                                      boxstyle="round,pad=0.03",
                                      facecolor=PURPLE, edgecolor='none', zorder=4))
ax.plot([6.7, 7.3], [8.725, 8.725], color=PURPLE, lw=2, zorder=4)
ax.text(7.2, 8.42, "Boomi Platform", ha='center', va='center',
        fontsize=8, fontweight='bold', color=PURPLE, zorder=5)
for item, ty in [("• Receives your question", 8.07), ("• Routes it securely", 7.77),
                 ("• Manages the connection", 7.47), ("• Enterprise-grade security", 7.17)]:
    ax.text(7.2, ty, item, ha='center', va='center', fontsize=8, color=TEXT_DARK, zorder=4)

# ── Connector 2→3 ─────────────────────────────────────────────────────────────
ax.plot([9.0, 9.8], [8.05, 8.05], color='#94a3b8', lw=1.5,
        linestyle=(0, (5, 3)), zorder=4)
dashed_arrow(ax, 9.7, 8.05, 9.88, 8.05, '#94a3b8')

# ── Engine 3: Your AI Agent ───────────────────────────────────────────────────
rounded_rect(ax, 9.9, 7.0, 3.6, 2.1, GREEN_LT, GREEN, lw=1.5, zorder=3, pad=0.1)
# Robot icon
robot_head = Circle((11.3, 8.78), 0.28, color=GREEN, zorder=4)
ax.add_patch(robot_head)
for ex in [11.17, 11.43]:
    eye = Circle((ex, 8.81), 0.07, color=WHITE, zorder=5)
    ax.add_patch(eye)
ax.add_patch(mpatches.FancyBboxPatch((11.08, 8.34), 0.44, 0.38,
                                      boxstyle="round,pad=0.03",
                                      facecolor=GREEN, edgecolor='none', zorder=4))
ax.text(12.05, 8.75, "AI Agent", ha='left', va='center',
        fontsize=8, fontweight='bold', color=GREEN, zorder=5)
for item, ty in [("• Understands your question", 7.97), ("• Knows your HR context", 7.67),
                 ("• Finds the right data", 7.37), ("• Writes a clear answer", 7.07)]:
    ax.text(11.7, ty, item, ha='center', va='center', fontsize=8, color=TEXT_DARK, zorder=4)

# ── Connector 3→4 ─────────────────────────────────────────────────────────────
ax.plot([13.5, 14.3], [8.05, 8.05], color='#94a3b8', lw=1.5,
        linestyle=(0, (5, 3)), zorder=4)
dashed_arrow(ax, 14.2, 8.05, 14.38, 8.05, '#94a3b8')

# ── Engine 4: Your HR Systems ─────────────────────────────────────────────────
rounded_rect(ax, 14.4, 7.0, 6.8, 2.1, ORANGE_LT, ORANGE, lw=1.5, zorder=3, pad=0.1)
ax.text(17.8, 9.0, "Your HR Systems", ha='center', va='center',
        fontsize=8, fontweight='bold', color=ORANGE, zorder=4)

# System chips
chips = [
    (14.6, 'Workday', '#e05a00'),
    (15.9, 'ADP', '#cc0000'),
    (17.2, 'Benefits', BLUE),
    (18.5, 'Lattice', PURPLE),
    (19.8, 'Glint', GREEN),
]
for cx_chip, label, ec in chips:
    rounded_rect(ax, cx_chip, 8.32, 1.1, 0.38, '#fff9ed', ec, lw=1.2, zorder=4, pad=0.04)
    ax.text(cx_chip + 0.55, 8.51, label, ha='center', va='center',
            fontsize=7, fontweight='bold', color=ec, zorder=5)

ax.text(17.8, 7.92,
        "All queried automatically — you never need to log into each system separately",
        ha='center', va='center', fontsize=8, color=ORANGE, style='italic', zorder=4)
ax.text(17.8, 7.55,
        "One question  →  All systems searched  →  One clear answer",
        ha='center', va='center', fontsize=8, fontweight='bold', color=TEXT_DARK, zorder=4)


# ══════════════════════════════════════════════════════════════════════════════
#  BOTTOM SECTION — "How This Helps You" Benefits
# ══════════════════════════════════════════════════════════════════════════════
ax.text(11, 6.08, "How This Makes Your Job Easier",
        ha='center', va='center', fontsize=14, fontweight='bold', color=TEXT_DARK, zorder=3)

BCARDS = [
    (0.5,  BLUE_LT,   BLUE,   '50%',   BLUE,   36,
     'Less time on admin — more time on people',
     ['Stop switching between 5+ systems', 'Instant cross-system answers',
      'Automated data lookup', 'Focus on strategy, not spreadsheets']),
    (5.5,  PURPLE_LT, PURPLE, '3.6', PURPLE, 36,
     'Hours back in your week, every week',
     ['Auto-prioritized case queue', 'Full employee history in one click',
      'Compliance deadlines always current', 'No manual triage needed']),
    (10.8, GREEN_LT,  GREEN,  '85%', GREEN,  36,
     'Of HR AI users say it makes their job easier',
     ['5 systems queried simultaneously', 'Risks surfaced before they escalate',
      'Instant employee data lookup', 'Zero manual system logins']),
    (16.0, ORANGE_LT, ORANGE, '65%', ORANGE, 36,
     'Cite automation as their top compliance fix',
     ['Automated policy deadline alerts', 'Real-time audit trail',
      'Certification gaps flagged early', 'Full visibility, zero surprises']),
]

BCARD_W = 4.7
BCARD_H = 3.8
BCARD_Y = 1.5

for bx, lt, dc, big_txt, big_c, big_sz, sub, bullets in BCARDS:
    # Main card
    rounded_rect(ax, bx, BCARD_Y, BCARD_W, BCARD_H, WHITE, lt, lw=2, zorder=3, pad=0.12)
    # Top color bar
    top_bar = mpatches.FancyBboxPatch((bx, BCARD_Y + BCARD_H - 0.42), BCARD_W, 0.42,
                                       boxstyle="round,pad=0.06",
                                       facecolor=dc, edgecolor='none', zorder=4)
    ax.add_patch(top_bar)

    cx_card = bx + BCARD_W / 2

    # Big number / text
    ax.text(cx_card, BCARD_Y + 2.52, big_txt,
            ha='center', va='center', fontsize=big_sz, fontweight='bold',
            color=big_c, zorder=5, linespacing=1.1)

    # Sub-label
    ax.text(cx_card, BCARD_Y + 1.95, sub,
            ha='center', va='center', fontsize=9, color=TEXT_MUTED, zorder=5)

    # Divider
    ax.plot([bx + 0.3, bx + BCARD_W - 0.3], [BCARD_Y + 1.75, BCARD_Y + 1.75],
            color='#e2e8f0', lw=1, zorder=4)

    # Bullets
    bullet_ys = [BCARD_Y + 1.48, BCARD_Y + 1.07, BCARD_Y + 0.67, BCARD_Y + 0.27]
    for btext, by in zip(bullets, bullet_ys):
        ax.text(cx_card, by, f"✓  {btext}",
                ha='center', va='center', fontsize=8.5, color=TEXT_DARK, zorder=5)


# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER BAR
# ══════════════════════════════════════════════════════════════════════════════
footer = mpatches.FancyBboxPatch((0, 0), 22, 0.85,
                                  boxstyle="square,pad=0",
                                  facecolor=SLATE_DARK, edgecolor='none',
                                  linewidth=0, zorder=3)
ax.add_patch(footer)
ax.text(11, 0.42,
        "HR Operations Console  •  Powered by Boomi",
        ha='center', va='center', fontsize=10, color=WHITE, zorder=4)


# ══════════════════════════════════════════════════════════════════════════════
#  SAVE
# ══════════════════════════════════════════════════════════════════════════════
out_path = ("/mnt/c/users/BrianMerrick/Documents/Dev/ClaudeCode/"
            "boomicompanion_template_workspace/business-demo/hr/hr-ops-hr-visual.png")

plt.savefig(out_path, dpi=150, facecolor=BG)
plt.close()
print(f"Saved: {out_path}")
