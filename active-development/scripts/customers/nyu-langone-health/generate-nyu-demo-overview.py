"""
NYU Langone Health — Employee Onboarding Orchestration Flow Diagram
=====================================================================
Reflects current nyu-onboarding-orchestration process structure:

Stage 1 (linear):
  Salesforce (New Hire Query)
  → Map + Enrich (set DDP: BenefitsEligible)
  → 2-way Branch

Stage 2 (conditional routing):
  Branch path 2 (always): Oracle Audit Log (HIPAA compliance)
  Branch path 1 → Decision: BenefitsEligible?
    True  → Branch → Workday HCM Worker Record
                    → Benefits Vendor Enrollment CSV
    False → ServiceNow IT Onboarding Ticket

Requirements:
    pip install Pillow

Fonts expected at /tmp/Poppins-{style}.ttf
Boomi logo expected at /tmp/boomi-logo2.png

Run:
    python3 generate-nyu-demo-overview.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── OUTPUT ───────────────────────────────────────────────────────────────────

OUTPUT_FILE = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../../../..",
                 "business-demo/customers/nyu-langone-health/nyu-demo-overview.png")
)
SCALE        = 2                        # render at 2× for crisp display in Google Slides
WIDTH, HEIGHT = 1600 * SCALE, 900 * SCALE
FONT_DIR  = "/tmp"
LOGO_PATH = "/tmp/boomi-logo2.png"

# ── COLORS ───────────────────────────────────────────────────────────────────

BG_TOP      = (38,  35,  68)
BG_BOTTOM   = (52,  46,  90)
NYU_PURPLE  = "#57068C"
DIVIDER     = "#4A4A72"
TEXT_MAIN   = "#FFFFFF"
TEXT_SUB    = "#D0D0F0"
TEXT_MUTED  = "#B8B8D8"
CONNECTOR   = "#9898C8"

# Connector brand colors
C_SALESFORCE = "#0176D3"
C_MAP        = "#7C3FF5"
C_ORACLE     = "#C74634"
C_WORKDAY    = "#F66B2B"
C_FTP        = "#00C4CC"
C_SERVICENOW = "#62D84E"
C_DECISION   = "#E8E8FF"

# ── HELPERS ──────────────────────────────────────────────────────────────────

def font(style, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, f"Poppins-{style}.ttf"), size)

def tsz(draw, text, f):
    return draw.textsize(text, font=f)

def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rr(draw, xy, r, fill=None, outline=None, lw=1):
    """Rounded rectangle compatible with Pillow 7."""
    x0, y0, x1, y1 = xy
    if fill:
        draw.rectangle([x0+r, y0, x1-r, y1], fill=fill)
        draw.rectangle([x0, y0+r, x1, y1-r], fill=fill)
        for ex, ey in [(x0,y0),(x1-2*r,y0),(x0,y1-2*r),(x1-2*r,y1-2*r)]:
            draw.ellipse([ex, ey, ex+2*r, ey+2*r], fill=fill)
    if outline:
        draw.arc([x0,    y0,    x0+2*r, y0+2*r], 180, 270, fill=outline, width=lw)
        draw.arc([x1-2*r,y0,    x1,     y0+2*r], 270, 360, fill=outline, width=lw)
        draw.arc([x0,    y1-2*r,x0+2*r, y1    ], 90,  180, fill=outline, width=lw)
        draw.arc([x1-2*r,y1-2*r,x1,     y1    ], 0,   90,  fill=outline, width=lw)
        draw.line([x0+r, y0, x1-r, y0], fill=outline, width=lw)
        draw.line([x0+r, y1, x1-r, y1], fill=outline, width=lw)
        draw.line([x0, y0+r, x0, y1-r], fill=outline, width=lw)
        draw.line([x1, y0+r, x1, y1-r], fill=outline, width=lw)

def alpha_fill(img, xy, r, color_rgba):
    layer = Image.new("RGBA", img.size, (0,0,0,0))
    rr(ImageDraw.Draw(layer), xy, r, fill=color_rgba)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

# Arrowhead default sizes scale with SCALE since it's a module-level constant
def arrowhead_right(draw, x, y, color, size=8*SCALE):
    draw.polygon([(x, y), (x-size, y-size//2), (x-size, y+size//2)], fill=color)

def arrowhead_down(draw, x, y, color, size=8*SCALE):
    draw.polygon([(x, y), (x-size//2, y-size), (x+size//2, y-size)], fill=color)

def draw_node(draw, img_ref, x, cy, w, h, color, label, sublabel, f_label, f_sub):
    """Draw a system node box. All coordinates already at SCALE resolution."""
    S = SCALE
    cr, cg, cb = hex_rgb(color)
    ny = cy - h // 2
    img_ref[0] = alpha_fill(img_ref[0], [x, ny, x+w, ny+h], 10*S, (cr, cg, cb, 45))
    d = ImageDraw.Draw(img_ref[0])
    rr(d, [x, ny, x+w, ny+h], 10*S, outline=DIVIDER, lw=S)
    d.rectangle([x, ny+8*S, x+4*S, ny+h-8*S], fill=color)
    ic_cx = x + 24*S
    d.ellipse([ic_cx-13*S, cy-13*S, ic_cx+13*S, cy+13*S], fill=color)
    initial = label[0]
    iw, ih = tsz(d, initial, font("Bold", 13*S))
    d.text((ic_cx - iw//2, cy - ih//2 - S), initial, font=font("Bold", 13*S), fill="#FFFFFF")
    tx = x + 46*S
    lw2, lh2 = tsz(d, label, f_label)
    d.text((tx, cy - lh2 - 2*S), label, font=f_label, fill=TEXT_MAIN)
    d.text((tx, cy + 3*S), sublabel, font=f_sub, fill=TEXT_SUB)
    return d

def draw_pill(draw, img_ref, cx, cy, text, color, f):
    """Draw a connector-type pill. All coordinates already at SCALE resolution."""
    S = SCALE
    cr, cg, cb = hex_rgb(color)
    tw, th = tsz(draw, text, f)
    pw, ph = tw + 18*S, 22*S
    x0, y0 = cx - pw//2, cy - ph//2
    img_ref[0] = alpha_fill(img_ref[0], [x0, y0, x0+pw, y0+ph], 11*S, (cr, cg, cb, 40))
    d = ImageDraw.Draw(img_ref[0])
    rr(d, [x0, y0, x0+pw, y0+ph], 11*S, outline=color, lw=S)
    d.text((x0+9*S, y0+4*S), text, font=f, fill=color)
    return d

def draw_branch_circle(draw, img_ref, cx, cy, r, label, f_stage):
    """Draw a branch circle. cx, cy, r already at SCALE resolution."""
    S = SCALE
    cr, cg, cb = hex_rgb(C_DECISION)
    img_ref[0] = alpha_fill(img_ref[0], [cx-r, cy-r, cx+r, cy+r], r, (cr, cg, cb, 45))
    d = ImageDraw.Draw(img_ref[0])
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=C_DECISION, width=2*S)
    bw, bh = tsz(d, "B", font("Bold", 14*S))
    d.text((cx - bw//2, cy - bh//2 - S), "B", font=font("Bold", 14*S), fill=C_DECISION)
    lw2, _ = tsz(d, label, f_stage)
    d.text((cx - lw2//2, cy + r + 5*S), label, font=f_stage, fill=TEXT_MUTED)
    return d

def wrap_text(draw, text, f, max_w):
    """Word-wrap text to fit within max_w pixels. Returns list of lines."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        w, _ = draw.textsize(test, font=f)
        if w <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_decision_diamond(draw, img_ref, cx, cy, hw, hh, label, sublabel, f_stage, f_sub):
    """Draw a decision diamond. All coordinates already at SCALE resolution."""
    S = SCALE
    pts = [(cx, cy-hh), (cx+hw, cy), (cx, cy+hh), (cx-hw, cy)]
    cr, cg, cb = hex_rgb(C_DECISION)
    img_ref[0] = alpha_fill(img_ref[0],
        [cx-hw, cy-hh, cx+hw, cy+hh], 4*S, (cr, cg, cb, 38))
    d = ImageDraw.Draw(img_ref[0])
    d.polygon(pts, outline=C_DECISION)
    lw2, lh2 = tsz(d, label, f_stage)
    d.text((cx - lw2//2, cy - lh2//2), label, font=f_stage, fill=C_DECISION)
    sw, _ = tsz(d, sublabel, f_sub)
    d.text((cx - sw//2, cy - hh - 18*S), sublabel, font=f_sub, fill=TEXT_MUTED)
    return d

# ── MAIN ──────────────────────────────────────────────────────────────────────

def generate():
    S = SCALE
    W, H = WIDTH, HEIGHT
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Background gradient
    for y in range(H):
        t = y / H
        r = int(BG_TOP[0] + t*(BG_BOTTOM[0]-BG_TOP[0]))
        g = int(BG_TOP[1] + t*(BG_BOTTOM[1]-BG_TOP[1]))
        b = int(BG_TOP[2] + t*(BG_BOTTOM[2]-BG_TOP[2]))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Purple glow — top-left
    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    for i in range(280*S, 0, -4*S):
        a = int(12*(i/(280*S))**2)
        gd.ellipse([-i+120*S, -i+80*S, i+120*S, i+80*S], fill=(87,6,140,a))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Top accent bar
    draw.rectangle([0, 0, W, 5*S], fill=NYU_PURPLE)

    # ── FONTS ────────────────────────────────────────────────────────────────
    f_tag      = font("SemiBold", 12*S)
    f_title    = font("Bold",     36*S)
    f_eyebr    = font("SemiBold", 14*S)
    f_node     = font("SemiBold", 17*S)
    f_nodesb   = font("Regular",  12*S)
    f_stage    = font("SemiBold", 11*S)
    f_dec      = font("SemiBold", 13*S)
    f_footer   = font("SemiBold", 12*S)
    f_badge    = font("SemiBold", 10*S)
    f_card_ttl = font("SemiBold", 15*S)
    f_card_dsc = font("Regular",  13*S)
    f_focus_sec = font("SemiBold", 13*S)

    # ── HEADER ───────────────────────────────────────────────────────────────
    logo_y = 30*S
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
        lh = 32*S; lw = int(logo.width * lh / logo.height)
        logo = logo.resize((lw, lh), Image.LANCZOS)
        img.paste(logo, (60*S, logo_y), logo)
        draw = ImageDraw.Draw(img)
    except FileNotFoundError:
        pass

    nyu_text = "NYU LANGONE HEALTH"
    nw, _ = tsz(draw, nyu_text, f_tag)
    rr(draw, [60*S, 76*S, 60*S+nw+24*S, 76*S+24*S], r=12*S, fill=NYU_PURPLE)
    draw.text((72*S, 82*S), nyu_text, font=f_tag, fill="#FFFFFF")

    title = "Integration Development"
    draw.text((60*S, 112*S), title, font=f_title, fill=TEXT_MAIN)

    proc_text = "nyu-onboarding-orchestration  ·  5 connectors  ·  4 distinct types  ·  0 lines of code"
    draw.text((62*S, 158*S), proc_text, font=f_eyebr, fill=TEXT_SUB)

    draw.line([(60*S, 186*S), (W-60*S, 186*S)], fill=DIVIDER, width=S)

    # ── LAYOUT CONSTANTS (all in SCALE-space pixels) ──────────────────────────
    FLOW_CY     = 430*S

    NODE_W, NODE_H = 200*S, 68*S
    SF_X    = 60*S
    MAP_X   = SF_X + NODE_W + 70*S

    B1_CX   = MAP_X + NODE_W + 80*S
    B1_CY   = FLOW_CY
    B1_R    = 26*S

    VB1_X   = B1_CX + B1_R + 35*S

    ORA_CY  = 290*S
    ORA_X   = VB1_X + 40*S
    ORA_W   = 260*S
    ORA_H   = 68*S

    DEC_CX  = VB1_X + 185*S
    DEC_CY  = FLOW_CY
    DEC_HW  = 52*S
    DEC_HH  = 36*S

    B2_CX   = DEC_CX + DEC_HW + 90*S
    B2_CY   = FLOW_CY
    B2_R    = 26*S

    VB2_X   = B2_CX + B2_R + 40*S

    TRUE_X  = VB2_X + 40*S
    TRUE_W  = 235*S
    TRUE_H  = 64*S
    WD_CY   = FLOW_CY - 108*S
    BEN_CY  = FLOW_CY + 108*S

    SN_CY   = FLOW_CY + 220*S
    SN_X    = DEC_CX - 80*S
    SN_W    = 260*S
    SN_H    = 64*S

    DIV_X   = (MAP_X + NODE_W + B1_CX - B1_R) // 2

    # ── STAGE LABELS ─────────────────────────────────────────────────────────
    S1_MID_X = (SF_X + MAP_X + NODE_W) // 2
    S2_MID_X = (ORA_X + TRUE_X + TRUE_W) // 2

    S1_LABEL_Y = FLOW_CY - NODE_H//2 - 26*S
    S2_LABEL_Y = ORA_CY  - ORA_H//2  - 26*S

    for text, cx, ly in [
        ("STAGE 1  ·  COLLECT & ENRICH",    S1_MID_X, S1_LABEL_Y),
        ("STAGE 2  ·  ROUTE & DELIVER",     S2_MID_X, S2_LABEL_Y),
    ]:
        tw, _ = tsz(draw, text, f_stage)
        draw.text((cx - tw//2, ly), text, font=f_stage, fill=TEXT_MUTED)

    # Stage divider (dashed vertical)
    div_top = min(S1_LABEL_Y, S2_LABEL_Y) - 6*S
    div_bot = H - 52*S
    for y in range(div_top, div_bot, 10*S):
        draw.line([(DIV_X, y), (DIV_X, min(y+5*S, div_bot))], fill=DIVIDER, width=S)

    # ── ROUTING LINES ────────────────────────────────────────────────────────
    LC = CONNECTOR
    LW = 2*S

    # Salesforce → Map
    draw.line([(SF_X+NODE_W+4*S, FLOW_CY), (MAP_X-4*S, FLOW_CY)], fill=LC, width=LW)
    arrowhead_right(draw, MAP_X-4*S, FLOW_CY, LC)
    mid1 = (SF_X+NODE_W + MAP_X) // 2
    lbl = "New Hire"
    lw2, lh2 = tsz(draw, lbl, f_badge)
    draw.text((mid1 - lw2//2, FLOW_CY - lh2 - 5*S), lbl, font=f_badge, fill=TEXT_MUTED)

    # Map → Branch1
    draw.line([(MAP_X+NODE_W+4*S, FLOW_CY), (B1_CX-B1_R-4*S, FLOW_CY)], fill=LC, width=LW)
    arrowhead_right(draw, B1_CX-B1_R-2*S, FLOW_CY, LC)
    mid2 = (MAP_X+NODE_W + B1_CX-B1_R) // 2
    lbl2 = "Enriched"
    lw3, lh3 = tsz(draw, lbl2, f_badge)
    draw.text((mid2 - lw3//2, FLOW_CY - lh3 - 5*S), lbl2, font=f_badge, fill=TEXT_MUTED)

    # Branch1 → VB1
    draw.line([(B1_CX+B1_R, FLOW_CY), (VB1_X, FLOW_CY)], fill=LC, width=LW)

    # VB1 vertical bar
    draw.line([(VB1_X, ORA_CY), (VB1_X, FLOW_CY)], fill=LC, width=LW)

    # VB1 → Oracle arm
    draw.line([(VB1_X, ORA_CY), (ORA_X-4*S, ORA_CY)], fill=LC, width=LW)
    arrowhead_right(draw, ORA_X-2*S, ORA_CY, LC)

    # VB1 → Decision
    draw.line([(VB1_X, FLOW_CY), (DEC_CX-DEC_HW-4*S, FLOW_CY)], fill=LC, width=LW)
    arrowhead_right(draw, DEC_CX-DEC_HW-2*S, FLOW_CY, LC)

    # Decision True → Branch2
    draw.line([(DEC_CX+DEC_HW+2*S, FLOW_CY), (B2_CX-B2_R-4*S, FLOW_CY)], fill=LC, width=LW)
    arrowhead_right(draw, B2_CX-B2_R-2*S, FLOW_CY, LC)
    tlw, _ = tsz(draw, "True", f_dec)
    draw.text((DEC_CX+DEC_HW+8*S, FLOW_CY - 18*S), "True", font=f_dec, fill=C_DECISION)

    # Decision False → ServiceNow (routed left of SN box)
    BYPASS_X = SN_X - 32*S
    JOG_Y    = SN_CY - SN_H//2 - 18*S
    draw.line([(DEC_CX, DEC_CY+DEC_HH+2*S), (DEC_CX, JOG_Y)],     fill=LC, width=LW)
    draw.line([(DEC_CX, JOG_Y),  (BYPASS_X, JOG_Y)],               fill=LC, width=LW)
    draw.line([(BYPASS_X, JOG_Y), (BYPASS_X, SN_CY)],              fill=LC, width=LW)
    draw.line([(BYPASS_X, SN_CY), (SN_X-4*S, SN_CY)],             fill=LC, width=LW)
    arrowhead_right(draw, SN_X-2*S, SN_CY, LC)
    draw.text((DEC_CX + 6*S, DEC_CY+DEC_HH+6*S), "False", font=f_dec, fill=TEXT_MUTED)

    # Branch2 → VB2
    draw.line([(B2_CX+B2_R, FLOW_CY), (VB2_X, FLOW_CY)], fill=LC, width=LW)

    # VB2 vertical bar
    draw.line([(VB2_X, WD_CY), (VB2_X, BEN_CY)], fill=LC, width=LW)

    # VB2 → Workday
    draw.line([(VB2_X, WD_CY),  (TRUE_X-4*S, WD_CY)],  fill=LC, width=LW)
    arrowhead_right(draw, TRUE_X-2*S, WD_CY, LC)

    # VB2 → Benefits
    draw.line([(VB2_X, BEN_CY), (TRUE_X-4*S, BEN_CY)], fill=LC, width=LW)
    arrowhead_right(draw, TRUE_X-2*S, BEN_CY, LC)

    # ── STAGE 1 NODES ────────────────────────────────────────────────────────
    img_ref = [img]
    stage1_defs = [
        (SF_X,  FLOW_CY, NODE_W, NODE_H, C_SALESFORCE, "Salesforce",   "New Hire Query",        "Application Connector"),
        (MAP_X, FLOW_CY, NODE_W, NODE_H, C_MAP,         "Map + Enrich", "Set BenefitsEligible",  "Map Step"),
    ]
    for x, cy, w, h, color, label, sub, tag in stage1_defs:
        draw = draw_node(draw, img_ref, x, cy, w, h, color, label, sub, f_node, f_nodesb)
        img_ref = [img_ref[0]]
        draw = draw_pill(draw, img_ref, x + w//2, cy + h//2 + 18*S, tag, color, f_badge)

    # ── BRANCH 1 CIRCLE ──────────────────────────────────────────────────────
    draw = draw_branch_circle(draw, img_ref, B1_CX, B1_CY, B1_R, "Branch", f_stage)

    # ── ORACLE NODE ───────────────────────────────────────────────────────────
    alw, _ = tsz(draw, "Always runs", f_badge)
    draw.text((ORA_X + ORA_W//2 - alw//2, ORA_CY - ORA_H//2 - 18*S), "Always runs", font=f_badge, fill=TEXT_MUTED)
    img_ref = [img_ref[0]]
    draw = draw_node(draw, img_ref, ORA_X, ORA_CY, ORA_W, ORA_H,
                     C_ORACLE, "Oracle Audit Log", "HIPAA Compliance Log", f_node, f_nodesb)
    draw = draw_pill(draw, img_ref, ORA_X + ORA_W + 16*S + 20*S, ORA_CY, "Database", C_ORACLE, f_badge)

    # ── DECISION DIAMOND ─────────────────────────────────────────────────────
    img_ref = [img_ref[0]]
    draw = draw_decision_diamond(draw, img_ref, DEC_CX, DEC_CY, DEC_HW, DEC_HH,
                                 "Benefits", "Eligible?", f_dec, f_dec)

    # ── BRANCH 2 CIRCLE ──────────────────────────────────────────────────────
    draw = draw_branch_circle(draw, img_ref, B2_CX, B2_CY, B2_R, "Branch", f_stage)

    # ── TRUE-PATH NODES ───────────────────────────────────────────────────────
    for x, cy, w, h, color, label, sub, tag, pill_color, pill_off in [
        (TRUE_X, WD_CY,  TRUE_W, TRUE_H, C_WORKDAY, "Workday HCM",    "Worker Record",  "Application Connector", C_SALESFORCE, 55*S),
        (TRUE_X, BEN_CY, TRUE_W, TRUE_H, C_FTP,      "Benefits Vendor", "Enrollment CSV", "FTP Connector",         C_FTP,        38*S),
    ]:
        img_ref = [img_ref[0]]
        draw = draw_node(draw, img_ref, x, cy, w, h, color, label, sub, f_node, f_nodesb)
        draw = draw_pill(draw, img_ref, x + w + 16*S + pill_off, cy, tag, pill_color, f_badge)

    # ── ERROR HANDLER (subtle, centered at bottom of Stage 1) ────────────────
    EH_W   = 220*S
    EH_H   = 50*S
    EH_X   = (SF_X + MAP_X + NODE_W) // 2 - EH_W // 2   # centered over Stage 1
    EH_CY  = (FLOW_CY + NODE_H//2 + 40*S + 700*S) // 2  # midpoint between pills and focus strip
    EH_CLR = "#9E3A2B"   # muted dark red — subdued, not alarming

    er, eg, eb = hex_rgb(EH_CLR)
    img_ref[0] = alpha_fill(img_ref[0],
        [EH_X, EH_CY-EH_H//2, EH_X+EH_W, EH_CY+EH_H//2], 6*S, (er, eg, eb, 18))
    draw = ImageDraw.Draw(img_ref[0])

    # Dashed border (simulated with short segments)
    x0, y0, x1, y1 = EH_X, EH_CY-EH_H//2, EH_X+EH_W, EH_CY+EH_H//2
    dash, gap = 8*S, 5*S
    for px in range(x0, x1, dash+gap):
        draw.line([(px, y0), (min(px+dash, x1), y0)], fill=EH_CLR, width=S)
        draw.line([(px, y1), (min(px+dash, x1), y1)], fill=EH_CLR, width=S)
    for py in range(y0, y1, dash+gap):
        draw.line([(x0, py), (x0, min(py+dash, y1))], fill=EH_CLR, width=S)
        draw.line([(x1, py), (x1, min(py+dash, y1))], fill=EH_CLR, width=S)

    # Small warning circle + "!" icon
    wc_cx, wc_cy = EH_X + 20*S, EH_CY
    draw.ellipse([wc_cx-9*S, wc_cy-9*S, wc_cx+9*S, wc_cy+9*S], fill=EH_CLR)
    ew, eh2 = tsz(draw, "!", f_badge)
    draw.text((wc_cx - ew//2, wc_cy - eh2//2), "!", font=f_badge, fill="#FFFFFF")

    # Labels
    _, lh_ttl = tsz(draw, "Error Handler", f_stage)
    draw.text((EH_X + 36*S, EH_CY - lh_ttl - S), "Error Handler", font=f_stage, fill=TEXT_MUTED)
    draw.text((EH_X + 36*S, EH_CY + 3*S),         "Try / Catch",   font=f_badge,  fill=TEXT_MUTED)

    # ── FALSE-PATH NODE ───────────────────────────────────────────────────────
    img_ref = [img_ref[0]]
    draw = draw_node(draw, img_ref, SN_X, SN_CY, SN_W, SN_H,
                     C_SERVICENOW, "ServiceNow", "IT Onboarding Ticket", f_node, f_nodesb)
    draw = draw_pill(draw, img_ref, SN_X + SN_W + 16*S + 55*S, SN_CY, "Application Connector", C_SALESFORCE, f_badge)

    img = img_ref[0]
    draw = ImageDraw.Draw(img)

    # ── CONNECTOR LEGEND (top-right) ──────────────────────────────────────────
    seen, unique_legend = set(), []
    for color, label in [(C_SALESFORCE,"Application"),(C_MAP,"Map Step"),(C_ORACLE,"Database"),(C_FTP,"FTP")]:
        if label not in seen:
            seen.add(label)
            unique_legend.append((color, label))

    lx = W - 60*S
    for color, label in reversed(unique_legend):
        tw, _ = tsz(draw, label, f_badge)
        pw = tw + 18*S
        lx -= pw
        img_ref = [img]
        draw = draw_pill(draw, img_ref, lx + pw//2, 202*S, label, color, f_badge)
        img = img_ref[0]
        draw = ImageDraw.Draw(img)
        lx -= 10*S

    # ── DEMO FOCUS AREAS STRIP ───────────────────────────────────────────────
    FOCUS_ITEMS = [
        {"num": "01", "color": C_SALESFORCE,
         "title": "Building an Integration Flow",
         "desc":  "Designing a complete integration with Boomi's intuitive low-code interface guided by AI"},
        {"num": "02", "color": C_MAP,
         "title": "Mapping & Transformation",
         "desc":  "Using Boomi's drag-and-drop mapping tools to standardize and enrich data"},
        {"num": "03", "color": C_ORACLE,
         "title": "Error Handling",
         "desc":  "Implementing reusable error-handling components to manage exceptions"},
        {"num": "04", "color": C_FTP,
         "title": "Testing & Debugging",
         "desc":  "Testing and debugging directly in Boomi's web-based canvas — no local installs required"},
    ]

    CARD_H    = 130*S
    CARD_GAP  = 16*S
    CARD_MAR  = 60*S
    card_w    = (W - 2*CARD_MAR - 3*CARD_GAP) // 4
    # Center the block (label band + cards) between flow content bottom and footer
    _content_bottom = SN_CY + SN_H//2
    _footer_top     = H - 48*S
    _block_h        = 22*S + CARD_H
    STRIP_TOP = _content_bottom + (_footer_top - _content_bottom - _block_h) // 2

    draw.line([(CARD_MAR, STRIP_TOP), (W-CARD_MAR, STRIP_TOP)], fill=DIVIDER, width=S)
    sec_lbl = "DEMO FOCUS AREAS"
    slw, _ = tsz(draw, sec_lbl, f_focus_sec)
    draw.text((W//2 - slw//2, STRIP_TOP - 1*S), sec_lbl, font=f_focus_sec, fill=TEXT_MUTED)

    img_ref = [img]
    for i, item in enumerate(FOCUS_ITEMS):
        cx0   = CARD_MAR + i * (card_w + CARD_GAP)
        cy0   = STRIP_TOP + 20*S
        color = item["color"]
        cr, cg, cb = hex_rgb(color)

        img_ref[0] = alpha_fill(img_ref[0], [cx0, cy0, cx0+card_w, cy0+CARD_H], 8*S, (cr, cg, cb, 22))
        draw = ImageDraw.Draw(img_ref[0])
        rr(draw, [cx0, cy0, cx0+card_w, cy0+CARD_H], 8*S, outline=DIVIDER, lw=S)
        draw.rectangle([cx0, cy0+6*S, cx0+3*S, cy0+CARD_H-6*S], fill=color)

        num_cx, num_cy = cx0 + 22*S, cy0 + 18*S
        draw.ellipse([num_cx-11*S, num_cy-11*S, num_cx+11*S, num_cy+11*S], fill=color)
        nw, nh = tsz(draw, item["num"], f_badge)
        draw.text((num_cx - nw//2, num_cy - nh//2), item["num"], font=f_badge, fill="#FFFFFF")

        draw.text((cx0 + 42*S, cy0 + 10*S), item["title"], font=f_card_ttl, fill=TEXT_MAIN)

        lines  = wrap_text(draw, item["desc"], f_card_dsc, card_w - 20*S)
        desc_y = cy0 + 38*S
        for j, line in enumerate(lines):
            draw.text((cx0 + 14*S, desc_y + j * 18*S), line, font=f_card_dsc, fill=TEXT_SUB)

    img = img_ref[0]
    draw = ImageDraw.Draw(img)

    # ── FOOTER ───────────────────────────────────────────────────────────────
    draw.rectangle([0, H-48*S, W, H], fill=(30, 28, 55))
    draw.line([(0, H-48*S), (W, H-48*S)], fill=DIVIDER, width=S)
    draw.text((60*S, H-30*S), "Boomi Enterprise Integration Platform  ·  NYU Langone Health", font=f_footer, fill=TEXT_MUTED)
    rw, _ = tsz(draw, "boomi.com", f_footer)
    draw.text((W-60*S-rw, H-30*S), "boomi.com", font=f_footer, fill=TEXT_MUTED)

    # ── SAVE ─────────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    img.save(OUTPUT_FILE, "PNG", dpi=(144, 144))
    print(f"Saved: {OUTPUT_FILE}  ({W}x{H}  SCALE={S})")


if __name__ == "__main__":
    generate()
