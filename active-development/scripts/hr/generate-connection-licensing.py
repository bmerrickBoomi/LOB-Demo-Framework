#!/usr/bin/env python3
"""
Boomi Connection Licensing — Visual Reference
Google Slides widescreen 13.33" x 7.5"
Boomi brand: Navy #082B55  Teal #003C57  Coral #FF7864
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

W, H = 13.33, 7.5
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor('#04101F')
ax.set_facecolor('#04101F')
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis('off')

# ─── Palette ──────────────────────────────────────────────────────────────────
NAVY    = '#082B55'
NAVY2   = '#051830'
TEAL    = '#003C57'
TEAL_LL = '#7EC8E3'
CORAL   = '#FF7864'
CORAL_L = '#FF9E90'
CORAL_LL = '#FFCDC7'
GOLD_L  = '#FCD34D'
WHITE   = '#ffffff'
TEXT2   = '#A8BDD4'
TEXT3   = '#3D5A72'
BORDER  = '#0D3A5C'

# ─── Primitives ───────────────────────────────────────────────────────────────
def fbox(x, y, w, h, fc, ec='none', lw=1.2, pad=0.08, zo=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad={pad}',
                                fc=fc, ec=ec, lw=lw, zorder=zo))

def cdot(cx, cy, lbl='', r=0.12, fc=CORAL, zo=7):
    ax.add_patch(Circle((cx, cy), r, fc=fc, ec='none', zorder=zo))
    if lbl:
        ax.text(cx, cy, lbl, color=WHITE, fontsize=5.5, fontweight='bold',
                ha='center', va='center', zorder=zo+1)

def rtbox(cx, cy, lbl='BR', w=0.50, h=0.28, fc=NAVY, zo=7):
    fbox(cx-w/2, cy-h/2, w, h, fc=fc, ec=TEAL_LL, lw=0.9, pad=0.03, zo=zo)
    ax.text(cx, cy, lbl, color=WHITE, fontsize=4.8, fontweight='bold',
            ha='center', va='center', zorder=zo+1)

def rarr(x1, y, x2, c=TEXT3, lw=1.0):
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->,head_width=0.07,head_length=0.06',
                                color=c, lw=lw), zorder=5)

def badge(cx, cy, n, r=0.22, fs=12):
    ax.add_patch(Circle((cx, cy), r*1.55, fc=CORAL, ec='none', alpha=0.14, zorder=6))
    ax.add_patch(Circle((cx, cy), r, fc=CORAL, ec='none', zorder=7))
    ax.text(cx, cy, str(n), color=WHITE, fontsize=fs, fontweight='bold',
            ha='center', va='center', zorder=8)

# ─── Card layout constants ────────────────────────────────────────────────────
M    = 0.24        # outer margin
GAP  = 0.16        # gap between cards
CW   = (W - 2*M - 2*GAP) / 3   # ≈ 4.19
CH   = 2.18
HDRH = 0.33        # header strip height
# x-positions inside card (relative to card left)
C_CX  = 0.78       # connections area center-x
A1X1  = 1.25       # arrow-1 start
A1X2  = 1.68       # arrow-1 end
R_CX  = 2.50       # runtime area center-x
A2X1  = 3.00       # arrow-2 start
A2X2  = 3.28       # arrow-2 end
L_CX  = 3.66       # license badge center-x
DIAGY = CH - HDRH - 0.52   # diagram center-y (relative to card bottom)
DIV_Y = 0.86       # divider y (relative to card bottom)

COLS  = [M + i*(CW+GAP) for i in range(3)]
ROWS  = [4.45, 2.10]   # card bottom-y for row 1, row 2

# ─── Card components ─────────────────────────────────────────────────────────
def draw_header(cx, cy, num, title):
    fbox(cx, cy+CH-HDRH, CW, HDRH, fc=NAVY, ec='none', lw=0, pad=0.08, zo=3)
    ax.add_patch(Circle((cx+0.20, cy+CH-HDRH/2), 0.115,
                         fc=CORAL, ec='none', zorder=4))
    ax.text(cx+0.20, cy+CH-HDRH/2, str(num), color=WHITE, fontsize=6.5,
            fontweight='bold', ha='center', va='center', zorder=5)
    ax.text(cx+0.40, cy+CH-HDRH/2, title, color=WHITE, fontsize=6.8,
            fontweight='bold', ha='left', va='center', zorder=4)

def draw_conns(cx, cy, labels, note=None):
    """Draw connection dots, centered at C_CX."""
    dy = cy + DIAGY
    n  = len(labels)
    offsets = {1: [0], 2: [-0.22, 0.22], 3: [-0.34, 0, 0.34]}
    for off, lbl in zip(offsets[n], labels):
        cdot(cx + C_CX + off, dy, lbl, r=0.115, fc=CORAL, zo=7)
    ax.text(cx + C_CX, dy + 0.25, f'{n} connection{"s" if n>1 else ""}',
            color=CORAL_LL, fontsize=5.8, ha='center', va='center', zorder=5)
    if note:
        ax.text(cx + C_CX, dy - 0.25, note,
                color=GOLD_L, fontsize=5.2, ha='center', va='center',
                style='italic', zorder=5)

def draw_rts(cx, cy, items, note=None):
    """items = list of (label, color, count)."""
    dy = cy + DIAGY
    icons = []
    for lbl, color, cnt in items:
        for k in range(cnt):
            icons.append((f'{lbl}{k+1 if cnt > 1 else ""}', color))
    n = len(icons)
    offsets = {1: [0], 2: [-0.30, 0.30], 3: [-0.46, 0, 0.46]}
    for off, (lbl, color) in zip(offsets[n], icons):
        rtbox(cx + R_CX + off, dy, lbl=lbl, w=0.46, h=0.26, fc=color, zo=7)
    lbl_map = {1: '1 basic runtime', 2: '2 basic runtimes', 3: '3 basic runtimes'}
    if n == 1 and 'Cluster' in icons[0][0]:
        rt_lbl = '1 runtime cluster'
    else:
        rt_lbl = lbl_map.get(n, f'{n} runtimes')
    ax.text(cx + R_CX, dy + 0.25, rt_lbl,
            color=TEAL_LL, fontsize=5.8, ha='center', va='center', zorder=5)
    if note:
        ax.text(cx + R_CX, dy - 0.25, note,
                color=GOLD_L, fontsize=5.2, ha='center', va='center',
                style='italic', zorder=5)

def draw_arrows(cx, cy):
    dy = cy + DIAGY
    rarr(cx + A1X1, dy, cx + A1X2, c=TEXT3, lw=0.9)
    rarr(cx + A2X1, dy, cx + A2X2, c=TEXT3, lw=0.9)

def draw_license(cx, cy, n):
    dy = cy + DIAGY
    badge(cx + L_CX, dy, n, r=0.21, fs=12)
    ax.text(cx + L_CX, dy - 0.27, 'licenses', color=CORAL_L, fontsize=5.5,
            ha='center', va='center', zorder=5)

def draw_note(cx, cy, lines):
    y = cy + DIV_Y - 0.16
    ax.plot([cx+0.12, cx+CW-0.12], [cy+DIV_Y, cy+DIV_Y],
            color=BORDER, lw=0.6, zorder=3)
    for line in lines:
        ax.text(cx+0.16, y, line, color=TEXT2, fontsize=6.2,
                ha='left', va='top', zorder=4)
        y -= 0.20

def draw_card(cx, cy, num, title, conn_labels, rt_items, lic,
              note_lines, conn_note=None, rt_note=None):
    fbox(cx, cy, CW, CH, fc='#040E1C', ec=BORDER, lw=1.0, pad=0.10, zo=2)
    draw_header(cx, cy, num, title)
    draw_conns(cx, cy, conn_labels, note=conn_note)
    draw_rts(cx, cy, rt_items, note=rt_note)
    draw_arrows(cx, cy)
    draw_license(cx, cy, lic)
    draw_note(cx, cy, note_lines)

# ─── HEADER BAND ──────────────────────────────────────────────────────────────
fbox(0, 6.88, W, 0.62, fc=TEAL, ec='none', lw=0, pad=0, zo=2)
ax.text(0.28, 7.22, 'Boomi Connection Licensing', color=WHITE, fontsize=19,
        fontweight='bold', ha='left', va='center', zorder=4)
ax.text(0.28, 6.99, 'How licenses are counted when connections are deployed to runtimes',
        color=TEAL_LL, fontsize=8.5, ha='left', va='center', zorder=4)
# Key rule callout
fbox(6.70, 6.93, 6.38, 0.50, fc=NAVY2, ec=CORAL, lw=1.8, pad=0.09, zo=3)
ax.text(6.94, 7.22, 'Key Rule:', color=CORAL, fontsize=8.5,
        fontweight='bold', ha='left', va='center', zorder=4)
ax.text(7.82, 7.22, '1 license per unique connection per runtime',
        color=WHITE, fontsize=8.5, ha='left', va='center', zorder=4)
ax.text(6.94, 7.01, 'Unique = component ID  |  Same ID reused across many processes counts only once',
        color=TEXT2, fontsize=7.0, ha='left', va='center', zorder=4)

# ─── SCENARIO CARDS ───────────────────────────────────────────────────────────

# Scenario 1 — 2 conns, 1 BR → 2
draw_card(
    COLS[0], ROWS[0], 1,
    '2 Connections · 1 Basic Runtime',
    ['C1', 'C2'],
    [('BR', NAVY, 1)],
    lic=2,
    note_lines=['2 unique connections × 1 runtime = 2'],
)

# Scenario 2 — 1 conn reused across 2 processes, 1 BR → still 1
draw_card(
    COLS[1], ROWS[0], 2,
    '1 Connection · Reused in 2 Processes · 1 BR',
    ['C1'],
    [('BR', NAVY, 1)],
    lic=1,
    conn_note='used in Process A and Process B',
    note_lines=['Reuse across processes does not multiply.',
                '1 unique connection × 1 runtime = 1.'],
)

# Scenario 3 — 2 conns, 2 basic runtimes → 4
draw_card(
    COLS[2], ROWS[0], 3,
    '2 Connections · 2 Basic Runtimes',
    ['C1', 'C2'],
    [('BR', NAVY, 2)],
    lic=4,
    note_lines=['2 connections × 2 runtimes = 4.',
                'Each basic runtime counts independently.'],
)

# Scenario 4 — 2 conns, 1 cluster (3 nodes) → 2
draw_card(
    COLS[0], ROWS[1], 4,
    '2 Connections · 1 Runtime Cluster',
    ['C1', 'C2'],
    [('Cluster', TEAL, 1)],
    lic=2,
    rt_note='3-node cluster = 1 runtime',
    note_lines=['Cluster counts as 1 regardless of node count.',
                '2 connections × 1 cluster = 2.'],
)

# Scenario 5 — 3 conns, 50 processes, 1 BR → 3
draw_card(
    COLS[1], ROWS[1], 5,
    '3 Connections · 50 Processes · 1 BR',
    ['C1', 'C2', 'C3'],
    [('BR', NAVY, 1)],
    lic=3,
    conn_note='used across 50 processes',
    note_lines=['License count is based on unique connections,',
                'not on number of processes using them.'],
)

# Scenario 6 — original + test copy (new IDs) → 4
# Special: two groups of connections (original and test copy)
cx6, cy6 = COLS[2], ROWS[1]
fbox(cx6, cy6, CW, CH, fc='#040E1C', ec=BORDER, lw=1.0, pad=0.10, zo=2)
draw_header(cx6, cy6, 6, '2 Connections + Test Copy · 1 Cluster')

dy6 = cy6 + DIAGY
# Group 1: original C1, C2
fbox(cx6+0.14, dy6-0.24, 1.14, 0.52, fc='#031520', ec=TEAL, lw=0.7, pad=0.04, zo=4)
ax.text(cx6+0.71, dy6+0.26, 'original', color=TEAL_LL, fontsize=5.5,
        ha='center', va='center', zorder=5)
cdot(cx6+0.43, dy6, 'C1', r=0.105, fc=CORAL, zo=7)
cdot(cx6+0.99, dy6, 'C2', r=0.105, fc=CORAL, zo=7)
# Group 2: test copy C3, C4 (new IDs)
fbox(cx6+1.40, dy6-0.24, 1.14, 0.52, fc='#1a0a04', ec=CORAL_L, lw=0.7, pad=0.04, zo=4)
ax.text(cx6+1.97, dy6+0.26, 'test copy', color=CORAL_LL, fontsize=5.5,
        ha='center', va='center', zorder=5)
cdot(cx6+1.70, dy6, 'C3', r=0.105, fc=CORAL, zo=7)
cdot(cx6+2.26, dy6, 'C4', r=0.105, fc=CORAL, zo=7)
ax.text(cx6+1.97, dy6-0.37, 'new component IDs!', color=GOLD_L, fontsize=5.0,
        style='italic', ha='center', va='center', zorder=5)
# Arrow and runtime
rarr(cx6+2.56, dy6, cx6+2.90, c=TEXT3, lw=0.9)
rtbox(cx6+R_CX+0.28, dy6, lbl='Cluster', w=0.52, h=0.26, fc=TEAL, zo=7)
ax.text(cx6+R_CX+0.28, dy6+0.25, '1 runtime cluster',
        color=TEAL_LL, fontsize=5.8, ha='center', va='center', zorder=5)
rarr(cx6+3.20, dy6, cx6+A2X2+0.10, c=TEXT3, lw=0.9)
badge(cx6+L_CX+0.10, dy6, 4, r=0.21, fs=12)
ax.text(cx6+L_CX+0.10, dy6-0.27, 'licenses', color=CORAL_L, fontsize=5.5,
        ha='center', va='center', zorder=5)
draw_note(cx6, cy6,
          ['Copying a process generates new component IDs.',
           'Reusing the originals would keep it at 2.'])

# ─── PRODUCTION vs TEST STRIP ─────────────────────────────────────────────────
strip_y = 0.22
strip_h = 1.65
fbox(M, strip_y, W-2*M, strip_h, fc=NAVY2, ec=BORDER, lw=1.0, pad=0.10, zo=2)

# Section label
fbox(M, strip_y+strip_h-0.30, 3.4, 0.30, fc=TEAL, ec='none', lw=0, pad=0.06, zo=3)
ax.text(M+0.18, strip_y+strip_h-0.15, 'Production vs Test Licenses',
        color=WHITE, fontsize=8.5, fontweight='bold', ha='left', va='center', zorder=4)

# Visual: 2 conns → split to Test BR → 2 test  AND  Prod Cluster → 2 prod
prod_y = strip_y + 0.55
prod_start_x = M + 0.30

# Two connection dots
cdot(prod_start_x + 0.20, prod_y, 'C1', r=0.11, fc=CORAL, zo=6)
cdot(prod_start_x + 0.52, prod_y, 'C2', r=0.11, fc=CORAL, zo=6)
ax.text(prod_start_x + 0.36, prod_y + 0.24, '2 connections',
        color=CORAL_LL, fontsize=6.0, ha='center', va='center', zorder=5)

# Branch arrows
split_x = prod_start_x + 0.84
# upper branch
ax.annotate('', xy=(split_x+0.42, prod_y+0.26), xytext=(split_x, prod_y),
            arrowprops=dict(arrowstyle='->,head_width=0.06,head_length=0.05',
                            color=TEXT3, lw=0.9), zorder=5)
# lower branch
ax.annotate('', xy=(split_x+0.42, prod_y-0.26), xytext=(split_x, prod_y),
            arrowprops=dict(arrowstyle='->,head_width=0.06,head_length=0.05',
                            color=TEXT3, lw=0.9), zorder=5)

# Test env
test_x = split_x + 0.55
rtbox(test_x, prod_y+0.26, lbl='Test BR', w=0.58, h=0.26, fc='#1A3A1A', zo=6)
ax.text(test_x, prod_y+0.52, 'Test Environment', color=TEAL_LL, fontsize=5.5,
        ha='center', va='center', zorder=5)
rarr(test_x+0.35, prod_y+0.26, test_x+0.68, c=TEXT3, lw=0.9)
badge(test_x+0.95, prod_y+0.26, 2, r=0.17, fs=9)
ax.text(test_x+1.22, prod_y+0.26, '  test licenses',
        color=TEXT2, fontsize=7.0, fontweight='bold', ha='left', va='center', zorder=5)

# Prod env
rtbox(test_x, prod_y-0.26, lbl='Prod Cluster', w=0.68, h=0.26, fc=TEAL, zo=6)
ax.text(test_x, prod_y-0.52, 'Production Environment', color=CORAL_LL, fontsize=5.5,
        ha='center', va='center', zorder=5)
rarr(test_x+0.40, prod_y-0.26, test_x+0.73, c=TEXT3, lw=0.9)
badge(test_x+1.00, prod_y-0.26, 2, r=0.17, fs=9)
ax.text(test_x+1.27, prod_y-0.26, '  production licenses',
        color=TEXT2, fontsize=7.0, fontweight='bold', ha='left', va='center', zorder=5)

# Summary text — centered in whitespace between visual (~x=4.2) and Note box (~x=8.99)
TEXT_CX = 6.6
ax.text(TEXT_CX, strip_y+strip_h-0.44,
        'Purchase test and production licenses separately. They behave identically;\n'
        'environment extensions such as passwords and URLs can be configured independently.',
        color=TEXT2, fontsize=7.0, ha='center', va='top', zorder=4, linespacing=1.5)
ax.text(TEXT_CX, strip_y+strip_h-0.82,
        'Connections deployed to Production environments consume production licenses.\n'
        'Test environments consume test licenses. Same counting rules apply to both.',
        color=TEXT2, fontsize=7.0, ha='center', va='top', zorder=4, linespacing=1.5)

# Tip box: Build tab note
tip_x = W - M - 4.10
fbox(tip_x, strip_y+0.12, 4.10, 1.30, fc='#030C17', ec=TEAL, lw=1.0, pad=0.08, zo=3)
ax.text(tip_x+0.20, strip_y+1.18, 'Note:', color=TEAL_LL, fontsize=7.5,
        fontweight='bold', ha='left', va='center', zorder=4)
ax.text(tip_x+0.75, strip_y+1.18, 'Build-tab connections are never counted',
        color=WHITE, fontsize=7.5, ha='left', va='center', zorder=4)
ax.text(tip_x+0.20, strip_y+0.88,
        'Connections only consume licenses when deployed.',
        color=TEXT2, fontsize=7.0, ha='left', va='center', zorder=4)
ax.text(tip_x+0.20, strip_y+0.66,
        'Licenses are checked at deployment time.',
        color=TEXT2, fontsize=7.0, ha='left', va='center', zorder=4)
ax.text(tip_x+0.20, strip_y+0.44,
        "If you don't have enough, the deployment will fail.",
        color=TEXT2, fontsize=7.0, ha='left', va='center', zorder=4)

# ─── Save ─────────────────────────────────────────────────────────────────────
output_path = (
    '/mnt/c/users/BrianMerrick/Documents/Dev/ClaudeCode/'
    'boomicompanion_template_workspace/business-demo/hr/boomi-connection-licensing.png'
)
plt.savefig(output_path, dpi=144, facecolor='#04101F', edgecolor='none', format='png')
plt.close(fig)
print(f'Saved: {output_path}')
