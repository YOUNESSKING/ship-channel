"""Fleet's End vector logo (SVG, text converted to outlines so it needs no font installed).

Concept A "Last light": a carrier in side profile going down stern-first, black against a setting sun on the horizon.
Concept B "Last stand": a carrier's bow standing vertical out of the water against the setting sun (the Oriskany image).
Outputs SVG masters + PNG previews (cairosvg) at YouTube sizes.
"""
import os
import sys

import cairosvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "vector")
os.makedirs(OUT, exist_ok=True)
ANTON = TTFont(os.path.join(ROOT, "tools", "fonts", "Anton-Regular.ttf"))
OSWALD = TTFont(os.path.join(ROOT, "tools", "maps", "oswald-latin-700-normal.ttf"))

NAVY = "#0A1622"
INK = "#06101A"
SEA = "#1C4A72"
SEA_DEEP = "#0F2C47"
SUN = "#E8A33A"
SUN_HOT = "#F4C76A"
RED = "#D9372B"
WHITE = "#F4F1EA"


def text_path(font, text, x, y, size, fill, tracking=0.0, anchor="start"):
    """Outline `text` as one SVG <path>; (x, y) is the baseline start (or end/middle per anchor)."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    sc = size / upm
    hmtx = font["hmtx"]
    names = [cmap.get(ord(ch)) for ch in text]
    widths = [hmtx[n][0] if n else upm * 0.3 for n in names]
    total = (sum(widths) + tracking * upm * (len(text) - 1)) * sc
    if anchor == "end":
        x -= total
    elif anchor == "middle":
        x -= total / 2
    pen = SVGPathPen(gs)
    cx = 0.0
    for n, w in zip(names, widths):
        if n:
            tp = TransformPen(pen, (sc, 0, 0, -sc, x + cx * sc, y))
            gs[n].draw(tp)
        cx += w + tracking * upm
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>', total


# carrier side profile, bow to the right, in a 220 x 70 box (deck at y=34)
CARRIER = (
    "M0,34 L222,34 L222,39 L214,39 L204,60 L18,60 L10,39 L0,39 Z "      # flight deck + hull
    "M124,34 L124,14 L146,14 L146,34 Z "                                # island
    "M129,14 L129,6 L142,6 L142,14 Z "                                  # funnel
    "M134.5,6 L134.5,-8 L136.5,-8 L136.5,6 Z "                          # mast
    "M129,-2 L142,-2 L142,0 L129,0 Z"                                   # yard
)


def sun_and_sea(cx, cy, r_sun, w, h, horizon, clip_id):
    reflections = "".join(
        f'<rect x="{cx - r_sun * f:.1f}" y="{horizon + 14 + i * 22}" width="{2 * r_sun * f:.1f}" height="7" '
        f'rx="3.5" fill="{SUN}" opacity="{0.75 - i * 0.15:.2f}"/>'
        for i, f in enumerate([0.70, 0.50, 0.34, 0.22])
    )
    return f"""
  <defs>
    <linearGradient id="sea{clip_id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SEA}"/><stop offset="1" stop-color="{SEA_DEEP}"/>
    </linearGradient>
    <radialGradient id="sun{clip_id}" cx="0.5" cy="0.62" r="0.6">
      <stop offset="0" stop-color="{SUN_HOT}"/><stop offset="1" stop-color="{SUN}"/>
    </radialGradient>
    <clipPath id="above{clip_id}"><rect x="0" y="0" width="{w}" height="{horizon}"/></clipPath>
  </defs>
  <circle cx="{cx}" cy="{horizon}" r="{r_sun}" fill="url(#sun{clip_id})" clip-path="url(#above{clip_id})"/>
  <rect x="0" y="{horizon}" width="{w}" height="{h - horizon}" fill="url(#sea{clip_id})"/>
  {reflections}"""


def icon_A(size=512, ring=True, cid="A"):
    s = size
    hz = s * 0.60
    body = sun_and_sea(s / 2, hz, s * 0.30, s, s, hz, cid)
    # ship: scaled, rotated bow-up, stern below the horizon; sea re-drawn over its submerged part
    ship = (f'<g transform="translate({s * 0.15:.1f},{hz + s * 0.035:.1f}) rotate(-17) scale({s / 300:.4f})">'
            f'<path d="{CARRIER}" fill="{INK}" transform="translate(0,-60)"/></g>')
    cover = f'<rect x="0" y="{hz}" width="{s}" height="{s - hz}" fill="url(#sea{cid})"/>'
    refl = "".join(
        f'<rect x="{s / 2 - s * 0.30 * f:.1f}" y="{hz + 14 + i * 22}" width="{2 * s * 0.30 * f:.1f}" height="7" rx="3.5" '
        f'fill="{SUN}" opacity="{0.75 - i * 0.15:.2f}"/>' for i, f in enumerate([0.70, 0.50, 0.34, 0.22]))
    waterline = f'<rect x="0" y="{hz - 2}" width="{s}" height="5" fill="{RED}"/>'
    ringsvg = (f'<circle cx="{s/2}" cy="{s/2}" r="{s/2 - 10}" fill="none" stroke="{SUN}" stroke-width="8"/>'
               if ring else "")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s} {s}" width="{s}" height="{s}">
  <defs><clipPath id="disc{cid}"><circle cx="{s/2}" cy="{s/2}" r="{s/2}"/></clipPath></defs>
  <g clip-path="url(#disc{cid})">
  <rect width="{s}" height="{s}" fill="{NAVY}"/>{body}
  {ship}{cover}{refl}{waterline}
  </g>{ringsvg}
</svg>"""


def icon_B(size=512, ring=True, cid="B"):
    s = size
    hz = s * 0.62
    body = sun_and_sea(s / 2, hz, s * 0.30, s, s, hz, cid)
    k = s / 512
    # bow standing on end: flight-deck slab + hull flare, black against the sun
    bow = (f'M{200*k},{hz} L{282*k},{96*k} L{306*k},{82*k} L{322*k},{92*k} L{316*k},{118*k} '
           f'L{340*k},{hz} Z')
    side = f'M{258*k},{hz} L{304*k},{150*k} L{316*k},{118*k} L{340*k},{hz} Z'
    deck_edge = f'M{200*k},{hz} L{282*k},{96*k}'
    cover = f'<rect x="0" y="{hz}" width="{s}" height="{s - hz}" fill="url(#sea{cid})"/>'
    foam = (f'<ellipse cx="{272*k}" cy="{hz + 6*k}" rx="{92*k}" ry="{12*k}" fill="{WHITE}" opacity="0.85"/>')
    refl = "".join(
        f'<rect x="{s / 2 - s * 0.30 * f:.1f}" y="{hz + 26*k + i * 22*k:.1f}" width="{2 * s * 0.30 * f:.1f}" height="{7*k:.1f}" '
        f'rx="3.5" fill="{SUN}" opacity="{0.7 - i * 0.15:.2f}"/>' for i, f in enumerate([0.62, 0.44, 0.30, 0.2]))
    ringsvg = (f'<circle cx="{s/2}" cy="{s/2}" r="{s/2 - 10}" fill="none" stroke="{SUN}" stroke-width="8"/>'
               if ring else "")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s} {s}" width="{s}" height="{s}">
  <defs><clipPath id="disc{cid}"><circle cx="{s/2}" cy="{s/2}" r="{s/2}"/></clipPath></defs>
  <g clip-path="url(#disc{cid})">
  <rect width="{s}" height="{s}" fill="{NAVY}"/>{body}
  <path d="{bow}" fill="{INK}"/><path d="{side}" fill="#14222F"/>
  <path d="{deck_edge}" stroke="{SUN_HOT}" stroke-width="{3*k:.1f}" opacity="0.6"/>
  {cover}{foam}{refl}
  </g>{ringsvg}
</svg>"""


def inner(svg):
    """Strip the outer <svg> so an icon can be nested."""
    return svg[svg.index(">", svg.index("<svg")) + 1: svg.rindex("</svg>")]


def lockup(icon_fn, w=1800, h=480, bg=NAVY, cid="L"):
    ic = icon_fn(512, True, cid)
    t1, w1 = text_path(ANTON, "FLEET’S", 0, 0, 230, WHITE)
    x0 = h + 40
    t1, w1 = text_path(ANTON, "FLEET’S", x0, h * 0.62, 230, WHITE)
    t2, w2 = text_path(ANTON, "END", x0 + w1 + 46, h * 0.62, 230, RED)
    t3, _ = text_path(OSWALD, "WHAT HAPPENED TO THE SHIPS", x0 + 4, h * 0.86, 62, SUN, tracking=0.06)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="{w}" height="{h}" fill="{bg}"/>
  <g transform="translate(24,24) scale({(h - 48) / 512:.4f})">{inner(ic)}</g>
  {t1}{t2}{t3}
</svg>"""


def banner(icon_fn, cid="N"):
    W, H = 2560, 1440
    lk = lockup(icon_fn, 1546, 412, bg=NAVY, cid=cid + "L")
    hz = H * 0.66
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs><linearGradient id="bsea" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{SEA}"/><stop offset="1" stop-color="{SEA_DEEP}"/></linearGradient></defs>
  <rect width="{W}" height="{H}" fill="{NAVY}"/>
  <rect y="{hz}" width="{W}" height="{H - hz}" fill="url(#bsea)"/>
  <rect y="{hz - 3}" width="{W}" height="6" fill="{RED}"/>
  <g transform="translate({(W - 1546) / 2},{(H - 412) / 2 - 20})">{inner(lk)}</g>
</svg>"""


def write(name, svg, png_w=None):
    p = os.path.join(OUT, name + ".svg")
    open(p, "w").write(svg)
    if png_w:
        cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, name + ".png"), output_width=png_w)


for key, fn in (("A", icon_A), ("B", icon_B)):
    write(f"icon_{key}", fn(512, True, key), 800)
    write(f"lockup_{key}", lockup(fn, cid="L" + key), 1800)
    write(f"banner_{key}", banner(fn, cid="N" + key), 2560)
    for px in (176, 98, 48, 24):
        cairosvg.svg2png(bytestring=fn(512, True, key).encode(),
                         write_to=os.path.join(OUT, f"icon_{key}_{px}.png"), output_width=px)
