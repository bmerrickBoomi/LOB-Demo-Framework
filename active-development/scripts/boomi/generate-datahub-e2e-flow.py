#!/usr/bin/env python3.11
"""
Boomi DataHub — Employee 360 HR Domain — End-to-End Flow Diagram
Phases: Model Design → Deploy → Inbound Sync → Stewardship → Outbound Sync
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ─── Canvas — 16:9 for Google Slides ──────────────────────────────────────────
FW, FH = 16, 9
fig, ax = plt.subplots(figsize=(FW, FH))
# ── Boomi brand palette ────────────────────────────────────────────────────────
# Primary:    #003C57  (navy/teal,  Pantone 302 C)
# Deep navy:  #082B55  (Madison,    Brandfetch)
# Brand blue: #083F69  (Brandfetch)
# Coral:      #FF7864  (accent,     Pantone 805 C)
# Derived tints from the two anchors fill the remaining roles.
BG = '#E8F2F6'   # very light tint of Boomi primary navy
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.axis('off')

WHITE      = '#FFFFFF'
NAVY       = '#003C57'   # Boomi primary navy (text / titles)
ARROW_CLR  = '#7FBFD4'   # light tint of primary navy

# ─── Phase definitions ─────────────────────────────────────────────────────────
# (display label, header/accent color, step fill color)
PHASES = [
    ('1   MODEL DESIGN',  '#003C57', '#0D5175'),   # Boomi primary navy
    ('2   DEPLOY',        '#083F69', '#1A5A8A'),   # Boomi brand blue
    ('3   INBOUND SYNC',  '#1A6E99', '#2480B0'),   # medium blue tint
    ('4   STEWARDSHIP',   '#FF7864', '#FF8E7D'),   # Boomi coral accent
    ('5   OUTBOUND SYNC', '#082B55', '#0E3D75'),   # Boomi deep navy
]

# ─── Persona badge definitions ──────────────────────────────────────────────────
# key: (badge_color, text_color, long_label)
PERSONA = {
    'DA':   ('#003C57', WHITE, 'Data Architect'),          # Boomi primary navy
    'PA':   ('#082B55', WHITE, 'Platform Admin'),          # Boomi deep navy
    'ID':   ('#083F69', WHITE, 'Integration Dev'),         # Boomi brand blue
    'DS':   ('#FF7864', WHITE, 'Data Steward'),            # Boomi coral
    'HDO':  ('#1A6E99', WHITE, 'HR Data Owner / Governance'), # medium blue tint
    'AUTO': ('#2D5A7B', WHITE, 'Hub (Automated)'),         # mid-tone tint
}

# ─── Steps per phase (2-line labels for slide readability) ────────────────────
STEPS = [
    [  # Phase 1: Model Design
        ('Create Model\nName + Root Element',          ['DA']),
        ('Define Fields\nEmpID · Name · Dept · Email', ['DA', 'HDO']),
        ('Data Quality Steps\nValidation & Enrichment',['DA']),
        ('Match Rules\nExact · Fuzzy · Threshold',     ['DA', 'HDO']),
        ('Configure Sources\nLenel Badge · PeopleSoft', ['DA', 'ID']),
    ],
    [  # Phase 2: Deploy
        ('Publish Model\nVersion Auto-Assigned',       ['DA']),
        ('Deploy to Repository\nActivates Domain',     ['PA']),
    ],
    [  # Phase 3: Inbound Sync
        ('Build Inbound Process\nOne per Source',      ['ID']),
        ('Sources Contribute\nEmployee Records to Hub',['ID', 'AUTO']),
        ('Hub Creates / Updates\nGolden Records',      ['AUTO']),
    ],
    [  # Phase 4: Stewardship
        ('Quarantine Review\nDuplicates & Errors',     ['DS']),
        ('Resolve Duplicates\nMerge or End-Date',      ['DS', 'HDO']),
        ('Enrich & Fix Data\nManual Corrections',      ['DS', 'HDO']),
        ('Governance & Audit\nApprovals + Trail',      ['HDO', 'DA']),
    ],
    [  # Phase 5: Outbound Sync
        ('Generate Channel Updates\nFULL or DIFF Mode',['AUTO']),
        ('Build Outbound Process\nOne per Target',     ['ID']),
        ('Fetch Channel Updates\nDataHub Connector',   ['ID', 'AUTO']),
        ('Sync to Downstream\nLenel Badge',            ['ID', 'AUTO']),
    ],
]

# ─── Layout constants (tuned for 16:9) ─────────────────────────────────────────
MARGIN_X   = 0.25
MARGIN_Y_B = 0.72     # single-row legend
MARGIN_Y_T = 0.48     # title
GAP        = 0.07     # gap between phase bands
PHASE_H    = (FH - MARGIN_Y_B - MARGIN_Y_T - 4 * GAP) / 5   # ~1.49
STEP_W     = 2.62
STEP_H     = 0.94
BADGE_W    = 0.58
BADGE_H    = 0.17


def phase_bottom(i):
    """Bottom y-coord of phase band i (i=0 is topmost)."""
    return FH - MARGIN_Y_T - (i + 1) * PHASE_H - i * GAP


def step_cx_positions(n):
    """Return n evenly-spaced x-centers, capped max spacing for visual balance."""
    usable  = FW - 2 * MARGIN_X
    spacing = min(usable / n, 4.2)
    total   = spacing * n
    x_start = (FW - total) / 2
    return [x_start + spacing * (j + 0.5) for j in range(n)]


def draw_phase_band(i, label, hdr_color):
    y0 = phase_bottom(i)
    y1 = y0 + PHASE_H

    # Subtle tinted background
    ax.add_patch(FancyBboxPatch(
        (MARGIN_X - 0.10, y0), FW - 2 * MARGIN_X + 0.2, PHASE_H,
        boxstyle='round,pad=0.0',
        facecolor=hdr_color, edgecolor='none', alpha=0.10, zorder=1))

    # Left accent bar
    ax.add_patch(plt.Rectangle(
        (MARGIN_X - 0.10, y0), 0.14, PHASE_H,
        facecolor=hdr_color, edgecolor='none', alpha=0.85, zorder=2))

    # Phase label (top-left of band)
    ax.text(MARGIN_X + 0.14, y1 - 0.14, label,
            fontsize=6.5, fontweight='bold', color=hdr_color,
            va='top', ha='left', zorder=3, fontfamily='sans-serif')


def draw_step(cx, cy, label, personas, fill_color):
    # Drop shadow
    ax.add_patch(FancyBboxPatch(
        (cx - STEP_W/2 + 0.04, cy - STEP_H/2 - 0.04), STEP_W, STEP_H,
        boxstyle='round,pad=0.08', facecolor='#94A3B8',
        edgecolor='none', alpha=0.28, zorder=2))

    # Main box
    ax.add_patch(FancyBboxPatch(
        (cx - STEP_W/2, cy - STEP_H/2), STEP_W, STEP_H,
        boxstyle='round,pad=0.08', facecolor=fill_color,
        edgecolor=WHITE, linewidth=1.0, zorder=3))

    # Step label
    ax.text(cx, cy + 0.08, label,
            ha='center', va='center',
            fontsize=5.8, color=WHITE, fontweight='bold',
            linespacing=1.3, zorder=4)

    # Persona badges (bottom of box)
    n      = len(personas)
    total  = n * BADGE_W + (n - 1) * 0.06
    x0     = cx - total / 2
    by     = cy - STEP_H / 2 + 0.07

    for j, p in enumerate(personas):
        bx             = x0 + j * (BADGE_W + 0.06) + BADGE_W / 2
        pc, tc, _label = PERSONA[p]
        ax.add_patch(FancyBboxPatch(
            (bx - BADGE_W/2, by), BADGE_W, BADGE_H,
            boxstyle='round,pad=0.03', facecolor=pc,
            edgecolor='none', alpha=0.92, zorder=5))
        ax.text(bx, by + BADGE_H / 2, p,
                ha='center', va='center',
                fontsize=4.8, color=tc, fontweight='bold', zorder=6)


def h_arrow(x1, x2, y):
    ax.annotate('', xy=(x2 - 0.05, y), xytext=(x1 + 0.05, y),
                arrowprops=dict(arrowstyle='->', color=ARROW_CLR, lw=1.2,
                                mutation_scale=9))


# ─── Title ─────────────────────────────────────────────────────────────────────
ax.text(FW / 2, FH - MARGIN_Y_T / 2 + 0.05,
        'Boomi DataHub  —  Employee 360 HR Domain  —  End-to-End Lifecycle',
        ha='center', va='center', fontsize=10, fontweight='bold',
        color=NAVY, zorder=5)

# ─── Draw phases & steps ───────────────────────────────────────────────────────
all_centers = []   # list of lists: all_centers[phase_i][step_j] = (cx, cy)

for i, ((label, hdr, fill), phase_steps) in enumerate(zip(PHASES, STEPS)):
    draw_phase_band(i, label, hdr)

    y0  = phase_bottom(i)
    cy  = y0 + PHASE_H / 2 - 0.05   # step vertical center in band
    xs  = step_cx_positions(len(phase_steps))
    row = []

    for j, ((step_label, personas), cx) in enumerate(zip(phase_steps, xs)):
        draw_step(cx, cy, step_label, personas, fill)
        row.append((cx, cy))

        if j > 0:
            prev_cx = xs[j - 1]
            h_arrow(prev_cx + STEP_W / 2, cx - STEP_W / 2, cy)

    all_centers.append(row)

# ─── Inter-phase arrows (↓ on left margin between bands) ──────────────────────
for i in range(len(PHASES) - 1):
    y_top_of_lower = phase_bottom(i + 1) + PHASE_H
    y_bot_of_upper = phase_bottom(i)

    ax.annotate('', xy=(0.72, y_top_of_lower + 0.04), xytext=(0.72, y_bot_of_upper - 0.04),
                arrowprops=dict(arrowstyle='->', color=ARROW_CLR, lw=1.4,
                                mutation_scale=10))

# ─── Legend — single row ───────────────────────────────────────────────────────
items  = list(PERSONA.items())
n      = len(items)
lx0    = MARGIN_X + 0.1
ly     = 0.35
col_w  = (FW - 2 * MARGIN_X - 0.2) / n

ax.text(lx0 - 0.05, ly + 0.04, 'ROLES:',
        fontsize=5.8, fontweight='bold', color=NAVY, va='center')

for idx, (key, (color, tc, long_label)) in enumerate(items):
    lx = lx0 + 0.55 + idx * col_w

    ax.add_patch(FancyBboxPatch(
        (lx, ly - 0.10), 0.50, 0.18,
        boxstyle='round,pad=0.03', facecolor=color,
        edgecolor='none', zorder=5))
    ax.text(lx + 0.25, ly - 0.01, key,
            ha='center', va='center',
            fontsize=4.8, color=tc, fontweight='bold', zorder=6)
    ax.text(lx + 0.60, ly - 0.01, f'= {long_label}',
            ha='left', va='center',
            fontsize=5.5, color=NAVY, zorder=6)

# ─── Footer ────────────────────────────────────────────────────────────────────
ax.text(FW / 2, 0.05,
        'Boomi DataHub  ·  MDM Lifecycle  ·  Employee 360 HR Domain',
        ha='center', va='bottom', fontsize=5, color='#94A3B8', style='italic')

# ─── Save — 200 DPI for crisp rendering at full slide size ────────────────────
output_path = ('/mnt/c/users/BrianMerrick/Documents/Dev/ClaudeCode/'
               'boomicompanion_template_workspace/business-demo/boomi/'
               'boomi-datahub-e2e-flow.png')

plt.savefig(output_path, dpi=200, bbox_inches='tight',
            facecolor=BG, edgecolor='none', format='png')
plt.close(fig)
print(f'Saved: {output_path}')
