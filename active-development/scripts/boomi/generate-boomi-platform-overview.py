#!/usr/bin/env python3
# /// script
# dependencies = ["matplotlib"]
# ///
"""
Generates: business-demo/boomi/boomi-platform-overview.png

Recreates the "Boomi: The Intelligent Integration & Automation Platform"
architecture overview diagram.

Usage (requires matplotlib):
    python3.11 active-development/scripts/boomi/generate-boomi-platform-overview.py
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, FancyArrowPatch
from matplotlib.lines import Line2D
import numpy as np

# ── Palette ───────────────────────────────────────────────────────────────────
C = {
    'bg':          '#ffffff',
    'panel':       '#e8f4fb',
    'boomi':       '#003C57',
    'blue':        '#0072C6',
    'blue_lt':     '#cce4f4',
    'blue_md':     '#5aacdf',
    'blue_dk':     '#004f8b',
    'text':        '#1a1a2e',
    'text2':       '#334155',
    'text3':       '#64748b',
    'border':      '#b0cfe0',
    'green':       '#16a34a',
    'green_lt':    '#dcfce7',
    'orange':      '#d97706',
    'orange_lt':   '#fef3c7',
    'purple':      '#7c3aed',
    'purple_lt':   '#ede9fe',
    'red':         '#dc2626',
    'runtime_bg':  '#fff8e1',
    'runtime_bdr': '#fbbf24',
    'sf_blue':     '#00A1E0',
    'sap_blue':    '#0070c0',
    'proc_bg':     '#f0f7ff',
}

DPI = 150
FW, FH = 16, 10

fig, ax = plt.subplots(figsize=(FW, FH))
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.axis('off')
fig.patch.set_facecolor(C['bg'])


# ── Helpers ───────────────────────────────────────────────────────────────────

def box(x, y, w, h, fc, ec=None, lw=1.0, r=0.2, zorder=2, ls='-', alpha=1.0):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f'round,pad=0,rounding_size={r}',
        facecolor=fc, edgecolor=ec if ec else fc,
        linewidth=lw, linestyle=ls, zorder=zorder, alpha=alpha,
    )
    ax.add_patch(p)


def txt(x, y, s, size=10, color=C['text'], weight='normal',
        ha='center', va='center', zorder=6):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=zorder, multialignment='center')


def hline(x1, x2, y, color=C['border'], lw=0.8, zorder=3):
    ax.add_line(Line2D([x1, x2], [y, y], color=color, lw=lw, zorder=zorder))


def arr(x1, y1, x2, y2, color=C['blue_md'], lw=1.5, zorder=4, style='->'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                mutation_scale=10), zorder=zorder)


def dashed_arr(x1, y1, x2, y2, color=C['blue_md'], lw=1.0, zorder=4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                mutation_scale=8,
                                linestyle='dashed',
                                connectionstyle='arc3,rad=0'), zorder=zorder)


def thought_bubble(cx, cy, w, h, title, sub_lines, border_color,
                   src_x, src_y, zorder=5):
    """Thought bubble: oval body + trail of diminishing circles from source."""
    # Trail dots: small near source, growing toward bubble
    bub_lx = cx - w / 2   # left edge of bubble
    dots = [
        (src_x + (bub_lx - src_x) * 0.22, src_y + (cy - src_y) * 0.22, 0.045),
        (src_x + (bub_lx - src_x) * 0.50, src_y + (cy - src_y) * 0.50, 0.072),
        (src_x + (bub_lx - src_x) * 0.76, src_y + (cy - src_y) * 0.76, 0.100),
    ]
    for dx, dy, r in dots:
        ax.add_patch(Circle((dx, dy), r,
                            facecolor=C['bg'], edgecolor=border_color,
                            linewidth=1.0, zorder=zorder))
    # Main oval bubble body
    bubble = mpatches.Ellipse((cx, cy), w, h,
                               facecolor=C['bg'], edgecolor=border_color,
                               linewidth=1.2, zorder=zorder + 1)
    ax.add_patch(bubble)
    # Text inside bubble
    n = len(sub_lines)
    total_h = (1 + n) * 0.145
    top_y   = cy + total_h / 2 - 0.072
    txt(cx, top_y, title, size=7.0, color=border_color,
        weight='bold', zorder=zorder + 2)
    for i, line in enumerate(sub_lines):
        txt(cx, top_y - (i + 1) * 0.145, line, size=6.0, color=C['text3'],
            zorder=zorder + 2)


def cloud_shape(cx, cy, color, border_color, scale=1.0, zorder=3):
    """Draw a rounded cloud silhouette using overlapping circles."""
    # Draw border circles first (slightly larger, border color)
    blobs = [
        (0.00,  0.00, 0.38),
        (-0.30, -0.05, 0.25),
        ( 0.30, -0.05, 0.25),
        (-0.16,  0.22, 0.20),
        ( 0.16,  0.22, 0.20),
    ]
    for dx, dy, r in blobs:
        c = Circle((cx + dx * scale, cy + dy * scale), (r + 0.03) * scale,
                   facecolor=border_color, edgecolor='none', zorder=zorder - 0.1)
        ax.add_patch(c)
    for dx, dy, r in blobs:
        c = Circle((cx + dx * scale, cy + dy * scale), r * scale,
                   facecolor=color, edgecolor='none', zorder=zorder)
        ax.add_patch(c)


def brain_icon(cx, cy, color, size=0.18, zorder=5):
    """Simple brain-like shape: two overlapping lobes."""
    for dx in [-size * 0.45, size * 0.45]:
        lobe = mpatches.Ellipse((cx + dx, cy), size * 0.9, size * 1.3,
                                facecolor=color, edgecolor='none', zorder=zorder)
        ax.add_patch(lobe)
    # center stem
    stem = mpatches.Ellipse((cx, cy - size * 0.3), size * 0.3, size * 0.6,
                             facecolor=color, edgecolor='none', zorder=zorder)
    ax.add_patch(stem)
    # highlight lines
    for dx, dy in [(-0.42, 0.2), (-0.42, -0.1), (0.42, 0.2), (0.42, -0.1)]:
        ax.add_line(Line2D([cx + dx * size, cx + dx * size * 0.5],
                           [cy + dy * size, cy + dy * size * 1.2],
                           color='white', lw=0.8, zorder=zorder + 1))


def connector_box(bx, by, cw, ch, dot_color, abbrev, line1, line2, zorder=3):
    box(bx, by, cw, ch, C['bg'], C['border'], lw=1.0, r=0.15, zorder=zorder)
    c = Circle((bx + 0.33, by + ch / 2), 0.21, facecolor=dot_color,
               edgecolor='none', zorder=zorder + 1)
    ax.add_patch(c)
    txt(bx + 0.33, by + ch / 2, abbrev, size=8, color='white',
        weight='bold', zorder=zorder + 2)
    txt(bx + cw * 0.66, by + ch * 0.68, line1, size=8,
        weight='bold', color=C['text'], zorder=zorder + 1)
    txt(bx + cw * 0.66, by + ch * 0.28, line2, size=6.5,
        color=C['text3'], zorder=zorder + 1)


# ── Process shapes ────────────────────────────────────────────────────────────
def proc_circle(cx, cy, r, color, label, zorder=5):
    """Rounded shape for Start/Stop."""
    c = Circle((cx, cy), r, facecolor=color, edgecolor='white',
               linewidth=1.5, zorder=zorder)
    ax.add_patch(c)
    txt(cx, cy - r - 0.21, label, size=6.5, color=C['text2'], zorder=zorder + 1)


def proc_rect(cx, cy, w, h, color, label, zorder=5):
    """Rectangle shape for Map."""
    box(cx - w / 2, cy - h / 2, w, h, color, 'white', lw=1.5, r=0.06, zorder=zorder)
    # inner lines to suggest map/doc
    for dy in [-0.06, 0.0, 0.06]:
        ax.add_line(Line2D([cx - w * 0.3, cx + w * 0.3],
                           [cy + dy, cy + dy],
                           color='white', lw=0.8, zorder=zorder + 1))
    txt(cx, cy - h / 2 - 0.21, label, size=6.5, color=C['text2'], zorder=zorder + 1)


def proc_diamond(cx, cy, s, color, label, zorder=5):
    """Diamond shape for Decision."""
    pts = [[cx, cy + s], [cx + s, cy], [cx, cy - s], [cx - s, cy]]
    d = plt.Polygon(pts, closed=True, facecolor=color, edgecolor='white',
                    linewidth=1.5, zorder=zorder)
    ax.add_patch(d)
    txt(cx, cy - s - 0.21, label, size=6.5, color=C['text2'], zorder=zorder + 1)


# ── Pillar icons ──────────────────────────────────────────────────────────────
def icon_integration(cx, cy, color, s=0.30, zorder=5):
    """Two interlocking puzzle pieces."""
    # Left piece
    box(cx - s * 1.05, cy - s * 0.5, s, s, color, None, r=0.06, zorder=zorder)
    # Right piece
    box(cx + s * 0.05, cy - s * 0.5, s, s, color, None, r=0.06, zorder=zorder)
    # Tab connecting them (notch)
    box(cx - s * 0.22, cy - s * 0.08, s * 0.44, s * 0.35,
        C['bg'], None, r=0.04, zorder=zorder + 1)
    # Small overlap highlight
    box(cx - s * 0.12, cy - s * 0.5, s * 0.24, s * 0.24,
        color, None, r=0.03, zorder=zorder + 2)


def icon_api(cx, cy, color, s=0.30, zorder=5):
    """Padlock with 'API' label."""
    # Lock body
    box(cx - s * 0.65, cy - s * 0.7, s * 1.3, s * 0.9,
        color, None, r=0.08, zorder=zorder)
    # Lock shackle (arc using ellipse top-half)
    shackle = mpatches.Arc((cx, cy + s * 0.2), s * 0.8, s * 0.8,
                            angle=0, theta1=0, theta2=180,
                            color='white', lw=2.5, zorder=zorder + 1)
    ax.add_patch(shackle)
    txt(cx, cy - s * 0.28, 'API', size=7, color='white',
        weight='bold', zorder=zorder + 2)


def icon_database(cx, cy, color, s=0.30, zorder=5):
    """Stacked cylinders."""
    cyl_w = s * 1.6
    cyl_h = s * 0.32
    e_h   = s * 0.14
    tops = [cy - s * 0.45, cy - s * 0.10, cy + s * 0.25]
    for yy in tops:
        # body
        box(cx - cyl_w / 2, yy, cyl_w, cyl_h,
            color, None, r=0.03, zorder=zorder)
        # top ellipse cap
        e = Ellipse((cx, yy + cyl_h), cyl_w, e_h,
                    facecolor='#f0b429' if yy == tops[-1] else color,
                    edgecolor='none', zorder=zorder + 0.5)
        ax.add_patch(e)
    # bottom ellipse
    eb = Ellipse((cx, tops[0]), cyl_w, e_h,
                 facecolor=color, edgecolor='none', zorder=zorder)
    ax.add_patch(eb)


def icon_agent(cx, cy, color, s=0.30, zorder=5):
    """Humanoid agent figure."""
    # Head
    head = Circle((cx, cy + s * 0.7), s * 0.3,
                  facecolor=color, edgecolor='none', zorder=zorder)
    ax.add_patch(head)
    # Body
    box(cx - s * 0.38, cy + s * 0.05, s * 0.76, s * 0.55,
        color, None, r=0.08, zorder=zorder)
    # Arms
    ax.add_line(Line2D([cx - s * 0.38, cx - s * 0.65],
                       [cy + s * 0.45, cy + s * 0.15],
                       color=color, lw=4, solid_capstyle='round', zorder=zorder))
    ax.add_line(Line2D([cx + s * 0.38, cx + s * 0.65],
                       [cy + s * 0.45, cy + s * 0.15],
                       color=color, lw=4, solid_capstyle='round', zorder=zorder))
    # Legs
    for dx in [-0.18, 0.18]:
        ax.add_line(Line2D([cx + dx * s, cx + dx * s],
                           [cy + s * 0.05, cy - s * 0.45],
                           color=color, lw=4, solid_capstyle='round', zorder=zorder))
    # Eyes
    for ex in [cx - s * 0.1, cx + s * 0.1]:
        dot = Circle((ex, cy + s * 0.72), s * 0.06,
                     facecolor='white', zorder=zorder + 1)
        ax.add_patch(dot)


# ══════════════════════════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════════════════════════
txt(FW / 2, 9.55,
    'Boomi: The Intelligent Integration & Automation Platform',
    size=18, weight='bold', color=C['boomi'])
txt(FW / 2, 9.10,
    'Connect everything, automate faster, and accelerate business outcomes'
    ' with a unified, AI-driven platform.',
    size=10, color=C['text2'])
hline(0.4, FW - 0.4, 8.78, lw=0.7)

# ══════════════════════════════════════════════════════════════════════════════
# LEFT PANEL
# ══════════════════════════════════════════════════════════════════════════════
LX, LY, LW, LH = 0.4, 0.45, 7.5, 8.15

box(LX, LY, LW, LH, C['panel'], C['border'], lw=1.0, r=0.3, zorder=1)
txt(LX + LW / 2, 8.50, 'Core Architecture: The Building Blocks',
    size=12, weight='bold', color=C['boomi'])

# Connector dimensions
CW, CH = 1.68, 0.90
CX = LX + 0.22

# Salesforce connector
connector_box(CX, 6.50, CW, CH, C['sf_blue'],  'SF',
              'Connectors', '(e.g., Salesforce)')
# SAP connector
connector_box(CX, 5.00, CW, CH, C['sap_blue'], 'S',
              'Connectors', '(e.g., SAP\nDatabase)')

# ── Layout anchors ────────────────────────────────────────────────────────────
PX, PW = CX + CW + 0.45, 3.40   # process box x + width

# Boomi AI badge — high up, clear of everything
BAI_W  = 1.80
BAI_H  = 0.42
BAI_CX = PX + PW / 2
BAI_CY = 7.10

BAI_LEFT  = BAI_CX - BAI_W / 2
BAI_RIGHT = BAI_CX + BAI_W / 2

box(BAI_LEFT, BAI_CY - BAI_H / 2, BAI_W, BAI_H, C['blue_dk'], None,
    r=0.13, zorder=4)
cloud_shape(BAI_LEFT + 0.28, BAI_CY, color='#6ab0d4',
            border_color=C['blue_dk'], scale=0.22, zorder=4)
brain_icon(BAI_LEFT + 0.28, BAI_CY, color=C['blue_dk'], size=0.10, zorder=5)
txt(BAI_CX + 0.14, BAI_CY,
    'Boomi AI', size=9, weight='bold', color='white', zorder=6)

# ── Callouts — both above badge centre so they don't crowd the process box ────
CO_X  = BAI_RIGHT + 0.16
CO_W  = 1.82
CO_CX = CO_X + CO_W / 2

# DesignGen — higher thought bubble
DG_CY = BAI_CY + 0.72
thought_bubble(CO_CX, DG_CY, CO_W, 0.68,
               'Boomi DesignGen:',
               ['Autonomous design from', 'natural language'],
               C['blue'],
               src_x=BAI_RIGHT, src_y=BAI_CY, zorder=5)

# Pathfinder — lower thought bubble (still above badge centre)
PF_CY = BAI_CY + 0.18
thought_bubble(CO_CX, PF_CY, CO_W, 0.52,
               'Boomi Pathfinder:',
               ['Suggests next best steps'],
               C['blue_md'],
               src_x=BAI_RIGHT, src_y=BAI_CY, zorder=5)

# Arrow: Boomi AI badge → Process box top
# Process box top = BAI_CY - BAI_H/2 - 0.38 gap
PROC_TOP = BAI_CY - BAI_H / 2 - 0.38
PH = 1.90
PY = PROC_TOP - PH

arr(BAI_CX, BAI_CY - BAI_H / 2,
    BAI_CX, PROC_TOP + 0.04,
    color=C['blue_md'], lw=1.3, zorder=4)

# ── Process box ───────────────────────────────────────────────────────────────
box(PX, PY, PW, PH, C['proc_bg'], C['blue_dk'], lw=1.5, r=0.2, zorder=3)
txt(PX + PW / 2, PY + PH - 0.22, 'The Process',
    size=9, weight='bold', color=C['boomi'], zorder=4)

# ── Process flow shapes ───────────────────────────────────────────────────────
SZ   = 0.22
SY   = PY + 0.95
n_sh = 4
step = PW / (n_sh + 0.3)

shape_data = [
    ('start',    'Start\nShape',    C['green']),
    ('map',      'Map\nShape',      C['blue']),
    ('decision', 'Decision\nShape', C['orange']),
    ('stop',     'Stop\nShape',     C['red']),
]

for i, (stype, label, color) in enumerate(shape_data):
    sx = PX + 0.50 + i * step
    if stype == 'start':
        proc_circle(sx, SY, SZ, color, label)
    elif stype == 'map':
        proc_rect(sx, SY, SZ * 1.8, SZ * 1.6, color, label)
    elif stype == 'decision':
        proc_diamond(sx, SY, SZ * 1.1, color, label)
    elif stype == 'stop':
        proc_circle(sx, SY, SZ, color, label)
    # connector dot + line to next shape
    if i < n_sh - 1:
        nx = PX + 0.50 + (i + 1) * step
        gap_start = sx + SZ * 1.15
        gap_end   = nx - SZ * 1.35
        ax.add_line(Line2D([gap_start, gap_end], [SY, SY],
                           color=C['border'], lw=1.2, zorder=4))
        # arrowhead at end
        arr(gap_end - 0.01, SY, gap_end, SY,
            color=C['border'], lw=1.0, zorder=4)

# ── Arrows: connectors → process box ─────────────────────────────────────────
arr(CX + CW, 6.95, PX, min(PY + PH - 0.25, PROC_TOP - 0.15), color=C['blue_md'], lw=1.4)
arr(CX + CW, 5.45, PX, PY + PH * 0.42,                        color=C['blue_md'], lw=1.4)

# ── The Boomi Runtime ─────────────────────────────────────────────────────────
RTX, RTY = LX + 0.45, LY + 0.82
RTW, RTH = LW - 0.9, 1.05

# Arrow from process box down to runtime
arr(PX + PW / 2, PY, PX + PW / 2, RTY + RTH + 0.06,
    color=C['blue_md'], lw=1.4)

box(RTX, RTY, RTW, RTH, C['runtime_bg'], C['runtime_bdr'], lw=1.5, r=0.2, zorder=3)

# Gear (using unicode gear — reliable in DejaVu Sans)
gear = Circle((RTX + 0.48, RTY + RTH / 2), 0.29,
              facecolor=C['orange'], edgecolor='none', zorder=4)
ax.add_patch(gear)
txt(RTX + 0.48, RTY + RTH / 2, '\u2699', size=15, color='white', zorder=5)

txt(RTX + RTW / 2 + 0.18, RTY + RTH / 2 + 0.20,
    'The Boomi Runtime', size=10, weight='bold', color=C['boomi'], zorder=4)
txt(RTX + RTW / 2 + 0.18, RTY + RTH / 2 - 0.18,
    'Lightweight engine executing processes', size=8.5, color=C['text2'], zorder=4)

# Left caption
txt(LX + LW / 2, LY + 0.35,
    'Visual workflows, pre-built connectors, and embedded AI running on a patented engine.',
    size=8, color=C['text3'])

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL
# ══════════════════════════════════════════════════════════════════════════════
RX = LX + LW + 0.4
RW = FW - RX - 0.35
RY, RH = 0.45, 8.15

box(RX, RY, RW, RH, C['panel'], C['border'], lw=1.0, r=0.3, zorder=1)
txt(RX + RW / 2, 8.50,
    'Platform Pillars: Unified Capabilities for Success',
    size=12, weight='bold', color=C['boomi'])

pillars = [
    {
        'fn':    icon_integration,
        'color': C['blue'],
        'bg':    C['blue_lt'],
        'title': 'Integration &\nAutomation',
        'desc':  'Unify apps, APIs,\ndata, & AI. Accelerate\nwith low-code &\npre-built tools.',
    },
    {
        'fn':    icon_api,
        'color': C['green'],
        'bg':    C['green_lt'],
        'title': 'API\nManagement',
        'desc':  'Secure, govern,\nand scale APIs.\nStrategic exposure\nfor innovation.',
    },
    {
        'fn':    icon_database,
        'color': C['orange'],
        'bg':    C['orange_lt'],
        'title': 'Data Management\n(Data Hub)',
        'desc':  'Synchronized,\nhigh-quality, trusted\ndata for analytics\n& AI context.',
    },
    {
        'fn':    icon_agent,
        'color': C['purple'],
        'bg':    C['purple_lt'],
        'title': 'AI Agent\nManagement\n(Agentstudio)',
        'desc':  'Design, govern,\nand orchestrate\nAI agents\nresponsibly at scale.',
    },
]

n     = len(pillars)
pad   = 0.25
cw    = (RW - pad * (n + 1)) / n
ch    = 5.5
cy0   = 2.20
ih    = 1.65   # icon area height

for i, p in enumerate(pillars):
    cx = RX + pad + i * (cw + pad)
    cy = cy0

    # Card
    box(cx, cy, cw, ch, C['bg'], C['border'], lw=1.0, r=0.2, zorder=2)

    # Icon region
    box(cx, cy + ch - ih, cw, ih, p['bg'], None, r=0.2, zorder=3)

    # Icon
    icx = cx + cw / 2
    icy = cy + ch - ih / 2
    p['fn'](icx, icy, p['color'], s=0.30, zorder=4)

    # Title
    txt(cx + cw / 2, cy + ch - ih - 0.70,
        p['title'], size=8.5, weight='bold', color=C['boomi'], zorder=4)

    # Description
    txt(cx + cw / 2, cy + 1.05,
        p['desc'], size=7.5, color=C['text2'], zorder=4)

# Right caption
txt(RX + RW / 2, RY + 0.35,
    'One unified platform to connect, manage, and govern your entire digital landscape.',
    size=8, color=C['text3'])

# ══════════════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════════════
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       '..', '..', '..', 'business-demo', 'boomi')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'boomi-platform-overview.png')

plt.savefig(out_path, dpi=DPI, bbox_inches='tight', facecolor=C['bg'])
print(f'Saved -> {out_path}')
plt.close()
