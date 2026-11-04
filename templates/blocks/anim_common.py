"""Shared pieces of the animation blocks (GOLD rules 95-100, the locked look of templates/tests_anim/):
green-ink background + vignette, drifting specks, layered greens (leaves, fronds, trees, vines, reeds, water), slow push + parallax,
flash + expanding gold ring "land", gold lock-on brackets, kicker / Cormorant / italic text styles, the stick figure "you"
(common.fig + runtime pose), the supporting cast (one figure + ONE prop) and the modes (backlit disc, gold X-ray body).

Not a template itself (no META): the anim_* blocks build a `Scene`, add layers / texts / effects, then `return sc.done()`.
All times given to Scene methods are absolute chapter seconds (use sc.t(spec, default_rel) = ctx.t)."""
import math, os, random, re, struct
from .common import fig, esc, rich, GOLD, WARM, SOFT, ITAL, ICONS
from .croc_gfx import SHAPES, shape_svg

BG = 'radial-gradient(ellipse at 55% 45%,#173126 0%,#0c1712 55%,#040806 100%)'
BG_NIGHT = 'radial-gradient(ellipse at 70% 30%,#1b3a2c 0%,#0a1712 55%,#030605 100%)'
INK = '#0e1d16'                       # fill of line-art shapes (green-ink, never blue)
EASE_IN = "'power3.out'"              # the snap-in ease

CSS = '''
.an-bg{position:absolute;left:0;top:0;width:1280px;height:720px}
.an-sc{position:absolute;left:0;top:0;width:1280px;height:720px}
.an-ly{position:absolute;left:0;top:0;width:1280px;height:720px;overflow:visible}
.an-vig{position:absolute;left:0;top:0;width:1280px;height:720px;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0) 45%,rgba(0,0,0,.75) 100%);pointer-events:none}
.an-fl{position:absolute;left:0;top:0;width:1280px;height:720px;background:#fff3d6;opacity:0;mix-blend-mode:screen;pointer-events:none}
.an-a{position:absolute}
.an-k{font-family:Jost,sans-serif;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:#f6efe0;font-size:26px;white-space:nowrap;line-height:1.25;text-shadow:0 2px 14px rgba(0,0,0,.75)}
.an-k .an-ki{font-family:"Cormorant Garamond",serif;font-style:italic;font-weight:600;color:#d9bd7e;letter-spacing:.02em;text-transform:none;font-size:1.45em}
.an-big{font-family:"Cormorant Garamond",serif;font-weight:600;color:#f6efe0;white-space:nowrap;line-height:1;font-variant-numeric:lining-nums;text-shadow:0 2px 20px rgba(0,0,0,.6)}
.an-big i,.an-it{font-family:"Cormorant Garamond",serif;font-style:italic;font-weight:600;color:#d9bd7e}
.an-it{white-space:nowrap;line-height:1.1;text-shadow:0 2px 16px rgba(0,0,0,.85)}
.an-hair{position:absolute;height:2px;background:#c9a45c}
.shp .eye{fill:#f6efe0;stroke:none}
.an-svgk{font-family:Jost,sans-serif;font-weight:500;letter-spacing:.22em;fill:#f6efe0;paint-order:stroke;stroke:rgba(0,0,0,.7);stroke-width:5px;stroke-linejoin:round}
'''

def kick_html(s):
    """Caps kicker text; *word* becomes the gold italic Cormorant word ("IT ALREADY *sees* YOU")."""
    return re.sub(r'\*([^*]+)\*', r'<span class="an-ki">\1</span>', esc(s).replace("'", '’'))

def sfx(ctx, cue, t, gain=1.0, dur=None):
    """Sound event with an optional duration (ticks / ticks_up / beep). Cues: tick ticks ticks_up beep thud click scratch marker swoosh shimmer hit heart."""
    e = {'t': round(float(t), 3), 'cue': cue, 'gain': gain}
    if dur: e['dur'] = round(float(dur), 3)
    ctx.events.append(e)

# ---------------------------------------------------------------- greens (far = lighter / hazier, near = darker)
def leaves(seed, n, y0, y1, scale, col, vein='#2c4d3a', x0=-150, x1=1450, cls='sw'):
    r = random.Random(seed); out = []
    for _ in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); a = r.uniform(-70, 70); L = r.uniform(90, 220) * scale; wd = L * r.uniform(.22, .34)
        out.append(f'<g class="{cls}" data-o="{x:.0f} {y:.0f}" transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})"><path d="M0,0 C{wd:.0f},{-L*.3:.0f} {wd*.6:.0f},{-L*.8:.0f} 0,{-L:.0f} C{-wd*.6:.0f},{-L*.8:.0f} {-wd:.0f},{-L*.3:.0f} 0,0 Z" fill="{col}"/>'
                   f'<path d="M0,0 L0,{-L*.95:.0f}" stroke="{vein}" stroke-width="2" opacity=".6"/></g>')
    return ''.join(out)

def frond(x, y, L, a, col, n=9):
    s = [f'<g class="sw" data-o="{x:.0f} {y:.0f}" transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})">', f'<path d="M0,0 Q{L*.15:.0f},{-L*.5:.0f} 0,{-L:.0f}" stroke="{col}" stroke-width="5" fill="none"/>']
    for k in range(1, n):
        t = k / n; py = -L * t; ll = L * .32 * math.sin(math.pi * t) + 10
        for sg in (-1, 1):
            s.append(f'<path d="M0,{py:.0f} q{sg*ll*.5:.0f},{-ll*.15:.0f} {sg*ll:.0f},{ll*.25:.0f} q{-sg*ll*.55:.0f},{ll*.05:.0f} {-sg*ll:.0f},{-ll*.22:.0f}" fill="{col}"/>')
    return ''.join(s) + '</g>'

def broad(x, y, L, a, col, vein='#1f3a2c'):
    w = L * .42
    return (f'<g class="sw" data-o="{x:.0f} {y:.0f}" transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})"><path d="M0,0 C{w:.0f},{-L*.25:.0f} {w*.8:.0f},{-L*.85:.0f} 0,{-L:.0f} C{-w*.8:.0f},{-L*.85:.0f} {-w:.0f},{-L*.25:.0f} 0,0 Z" fill="{col}"/>'
            f'<path d="M0,0 L0,{-L*.96:.0f}" stroke="{vein}" stroke-width="2.5" opacity=".7"/></g>')

def broads(seed, n, y0, y1, L0, L1, a0, a1, col):
    r = random.Random(seed)
    return ''.join(broad(r.uniform(-80, 1400), r.uniform(y0, y1), r.uniform(L0, L1), r.uniform(a0, a1), col) for _ in range(n))

def fronds(seed, n, y0, y1, col, L0=150, L1=260):
    r = random.Random(seed)
    return ''.join(frond(r.uniform(-100, 1450), r.uniform(y0, y1), r.uniform(L0, L1), r.uniform(-55, 55), col) for _ in range(n))

def trees(seed, xs, w0, w1, t0, t1, col, canopy):
    r = random.Random(seed); s = ''
    for x in xs:
        w = r.uniform(w0, w1); top = r.uniform(t0, t1)
        s += f'<path d="M{x-w/2:.0f},740 C{x-w/2+6:.0f},500 {x-w*.35:.0f},{top+80:.0f} {x-w*.3:.0f},{top:.0f} L{x+w*.3:.0f},{top:.0f} C{x+w*.35:.0f},{top+80:.0f} {x+w/2-6:.0f},500 {x+w/2:.0f},740 Z" fill="{col}"/>'
        for _ in range(7):
            cx = x + r.uniform(-170, 170); cy = top + r.uniform(-60, 60); rr = r.uniform(70, 140)
            s += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rr*1.3:.0f}" ry="{rr*.8:.0f}" fill="{canopy}"/>'
    return s

def vine(x, top, L, col):
    d = f'M{x},{top} ' + ' '.join(f'Q{x+(18 if i%2 else -18)},{top+L*(i+.5)/6:.0f} {x},{top+L*(i+1)/6:.0f}' for i in range(6))
    lv = ''.join(f'<ellipse cx="{x+(10 if i%2 else -10)}" cy="{top+L*i/7:.0f}" rx="12" ry="6" fill="{col}" transform="rotate({30 if i%2 else -30} {x+(10 if i%2 else -10)} {top+L*i/7:.0f})"/>' for i in range(1, 7))
    return f'<g class="sw vn" data-o="{x} {top}"><path d="{d}" stroke="{col}" stroke-width="4" fill="none"/>{lv}</g>'

def reeds(seed, n, y0, y1, col, h0=90, h1=230, x0=-60, x1=1340):
    """Reeds / grass blades (river bank, swamp)."""
    r = random.Random(seed); s = ''
    for _ in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); h = r.uniform(h0, h1); bend = r.uniform(-40, 40); w = r.uniform(5, 10)
        s += (f'<g class="sw" data-o="{x:.0f} {y:.0f}"><path d="M{x-w/2:.0f},{y:.0f} Q{x+bend*.3:.0f},{y-h*.6:.0f} {x+bend:.0f},{y-h:.0f} Q{x+bend*.3+w*.4:.0f},{y-h*.6:.0f} {x+w/2:.0f},{y:.0f} Z" fill="{col}"/>'
              + (f'<ellipse cx="{x+bend:.0f}" cy="{y-h+8:.0f}" rx="5" ry="16" fill="{col}" transform="rotate({bend*.4:.0f} {x+bend:.0f} {y-h+8:.0f})"/>' if r.random() < .25 else '') + '</g>')
    return s

def waterline(y, x0=-200, x1=1500, amp=7, period=140):
    d = f'M{x0},{y} '; x = x0
    while x < x1:
        d += f'q {period/4},{-amp} {period/2},0 t {period/2},0 '; x += period
    return d

def water_band(p, y, col='#0b1a14', line=SOFT, lines=5):
    """Dark green water from y down + a warm surface line + glints (glints get class 'gl')."""
    s = f'<path d="{waterline(y)} V760 H-200 Z" fill="{col}"/><path d="{waterline(y)}" fill="none" stroke="{line}" stroke-width="2.5" stroke-opacity=".55"/>'
    r = random.Random(len(p) + int(y))
    for k in range(lines * 3):
        yy = y + 18 + r.uniform(0, 720 - y - 30); x = r.uniform(-50, 1300); w = r.uniform(30, 120)
        s += f'<path class="gl" d="M{x:.0f},{yy:.0f} h{w:.0f}" stroke="{line}" stroke-width="2" stroke-linecap="round" opacity="{r.uniform(.12, .35):.2f}"/>'
    return s

# ---------------------------------------------------------------- people (GOLD 97): "you" = fig; cast = fig + ONE prop
def scientist(hx, hy, s):
    sy = hy - 78 * s
    return (f'<path d="M{hx-26*s:.0f},{sy-4*s:.0f} L{hx+26*s:.0f},{sy-4*s:.0f} L{hx+32*s:.0f},{hy+30*s:.0f} L{hx-32*s:.0f},{hy+30*s:.0f} Z" fill="#e9e4d6" stroke="#0d0b08" stroke-width="2"/>'
            f'<path d="M{hx:.0f},{sy-4*s:.0f} L{hx-6*s:.0f},{hy+30*s:.0f} M{hx:.0f},{sy-4*s:.0f} L{hx+6*s:.0f},{hy+30*s:.0f}" stroke="#b7b09e" stroke-width="2"/>'
            f'<g fill="none" stroke="#0d0b08" stroke-width="{2.4*s:.1f}"><circle cx="{hx-9*s:.0f}" cy="{hy-117*s:.0f}" r="{7*s:.0f}" fill="#fff" fill-opacity=".25"/><circle cx="{hx+9*s:.0f}" cy="{hy-117*s:.0f}" r="{7*s:.0f}" fill="#fff" fill-opacity=".25"/><path d="M{hx-2*s:.0f},{hy-117*s:.0f} h{4*s:.0f}"/></g>'
            f'<rect x="{hx+22*s:.0f}" y="{sy+20*s:.0f}" width="{26*s:.0f}" height="{34*s:.0f}" rx="3" fill="#8a6e45" stroke="#0d0b08" stroke-width="2"/><rect x="{hx+26*s:.0f}" y="{sy+26*s:.0f}" width="{18*s:.0f}" height="{22*s:.0f}" fill="#f6efe0"/>')

def honey_collector(hx, hy, s):
    return (f'<ellipse cx="{hx-22*s:.0f}" cy="{hy-113*s:.0f}" rx="{9*s:.0f}" ry="{19*s:.0f}" fill="#d9b278" stroke="#0d0b08" stroke-width="2"/>'
            f'<circle cx="{hx-25*s:.0f}" cy="{hy-119*s:.0f}" r="{2.6*s:.1f}" fill="#0d0b08"/>'
            f'<path d="M{hx-24*s:.0f},{hy-138*s:.0f} q{24*s:.0f},{-16*s:.0f} {48*s:.0f},0" stroke="#c84f2e" stroke-width="{7*s:.0f}" fill="none" stroke-linecap="round"/>'
            f'<g transform="translate({hx+34*s:.0f},{hy-10*s:.0f}) scale({s:.2f})"><path d="M-14,-8 q14,-14 28,0 v20 q-14,10 -28,0 z" fill="#9b6a35" stroke="#0d0b08" stroke-width="2"/><path d="M-14,-8 h28" stroke="#5a3a1c" stroke-width="3"/></g>')

def hunter(hx, hy, s):
    return (f'<path d="M{hx-30*s:.0f},{hy-128*s:.0f} q{30*s:.0f},{-8*s:.0f} {60*s:.0f},0 M{hx-22*s:.0f},{hy-128*s:.0f} q{22*s:.0f},{-34*s:.0f} {44*s:.0f},0 z" fill="#d8c9a3" stroke="#0d0b08" stroke-width="2"/>'
            f'<path d="M{hx-30*s:.0f},{hy-128*s:.0f} h{60*s:.0f}" stroke="#d8c9a3" stroke-width="{6*s:.0f}" stroke-linecap="round"/>'
            f'<path d="M{hx+6*s:.0f},{hy-60*s:.0f} L{hx+78*s:.0f},{hy-96*s:.0f}" stroke="#6b4a2a" stroke-width="{7*s:.0f}" stroke-linecap="round"/><path d="M{hx+48*s:.0f},{hy-81*s:.0f} L{hx+92*s:.0f},{hy-103*s:.0f}" stroke="#2a2a2a" stroke-width="{4*s:.0f}" stroke-linecap="round"/>'
            f'<path d="M{hx-18*s:.0f},{hy-80*s:.0f} L{hx+18*s:.0f},{hy-30*s:.0f}" stroke="#7a5a32" stroke-width="{5*s:.0f}"/>')

def worker(hx, hy, s):
    """Local worker / fisher: one costume item (a conical hat)."""
    return f'<path d="M{hx-40*s:.0f},{hy-126*s:.0f} L{hx:.0f},{hy-158*s:.0f} L{hx+40*s:.0f},{hy-126*s:.0f} Q{hx:.0f},{hy-120*s:.0f} {hx-40*s:.0f},{hy-126*s:.0f} Z" fill="#c9a86a" stroke="#0d0b08" stroke-width="2"/>'

def explorer(hx, hy, s):
    """Hat + backpack + head torch (lamp point at hx+18s, hy-120s)."""
    return (f'<path d="M{hx-30*s:.0f},{hy-128*s:.0f} h{60*s:.0f} M{hx-18*s:.0f},{hy-128*s:.0f} q{18*s:.0f},{-26*s:.0f} {36*s:.0f},0" stroke="{WARM}" stroke-width="{6*s:.1f}" fill="#16120d" stroke-linecap="round"/>'
            f'<rect x="{hx-34*s:.0f}" y="{hy-82*s:.0f}" width="{26*s:.0f}" height="{48*s:.0f}" rx="{6*s:.0f}" fill="#16120d" stroke="{WARM}" stroke-width="{4*s:.1f}"/>'
            f'<circle cx="{hx+18*s:.0f}" cy="{hy-120*s:.0f}" r="{5*s:.1f}" fill="#fff6dc"/>')

PROPS = {'you': None, 'scientist': scientist, 'honey': honey_collector, 'hunter': hunter, 'worker': worker, 'explorer': explorer, 'child': None}

def person(p, role, hx, hy, s):
    """Stick figure (ids p-fig, p-armL ... for pose) + the role's one prop. role: you|scientist|honey|hunter|worker|explorer|child."""
    if role not in PROPS: raise KeyError(f'unknown person "{role}". Known: {", ".join(PROPS)}')
    if role == 'child': s = s * .62; hy = hy + 84 * s * .6
    pr = PROPS[role]
    return f'<g id="{p}-who">{fig(p, hx, hy, s)}{pr(hx, hy, s) if pr else ""}</g>', hx, hy, s

def posed(svg, p, hx, hy, s, aL=22, aR=-22, lL=13, lR=-13):
    """Give a fig() a static pose (svg transforms; for figures that are not animated with the runtime pose())."""
    sy = hy - 78 * s
    for part, ang, oy in (('armL', aL, sy), ('armR', aR, sy), ('legL', lL, hy), ('legR', lR, hy)):
        svg = svg.replace(f'<g id="{p}-{part}">', f'<g id="{p}-{part}" transform="rotate({ang} {hx:.1f} {oy:.1f})">')
    return svg

def backlit(p, hx, hy, s):
    """Mode: black silhouette in a warm light disc (disc id p-disc)."""
    return (f'<defs><radialGradient id="{p}-dg"><stop offset="0" stop-color="#f3dca0" stop-opacity=".75"/><stop offset=".55" stop-color="#e0a24a" stop-opacity=".25"/><stop offset="1" stop-color="#e0a24a" stop-opacity="0"/></radialGradient></defs>'
            f'<circle id="{p}-disc" cx="{hx}" cy="{hy-40*s:.0f}" r="{130*s:.0f}" fill="url(#{p}-dg)"/>'
            f'<g fill="none" stroke="#050403" stroke-width="{7*s:.1f}" stroke-linecap="round"><circle cx="{hx}" cy="{hy-112*s:.0f}" r="{24*s:.0f}" fill="#050403"/>'
            f'<path d="M{hx},{hy-88*s:.0f} V{hy} M{hx},{hy-78*s:.0f} l{-28*s:.0f},{48*s:.0f} M{hx},{hy-78*s:.0f} l{28*s:.0f},{48*s:.0f} M{hx},{hy} l{-18*s:.0f},{84*s:.0f} M{hx},{hy} l{18*s:.0f},{84*s:.0f}"/></g>')

def crowd(x, y, n=6, gap=20, col=WARM):
    return ''.join(f'<g stroke="{col}" stroke-width="2.4" stroke-linecap="round"><circle cx="{x-(n-1)*gap/2+i*gap:.0f}" cy="{y-26}" r="5" fill="{col}"/><path d="M{x-(n-1)*gap/2+i*gap:.0f},{y-21} v14"/></g>' for i in range(n))

# ---------------------------------------------------------------- X-ray mode (gold cutaway + glowing organ)
def organ_svg(kind, cx, cy, r, col=GOLD):
    """A glowing organ around (cx,cy), size r. kind: heart|lungs|brain|gut|gland|dot."""
    k = r / 20
    if kind == 'heart':
        d = f'<path d="M{cx},{cy-6*k:.1f} c{-4*k:.1f},{-9*k:.1f} {-18*k:.1f},{-8*k:.1f} {-16*k:.1f},{4*k:.1f} c{2*k:.1f},{9*k:.1f} {16*k:.1f},{17*k:.1f} {16*k:.1f},{17*k:.1f} c0,0 {14*k:.1f},{-8*k:.1f} {16*k:.1f},{-17*k:.1f} c{2*k:.1f},{-12*k:.1f} {-12*k:.1f},{-13*k:.1f} {-16*k:.1f},{-4*k:.1f} z" fill="{col}" fill-opacity=".9"/>'
    elif kind == 'lungs':
        d = (f'<path d="M{cx-3*k:.1f},{cy-16*k:.1f} C{cx-16*k:.1f},{cy-16*k:.1f} {cx-22*k:.1f},{cy+4*k:.1f} {cx-20*k:.1f},{cy+16*k:.1f} C{cx-16*k:.1f},{cy+20*k:.1f} {cx-6*k:.1f},{cy+18*k:.1f} {cx-3*k:.1f},{cy+12*k:.1f} Z" fill="{col}" fill-opacity=".85"/>'
             f'<path d="M{cx+3*k:.1f},{cy-16*k:.1f} C{cx+16*k:.1f},{cy-16*k:.1f} {cx+22*k:.1f},{cy+4*k:.1f} {cx+20*k:.1f},{cy+16*k:.1f} C{cx+16*k:.1f},{cy+20*k:.1f} {cx+6*k:.1f},{cy+18*k:.1f} {cx+3*k:.1f},{cy+12*k:.1f} Z" fill="{col}" fill-opacity=".85"/>'
             f'<path d="M{cx},{cy-24*k:.1f} V{cy-12*k:.1f}" stroke="{col}" stroke-width="{2.5*k:.1f}"/>')
    elif kind == 'brain':
        d = (f'<ellipse cx="{cx}" cy="{cy}" rx="{17*k:.1f}" ry="{13*k:.1f}" fill="{col}" fill-opacity=".85"/>'
             f'<path d="M{cx-11*k:.1f},{cy-3*k:.1f} q{5*k:.1f},{-6*k:.1f} {9*k:.1f},0 t{9*k:.1f},0 M{cx-9*k:.1f},{cy+5*k:.1f} q{5*k:.1f},{-5*k:.1f} {9*k:.1f},0 t{8*k:.1f},0" stroke="#3a2c12" stroke-width="{1.6*k:.1f}" fill="none"/>')
    elif kind == 'gut':
        d = (f'<path d="M{cx-14*k:.1f},{cy-12*k:.1f} h{28*k:.1f} q{6*k:.1f},0 {6*k:.1f},{6*k:.1f} t{-6*k:.1f},{6*k:.1f} h{-28*k:.1f} q{-6*k:.1f},0 {-6*k:.1f},{6*k:.1f} t{6*k:.1f},{6*k:.1f} h{28*k:.1f}" '
             f'stroke="{col}" stroke-width="{5*k:.1f}" fill="none" stroke-linecap="round" stroke-opacity=".9"/>')
    elif kind == 'gland':
        d = f'<ellipse cx="{cx}" cy="{cy}" rx="{14*k:.1f}" ry="{8*k:.1f}" fill="{col}" fill-opacity=".9"/>' + ''.join(
            f'<circle cx="{cx+(i-1.5)*7*k:.1f}" cy="{cy+(3 if i % 2 else -3)*k:.1f}" r="{1.8*k:.1f}" fill="#3a2c12"/>' for i in range(4))
    else:
        d = f'<circle cx="{cx}" cy="{cy}" r="{10*k:.1f}" fill="{col}" fill-opacity=".9"/>'
    return d

def glow_defs(p):
    return (f'<radialGradient id="{p}-og"><stop offset="0" stop-color="#ffe2a0" stop-opacity=".9"/><stop offset=".35" stop-color="{GOLD}" stop-opacity=".45"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="{p}-scg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset=".85" stop-color="{GOLD}" stop-opacity=".22"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="{p}-eg"><stop offset="0" stop-color="#ffe9a8" stop-opacity="1"/><stop offset=".35" stop-color="#e8b04a" stop-opacity=".7"/><stop offset="1" stop-color="#e8b04a" stop-opacity="0"/></radialGradient>')

HUMAN_ORGANS = {'heart': (6, 38, 'heart'), 'lungs': (0, 34, 'lungs'), 'brain': (0, -112, 'brain'), 'gut': (0, 62, 'gut'), 'gland': (0, -100, 'gland')}   # (dx, dy from shoulder y) in figure units

def xray_human(p, hx, hy, s, organ='heart'):
    """Gold X-ray stick body (as make_test6 xray, larger stroke for big sizes). Returns (svg, organ centre (x,y), organ radius)."""
    sy = hy - 78 * s; sw = max(3, 3 * s / .85 * .8)
    body = (f'<g id="{p}-xb" fill="none" stroke="{GOLD}" stroke-width="{sw:.1f}" stroke-linecap="round" stroke-linejoin="round">'
            f'<circle cx="{hx}" cy="{hy-112*s:.0f}" r="{24*s:.0f}" stroke-opacity=".85"/>'
            f'<path d="M{hx-26*s:.0f},{sy:.0f} Q{hx},{sy-10*s:.0f} {hx+26*s:.0f},{sy:.0f} L{hx+22*s:.0f},{hy:.0f} L{hx-22*s:.0f},{hy:.0f} Z" stroke-opacity=".85"/>'
            f'<path d="M{hx-26*s:.0f},{sy:.0f} l{-7*s:.0f},{56*s:.0f} M{hx+26*s:.0f},{sy:.0f} l{7*s:.0f},{56*s:.0f} M{hx-12*s:.0f},{hy:.0f} v{84*s:.0f} M{hx+12*s:.0f},{hy:.0f} v{84*s:.0f}" stroke-opacity=".85"/>'
            f'<path d="M{hx},{sy+4*s:.0f} V{hy-6*s:.0f}" stroke-opacity=".3" stroke-dasharray="{3*s:.0f} {4*s:.0f}"/>'
            + ''.join(f'<path d="M{hx-18*s:.0f},{sy+(10+i*9)*s:.0f} q{18*s:.0f},{5*s:.0f} {36*s:.0f},0" stroke-opacity=".28" stroke-width="{sw*.6:.1f}"/>' for i in range(4)) + '</g>')
    dx, dy, kind = HUMAN_ORGANS.get(organ, (0, 34, organ))
    oy = (hy - 112 * s) if organ == 'brain' else sy + dy * s
    return body, (hx + dx * s, oy), 17 * s

def xray_shape(p, shape, x, y, w, ribs=True):
    """Line-art animal (croc_gfx SHAPES) as a gold X-ray outline, ground at (x,y), facing right, w px long. Returns svg."""
    sc = w / 1000
    inner = shape_svg(shape, GOLD, 3 / sc, .95).replace('fill="#1a2429"', f'fill="{GOLD}" fill-opacity=".06"')
    rb = ''
    if ribs:
        top = SHAPES[shape][1] * 1000
        for i in range(9):
            xx = 300 + i * 45
            rb += f'<path d="M{xx},{-top*.12:.0f} q14,{-top*.35:.0f} 0,{-top*.7:.0f}" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width="{2.2/sc:.1f}"/>'
        rb += f'<path d="M80,{-top*.25:.0f} C300,{-top*.62:.0f} 600,{-top*.86:.0f} 900,{-top*.78:.0f}" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="{2.4/sc:.1f}" stroke-dasharray="{8/sc:.0f} {7/sc:.0f}"/>'
    return f'<g id="{p}-xb" transform="translate({x:.0f},{y:.0f}) scale({sc:.4f})">{inner}{rb}</g>'

def shape_box(shape, w):
    return w, SHAPES[shape][1] * w   # length, height (above ground)

# ---------------------------------------------------------------- animals / glyphs: {"image": path, "aspect": h/w} | {"shape": "croc"} | {"icon": "fish"} | {"person": "you"}
def img_aspect(path):
    try:
        from PIL import Image
        with Image.open(path) as im: return im.size[1] / im.size[0]
    except Exception:
        try:
            with open(path, 'rb') as f: h = f.read(24)
            w, hh = struct.unpack('>II', h[16:24]); return hh / w
        except Exception: return .5

def glyph(ctx, gid, spec, cx, ground, w, flip=False, col=WARM, op=1.0):
    """An animal / icon whose box is centred at cx with its bottom on `ground`, w px wide. Returns (svg, height)."""
    if isinstance(spec, str): spec = {'shape': spec} if spec in SHAPES else ({'icon': spec} if spec in ICONS else {'image': spec})
    fl = f' translate({2*cx:.0f},0) scale(-1,1)' if flip else ''
    if spec.get('image'):
        src = ctx.asset(spec['image']); path = ctx.B.resolve(spec['image'])
        asp = float(spec.get('aspect') or img_aspect(path)); h = w * asp
        return (f'<g id="{gid}" opacity="{op}"><g transform="{fl.strip()}"><image href="{src}" x="{cx-w/2:.0f}" y="{ground-h:.0f}" width="{w:.0f}" height="{h:.0f}" preserveAspectRatio="xMidYMid meet"/></g></g>', h)
    if spec.get('shape'):
        sh = spec['shape']; sc = w / 1000; h = SHAPES[sh][1] * w
        c = spec.get('color', col)
        inner = shape_svg(sh, c, 3.2 / sc, .95).replace('fill="#1a2429"', f'fill="{INK}"')
        return f'<g id="{gid}" opacity="{op}"><g transform="{fl.strip()}"><g transform="translate({cx-w/2:.0f},{ground:.0f}) scale({sc:.4f})">{inner}</g></g></g>', h
    if spec.get('icon'):
        k = w / 190
        return f'<g id="{gid}" opacity="{op}"><g transform="{fl.strip()}"><g transform="translate({cx:.0f},{ground-95*k:.0f}) scale({k:.3f})">{ICONS[spec["icon"]]}</g></g></g>', 190 * k
    if spec.get('person'):   # w = figure height (head to feet); drawn in a static relaxed pose
        s = w / 220; svg, hx, hy, ss = person(gid + 'p', spec['person'], cx, ground - 84 * s, s)
        return f'<g id="{gid}" opacity="{op}">{posed(svg, gid + "p", hx, hy, ss)}</g>', 220 * s
    raise KeyError('animal/icon spec needs "image", "shape", "icon" or "person"')

# ---------------------------------------------------------------- the scene
class Scene:
    """One animation shot: background, layers (parallax), effects, texts, vignette, flash."""
    def __init__(self, ctx, bg=BG, push=(1.0, 1.05, '50% 50%'), fade=.3):
        self.ctx = ctx; self.p = ctx.id; self.a = ctx.a; self.b = ctx.b; self.D = ctx.dur
        self.bg = bg; self.push = push; self.fade = fade
        self.layers = []; self.fx = []; self.html = []; self.top = []; self.js = []; self.defs = [glow_defs(self.p)]; self.n = 0
    def t(self, spec, rel): return self.ctx.t(spec, rel)
    def sfx(self, cue, t, gain=1.0, dur=None): sfx(self.ctx, cue, t, gain, dur)
    def J(self, s): self.js.append(s)
    # ---- layers
    def svg(self, content, drift=0.0, sway=0.0, lid=None):
        """Add an svg layer; drift = px of parallax over the shot (negative = left); sway = degrees for its .sw children."""
        self.n += 1; lid = lid or f'{self.p}-L{self.n}'
        self.layers.append(f'<svg id="{lid}" class="an-ly" width="1280" height="720" viewBox="0 0 1280 720">{content}</svg>')
        if drift: self.J(f"tl.fromTo('#{lid}',{{x:0}},{{x:{drift},duration:{self.D:.3f},ease:'none'}},{self.a:.3f});")
        if sway:
            self.J(f"document.querySelectorAll('#{lid} .sw').forEach((l,i)=>{{const a=(i%2?{sway}:-{sway});tl.fromTo(l,{{rotation:0,svgOrigin:l.dataset.o}},{{rotation:a,duration:1.6+(i%5)*.3,yoyo:true,repeat:Math.ceil({self.D:.3f}/1.6),ease:'sine.inOut'}},{self.a:.3f}+(i%7)*.12);}});")
        return lid
    def add_html(self, h): self.html.append(h)
    # ---- ambient motion
    def specks(self, n=34, seed=3, col='#e4f29a', y0=120, y1=640, r0=1.3, r1=2.8, lid=None):
        r = random.Random(seed); s = ''; js = []
        for i in range(n):
            x = r.uniform(0, 1280); y = r.uniform(y0, y1); rr = r.uniform(r0, r1)
            s += f'<circle id="{self.p}-sp{i}" cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="{col}" opacity=".2"/>'
            dx = (1 if i % 2 else -1) * r.uniform(15, 60); dy = -r.uniform(10, 45); per = r.uniform(.6, 1.8)
            js.append(f"tl.fromTo('#{self.p}-sp{i}',{{x:0,y:0}},{{x:{dx:.0f},y:{dy:.0f},duration:{self.D:.3f},ease:'sine.inOut'}},{self.a:.3f});"
                      f"tl.fromTo('#{self.p}-sp{i}',{{opacity:.12}},{{opacity:.9,duration:{per:.2f},yoyo:true,repeat:{int(self.D / per) + 1},ease:'sine.inOut'}},{self.a + r.uniform(0, 1):.3f});")
        self.svg(s, lid=lid); self.J(''.join(js))
    def dust(self, n=40, seed=5):
        """Pale floating dust specks (for plain green-ink cards)."""
        self.specks(n, seed, col='#e9dcc0', y0=40, y1=700, r0=.9, r1=2.0)
    def glints(self, lid):
        self.J(f"document.querySelectorAll('#{lid} .gl').forEach((g,i)=>{{tl.fromTo(g,{{x:0}},{{x:(i%2?28:-22),duration:2.2+(i%4)*.5,yoyo:true,repeat:Math.ceil({self.D:.3f}/2.2),ease:'sine.inOut'}},{self.a:.3f});}});")
    def glow(self, cx, cy, rx, ry, col='#e0a24a', op=.10, pulse=True):
        gid = f'{self.p}-gw{self.n}'
        self.svg(f'<ellipse id="{gid}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}" opacity="{op}"/>')
        if pulse: self.J(f"tl.fromTo('#{gid}',{{opacity:{op*.7:.3f}}},{{opacity:{op*1.4:.3f},duration:2.4,yoyo:true,repeat:Math.ceil({self.D:.3f}/2.4),ease:'sine.inOut'}},{self.a:.3f});")
    # ---- graphic events
    def flash(self, t, amt=.24):
        self.J(f"tl.fromTo('#{self.p}-fl',{{opacity:0}},{{opacity:{amt},duration:.05,immediateRender:false}},{t:.3f});tl.to('#{self.p}-fl',{{opacity:0,duration:.45}},{t+.05:.3f});")
    def land(self, t, cx, cy, r1=170, r2=260, hit=True, gain=1.0, pulses=True):
        """Count-up landing: short flash + two expanding gold rings + deep hit (+ soft shimmer), then rings keep pulsing softly."""
        k = len(self.fx)
        self.fx.append(f'<circle id="{self.p}-rg{k}a" cx="{cx:.0f}" cy="{cy:.0f}" r="10" fill="none" stroke="{GOLD}" stroke-width="3" opacity="0"/>'
                       f'<circle id="{self.p}-rg{k}b" cx="{cx:.0f}" cy="{cy:.0f}" r="10" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0"/>'
                       f'<circle id="{self.p}-rg{k}c" cx="{cx:.0f}" cy="{cy:.0f}" r="10" fill="none" stroke="{GOLD}" stroke-width="1.5" opacity="0"/>')
        self.flash(t, .28)
        self.J(f"tl.fromTo('#{self.p}-rg{k}a',{{attr:{{r:10}},opacity:1}},{{attr:{{r:{r1}}},opacity:0,duration:.9,ease:'power2.out',immediateRender:false}},{t:.3f});"
               f"tl.fromTo('#{self.p}-rg{k}b',{{attr:{{r:10}},opacity:.8}},{{attr:{{r:{r2}}},opacity:0,duration:1.3,ease:'power2.out',immediateRender:false}},{t+.1:.3f});")
        if pulses:
            tt = t + 1.4
            while tt < self.b - .4:
                self.J(f"tl.fromTo('#{self.p}-rg{k}c',{{attr:{{r:12}},opacity:.45}},{{attr:{{r:{r1*.7:.0f}}},opacity:0,duration:1.1,ease:'power1.out',immediateRender:false}},{tt:.3f});"); tt += 1.4
        if hit: self.sfx('hit', t, gain); self.sfx('shimmer', t, .3 * gain)
    def brackets(self, t, cx, cy, hw, hh, beep=1.0, gain=.5, breathe=True):
        """Gold lock-on brackets snap from wide to around (cx,cy) +-(hw,hh) in .32 s, then breathe; held beep."""
        k = len(self.fx); p = f'{self.p}-br{k}'
        self.fx.append(f'<g stroke="{GOLD}" stroke-width="4" fill="none" stroke-linecap="square">'
                       f'<path id="{p}1" d="M0,26 V0 H26" opacity="0"/><path id="{p}2" d="M0,-26 V0 H26" opacity="0"/><path id="{p}3" d="M0,26 V0 H-26" opacity="0"/><path id="{p}4" d="M0,-26 V0 H-26" opacity="0"/></g>')
        C = [(cx - hw - 90, cy - hh - 80, cx - hw, cy - hh, 1), (cx - hw - 90, cy + hh + 80, cx - hw, cy + hh, 2), (cx + hw + 90, cy - hh - 80, cx + hw, cy - hh, 3), (cx + hw + 90, cy + hh + 80, cx + hw, cy + hh, 4)]
        for x0, y0, x1, y1, i in C:
            self.J(f"tl.fromTo('#{p}{i}',{{x:{x0:.0f},y:{y0:.0f},opacity:0}},{{x:{x1:.0f},y:{y1:.0f},opacity:1,duration:.32,ease:'power3.out',immediateRender:false}},{t:.3f});")
            if breathe:
                n = max(1, int((self.b - t - .5) / .5))
                self.J(f"tl.to('#{p}{i}',{{x:{x1 + (-6 if x1 < cx else 6):.0f},y:{y1 + (-6 if y1 < cy else 6):.0f},duration:.5,yoyo:true,repeat:{n},ease:'sine.inOut'}},{t+.35:.3f});")
        self.sfx('beep', t, gain, beep)
        return p
    def heartbeat_rings(self, times, cx, cy, r0=40, r1=120, sound=True, gain=.8):
        k = len(self.fx)
        self.fx.append(f'<circle id="{self.p}-hb{k}" cx="{cx:.0f}" cy="{cy:.0f}" r="{r0}" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0"/>')
        for t in times:
            self.J(f"tl.fromTo('#{self.p}-hb{k}',{{attr:{{r:{r0}}},opacity:.9}},{{attr:{{r:{r1}}},opacity:0,duration:.7,ease:'power2.out',immediateRender:false}},{t:.3f});")
            if sound: self.sfx('heart', t, gain)
    # ---- text
    def kicker(self, text, t, y=612, x=None, w=1280, size=26, hair=True, align='center', sound=None):
        i = f'{self.p}-k{len(self.html)}'
        left = 0 if x is None else x; ww = 1280 if x is None else w
        self.html.append(f'<div id="{i}" class="an-a an-k" style="left:{left}px;width:{ww}px;top:{y}px;text-align:{align};font-size:{size}px;opacity:0">{kick_html(text)}</div>')
        self.J(f"tl.fromTo('#{i}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.45,ease:'power2.out',immediateRender:false}},{t:.3f});")
        if hair:
            hw = 160; hx = (640 - hw / 2) if (x is None or align == 'center') else left
            self.html.append(f'<div id="{i}h" class="an-hair" style="left:{hx:.0f}px;width:{hw}px;top:{y + size * 1.7:.0f}px;opacity:0"></div>')
            self.J(f"tl.fromTo('#{i}h',{{scaleX:0,opacity:1,transformOrigin:'{'50% 50%' if align == 'center' else '0 50%'}'}},{{scaleX:1,duration:.5,ease:'power2.out',immediateRender:false}},{t+.15:.3f});")
        if sound: self.sfx(sound, t, .4)
        return i
    def line(self, text, t, y=630, size=40, x=None, w=1280, align='center', cls='an-it'):
        """Italic gold Cormorant line (or cls='an-big' for warm white)."""
        i = f'{self.p}-t{len(self.html)}'
        left = 0 if x is None else x
        self.html.append(f'<div id="{i}" class="an-a {cls}" style="left:{left}px;width:{1280 if x is None else w}px;top:{y}px;text-align:{align};font-size:{size}px;opacity:0">{rich(text)}</div>')
        self.J(f"tl.fromTo('#{i}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.5,ease:'power2.out',immediateRender:false}},{t:.3f});")
        return i
    def hud(self, text, t):
        """Small place / time caption top left (e.g. "SUNDARBANS · 02:14 AM")."""
        i = f'{self.p}-hud'
        self.html.append(f'<div id="{i}" class="an-a an-k" style="left:56px;top:44px;font-size:22px;letter-spacing:.24em;opacity:0">{kick_html(text)}<div style="width:120px;height:1px;background:{GOLD};margin-top:8px"></div></div>')
        self.J(f"tl.fromTo('#{i}',{{opacity:0,x:-10}},{{opacity:1,x:0,duration:.5,ease:'power2.out',immediateRender:false}},{t:.3f});")
    # ---- figure helpers (js)
    def walk(self, p, hx, hy, s, t0, dur, dx=0, sel=None, per=.38):
        n = max(1, int(dur / per))
        self.J(f"tl.fromTo('#{p}-legL',{{rotation:16,svgOrigin:'{hx} {hy}'}},{{rotation:-16,svgOrigin:'{hx} {hy}',duration:{per},yoyo:true,repeat:{n},ease:'sine.inOut',immediateRender:false}},{t0:.3f});"
               f"tl.fromTo('#{p}-legR',{{rotation:-16,svgOrigin:'{hx} {hy}'}},{{rotation:16,svgOrigin:'{hx} {hy}',duration:{per},yoyo:true,repeat:{n},ease:'sine.inOut',immediateRender:false}},{t0:.3f});")
        if dx: self.J(f"tl.fromTo('{sel}',{{x:{-dx}}},{{x:0,duration:{dur:.3f},ease:'power1.out'}},{t0:.3f});")
        if sel: self.J(f"bob('{sel}',{t0:.3f},{dur:.3f},-4,.19);")
    def blink(self, p, times):
        for t in times: self.J(f"tl.to('#{p}-eyes',{{scaleY:.1,transformOrigin:'50% 50%',duration:.07,yoyo:true,repeat:1}},{t:.3f});")
    def idle(self, sel, t0=None, amp=-3, per=1.1):
        t0 = self.a + .3 if t0 is None else t0
        self.J(f"bob('{sel}',{t0:.3f},{max(.5, self.b - t0):.3f},{amp},{per});")
    # ---- output
    def done(self, cls='anim'):
        p = self.p
        js = [f"kb('#{p}-sc',{self.a:.3f},{self.b:.3f},{self.push[0]},{self.push[1]},'{self.push[2]}');"] if self.push else []
        if self.fade: js.append(f"tl.fromTo('#{p}-sc',{{opacity:0}},{{opacity:1,duration:{self.fade},ease:'none'}},{self.a:.3f});")
        fx = f'<svg class="an-ly" width="1280" height="720" viewBox="0 0 1280 720">{"".join(self.fx)}</svg>' if self.fx else ''
        inner = (f'<svg width="0" height="0" style="position:absolute"><defs>{"".join(self.defs)}</defs></svg>'
                 f'<div class="an-bg" style="background:{self.bg}"></div><div id="{p}-sc" class="an-sc">{"".join(self.layers)}{fx}{"".join(self.html)}</div>'
                 f'<div class="an-vig"></div>{"".join(self.top)}<div id="{p}-fl" class="an-fl"></div>')
        self.ctx.js.append('\n'.join(js + self.js))
        return dict(html=self.ctx.shot_div(inner, cls), css=CSS)
