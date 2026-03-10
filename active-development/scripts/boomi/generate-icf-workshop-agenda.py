#!/usr/bin/env python3
# /// script
# dependencies = ["matplotlib"]
# ///
"""
Generates: business-demo/boomi/icf-workshop-alignment-agenda.png

ICF Blueprint Workshop Alignment Call — Agenda & Goals visualization.

Usage:
    python3.11 active-development/scripts/boomi/generate-icf-workshop-agenda.py
"""

import os
import textwrap
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D

# ── Palette — Boomi brand colours ─────────────────────────────────────────────
# Primary brand:  #003C57  (Boomi navy/teal, Pantone 302 C)
# Accent:         #FF7864  (Boomi coral,     Pantone 805 C)
# Dark navy:      #082B55  (Boomi deep navy, per Brandfetch)
# All other tones are derived tints/shades of these anchors.
C = {
    'bg':        '#ffffff',
    'boomi':     '#003C57',       # Boomi primary navy
    'header_bg': '#003C57',       # Boomi primary navy
    'header_sub':'#7FBFD4',       # tint of primary navy

    # blue  → Boomi medium brand blue (derived from primary navy)
    'blue':      '#1A6E99',
    'blue_lt':   '#E6F3F8',

    # green → Boomi teal (sibling of primary navy)
    'green':     '#007A8A',
    'green_lt':  '#E0F4F6',

    # orange → Boomi coral accent (official brand colour)
    'orange':    '#FF7864',
    'orange_lt': '#FFF0EE',

    # purple → Boomi deep navy (darker brand variant)
    'purple':    '#082B55',
    'purple_lt': '#E8EDF4',

    'text':      '#0f172a',
    'text2':     '#334155',
    'text3':     '#64748b',
    'border':    '#e2e8f0',
    'panel':     '#f8fafc',
}

COLOR_MAP = {
    'blue':   (C['blue'],   C['blue_lt']),
    'green':  (C['green'],  C['green_lt']),
    'orange': (C['orange'], C['orange_lt']),
    'purple': (C['purple'], C['purple_lt']),
}

# ── Canvas — 16:9 for Google Slides ───────────────────────────────────────────
# Coordinate space is 16 × 9 (1 unit = 1 inch at 150 DPI → 150 px/unit).
# All Y values are natively in the 0-9 range; no compression occurs.
DPI = 150
FW, FH = 16, 9

fig, ax = plt.subplots(figsize=(FW, FH))
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.axis('off')
fig.patch.set_facecolor(C['bg'])


# ── Helpers ───────────────────────────────────────────────────────────────────
def box(x, y, w, h, fc, ec=None, lw=1.0, r=0.15, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f'round,pad=0,rounding_size={r}',
                       facecolor=fc, edgecolor=ec if ec else fc,
                       linewidth=lw, zorder=zorder)
    ax.add_patch(p)


def txt(x, y, s, size=10, color=C['text'], weight='normal',
        ha='center', va='center', zorder=6):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=zorder, multialignment=ha)


def hline(x1, x2, y, color=C['border'], lw=0.7, zorder=3):
    ax.add_line(Line2D([x1, x2], [y, y], color=color, lw=lw, zorder=zorder))


def draw_goal_icon(icon, cx, cy, s=0.09):
    """Draw a white icon centred at (cx, cy). s = base scale unit."""
    kw = dict(zorder=7)
    lw = 1.8
    if icon == 'align':
        # Two overlapping circles — Venn / alignment
        ax.add_patch(Circle((cx - s * 0.60, cy), s,
                            facecolor='none', edgecolor='white', linewidth=lw, **kw))
        ax.add_patch(Circle((cx + s * 0.60, cy), s,
                            facecolor='none', edgecolor='white', linewidth=lw, **kw))
    elif icon == 'educate':
        # Lightbulb — circle body + two horizontal base lines
        ax.add_patch(Circle((cx, cy + s * 0.28), s,
                            facecolor='none', edgecolor='white', linewidth=lw, **kw))
        ax.add_line(Line2D([cx - s * 0.55, cx + s * 0.55],
                           [cy - s * 0.62, cy - s * 0.62],
                           color='white', lw=lw, zorder=7))
        ax.add_line(Line2D([cx - s * 0.38, cx + s * 0.38],
                           [cy - s * 0.92, cy - s * 0.92],
                           color='white', lw=lw, zorder=7))
    elif icon == 'scope':
        # Bullseye — two rings + solid centre dot
        ax.add_patch(Circle((cx, cy), s * 1.18,
                            facecolor='none', edgecolor='white', linewidth=lw, **kw))
        ax.add_patch(Circle((cx, cy), s * 0.68,
                            facecolor='none', edgecolor='white', linewidth=lw, **kw))
        ax.add_patch(Circle((cx, cy), s * 0.22,
                            facecolor='white', edgecolor='none', **kw))


# ══════════════════════════════════════════════════════════════════════════════
# HEADER  (top 0.50 of canvas)
# ══════════════════════════════════════════════════════════════════════════════
box(0, 8.50, FW, 0.50, C['header_bg'], None, r=0, zorder=2)
txt(FW / 2, 8.75,
    'ICF Blueprint \u2014 Workshop Alignment Call Agenda',
    size=17, weight='bold', color='white', zorder=5)

# ══════════════════════════════════════════════════════════════════════════════
# WORKSHOP GOALS STRIP
# ══════════════════════════════════════════════════════════════════════════════
txt(0.50, 8.38, 'Workshop Goals',
    size=9.5, weight='bold', color=C['boomi'], ha='left', zorder=5)

goals = [
    ('blue',   'align',    'Establish Stakeholder Alignment',
     'Align the team on the ICF Blueprint\nworkshop value and next steps'),
    ('green',  'educate',  'Build Shared Understanding',
     'Educate the team on architecture and patterns\nso decisions are grounded in real knowledge'),
    ('purple', 'scope',    'Scope the Right Pilot',
     'Collect use cases, timing, and resourcing\nto size the pilot correctly'),
]

MAR    = 0.50
GW     = (FW - 2 * MAR - 2 * 0.18) / 3   # goal card width
GH     = 0.74
ICON_W = 0.52
ICON_H = 0.34

for i, (ck, icon, gtitle, gdesc) in enumerate(goals):
    color, bg = COLOR_MAP[ck]
    gx = MAR + i * (GW + 0.18)
    gy = 7.58

    # Card
    box(gx, gy, GW, GH, bg, color, lw=1.3, r=0.14, zorder=3)
    # Left accent bar
    box(gx, gy, 0.07, GH, color, None, r=0.05, zorder=4)

    # Icon badge (coloured rounded square)
    bpx = gx + 0.16
    bpy = gy + GH / 2 - ICON_H / 2
    box(bpx, bpy, ICON_W, ICON_H, color, None, r=0.10, zorder=4)
    draw_goal_icon(icon, bpx + ICON_W / 2, bpy + ICON_H / 2)

    # Text — sits to the right of the icon badge
    TX = gx + 0.82 + (GW - 0.82) / 2
    txt(TX, gy + GH * 0.68, gtitle,
        size=9.5, weight='bold', color=C['boomi'],
        ha='center', zorder=5)
    txt(TX, gy + GH * 0.28, gdesc,
        size=7.5, color=C['text2'],
        ha='center', zorder=5)

hline(MAR, FW - MAR, 7.49)

# ══════════════════════════════════════════════════════════════════════════════
# AGENDA ITEMS — 6 cards, 2 per section
# Combined cards carry two subitems; single cards carry one.
# subitems: list of (subtitle, goal_text)
# ══════════════════════════════════════════════════════════════════════════════
sections = [
    {
        'label': 'Pre-Workshop',
        'ck': 'blue',
        'rows': [[
            {
                'num': 1, 'ck': 'blue',
                'title': 'Workshop Intent & Decision Drivers',
                'subitems': [
                    ('Confirm Intent + Guardrails',
                     'Align that the next step is education and architecture '
                     'alignment\u2014so every participant hour drives maximum value.'),
                    ('Decision Drivers + Timeline Reality',
                     'Understand timing pressure and internal milestones '
                     '(security, procurement, IT windows) before committing resources.'),
                ],
            },
            {
                'num': 2, 'ck': 'blue',
                'title': 'Confirm Evaluation Criteria',
                'subitems': [
                    ('Explicit, Measurable Benchmarks',
                     'Lock comfort items into explicit, measurable criteria: '
                     'staff capability, repeatability, scalability, and operability.'),
                    ('Use Case Scope Alignment',
                     'Agree on the correct use case scope for the workshop so '
                     'the right depth and boundaries are set before it begins.'),
                ],
            },
        ]],
    },
    {
        'label': 'Workshop',
        'ck': 'green',
        'rows': [[
            {
                'num': 3, 'ck': 'green',
                'title': 'Use Case: Primary Proof-of-Technology',
                'subitems': [
                    ('CLM \u2192 Costpoint: Happy-Path Scope',
                     'Validate CLM \u2192 Costpoint as the happy-path use case; identify '
                     'required depth vs. Phase 2 complexity and delta handling.'),
                    ('Art of the Possible: Events & APIs',
                     'Explore what becomes achievable with event-driven patterns and '
                     'API-led connectivity \u2014 expanding the vision beyond the initial use case.'),
                ],
            },
            {
                'num': 4, 'ck': 'green',
                'title': 'Architecture, Runtime & BPM Scope',
                'subitems': [
                    ('Architecture & Runtime',
                     'Agree on hybrid / on-prem runtime to minimise latency and '
                     'avoid cloud-hopping for on-prem APIs (Costpoint, CLM).'),
                    ("Workflow / BPM: Integrify's Role",
                     'Clarify the role of Integrify to sharpen pilot focus; align '
                     'on whether Boomi Flow adds the most value now or as a '
                     'dedicated future phase.'),
                ],
            },
        ]],
    },
    {
        'label': 'Post-Workshop',
        'ck': 'purple',
        'rows': [[
            {
                'num': 5, 'ck': 'purple',
                'title': 'Enablement & Support Model',
                'subitems': [
                    ('Guided Self-Run Framework',
                     'Confirm whether a guided self-run model or a Boomi-led build '
                     'is the right fit; define the support structure accordingly.'),
                ],
            },
            {
                'num': 6, 'ck': 'purple',
                'title': 'Close: Workshop Outputs + Next Steps',
                'subitems': [
                    ('Locked Scope & Clear Ownership',
                     'Lock scope, attendees, and deliverables so every participant '
                     'walks away with clear next steps and a de-risked pilot proposal.'),
                ],
            },
        ]],
    },
]

CGAP      = 0.22   # column gap
SGAP      = 0.15   # gap before each section (after first)
SECTION_H = 0.21   # section header bar height
CW        = (FW - 2 * MAR - CGAP) / 2
# 3 sections × 1 row each; fill space between goals strip and footer
TOP_Y     = 7.40
FOOTER_Y  = 0.39
CH        = (TOP_Y - FOOTER_Y - 3 * SECTION_H - 2 * SGAP) / 3   # ≈ 2.02

cur_y = TOP_Y

for s_idx, section in enumerate(sections):
    if s_idx > 0:
        cur_y -= SGAP

    sec_color, sec_bg = COLOR_MAP[section['ck']]

    # ── Section header ───────────────────────────────────────────
    box(MAR, cur_y - SECTION_H, 1.90, SECTION_H,
        sec_bg, sec_color, lw=1.0, r=0.10, zorder=3)
    txt(MAR + 0.18, cur_y - SECTION_H / 2, section['label'],
        size=8.5, weight='bold', color=sec_color,
        ha='left', va='center', zorder=5)
    hline(MAR + 2.00, FW - MAR, cur_y - SECTION_H / 2,
          color=sec_color, lw=0.8, zorder=3)
    cur_y -= SECTION_H

    for row in section['rows']:
        by = cur_y - CH

        for c_idx, item in enumerate(row):
            bx    = MAR + c_idx * (CW + CGAP)
            color, bg = COLOR_MAP[item['ck']]

            # ── Card shell ──────────────────────────────────────
            box(bx, by, CW, CH, C['panel'], C['border'], lw=1.0, r=0.16, zorder=2)

            # Coloured left accent strip
            box(bx, by, 0.07, CH, color, None, r=0.05, zorder=3)

            # ── Number circle ────────────────────────────────────
            NR  = 0.18
            NCX = bx + 0.38
            NCY = by + CH - 0.31
            nc  = Circle((NCX, NCY), NR, facecolor=color, edgecolor='none', zorder=4)
            ax.add_patch(nc)
            txt(NCX, NCY, str(item['num']),
                size=10, weight='bold', color='white', zorder=5)

            # ── Title ────────────────────────────────────────────
            txt(bx + 0.72, NCY, item['title'],
                size=9.5, weight='bold', color=C['boomi'],
                ha='left', va='center', zorder=4)

            # ── Main divider ─────────────────────────────────────
            DIV_Y = by + CH - 0.54
            hline(bx + 0.14, bx + CW - 0.14, DIV_Y, lw=0.6)

            # ── Content area ─────────────────────────────────────
            subitems = item['subitems']
            if len(subitems) == 1:
                # Single item — subtitle + goal text
                subtitle, goal = subitems[0]
                txt(bx + 0.22, DIV_Y - 0.10, subtitle,
                    size=8.0, weight='bold', color=color,
                    ha='left', va='top', zorder=4)
                wrapped = textwrap.fill(goal.replace('\n', ' '), width=58)
                txt(bx + 0.22, DIV_Y - 0.25, wrapped,
                    size=7.5, color=C['text2'],
                    ha='left', va='top', zorder=4)
            else:
                # Two sub-items — split content area with a mid separator
                content_top = DIV_Y - 0.07
                content_bot = by + 0.10
                mid_sep_y   = (content_top + content_bot) / 2

                hline(bx + 0.14, bx + CW - 0.14, mid_sep_y,
                      color=C['border'], lw=0.5)

                for s_i, (subtitle, goal) in enumerate(subitems):
                    if s_i == 0:
                        title_y = content_top - 0.02
                        goal_y  = content_top - 0.16
                    else:
                        title_y = mid_sep_y - 0.05
                        goal_y  = mid_sep_y - 0.19

                    if subtitle:
                        txt(bx + 0.22, title_y, subtitle,
                            size=8.0, weight='bold', color=color,
                            ha='left', va='top', zorder=4)
                    wrapped = textwrap.fill(goal.replace('\n', ' '), width=55)
                    txt(bx + 0.22, goal_y, wrapped,
                        size=7.5, color=C['text2'],
                        ha='left', va='top', zorder=4)

        cur_y -= CH

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
hline(MAR, FW - MAR, 0.39)
txt(FW / 2, 0.23,
    'Every decision made here is designed to de-risk the path forward '
    'and ensure participant time and effort deliver maximum, measurable value.',
    size=8, color=C['text3'], zorder=5)

# ══════════════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════════════
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       '..', '..', '..', 'business-demo', 'boomi')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'icf-workshop-alignment-agenda.png')

plt.savefig(out_path, dpi=DPI, facecolor=C['bg'])
print(f'Saved -> {out_path}')
plt.close()
