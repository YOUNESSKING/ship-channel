"""Video 02 fix pass, batch B (ch04-ch08, scenes S07-S13 of videos/video02/plan/fixpass/PLAN.md): custom animation scenes.

One shared gold X-ray setup (`_xr_*` helpers: gold line art + scan line + glow + leader labels) is used by the three X-ray scenes
(S07 palate, S08 salt glands, S11 hippo vs croc). The hero croc is in true colours (templates/lib/anim_assets, PhyloPic CC0, recoloured)
or, in X-ray mode, gold line art. Look and motion: GOLD rules 95-100 (templates/tests_anim/, blocks/anim_common.py).
All times default to the narration words of the scene (wNNN), so the scenes stay in sync if a shot start moves."""
import math, os, random
from .common import fig, esc, rich, GOLD, WARM, SOFT, ICONS
from .anim_common import (Scene, BG, INK, person, organ_svg, xray_shape, kick_html, frond, reeds,
                          waterline, water_band, crowd)
from .croc_gfx import SHAPES, shape_svg

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, '..', 'lib', 'anim_assets'))
SWIM = (os.path.join(ASSETS, 'croc_porosus_swim.png'), 675 / 1600)   # faces right
GAPE = (os.path.join(ASSETS, 'croc_porosus_gape.png'), 758 / 1600)   # faces left, jaws open
OLIVE, OLIVE_D, BELLY, RIM = '#5a5630', '#3e3c22', '#a39466', '#d9b77a'

LONG_OK = ('xray_palate', 'xray_salt', 'lake_lock', 'scientist', 'xray_hippo', 'sea_options', 'body_temp')
META = dict(name='v02_anim_b', about='Video 02 fix pass, batch B custom scenes (PLAN.md S07-S13): "xray_palate" = croc head X-ray, bony roof + throat flap, '
            'holds prey underwater and breathes (S07); "xray_salt" = drying creek, backlit giants, our croc leaves along a gold path, X-ray salt glands (S08); '
            '"lake_lock" = Turkana lakeshore, gold ticks over the herds, camera to the water, lock-on brackets find the giant (S09); '
            '"scientist" = scientist + clipboard, ? card, shrug, quote types in, pan to the early humans (S10); "xray_hippo" = cold Thames, hippo vs croc in gold X-ray, '
            'heat / no heat, three gold X (S11); "sea_options" = way-out list, escape by sea, North Sea in winter mini scene, strike (S12); '
            '"body_temp" = basking croc, body-temperature gauge lands 32-33 C, dive + energy bars drain, croc hides in the shade (S13).',
  variants=list(LONG_OK),
  params={'at': 'optional dict of beat times {"name": time spec} overriding the word-based defaults of the variant (see the BEATS table in the code)',
          'kicker': 'optional caps kicker override (*word* = gold italic)'})

BEATS = {   # default beat times per variant (word specs from PLAN.md)
 'xray_palate': dict(xray='w877+0.45', bony='w879', roof_lab='w880', flap='w886', flap_lab='w889', open='w893', hold='w896', water='w904', breathe='w907', nose='w910'),
 'xray_salt': dict(croc='w1069', giants='w1074', leave='w1076', salt='w1079', go='w1083', sea='w1086'),
 'lake_lock': dict(food='w1128', problem='w1132', who='w1136', here='w1138'),
 'scientist': dict(asked='w1199', giant='w1202', said='w1206', quote='w1207', it='w1208', them='w1211'),
 'xray_hippo': dict(own='w1361', croc='w1364', cold='w1370', warm='w1373', digest='w1377', eating='w1380'),
 'sea_options': dict(box=0.35, salt='w1415', swim='w1421', north='w1424', winter='w1427'),
 'body_temp': dict(above='w1609', land='w1613', shorter='w1615', less='w1617', hottest='w1623', shade='w1628'),
}

def _T(ctx):
    over = ctx.p('at') or {}
    return {k: ctx.t(over.get(k, v)) for k, v in BEATS[ctx.variant].items()}

def J_from(sc, sel, frm, to, t):
    """fromTo with immediateRender:false (dicts given as js object text without braces)."""
    sc.J(f"tl.fromTo('{sel}',{{{frm}}},{{{to},immediateRender:false}},{t:.3f});")

def snap(sc, sel, t, dy=16, dur=.4, scale=None, origin='50% 50%'):
    """Snap in (strong ease-out)."""
    sc.J(f"gsap.set('{sel}',{{opacity:0}});")
    if scale: sc.J(f"tl.fromTo('{sel}',{{opacity:0,scale:{scale},transformOrigin:'{origin}'}},{{opacity:1,scale:1,duration:{dur},ease:'power3.out',immediateRender:false}},{t:.3f});")
    else: sc.J(f"tl.fromTo('{sel}',{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:'power3.out',immediateRender:false}},{t:.3f});")

def fade(sc, sel, t, to=0.0, dur=.35):
    sc.J(f"tl.to('{sel}',{{opacity:{to},duration:{dur}}},{t:.3f});")

def croc_img(ctx, gid, kind, x, ground, w, op=1.0, flip=False, rot=None):
    """True-colour croc image (swim: faces right; gape: faces left), box left x, bottom on `ground`, w px wide."""
    path, asp = SWIM if kind == 'swim' else GAPE
    h = w * asp; src = ctx.asset(path)
    if rot is None: rot = 19 if kind == 'swim' else 0     # the swim pose climbs ~19 deg: level it
    fl = f' transform="translate({2 * x + w:.0f},0) scale(-1,1)"' if flip else ''
    rt = f' transform="rotate({rot} {x + w / 2:.0f} {ground - h / 2:.0f})"' if rot else ''
    return f'<g id="{gid}" opacity="{op}"><g{rt}><g{fl}><image href="{src}" x="{x:.0f}" y="{ground - h:.0f}" width="{w:.0f}" height="{h:.0f}"/></g></g></g>', h

def soft(sc, cx, cy, rx, ry, col='#e0a24a', op=.12, gid=None):
    """Soft glow ellipse (radial gradient, no hard edge)."""
    k = len(sc.defs); gid = gid or f'{sc.p}-sg{k}'
    sc.defs.append(f'<radialGradient id="{gid}g"><stop offset="0" stop-color="{col}" stop-opacity="{op}"/><stop offset=".6" stop-color="{col}" stop-opacity="{op * .35:.3f}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
    return f'<ellipse id="{gid}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{gid}g)"/>'

def far_line(seed, y, col, x0=-80, x1=1420, h0=24, h1=70, w0=40, w1=110):
    """Far tree line: small rounded crowns along y (hazy far layer)."""
    r = random.Random(seed); s = ''; x = x0
    while x < x1:
        w = r.uniform(w0, w1); h = r.uniform(h0, h1)
        s += f'<ellipse cx="{x:.0f}" cy="{y - h * .45:.0f}" rx="{w * .6:.0f}" ry="{h * .55:.0f}" fill="{col}"/>'; x += w * .8
    return s + f'<rect x="{x0}" y="{y - 6}" width="{x1 - x0}" height="14" fill="{col}"/>'

def label(sc, i, text, x, y, t, size=26, align='left', w=None):
    """Caps label (Jost, *word* = gold italic) snapping in with a tick."""
    p = sc.p; ww = f'width:{w}px;' if w else ''
    sc.add_html(f'<div id="{p}-lb{i}" class="an-a an-k" style="left:{x:.0f}px;top:{y:.0f}px;{ww}text-align:{align};font-size:{size}px;opacity:0">{kick_html(text)}</div>')
    sc.J(f"tl.fromTo('#{p}-lb{i}',{{opacity:0,x:-14}},{{opacity:1,x:0,duration:.35,ease:'power3.out',immediateRender:false}},{t:.3f});")

def leader(i, p, pts, op=1.0):
    d = 'M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in pts)
    return (f'<path id="{p}-ld{i}" d="{d}" fill="none" stroke="{GOLD}" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity="{op}"/>'
            f'<circle id="{p}-ldc{i}" cx="{pts[0][0]:.0f}" cy="{pts[0][1]:.0f}" r="4.5" fill="{GOLD}" opacity="0"/>')

def draw_leader(sc, i, t):
    p = sc.p
    sc.J(f"tl.fromTo('#{p}-ld{i}',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.3,ease:'power2.out',immediateRender:false}},{t:.3f});"
         f"tl.fromTo('#{p}-ldc{i}',{{opacity:0}},{{opacity:1,duration:.1,immediateRender:false}},{t:.3f});")

def draw_path(sc, sel, t, dur=.5, ease='power2.out'):
    sc.J(f"tl.fromTo('{sel}',{{strokeDashoffset:1,opacity:1}},{{strokeDashoffset:0,duration:{dur},ease:'{ease}',immediateRender:false}},{t:.3f});")

def xmark_svg(i, x, y, r=16, sw=6):
    return f'<path id="{i}" d="M{x - r},{y - r} L{x + r},{y + r} M{x + r},{y - r} L{x - r},{y + r}" stroke="{GOLD}" stroke-width="{sw}" stroke-linecap="round" fill="none" opacity="0"/>'

def xmark_in(sc, sel, t):
    sc.J(f"tl.fromTo('{sel}',{{opacity:0,scale:1.8,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{t:.3f});")
    sc.sfx('click', t, .6); sc.sfx('thud', t + .02, .3)

def check_svg(i, x, y, k=1.0):
    return f'<path id="{i}" d="M{x - 14 * k:.0f},{y:.0f} L{x - 4 * k:.0f},{y + 11 * k:.0f} L{x + 16 * k:.0f},{y - 13 * k:.0f}" stroke="{GOLD}" stroke-width="{5 * k:.1f}" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0"/>'

def bubbles(sc, n, x0, x1, y0, y1, seed=1, col=SOFT):
    r = random.Random(seed); s = ''
    for i in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); rr = r.uniform(2, 5)
        s += f'<circle id="{sc.p}-bu{seed}_{i}" cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="none" stroke="{col}" stroke-width="1.5" opacity=".0"/>'
        per = r.uniform(1.4, 2.6)
        sc.J(f"tl.fromTo('#{sc.p}-bu{seed}_{i}',{{y:0,opacity:.55}},{{y:{-r.uniform(60, 140):.0f},opacity:0,duration:{per:.2f},repeat:{int(sc.D / per) + 1},ease:'none'}},{sc.a + r.uniform(0, 1.2):.3f});")
    return s

def snow(sc, n=60, seed=9, wind=60, fast=False, lid=None, t0=None, col='#eef2ea'):
    """Drifting snow flakes (pale warm white)."""
    r = random.Random(seed); s = ''; t0 = sc.a if t0 is None else t0; D = sc.b - t0
    for i in range(n):
        x = r.uniform(-100, 1300); y = r.uniform(-40, 700); rr = r.uniform(1.2, 3.2)
        s += f'<circle id="{sc.p}-sn{seed}_{i}" cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="{col}" opacity="{r.uniform(.35, .85):.2f}"/>'
        per = r.uniform(.5, .9) if fast else r.uniform(2.5, 4.5)
        dx = (r.uniform(260, 420) if fast else r.uniform(-wind, wind)); dy = r.uniform(60, 140) if fast else r.uniform(80, 200)
        sc.J(f"tl.fromTo('#{sc.p}-sn{seed}_{i}',{{x:0,y:0}},{{x:{dx:.0f},y:{dy:.0f},duration:{per:.2f},repeat:{int(D / per) + 1},ease:'none',immediateRender:false}},{t0 + r.uniform(0, per):.3f});")
    sc.svg(s, lid=lid)

# ================================================================== S07: croc head X-ray, bony palate + throat flap
HINGE = (470, 372)

def _head_paths():
    skull = ('M-40,318 C120,300 260,292 380,292 C470,290 560,286 600,282 C630,272 668,272 690,290 C760,300 900,312 1040,316 '
             'C1052,302 1080,302 1090,314 C1104,322 1114,334 1110,346 C1104,354 1092,356 1080,356 L470,372 C440,382 420,396 420,410 '
             'L420,420 C300,440 160,460 -40,470 Z')
    jaw = 'M470,372 L1092,358 C1102,360 1104,368 1096,372 C1050,384 960,398 840,404 C700,412 560,420 470,420 C440,418 430,400 440,384 Z'
    return skull, jaw

def _teeth(y0, x0, x1, n, up):
    s = ''
    for k in range(n):
        x = x0 + (x1 - x0) * k / (n - 1); y = y0(x)
        s += f'M{x - 6:.0f},{y:.0f} L{x:.0f},{y + (12 if not up else -12):.0f} L{x + 6:.0f},{y:.0f} '
    return s

def build_xray_palate(ctx, sc, T):
    p = sc.p; a = sc.a; b = sc.b
    WL = 330
    skull, jaw = _head_paths()
    up_line = lambda x: 356 + (1080 - x) / (1080 - 470) * 16      # upper tooth line y
    lo_line = lambda x: 358 + (1092 - x) / (1092 - 470) * 14
    teeth_up = _teeth(up_line, 520, 1070, 14, False)
    teeth_lo = _teeth(lo_line, 530, 1060, 13, True)
    sc.defs.append(f'<linearGradient id="{p}-cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{OLIVE}"/><stop offset=".7" stop-color="{OLIVE_D}"/><stop offset="1" stop-color="{BELLY}"/></linearGradient>')
    # sky glow + far water haze (layered)
    sc.svg(soft(sc, 900, 130, 560, 200, '#e0a24a', .14) + far_line(4, WL - 4, '#1b3529', h0=18, h1=46), drift=-14)
    scutes = ''.join(f'<path d="M{x},{300 - (6 if 380 < x < 700 else 0)} q14,-16 28,0" fill="none" stroke="{RIM}" stroke-width="3" opacity=".7"/>' for x in range(-20, 380, 46))
    col_head = (f'<g class="{p}-col"><path d="{skull}" fill="url(#{p}-cg)" stroke="{RIM}" stroke-width="3" stroke-linejoin="round"/>{scutes}'
                f'<path d="{teeth_up}" fill="#efe6cc" stroke="none"/><circle cx="642" cy="286" r="9" fill="#e9c46a"/><circle cx="642" cy="286" r="4" fill="#1a1406"/>'
                f'<ellipse cx="1076" cy="312" rx="7" ry="4" fill="#1a1406"/></g>')
    col_jaw = f'<g class="{p}-col"><path d="{jaw}" fill="url(#{p}-cg)" stroke="{RIM}" stroke-width="3" stroke-linejoin="round"/><path d="{teeth_lo}" fill="#efe6cc"/></g>'
    ribs = ''.join(f'<path d="M{x},{330 + (x + 40) * .02:.0f} q16,60 0,120" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width="2.5"/>' for x in range(-20, 380, 40))
    xr_head = (f'<g class="{p}-xr" opacity="0"><path d="{skull}" fill="{GOLD}" fill-opacity=".05" stroke="{GOLD}" stroke-width="3" stroke-linejoin="round"/>{ribs}'
               f'<path d="{teeth_up}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-opacity=".75"/><circle cx="642" cy="286" r="9" fill="none" stroke="{GOLD}" stroke-width="2.5"/>'
               f'<ellipse cx="1076" cy="312" rx="7" ry="4" fill="{GOLD}"/><path d="M-30,330 C100,322 260,318 380,320" fill="none" stroke="{GOLD}" stroke-opacity=".4" stroke-width="2.4" stroke-dasharray="8 7"/></g>')
    xr_jaw = f'<g class="{p}-xr" opacity="0"><path d="{jaw}" fill="{GOLD}" fill-opacity=".05" stroke="{GOLD}" stroke-width="3" stroke-linejoin="round"/><path d="{teeth_lo}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-opacity=".75"/></g>'
    # bony roof (palate): nostril -> throat, glows on "bony"
    palate = f'M1078,344 C900,350 700,356 476,364'
    # throat flap (gular valve): hangs from the back of the palate, starts folded up
    flap = f'<g id="{p}-flap" opacity="0"><path d="M462,366 C470,380 470,398 458,414" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/></g>'
    # water in the open mouth: between the palate and the open lower jaw (jaw open = rotated 14 deg about the hinge)
    ang = math.radians(14); hx, hy = HINGE
    def rot(x, y): dx, dy = x - hx, y - hy; return hx + dx * math.cos(ang) - dy * math.sin(ang), hy + dx * math.sin(ang) + dy * math.cos(ang)
    lo = [rot(x, lo_line(x) + 4) for x in range(1080, 470, -60)]
    wpoly = 'M470,370 L1086,354 ' + ' '.join(f'L{x:.0f},{y:.0f}' for x, y in lo) + ' Z'
    water_in = f'<path id="{p}-win" d="{wpoly}" fill="#3f7a5a" fill-opacity=".55" stroke="#9fd0b0" stroke-opacity=".5" stroke-width="2" opacity="0"/>'
    # prey: a fish in the jaws
    fsc = .16; fx0, fy0 = 850, 446
    prey = (f'<g id="{p}-prey" opacity="0"><g transform="translate({fx0},{fy0}) scale({fsc}) rotate(-8)">'
            f'{shape_svg("fish", WARM, 3 / fsc, .95).replace("fill=\"#1a2429\"", f"fill=\"{INK}\"")}</g></g>')
    lungs = f'<g id="{p}-lung" opacity="0">{organ_svg("lungs", 170, 405, 34)}</g><circle id="{p}-lg" cx="170" cy="405" r="110" fill="url(#{p}-og)" opacity="0"/>'
    airway = f'<path id="{p}-air" d="M1076,322 C980,334 760,340 520,350 C470,352 440,360 430,380 C420,396 360,400 300,402 L200,404" fill="none" stroke="{GOLD}" stroke-opacity=".55" stroke-width="2.5" stroke-dasharray="6 7" opacity="0"/>'
    roof = f'<path id="{p}-roof" d="{palate}" fill="none" stroke="{GOLD}" stroke-width="9" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    roofglow = f'<path id="{p}-roofg" d="{palate}" fill="none" stroke="#ffe2a0" stroke-width="22" stroke-linecap="round" opacity="0" style="filter:blur(6px)"/>'
    jaw_g = f'<g id="{p}-jaw">{col_jaw}{xr_jaw}</g>'
    sc.svg(f'<g id="{p}-head">{lungs}{airway}{col_head}{xr_head}{water_in}{roofglow}{roof}{flap}{jaw_g}{prey}</g>', lid=f'{p}-HL')
    # water over the lower half (head is half under the wave line) + glints + bubbles
    wl = sc.svg(f'<path d="{waterline(WL, -200, 1500, 6, 150)} V760 H-200 Z" fill="#0b2018" fill-opacity=".42"/>'
                f'<path id="{p}-wv" d="{waterline(WL, -200, 1500, 6, 150)}" fill="none" stroke="{SOFT}" stroke-width="2.5" stroke-opacity=".6"/>'
                + ''.join(f'<path class="gl" d="M{x},{y} h{w}" stroke="{SOFT}" stroke-width="2" stroke-linecap="round" opacity=".2"/>' for x, y, w in
                          ((80, 520, 90), (300, 600, 60), (620, 560, 110), (900, 640, 70), (1100, 500, 80), (200, 680, 120), (760, 690, 60)))
                + bubbles(sc, 14, 520, 1080, 440, 700, 3))
    sc.glints(wl)
    sc.J(f"tl.fromTo('#{p}-wv',{{x:0}},{{x:-75,duration:1.6,yoyo:true,repeat:{int(sc.D / 1.6) + 1},ease:'sine.inOut'}},{a:.3f});")
    # ---- head snaps in (true colours), bobs at the surface
    snap(sc, f'#{p}-HL', a + .02, dy=24, dur=.45)
    sc.J(f"tl.fromTo('#{p}-head',{{y:0}},{{y:5,duration:1.3,yoyo:true,repeat:{int(sc.D / 1.3) + 1},ease:'sine.inOut',immediateRender:false}},{a + .5:.3f});")
    sc.sfx('swoosh', a + .02, .3)
    # ---- switch to gold X-ray with a scan line
    xt = T['xray']
    sc.J(f"tl.to('.{p}-col',{{opacity:0,duration:.4}},{xt:.3f});tl.to('.{p}-xr',{{opacity:1,duration:.4}},{xt:.3f});")
    sc.flash(xt, .12); sc.sfx('shimmer', xt, .4)
    sc.fx.append(f'<g id="{p}-scan" opacity="0"><rect x="-20" y="{220 - 60}" width="1320" height="60" fill="url(#{p}-scg)"/><line x1="-20" y1="220" x2="1300" y2="220" stroke="{GOLD}" stroke-width="2.5" opacity=".8"/></g>')
    n = max(1, int((b - xt - .3) / 2.0))
    sc.J(f"tl.fromTo('#{p}-scan',{{opacity:0}},{{opacity:.85,duration:.2,immediateRender:false}},{xt:.3f});"
         f"tl.fromTo('#{p}-scan',{{y:0}},{{y:260,duration:2.0,yoyo:true,repeat:{n},ease:'sine.inOut',immediateRender:false}},{xt:.3f});")
    # ---- bony roof glows
    bt = T['bony']
    draw_path(sc, f'#{p}-roof', bt, .9, 'power2.inOut')
    sc.J(f"tl.fromTo('#{p}-roofg',{{opacity:0}},{{opacity:.55,duration:.5,immediateRender:false}},{bt + .5:.3f});"
         f"tl.to('#{p}-roofg',{{opacity:.25,duration:1.1,yoyo:true,repeat:{int((b - bt) / 1.1)},ease:'sine.inOut'}},{bt + 1.0:.3f});")
    sc.sfx('shimmer', bt, .55)
    lab = leader(0, p, [(780, 350), (780, 205), (800, 205)])
    label(sc, 0, 'BONY *roof*', 812, 186, T['roof_lab'] + .25)
    # ---- throat flap swings shut
    ft = T['flap']
    sc.J(f"tl.fromTo('#{p}-flap',{{rotation:-75,svgOrigin:'462 366'}},{{rotation:0,svgOrigin:'462 366',duration:.35,ease:'back.out(2)',immediateRender:false}},{ft + .1:.3f});")
    sc.J(f"gsap.set('#{p}-flap',{{rotation:-75,svgOrigin:'462 366'}});")
    sc.J(f"tl.fromTo('#{p}-flap',{{opacity:0}},{{opacity:1,duration:.25,immediateRender:false}},{ft - .15:.3f});")
    sc.sfx('click', ft + .4, .7); sc.sfx('thud', ft + .42, .25)
    lab += leader(1, p, [(458, 400), (330, 205), (300, 205)])
    label(sc, 1, 'THROAT *flap*', 60, 186, T['flap_lab'])
    sc.svg(lab)
    draw_leader(sc, 0, T['roof_lab']); draw_leader(sc, 1, T['flap_lab'] - .2)
    # ---- jaws open, prey thrashes
    ot = T['open']; ht = T['hold']
    sc.J(f"tl.fromTo('#{p}-jaw',{{rotation:0,svgOrigin:'{HINGE[0]} {HINGE[1]}'}},{{rotation:14,svgOrigin:'{HINGE[0]} {HINGE[1]}',duration:.45,ease:'power3.out',immediateRender:false}},{ot:.3f});")
    sc.sfx('el:jaws_snap', ot, .25)
    sc.J(f"tl.fromTo('#{p}-prey',{{opacity:0,x:120}},{{opacity:1,x:0,duration:.4,ease:'power3.out',immediateRender:false}},{ht - .1:.3f});")
    nt = T['nose']; thr = max(1, int((nt - ht) / .14))
    sc.J(f"tl.fromTo('#{p}-prey',{{rotation:-9,svgOrigin:'{fx0 + 90} {fy0 - 25}'}},{{rotation:9,svgOrigin:'{fx0 + 90} {fy0 - 25}',duration:.14,yoyo:true,repeat:{thr},ease:'sine.inOut',immediateRender:false}},{ht + .3:.3f});")
    sc.sfx('el:fish_splash', ht + .2, .45); sc.sfx('el:fish_splash', ht + 1.6, .3)
    sc.svg(bubbles(sc, 10, 860, 1060, 400, 470, 7))
    # ---- water fills the mouth, stops at the closed flap
    wt = T['water']
    sc.J(f"tl.fromTo('#{p}-win',{{opacity:0,scaleX:.05,transformOrigin:'100% 50%'}},{{opacity:1,scaleX:1,duration:.8,ease:'power2.out',immediateRender:false}},{wt:.3f});")
    sc.sfx('el:sink_bubbles', wt, .3)
    sc.svg(leader(2, p, [(500, 395), (560, 560), (590, 560)]))
    draw_leader(sc, 2, wt + .7)
    label(sc, 2, 'WATER *stops here*', 600, 541, wt + .8)
    sc.J(f"tl.fromTo('#{p}-flap',{{scale:1}},{{scale:1.15,transformOrigin:'50% 50%',duration:.25,yoyo:true,repeat:1,immediateRender:false}},{wt + .75:.3f});")
    # ---- breathe: air dots nostril -> roof -> past the flap -> lungs
    brt = T['breathe']
    pts = [(1076, 318), (980, 334), (760, 341), (520, 350), (440, 366), (420, 396), (300, 402), (200, 404)]
    dots = ''
    for k in range(7):
        dots += f'<circle id="{p}-ad{k}" cx="0" cy="0" r="6" fill="#ffe2a0" opacity="0"/>'
        kf = ','.join(f"{{x:{x},y:{y},duration:{.18 if i else .01}}}" for i, (x, y) in enumerate(pts))
        st = brt + k * .14
        sc.J(f"gsap.set('#{p}-ad{k}',{{x:{pts[0][0]},y:{pts[0][1]}}});tl.set('#{p}-ad{k}',{{opacity:1}},{st:.3f});tl.to('#{p}-ad{k}',{{keyframes:[{kf}],ease:'none'}},{st:.3f});tl.to('#{p}-ad{k}',{{opacity:0,duration:.15}},{st + 1.3:.3f});")
    sc.svg(dots)
    sc.J(f"tl.fromTo('#{p}-air',{{opacity:0}},{{opacity:1,duration:.3,immediateRender:false}},{brt - .1:.3f});")
    sc.sfx('swoosh', brt, .3); sc.sfx('el:sink_bubbles', brt + .1, .15)
    # ---- nose: lungs pulse gold once, prey goes still
    sc.J(f"tl.fromTo('#{p}-lung',{{opacity:0,scale:.4,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.35,ease:'back.out(2)',immediateRender:false}},{nt - .3:.3f});"
         f"tl.fromTo('#{p}-lung',{{scale:1}},{{scale:1.25,transformOrigin:'50% 50%',duration:.25,yoyo:true,repeat:1,immediateRender:false}},{nt + .15:.3f});"
         f"tl.fromTo('#{p}-lg',{{opacity:0}},{{opacity:1,duration:.3,yoyo:true,repeat:1,immediateRender:false}},{nt + .15:.3f});"
         f"tl.to('#{p}-prey',{{opacity:.55,duration:.4}},{nt + .2:.3f});")
    sc.sfx('heart', nt + .15, .5); sc.sfx('shimmer', nt + .15, .35)
    sc.kicker(ctx.p('kicker', 'Inside the *croc*'), a + .2, y=56, x=60, w=900, align='left', size=26)

# ================================================================== S08: drying creek, salt glands, out to sea
def build_xray_salt(ctx, sc, T):
    p = sc.p; a = sc.a; b = sc.b
    GY = 600
    # sky glow (hot, dry) + far hazy trees + dry grass
    sc.svg(soft(sc, 900, 150, 640, 230, '#e0a24a', .18) + soft(sc, 1010, 130, 110, 110, '#f3dca0', .35) + '<circle cx="1010" cy="130" r="40" fill="#f3dca0" opacity=".6"/>')
    sc.svg(far_line(5, 470, '#2c4636', h0=26, h1=60) + far_line(6, 482, '#24402f', h0=14, h1=34, x1=980), drift=-12)
    sc.svg(reeds(6, 40, 470, 490, '#3a5236', 30, 80, -60, 900), drift=-20, sway=1.2)
    # sea edge on the right with surf
    sea = (f'<path d="M1010,470 C1040,520 1060,560 1080,760 L1500,760 L1500,470 Z" fill="#14271f"/>'
           + ''.join(f'<path id="{p}-sf{k}" d="M{1030 + k * 18},{480 + k * 55} q30,-10 60,0 t60,0 t60,0 t60,0" fill="none" stroke="{SOFT}" stroke-width="2.5" stroke-opacity=".55"/>' for k in range(5)))
    sc.svg(sea)
    for k in range(5):
        sc.J(f"tl.fromTo('#{p}-sf{k}',{{x:0}},{{x:-28,duration:{1.1 + k * .15:.2f},yoyo:true,repeat:{int(sc.D / 1.1) + 1},ease:'sine.inOut'}},{a:.3f});")
    # cracked mud ground + the last pool
    r = random.Random(11); cracks = ''
    for _ in range(26):
        x = r.uniform(-40, 1000); y = r.uniform(500, 700)
        cracks += f'<path d="M{x:.0f},{y:.0f} l{r.uniform(20, 50):.0f},{r.uniform(-12, 12):.0f} l{r.uniform(10, 40):.0f},{r.uniform(-14, 14):.0f}" stroke="#2a2416" stroke-width="2.4" fill="none" opacity=".75"/>'
    ground = (f'<path d="M-100,490 C200,482 600,486 1010,470 C1040,520 1060,560 1080,760 L-100,760 Z" fill="#5b4a2e" opacity=".55"/>'
              f'<path d="M-100,490 C200,482 600,486 1010,470" fill="none" stroke="{SOFT}" stroke-opacity=".35" stroke-width="2"/>{cracks}'
              f'<ellipse cx="300" cy="545" rx="210" ry="34" fill="#13261d"/><ellipse id="{p}-pl" cx="300" cy="545" rx="210" ry="34" fill="none" stroke="{SOFT}" stroke-opacity=".5" stroke-width="2"/>')
    sc.svg(ground)
    sc.J(f"tl.fromTo('#{p}-pl',{{attr:{{rx:206}}}},{{attr:{{rx:196}},duration:{sc.D:.2f},ease:'none'}},{a:.3f});")
    # backlit giants at the pool (Paludirex-like freshwater croc 7 m + Megalania)
    disc = f'<defs><radialGradient id="{p}-dg"><stop offset="0" stop-color="#f3dca0" stop-opacity=".55"/><stop offset=".55" stop-color="#e0a24a" stop-opacity=".18"/><stop offset="1" stop-color="#e0a24a" stop-opacity="0"/></radialGradient></defs>'
    gi = (f'<g id="{p}-gi">{disc}<ellipse cx="330" cy="480" rx="420" ry="170" fill="url(#{p}-dg)"/>'
          f'<g transform="translate(20,530) scale(.38)">{shape_svg("croc", "#050403", 1, 1).replace("fill=\"#1a2429\"", "fill=\"#050403\"")}</g>'
          f'<g transform="translate(400,522) translate(260,0) scale(-.26,.26)">{shape_svg("monitor", "#050403", 1, 1).replace("fill=\"#1a2429\"", "fill=\"#050403\"")}</g></g>')
    sc.svg(gi)
    snap(sc, f'#{p}-gi', a + .05, dy=10, dur=.45)
    sc.J(f"tl.fromTo('#{p}-gi',{{x:0}},{{x:-12,duration:{sc.D:.2f},ease:'none'}},{a:.3f});")
    label(sc, 0, 'THE *giants*', 170, 400, a + .5, size=24)
    # our croc, true colours, front
    cx0, cw = 560, 320
    img, ch = croc_img(ctx, f'{p}-cc', 'gape', cx0, 650, cw, flip=True)
    xr = f'<g id="{p}-cx" opacity="0">{xray_shape(p + "x", "croc", cx0 + 10, 628, cw - 20)}</g>'
    gx, gy = cx0 + 10 + .90 * (cw - 20), 628 - .45 * .15 * (cw - 20)   # tongue / salt gland near the head
    gland = f'<g id="{p}-gl" opacity="0">{organ_svg("gland", gx, gy, 16)}</g><circle id="{p}-glg" cx="{gx:.0f}" cy="{gy:.0f}" r="60" fill="url(#{p}-og)" opacity="0"/>'
    drops = ''.join(f'<path id="{p}-dr{k}" d="M{gx - 10 + k * 10:.0f},{gy + 8:.0f} q-4,8 0,12 q4,-4 0,-12 z" fill="#f6efe0" opacity="0"/>' for k in range(3))
    sc.svg(f'<g id="{p}-ours">{img}{xr}{gland}{drops}</g>', lid=f'{p}-OL')
    ct = T['croc']
    snap(sc, f'#{p}-OL', ct, dy=20, dur=.4); sc.sfx('el:reeds_rustle', ct, .35); sc.sfx('swoosh', ct, .25)
    sc.J(f"tl.fromTo('#{p}-ours',{{y:0}},{{y:-4,duration:1.0,yoyo:true,repeat:{int(sc.D)},ease:'sine.inOut',immediateRender:false}},{ct + .4:.3f});")
    label(sc, 1, 'OUR *croc*', cx0 + 60, 664, ct + .3, size=24)
    # giants dim
    gt = T['giants']
    sc.J(f"tl.to('#{p}-gi',{{opacity:.35,duration:.5}},{gt:.3f});tl.to('#{p}-lb0',{{opacity:.35,duration:.5}},{gt:.3f});")
    sc.sfx('thud', gt, .25)
    # gold dotted path to the sea
    lt = T['leave']
    path = f'M{cx0 + cw - 10},600 C{cx0 + cw + 90},590 960,560 1130,540'
    sc.svg(f'<path id="{p}-pth" d="{path}" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 14" opacity="0" mask="url(#{p}-mk)"/>'
           f'<path id="{p}-arr" d="M1112,524 L1140,538 L1114,556" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0"/>')
    sc.defs.append(f'<mask id="{p}-mk" maskUnits="userSpaceOnUse" x="0" y="0" width="1280" height="720"><path id="{p}-mkp" d="{path}" fill="none" stroke="#fff" stroke-width="20" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></mask>')
    sc.J(f"tl.set('#{p}-pth',{{opacity:1}},{lt:.3f});"
         f"tl.fromTo('#{p}-mkp',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.8,ease:'power2.inOut',immediateRender:false}},{lt:.3f});"
         f"tl.fromTo('#{p}-arr',{{opacity:0,x:-12}},{{opacity:1,x:0,duration:.3,ease:'power3.out',immediateRender:false}},{lt + .7:.3f});")
    sc.sfx('swoosh', lt, .45)
    label(sc, 2, 'THE *sea*', 1080, 420, lt + .5, size=26)
    # X-ray: salt glands glow, drops fall
    st = T['salt']
    sc.J(f"tl.to('#{p}-cc',{{opacity:0,duration:.3}},{st - .1:.3f});tl.fromTo('#{p}-cx',{{opacity:0}},{{opacity:1,duration:.3,immediateRender:false}},{st - .1:.3f});"
         f"tl.fromTo('#{p}-gl',{{opacity:0,scale:.3,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.35,ease:'back.out(2)',immediateRender:false}},{st + .1:.3f});"
         f"tl.fromTo('#{p}-glg',{{opacity:0}},{{opacity:1,duration:.3,yoyo:true,repeat:3,immediateRender:false}},{st + .1:.3f});")
    sc.flash(st - .1, .1); sc.sfx('shimmer', st - .1, .45)
    sc.fx.append(f'<g id="{p}-scan" opacity="0"><rect x="{cx0 - 20}" y="510" width="{cw + 40}" height="40" fill="url(#{p}-scg)"/><line x1="{cx0 - 20}" y1="550" x2="{cx0 + cw + 20}" y2="550" stroke="{GOLD}" stroke-width="2.5"/></g>')
    sc.J(f"tl.fromTo('#{p}-scan',{{opacity:0,y:0}},{{opacity:.9,y:0,duration:.15,immediateRender:false}},{st - .1:.3f});tl.to('#{p}-scan',{{y:90,duration:.6,yoyo:true,repeat:1,ease:'sine.inOut'}},{st:.3f});tl.to('#{p}-scan',{{opacity:0,duration:.2}},{st + 1.25:.3f});")
    for k in range(3):
        dt = st + .45 + k * .3
        sc.J(f"tl.fromTo('#{p}-dr{k}',{{opacity:1,y:0}},{{opacity:0,y:46,duration:.5,ease:'power1.in',immediateRender:false}},{dt:.3f});")
        sc.sfx('tick', dt + .45, .35)
    sc.svg(leader(3, p, [(gx, gy - 6), (gx - 40, 440), (gx - 70, 440)]))
    draw_leader(sc, 3, st + .2)
    label(sc, 3, 'SALT *glands*', gx - 300, 421, st + .35, size=26)
    # back to colour, slide along the path into the surf
    gt2 = T['go']
    sc.J(f"tl.to('#{p}-cx',{{opacity:0,duration:.3}},{gt2 - .1:.3f});tl.to('#{p}-cc',{{opacity:1,duration:.3}},{gt2 - .1:.3f});tl.to('#{p}-gl,#{p}-lb1,#{p}-lb3,#{p}-ld3,#{p}-ldc3',{{opacity:0,duration:.25}},{gt2 - .1:.3f});"
         f"tl.to('#{p}-OL',{{x:330,y:-60,duration:{max(.6, b - gt2 + .2):.2f},ease:'power1.in'}},{gt2:.3f});")
    sc.sfx('el:reeds_rustle', gt2, .3); sc.sfx('el:splash_small', T['sea'] + .05, .5)
    sc.dust(26, 21)
    sc.kicker(ctx.p('kicker', 'Our croc can *leave*'), a + .25, y=56, x=60, w=900, align='left', size=26)

# ================================================================== S09: Turkana lakeshore, ticks, lock-on the giant
def _beast(kind, x, y, k=1.0, col=WARM):
    st = f'fill="{INK}" stroke="{col}" stroke-width="{3 / k:.1f}" stroke-linejoin="round" stroke-linecap="round"'
    if kind == 'antelope':
        d = (f'<path d="M-30,-40 C-20,-52 20,-52 30,-42 L44,-62 L54,-58 L46,-36 C44,-30 36,-30 30,-32 L28,-30 C10,-26 -10,-26 -30,-30 Z" {st}/>'
             f'<path d="M48,-60 l-6,-22 M52,-60 l2,-22 M-26,-30 v32 M-16,-30 v32 M20,-30 v32 M28,-30 v32 M-30,-38 l-10,10" fill="none" stroke="{col}" stroke-width="{3 / k:.1f}" stroke-linecap="round"/>')
    elif kind == 'pig':
        d = (f'<path d="M-34,-18 C-34,-46 30,-50 36,-26 L50,-24 L50,-14 L36,-12 C30,-2 -28,0 -34,-18 Z" {st}/>'
             f'<path d="M-24,-6 v8 M-12,-4 v8 M16,-4 v8 M26,-6 v8 M30,-38 l4,-8 l4,8" fill="none" stroke="{col}" stroke-width="{3 / k:.1f}" stroke-linecap="round"/>')
    else:   # three-toed horse
        d = (f'<path d="M-34,-36 C-30,-50 22,-50 30,-40 L44,-66 C48,-72 58,-70 60,-62 L52,-50 L40,-34 C36,-28 28,-28 22,-28 C0,-24 -20,-24 -34,-30 Z" {st}/>'
             f'<path d="M-30,-30 v32 M-20,-28 v30 M16,-28 v30 M26,-30 v32 M-34,-36 q-12,6 -10,22" fill="none" stroke="{col}" stroke-width="{3 / k:.1f}" stroke-linecap="round"/>')
    return f'<g transform="translate({x},{y}) scale({k})">{d}</g>'

def build_lake_lock(ctx, sc, T):
    p = sc.p; a = sc.a; b = sc.b
    SH = 410; CAM = -170
    sky = (soft(sc, 900, 160, 600, 220, '#e0a24a', .18) + f'<circle cx="960" cy="140" r="40" fill="#f3dca0" opacity=".55"/>'
           f'<path d="M-100,330 C120,290 300,300 480,320 C700,280 900,290 1100,310 C1250,300 1380,320 1400,330 L1400,{SH} L-100,{SH} Z" fill="#2c4a3a"/>')
    # whole world (moves down = camera tilts to the water)
    world = []
    world.append(sky)
    world.append(far_line(8, SH - 60, '#24432f', h0=20, h1=50))
    world.append(f'<path d="M-100,{SH - 20} C300,{SH - 30} 900,{SH - 10} 1400,{SH - 22} L1400,{SH + 10} L-100,{SH + 10} Z" fill="#3b5534"/>')
    world.append(reeds(9, 26, SH - 4, SH + 8, '#203c2a', 26, 70))
    sc.svg(f'<g id="{p}-w0">{"".join(world)}</g>', lid=f'{p}-W0', drift=-18, sway=1.0)
    # herds + tiny early humans along the shore
    groups = [('antelope', 190, 3), ('pig', 430, 3), ('horse', 680, 3)]
    hs = ''
    for gi, (kind, x0, n) in enumerate(groups):
        g = ''.join(_beast(kind, x0 + i * 56, SH + 2 - (i % 2) * 6, .8 + .1 * (i % 2)) for i in range(n))
        hs += f'<g id="{p}-h{gi}">{g}</g>'
    hs += f'<g id="{p}-h3">{crowd(985, SH + 4, 5, 18)}</g>'
    ticks = ''.join(check_svg(f'{p}-tk{gi}', x, SH - 92, 1.2) for gi, x in enumerate((246, 486, 736, 985)))
    # water + the dark shape under the surface
    WY = SH + 14
    water = (f'<path d="{waterline(WY, -200, 1500, 5, 130)} V900 H-200 Z" fill="#12281f"/>'
             + soft(sc, 960, WY + 230, 170, 300, '#f3dca0', .22) + soft(sc, 640, WY + 260, 700, 200, '#3f6a4c', .35)
             + f'<path d="{waterline(WY, -200, 1500, 5, 130)}" fill="none" stroke="{SOFT}" stroke-opacity=".5" stroke-width="2.4"/>')
    r = random.Random(3)
    for k in range(18):
        yy = WY + 20 + r.uniform(0, 420); x = r.uniform(-50, 1300); w = r.uniform(30, 110)
        water += f'<path class="gl" d="M{x:.0f},{yy:.0f} h{w:.0f}" stroke="{SOFT}" stroke-width="2" stroke-linecap="round" opacity="{r.uniform(.12, .3):.2f}"/>'
    for k in range(16):   # moon glints on the water (column under the moon)
        yy = WY + 30 + k * 26 + r.uniform(-6, 6); w = r.uniform(30, 90) * (1 + k * .04); x = 960 - w / 2 + r.uniform(-30, 30)
        water += f'<path class="gl" d="M{x:.0f},{yy:.0f} h{w:.0f}" stroke="#f3dca0" stroke-width="3" stroke-linecap="round" opacity="{r.uniform(.45, .8):.2f}"/>'
    shx, shy, shw = 560, WY + 250, 420
    shape = (f'<g id="{p}-sh" opacity="0"><g transform="translate({shx},{shy}) scale({shw / 1000:.3f})">'
             f'{shape_svg("croc", "#020403", 1, 1).replace("fill=\"#1a2429\"", "fill=\"#020403\"").replace("<path", f"<path stroke=\"{RIM}\" stroke-opacity=\".6\" stroke-width=\"7\"", 1)}</g></g>')
    ex, ey = shx + .85 * shw, shy - .128 * shw
    eyes = (f'<g id="{p}-ey" opacity="0"><circle cx="{ex - 8:.0f}" cy="{ey:.0f}" r="5" fill="#ffe9a8"/><circle cx="{ex + 10:.0f}" cy="{ey:.0f}" r="5" fill="#ffe9a8"/>'
            f'<circle cx="{ex + 1:.0f}" cy="{ey:.0f}" r="22" fill="url(#{p}-eg)" opacity=".7"/></g>')
    rip = ''.join(f'<ellipse id="{p}-rp{k}" cx="{ex:.0f}" cy="{ey + 8:.0f}" rx="30" ry="7" fill="none" stroke="{SOFT}" stroke-width="2.2" opacity="0"/>' for k in range(3))
    wl = sc.svg(f'<g id="{p}-w1">{water}{rip}{shape}{eyes}{hs}{ticks}</g>', lid=f'{p}-W1')
    sc.glints(wl)
    # dim overlay
    sc.top.append(f'<div id="{p}-dim" style="position:absolute;left:0;top:0;width:1280px;height:720px;background:#020403;opacity:0"></div>')
    # herds walk / drink
    for gi in range(4):
        sc.J(f"tl.fromTo('#{p}-h{gi}',{{x:0}},{{x:{(-1) ** gi * 14},duration:{1.3 + gi * .2:.2f},yoyo:true,repeat:{int(sc.D) + 1},ease:'sine.inOut'}},{a:.3f});")
    # ticks one by one
    ft = T['food']
    for gi in range(4):
        t = ft + gi * .38
        sc.J(f"tl.fromTo('#{p}-tk{gi}',{{opacity:0,scale:.2,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.3,ease:'back.out(2.5)',immediateRender:false}},{t:.3f});")
        sc.sfx('tick', t, .55)
    label(sc, 0, 'PLENTY OF *food*', 0, 120, ft + 1.6, size=30, align='center', w=1280)
    # problem: dim + camera to the water
    pt = T['problem']
    sc.J(f"tl.to('#{p}-dim',{{opacity:.16,duration:1.0}},{pt:.3f});tl.to('#{p}-W0,#{p}-W1',{{y:{CAM},duration:1.3,ease:'power2.inOut'}},{pt:.3f});"
         f"tl.to('#{p}-lb0',{{opacity:0,duration:.4}},{pt:.3f});")
    sc.sfx('swoosh', pt, .3)
    sc.J(f"tl.fromTo('#{p}-sh',{{opacity:0}},{{opacity:1,duration:.8,immediateRender:false}},{pt + .4:.3f});"
         f"tl.fromTo('#{p}-sh',{{x:-60,scale:.85,transformOrigin:'50% 50%'}},{{x:20,scale:1.15,duration:{max(1, b - pt - .4):.2f},ease:'sine.inOut',immediateRender:false}},{pt + .4:.3f});")
    for k in range(3):
        sc.J(f"tl.fromTo('#{p}-rp{k}',{{opacity:.7,attr:{{rx:30,ry:7}}}},{{opacity:0,attr:{{rx:130,ry:24}},duration:1.5,repeat:{int((b - pt) / 1.5)},ease:'power1.out',immediateRender:false}},{pt + .6 + k * .5:.3f});")
    # reed silhouettes at the sides (foreground, fade in with the drop)
    sc.svg(f'<g id="{p}-fr" opacity="0">' + reeds(41, 26, 700, 740, '#040a07', 140, 320, -60, 230) + reeds(42, 26, 700, 740, '#040a07', 140, 320, 1050, 1340) + '</g>', sway=1.6)
    sc.J(f"tl.fromTo('#{p}-fr',{{opacity:0,y:60}},{{opacity:1,y:0,duration:.9,ease:'power2.out',immediateRender:false}},{pt + .2:.3f});")
    sc.kicker(ctx.p('kicker', "WHO'S *already* HERE"), T['who'], y=618, size=28)
    # search brackets, then lock
    wt = T['who']; ht = T['here']
    cy = shy + CAM - .06 * shw; cx = shx + shw / 2 + 20
    hw, hh = shw * .58, 70
    sb = (f'<g id="{p}-sb" opacity="0" stroke="{GOLD}" stroke-width="4" fill="none" stroke-linecap="square">'
          f'<path d="M-90,-36 V-60 H-66 M90,-36 V-60 H66 M-90,36 V60 H-66 M90,36 V60 H66"/></g>')
    sc.fx.append(sb)
    hops = [(260, cy - 20), (980, cy + 30), (cx - 120, cy)]
    sc.J(f"tl.fromTo('#{p}-sb',{{opacity:0,x:{hops[0][0]},y:{hops[0][1]}}},{{opacity:1,duration:.15,immediateRender:false}},{wt - .1:.3f});")
    for k, (hx_, hy_) in enumerate(hops[1:]):
        t = wt + .1 + k * .3
        sc.J(f"tl.to('#{p}-sb',{{x:{hx_:.0f},y:{hy_:.0f},duration:.25,ease:'power2.inOut'}},{t:.3f});")
        sc.sfx('tick', t + .25, .4)
    sc.sfx('tick', wt, .4)
    sc.J(f"tl.to('#{p}-sb',{{opacity:0,duration:.1}},{ht - .05:.3f});")
    sc.J(f"tl.fromTo('#{p}-ey',{{opacity:0}},{{opacity:1,duration:.2,immediateRender:false}},{wt + .2:.3f});"
         f"tl.to('#{p}-ey',{{opacity:.4,duration:.12,yoyo:true,repeat:5}},{ht + .3:.3f});")
    sc.brackets(ht, cx, cy, hw, hh, beep=1.0, gain=.5)
    sc.heartbeat_rings([ht + .15, ht + .75], ex + 1, ey + CAM, 20, 90, sound=False)
    sc.sfx('heart', ht + .15, .5)
    sc.specks(24, 6, y0=80, y1=620)

# ================================================================== S10: the scientist's answer
def _tooth(x, y, k):
    return (f'<g transform="translate({x},{y}) scale({k})"><path d="M-40,60 C-44,10 -28,-60 0,-90 C28,-60 44,10 40,60 C20,70 -20,70 -40,60 Z" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M-30,30 C-20,-20 -10,-50 0,-70" fill="none" stroke="{GOLD}" stroke-width="2.5" stroke-opacity=".6"/>'
            + ''.join(f'<path d="M{-40 + i * 2},{50 - i * 22} l-8,-4 M{40 - i * 2},{50 - i * 22} l8,-4" stroke="{GOLD}" stroke-width="2.5"/>' for i in range(5)) + '</g>')

def build_scientist(ctx, sc, T):
    p = sc.p; a = sc.a; b = sc.b
    hx, hy, s = 330, 420, 1.55
    q = f'{p}s'
    svg, _, _, _ = person(q, 'scientist', hx, hy, s)
    disc = (f'<defs><radialGradient id="{p}-dg"><stop offset="0" stop-color="#f3dca0" stop-opacity=".42"/><stop offset=".55" stop-color="#e0a24a" stop-opacity=".14"/><stop offset="1" stop-color="#e0a24a" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse id="{p}-disc" cx="{hx}" cy="{hy - 10}" rx="300" ry="300" fill="url(#{p}-dg)"/>')
    floor = f'<path d="M-100,{hy + 132 * s / 1.55:.0f} C300,{hy + 126} 900,{hy + 136} 2400,{hy + 128}" fill="none" stroke="{SOFT}" stroke-opacity=".35" stroke-width="2"/>'
    # the ? card and the big clipboard (tooth sketch)
    qc = (f'<g id="{p}-qc" opacity="0"><rect x="640" y="140" width="170" height="200" rx="10" fill="#0a1611" fill-opacity=".7" stroke="{GOLD}" stroke-width="3"/>'
          f'<text x="725" y="290" text-anchor="middle" font-family="Cormorant Garamond,serif" font-weight="600" font-size="170" fill="{WARM}">?</text></g>')
    cb = (f'<g id="{p}-cb" opacity="0"><rect x="860" y="200" width="250" height="320" rx="10" fill="#8a6e45" stroke="#0d0b08" stroke-width="3"/>'
          f'<rect x="880" y="236" width="210" height="266" fill="#f6efe0" fill-opacity=".1" stroke="{SOFT}" stroke-opacity=".5"/><rect x="945" y="188" width="80" height="30" rx="6" fill="#3a2c18" stroke="{GOLD}" stroke-width="2"/>'
          f'{_tooth(985, 370, .95)}</g>')
    # shore with tiny early humans (revealed by the pan)
    SX = 1280 + 260
    shore = (f'<path d="M{SX - 300},{hy + 70} C{SX},{hy + 40} {SX + 400},{hy + 50} {SX + 900},{hy + 60} L{SX + 900},800 L{SX - 300},800 Z" fill="#0c1d16"/>'
             f'<path d="{waterline(hy + 80, SX - 300, SX + 900, 5, 120)}" fill="none" stroke="{SOFT}" stroke-opacity=".45" stroke-width="2.2"/>'
             f'<path d="M{SX - 300},{hy + 70} C{SX - 100},{hy + 30} {SX + 300},{hy + 26} {SX + 900},{hy + 40}" fill="none" stroke="#3b5534" stroke-width="22"/>'
             + far_line(12, hy + 30, '#1f3f2e', SX - 300, SX + 900, 30, 80))
    crowd_g = ''.join(f'<g id="{p}-cr{i}">{crowd(SX + 60 + i * 34, hy + 36, 1, 0, WARM)}</g>' for i in range(7))
    world = f'<g id="{p}-pan">{disc}{floor}<g id="{p}-sci">{svg}</g>{qc}{cb}{shore}{crowd_g}</g>'
    sc.svg(world, lid=f'{p}-PL')
    J = sc.J
    J(f"pose('{q}',{hx},{hy},{s},{{aL:18,aR:-24,lL:10,lR:-10}});")
    snap(sc, f'#{p}-sci', a + .02, dy=20, dur=.4); sc.sfx('swoosh', a + .02, .25)
    J(f"tl.fromTo('#{p}-disc',{{opacity:.75}},{{opacity:1,duration:1.4,yoyo:true,repeat:{int(sc.D / 1.4) + 1},ease:'sine.inOut'}},{a:.3f});")
    J(f"bob('#{p}-sci',{a + .4:.3f},{max(.5, T['them'] - a - .4):.3f},-3,.9);")
    sc.blink(q, [a + .8, T['giant'] + .9, T['quote'] + .2])
    # ? card floats in
    at = T['asked']
    J(f"tl.fromTo('#{p}-qc',{{opacity:0,x:-420,rotation:-12,transformOrigin:'50% 50%'}},{{opacity:1,x:0,rotation:-4,duration:.5,ease:'power3.out',immediateRender:false}},{at:.3f});"
      f"tl.to('#{p}-qc',{{y:-10,rotation:3,duration:1.2,yoyo:true,repeat:3,ease:'sine.inOut'}},{at + .5:.3f});")
    sc.sfx('click', at, .5); sc.sfx('swoosh', at, .3)
    label(sc, 0, 'WHAT DID IT *eat*?', 560, 360, at + .35, size=26)
    # looks at the clipboard: tooth sketch
    gt = T['giant']
    J(f"tl.to('#{q}-head',{{rotation:14,svgOrigin:'{hx} {hy - 112 * s + 20:.0f}',duration:.35,ease:'power3.out'}},{gt - .1:.3f});"
      f"tl.fromTo('#{p}-cb',{{opacity:0,scale:.3,transformOrigin:'0% 100%'}},{{opacity:1,scale:1,duration:.45,ease:'power3.out',immediateRender:false}},{gt:.3f});"
      f"tl.to('#{p}-qc',{{opacity:.35,duration:.4}},{gt:.3f});tl.to('#{p}-lb0',{{opacity:0,duration:.3}},{gt:.3f});")
    sc.sfx('click', gt, .45); sc.sfx('el:reeds_rustle', gt, .12)
    J(f"tl.fromTo('#{p}-cb',{{rotation:0}},{{rotation:2,transformOrigin:'50% 100%',duration:.8,yoyo:true,repeat:2,ease:'sine.inOut',immediateRender:false}},{gt + .5:.3f});")
    # shrug
    st = T['said']
    sy = hy - 78 * s
    J(f"tl.to('#{q}-head',{{rotation:-6,svgOrigin:'{hx} {hy - 112 * s + 20:.0f}',duration:.3}},{st:.3f});"
      f"tl.to('#{q}-armL',{{rotation:115,svgOrigin:'{hx} {sy:.0f}',duration:.3,ease:'power3.out'}},{st:.3f});"
      f"tl.to('#{q}-armR',{{rotation:-115,svgOrigin:'{hx} {sy:.0f}',duration:.3,ease:'power3.out'}},{st:.3f});"
      f"tl.to('#{p}-sci',{{y:-12,duration:.25,yoyo:true,repeat:1,ease:'power2.out'}},{st:.3f});"
      f"tl.to('#{p}-cb,#{p}-qc',{{opacity:0,duration:.35}},{st + .1:.3f});")
    sc.sfx('swoosh', st, .2); sc.sfx('el:reeds_rustle', st, .1)
    # quote marks + words type in
    qt = T['quote']; it = T['it']
    words = ['it', 'probably', 'ate', 'them.']
    wt = [it, ctx.t('w1209'), ctx.t('w1210'), T['them']]
    qhtml = (f'<div id="{p}-q" class="an-a" style="left:0;top:96px;width:1280px;text-align:center;font-family:Cormorant Garamond,serif;font-style:italic;font-weight:600;color:#d9bd7e;font-size:68px;line-height:1.1;text-shadow:0 2px 16px rgba(0,0,0,.85)">'
             f'<span id="{p}-qo" style="opacity:0;color:{GOLD};font-size:96px">“</span>'
             + ' '.join(f'<span id="{p}-w{i}" style="opacity:0;display:inline-block">{esc(w)}</span>' for i, w in enumerate(words))
             + f'<span id="{p}-qe" style="opacity:0;color:{GOLD};font-size:96px">”</span></div>')
    sc.top.append(qhtml)
    J(f"tl.fromTo('#{p}-qo',{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{qt:.3f});"
      f"tl.fromTo('#{p}-qe',{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{qt + .08:.3f});")
    sc.sfx('snap', qt, .4)
    for i, t in enumerate(wt):
        J(f"tl.fromTo('#{p}-w{i}',{{opacity:0,y:12}},{{opacity:1,y:0,duration:.25,ease:'power3.out',immediateRender:false}},{t:.3f});")
        sc.sfx('tick', t, .45)
    # pan right: the early humans on the shore freeze
    tt = T['them']
    J(f"tl.to('#{p}-PL',{{x:-1180,duration:.7,ease:'power3.inOut'}},{tt - .05:.3f});")
    for i in range(7):
        J(f"tl.fromTo('#{p}-cr{i}',{{y:0}},{{y:-3,duration:.3,yoyo:true,repeat:{int((tt + .4 - a) / .3)},ease:'sine.inOut'}},{a + i * .07:.3f});"
          f"tl.to('#{p}-cr{i}',{{y:-9,duration:.12,yoyo:true,repeat:1,ease:'power2.out'}},{tt + .65:.3f});")
    sc.sfx('swoosh', tt, .35); sc.sfx('boom', tt + .65, .45)
    sc.dust(30, 23)

# ================================================================== S11: cold Thames, hippo vs croc
HIPPO = ('M60,-260 C60,-420 250,-470 480,-460 C620,-455 700,-440 760,-420 C800,-470 880,-480 930,-440 C990,-400 1010,-320 990,-262 '
         'C975,-220 930,-206 880,-210 C840,-186 800,-176 770,-184 L752,-60 L766,0 L656,0 L644,-140 C520,-130 400,-130 300,-142 L290,0 L180,0 L172,-70 '
         'C120,-112 66,-180 60,-260 Z')

def build_xray_hippo(ctx, sc, T):
    p = sc.p; a = sc.a; b = sc.b
    GY = 560; WY = 470
    # cold sky haze, far frosty bank, snow
    sc.svg(soft(sc, 640, 180, 720, 240, '#c8d4c4', .12) + f'<path d="M-100,420 C200,400 500,412 800,404 C1000,398 1200,410 1400,404 L1400,{WY} L-100,{WY} Z" fill="#2b4136"/>'
           + far_line(15, 412, '#36493f', h0=22, h1=56), drift=-12)
    frostbank = f'<path d="M-100,{WY - 6} C300,{WY - 14} 900,{WY - 2} 1400,{WY - 10}" fill="none" stroke="#e8eee6" stroke-width="5" stroke-opacity=".55" stroke-dasharray="3 7"/>'
    sc.svg(frostbank + reeds(16, 30, WY - 4, WY + 4, '#4a5f53', 20, 60), sway=.8)
    wl = sc.svg(f'<path d="{waterline(WY, -200, 1500, 4, 150)} V760 H-200 Z" fill="#26372f"/>'
                f'<path d="{waterline(WY, -200, 1500, 4, 150)}" fill="none" stroke="#dfe6dd" stroke-opacity=".55" stroke-width="2.4"/>'
                + ''.join(f'<path class="gl" d="M{x},{y} h{w}" stroke="#dfe6dd" stroke-width="2" stroke-linecap="round" opacity=".22"/>' for x, y, w in
                          ((60, 520, 90), (330, 600, 70), (640, 540, 120), (900, 650, 80), (1150, 590, 70), (200, 690, 110), (760, 700, 60))))
    sc.glints(wl)
    # hippo (left) and croc (right), gold X-ray
    HX, HW = 70, 400; hk = HW / 1000
    hip = (f'<g id="{p}-hip"><g transform="translate({HX},{GY}) scale({hk:.3f})"><path d="{HIPPO}" fill="{GOLD}" fill-opacity=".06" stroke="{GOLD}" stroke-width="{3 / hk:.1f}" stroke-linejoin="round"/>'
           f'<path d="M870,-470 l10,-34 l26,22 M930,-430" fill="none" stroke="{GOLD}" stroke-width="{3 / hk:.1f}"/><circle cx="880" cy="-400" r="12" fill="none" stroke="{GOLD}" stroke-width="{2.5 / hk:.1f}"/>'
           + ''.join(f'<path d="M{x},-150 q20,-120 0,-260" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width="{2.2 / hk:.1f}"/>' for x in range(300, 700, 55)) + '</g></g>')
    hcx, hcy = HX + .48 * HW, GY - .3 * HW * .95
    hcore = (f'<circle id="{p}-hg" cx="{hcx:.0f}" cy="{hcy:.0f}" r="150" fill="url(#{p}-og)" opacity="0"/>'
             f'<g id="{p}-hh" opacity="0">{organ_svg("heart", hcx, hcy, 26)}</g>'
             + ''.join(f'<path id="{p}-rp{k}" d="M{hcx - 60},{hcy} a60,60 0 1,0 120,0 a60,60 0 1,0 -120,0" fill="none" stroke="#f0c070" stroke-width="2.5" opacity="0"/>' for k in range(3)))
    CX, CW = 520, 600
    cro = f'<g id="{p}-cro">{xray_shape(p + "c", "croc", CX, GY, CW)}</g>'
    ccx, ccy = CX + .52 * CW, GY - .32 * .15 * CW
    cgut = (f'<g id="{p}-cg" opacity="0"><g opacity=".35">{organ_svg("gut", ccx, ccy, 15, "#9aa79c")}</g></g>'
            f'<g id="{p}-fsh" opacity="0"><g transform="translate({ccx - 30:.0f},{ccy + 10:.0f}) scale(.07)">{shape_svg("fish", GOLD, 3 / .07, .95).replace("fill=\"#1a2429\"", "fill=\"none\"")}</g></g>'
            f'<circle id="{p}-cgl" cx="{ccx:.0f}" cy="{ccy:.0f}" r="44" fill="url(#{p}-og)" opacity="0"/>')
    # thermometer beside the croc
    TX, T0, T1 = 1190, 470, 300
    th = (f'<g id="{p}-th" opacity="0"><rect x="{TX - 11}" y="{T1 - 10}" width="22" height="{T0 - T1 + 10}" rx="11" fill="#0a1611" stroke="{WARM}" stroke-opacity=".7" stroke-width="2.5"/>'
          f'<circle cx="{TX}" cy="{T0 + 14}" r="20" fill="{GOLD}" stroke="{WARM}" stroke-opacity=".7" stroke-width="2.5"/>'
          f'<line id="{p}-thf" x1="{TX}" y1="{T0}" x2="{TX}" y2="{T0 - 40}" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/>'
          + ''.join(f'<line x1="{TX + 14}" y1="{y}" x2="{TX + 24}" y2="{y}" stroke="{WARM}" stroke-opacity=".5" stroke-width="2"/>' for y in range(T1 + 10, T0, 30)) + '</g>')
    fish = f'<g id="{p}-fs" opacity="0"><g transform="translate(1300,{GY - 30}) scale(-.09,.09)">{shape_svg("fish", WARM, 3 / .09, .95).replace("fill=\"#1a2429\"", f"fill=\"{INK}\"")}</g></g>'
    sc.svg(f'{hip}{hcore}{cro}{cgut}{th}{fish}', lid=f'{p}-AN')
    # water over the lower bodies
    sc.svg(f'<path d="{waterline(WY + 40, -200, 1500, 4, 150)} V760 H-200 Z" fill="#26372f" fill-opacity=".55"/>'
           f'<path id="{p}-wv2" d="{waterline(WY + 40, -200, 1500, 4, 150)}" fill="none" stroke="#dfe6dd" stroke-opacity=".35" stroke-width="2"/>')
    sc.J(f"tl.fromTo('#{p}-wv2',{{x:0}},{{x:-60,duration:1.7,yoyo:true,repeat:{int(sc.D / 1.7) + 1},ease:'sine.inOut'}},{a:.3f});")
    # frost creeping along the water line (on "cold")
    fr = ''
    r = random.Random(4)
    for k in range(40):
        x = -40 + k * 34; y = WY + r.uniform(-4, 6); L = r.uniform(10, 24)
        fr += f'<path class="{p}-fr" d="M{x},{y} l{L * .7:.0f},{-L:.0f} M{x},{y} l{-L * .5:.0f},{-L * .8:.0f} M{x},{y} l{L:.0f},{-L * .2:.0f}" stroke="#eef2ea" stroke-width="2" stroke-linecap="round" opacity="0"/>'
    sc.svg(fr)
    snow(sc, 70, 9, 70)
    # ---- in: both X-ray, scan line
    snap(sc, f'#{p}-AN', a + .02, dy=18, dur=.45); sc.flash(a + .05, .1); sc.sfx('shimmer', a + .05, .4); sc.sfx('swoosh', a + .02, .3)
    sc.fx.append(f'<g id="{p}-scan" opacity="0"><rect x="40" y="200" width="1220" height="60" fill="url(#{p}-scg)"/><line x1="40" y1="260" x2="1260" y2="260" stroke="{GOLD}" stroke-width="2.5"/></g>')
    sc.J(f"tl.fromTo('#{p}-scan',{{opacity:0}},{{opacity:.8,duration:.2,immediateRender:false}},{a + .1:.3f});tl.fromTo('#{p}-scan',{{y:0}},{{y:300,duration:1.9,yoyo:true,repeat:{int((sc.D - .2) / 1.9)},ease:'sine.inOut',immediateRender:false}},{a + .1:.3f});")
    sc.J(f"tl.fromTo('#{p}-hip',{{y:0}},{{y:-4,duration:1.4,yoyo:true,repeat:{int(sc.D / 1.4) + 1},ease:'sine.inOut',immediateRender:false}},{a + .4:.3f});"
         f"tl.fromTo('#{p}-cro',{{y:0}},{{y:-2,duration:1.8,yoyo:true,repeat:{int(sc.D / 1.8) + 1},ease:'sine.inOut',immediateRender:false}},{a + .4:.3f});")
    sc.sfx('el:hippo_grunt', a + .6, .5)
    label(sc, 0, 'HIPPO', HX + 40, 600, a + .5, size=26)
    label(sc, 1, 'CROC', CX + 220, 600, T['croc'] + .1, size=26)
    # ---- hippo makes its own heat
    ot = T['own']
    sc.J(f"tl.fromTo('#{p}-hg',{{opacity:0}},{{opacity:1,duration:.5,immediateRender:false}},{ot:.3f});"
         f"tl.fromTo('#{p}-hh',{{opacity:0,scale:.3,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.35,ease:'back.out(2)',immediateRender:false}},{ot:.3f});")
    for k in range(3):
        sc.J(f"tl.fromTo('#{p}-rp{k}',{{opacity:.8,scale:1,transformOrigin:'50% 50%'}},{{opacity:0,scale:2.6,duration:1.6,repeat:{int((b - ot) / 1.6)},ease:'power1.out',immediateRender:false}},{ot + .2 + k * .53:.3f});")
    hb = ot + .3; n = 0
    while hb < b - .3:
        sc.J(f"tl.fromTo('#{p}-hh',{{scale:1}},{{scale:1.25,transformOrigin:'50% 50%',duration:.1,yoyo:true,repeat:1,immediateRender:false}},{hb:.3f});")
        if n < 4: sc.sfx('heart', hb, .45 - n * .08)
        hb += .86; n += 1
    sc.sfx('shimmer', ot, .35)
    label(sc, 2, 'OWN *heat*', HX + 150, 600, ot + .3, size=26)
    sc.J(f"tl.to('#{p}-lb0',{{opacity:0,duration:.2}},{ot + .2:.3f});")
    # ---- crocodile: core stays dim, thermometer
    ct = T['croc']
    sc.J(f"tl.fromTo('#{p}-cg',{{opacity:0}},{{opacity:1,duration:.4,immediateRender:false}},{ct:.3f});"
         f"tl.fromTo('#{p}-th',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.4,ease:'power3.out',immediateRender:false}},{ct + .3:.3f});")
    sc.sfx('click', ct + .3, .4)
    # ---- cold: frost creeps along the water line (signature sound)
    cl = T['cold']
    sc.J(f"document.querySelectorAll('.{p}-fr').forEach((f,i)=>tl.fromTo(f,{{opacity:0,scale:.2,transformOrigin:'50% 100%'}},{{opacity:.85,scale:1,duration:.3,ease:'power2.out',immediateRender:false}},{cl:.3f}+i*.025));")
    sc.sfx('el:sig_frost', cl, .8)
    sc.J(f"tl.to('#{p}-thf',{{attr:{{y2:{T0 - 20}}},duration:.6,ease:'power2.inOut'}},{cl + .2:.3f});")
    # ---- checklist top right: warm up / digest / eat, each gets a gold X
    LX = 860
    rows = [('WARM UP', T['warm']), ('DIGEST', T['digest']), ('EAT', T['eating'])]
    xs = ''
    for k, (txt, t) in enumerate(rows):
        y = 96 + k * 58
        label(sc, 10 + k, txt, LX + 46, y, t - .15, size=28)
        xs += xmark_svg(f'{p}-x{k}', LX + 16, y + 20, 14, 5)
    sc.svg(xs)
    # warm: thermometer tries to rise, falls back
    wt = T['warm']
    sc.J(f"tl.to('#{p}-thf',{{attr:{{y2:{T1 + 40}}},duration:.45,ease:'power2.out'}},{wt:.3f});tl.to('#{p}-thf',{{attr:{{y2:{T0 - 18}}},duration:.5,ease:'power2.in'}},{wt + .5:.3f});")
    sc.sfx('ticks_up', wt, .3, .45); sc.sfx('slide_down', wt + .5, .25)
    xmark_in(sc, f'#{p}-x0', wt + .9)
    # digest: stomach with a fish, stays unchanged
    dt = T['digest']
    sc.J(f"tl.fromTo('#{p}-fsh',{{opacity:0}},{{opacity:1,duration:.3,immediateRender:false}},{dt - .2:.3f});"
         f"tl.fromTo('#{p}-cgl',{{opacity:0}},{{opacity:.6,duration:.3,yoyo:true,repeat:1,immediateRender:false}},{dt - .2:.3f});")
    xmark_in(sc, f'#{p}-x1', dt + .4)
    # eating: a fish swims past its mouth, no reaction
    et = T['eating']
    sc.J(f"tl.fromTo('#{p}-fs',{{opacity:0,x:0}},{{opacity:1,x:-60,duration:.3,immediateRender:false}},{et - .5:.3f});tl.to('#{p}-fs',{{x:-330,duration:{max(.6, b - et + .2):.2f},ease:'none'}},{et - .2:.3f});")
    sc.sfx('el:fish_splash', et - .4, .25)
    xmark_in(sc, f'#{p}-x2', et + .35)
    sc.kicker(ctx.p('kicker', 'Thames *winter*'), a + .2, y=56, x=60, w=700, align='left', size=26)

# ================================================================== S12: the way out (list) + North Sea in winter
def build_sea_options(ctx, sc, T):
    p = sc.p; a = sc.a; b = sc.b
    sc.dust(30, 13)
    items = ['1. Warm up', '2. Keep eating', '3. Escape by sea']
    size = 48; gap = 84; top0 = 230
    tw = [len(t) * size * .43 + 10 for t in items]; bw = max(tw) + 50; L = int(640 - bw / 2 + 24)
    rows = ''; svg = ''
    for i, t in enumerate(items):
        y = top0 + i * gap
        rows += f'<div id="{p}-o{i}" class="an-a an-big" style="left:{L}px;top:{y}px;font-size:{size}px;opacity:{.45 if i < 2 else 0}">{rich(t)}</div>'
        svg += (f'<rect id="{p}-bx{i}" x="{L - 24}" y="{y - 12}" width="{bw:.0f}" height="{size + 26}" rx="6" fill="none" stroke="{GOLD}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
                f'<line id="{p}-st{i}" x1="{L - 10}" y1="{y + size * .58:.0f}" x2="{L + tw[i] + 6:.0f}" y2="{y + size * .54:.0f}" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="{0 if i < 2 else 1}"/>')
    gx, gy = L + tw[2] + 70, top0 + 2 * gap + 26
    svg += f'<g id="{p}-gl" opacity="0">{organ_svg("gland", gx, gy, 20)}</g>' + check_svg(f'{p}-ck', gx + 52, gy, 1.1)
    head = (f'<div id="{p}-q" class="an-a an-k" style="left:0;width:1280px;top:132px;text-align:center;font-size:28px">{kick_html(ctx.p("kicker", "Its way *out*?"))}</div>'
            f'<div class="an-hair" style="left:560px;width:160px;top:178px"></div>')
    sc.add_html(f'<div id="{p}-lst" class="an-a" style="left:0;top:0;width:1280px;height:720px">{head}{rows}<svg class="an-ly" width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg></div>')
    # list is already there (carried over); row 3 clicks in and gets the box
    sc.J(f"tl.fromTo('#{p}-lst',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.35,ease:'power3.out',immediateRender:false}},{a + .02:.3f});")
    sc.sfx('swoosh', a + .02, .25)
    bt = T['box']
    sc.J(f"tl.fromTo('#{p}-o2',{{opacity:0,x:-24}},{{opacity:1,x:0,duration:.3,ease:'power3.out',immediateRender:false}},{bt - .2:.3f});")
    sc.sfx('click', bt - .2, .5)
    sc.J(f"tl.fromTo('#{p}-bx2',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.45,ease:'power2.out',immediateRender:false}},{bt + .15:.3f});"
         f"tl.fromTo('#{p}-o2',{{scale:1.06,transformOrigin:'0 50%'}},{{scale:1,duration:.35,ease:'power3.out',immediateRender:false}},{bt + .15:.3f});")
    sc.sfx('marker', bt + .15, .35)
    sc.J(f"tl.fromTo('#{p}-bx2',{{opacity:1}},{{opacity:.55,duration:.6,yoyo:true,repeat:3,ease:'sine.inOut',immediateRender:false}},{bt + .7:.3f});")
    # salt gland icon ticks
    st = T['salt']
    sc.J(f"tl.fromTo('#{p}-gl',{{opacity:0,scale:.3,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.35,ease:'back.out(2)',immediateRender:false}},{st:.3f});"
         f"tl.fromTo('#{p}-ck',{{opacity:0,scale:.2,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.3,ease:'back.out(2.5)',immediateRender:false}},{st + .3:.3f});")
    sc.sfx('tick', st + .3, .6)
    label(sc, 5, 'SALT GLANDS', gx + 84, gy - 15, st + .35, size=22)
    # mini scene: out of the river mouth into the North Sea, winter
    mt = T['swim']; nt = T['north']; wt = T['winter']
    back_t = min(b - .55, wt + .45)
    q = f'{p}-m'
    land = (f'<path d="M-100,330 C150,320 300,340 420,360 C380,420 330,470 300,760 L-100,760 Z" fill="#203b2c"/>'
            f'<path d="M-100,560 C100,520 200,500 300,520 L300,760 L-100,760 Z" fill="#17301f"/>'
            + reeds(21, 22, 330, 370, '#2b4a37', 30, 80, -80, 380) + f'<path d="M-100,326 C150,316 300,336 420,356" fill="none" stroke="#eef2ea" stroke-width="4" stroke-opacity=".5" stroke-dasharray="3 7"/>')
    sea = f'<path d="M-100,380 L1400,380 L1400,760 L-100,760 Z" fill="#46524c"/><path d="M420,380 L1400,380" stroke="#cfd6cf" stroke-width="2" opacity=".5"/>'
    waves = ''.join(f'<path id="{q}w{k}" d="{waterline(420 + k * 58, 280, 1500, 9, 90)}" fill="none" stroke="#dfe4dc" stroke-width="2.5" stroke-opacity="{.55 - k * .06:.2f}"/>' for k in range(6))
    img, ch = croc_img(ctx, f'{q}c', 'swim', 120, 520, 330)
    shiver = ''.join(f'<path id="{q}sv{k}" d="M{760 + k * 16},{420 + (k % 2) * 30} q-8,10 0,20 q8,10 0,20" fill="none" stroke="{WARM}" stroke-width="3" stroke-linecap="round" opacity="0"/>' for k in range(3))
    sc.svg(f'<g id="{q}" opacity="0">{sea}{waves}{land}<g id="{q}cg">{img}</g>{shiver}</g>', lid=f'{q}L')
    for k in range(6):
        sc.J(f"tl.fromTo('#{q}w{k}',{{x:0}},{{x:{-60 if k % 2 else 50},duration:{.7 + k * .1:.2f},yoyo:true,repeat:{int(sc.D) + 2},ease:'sine.inOut'}},{a:.3f});")
    sc.J(f"tl.to('#{p}-lst',{{opacity:0,x:-60,duration:.3,ease:'power2.in'}},{mt - .25:.3f});tl.to('#{p}-lb5',{{opacity:0,duration:.25}},{mt - .25:.3f});"
         f"tl.fromTo('#{q}',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35,ease:'power3.out',immediateRender:false}},{mt:.3f});"
         f"tl.fromTo('#{q}cg',{{x:0}},{{x:470,duration:{wt - mt:.2f},ease:'power1.out',immediateRender:false}},{mt:.3f});"
         f"tl.fromTo('#{q}cg',{{y:0}},{{y:8,duration:.3,yoyo:true,repeat:{int((wt - mt) / .3) + 1},ease:'sine.inOut',immediateRender:false}},{mt:.3f});")
    sc.sfx('swoosh', mt, .35); sc.sfx('el:splash_small', mt + .2, .4)
    sc.add_html(f'<div id="{q}n" class="an-a an-big" style="left:700px;top:180px;width:520px;text-align:center;font-size:66px;letter-spacing:.06em;opacity:0">NORTH SEA</div>'
                f'<div id="{q}i" class="an-a an-it" style="left:700px;top:262px;width:520px;text-align:center;font-size:46px;opacity:0">in winter</div>')
    sc.J(f"tl.fromTo('#{q}n',{{opacity:0,scale:1.25,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.35,ease:'power3.out',immediateRender:false}},{nt:.3f});"
         f"tl.fromTo('#{q}i',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.35,ease:'power3.out',immediateRender:false}},{wt:.3f});")
    sc.sfx('thud', nt, .45)
    # winter: snow whips across, croc stops and shivers
    snow(sc, 70, 31, fast=True, lid=f'{q}sn', t0=mt)
    sc.J(f"tl.fromTo('#{q}sn',{{opacity:0}},{{opacity:.9,duration:.3,immediateRender:false}},{wt - .15:.3f});")
    sc.J(f"tl.fromTo('#{q}cg',{{x:470}},{{x:478,duration:.05,yoyo:true,repeat:7,immediateRender:false}},{wt + .05:.3f});")
    for k in range(3): sc.J(f"tl.fromTo('#{q}sv{k}',{{opacity:0}},{{opacity:.9,duration:.08,yoyo:true,repeat:3,immediateRender:false}},{wt + .05 + k * .06:.3f});")
    sc.sfx('el:sig_frost', wt, .8); sc.sfx('wind', wt - .2, .35)
    # back to the list: strike row 3
    sc.J(f"tl.to('#{q},#{q}n,#{q}i,#{q}sn',{{opacity:0,duration:.25}},{back_t - .2:.3f});"
         f"tl.to('#{p}-lst,#{p}-lb5',{{opacity:1,x:0,duration:.3,ease:'power2.out'}},{back_t - .1:.3f});"
         f"tl.fromTo('#{p}-st2',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.3,ease:'power1.inOut',immediateRender:false}},{back_t + .1:.3f});"
         f"tl.to('#{p}-o2,#{p}-gl,#{p}-ck,#{p}-lb5',{{opacity:.45,duration:.25}},{back_t + .3:.3f});tl.to('#{p}-bx2',{{opacity:0,duration:.2}},{back_t + .1:.3f});")
    sc.sfx('scratch', back_t + .1, .8)

# ================================================================== S13: body-temperature gauge
def build_body_temp(ctx, sc, T):
    p = sc.p; a = sc.a; b = sc.b
    GY = 560
    # hot sky + sun disc that arcs to noon
    sc.svg(soft(sc, 500, 180, 680, 260, '#e0a24a', .2))
    sun = (f'<g id="{p}-sun">' + soft(sc, 560, 200, 170, 170, '#f3dca0', .4, gid=f'{p}-sh') +
           f'<circle cx="560" cy="200" r="46" fill="#f6e2a8" opacity=".85"/></g>')
    sc.svg(sun)
    sc.svg(far_line(17, GY - 40, '#2a4a36', h0=26, h1=70), drift=-10)
    # palm with its shadow patch (left)
    palm = (f'<path d="M150,{GY} C160,460 170,380 190,300" fill="none" stroke="#2f2a1a" stroke-width="16" stroke-linecap="round"/>'
            + ''.join(frond(190, 300, L, ang, '#1d3c2a') for L, ang in ((150, -70), (170, -35), (160, 0), (170, 35), (150, 70), (120, -110), (120, 110))))
    shade = f'<ellipse id="{p}-shd" cx="190" cy="{GY + 40}" rx="220" ry="46" fill="#0e2a1f" opacity=".85"/>'
    ground = (f'<path d="M-100,{GY - 10} C200,{GY - 20} 500,{GY - 4} 1400,{GY - 12} L1400,760 L-100,760 Z" fill="#4c4026" opacity=".6"/>'
              f'<path d="M-100,{GY - 10} C200,{GY - 20} 500,{GY - 4} 1400,{GY - 12}" fill="none" stroke="{SOFT}" stroke-opacity=".3" stroke-width="2"/>{shade}')
    sc.svg(ground + palm, sway=1.0)
    # heat shimmer lines
    shim = ''.join(f'<path id="{p}-hs{k}" d="M{300 + k * 70},{GY - 30} q10,-20 0,-40 q-10,-20 0,-40" fill="none" stroke="#f3dca0" stroke-width="2" opacity=".0"/>' for k in range(6))
    sc.svg(shim)
    for k in range(6):
        sc.J(f"tl.fromTo('#{p}-hs{k}',{{y:0,opacity:.0}},{{y:-30,opacity:.35,duration:.9,repeat:{int(sc.D / .9) + 1},yoyo:true,ease:'sine.inOut',immediateRender:false}},{a + k * .15:.3f});")
    # our croc basking (true colours)
    CX, CW = 290, 400
    img, ch = croc_img(ctx, f'{p}-cc', 'gape', CX, GY + 30, CW, flip=True)
    sc.svg(f'<g id="{p}-cr">{img}</g>', lid=f'{p}-CL')
    snap(sc, f'#{p}-CL', a + .05, dy=16, dur=.4); sc.sfx('swoosh', a + .05, .25)
    sc.J(f"tl.fromTo('#{p}-cr',{{scaleY:1}},{{scaleY:1.025,transformOrigin:'50% 100%',duration:1.6,yoyo:true,repeat:{int(sc.D / 1.6) + 1},ease:'sine.inOut',immediateRender:false}},{a + .4:.3f});")
    # thermometer gauge (right)
    TX, Y0, Y1 = 900, 560, 170
    lo, hi = 20.0, 40.0
    Y = lambda v: Y0 - (Y0 - Y1) * (v - lo) / (hi - lo)
    g = (f'<g id="{p}-g" opacity="0"><rect x="{TX - 24}" y="{Y1 - 14}" width="48" height="{Y0 - Y1 + 30}" rx="24" fill="{WARM}" fill-opacity=".06" stroke="{WARM}" stroke-opacity=".35" stroke-width="2"/>'
         f'<circle cx="{TX}" cy="{Y0 + 30}" r="34" fill="{GOLD}" fill-opacity=".85" stroke="{WARM}" stroke-opacity=".35" stroke-width="2"/>'
         f'<rect id="{p}-band" x="{TX - 24}" y="{Y(40):.0f}" width="48" height="{Y(32.5) - Y(40):.0f}" fill="url(#{p}-hatch)" opacity="0"/>')
    sc.defs.append(f'<pattern id="{p}-hatch" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="12" height="12" fill="{GOLD}" fill-opacity=".12"/><line x1="0" y1="0" x2="0" y2="12" stroke="{GOLD}" stroke-width="5" stroke-opacity=".75"/></pattern>')
    for v in (20, 25, 30, 35, 40):
        g += f'<line x1="{TX - 44}" y1="{Y(v):.0f}" x2="{TX - 30}" y2="{Y(v):.0f}" stroke="{WARM}" stroke-opacity=".5" stroke-width="2"/>'
        sc.add_html(f'<div class="an-a an-k" style="left:{TX - 150}px;width:100px;text-align:right;top:{Y(v) - 15:.0f}px;font-size:22px;letter-spacing:.06em;opacity:.7">{v}°</div>')
    g += f'<line id="{p}-fill" x1="{TX}" y1="{Y0 + 10}" x2="{TX}" y2="{Y(lo) - 2:.0f}" stroke="{GOLD}" stroke-width="26" stroke-linecap="round"/></g>'
    sc.svg(g)
    sc.J(f"tl.fromTo('#{p}-g',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:'power3.out',immediateRender:false}},{a + .3:.3f});")
    sc.sfx('click', a + .3, .35)
    sc.kicker(ctx.p('kicker', 'Body *temperature*'), a + .3, y=76, x=780, w=480, align='left', size=26)
    # count-up and land
    ab = T['above']; lt = T['land']; dur = max(.9, lt - ab)
    sc.J(f"tl.fromTo('#{p}-fill',{{attr:{{y2:{Y(lo):.0f}}}}},{{attr:{{y2:{Y(32.5):.0f}}},duration:{dur:.2f},ease:'power2.in',immediateRender:false}},{ab:.3f});")
    sc.add_html(f'<div id="{p}-n" class="an-a an-big" style="left:{TX + 70}px;top:{Y(32.5) - 52:.0f}px;width:360px;font-size:84px;opacity:0"></div>')
    sc.J(f"tl.set('#{p}-n',{{opacity:1}},{ab:.3f});counter('#{p}-n',{ab:.3f},{dur:.2f},20,33,v=>Math.round(v)+'<span style=\"font-size:46px\">°C</span>','power2.in');"
         f"tl.call(()=>{{const e=document.querySelector('#{p}-n');if(e)e.innerHTML='32–33<span style=\"font-size:46px\">°C</span>';}},null,{lt:.3f});"
         f"tl.call(()=>{{const e=document.querySelector('#{p}-n');if(e)e.innerHTML='20<span style=\"font-size:46px\">°C</span>';}},null,{ab - .01:.3f});"
         f"tl.fromTo('#{p}-n',{{scale:1.2,transformOrigin:'0% 50%'}},{{scale:1,duration:.4,ease:'power3.out',immediateRender:false}},{lt:.3f});")
    sc.sfx('ticks_up', ab, .45, dur)
    sc.land(lt, TX, Y(32.5), r1=150, r2=230)
    sc.J(f"tl.fromTo('#{p}-band',{{opacity:0}},{{opacity:1,duration:.4,immediateRender:false}},{lt + .2:.3f});")
    sc.add_html(f'<div id="{p}-bl" class="an-a an-k" style="left:{TX + 74}px;top:{Y(37) - 16:.0f}px;font-size:24px;opacity:0">*struggle* ZONE</div>'.replace('*struggle*', '<span class="an-ki">struggle</span>'))
    sc.J(f"tl.fromTo('#{p}-bl',{{opacity:0,x:-14}},{{opacity:1,x:0,duration:.35,ease:'power3.out',immediateRender:false}},{lt + .45:.3f});")
    sc.sfx('tick', lt + .45, .35)
    # dive + energy bars drain
    BX, BW = 980, 230
    bars = ''
    for k, (lab_, yy) in enumerate((('DIVES', 420), ('ENERGY', 500))):
        bars += (f'<g id="{p}-bg{k}" opacity="0"><line x1="{BX}" y1="{yy}" x2="{BX + BW}" y2="{yy}" stroke="{WARM}" stroke-opacity=".18" stroke-width="12" stroke-linecap="round"/>'
                 f'<line id="{p}-b{k}" x1="{BX}" y1="{yy}" x2="{BX + BW}" y2="{yy}" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/></g>')
        sc.add_html(f'<div id="{p}-bt{k}" class="an-a an-k" style="left:{BX}px;top:{yy - 46}px;font-size:22px;opacity:0">{lab_}</div>')
    sc.svg(bars)
    for k, (key, to) in enumerate((('shorter', .38), ('less', .22))):
        t = T[key]
        sc.J(f"tl.fromTo('#{p}-bg{k},#{p}-bt{k}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.3,ease:'power3.out',immediateRender:false}},{t - .25:.3f});"
             f"tl.fromTo('#{p}-b{k}',{{attr:{{x2:{BX + BW}}}}},{{attr:{{x2:{BX + BW * to:.0f}}},duration:.9,ease:'power2.inOut',immediateRender:false}},{t + .1:.3f});")
        sc.sfx('click', t - .25, .35); sc.sfx('downsweep' if k else 'ticks', t + .1, .3 if k else .35)
    # hottest hours: sun arcs to noon, shimmer grows
    ht = T['hottest']
    sc.J(f"tl.to('#{p}-sun',{{x:-160,y:-110,duration:1.0,ease:'power2.inOut'}},{ht:.3f});tl.to('#{p}-sh',{{attr:{{rx:240,ry:240}},duration:1.0}},{ht:.3f});")
    for k in range(6): sc.J(f"tl.to('#{p}-hs{k}',{{scaleY:1.6,transformOrigin:'50% 100%',duration:.8}},{ht:.3f});")
    sc.sfx('swoosh', ht, .3); sc.sfx('shimmer', ht + .2, .3)
    # shade: croc drags itself under the palm shadow, dims
    sd = T['shade']
    sc.J(f"tl.to('#{p}-CL',{{x:-170,duration:{max(.8, b - sd + .5):.2f},ease:'power1.inOut'}},{sd - .5:.3f});tl.to('#{p}-cc',{{opacity:.7,duration:.6}},{sd:.3f});"
         f"tl.fromTo('#{p}-shd',{{opacity:.85}},{{opacity:1,duration:.5,immediateRender:false}},{sd - .3:.3f});")
    sc.sfx('el:reeds_rustle', sd - .5, .4)
    sc.specks(20, 8, col='#f3dca0', y0=100, y1=520)

BUILD = {'xray_palate': (build_xray_palate, (1.0, 1.05, '55% 55%')), 'xray_salt': (build_xray_salt, (1.0, 1.05, '60% 70%')),
         'lake_lock': (build_lake_lock, (1.0, 1.06, '55% 60%')), 'scientist': (build_scientist, (1.0, 1.04, '40% 50%')),
         'xray_hippo': (build_xray_hippo, (1.0, 1.04, '50% 60%')), 'sea_options': (build_sea_options, (1.0, 1.04, '50% 50%')),
         'body_temp': (build_body_temp, (1.0, 1.04, '45% 55%'))}

SYNTH = {'tick', 'ticks', 'ticks_up', 'beep', 'thud', 'click', 'scratch', 'marker', 'swoosh', 'shimmer', 'hit', 'heart'}
ALIAS = {'snap': 'click', 'boom': 'hit', 'slide_down': 'ticks', 'downsweep': 'ticks'}
PRIO = ['hit', 'beep', 'heart', 'scratch', 'marker', 'click', 'ticks_up', 'ticks', 'thud', 'tick', 'shimmer', 'swoosh']

def _lean(events, gap=.18):
    """Only synth graphic cues (real recordings + the frost signature live in fixpass/sound_<chapter>.json), and one sound per moment:
    events closer than `gap` s are merged (the most meaningful cue wins)."""
    ev = []
    for e in events:
        c = ALIAS.get(e['cue'], e['cue'])
        if c in SYNTH: ev.append(dict(e, cue=c))
    ev.sort(key=lambda e: e['t']); out = []
    for e in ev:
        if out and e['t'] - out[-1]['t'] < gap:
            if PRIO.index(e['cue']) < PRIO.index(out[-1]['cue']): out[-1] = e
            continue
        out.append(e)
    return out

def build(ctx):
    fn, push = BUILD[ctx.variant]
    sc = Scene(ctx, bg=BG, push=push)
    fn(ctx, sc, _T(ctx))
    ctx.events[:] = _lean(ctx.events)
    return sc.done()
