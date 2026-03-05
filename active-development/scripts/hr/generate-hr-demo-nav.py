#!/usr/bin/env python3
"""
Value Based Demo Framework — Demo Navigation Visual
Sized for Google Slides widescreen (13.33" x 7.5" / 16:9).
Boomi official brand colors: Navy #082B55 · Teal #003C57 · Coral #FF7864
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

# ─── Figure — exact Google Slides widescreen ratio, edge-to-edge fill ─────────
W, H = 13.33, 7.5
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor('#04101F')
ax.set_facecolor('#04101F')
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)   # axes fill entire figure
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis('off')
# No set_aspect('equal') — coordinate space is already 16:9 to match the figure

# ─── Palette — Boomi Official Brand Colors ────────────────────────────────────
SURFACE   = '#082B55'   # Boomi Navy
SURFACE2  = '#062040'   # darker navy
TEAL      = '#003C57'   # Boomi Teal
TEAL_L    = '#005A80'
TEAL_LL   = '#7EC8E3'
TEAL_BG   = '#011B26'
CORAL     = '#FF7864'   # Boomi Coral
CORAL_L   = '#FF9E90'
CORAL_LL  = '#FFCDC7'
CORAL_BG  = '#280B07'
WHITE     = '#ffffff'
TEXT2     = '#A8BDD4'
TEXT3     = '#3D5A72'
BORDER    = '#0D3A5C'

# ─── Helpers ──────────────────────────────────────────────────────────────────
def box(x, y, w, h, fc, ec, lw=1.8, pad=0.12, zorder=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad={pad}',
                                facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder))

def seg(x1, y1, x2, y2, c=BORDER, lw=1.5, zorder=4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-', color=c, lw=lw), zorder=zorder)

def arr(x1, y1, x2, y2, c=WHITE, lw=2.0, hw=0.11, zorder=4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=f'->,head_width={hw},head_length=0.10',
                                color=c, lw=lw), zorder=zorder)

# ─── Title ────────────────────────────────────────────────────────────────────
ax.text(W/2, 7.12, 'Value Based Demo Framework', color=WHITE, fontsize=22,
        fontweight='bold', ha='center', va='center', zorder=6,
        family='sans-serif')
ax.text(W/2, 6.78, 'Demo Navigation Guide', color=TEAL_LL, fontsize=11,
        ha='center', va='center', zorder=6)

# thin coral rule under subtitle
ax.plot([W/2 - 1.8, W/2 + 1.8], [6.60, 6.60], color=CORAL, lw=1.5, alpha=0.6, zorder=5)

# ─── Unified Entry Box ────────────────────────────────────────────────────────
ECX, ECY = W/2, 5.82
EW, EH   = 5.6, 0.95
EX, EY   = ECX - EW/2, ECY - EH/2

# glow rings
for gw, alpha in [(7.0, 0.05), (6.2, 0.09), (5.4, 0.07)]:
    gh = gw * (EH / EW)
    ax.add_patch(FancyBboxPatch((ECX - gw/2, ECY - gh/2), gw, gh,
                                boxstyle='round,pad=0.35', fc=SURFACE, ec='none',
                                alpha=alpha, zorder=2))

box(EX, EY, EW, EH, fc=SURFACE2, ec=CORAL, lw=2.5, pad=0.15, zorder=4)

# top coral accent bar
ax.add_patch(plt.Rectangle((EX + 0.15, EY + EH - 0.055), EW - 0.30, 0.038,
                             fc=CORAL, ec='none', zorder=5))

ax.text(ECX, ECY + 0.18, 'Unified Entry Page', color=WHITE, fontsize=13,
        fontweight='bold', ha='center', va='center', zorder=6)
ax.text(ECX, ECY - 0.16, 'Single URL  —  All audience paths begin here',
        color=CORAL_L, fontsize=8.5, ha='center', va='center', zorder=6)

# ─── Entry → split ────────────────────────────────────────────────────────────
arr(ECX, EY - 0.01, ECX, 5.12, c=TEXT3, lw=1.6, hw=0.08)

SPY = 5.10
LEFT_X, RIGHT_X = 3.35, W - 3.35   # = 3.35, 9.98

seg(LEFT_X, SPY, RIGHT_X, SPY, c=BORDER, lw=1.6)
ax.add_patch(Circle((ECX, SPY), 0.075, fc=TEXT2, ec='none', zorder=6))

arr(LEFT_X,  SPY, LEFT_X,  4.50, c=CORAL, lw=2.0, hw=0.11)
arr(RIGHT_X, SPY, RIGHT_X, 4.50, c=TEAL,  lw=2.0, hw=0.11)

# ─── Path header boxes ────────────────────────────────────────────────────────
PW, PH = 5.6, 0.95
BX, BY = LEFT_X - PW/2, 3.48
IX, IY = RIGHT_X - PW/2, 3.48

# Business Path
box(BX, BY, PW, PH, fc=CORAL_BG, ec=CORAL, lw=2.2, pad=0.15, zorder=4)
ax.add_patch(FancyBboxPatch((BX + 0.14, BY + PH - 0.27), 1.48, 0.20,
                             boxstyle='round,pad=0.04', fc=CORAL, ec='none', zorder=5))
ax.text(BX + 0.14 + 0.74, BY + PH - 0.17, 'BUSINESS PATH',
        color=WHITE, fontsize=6, fontweight='bold', ha='center', va='center', zorder=6)
ax.text(LEFT_X, BY + 0.52, 'KPIs & Value',
        color=CORAL_L, fontsize=14, fontweight='bold', ha='center', va='center', zorder=6)
ax.text(LEFT_X, BY + 0.20, 'Business stakeholder view',
        color=CORAL_LL, fontsize=8, ha='center', va='center', zorder=6)

# IT Path
box(IX, IY, PW, PH, fc=TEAL_BG, ec=TEAL, lw=2.2, pad=0.15, zorder=4)
ax.add_patch(FancyBboxPatch((IX + 0.14, IY + PH - 0.27), 0.95, 0.20,
                             boxstyle='round,pad=0.04', fc=TEAL, ec='none', zorder=5))
ax.text(IX + 0.14 + 0.475, IY + PH - 0.17, 'IT PATH',
        color=WHITE, fontsize=6, fontweight='bold', ha='center', va='center', zorder=6)
ax.text(RIGHT_X, IY + 0.52, 'Architecture & APIs',
        color=TEAL_L, fontsize=14, fontweight='bold', ha='center', va='center', zorder=6)
ax.text(RIGHT_X, IY + 0.20, 'Technical implementation view',
        color=TEAL_LL, fontsize=8, ha='center', va='center', zorder=6)

# ─── Sub-item rows ────────────────────────────────────────────────────────────
BIZ_ITEMS = [
    ('Business Value Dashboard',   'ROI metrics, KPIs & performance indicators'),
    ('360 Entity Profiles',         'Cross-system data, risk scoring & analytics'),
    ('Process & Case Management',   'Workflow tracking, SLAs & case timeline'),
    ('Compliance & Governance',     'Risk alerts, policy acknowledgments & audit docs'),
]

IT_ITEMS = [
    ('Integration Architecture',    'MCP server, APIs & AI Agent routing'),
    ('API Endpoints & Operations',  'REST endpoints — GET/POST with JSON schemas'),
    ('Connector Health Monitor',    'Real-time sync status across all systems'),
    ('Data Flow & Error Handling',  'Reconciliation, exceptions & audit trail'),
]

RH  = 0.56   # row spacing
RHH = 0.44   # row box height
RW  = 5.6

arr(LEFT_X,  BY, LEFT_X,  BY - 0.04, c=CORAL, lw=1.3, hw=0.07)
arr(RIGHT_X, IY, RIGHT_X, IY - 0.04, c=TEAL,  lw=1.3, hw=0.07)

FIRST_Y = BY - 0.10

for i, (title, sub) in enumerate(BIZ_ITEMS):
    ry  = FIRST_Y - 0.08 - i * RH
    rx  = LEFT_X - RW/2
    box(rx, ry - RHH + 0.02, RW, RHH, fc='#180703', ec=CORAL, lw=0.9, pad=0.07, zorder=4)
    ax.add_patch(Circle((rx + 0.15, ry - RHH/2 + 0.02), 0.052, fc=CORAL, ec='none', zorder=6))
    ax.text(rx + 0.33, ry - 0.07,  title, color=CORAL_LL, fontsize=8.0,
            fontweight='bold', ha='left', va='center', zorder=6)
    ax.text(rx + 0.33, ry - 0.24,  sub,   color=TEXT3,    fontsize=7.0,
            ha='left', va='center', zorder=6)
    if i < len(BIZ_ITEMS) - 1:
        seg(LEFT_X, ry - RHH + 0.02, LEFT_X, ry - RH - RHH + 0.04, c=BORDER, lw=0.7)

for i, (title, sub) in enumerate(IT_ITEMS):
    ry  = FIRST_Y - 0.08 - i * RH
    rx  = RIGHT_X - RW/2
    box(rx, ry - RHH + 0.02, RW, RHH, fc='#010F18', ec=TEAL, lw=0.9, pad=0.07, zorder=4)
    ax.add_patch(Circle((rx + 0.15, ry - RHH/2 + 0.02), 0.052, fc=TEAL, ec='none', zorder=6))
    ax.text(rx + 0.33, ry - 0.07,  title, color=TEAL_LL, fontsize=8.0,
            fontweight='bold', ha='left', va='center', zorder=6)
    ax.text(rx + 0.33, ry - 0.24,  sub,   color=TEXT3,   fontsize=7.0,
            ha='left', va='center', zorder=6)
    if i < len(IT_ITEMS) - 1:
        seg(RIGHT_X, ry - RHH + 0.02, RIGHT_X, ry - RH - RHH + 0.04, c=BORDER, lw=0.7)

# ─── Footer ───────────────────────────────────────────────────────────────────
ax.plot([0.5, W - 0.5], [0.38, 0.38], color=BORDER, lw=0.7, zorder=3)
ax.text(W/2, 0.20, 'Boomi Value Based Demo Framework  —  Adaptable to any industry or use case',
        color=TEXT3, fontsize=7.5, ha='center', va='center', zorder=4)

# ─── Save — exact pixel dimensions for Google Slides 16:9 ────────────────────
# 13.33" x 7.5" @ 144 dpi = 1920 x 1080
output_path = (
    '/mnt/c/users/BrianMerrick/Documents/Dev/ClaudeCode/'
    'boomicompanion_template_workspace/business-demo/hr/vbdf-demo-nav.png'
)
plt.savefig(output_path, dpi=144, facecolor='#04101F', edgecolor='none', format='png')
plt.close(fig)
print(f'Saved: {output_path}')
