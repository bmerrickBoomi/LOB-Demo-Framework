#!/usr/bin/env python3
# /// script
# dependencies = ["matplotlib"]
# ///
"""
Generates: business-demo/boomi/boomi-platform-overview.png
Clean, modern Boomi Platform Overview — no heavy panel boxes.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D
import numpy as np

# ── Boomi Brand Colors (sourced from official SVGs + boomi.com CSS) ───────────
# Confirmed from brand.svg + boomi-1.svg:
#   #072B55  dark navy wordmark
#   #003D58  navy logo background
#   #FF7C66  coral accent
# Confirmed from boomi.com website CSS:
#   #0693E3  vivid blue (links, CTAs, interactive)
C = {
    'bg':         '#ffffff',
    'navy':       '#003D58',   # confirmed — logo bg
    'dark':       '#072B55',   # confirmed — wordmark
    'blue':       '#0693E3',   # confirmed — website interactive blue
    'coral':      '#FF7C66',   # confirmed — brand accent
    'mid':        '#00527A',   # derived mid between navy + blue
    'teal':       '#0099BB',   # derived teal (navy → blue midpoint, cooler)
    'text':       '#072B55',
    'text2':      '#2E4A63',
    'text3':      '#6B8299',
    'divider':    '#DCE8EF',
    'border':     '#8BBCCE',   # mid-tone for card/chip outlines
    'card_bg':    '#F4F8FB',
    'chip_bg':    '#E8F3F8',
    # Pillar accent palette — all Boomi-derived
    'p1':         '#0693E3',   # blue  — Integration
    'p2':         '#003D58',   # navy  — API Management
    'p3':         '#FF7C66',   # coral — Data Hub
    'p4':         '#072B55',   # dark  — AI Agent Studio
    # flow node colors — derived from brand palette
    'flow_start': '#0693E3',
    'flow_map':   '#00527A',
    'flow_dec':   '#FF7C66',
    'flow_stop':  '#072B55',
}

DPI = 200
FW, FH = 10.5 * 16 / 9, 10.5   # exact 16:9 for Google Slides widescreen

fig, ax = plt.subplots(figsize=(FW, FH))
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.axis('off')
fig.patch.set_facecolor(C['bg'])
ax.set_facecolor(C['bg'])


# ── Helpers ───────────────────────────────────────────────────────────────────

def box(x, y, w, h, fc, ec=None, lw=1.0, r=0.18, zorder=2, alpha=1.0):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f'round,pad=0,rounding_size={r}',
        facecolor=fc, edgecolor=ec if ec else fc,
        linewidth=lw, zorder=zorder, alpha=alpha,
    )
    ax.add_patch(p)


def txt(x, y, s, size=10, color=C['text'], weight='normal',
        ha='center', va='center', zorder=6, style='normal'):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=zorder, multialignment='center',
            fontstyle=style, fontfamily=['Poppins', 'DejaVu Sans'])


def hline(x1, x2, y, color=C['divider'], lw=0.8, zorder=3, ls='-'):
    ax.add_line(Line2D([x1, x2], [y, y], color=color, lw=lw,
                       linestyle=ls, zorder=zorder))


def vline(x, y1, y2, color=C['divider'], lw=0.8, zorder=3):
    ax.add_line(Line2D([x, x], [y1, y2], color=color, lw=lw, zorder=zorder))


def arr(x1, y1, x2, y2, color=C['blue'], lw=1.5, zorder=4, rad=0):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->', color=color, lw=lw,
                    mutation_scale=10,
                    connectionstyle=f'arc3,rad={rad}',
                ), zorder=zorder)


def section_label(x, y, text, color=C['navy']):
    """Section header with left coral accent bar."""
    ax.add_patch(FancyBboxPatch((x, y - 0.13), 0.05, 0.36,
                                boxstyle='round,pad=0,rounding_size=0.02',
                                facecolor=C['coral'], edgecolor='none', zorder=5))
    txt(x + 0.18, y + 0.05, text, size=12, weight='bold',
        color=color, ha='left', zorder=6)


def chip(cx, cy, w, h, dot_color, abbrev, line1, line2, zorder=3):
    """Modern pill-shaped connector chip."""
    box(cx - w/2, cy - h/2, w, h, C['chip_bg'], C['border'],
        lw=1.5, r=h/2, zorder=zorder)
    # colored dot
    dot_r = h * 0.32
    ax.add_patch(Circle((cx - w/2 + dot_r + 0.12, cy), dot_r,
                        facecolor=dot_color, edgecolor='none', zorder=zorder+1))
    txt(cx - w/2 + dot_r + 0.12, cy, abbrev, size=8.5,
        color='white', weight='bold', zorder=zorder+2)
    txt(cx, cy + h*0.18, line1, size=9.5, weight='bold',
        color=C['text'], ha='center', zorder=zorder+1)
    txt(cx, cy - h*0.14, line2, size=9.5, color=C['text2'],
        ha='center', zorder=zorder+1)


def flow_node(cx, cy, shape, color, label, sz=0.22, zorder=5):
    if shape == 'circle':
        ax.add_patch(Circle((cx, cy), sz, facecolor=color,
                            edgecolor='white', linewidth=1.5, zorder=zorder))
    elif shape == 'rect':
        box(cx - sz*0.9, cy - sz*0.7, sz*1.8, sz*1.4,
            color, 'white', lw=1.5, r=0.06, zorder=zorder)
        for dy in [-0.05, 0.0, 0.05]:
            ax.add_line(Line2D([cx - sz*0.5, cx + sz*0.5],
                               [cy+dy, cy+dy],
                               color='white', lw=0.8, zorder=zorder+1))
    elif shape == 'diamond':
        pts = [[cx, cy+sz*1.1], [cx+sz*1.0, cy],
               [cx, cy-sz*1.1], [cx-sz*1.0, cy]]
        ax.add_patch(plt.Polygon(pts, closed=True, facecolor=color,
                                 edgecolor='white', linewidth=1.5, zorder=zorder))
    txt(cx, cy - sz*1.4 - 0.05, label, size=7.5,
        color=C['text2'], zorder=zorder+1)


def pillar_card(cx, cy, w, h, accent, icon_fn, title, desc, metrics=None, zorder=2):
    """Modern flat pillar card — white bg, colored top accent strip, no outer border."""
    strip_h = 0.06
    # subtle card shadow (offset gray layer)
    box(cx - w/2 + 0.03, cy - 0.03, w, h, '#E8EEF2', None,
        r=0.18, zorder=zorder)
    # card body
    box(cx - w/2, cy, w, h, C['bg'], C['border'], lw=1.5, r=0.18, zorder=zorder+1)
    # top accent strip
    box(cx - w/2, cy + h - strip_h, w, strip_h + 0.01,
        accent, None, r=0.18, zorder=zorder+2)
    # icon circle
    icon_cy = cy + h - 0.72
    ax.add_patch(Circle((cx, icon_cy), 0.30,
                        facecolor=accent, edgecolor='none',
                        alpha=0.15, zorder=zorder+2))
    if callable(icon_fn):
        icon_fn(cx, icon_cy, accent, zorder=zorder+3)
    else:
        r = 0.27
        img = plt.imread(icon_fn)
        ax.imshow(img, extent=[cx - r, cx + r, icon_cy - r, icon_cy + r],
                  zorder=zorder+3, aspect='auto')
    # title
    txt(cx, cy + h - 1.38, title, size=10, weight='bold',
        color=C['dark'], zorder=zorder+3)
    # desc — just below title
    desc_cy = cy + h - 2.10
    txt(cx, desc_cy, desc, size=8.5, color=C['text2'], zorder=zorder+3)
    # metrics — fills whitespace below desc
    if metrics:
        sep_y = cy + h - 2.72
        hline(cx - w/2 + 0.25, cx + w/2 - 0.25, sep_y,
              color=C['divider'], lw=1.5, zorder=zorder+3)
        n_m   = len(metrics)
        avail = sep_y - 0.20 - cy          # space from sep to near card bottom
        step  = avail / n_m
        for mi, (stat, label) in enumerate(metrics):
            my = sep_y - step * (mi + 0.5)
            txt(cx, my + 0.10, stat,  size=12, weight='bold',
                color=accent, zorder=zorder+4)
            txt(cx, my - 0.14, label, size=8.5, color=C['text2'],
                zorder=zorder+4)


# ── Icons ─────────────────────────────────────────────────────────────────────

def icon_integration(cx, cy, color, zorder=5, s=1.0, **kw):
    sc = s  # scale factor
    for dx in [-0.13*sc, 0.13*sc]:
        ax.add_patch(Circle((cx+dx, cy), 0.09*sc, facecolor=color,
                            edgecolor='none', zorder=zorder))
    ax.add_line(Line2D([cx-0.13*sc, cx+0.13*sc], [cy, cy],
                       color=color, lw=2.5*sc, zorder=zorder))
    for dx in [-0.13*sc, 0.13*sc]:
        ax.add_line(Line2D([cx+dx, cx+dx], [cy, cy+0.18*sc],
                           color=color, lw=2.0*sc, zorder=zorder))
        ax.add_line(Line2D([cx+dx, cx+dx], [cy, cy-0.18*sc],
                           color=color, lw=2.0*sc, zorder=zorder))


def icon_api(cx, cy, color, zorder=5, s=1.0, **kw):
    sc = s
    box(cx - 0.22*sc, cy - 0.17*sc, 0.44*sc, 0.28*sc, color, None,
        r=0.06*sc, zorder=zorder)
    ax.add_patch(mpatches.Arc((cx, cy+0.11*sc), 0.26*sc, 0.26*sc,
                              angle=0, theta1=0, theta2=180,
                              color=color, lw=2.5, zorder=zorder+1))
    txt(cx, cy - 0.03*sc, 'API', size=max(5, int(8*sc)), color='white',
        weight='bold', zorder=zorder+2)


def icon_datahub(cx, cy, color, zorder=5, s=1.0, **kw):
    sc = s
    for i, yy in enumerate([cy-0.16*sc, cy-0.02*sc, cy+0.12*sc]):
        box(cx - 0.20*sc, yy, 0.40*sc, 0.11*sc, color, None,
            r=0.04*sc, zorder=zorder, alpha=1.0 - i*0.15)
        ax.add_patch(mpatches.Ellipse((cx, yy+0.11*sc), 0.40*sc, 0.07*sc,
                                      facecolor=color, edgecolor='none',
                                      alpha=1.0 - i*0.15, zorder=zorder+0.5))


def icon_agent(cx, cy, color, zorder=5, s=1.0, **kw):
    ax.add_patch(Circle((cx, cy+0.17), 0.10, facecolor=color,
                        edgecolor='none', zorder=zorder))
    box(cx - 0.12, cy - 0.08, 0.24, 0.20, color, None, r=0.06, zorder=zorder)
    for dx in [-0.12, 0.12]:
        ax.add_line(Line2D([cx+dx, cx+dx*1.8], [cy+0.04, cy-0.08],
                           color=color, lw=2.5,
                           solid_capstyle='round', zorder=zorder))
    for dx in [-0.06, 0.06]:
        ax.add_line(Line2D([cx+dx, cx+dx], [cy-0.08, cy-0.26],
                           color=color, lw=2.5,
                           solid_capstyle='round', zorder=zorder))


def icon_b2b(cx, cy, color, zorder=5, s=1.0, **kw):
    """Two document shapes with a bidirectional arrow — B2B/EDI exchange."""
    for dx, anchor in [(-0.20, 'left'), (0.20, 'right')]:
        dw, dh = 0.18, 0.26
        dl = cx + dx - dw/2
        db = cy - dh/2
        box(dl, db, dw, dh, color, None, r=0.03, zorder=zorder, alpha=0.9)
        # doc fold corner
        fold = 0.06
        ax.add_patch(plt.Polygon(
            [[dl+dw-fold, db+dh], [dl+dw, db+dh-fold], [dl+dw-fold, db+dh-fold]],
            closed=True, facecolor='white', edgecolor='none',
            alpha=0.5, zorder=zorder+1))
        # horizontal lines inside doc
        for dy_off in [0.06, 0.00, -0.06]:
            lx0 = dl + 0.03
            lx1 = dl + dw - 0.06 if dy_off > -0.05 else dl + dw*0.6
            ax.add_line(Line2D([lx0, lx1], [cy+dy_off, cy+dy_off],
                               color='white', lw=0.8, alpha=0.7, zorder=zorder+1))
    # bidirectional arrow between docs
    ax.annotate('', xy=(cx+0.08, cy), xytext=(cx-0.08, cy),
                arrowprops=dict(arrowstyle='<->', color='white',
                                lw=1.4, mutation_scale=8), zorder=zorder+2)


# ══════════════════════════════════════════════════════════════════════════════
# TITLE BAR
# ══════════════════════════════════════════════════════════════════════════════
# Dark title bar background
box(0, FH - 1.30, FW, 1.30, C['dark'], None, r=0, zorder=4)

txt(FW/2, FH - 0.55,
    'Boomi: The Intelligent Integration & Automation Platform',
    size=19, weight='bold', color='white')
txt(FW/2, FH - 1.02,
    'Connecting clinical, operational & financial systems',
    size=13, color='#B8CCE0', style='italic')

hline(0, FW, FH - 1.30, color=C['mid'], lw=2.5)


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT ANCHORS
# ══════════════════════════════════════════════════════════════════════════════
TOP    = FH - 1.55
BOT    = 0.45
MID_X  = FW * 0.465   # vertical divider x

# ── Vertical divider ──────────────────────────────────────────────────────────
vline(MID_X, BOT, TOP, color=C['mid'], lw=2.5)


# ══════════════════════════════════════════════════════════════════════════════
# LEFT — Core Architecture  (4 layers: Systems → Components → Process → Runtime)
# ══════════════════════════════════════════════════════════════════════════════
LX    = 0.5
LW    = MID_X - LX - 0.3   # usable left width
LCX   = LX + LW / 2        # left section centre x

section_label(LX, TOP - 0.35, 'Core Architecture')

# ── Layer boundaries ─────────────────────────────────────────────────────────
L1_Y  = TOP - 0.65          # Source/Target Systems  (top)
L2_Y  = TOP - 3.00          # Integration Components
L3_Y  = TOP - 5.10          # Process Flow
L4_Y  = BOT + 0.18          # Runtime               (bottom)

ARR_COLOR = C['blue']

# helper: small layer label on far left
def layer_label(y, text):
    txt(LX + 0.01, y, text, size=9, color=C['text2'],
        weight='bold', ha='left', va='top', zorder=5)

# ═══════════════════════════════════════════════════════════════════════════
# LAYER 1 — Source & Target Systems
# ═══════════════════════════════════════════════════════════════════════════
layer_label(L1_Y, 'SOURCE & TARGET SYSTEMS')

# 4 system chips in a 2×2 grid
SYS_W, SYS_H = (LW - 0.55) / 2, 0.58
SYS_GAP = 0.18
cols = [LX + 0.28, LX + 0.28 + SYS_W + SYS_GAP]
rows = [L1_Y - 0.82, L1_Y - 1.52]

sys_items = [
    ('#C6151B', 'Epic', 'Epic EHR',          'Clinical · ADT · Orders · Results'),
    ('#005A9C', 'WD',   'Workday',           'HR · Finance · Payroll'),
    ('#00A1E0', 'SF',   'Salesforce',        'CRM · Patient Engagement'),
    (C['mid'],  'HL7',  'HL7 · FHIR · X12', 'Clinical Data · Claims · EDI'),
]
for idx, (dc, abbr, name, sub) in enumerate(sys_items):
    cx = cols[idx % 2] + SYS_W / 2
    cy = rows[idx // 2] + SYS_H / 2
    chip(cx, cy, SYS_W, SYS_H, dc, abbr, name, sub)


# ═══════════════════════════════════════════════════════════════════════════
# LAYER 2 — Integration Components  (Maps · Profiles · XRef · Doc Cache + AI)
# ═══════════════════════════════════════════════════════════════════════════
layer_label(L2_Y + 0.18, 'PLATFORM COMPONENTS')

# 4 mini platform component cards — mirrors the top 4 from NYU Langone RFP
COMP_W, COMP_H = (LW - 0.55) / 4, 0.74
COMP_GAP = (LW - 0.55 - 4 * COMP_W) / 3
comp_start = LX + 0.28

components = [
    (C['blue'],  '⇄',  'Connectors',       'HL7 · FHIR · Epic'),
    ('#FF5A00',  '⚡',  'Event Broker',     'Pub-Sub · FIFO · Real-time'),
    (C['mid'],   '≋',  'Maps & Transforms','HL7 Parse · Enrich · Route'),
    (C['navy'],  '⬡',  'API Gateway',      'Secure · Throttle · Policies'),
]
for i, (cc, sym, name, sub) in enumerate(components):
    cx = comp_start + i * (COMP_W + COMP_GAP) + COMP_W / 2
    cy = L2_Y - 0.38

    # shadow
    box(cx - COMP_W/2 + 0.02, cy - COMP_H/2 - 0.02, COMP_W, COMP_H,
        '#DDE6EC', None, r=0.12, zorder=2)
    # card bg
    box(cx - COMP_W/2, cy - COMP_H/2, COMP_W, COMP_H,
        C['bg'], C['border'], lw=1.5, r=0.12, zorder=3)
    # top accent strip
    box(cx - COMP_W/2, cy + COMP_H/2 - 0.05, COMP_W, 0.05,
        cc, None, r=0.12, zorder=4)
    txt(cx, cy + 0.16, sym, size=14, color=cc, zorder=5)
    txt(cx, cy - 0.04, name, size=8, weight='bold', color=C['dark'], zorder=5)
    txt(cx, cy - 0.22, sub, size=8.5, color=C['text2'], zorder=5)

# Boomi AI pill — sits right of components row
AI_W, AI_H = 2.50, 0.44
AI_CX = LX + LW - AI_W / 2 - 0.05
AI_CY = L2_Y - 1.05

box(AI_CX - AI_W/2, AI_CY - AI_H/2, AI_W, AI_H,
    C['dark'], None, r=AI_H/2, zorder=4)
ax.add_patch(Circle((AI_CX - AI_W/2 + 0.28, AI_CY), 0.12,
                    facecolor=C['coral'], edgecolor='none', zorder=5))
txt(AI_CX - AI_W/2 + 0.28, AI_CY, '✦', size=8, color='white', zorder=6)
txt(AI_CX + 0.06, AI_CY, 'Boomi AI', size=10, weight='bold',
    color='white', zorder=6)

# AI sub-features as small tags below
AI_FEATURES = ['Suggest · Smart Mapping', 'DesignGen · Documentation Generation', 'Pathfinder · Next Steps']
for fi, feat in enumerate(AI_FEATURES):
    fy = AI_CY - 0.52 - fi * 0.30
    box(AI_CX - AI_W/2 + 0.04, fy - 0.10, AI_W - 0.08, 0.22,
        '#EAF1F6', C['divider'], lw=0.6, r=0.06, zorder=4)
    txt(AI_CX, fy, feat, size=7.5, color=C['dark'], zorder=5)

# down arrow  (from component area centre to process)
arr(LCX - 0.8, L2_Y - 1.28, LCX - 0.8, L3_Y + 0.22,
    color=ARR_COLOR, lw=1.4)

# ═══════════════════════════════════════════════════════════════════════════
# LAYER 3 — Boomi Process Flow
# ═══════════════════════════════════════════════════════════════════════════
layer_label(L3_Y, 'PROCESS FLOW')

FLOW_Y  = L3_Y - 0.55
FLOW_CX = LCX - 0.8

nodes = [
    ('circle',  C['flow_start'], 'Start'),
    ('rect',    C['flow_map'],   'Map'),
    ('diamond', C['flow_dec'],   'Decision'),
    ('circle',  C['flow_stop'],  'Stop'),
]
spacing  = (LW * 0.72) / (len(nodes) - 1)
start_nx = FLOW_CX - spacing * (len(nodes) - 1) / 2

for i, (shape, color, label) in enumerate(nodes):
    nx = start_nx + i * spacing
    flow_node(nx, FLOW_Y, shape, color, label)
    if i < len(nodes) - 1:
        nx2 = start_nx + (i+1) * spacing
        ax.add_line(Line2D([nx + 0.26, nx2 - 0.26], [FLOW_Y, FLOW_Y],
                           color=C['border'], lw=1.5, zorder=4))
        ax.annotate('', xy=(nx2 - 0.26, FLOW_Y),
                    xytext=(nx2 - 0.27, FLOW_Y),
                    arrowprops=dict(arrowstyle='->', color=C['border'],
                                   lw=1.0, mutation_scale=8), zorder=4)

txt(FLOW_CX, FLOW_Y - 0.58, 'Low-code visual builder · Real-time · Batch · Event-driven · API',
    size=9, color=C['text2'], style='italic')

# down arrow
arr(FLOW_CX, FLOW_Y - 0.90, FLOW_CX, L4_Y + 1.17,
    color=ARR_COLOR, lw=1.4)

# ═══════════════════════════════════════════════════════════════════════════
# LAYER 4 — Execution Runtime  (Atom · Molecule · Atom Cloud)
# ═══════════════════════════════════════════════════════════════════════════
layer_label(L4_Y + 1.08, 'EXECUTION RUNTIME')

RT_ITEMS = [
    ('⬡', 'Atom',       'Single-node · Lightweight\nOn-Prem or Cloud'),
    ('⬡', 'Molecule',   'Multi-node Cluster\nLoad Balanced · HA'),
    ('☁', 'Atom Cloud', 'Boomi-Managed\nPublic · Dedicated'),
]
RT_W  = (LW - 0.55) / 3
RT_H  = 0.78
RT_GAP = (LW - 0.55 - 3 * RT_W) / 2
RT_Y  = L4_Y + 0.06

for i, (sym, name, desc) in enumerate(RT_ITEMS):
    rx = LX + 0.28 + i * (RT_W + RT_GAP)
    # shadow
    box(rx + 0.03, RT_Y - 0.03, RT_W, RT_H, '#DDE6EC', None,
        r=0.12, zorder=2)
    # card
    box(rx, RT_Y, RT_W, RT_H, C['bg'], C['border'],
        lw=1.5, r=0.12, zorder=3)
    # left accent bar
    box(rx, RT_Y, 0.05, RT_H, C['navy'], None, r=0.06, zorder=4)
    txt(rx + RT_W/2 + 0.04, RT_Y + RT_H*0.68, sym + '  ' + name,
        size=9.5, weight='bold', color=C['dark'], zorder=5)
    txt(rx + RT_W/2 + 0.04, RT_Y + RT_H*0.36, desc,
        size=8.5, color=C['text2'], zorder=5)

# bottom caption
txt(LCX, BOT - 0.02,
    'On-prem · Cloud · Hybrid · HIPAA-compliant · 1,000+ pre-built connectors',
    size=9.5, color=C['text2'], style='italic')


# ══════════════════════════════════════════════════════════════════════════════
# RIGHT — Platform Pillars
# ══════════════════════════════════════════════════════════════════════════════
RX     = MID_X + 0.35
RW     = FW - RX - 0.45
section_label(RX, TOP - 0.35, 'Platform Pillars')

_ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '..', '..', '..', 'icons', 'Icons - Boomi Services')

pillars = [
    {
        'accent':  C['p1'],
        'icon':    os.path.join(_ICON_DIR, 'Icon_Integration-Automation.png'),
        'title':   'Integration &\nAutomation',
        'desc':    'Unify clinical, HR &\noperational systems\nReal-time · Batch · Event\nHL7 · X12 · FHIR · EDI',
        'metrics': [
            ('1,000+',  'Pre-built connectors'),
            ('~60%',    'Faster integration delivery'),
            ('800+',    'Global implementation partners'),
            ('99.9%',   'Uptime SLA for mission-critical\nintegrations'),
        ],
    },
    {
        'accent':  C['p2'],
        'icon':    os.path.join(_ICON_DIR, 'Icon_APIM-Gateway.png'),
        'title':   'API\nManagement',
        'desc':    'FHIR API lifecycle\nSecure · Govern · Scale\nInteroperability at speed',
        'metrics': [
            ('AES-256',  'Encryption at rest'),
            ('TLS 1.2+', 'Encryption in transit'),
            ('6+',       'Protocols: REST · SOAP · GraphQL\nFHIR · HL7 · X12'),
            ('HIPAA',    'Compliant by design'),
        ],
    },
    {
        'accent':  C['p3'],
        'icon':    os.path.join(_ICON_DIR, 'Icon_Data-Management-Hub.png'),
        'title':   'Data\nManagement',
        'desc':    'ELT pipelines · Schema drift\ndetection & remediation\nMaster data · DQ & Governance\nData catalog & lineage',
        'metrics': [
            ('360°',      'Patient & employee golden record'),
            ('~40%',      'Reduction in duplicate records'),
            ('Real-time', 'Data quality enforcement'),
            ('3x',        'Faster regulatory & audit reporting'),
        ],
    },
    {
        'accent':  C['teal'],
        'icon':    os.path.join(_ICON_DIR, 'Icon_Agentstudio Agent Garden.png'),
        'title':   'AI Agent\nManagement',
        'desc':    'Intelligent automation\nAgent orchestration\nBoomi AI · Low-code design',
        'metrics': [
            ('Low-code',   'Business & IT accessible'),
            ('IoT + AI/ML','Emerging tech ready'),
            ('WCAG 2.0 AA','Accessibility compliant'),
            ('No-code',    'Agent creation without\ndeveloper dependency'),
        ],
    },
]

n      = len(pillars)
pad    = 0.28
cw     = (RW - pad * (n + 1)) / n
ch     = TOP - BOT - 1.30
cy0    = BOT + 0.55

for i, p in enumerate(pillars):
    pcx = RX + pad + i * (cw + pad) + cw/2
    pillar_card(pcx, cy0, cw, ch,
                p['accent'], p['icon'], p['title'], p['desc'],
                metrics=p.get('metrics'))

txt(RX + RW/2, BOT - 0.02,
    'HIPAA · HL7 · FHIR · Interoperability',
    size=9.5, color=C['text2'], style='italic')

# ══════════════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════════════
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       '..', '..', '..', 'business-demo', 'boomi')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'boomi-platform-overview.png')

plt.tight_layout(pad=0)
plt.savefig(out_path, dpi=DPI, facecolor=C['bg'])
print(f'Saved -> {out_path}')
plt.close()
