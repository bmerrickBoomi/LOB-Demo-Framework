#!/usr/bin/env python3.11
"""
Boomi Value Based Demo Framework — Logo Generator
Hexagonal emblem with node network + Boomi brand typography.
Brand colors sourced from Boomi official palette (Brandfetch).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

# ─── Figure ────────────────────────────────────────────────────
BG_COLOR = '#061C3C'   # deep Boomi navy background
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_aspect('equal')

# ─── Palette (official Boomi brand colors) ─────────────────────
EMBLEM_BG  = '#082B55'   # Madison — dark navy
BOOMI_BLUE = '#083F69'   # Boomi primary blue
BLUE_MID   = '#1A6BA0'   # mid blue for edges / connections
BLUE_LIGHT = '#4DB8E8'   # light blue — node highlights
CORAL      = '#FF7C66'   # Boomi coral/salmon accent
WHITE      = '#FFFFFF'

# ─── Emblem (left half) ────────────────────────────────────────
cx, cy = 3.5, 3.5

# Glow halos behind hex
for r, a in [(3.1, 0.05), (2.7, 0.09), (2.2, 0.07)]:
    ax.add_patch(Circle((cx, cy), r, fc=BOOMI_BLUE, ec='none', alpha=a, zorder=1))

# Hexagon body (flat-top orientation)
hex_r = 2.4
angles = np.linspace(np.pi / 6, 2 * np.pi + np.pi / 6, 7)
hx = cx + hex_r * np.cos(angles)
hy = cy + hex_r * np.sin(angles)
ax.fill(hx, hy, facecolor=EMBLEM_BG, edgecolor=BOOMI_BLUE, linewidth=2.8, zorder=2)

# Inner ring decoration
inner_r = 1.92
ax.plot(cx + inner_r * np.cos(angles), cy + inner_r * np.sin(angles),
        color=BLUE_MID, lw=0.9, alpha=0.5, zorder=3)

# Vertex accent dots — coral for brand pop
for a in angles[:-1]:
    ax.add_patch(Circle((cx + hex_r * np.cos(a), cy + hex_r * np.sin(a)),
                         0.13, fc=CORAL, ec='none', zorder=3))

# ─── Node network (triangle + center) ─────────────────────────
nodes = {
    't':  (cx,        cy + 1.2),
    'bl': (cx - 1.05, cy - 0.6),
    'br': (cx + 1.05, cy - 0.6),
    'c':  (cx,        cy),
}
pairs = [('t', 'bl'), ('t', 'br'), ('bl', 'br'),
         ('t', 'c'),  ('bl', 'c'), ('br', 'c')]

for a, b in pairs:
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]
    ax.plot([x1, x2], [y1, y2], color=BLUE_LIGHT, lw=2.0, alpha=0.55, zorder=4)

for key, (nx, ny) in nodes.items():
    center = key == 'c'
    r = 0.34 if center else 0.21
    ax.add_patch(Circle((nx, ny), r * 2.4, fc=BOOMI_BLUE, ec='none', alpha=0.2, zorder=4))
    ax.add_patch(Circle((nx, ny), r,
                         fc=CORAL if center else BLUE_LIGHT,
                         ec=BLUE_MID, lw=2.0, zorder=5))

# ─── Text block (right half) ───────────────────────────────────
tx = 6.85
ty = 3.85

# Left accent bar — coral for brand alignment
ax.add_patch(plt.Rectangle((tx - 0.2, ty - 1.15), 0.08, 2.3,
                             fc=CORAL, zorder=4))

# "BOOMI"
ax.text(tx + 0.2, ty + 0.3, 'BOOMI',
        color=WHITE, fontsize=60, fontweight='bold',
        ha='left', va='center', zorder=5, family='sans-serif')

# Horizontal separator — Boomi blue
ax.plot([tx + 0.2, 13.8], [ty - 0.42, ty - 0.42], color=BOOMI_BLUE, lw=2.0, zorder=4)

# Subtitle — light blue, consistent with brand palette
ax.text(tx + 0.2, ty - 1.05,
        'BUSINESS  FOCUSED  DEMO  FRAMEWORK',
        color=BLUE_LIGHT, fontsize=12.5, fontweight='bold',
        ha='left', va='center', zorder=5, family='sans-serif')

# ─── Save ──────────────────────────────────────────────────────
output_path = ('/mnt/c/users/BrianMerrick/Documents/Dev/ClaudeCode/'
               'boomicompanion_template_workspace/business-demo/boomi/boomi-vbdf-logo.png')

plt.savefig(output_path, bbox_inches='tight', dpi=150,
            facecolor=BG_COLOR, edgecolor='none', format='png')
plt.close(fig)
print(f'Saved: {output_path}')
