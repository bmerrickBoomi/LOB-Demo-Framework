#!/usr/bin/env python3.11
"""
HR Operations Console — IT Visual Walkthrough
Generates a visually rich architecture flow diagram as PNG.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patheffects as pe
import numpy as np
import subprocess

# ─── Figure setup ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(22, 14))
fig.patch.set_facecolor('#0f172a')
ax.set_facecolor('#0f172a')
ax.set_xlim(0, 22)
ax.set_ylim(0, 14)
ax.axis('off')
ax.set_aspect('equal')

# ─── Helper functions ──────────────────────────────────────────────────────────
def fancy_rect(x, y, w, h, fc, ec, lw=1.5, pad=0.12, zorder=2):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={pad}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder
    )
    ax.add_patch(patch)
    return patch

def circle(cx, cy, r, fc, ec='white', lw=1, zorder=5):
    c = Circle((cx, cy), r, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder)
    ax.add_patch(c)
    return c

def step_badge(cx, cy, label, color, size=10, zorder=10):
    circle(cx, cy, 0.28, color, 'white', 1.5, zorder=zorder)
    ax.text(cx, cy, str(label), color='white', fontsize=size,
            fontweight='bold', ha='center', va='center', zorder=zorder+1)

def arrow_between(x1, y1, x2, y2, color, lw=2.5, style='->', ls='solid', zorder=4,
                  connectionstyle='arc3,rad=0'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle=style,
                    color=color,
                    lw=lw,
                    linestyle=ls,
                    connectionstyle=connectionstyle,
                ),
                zorder=zorder)

# ═══════════════════════════════════════════════════════════════════════════════
# SWIM LANE DIVIDERS
# ═══════════════════════════════════════════════════════════════════════════════
ax.axhline(8.3, xmin=0.018, xmax=0.99, color='#334155', lw=1, ls='--', zorder=1)
ax.axhline(4.0, xmin=0.018, xmax=0.99, color='#334155', lw=1, ls='--', zorder=1)

# Swim lane background tints
ax.add_patch(plt.Rectangle((0.4, 8.3), 21.1, 5.4, facecolor='#0f172a', alpha=0.0, zorder=0))

# Swim lane labels (vertical text)
ax.text(0.2, 10.0, 'USER LAYER', color='#2563eb', fontsize=8, fontweight='bold',
        rotation=90, ha='center', va='center', zorder=3)
ax.text(0.2, 6.15, 'BOOMI PLATFORM', color='#7c3aed', fontsize=8, fontweight='bold',
        rotation=90, ha='center', va='center', zorder=3)
ax.text(0.2, 2.3, 'HR SYSTEMS', color='#d97706', fontsize=8, fontweight='bold',
        rotation=90, ha='center', va='center', zorder=3)

# ═══════════════════════════════════════════════════════════════════════════════
# TITLE & SUBTITLE
# ═══════════════════════════════════════════════════════════════════════════════
ax.text(11, 13.55, 'HR Operations Console — IT Visual Walkthrough',
        color='white', fontsize=18, fontweight='bold', ha='center', va='center', zorder=5)
ax.text(11, 13.1, 'Follow the numbered steps to understand the full request/response lifecycle',
        color='#94a3b8', fontsize=10, ha='center', va='center', zorder=5)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT A — "Sarah" the HR User
# ═══════════════════════════════════════════════════════════════════════════════

# Person figure
circle(1.5, 11.2, 0.35, '#2563eb', 'white', 1.5, zorder=5)  # head
# Body
ax.plot([1.5, 1.5], [10.85, 10.0], color='#93c5fd', lw=2.5, zorder=4)
# Arms
ax.plot([1.0, 1.5, 2.0], [10.0, 10.5, 10.0], color='#93c5fd', lw=2.5, zorder=4)
# Legs
ax.plot([1.5, 1.1], [10.0, 9.3], color='#93c5fd', lw=2.5, zorder=4)
ax.plot([1.5, 1.9], [10.0, 9.3], color='#93c5fd', lw=2.5, zorder=4)

# Name label
ax.text(1.5, 9.15, 'Sarah Reynolds', color='white', fontsize=11,
        fontweight='bold', ha='center', va='center', zorder=5)
ax.text(1.5, 8.78, 'HR Business Partner', color='#94a3b8', fontsize=9,
        ha='center', va='center', zorder=5)

# Desk/laptop rect
fancy_rect(0.8, 9.0, 1.4, 0.25, '#1e293b', '#334155', lw=1, pad=0.05, zorder=3)

# Step badge 1
step_badge(0.6, 11.8, '1', '#2563eb', size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT B — Browser / SPA
# ═══════════════════════════════════════════════════════════════════════════════

# Outer browser window
fancy_rect(2.9, 8.6, 3.1, 3.5, '#1e293b', '#334155', lw=2, pad=0.08, zorder=3)

# Chrome bar
ax.add_patch(plt.Rectangle((2.9, 11.7), 3.1, 0.4, facecolor='#334155', zorder=4))

# Browser dots
circle(3.1, 11.9, 0.07, '#ef4444', 'none', 0, zorder=5)
circle(3.3, 11.9, 0.07, '#f59e0b', 'none', 0, zorder=5)
circle(3.5, 11.9, 0.07, '#22c55e', 'none', 0, zorder=5)

# URL bar
fancy_rect(3.6, 11.75, 2.2, 0.25, '#0f172a', '#475569', lw=1, pad=0.03, zorder=5)
ax.text(4.7, 11.875, 'hr-operations-console.html', color='#94a3b8', fontsize=6.5,
        ha='center', va='center', zorder=6)

# Left sidebar
ax.add_patch(plt.Rectangle((2.9, 8.6), 0.5, 3.1, facecolor='#0f172a', zorder=4))
# Nav items
for yi in [11.3, 11.0, 10.7, 10.4, 10.1]:
    ax.plot([2.95, 3.35], [yi, yi], color='#334155', lw=2, zorder=5)

# Main content area
ax.add_patch(plt.Rectangle((3.4, 8.6), 2.6, 3.1, facecolor='#0f172a', zorder=4))

# 3 KPI cards
kpi_positions = [3.5, 4.1, 4.7]
for kx in kpi_positions:
    fancy_rect(kx, 11.0, 0.45, 0.5, '#1e293b', '#334155', lw=1, pad=0.04, zorder=5)

# Right AI panel
ax.add_patch(FancyBboxPatch((5.5, 8.6), 0.5, 3.1,
    boxstyle="round,pad=0.05", facecolor='#162032', edgecolor='#2563eb', lw=1, zorder=5))
ax.text(5.75, 10.5, 'AI\nCopilot', color='white', fontsize=6,
        ha='center', va='center', zorder=6)

# Browser labels
ax.text(4.45, 8.38, 'HR Operations Console', color='white', fontsize=11,
        fontweight='bold', ha='center', va='center', zorder=5)
ax.text(4.45, 8.1, 'Embeddable Agent', color='#94a3b8', fontsize=9,
        ha='center', va='center', zorder=5)

# Step badge 2
step_badge(3.0, 12.3, '2', '#2563eb', size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT C — HTTP POST Arrow (browser → Boomi)
# ═══════════════════════════════════════════════════════════════════════════════

# Curved arrow from browser bottom-right down to Boomi Runtime
ax.annotate('', xy=(7.5, 7.8), xytext=(5.5, 8.6),
            arrowprops=dict(
                arrowstyle='->', color='#7c3aed', lw=3,
                connectionstyle='arc3,rad=-0.3',
            ), zorder=6)

ax.text(7.05, 8.52, 'POST /ws/rest/v1/HR/hrOpsStatus', color='#c4b5fd', fontsize=7.5,
        ha='center', va='center', rotation=-18, zorder=7,
        bbox=dict(boxstyle='round,pad=0.15', facecolor='#0f172a', edgecolor='none', alpha=0.75))
ax.text(6.6, 7.99, '{ "question": "..." }', color='#a78bfa', fontsize=7,
        ha='center', va='center', rotation=-18, zorder=7)

# Step badge 3 (consolidated: HTTP POST arrow + Boomi Runtime)
step_badge(5.85, 7.75, '3', '#7c3aed', size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT D — Boomi Runtime (center, middle row)
# ═══════════════════════════════════════════════════════════════════════════════

# Outer server rack
fancy_rect(6.6, 4.6, 3.2, 3.0, '#1e293b', '#7c3aed', lw=2.5, pad=0.1, zorder=3)

# Header bar
ax.add_patch(plt.Rectangle((6.6, 7.2), 3.2, 0.4, facecolor='#7c3aed', zorder=4))
ax.text(8.2, 7.4, 'BOOMI RUNTIME', color='white', fontsize=10,
        fontweight='bold', ha='center', va='center', zorder=5)

# Server rack units
rack_y = [6.6, 6.1, 5.6]
rack_labels = ['HTTP Listener', 'Process Router', 'Agent Connector']
status_y = [6.79, 6.29, 5.79]

for ry, rl, sy in zip(rack_y, rack_labels, status_y):
    ax.add_patch(plt.Rectangle((6.8, ry), 2.8, 0.38, facecolor='#0f172a', edgecolor='#334155', lw=1, zorder=4))
    # Status LED
    circle(6.95, sy, 0.07, '#22c55e', 'none', 0, zorder=5)
    # Small activity bars
    for bx, bh in [(7.15, 0.15), (7.3, 0.22), (7.45, 0.1)]:
        ax.add_patch(plt.Rectangle((bx, sy - bh/2), 0.1, bh, facecolor='#7c3aed', alpha=0.7, zorder=5))
    ax.text(8.2, sy, rl, color='#94a3b8', fontsize=8, ha='center', va='center', zorder=5)


# Labels below
ax.text(8.2, 4.3, 'Boomi Runtime', color='white', fontsize=11,
        fontweight='bold', ha='center', va='center', zorder=5)
ax.text(8.2, 4.02, 'Scalable Runtime', color='#94a3b8', fontsize=9,
        ha='center', va='center', zorder=5)


# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT E — Arrow: Boomi Runtime → Agent Garden
# ═══════════════════════════════════════════════════════════════════════════════

arrow_between(10.0, 6.15, 11.2, 6.15, '#7c3aed', lw=3, zorder=6)
ax.text(10.6, 6.5, 'Agent Garden\nAPI', color='#c4b5fd', fontsize=8,
        ha='center', va='center', zorder=7)

step_badge(10.6, 7.2, '4', '#7c3aed', size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT F — Boomi Agent Garden
# ═══════════════════════════════════════════════════════════════════════════════

# Outer rounded rect
fancy_rect(11.3, 4.1, 4.5, 3.5, '#1e293b', '#16a34a', lw=2.5, pad=0.1, zorder=3)

# Header bar
ax.add_patch(plt.Rectangle((11.3, 7.2), 4.5, 0.4, facecolor='#16a34a', zorder=4))
ax.text(13.55, 7.4, 'BOOMI AGENT GARDEN', color='white', fontsize=10,
        fontweight='bold', ha='center', va='center', zorder=5)

# Robot/AI icon
# Robot head
ax.add_patch(FancyBboxPatch((11.6, 6.3), 0.7, 0.6,
    boxstyle="round,pad=0.04", facecolor='#0f172a', edgecolor='#22c55e', lw=2, zorder=5))
# Robot eyes
circle(11.82, 6.65, 0.07, '#22c55e', 'none', 0, zorder=6)
circle(12.12, 6.65, 0.07, '#22c55e', 'none', 0, zorder=6)
# Robot antenna
ax.plot([11.95, 11.95], [6.9, 7.1], color='#22c55e', lw=1.5, zorder=6)
circle(11.95, 7.12, 0.05, '#22c55e', 'none', 0, zorder=6)
# Robot body
ax.add_patch(FancyBboxPatch((11.65, 5.7), 0.6, 0.55,
    boxstyle="round,pad=0.04", facecolor='#0f172a', edgecolor='#22c55e', lw=1.5, zorder=5))
# Robot arms
ax.plot([11.65, 11.4], [5.9, 5.7], color='#22c55e', lw=2, zorder=5)
ax.plot([12.25, 12.5], [5.9, 5.7], color='#22c55e', lw=2, zorder=5)
# Robot legs
ax.plot([11.75, 11.65], [5.7, 5.4], color='#22c55e', lw=2, zorder=5)
ax.plot([12.15, 12.25], [5.7, 5.4], color='#22c55e', lw=2, zorder=5)

# Agent info text
ax.text(13.55, 6.55, 'HR Ops Console Agent', color='white', fontsize=9,
        fontweight='bold', ha='center', va='center', zorder=5)
ax.text(13.55, 6.25, 'ID: 8cadcf3c-e97e-4f20...', color='#94a3b8', fontsize=7,
        ha='center', va='center', zorder=5)
ax.text(13.55, 5.95, 'Mode: Structured', color='#4ade80', fontsize=8,
        ha='center', va='center', zorder=5)

# Tool badges grid
tool_labels = [
    ['Get Dashboard', 'Get Employees', 'Get Cases'],
    ['Create Case', 'Get Compliance', 'Get Integrations'],
    ['Get Tasks', 'Get Notifs', 'Get Audit Log'],
]
tool_y = [5.45, 5.0, 4.55]
tool_x = [11.5, 13.0, 14.5]

for row_idx, (ry, row) in enumerate(zip(tool_y, tool_labels)):
    for col_idx, (rx, label) in enumerate(zip(tool_x, row)):
        ax.add_patch(FancyBboxPatch((rx, ry), 1.3, 0.33,
            boxstyle="round,pad=0.04", facecolor='#0f172a', edgecolor='#16a34a', lw=1, zorder=5))
        ax.text(rx + 0.65, ry + 0.165, label, color='#4ade80', fontsize=6.5,
                ha='center', va='center', zorder=6)

# Labels below
ax.text(13.55, 3.85, 'Agent Garden', color='white', fontsize=11,
        fontweight='bold', ha='center', va='center', zorder=5)
ax.text(13.55, 3.59, '9 OpenAPI Tools • Structured Mode', color='#94a3b8', fontsize=9,
        ha='center', va='center', zorder=5)

# Step badge 5
step_badge(11.4, 7.95, '5', '#16a34a', size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT G — Arrow down: Agent Garden → HR Systems
# ═══════════════════════════════════════════════════════════════════════════════

arrow_between(11.8, 4.1, 11.8, 3.5, '#d97706', lw=2.5, zorder=6)
ax.text(14.8, 3.78, 'Data Sources', color='#fbbf24', fontsize=8,
        ha='left', va='center', zorder=7)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT H — HR Systems (bottom row)
# ═══════════════════════════════════════════════════════════════════════════════

# Outer container
fancy_rect(7.1, 1.1, 12.0, 2.2, '#1e293b', '#d97706', lw=2, pad=0.1, zorder=3)
ax.text(13.1, 3.05, 'HR SYSTEMS (Mock Data via Agent Tools)', color='#fbbf24',
        fontsize=9, fontweight='bold', ha='center', va='center', zorder=5)

# System boxes config
systems = [
    {'x': 7.4,  'label': 'W', 'name': 'Workday\nHRIS',      'lc': '#e05a00', 'tc': '#e05a00'},
    {'x': 9.5,  'label': 'A', 'name': 'ADP\nPayroll',       'lc': '#cc0000', 'tc': '#cc0000'},
    {'x': 11.6, 'label': 'B', 'name': 'Benefitfocus',       'lc': '#2563eb', 'tc': '#2563eb'},
    {'x': 13.7, 'label': 'L', 'name': 'Lattice',            'lc': '#7c3aed', 'tc': '#7c3aed'},
    {'x': 15.8, 'label': 'G', 'name': 'Glint',              'lc': '#16a34a', 'tc': '#16a34a'},
]

for s in systems:
    # System box
    ax.add_patch(FancyBboxPatch((s['x'], 1.3), 1.8, 1.4,
        boxstyle="round,pad=0.06", facecolor='#0f172a', edgecolor=s['lc'], lw=1.5, zorder=4))
    # Big letter
    ax.text(s['x'] + 0.9, 2.2, s['label'], color=s['tc'], fontsize=22,
            fontweight='bold', ha='center', va='center', zorder=5)
    # System name
    ax.text(s['x'] + 0.9, 1.55, s['name'], color='#94a3b8', fontsize=7.5,
            ha='center', va='center', zorder=5)

# Step badge 6
step_badge(7.3, 3.3, '6', '#d97706', size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT I — Response path (return arrows) steps 8 & 9
# ═══════════════════════════════════════════════════════════════════════════════

# Draw multi-segment return path using PathPatch
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path

# Segment 1: Agent Garden right side → go right
ax.annotate('', xy=(17.0, 6.15), xytext=(16.0, 6.15),
            arrowprops=dict(arrowstyle='-', color='#22c55e', lw=2.5, linestyle='dashed'), zorder=6)
# Segment 2: go up
ax.annotate('', xy=(17.0, 10.5), xytext=(17.0, 6.15),
            arrowprops=dict(arrowstyle='-', color='#22c55e', lw=2.5, linestyle='dashed'), zorder=6)
# Segment 3: go left
ax.annotate('', xy=(6.2, 10.5), xytext=(17.0, 10.5),
            arrowprops=dict(arrowstyle='-', color='#22c55e', lw=2.5, linestyle='dashed'), zorder=6)
# Segment 4: go down to AI panel with arrowhead
ax.annotate('', xy=(5.85, 10.0), xytext=(6.2, 10.5),
            arrowprops=dict(arrowstyle='->', color='#22c55e', lw=2.5, linestyle='dashed'), zorder=6)

# JSON response label along top segment
ax.text(11.5, 10.82, '{ "success": true, "data": { "answer": "..." } }',
        color='#4ade80', fontsize=8, ha='center', va='center', zorder=7,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#0f172a', edgecolor='none', alpha=0.8))

# Step badges 7 and 8
step_badge(17.2, 8.5, '7', '#16a34a', size=10)
step_badge(10.5, 11.5, '8', '#16a34a', size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT J — Final display in AI panel
# ═══════════════════════════════════════════════════════════════════════════════

# Chat bubble in AI panel
ax.add_patch(FancyBboxPatch((5.5, 9.2), 0.45, 0.8,
    boxstyle="round,pad=0.05", facecolor='#16a34a', edgecolor='none', zorder=7))
ax.text(5.725, 9.6, 'Answer', color='white', fontsize=5.5,
        ha='center', va='center', zorder=8)

# Connected badge
ax.add_patch(FancyBboxPatch((5.35, 9.05), 0.65, 0.15,
    boxstyle="round,pad=0.02", facecolor='#15803d', edgecolor='none', zorder=7))
ax.text(5.675, 9.125, 'Boomi AI Connected', color='white', fontsize=4.5,
        ha='center', va='center', zorder=8)

# Final step badge (checkmark)
circle(5.3, 12.45, 0.32, '#16a34a', 'white', 1.5, zorder=9)
ax.text(5.3, 12.45, '✓', color='white', fontsize=11,
        fontweight='bold', ha='center', va='center', zorder=10)
ax.text(5.3, 12.0, 'FINAL', color='#4ade80', fontsize=7,
        ha='center', va='center', zorder=9)

# ═══════════════════════════════════════════════════════════════════════════════
# LEGEND (bottom left)
# ═══════════════════════════════════════════════════════════════════════════════

legend_x, legend_y = 0.5, 0.3
ax.text(legend_x, legend_y + 0.65, 'LEGEND', color='white', fontsize=8,
        fontweight='bold', ha='left', va='center', zorder=5)

legend_items = [
    ('#2563eb', 'Browser / User'),
    ('#7c3aed', 'Boomi Runtime'),
    ('#16a34a', 'Agent Garden'),
    ('#d97706', 'HR Systems'),
]
for i, (color, label) in enumerate(legend_items):
    lx = legend_x + i * 2.4
    circle(lx + 0.12, legend_y + 0.3, 0.1, color, 'white', 1, zorder=5)
    ax.text(lx + 0.3, legend_y + 0.3, label, color='#94a3b8', fontsize=7,
            ha='left', va='center', zorder=5)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

ax.text(11, 0.15,
        'Boomi Runtime must be running at localhost:8077  •  Auth: Basic  •  '
        'Agent ID: 8cadcf3c-e97e-4f20-aa0d-82153cb2a6af',
        color='#475569', fontsize=7, ha='center', va='center', zorder=5)

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════

output_path = ('/mnt/c/users/BrianMerrick/Documents/Dev/ClaudeCode/'
               'boomicompanion_template_workspace/business-demo/hr-ops-it-visual.png')

plt.savefig(output_path, bbox_inches='tight', dpi=150, facecolor='#0f172a',
            edgecolor='none', format='png')
plt.close(fig)

# Resize to 1920x1080 (16:9) with dark background padding to match Google Slides
subprocess.run([
    'convert', output_path,
    '-resize', '1920x1080',
    '-background', '#0f172a',
    '-gravity', 'center',
    '-extent', '1920x1080',
    output_path
], check=True)

print(f"Saved to: {output_path} (1920x1080, 16:9)")
