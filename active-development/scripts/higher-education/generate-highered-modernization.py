#!/usr/bin/env python3.11
"""
Higher Education — Cloud Modernization  |  IT Visual Walkthrough
Swim-lane flow: IT Admin → Migration Console → Boomi Platform → Legacy + Cloud Systems
Modeled after hr-ops-it-visual.png style.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import subprocess

# ─── Color palette ────────────────────────────────────────────────────────────
BG          = '#f8fafc'
CARD        = '#ffffff'
CARD2       = '#f1f5f9'
BORDER      = '#cbd5e1'
TEXT        = '#1e293b'
TEXT2       = '#475569'
BLUE        = '#2563eb'     # user layer
PURPLE      = '#003C57'     # Boomi platform (official Boomi teal)
PURPLE_DARK = '#005580'
GREEN       = '#16a34a'     # cloud targets
GREEN_DARK  = '#15803d'
ORANGE      = '#d97706'     # legacy systems
TEAL        = '#0d9488'

fig, ax = plt.subplots(figsize=(22, 14))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 22)
ax.set_ylim(-0.45, 14)
ax.axis('off')
ax.set_aspect('equal')

# ─── Helpers ─────────────────────────────────────────────────────────────────
def fancy_rect(x, y, w, h, fc, ec, lw=1.5, pad=0.12, zorder=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={pad}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder))

def circle(cx, cy, r, fc, ec='white', lw=1, zorder=5):
    ax.add_patch(Circle((cx, cy), r, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder))

def step_badge(cx, cy, label, color, size=10, zorder=10):
    circle(cx, cy, 0.28, color, 'white', 1.5, zorder=zorder)
    ax.text(cx, cy, str(label), color='white', fontsize=size,
        fontweight='bold', ha='center', va='center', zorder=zorder+1)

def arrow(x1, y1, x2, y2, color, lw=2.5, style='->', ls='solid', zorder=4, cs='arc3,rad=0'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle=style, color=color, lw=lw,
            linestyle=ls, connectionstyle=cs), zorder=zorder)

# ═══════════════════════════════════════════════════════════════════════════════
# SWIM LANE DIVIDERS
# ═══════════════════════════════════════════════════════════════════════════════
ax.axhline(8.3, xmin=0.018, xmax=0.99, color=BORDER, lw=1, ls='--', zorder=1)
ax.axhline(4.0, xmin=0.018, xmax=0.99, color=BORDER, lw=1, ls='--', zorder=1)

ax.text(0.2, 10.8, 'USER\nLAYER',       color=BLUE,   fontsize=8, fontweight='bold',
    rotation=90, ha='center', va='center', zorder=3)
ax.text(0.2, 6.15, 'BOOMI\nPLATFORM',   color=PURPLE, fontsize=8, fontweight='bold',
    rotation=90, ha='center', va='center', zorder=3)
ax.text(0.2, 1.75, 'UNIVERSITY\nSYSTEMS', color=ORANGE, fontsize=8, fontweight='bold',
    rotation=90, ha='center', va='center', zorder=3)

# ═══════════════════════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════════════════════
ax.text(11, 13.55, 'Higher Education  —  Cloud Modernization  |  IT Visual Walkthrough',
    color=TEXT, fontsize=18, fontweight='bold', ha='center', va='center', zorder=5)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT A — University IT Admin (stick figure)  STEP 1
# ═══════════════════════════════════════════════════════════════════════════════
circle(1.5, 11.45, 0.35, BLUE, 'white', 1.5, zorder=5)          # head
ax.plot([1.5, 1.5], [11.1, 10.25], color=BLUE, lw=2.5, zorder=4)  # body
ax.plot([1.0, 1.5, 2.0], [10.25, 10.75, 10.25], color=BLUE, lw=2.5, zorder=4)  # arms
ax.plot([1.5, 1.1], [10.25, 9.55], color=BLUE, lw=2.5, zorder=4)    # leg L
ax.plot([1.5, 1.9], [10.25, 9.55], color=BLUE, lw=2.5, zorder=4)    # leg R

ax.text(1.5, 9.15, 'Sarah Kim',            color=TEXT,  fontsize=11, fontweight='bold',
    ha='center', va='center', zorder=5)
ax.text(1.5, 8.78, 'University Registrar', color=TEXT2, fontsize=9,
    ha='center', va='center', zorder=5)

fancy_rect(0.5, 8.94, 2.0, 0.42, CARD2, BORDER, lw=1, pad=0.05, zorder=3)
step_badge(0.6, 12.05, '1', BLUE, size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT B — Boomi Migration Console (browser/SPA)  STEP 2
# ═══════════════════════════════════════════════════════════════════════════════
fancy_rect(2.9, 8.6, 3.1, 3.5, CARD2, BORDER, lw=2, pad=0.08, zorder=3)

# Browser chrome
ax.add_patch(plt.Rectangle((2.9, 11.7), 3.1, 0.4, facecolor=BORDER, zorder=4))
circle(3.1, 11.9, 0.07, '#ef4444', 'none', 0, zorder=5)
circle(3.3, 11.9, 0.07, '#f59e0b', 'none', 0, zorder=5)
circle(3.5, 11.9, 0.07, '#22c55e', 'none', 0, zorder=5)
fancy_rect(3.6, 11.75, 2.2, 0.25, CARD, BORDER, lw=1, pad=0.03, zorder=5)
ax.text(4.7, 11.875, 'registrar-portal.html', color=TEXT2, fontsize=6.5,
    ha='center', va='center', zorder=6)

# Left nav sidebar
ax.add_patch(plt.Rectangle((2.9, 8.6), 0.5, 3.1, facecolor=BG, zorder=4))
for yi in [11.3, 11.0, 10.7, 10.4, 10.1]:
    ax.plot([2.95, 3.35], [yi, yi], color=BORDER, lw=2, zorder=5)

# Main content
ax.add_patch(plt.Rectangle((3.4, 8.6), 2.1, 3.1, facecolor=BG, zorder=4))

# KPI cards
for kx in [3.5, 4.1, 4.7]:
    fancy_rect(kx, 11.0, 0.45, 0.5, CARD, BORDER, lw=1, pad=0.04, zorder=5)

# Migration status card
ax.add_patch(FancyBboxPatch((3.45, 9.6), 2.0, 0.72,
    boxstyle="round,pad=0.05", facecolor='#f0fdf4', edgecolor=GREEN, lw=1, zorder=5))
ax.text(4.45, 9.97, 'Enrollment Status', color=TEXT, fontsize=6.5,
    fontweight='bold', ha='center', va='center', zorder=6)
ax.text(4.45, 9.74, 'Spring 2025 Registration  ·  In Progress', color=GREEN, fontsize=5.5,
    ha='center', va='center', zorder=6)
# Progress bar
ax.add_patch(plt.Rectangle((3.5, 9.50), 1.9, 0.16, facecolor=BORDER, zorder=5))
ax.add_patch(plt.Rectangle((3.5, 9.50), 1.22, 0.16, facecolor=GREEN, zorder=6))
ax.text(4.45, 9.38, '64% enrolled', color=TEXT2, fontsize=5.5,
    ha='center', va='center', zorder=6)

# Right monitor panel
ax.add_patch(FancyBboxPatch((5.5, 8.6), 0.5, 3.1,
    boxstyle="round,pad=0.05", facecolor='#eff6ff', edgecolor=BLUE, lw=1, zorder=5))
ax.text(5.75, 10.5, 'Enrollment\nMonitor', color=TEXT, fontsize=6, ha='center', va='center', zorder=6)

ax.text(4.45, 8.38, 'Registrar Enrollment Portal', color=TEXT, fontsize=11,
    fontweight='bold', ha='center', va='center', zorder=5)
ax.text(4.45, 8.1, 'Course Registration & Student Records', color=TEXT2, fontsize=9,
    ha='center', va='center', zorder=5)

step_badge(3.0, 12.3, '2', BLUE, size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT CP — Boomi API Control Plane (governance band)  STEP 3
# ═══════════════════════════════════════════════════════════════════════════════
ax.add_patch(FancyBboxPatch((10.3, 7.80), 8.5, 0.52,
    boxstyle="round,pad=0.05", facecolor='#e8f4f8', edgecolor=PURPLE, lw=1.5, zorder=4))
ax.add_patch(plt.Rectangle((10.3, 7.80), 0.07, 0.52, facecolor=PURPLE, zorder=5))
ax.text(14.55, 8.18, 'BOOMI API CONTROL PLANE', color=PURPLE, fontsize=8,
    fontweight='bold', ha='center', va='center', zorder=6)
ax.text(14.55, 7.94,
    'Federated Discovery  •  Multi-Gateway Governance  •  OWASP Security  •  OpenAPI Conformance',
    color=PURPLE_DARK, fontsize=8.5, ha='center', va='center', zorder=6, style='italic')
step_badge(17.4, 8.68, '4', PURPLE, size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT C — HTTP arrow: Console → Boomi Runtime  STEP 5
# ═══════════════════════════════════════════════════════════════════════════════
ax.annotate('', xy=(9.7, 7.6), xytext=(5.5, 8.6),
    arrowprops=dict(arrowstyle='->', color=PURPLE, lw=3,
        connectionstyle='arc3,rad=-0.15'), zorder=6)
ax.text(7.8, 9.0, 'POST /api/enrollment/register', color=PURPLE, fontsize=7.5,
    ha='center', va='center', rotation=-18, zorder=7,
    bbox=dict(boxstyle='round,pad=0.15', facecolor=CARD, edgecolor=BORDER, alpha=0.9))
ax.text(7.8, 8.77, '{ "term": "Spring-2025", "event": "enrollment" }', color=PURPLE_DARK,
    fontsize=7, ha='center', va='center', rotation=-18, zorder=7)
step_badge(7.82, 7.65, '3', PURPLE, size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT DH — Boomi Data Hub  STEP 4
# ═══════════════════════════════════════════════════════════════════════════════
fancy_rect(1.5, 4.6, 3.0, 3.0, CARD, PURPLE, lw=2.5, pad=0.1, zorder=3)
ax.add_patch(plt.Rectangle((1.5, 7.2), 3.0, 0.4, facecolor=PURPLE, zorder=4))
ax.text(3.0, 7.4, 'BOOMI DATA HUB', color='white', fontsize=9,
    fontweight='bold', ha='center', va='center', zorder=5)

dh_rows = [
    ('Institutional Golden Records', PURPLE,  True),
    ('Student 360',                  TEXT2,   False),
    ('Employee 360',                 TEXT2,   False),
    ('Finance 360',                  TEXT2,   False),
]
for (label, color, bold), ry in zip(dh_rows, [6.65, 6.15, 5.65, 5.15]):
    ax.add_patch(plt.Rectangle((1.7, ry), 2.6, 0.38,
        facecolor=CARD2, edgecolor=BORDER, lw=1, zorder=4))
    circle(1.85, ry + 0.19, 0.07, PURPLE, 'none', 0, zorder=5)
    ax.text(3.1, ry + 0.19, label, color=color, fontsize=7.5,
        fontweight='bold' if bold else 'normal', ha='center', va='center', zorder=5)

ax.text(3.0, 4.88, 'Master Data', color=PURPLE_DARK, fontsize=8,
    ha='center', va='center', zorder=5, style='italic')
ax.text(3.0, 4.3,  'Boomi Data Hub', color=TEXT, fontsize=11,
    fontweight='bold', ha='center', va='center', zorder=5)
ax.text(3.0, 4.02, 'Student  •  Employee  •  Finance', color=TEXT2, fontsize=9,
    ha='center', va='center', zorder=5)

step_badge(1.4, 7.95, '5', PURPLE, size=10)

# Bidirectional: Data Hub ↔ Boomi Runtime
arrow(4.5, 6.1, 8.1, 6.1, PURPLE_DARK, lw=2.0, style='<->', zorder=6)
ax.text(6.3, 6.35, 'Golden Record Lookup', color=PURPLE_DARK, fontsize=8.5,
    ha='center', va='center', zorder=7)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT D — Boomi Runtime  STEP 5 (receiving end)
# ═══════════════════════════════════════════════════════════════════════════════
fancy_rect(8.1, 4.6, 3.2, 3.0, CARD, PURPLE, lw=2.5, pad=0.1, zorder=3)
ax.add_patch(plt.Rectangle((8.1, 7.2), 3.2, 0.4, facecolor=PURPLE, zorder=4))
ax.text(9.7, 7.4, 'BOOMI RUNTIME', color='white', fontsize=10,
    fontweight='bold', ha='center', va='center', zorder=5)

for ry, rl, sy in zip([6.6, 6.1, 5.6],
                      ['API Integration', 'Event-Driven Sync', 'Scheduled Data Load'],
                      [6.79, 6.29, 5.79]):
    ax.add_patch(plt.Rectangle((8.3, ry), 2.8, 0.38,
        facecolor=CARD2, edgecolor=BORDER, lw=1, zorder=4))
    circle(8.45, sy, 0.07, '#22c55e', 'none', 0, zorder=5)
    for bx, bh in [(8.65, 0.15), (8.80, 0.22), (8.95, 0.1)]:
        ax.add_patch(plt.Rectangle((bx, sy - bh/2), 0.1, bh,
            facecolor=PURPLE, alpha=0.7, zorder=5))
    ax.text(9.15, sy, rl, color=TEXT2, fontsize=7.5, ha='left', va='center', zorder=5)

ax.text(9.7, 4.3,  'Boomi Runtime',           color=TEXT,  fontsize=11,
    fontweight='bold', ha='center', va='center', zorder=5)
ax.text(9.7, 4.02, 'Scalable Modernization Engine', color=TEXT2, fontsize=9,
    ha='center', va='center', zorder=5)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT E — Boomi Runtime → Integration Hub arrow  STEP 6
# ═══════════════════════════════════════════════════════════════════════════════
arrow(11.5, 6.15, 14.2, 6.15, PURPLE, lw=3, zorder=6)
ax.text(12.85, 6.5, 'Route &\nTransform', color=PURPLE, fontsize=8,
    ha='center', va='center', zorder=7)
step_badge(12.85, 7.2, '6', PURPLE, size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT F — Boomi Integration Hub  STEP 7
# ═══════════════════════════════════════════════════════════════════════════════
fancy_rect(14.3, 4.6, 6.5, 3.0, CARD, PURPLE, lw=2.5, pad=0.1, zorder=3)
ax.add_patch(plt.Rectangle((14.3, 7.2), 6.5, 0.4, facecolor=PURPLE, zorder=4))
ax.text(17.55, 7.4, 'BOOMI PLATFORM', color='white', fontsize=10,
    fontweight='bold', ha='center', va='center', zorder=5)

# Robot icon (compact, top-left)
ax.add_patch(FancyBboxPatch((14.48, 6.64), 0.44, 0.30,
    boxstyle="round,pad=0.03", facecolor=CARD2, edgecolor=PURPLE, lw=1.5, zorder=5))
circle(14.60, 6.80, 0.04, PURPLE, 'none', 0, zorder=6)
circle(14.80, 6.80, 0.04, PURPLE, 'none', 0, zorder=6)
ax.plot([14.70, 14.70], [6.94, 7.05], color=PURPLE, lw=1.2, zorder=6)
circle(14.70, 7.07, 0.04, PURPLE, 'none', 0, zorder=6)
ax.add_patch(FancyBboxPatch((14.50, 6.26), 0.40, 0.36,
    boxstyle="round,pad=0.03", facecolor=CARD2, edgecolor=PURPLE, lw=1.2, zorder=5))
ax.plot([14.50, 14.36], [6.42, 6.28], color=PURPLE, lw=1.5, zorder=5)
ax.plot([14.90, 15.04], [6.42, 6.28], color=PURPLE, lw=1.5, zorder=5)
ax.plot([14.60, 14.54], [6.26, 6.05], color=PURPLE, lw=1.5, zorder=5)
ax.plot([14.80, 14.86], [6.26, 6.05], color=PURPLE, lw=1.5, zorder=5)

ax.text(17.55, 6.88, 'Modernization Engine',              color=TEXT,  fontsize=9,
    fontweight='bold', ha='center', va='center', zorder=5)
ax.text(17.55, 6.65, 'Validate  ·  Transform  ·  Route', color=TEXT2, fontsize=7,
    ha='center', va='center', zorder=5)

# Integration process badges (3×3 grid) — uniform w=1.75 h=0.38, evenly spaced
proc_labels = [
    ['Course Enrollment', 'Waitlist Processing', 'Degree Audit'],
    ['Student Record Update', 'Grade Posting',   'Transcript Request'],
    ['Term Registration', 'Add / Drop',          'Graduation Clearance'],
]
for ry, row in zip([5.87, 5.32, 4.77], proc_labels):
    for rx, label in zip([14.45, 16.67, 18.90], row):
        ax.add_patch(FancyBboxPatch((rx, ry), 1.75, 0.38,
            boxstyle="round,pad=0.04", facecolor='#e8f4f8', edgecolor=PURPLE, lw=1, zorder=5))
        ax.text(rx + 0.875, ry + 0.19, label, color=PURPLE, fontsize=6.5,
            ha='center', va='center', zorder=6)

ax.text(17.55, 4.3,  'Hybrid Connectivity Hub',              color=TEXT,  fontsize=11,
    fontweight='bold', ha='center', va='center', zorder=5)
ax.text(17.55, 4.02, 'On-Premise & Cloud  •  Any System, Any Direction', color=TEXT2, fontsize=9,
    ha='center', va='center', zorder=5)

step_badge(21.0, 7.4, '7', PURPLE, size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT G — Arrows: Hub → Systems (down into swim lane)
# ═══════════════════════════════════════════════════════════════════════════════
# Pull Student Records — vertical arrow from Hub bottom to above coexistence banner
ax.annotate('', xy=(15.1, 3.3), xytext=(15.1, 4.5),
    arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2.5), zorder=6)
ax.text(14.85, 3.95, 'Pull Student\nRecords', color=ORANGE, fontsize=9.5,
    ha='right', va='center', zorder=7)

# Sync to Cloud Target — vertical arrow from Hub bottom to above coexistence banner
ax.annotate('', xy=(19.9, 3.3), xytext=(19.9, 4.5),
    arrowprops=dict(arrowstyle='->', color=GREEN, lw=2.5), zorder=6)
ax.text(20.15, 3.95, 'Sync to\nCloud Target', color=GREEN, fontsize=9.5,
    ha='left', va='center', zorder=7)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT H — University Systems bottom row  STEPS 8 & 9
# ═══════════════════════════════════════════════════════════════════════════════

# ── LEFT: Legacy Systems ─────────────────────────────────────────────────────
fancy_rect(0.5, 0.75, 8.6, 2.0, CARD, ORANGE, lw=2, pad=0.1, zorder=3)
ax.text(4.8, 2.58, 'ON-PREMISE APPLICATIONS', color=ORANGE,
    fontsize=9, fontweight='bold', ha='center', va='center', zorder=5)
ax.text(4.8, 2.38, 'any combination may be active alongside cloud', color=ORANGE,
    fontsize=8, style='italic', ha='center', va='center', zorder=5)

legacy = [
    {'x': 0.8,  'label': 'B',  'name': 'Banner\nSIS',        'lc': '#1A6BA0'},
    {'x': 2.65, 'label': 'PS', 'name': 'PeopleSoft\nHRMS',   'lc': '#455A64'},
    {'x': 4.50, 'label': 'S',  'name': 'SAP\nHCM',           'lc': '#082B55'},
    {'x': 6.35, 'label': 'OE', 'name': 'Oracle\nEBS',        'lc': '#C0392B'},
]
for s in legacy:
    ax.add_patch(FancyBboxPatch((s['x'], 0.88), 1.65, 1.35,
        boxstyle="round,pad=0.06", facecolor=CARD2, edgecolor=s['lc'], lw=1.5, zorder=4))
    ax.text(s['x'] + 0.825, 1.58, s['label'], color=s['lc'], fontsize=20,
        fontweight='bold', ha='center', va='center', zorder=5)
    ax.text(s['x'] + 0.825, 1.02, s['name'], color=TEXT2, fontsize=7.5,
        ha='center', va='center', zorder=5)

# Coexistence callout — spans both system containers
ax.add_patch(plt.Rectangle((0.5, 2.93), 20.9, 0.35,
    facecolor=TEXT2, alpha=0.10, zorder=3))
ax.text(11.0, 3.1,
    'Any combination of on-premise and cloud can be active simultaneously  ·  Boomi manages coexistence at every phase',
    ha='center', va='center', fontsize=9.5, color=TEXT2,
    fontweight='bold', style='italic', zorder=4)

step_badge(0.78, 2.75, '8', ORANGE, size=10)

# ── RIGHT: Modern Cloud Targets ──────────────────────────────────────────────
fancy_rect(9.4, 0.75, 12.0, 2.0, CARD, GREEN, lw=2, pad=0.1, zorder=3)
ax.text(15.4, 2.58, 'CLOUD APPLICATIONS', color=GREEN,
    fontsize=9, fontweight='bold', ha='center', va='center', zorder=5)
ax.text(15.4, 2.38, 'any combination may be active alongside on-premise', color=GREEN,
    fontsize=8, style='italic', ha='center', va='center', zorder=5)

cloud = [
    {'x': 9.65,  'label': 'OC', 'name': 'Oracle\nCloud',      'lc': '#C0392B'},
    {'x': 11.50, 'label': 'W',  'name': 'Workday',            'lc': '#0075B3'},
    {'x': 13.35, 'label': 'EC', 'name': 'Ellucian\nCloud',    'lc': '#006D5B'},
    {'x': 15.20, 'label': 'SF', 'name': 'Salesforce\nEdu',    'lc': '#0D9488'},
    {'x': 17.05, 'label': 'MS', 'name': 'Microsoft\nEntra',   'lc': '#455A64'},
]
for s in cloud:
    ax.add_patch(FancyBboxPatch((s['x'], 0.88), 1.65, 1.35,
        boxstyle="round,pad=0.06", facecolor=CARD2, edgecolor=s['lc'], lw=1.5, zorder=4))
    ax.text(s['x'] + 0.825, 1.58, s['label'], color=s['lc'], fontsize=20,
        fontweight='bold', ha='center', va='center', zorder=5)
    ax.text(s['x'] + 0.825, 1.02, s['name'], color=TEXT2, fontsize=7.5,
        ha='center', va='center', zorder=5)

step_badge(21.1, 2.75, '9', GREEN, size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT I — Response path (dashed return loop)  STEPS 10 & 11
# ═══════════════════════════════════════════════════════════════════════════════
# Segment 1: Hub right side → go right
ax.annotate('', xy=(21.6, 6.15), xytext=(20.9, 6.15),
    arrowprops=dict(arrowstyle='-', color=GREEN, lw=2.5, linestyle='dashed'), zorder=6)
# Segment 2: go up
ax.annotate('', xy=(21.6, 10.5), xytext=(21.6, 6.15),
    arrowprops=dict(arrowstyle='-', color=GREEN, lw=2.5, linestyle='dashed'), zorder=6)
# Segment 3: go left
ax.annotate('', xy=(6.2, 10.5), xytext=(21.6, 10.5),
    arrowprops=dict(arrowstyle='-', color=GREEN, lw=2.5, linestyle='dashed'), zorder=6)
# Segment 4: down into monitor panel
ax.annotate('', xy=(5.85, 10.0), xytext=(6.2, 10.5),
    arrowprops=dict(arrowstyle='->', color=GREEN, lw=2.5, linestyle='dashed'), zorder=6)

# JSON response label
ax.text(13.7, 10.82,
    '{ "status": "enrolled",  "student_id": "STU-48291",  "term": "Spring-2025" }',
    color=GREEN, fontsize=8, ha='center', va='center', zorder=7,
    bbox=dict(boxstyle='round,pad=0.2', facecolor=CARD, edgecolor=BORDER, alpha=0.9))

step_badge(21.6, 8.5,  '10', GREEN, size=10)
step_badge(13.7, 11.5, '11', GREEN, size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT J — Sync confirmation in monitor panel
# ═══════════════════════════════════════════════════════════════════════════════
ax.add_patch(FancyBboxPatch((5.5, 9.2), 0.45, 0.8,
    boxstyle="round,pad=0.05", facecolor=GREEN, edgecolor='none', zorder=7))
ax.text(5.725, 9.6, 'Enrolled', color='white', fontsize=5.5,
    ha='center', va='center', zorder=8)

ax.add_patch(FancyBboxPatch((5.35, 9.05), 0.65, 0.15,
    boxstyle="round,pad=0.02", facecolor=GREEN_DARK, edgecolor='none', zorder=7))
ax.text(5.675, 9.125, 'Boomi Connected', color='white', fontsize=4.5,
    ha='center', va='center', zorder=8)

# Final checkmark badge
circle(5.3, 12.75, 0.32, GREEN, 'white', 1.5, zorder=9)
ax.text(5.3, 12.75, '✓', color='white', fontsize=11,
    fontweight='bold', ha='center', va='center', zorder=10)
ax.text(5.3, 12.3, 'FINAL', color=GREEN, fontsize=7,
    ha='center', va='center', zorder=9)

# ═══════════════════════════════════════════════════════════════════════════════
# LEGEND
# ═══════════════════════════════════════════════════════════════════════════════
legend_x, legend_y = 0.5, -0.36
ax.text(legend_x, legend_y + 0.65, 'LEGEND', color=TEXT, fontsize=8,
    fontweight='bold', ha='left', va='center', zorder=5)

for i, (color, label) in enumerate([
    (BLUE,   'Browser / User'),
    (PURPLE, 'Boomi Platform'),
    (GREEN,  'Cloud Targets'),
    (ORANGE, 'Legacy Systems'),
]):
    lx = legend_x + i * 2.8
    circle(lx + 0.12, legend_y + 0.3, 0.1, color, 'white', 1, zorder=5)
    ax.text(lx + 0.3, legend_y + 0.3, label, color=TEXT2, fontsize=7,
        ha='left', va='center', zorder=5)

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
output_path = ('/mnt/c/users/BrianMerrick/Documents/Dev/ClaudeCode/'
               'boomicompanion_template_workspace/business-demo/higher-education/'
               'boomi-highered-modernization.png')

plt.savefig(output_path, bbox_inches='tight', dpi=150, facecolor=BG,
    edgecolor='none', format='png')
plt.close(fig)

subprocess.run([
    'convert', output_path,
    '-resize', '1920x1080',
    '-background', BG,
    '-gravity', 'center',
    '-extent', '1920x1080',
    output_path
], check=True)

print(f"Saved: {output_path}  (1920×1080, 16:9)")
