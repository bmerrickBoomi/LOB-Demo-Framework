#!/usr/bin/env python3.11
"""
Boomi Value Based Demo Framework — Logo Generator
Hexagonal emblem with node network + Boomi brand typography.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

# ─── Figure ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('#0f172a')
ax.set_facecolor('#0f172a')
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_aspect('equal')

# ─── Palette ───────────────────────────────────────────────────
EMBLEM_BG = '#160d2e'
PURPLE    = '#7c3aed'
PURPLE_L  = '#a78bfa'
PURPLE_LL = '#c4b5fd'
WHITE     = '#ffffff'

# ─── Emblem (left half) ────────────────────────────────────────
cx, cy = 3.5, 3.5

# Glow halos behind hex
for r, a in [(3.1, 0.04), (2.7, 0.07), (2.2, 0.06)]:
    ax.add_patch(Circle((cx, cy), r, fc=PURPLE, ec='none', alpha=a, zorder=1))

# Hexagon body (flat-top orientation)
hex_r = 2.4
angles = np.linspace(np.pi / 6, 2 * np.pi + np.pi / 6, 7)
hx = cx + hex_r * np.cos(angles)
hy = cy + hex_r * np.sin(angles)
ax.fill(hx, hy, facecolor=EMBLEM_BG, edgecolor=PURPLE, linewidth=2.8, zorder=2)

# Inner ring decoration
inner_r = 1.92
ax.plot(cx + inner_r * np.cos(angles), cy + inner_r * np.sin(angles),
        color=PURPLE, lw=0.9, alpha=0.45, zorder=3)

# Vertex accent dots
for a in angles[:-1]:
    ax.add_patch(Circle((cx + hex_r * np.cos(a), cy + hex_r * np.sin(a)),
                         0.13, fc=PURPLE, ec='none', zorder=3))

# ─── Node network (triangle + center) ─────────────────────────
nodes = {
    't':  (cx,       cy + 1.2),
    'bl': (cx - 1.05, cy - 0.6),
    'br': (cx + 1.05, cy - 0.6),
    'c':  (cx,        cy),
}
pairs = [('t', 'bl'), ('t', 'br'), ('bl', 'br'),
         ('t', 'c'),  ('bl', 'c'), ('br', 'c')]

for a, b in pairs:
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]
    ax.plot([x1, x2], [y1, y2], color=PURPLE_L, lw=2.0, alpha=0.55, zorder=4)

for key, (nx, ny) in nodes.items():
    center = key == 'c'
    r = 0.34 if center else 0.21
    ax.add_patch(Circle((nx, ny), r * 2.4, fc=PURPLE, ec='none', alpha=0.18, zorder=4))
    ax.add_patch(Circle((nx, ny), r,
                         fc=WHITE if center else PURPLE_LL,
                         ec=PURPLE, lw=2.0, zorder=5))

# ─── Text block (right half) ───────────────────────────────────
tx = 6.85
ty = 3.85

# Left accent bar
ax.add_patch(plt.Rectangle((tx - 0.2, ty - 1.15), 0.08, 2.3,
                             fc=PURPLE, zorder=4))

# "BOOMI"
ax.text(tx + 0.2, ty + 0.3, 'BOOMI',
        color=WHITE, fontsize=60, fontweight='bold',
        ha='left', va='center', zorder=5, family='sans-serif')

# Horizontal separator
ax.plot([tx + 0.2, 13.8], [ty - 0.42, ty - 0.42], color=PURPLE, lw=2.0, zorder=4)

# Subtitle — extra word spacing for elegance
ax.text(tx + 0.2, ty - 1.05,
        'BUSINESS  FOCUSED  DEMO  FRAMEWORK',
        color=PURPLE_L, fontsize=12.5, fontweight='bold',
        ha='left', va='center', zorder=5, family='sans-serif')

# ─── Save ──────────────────────────────────────────────────────
output_path = ('/mnt/c/users/BrianMerrick/Documents/Dev/ClaudeCode/'
               'boomicompanion_template_workspace/business-demo/hr/boomi-vbdf-logo.png')

plt.savefig(output_path, bbox_inches='tight', dpi=150,
            facecolor='#0f172a', edgecolor='none', format='png')
plt.close(fig)
print(f'Saved: {output_path}')
