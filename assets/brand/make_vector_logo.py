"""Fleet's End vector logo, v2 (after vector/CRITIQUE_LOGO.md). SVG masters, text outlined (no font needed).

C "Waterline": white Essex-class carrier going down stern-first, cut by the red waterline; the submerged part is a
faint steel-blue ghost (what happened below the line). Red ring. Recommended.
D "Last light" (A-fix): the same ship in black, entirely on a flat red-orange sun; white waterline and ring.
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

NAVY, INK = "#0A1622", "#06101A"
SEA, SEA_DEEP = "#1C4A72", "#0F2C47"
RED, WHITE, GHOST, STEEL = "#D9372B", "#F4F1EA", "#6E9AC0", "#8FB3D3"
SUN = "#D9572B"
HZ = 296  # horizon (top of the sea) in the 512 box

# Essex SCB-27C profile, bow right, deck top y=0, keel y=38 (critique spec; no yard on the mast)
SHIP = ("M0,0 L246,0 L246,9 L0,9 Z "
        "M10,9 L236,9 L224,38 L36,38 L22,24 L10,24 Z "
        "M128,0 L128,-20 L166,-20 L166,0 Z "
        "M134,-20 L134,-31 L160,-31 L160,-20 Z "
        "M138,-31 L136,-42 L152,-42 L154,-31 Z "
        "M157,-31 L157,-56 L160,-56 L160,-31 Z")
SHIP_T = "translate(40,404) rotate(-20) scale(1.80) translate(0,-38)"


def text_path(font, text, x, y, size, fill, tracking=0.0, kern=None, opacity=1.0):
    """Outline text as one <path>; (x, y) = baseline start. kern = {(a, b): font units}. Returns (svg, width)."""
    gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm
    sc, hmtx = size / upm, font["hmtx"]
    pen = SVGPathPen(gs)
    cx = 0.0
    for i, ch in enumerate(text):
        n = cmap.get(ord(ch))
        if n:
            gs[n].draw(TransformPen(pen, (sc, 0, 0, -sc, x + cx * sc, y)))
        cx += (hmtx[n][0] if n else upm * 0.3) + tracking * upm
        if kern and i + 1 < len(text):
            cx += kern.get((ch, text[i + 1]), 0)
    return f'<path d="{pen.getCommands()}" fill="{fill}" opacity="{opacity}"/>', (cx - tracking * upm) * sc


def icon(kind, cid):
    defs = f"""<defs>
    <clipPath id="disc{cid}"><circle cx="256" cy="256" r="241"/></clipPath>
    <clipPath id="above{cid}"><rect x="0" y="0" width="512" height="{HZ}"/></clipPath>
    <clipPath id="below{cid}"><rect x="0" y="{HZ}" width="512" height="{512 - HZ}"/></clipPath>
    <linearGradient id="sea{cid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SEA}"/><stop offset="1" stop-color="{SEA_DEEP}"/></linearGradient>
  </defs>"""
    sky = f'<rect width="512" height="512" fill="{NAVY}"/>'
    sea = f'<rect y="{HZ}" width="512" height="{512 - HZ}" fill="url(#sea{cid})"/>'
    if kind == "C":
        ship = (f'<g clip-path="url(#below{cid})"><path d="{SHIP}" transform="{SHIP_T}" fill="{GHOST}" opacity="0.40"/></g>'
                f'<g clip-path="url(#above{cid})"><path d="{SHIP}" transform="{SHIP_T}" fill="{WHITE}"/></g>')
        bubbles = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}" opacity="0.5"/>'
                          for x, y, r in ((96, 330, 4), (110, 352, 3), (88, 372, 2)))
        line = f'<rect x="0" y="{HZ - 6}" width="512" height="12" fill="{RED}"/>'
        ring_col = RED
        art = sky + sea + ship + bubbles + line
    else:  # D, A-fix
        sun = f'<g clip-path="url(#above{cid})"><circle cx="276" cy="{HZ + 4}" r="150" fill="{SUN}"/></g>'
        ship = f'<g clip-path="url(#above{cid})"><path d="{SHIP}" transform="{SHIP_T}" fill="{INK}"/></g>'
        line = f'<rect x="0" y="{HZ - 5}" width="512" height="10" fill="{WHITE}"/>'
        ring_col = WHITE
        art = sky + sun + sea + ship + line
    ring = f'<circle cx="256" cy="256" r="247" fill="none" stroke="{ring_col}" stroke-width="12"/>'
    return f'{defs}<g clip-path="url(#disc{cid})">{art}</g>{ring}'


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{body}</svg>'


KERN = {("T", "’"): -20}


def lockup_parts(x0, base, size=230):
    t1, w1 = text_path(ANTON, "FLEET’S", x0, base, size, WHITE, kern=KERN)
    gap = size * 0.2
    t2, w2 = text_path(ANTON, "END", x0 + w1 + gap, base, size, RED)
    word_w = w1 + gap + w2
    # tagline set to the wordmark width
    tag = "WHAT HAPPENED TO THE SHIP"
    _, raw = text_path(OSWALD, tag, 0, 0, size * 0.27, STEEL)
    trk = (word_w - raw) / (len(tag) - 1) / (size * 0.27) * (OSWALD["head"].unitsPerEm / OSWALD["head"].unitsPerEm)
    upm = OSWALD["head"].unitsPerEm
    t3, _ = text_path(OSWALD, tag, x0 + 3, base + size * 0.40, size * 0.27, STEEL,
                      tracking=(word_w - raw) / (len(tag) - 1) / (size * 0.27 / upm) / upm)
    return t1 + t2 + t3, word_w


def lockup(kind, cid):
    h = 480
    icon_px = h - 48
    x0 = 24 + icon_px + 56
    base = h / 2 + 230 * 0.36 - 40  # optical centre of wordmark + tagline block on the icon centre
    txt, word_w = lockup_parts(x0, base)
    w = int(x0 + word_w + 40)
    body = (f'<rect width="{w}" height="{h}" fill="{NAVY}"/>'
            f'<g transform="translate(24,24) scale({icon_px / 512:.5f})">{icon(kind, cid)}</g>{txt}')
    return svg(w, h, body)


def banner(cid):
    W, H = 2560, 1440
    hz = 870
    size = 220
    # measure wordmark width, then centre it in the 1546 x 423 safe area (x 507-2053, y 508-931)
    _, ww = lockup_parts(0, 0, size)
    x0 = (W - ww) / 2
    txt, _ = lockup_parts(x0, 650, size)
    promise, pw = text_path(OSWALD, "EVERY SHIP HAS AN ENDING · NEW STORY EVERY WEEK", 0, 0, 46, WHITE)
    promise, _ = text_path(OSWALD, "EVERY SHIP HAS AN ENDING · NEW STORY EVERY WEEK", (W - pw) / 2, 820, 46, WHITE, opacity=0.8)
    body = f"""<defs><linearGradient id="bsea" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{SEA}"/><stop offset="1" stop-color="{SEA_DEEP}"/></linearGradient></defs>
  <rect width="{W}" height="{H}" fill="{NAVY}"/>
  <rect y="{hz}" width="{W}" height="{H - hz}" fill="url(#bsea)"/>
  <rect y="{hz - 5}" width="{W}" height="10" fill="{RED}"/>{txt}{promise}"""
    return svg(W, H, body)


def write(name, s, png_w):
    open(os.path.join(OUT, name + ".svg"), "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(OUT, name + ".png"), output_width=png_w)


for k in ("C", "D"):
    s = svg(512, 512, icon(k, k))
    write(f"icon_{k}", s, 800)
    for px in (176, 98, 48, 24):
        cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(OUT, f"icon_{k}_{px}.png"), output_width=px)
    write(f"lockup_{k}", lockup(k, "L" + k), 1800)
write("banner", banner("B"), 2560)


# ---- two more concepts (owner asked for 2 more, 2026-11-10) ----
STEEL_RING, RIVET = "#7F8C99", "#56616C"


def icon_E(cid):
    """E "Porthole": the Waterline scene seen through a ship's porthole (steel rim, 8 rivets)."""
    inner = icon("C", cid)
    # reuse C's art but clip to the glass (r=196) and draw a steel rim instead of the red ring
    art = inner[: inner.rindex("<circle")]  # drop C's red ring
    art = art.replace('<circle cx="256" cy="256" r="241"/>', '<circle cx="256" cy="256" r="196"/>')
    art = (f'<g transform="translate(256,256) scale(0.84) translate(-256,-256)">{art}</g>')
    import math
    rivets = "".join(
        f'<circle cx="{256 + 222 * math.cos(math.radians(a)):.1f}" cy="{256 + 222 * math.sin(math.radians(a)):.1f}" '
        f'r="11" fill="{RIVET}"/>' for a in range(0, 360, 45))
    rim = (f'<circle cx="256" cy="256" r="232" fill="{STEEL_RING}"/>'
           f'<circle cx="256" cy="256" r="166" fill="{NAVY}"/>')
    hi = f'<path d="M150,120 A150,150 0 0 1 300,92" fill="none" stroke="{WHITE}" stroke-width="10" stroke-linecap="round" opacity="0.35"/>'
    return rim + rivets + art + f'<circle cx="256" cy="256" r="166" fill="none" stroke="{RIVET}" stroke-width="10"/>' + hi


def icon_F(cid):
    """F "Sonar": a carrier seen from above (angled deck) lying on contour lines, red sonar ping. Where she is now."""
    rings = "".join(f'<circle cx="{256 + dx}" cy="{256 + dy}" r="{r}" fill="none" stroke="{STEEL}" stroke-width="5" opacity="{op}"/>'
                    for r, dx, dy, op in ((70, 6, -4, .55), (120, 10, 6, .45), (170, -6, 10, .35), (220, 4, -6, .25)))
    sweep = (f'<path d="M256,256 L256,15 A241,241 0 0 1 426,86 Z" fill="{STEEL}" opacity="0.18"/>')
    # top-down Essex SCB-27C: hull/deck, angled-deck sponson (port), island (starboard), bow right
    deck = "M0,10 L232,10 L292,32 L232,54 L0,54 Z M58,10 L80,-5 L152,-5 L142,10 Z"
    island = "M128,50 L172,50 L172,62 L128,62 Z"
    ship = (f'<g transform="translate(256,262) rotate(-28) scale(1.25) translate(-146,-22)">'
            f'<path d="{deck}" fill="{WHITE}"/><path d="{island}" fill="{NAVY}"/>'
            f'<path d="M20,32 L210,32" stroke="{NAVY}" stroke-width="3" stroke-dasharray="14 10"/></g>')
    ping = (f'<circle cx="256" cy="262" r="58" fill="none" stroke="{RED}" stroke-width="10"/>'
            f'<circle cx="256" cy="262" r="11" fill="{RED}"/>')
    bg = f'<rect width="512" height="512" fill="{SEA_DEEP}"/>'
    ring = f'<circle cx="256" cy="256" r="247" fill="none" stroke="{RED}" stroke-width="12"/>'
    return (f'<defs><clipPath id="disc{cid}"><circle cx="256" cy="256" r="241"/></clipPath></defs>'
            f'<g clip-path="url(#disc{cid})">{bg}{rings}{sweep}{ship}{ping}</g>{ring}')


for k, fn in (("E", icon_E), ("F", icon_F)):
    s = svg(512, 512, fn(k))
    write(f"icon_{k}", s, 800)
    for px in (176, 98, 48, 24):
        cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(OUT, f"icon_{k}_{px}.png"), output_width=px)
