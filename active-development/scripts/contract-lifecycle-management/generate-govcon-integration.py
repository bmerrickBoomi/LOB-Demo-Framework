#!/usr/bin/env python3.11
"""
Contract Lifecycle Management — Boomi Data Activation
Professional Services & Government Consulting  |  16:9 Google Slides

Top  : 7-step contract lifecycle flow
Bottom: Left-to-right architecture matching the source sketch:
        [Source Systems] → [Boomi iPaaS] → [Deltek Costpoint Modules]
Foot : Compact roles footnote strip
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

FW, FH = 22, 12.375      # exact 16:9
fig, ax = plt.subplots(figsize=(FW, FH))

BG     = '#F6F9FC'
CARD   = '#FFFFFF'
CARD2  = '#F1F5F9'
BORDER = '#CBD5E1'
TEXT   = '#1E293B'
TEXT2  = '#475569'

NAVY       = '#082B55'
BLUE_MID   = '#1A6BA0'
BLUE_LIGHT = '#4DB8E8'
CORAL      = '#FF7C66'
CORAL_D    = '#C0392B'
WHITE      = '#FFFFFF'
TEAL       = '#006D5B'
GREEN      = '#16a34a'
SLATE      = '#455A64'
GRAY_L     = '#B0BEC5'

fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.axis('off')

# ─── Helpers ───────────────────────────────────────────────────────────────────
def frect(x, y, w, h, fc, ec, lw=1.5, pad=0.07, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f'round,pad={pad}', facecolor=fc, edgecolor=ec, lw=lw, zorder=z))

def circ(cx, cy, r, fc, ec='white', lw=1, z=5):
    ax.add_patch(Circle((cx, cy), r, facecolor=fc, edgecolor=ec, lw=lw, zorder=z))

def arr(x1, y1, x2, y2, color, lw=1.8, style='->', ls='solid', cs='arc3,rad=0', z=4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle=style, color=color, lw=lw,
            linestyle=ls, connectionstyle=cs), zorder=z)

def tint(x0, x1, y0, y1, color, a=0.07):
    ax.add_patch(FancyBboxPatch((x0, y0), x1-x0, y1-y0,
        boxstyle='round,pad=0', facecolor=color, edgecolor='none', alpha=a, zorder=1))

def hdr(x, y, w, h, color, title, fsize=8.0):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color, zorder=4))
    ax.text(x+w/2, y+h/2, title, color=WHITE, fontsize=fsize,
        fontweight='bold', ha='center', va='center', zorder=5)

def item_row(x, y, w, label, color, dot_color=None):
    """Single item row: subtle bg + dot + label."""
    ax.add_patch(plt.Rectangle((x, y), w, 0.34,
        facecolor=CARD2, edgecolor=BORDER, lw=0.6, zorder=5))
    dc = dot_color or color
    circ(x+0.16, y+0.17, 0.065, dc, 'none', 0, z=6)
    ax.text(x+0.35, y+0.17, label, color=TEXT2, fontsize=6.8,
        ha='left', va='center', zorder=6)

def sub_section(x, y_top, w, title, color, items):
    """Draw a titled group of item rows stacked downward from y_top."""
    # Mini header band
    ax.add_patch(FancyBboxPatch((x, y_top-0.28), w, 0.28,
        boxstyle='round,pad=0.03', facecolor=color, edgecolor='none', alpha=0.88, zorder=4))
    ax.text(x+w/2, y_top-0.14, title, color=WHITE, fontsize=6.5,
        fontweight='bold', ha='center', va='center', zorder=5)
    cy = y_top - 0.28
    for lbl in items:
        cy -= 0.38
        item_row(x+0.06, cy, w-0.12, lbl, color)
    return cy - 0.06   # return bottom y

# ═══════════════════════════════════════════════════════════════════════════════
# TITLE BAR
# ═══════════════════════════════════════════════════════════════════════════════
T_H = 0.52
ax.add_patch(plt.Rectangle((0, FH-T_H), FW, T_H, facecolor=NAVY, zorder=10))
ax.text(FW/2, FH-T_H/2,
    'Contract Lifecycle Management  —  How Boomi Activates Data & Replaces Legacy Platforms',
    ha='center', va='center', fontsize=11, fontweight='bold', color=WHITE, zorder=11)
ax.add_patch(plt.Rectangle((0, FH-T_H-0.035), FW, 0.035, facecolor=CORAL, zorder=10))

# ═══════════════════════════════════════════════════════════════════════════════
# CONTRACT LIFECYCLE — compact zones
# ═══════════════════════════════════════════════════════════════════════════════
STEP_Y  = 9.30
STEP_XS = [1.60, 4.70, 7.85, 11.00, 14.15, 17.30, 20.40]
STEP_R  = 0.55

LEGACY_Y0, LEGACY_Y1 = 10.35, 11.82    # height 1.47
BOOMI_Y0,  BOOMI_Y1  =  6.82,  7.85    # height 1.03

tint(0.30, 21.70, LEGACY_Y0, LEGACY_Y1, CORAL,    a=0.08)
tint(0.30, 21.70, BOOMI_Y0,  BOOMI_Y1,  BLUE_MID, a=0.08)

ax.text(0.15, (LEGACY_Y0+LEGACY_Y1)/2, 'LEGACY\nTODAY',
    ha='center', va='center', fontsize=6.5, fontweight='bold',
    color=CORAL, alpha=0.80, rotation=90, zorder=3)
ax.text(0.15, (BOOMI_Y0+BOOMI_Y1)/2, 'BOOMI\nACTIVATES',
    ha='center', va='center', fontsize=6.5, fontweight='bold',
    color=BLUE_MID, alpha=0.80, rotation=90, zorder=3)

steps = [
    {'label':'Opportunity\nIdentification',
     'legacy':'⚠  Manual GovWin exports\n& CRM data silos',
     'boomi': 'API sync: GovWin + Dynamics 365\nEvent trigger on new opportunity',
     'color': BLUE_MID, 'hl': False},
    {'label':'Proposal &\nBid Preparation',
     'legacy':'⚠  Spreadsheet pricing\n& emailed data pulls',
     'boomi': 'Live cost data fed to bid tools\nvia API in real time',
     'color': BLUE_MID, 'hl': False},
    {'label':'Contract\nAward',
     'legacy':'⚠  Award notification\nvia email only',
     'boomi': 'Award event triggers automated\ndownstream workflow instantly',
     'color': TEAL, 'hl': False},
    {'label':'Contract\nActivation',
     'legacy':'⚠  Manual re-entry\ninto Costpoint',
     'boomi': '⚡  Auto-creates: Project · WBS\nBilling · Org Keys · Funding',
     'color': CORAL, 'hl': True},
    {'label':'Execution &\nDelivery',
     'legacy':'⚠  Batch T&E file\ntransfers (nightly)',
     'boomi': 'Real-time labor, invoices &\ndeliverable sync across systems',
     'color': TEAL, 'hl': False},
    {'label':'Modifications\n& Amendments',
     'legacy':'⚠  Email change orders\n& manual ledger edits',
     'boomi': 'Change events sync ceilings,\nbudgets & mods across systems',
     'color': TEAL, 'hl': False},
    {'label':'Closeout\n& Audit',
     'legacy':'⚠  Manual audit package,\nweeks of effort',
     'boomi': 'Auto-compiled audit trail\n& DFARS/CMMC compliance archive',
     'color': BLUE_MID, 'hl': False},
]

replacements = {0:'Replaces: Manual CRM exports', 1:'Replaces: Spreadsheet tools',
                3:'Replaces: Manual Costpoint entry', 4:'Replaces: Nightly batch',
                6:'Replaces: Manual audit assembly'}

for sx in STEP_XS:
    ax.plot([sx,sx],[STEP_Y+STEP_R+0.04, LEGACY_Y0+0.05],
        color=CORAL, lw=0.7, ls=':', alpha=0.38, zorder=2)
    ax.plot([sx,sx],[STEP_Y-STEP_R-0.04, BOOMI_Y1-0.05],
        color=BLUE_LIGHT, lw=0.7, ls=':', alpha=0.38, zorder=2)

for i in range(len(STEP_XS)-1):
    ax.annotate('', xy=(STEP_XS[i+1]-STEP_R-0.06, STEP_Y),
        xytext=(STEP_XS[i]+STEP_R+0.06, STEP_Y),
        arrowprops=dict(arrowstyle='->', color=GRAY_L, lw=1.8, mutation_scale=13), zorder=3)

for i, (sx, s) in enumerate(zip(STEP_XS, steps)):
    r = STEP_R * 1.18 if s['hl'] else STEP_R
    if s['hl']:
        ax.add_patch(Circle((sx, STEP_Y), r+0.14,
            facecolor=CORAL, edgecolor='none', alpha=0.14, zorder=3))
        ax.add_patch(Circle((sx, STEP_Y), r+0.07,
            facecolor=CORAL, edgecolor='none', alpha=0.20, zorder=3))
    circ(sx, STEP_Y, r, s['color'], WHITE, 2.0, z=4)
    ax.text(sx, STEP_Y+0.05, str(i+1), ha='center', va='center',
        fontsize=18 if s['hl'] else 15, fontweight='bold', color=WHITE, zorder=5)
    ax.text(sx, STEP_Y-r-0.13, s['label'], ha='center', va='top',
        fontsize=8.5 if s['hl'] else 8.0,
        fontweight='bold' if s['hl'] else 'normal',
        color=s['color'] if s['hl'] else NAVY, linespacing=1.35, zorder=5)

for i, (sx, s) in enumerate(zip(STEP_XS, steps)):
    ly = (LEGACY_Y0+LEGACY_Y1)/2
    ax.text(sx, ly+0.06, s['legacy'], ha='center', va='center',
        fontsize=8.0, color=CORAL_D, style='italic', linespacing=1.35, zorder=3)
    if i in replacements:
        ax.text(sx, LEGACY_Y1-0.14, replacements[i], ha='center', va='top',
            fontsize=6.5, color=CORAL_D, fontweight='bold', zorder=4)

for i, (sx, s) in enumerate(zip(STEP_XS, steps)):
    cy = (BOOMI_Y0+BOOMI_Y1)/2
    if s['hl']:
        bw, bh = 3.2, 0.56
        box_cy = cy - 0.10   # shift down to clear step label above
        ax.add_patch(FancyBboxPatch((sx-bw/2, box_cy-bh/2), bw, bh,
            boxstyle='round,pad=0.07', facecolor=CORAL,
            edgecolor=CORAL_D, lw=1.3, alpha=0.92, zorder=4))
        ax.text(sx, box_cy+0.10, s['boomi'], ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=WHITE, linespacing=1.3, zorder=5)
        ax.text(sx, box_cy-0.22, 'Integration Engine  +  Event Broker',
            ha='center', va='center', fontsize=5.5, color=WHITE, alpha=0.85, zorder=5)
    else:
        ax.text(sx, cy+0.02, s['boomi'], ha='center', va='center',
            fontsize=7.0, color=NAVY, linespacing=1.35, zorder=3)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION DIVIDER
# ═══════════════════════════════════════════════════════════════════════════════
ARCH_Y = 6.60
ax.plot([0.28, 21.72], [ARCH_Y, ARCH_Y], color=NAVY, lw=0.9, alpha=0.20, zorder=2)
ax.text(FW/2, ARCH_Y-0.12,
    'Platform Architecture  ·  Boomi iPaaS connecting the full contract lifecycle',
    ha='center', va='top', fontsize=7.2, fontweight='bold',
    color=NAVY, alpha=0.52, zorder=3)

# Thin dashed lines connecting key steps down into architecture
for sx, color in [(1.60, BLUE_MID), (11.00, CORAL), (20.40, BLUE_MID)]:
    ax.plot([sx, sx], [BOOMI_Y0-0.04, ARCH_Y+0.02],
        color=color, lw=0.8, ls=':', alpha=0.35, zorder=2)

# ═══════════════════════════════════════════════════════════════════════════════
# ARCHITECTURE LAYOUT — left-to-right matching temp diagram
# ═══════════════════════════════════════════════════════════════════════════════
FOOT_H  = 0.38
CONT_Y0 = FOOT_H + 0.14    # 0.52
CONT_Y1 = ARCH_Y - 0.42    # 8.18
CONT_H  = CONT_Y1 - CONT_Y0   # ~7.66

# Column x boundaries
SRC_X0,  SRC_X1  = 0.48, 3.72     # Source Systems  (3.24 wide)
BOM_X0,  BOM_X1  = 4.05, 16.95    # Boomi Platform  (12.90 wide)
CST_X0,  CST_X1  = 17.28, 21.52   # Deltek Costpoint (4.24 wide)

# ─── SOURCE SYSTEMS ────────────────────────────────────────────────────────────
frect(SRC_X0, CONT_Y0, SRC_X1-SRC_X0, CONT_H, CARD, BLUE_MID, lw=2.0, pad=0.07, z=3)
hdr(SRC_X0, CONT_Y1-0.38, SRC_X1-SRC_X0, 0.38, BLUE_MID, 'SOURCE SYSTEMS', fsize=7.5)

src_cx = (SRC_X0+SRC_X1)/2
src_w  = SRC_X1 - SRC_X0 - 0.32

# CRM Platform box
CRM_Y0, CRM_Y1 = CONT_Y0 + CONT_H*0.52, CONT_Y1 - 0.48
frect(SRC_X0+0.16, CRM_Y0, src_w, CRM_Y1-CRM_Y0, CARD2, BLUE_MID, lw=1.2, pad=0.05, z=4)
ax.text(src_cx, CRM_Y1-0.22, 'CRM Platform', color=BLUE_MID,
    fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=5)
for i, lbl in enumerate(['Contract Award / MS Push', 'Opportunity / Opp']):
    item_row(SRC_X0+0.22, CRM_Y0+0.12+i*0.42, src_w-0.12, lbl, BLUE_MID)

# Dynamics 365 box
DYN_Y0, DYN_Y1 = CONT_Y0 + 0.18, CONT_Y0 + CONT_H*0.48
frect(SRC_X0+0.16, DYN_Y0, src_w, DYN_Y1-DYN_Y0, CARD2, BLUE_MID, lw=1.2, pad=0.05, z=4)
ax.text(src_cx, DYN_Y1-0.22, 'Dynamics 365 Sales', color=BLUE_MID,
    fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=5)
for i, lbl in enumerate(['Pipeline / Tech Data', 'Contact & Org Data']):
    item_row(SRC_X0+0.22, DYN_Y0+0.12+i*0.42, src_w-0.12, lbl, BLUE_MID)

# ─── BOOMI INTEGRATION PLATFORM ───────────────────────────────────────────────
frect(BOM_X0, CONT_Y0, BOM_X1-BOM_X0, CONT_H, CARD, NAVY, lw=2.2, pad=0.07, z=3)
hdr(BOM_X0, CONT_Y1-0.38, BOM_X1-BOM_X0, 0.38, NAVY,
    'BOOMI INTEGRATION PLATFORM  (iPaaS)', fsize=8.5)

# ── Interior layout ────────────────────────────────────────────────────────────
BPAD   = 0.20
OPS_H  = 1.10
OPS_Y0 = CONT_Y0 + 0.14
OPS_Y1 = OPS_Y0 + OPS_H
PIL_Y0 = OPS_Y1 + 0.18
PIL_Y1 = CONT_Y1 - 0.52
PIL_H  = PIL_Y1 - PIL_Y0
PIL_MID_Y = PIL_Y0 + PIL_H / 2

# ── Contract flow layout ────────────────────────────────────────────────────────
IX0      = BOM_X0 + BPAD          # 4.25
IX1      = BOM_X1 - BPAD          # 16.75
FLOW_Y   = PIL_Y1 - 0.48          # flow spine y ≈ 5.18
CARD_Y0  = PIL_Y0 + 0.18          # card bottom ≈ 2.12
CARD_Y1  = FLOW_Y - 0.50          # card top ≈ 4.68
CARD_H   = CARD_Y1 - CARD_Y0      # ≈ 2.56
FULL_Y0  = CARD_Y0 - 0.02         # inlet/outlet bottom ≈ 2.10
FULL_Y1  = PIL_Y1 - 0.06          # inlet/outlet top — uses available room above
FULL_H   = FULL_Y1 - FULL_Y0

INLET_W  = 1.84
OUTLET_W = 2.00
MID_GAP  = 0.22
CAPS_W   = (IX1 - IX0) - INLET_W - OUTLET_W - 2*MID_GAP
CAP_GAP  = 0.16
CAP_W    = (CAPS_W - 2*CAP_GAP) / 3

INLET_X  = IX0
CAP1_X   = INLET_X  + INLET_W  + MID_GAP
CAP2_X   = CAP1_X   + CAP_W    + CAP_GAP
CAP3_X   = CAP2_X   + CAP_W    + CAP_GAP
OUTLET_X = CAP3_X   + CAP_W    + MID_GAP

# ── Contract Event entry box ───────────────────────────────────────────────────
frect(INLET_X, FULL_Y0, INLET_W, FULL_H, CORAL, CORAL_D, lw=1.8, pad=0.06, z=4)
ax.add_patch(FancyBboxPatch((INLET_X, FULL_Y1-0.52), INLET_W, 0.52,
    boxstyle='round,pad=0.04', facecolor=CORAL_D, edgecolor='none', alpha=0.92, zorder=5))
ax.text(INLET_X+INLET_W/2, FULL_Y1-0.26, 'CONTRACT\nEVENT',
    ha='center', va='center', fontsize=8.5, fontweight='bold',
    color=WHITE, linespacing=1.25, zorder=6)
ce_items = [
    ('Award Notification',  'Contract win from CRM'),
    ('Amendment',           'Contract change event'),
    ('Activation Trigger',  'New project creation'),
    ('Change Order',        'Scope / cost update'),
]
for k, (lbl, sub) in enumerate(ce_items):
    iy = FULL_Y1 - 1.00 - k * 0.62
    ax.add_patch(FancyBboxPatch((INLET_X+0.12, iy-0.22), INLET_W-0.24, 0.44,
        boxstyle='round,pad=0.03', facecolor=CORAL_D, edgecolor='none', alpha=0.45, zorder=5))
    circ(INLET_X+0.26, iy, 0.09, WHITE, 'none', 0, z=6)
    ax.text(INLET_X+0.42, iy+0.07, lbl,
        color=WHITE, fontsize=6.8, fontweight='bold', ha='left', va='center', zorder=6)
    ax.text(INLET_X+0.42, iy-0.10, sub,
        color=WHITE, fontsize=6.2, alpha=0.82, ha='left', va='center', zorder=6)

# ── Flow spine with OR routing label ──────────────────────────────────────────
ax.annotate('', xy=(OUTLET_X-0.08, FLOW_Y), xytext=(INLET_X+INLET_W+0.08, FLOW_Y),
    arrowprops=dict(arrowstyle='->', color=BLUE_LIGHT, lw=2.8, mutation_scale=16), zorder=6)
ax.text((INLET_X+INLET_W + OUTLET_X) / 2, FLOW_Y+0.16,
    'Select the right capability based on business event & SLA  ·  Build once, reuse patterns across applications',
    ha='center', va='bottom', fontsize=8.0, color=BLUE_LIGHT,
    style='italic', zorder=7)

# ── Capability cards ───────────────────────────────────────────────────────────
CAPS = [
    (CAP1_X, NAVY,    BLUE_MID,  'INTEGRATION ENGINE',  'Boomi Integration',
     ['Sync & Orchestrate Records', 'Field Map & Transform',
      'Route by Contract Type',     'Retry & Error Handling']),
    (CAP2_X, TEAL,    '#009688', 'EVENT BROKER',        'Boomi Event Broker',
     ['Award Event Published',      'Pub/Sub Fan-out Delivery',
      'FIFO Queue Processing',      'Guaranteed Delivery']),
    (CAP3_X, CORAL_D, CORAL,     'API MANAGEMENT',       'Boomi API Management',
     ['Contract API Gateway',       'JWT / OAuth Authorization',
      'DFARS / CMMC Enforcement',   'Rate Limit & Throttle']),
]

for cx, hc, fc, title, subtitle, items in CAPS:
    frect(cx, CARD_Y0, CAP_W, CARD_H, CARD2, hc, lw=1.4, pad=0.05, z=4)
    HDR_H = 0.72
    ax.add_patch(FancyBboxPatch((cx, CARD_Y1-HDR_H), CAP_W, HDR_H,
        boxstyle='round,pad=0.04', facecolor=hc, edgecolor='none', alpha=0.95, zorder=5))
    ax.text(cx+CAP_W/2, CARD_Y1-HDR_H*0.35, title,
        ha='center', va='center', color=WHITE, fontsize=9.5, fontweight='bold', zorder=6)
    ax.text(cx+CAP_W/2, CARD_Y1-HDR_H*0.72, subtitle,
        ha='center', va='center', color=WHITE, fontsize=7.5, alpha=0.86, style='italic', zorder=6)
    # Vertical connector from spine down to card
    ax.annotate('', xy=(cx+CAP_W/2, CARD_Y1+0.06), xytext=(cx+CAP_W/2, FLOW_Y-0.10),
        arrowprops=dict(arrowstyle='->', color=hc, lw=1.6, mutation_scale=10), zorder=5)
    # OR label on the spine between cards
    if cx != CAP1_X:
        ax.text(cx - CAP_GAP/2, FLOW_Y, 'OR',
            ha='center', va='center', fontsize=8.5, fontweight='bold',
            color=WHITE, zorder=7,
            bbox=dict(boxstyle='round,pad=0.22', facecolor=NAVY,
                      edgecolor=BLUE_LIGHT, lw=1.2, alpha=0.90))
    for k, itm in enumerate(items):
        item_row(cx+0.10, CARD_Y1-HDR_H-0.50-k*0.44, CAP_W-0.20, itm, hc, dot_color=fc)

# ── Transform & Deliver output box ────────────────────────────────────────────
frect(OUTLET_X, FULL_Y0, OUTLET_W, FULL_H, GREEN, '#0A5C2E', lw=1.8, pad=0.06, z=4)
ax.add_patch(FancyBboxPatch((OUTLET_X, FULL_Y1-0.52), OUTLET_W, 0.52,
    boxstyle='round,pad=0.04', facecolor='#0A5C2E', edgecolor='none', alpha=0.92, zorder=5))
ax.text(OUTLET_X+OUTLET_W/2, FULL_Y1-0.26, 'TRANSFORM\n& DELIVER',
    ha='center', va='center', fontsize=8.0, fontweight='bold',
    color=WHITE, linespacing=1.25, zorder=6)
td_items = [
    ('WBS & Project Map',   'Structure to Costpoint'),
    ('Revenue Config',      'Billing & fee parameters'),
    ('Org Key Enrichment',  'Account & cost pools'),
    ('Costpoint API Push',  'Activate in Deltek'),
]
for k, (lbl, sub) in enumerate(td_items):
    iy = FULL_Y1 - 1.00 - k * 0.62
    ax.add_patch(FancyBboxPatch((OUTLET_X+0.12, iy-0.22), OUTLET_W-0.24, 0.44,
        boxstyle='round,pad=0.03', facecolor='#0A5C2E', edgecolor='none', alpha=0.55, zorder=5))
    circ(OUTLET_X+0.26, iy, 0.09, WHITE, 'none', 0, z=6)
    ax.text(OUTLET_X+0.42, iy+0.07, lbl,
        color=WHITE, fontsize=6.8, fontweight='bold', ha='left', va='center', zorder=6)
    ax.text(OUTLET_X+0.42, iy-0.10, sub,
        color=WHITE, fontsize=6.2, alpha=0.82, ha='left', va='center', zorder=6)

# ── Operations & Process Reporting band ───────────────────────────────────────
OPS_X0 = BOM_X0 + BPAD
OPS_W  = BOM_X1 - BOM_X0 - 2*BPAD
frect(OPS_X0, OPS_Y0, OPS_W, OPS_H, '#081F3E', NAVY, lw=1.0, pad=0.04, z=4)
OHR_H = 0.30
ax.add_patch(plt.Rectangle((OPS_X0, OPS_Y1-OHR_H), OPS_W, OHR_H,
    facecolor=NAVY, alpha=0.96, zorder=5))
ax.text(OPS_X0+OPS_W/2, OPS_Y1-OHR_H/2,
    'OPERATIONS  &  PROCESS REPORTING',
    color=WHITE, fontsize=7.5, fontweight='bold',
    ha='center', va='center', zorder=6)

ops_items = [
    (BLUE_LIGHT, 'Process Reporting\nDashboard'),
    (BLUE_LIGHT, 'Document Tracking'),
    (TEAL,       'Execution\nLogs & History'),
    (CORAL,      'Error\nAlerts & Alarms'),
    (GREEN,      'Audit Trail &\nCompliance'),
    (SLATE,      'Analytics'),
]
N_OPS  = len(ops_items)
CGAP   = 0.08
CHIP_H = OPS_H - OHR_H - 0.16
CHIP_W = (OPS_W - 0.16 - (N_OPS-1)*CGAP) / N_OPS
for m, (ic, lbl) in enumerate(ops_items):
    cx = OPS_X0 + 0.08 + m*(CHIP_W+CGAP)
    cy = OPS_Y0 + 0.08
    ax.add_patch(FancyBboxPatch((cx, cy), CHIP_W, CHIP_H,
        boxstyle='round,pad=0.04', facecolor=ic, edgecolor='none',
        alpha=0.20, zorder=5))
    circ(cx+0.18, cy+CHIP_H/2, 0.12, ic, 'none', 0, z=6)
    ax.text(cx+0.36, cy+CHIP_H/2, lbl,
        color=WHITE, fontsize=6.2, fontweight='bold',
        ha='left', va='center', linespacing=1.3, zorder=6)

MID_Y = PIL_MID_Y

# ─── DELTEK COSTPOINT ─────────────────────────────────────────────────────────
frect(CST_X0, CONT_Y0, CST_X1-CST_X0, CONT_H, CARD, GREEN, lw=2.2, pad=0.07, z=3)
hdr(CST_X0, CONT_Y1-0.38, CST_X1-CST_X0, 0.38, GREEN,
    'DELTEK COSTPOINT', fsize=7.5)
ax.text((CST_X0+CST_X1)/2, CONT_Y1-0.56, 'Target Modules',
    ha='center', va='center', fontsize=6.2, color=GREEN, style='italic', zorder=5)

# 4 module cards in 2×2 grid
MOD_W  = (CST_X1-CST_X0-0.36) / 2    # ~1.94
MOD_H  = (CONT_H - 0.72) / 2 - 0.12  # ~3.39
MOD_GAP = 0.14

modules = [
    ('Project',        GREEN,    ['WBS Structure', 'Task Hierarchy', 'Project Metadata', 'Billing Setup'],     CST_X0+0.18, CONT_Y0+MOD_H+MOD_GAP+0.06),
    ('Org Keys',       TEAL,     ['Org Keys', 'Account Codes', 'Cost Pools'],                                  CST_X0+0.18+MOD_W+MOD_GAP, CONT_Y0+MOD_H+MOD_GAP+0.06),
    ('Revenue Config', BLUE_MID, ['Revenue Config', 'Billing Notes', 'Fee Parameters'],                        CST_X0+0.18, CONT_Y0+0.06),
    ('Funding',        NAVY,     ['Funding Profraction', 'Ceiling Amounts', 'Period Budgets'],                  CST_X0+0.18+MOD_W+MOD_GAP, CONT_Y0+0.06),
]

for mod_name, mod_color, mod_items, mx, my in modules:
    frect(mx, my, MOD_W, MOD_H, CARD2, mod_color, lw=1.2, pad=0.05, z=4)
    hdr(mx, my+MOD_H-0.30, MOD_W, 0.30, mod_color, mod_name, fsize=6.8)
    for k, itm in enumerate(mod_items):
        item_row(mx+0.08, my+MOD_H-0.44-k*0.38, MOD_W-0.16, itm, mod_color)

# ─── FLOW ARROWS between panels ───────────────────────────────────────────────
CRM_MID_Y  = (CRM_Y0 + CRM_Y1) / 2
DYN_MID_Y  = (DYN_Y0 + DYN_Y1) / 2

# Contract Data box — inside source panel, clear of Boomi bullets
CD_X  = SRC_X1 - 0.52          # split difference between original and moved-left position
CD_W  = 0.88
CD_CX = CD_X + CD_W / 2

CD_Y = (CRM_Y0 + DYN_Y1) / 2   # overlap point between the two source boxes
ax.add_patch(FancyBboxPatch((CD_X, CD_Y-0.22), CD_W, 0.44,
    boxstyle='round,pad=0.05', facecolor=CARD, edgecolor=BLUE_MID,
    lw=1.0, alpha=0.95, zorder=6))
ax.text(CD_CX, CD_Y, 'Contract\nData',
    ha='center', va='center', fontsize=6.2, color=BLUE_MID,
    fontweight='bold', zorder=7)


# Contract API / JWT gateway — moved down to clear Billing Setup item
JWT_Y = 3.45
arr(BOM_X1+0.02, JWT_Y, CST_X0-0.02, JWT_Y, GREEN, lw=2.2, z=5)
ax.add_patch(FancyBboxPatch((BOM_X1+0.04, JWT_Y-0.22), 0.88, 0.44,
    boxstyle='round,pad=0.05', facecolor=CARD, edgecolor=GREEN, lw=1.0, alpha=0.95, zorder=6))
ax.text(BOM_X1+0.48, JWT_Y, 'Contract\nAPI / JWT',
    ha='center', va='center', fontsize=6.2, color=GREEN,
    fontweight='bold', zorder=7)

# ═══════════════════════════════════════════════════════════════════════════════
# ROLES FOOTNOTE — thin strip at bottom
# ═══════════════════════════════════════════════════════════════════════════════
ax.add_patch(plt.Rectangle((0, 0.06), FW, FOOT_H,
    facecolor=NAVY, alpha=0.88, zorder=8))
ax.text(0.50, 0.06+FOOT_H/2, 'KEY ROLES:', color=BLUE_LIGHT,
    fontsize=6.2, fontweight='bold', ha='left', va='center', zorder=9)

roles = [
    (BLUE_LIGHT, 'SA', 'Solution Architect',     'Platform design & integration patterns'),
    (CORAL,      'ID', 'Integration Developer',   'Process builds, APIs & event subscriptions'),
    (TEAL,       'DE', 'Data Engineer',           'Field mapping, WBS schemas & transformation'),
    (GRAY_L,     'PM', 'Program Manager',         'Milestone oversight & contract activations'),
    (SLATE,      'BA', 'Boomi Administrator',     'Runtime health, runtime ops & platform governance'),
]
role_spacing = (FW - 2.60) / len(roles)
for i, (color, initials, name, desc) in enumerate(roles):
    rx = 2.60 + i * role_spacing
    ry = 0.06 + FOOT_H/2
    circ(rx+0.14, ry, 0.12, color, 'white', 1, z=9)
    ax.text(rx+0.14, ry, initials, ha='center', va='center',
        fontsize=5.0, color=NAVY, fontweight='bold', zorder=10)
    ax.text(rx+0.35, ry+0.06, name, ha='left', va='center',
        fontsize=6.0, color=WHITE, fontweight='bold', zorder=9)
    ax.text(rx+0.35, ry-0.10, desc, ha='left', va='center',
        fontsize=5.2, color=BLUE_LIGHT, alpha=0.85, zorder=9)

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
output_path = ('/mnt/c/users/BrianMerrick/Documents/Dev/ClaudeCode/'
               'boomicompanion_template_workspace/business-demo/contract-lifecycle-management/'
               'boomi-govcon-integration.png')
plt.savefig(output_path, bbox_inches='tight', dpi=180,
    facecolor=BG, edgecolor='none', format='png')
plt.close(fig)
print(f'Saved: {output_path}')
