"""Video 02 fix pass, batch A (ch00-ch03): custom animated scenes S01-S06 (videos/video02/plan/fixpass/PLAN.md).
Locked look (GOLD 95-100): green-ink + vignette, gold line art, warm-white Cormorant/Jost, our croc in true colours
(templates/lib/anim_assets/croc_porosus_*.png, CC0), gold the only pointing colour, red only for "Wiped out".
Built on anim_common.Scene (same rings / flash / kicker / dust as the generic anim_* blocks).
Every time param is a time spec (seconds after the shot start, "w123", "@word"); defaults follow the V02 voice."""
import os, random
from .common import fig, esc, rich, GOLD, WARM, SOFT, ITAL, ICONS
from .anim_common import (Scene, glyph, kick_html, waterline, water_band, reeds, fronds, frond, broads, leaves, INK, BG)
from .croc_gfx import SHAPES, shape_svg

LONG_OK = ('s01_checks', 's02_ladder', 's03_bite', 's04_fire', 's05_mud', 's06_temp')
META = dict(name='v02_anim_a', about='V02 fix-pass scenes, batch A: "s01_checks" = the four checks as a list spine with icons + gold box (R05); '
            '"s02_ladder" = the tier ladder: our croc steps down Dominate > Establish > Survive (R09); "s03_bite" = bite-force bars, '
            'amphibians stop short, our croc counts to 16,414 N (C01-17); "s04_fire" = coal-swamp fires, the croc slides into the water (C01-21); '
            '"s05_mud" = croc waits in the mud, HOBBIES card, then WATER | BANK split (C02-21); "s06_temp" = thermometer counts to 14 C, '
            'frost below the line, empty riverbank (C03-14).',
  variants=list(LONG_OK),
  params={'at': 'dict of beat name -> time spec (override the default beats of the variant; see BEATS in the module)',
          'value': 's03_bite: our bite value (default 16414)', 'unit': 's03_bite: unit (default N)'})

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, '..', 'lib', 'anim_assets'))
TIER = {'DOMINATE': '#5f7f6a', 'ESTABLISH': '#8a9a62', 'SURVIVE': '#b8794d', 'WIPED OUT': '#9a4f4a'}
ROW_TXT = '#f6efe0'

# default beats (time specs relative to the shot); a shot may override any of them with params.at
BEATS = {
 's01_checks': dict(kick='w116', slots='w120', same='w122', r1='w125', r2='w127', r3='w128', r4='w136', glow='w145', blink1='w131', blink2='w141'),
 's02_ladder': dict(steps=0.0, croc='0.15', ring='w161', est='w162', shadow='w168', boss='w173', surv='w174', hang='w177'),
 's03_bite': dict(kick=0.1, amph='w321', close='w323', our='w324', count='w328', land='w331'),
 's04_fire': dict(f1='w348', f2='w349', f3='w350', look='w354', slide='w356', eyes='w359'),
 's05_mud': dict(waits='w509', card='w511', blink='w515', split='w516', rule='w517', steps='w520', walk='w524'),
 's06_temp': dict(kick=0.1, sub='w625', count='w629', land='w631', below='w632', bank='w634', find='w636'),
}

# ---------------------------------------------------------------- our croc in true colours (CC0 PNGs)
CROC = {'swim': ('croc_porosus_swim.png', 1600, 675, (1508, 26)), 'gape': ('croc_porosus_gape.png', 1600, 758, (66, 268))}

def croc(ctx, gid, kind, cx, cy, w, rot=0.0, flip=False, eye=True):
    """Our croc image centred at (cx, cy), w px wide. Returns (svg, h). Eye group id gid-eye (for blinks)."""
    f, W, H, (ex, ey) = CROC[kind]
    src = ctx.asset(os.path.join(ASSETS, f)); k = w / W; h = H * k
    fl = ' scale(-1,1)' if flip else ''
    e = ''
    if eye:
        er = max(2.6, 9 * k * 1.6)
        e = (f'<g id="{gid}-eye"><ellipse cx="{(ex - W / 2) * k:.1f}" cy="{(ey - H / 2) * k:.1f}" rx="{er:.1f}" ry="{er * .8:.1f}" fill="#e2b453" stroke="#2a2410" stroke-width="{max(1, er * .25):.1f}"/>'
             f'<ellipse cx="{(ex - W / 2) * k:.1f}" cy="{(ey - H / 2) * k:.1f}" rx="{er * .22:.1f}" ry="{er * .7:.1f}" fill="#120e06"/></g>')
    return (f'<g id="{gid}"><g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.1f}){fl}">'
            f'<image href="{src}" x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h:.1f}"/>{e}</g></g>'), h

def blink(sc, sel, t, hold=.07):
    sc.J(f"tl.to('{sel}',{{scaleY:.1,transformOrigin:'50% 50%',duration:{hold},yoyo:true,repeat:1}},{t:.3f});")

def snap(sc, sel, t, frm='opacity:0,y:20', dur=.4, ease='power3.out'):
    sc.J(f"tl.fromTo('{sel}',{{{frm}}},{{opacity:1,x:0,y:0,scale:1,duration:{dur},ease:'{ease}',immediateRender:false}},{t:.3f});")

def T(ctx, v, name):
    at = ctx.p('at') or {}
    return ctx.t(at.get(name, BEATS[v][name]))

# ---------------------------------------------------------------- small icons (drawn around 0,0, ~100 px)
def eyes_icon(p):
    return (f'<g><path d="{waterline(18, -60, 60, 5, 40)}" fill="none" stroke="{SOFT}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M-44,16 q14,-30 30,0 M14,16 q14,-30 30,0" fill="{INK}" stroke="{WARM}" stroke-width="5"/>'
            f'<g id="{p}"><ellipse cx="-29" cy="4" rx="7" ry="6" fill="#e2b453"/><ellipse cx="29" cy="4" rx="7" ry="6" fill="#e2b453"/>'
            f'<ellipse cx="-29" cy="4" rx="1.6" ry="5" fill="#120e06"/><ellipse cx="29" cy="4" rx="1.6" ry="5" fill="#120e06"/></g></g>')

def star_icon():
    import math
    pts = []
    for i in range(10):
        r = 46 if i % 2 == 0 else 20; a = -math.pi / 2 + i * math.pi / 5
        pts.append(f'{r * math.cos(a):.1f},{r * math.sin(a):.1f}')
    return (f'<path d="M{" L".join(pts)} Z" fill="{GOLD}" fill-opacity=".14" stroke="{GOLD}" stroke-width="4" stroke-linejoin="round"/>'
            f'<text x="0" y="13" text-anchor="middle" style="font-family:\'Cormorant Garamond\',serif;font-weight:700;font-size:38px" fill="{WARM}">?</text>')

def three_toe(x, y, s, rot=0, col=WARM, fill='#0c1510'):
    """Three-toed theropod print (same drawing as croc_gfx footprints)."""
    return (f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot}) scale({s:.2f})"><path d="M0,40 C-14,36 -18,20 -10,4 L-34,-40 C-38,-50 -26,-54 -20,-46 L-2,-14 L0,-62 C0,-72 14,-72 14,-62 L12,-14 L30,-46 C36,-54 48,-50 44,-40 L20,4 C28,20 22,36 10,40 Z" '
            f'fill="{fill}" stroke="{col}" stroke-width="3.5" stroke-linejoin="round"/></g>')

def croc_print(x, y, s, col=WARM):
    toes = ''.join(f'<path d="M{dx},{-8} l{tx},{-26}" stroke="{col}" stroke-width="4" stroke-linecap="round"/>' for dx, tx in ((-14, -10), (-5, -4), (5, 3), (14, 10)))
    return (f'<g transform="translate({x:.0f},{y:.0f}) scale({s:.2f})"><ellipse cx="0" cy="6" rx="22" ry="16" fill="#0c1510" stroke="{col}" stroke-width="4"/>{toes}'
            f'<path d="M-20,2 l-16,-14" stroke="{col}" stroke-width="4" stroke-linecap="round"/></g>')

def flame(i, x, y, s):
    return (f'<g id="{i}" opacity="0"><g transform="translate({x:.0f},{y:.0f}) scale({s:.2f})">'
            f'<path id="{i}f" d="M0,0 C-30,-6 -34,-40 -18,-66 C-14,-46 -4,-44 -2,-56 C2,-80 14,-96 10,-120 C34,-96 44,-60 30,-30 C38,-36 40,-46 40,-50 C52,-28 40,-4 0,0 Z" '
            f'fill="#d98a2b" fill-opacity=".55" stroke="#f0b54a" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M0,-6 C-12,-12 -12,-30 -2,-44 C4,-30 18,-28 12,-10 C10,-6 6,-4 0,-6 Z" fill="#f6d27a" fill-opacity=".8"/></g></g>')

# ================================================================ S01 the four checks (R05)
def s01_checks(ctx, sc):
    p = sc.p; v = 's01_checks'; a, b = sc.a, sc.b
    tk = T(ctx, v, 'kick'); tsl = T(ctx, v, 'slots'); tsm = T(ctx, v, 'same'); tg = T(ctx, v, 'glow')
    rows = [('Temperature', 'thermo', T(ctx, v, 'r1')), ('Food', 'fish', T(ctx, v, 'r2')), ('Who else is in the water', 'eyes', T(ctx, v, 'r3')), ('Its one special move', 'star', T(ctx, v, 'r4'))]
    # river at the bottom, far bank reeds (the "every river" world)
    sc.svg(reeds(21, 34, 640, 660, '#1d3a2b', 40, 110), sway=2)
    sc.svg(water_band(p + 'w', 655, '#0a1712'), lid=f'{p}-wat'); sc.glints(f'{p}-wat')
    sc.kicker('Every river, *same* checks', tk, y=70, size=30, sound=None); sc.sfx('swoosh', tk, .3)
    X0, Y0, GAP = 250, 172, 118
    spine = f'<line id="{p}-sp" x1="{X0}" y1="{Y0 - 30}" x2="{X0}" y2="{Y0 + 3 * GAP + 40}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    slots = ''; content = ''
    for i, (txt, ic, at) in enumerate(rows):
        y = Y0 + i * GAP
        slots += (f'<g id="{p}-sl{i}" opacity="0"><circle cx="{X0}" cy="{y + 30}" r="20" fill="#0c1712" stroke="{GOLD}" stroke-width="2.5"/>'
                  f'<text x="{X0}" y="{y + 39}" text-anchor="middle" class="an-svgk" style="font-size:22px;letter-spacing:0">{i + 1}</text></g>')
        if ic == 'thermo': g = f'<g transform="translate(360,{y + 32}) scale(.5)">{ICONS["thermometer"]}</g>'
        elif ic == 'fish': g = f'<g transform="translate(360,{y + 32}) scale(.46)">{ICONS["fish"]}</g>'
        elif ic == 'eyes': g = f'<g transform="translate(360,{y + 30}) scale(1.0)">{eyes_icon(p + "-ey")}</g>'
        else: g = f'<g id="{p}-star" transform="translate(360,{y + 32})"><g id="{p}-stari">{star_icon()}</g></g>'
        content += f'<g id="{p}-ic{i}" opacity="0">{g}</g>'
        sc.add_html(f'<div id="{p}-o{i}" class="an-a an-big" style="left:440px;top:{y - 2}px;font-size:60px;opacity:0">{rich(txt)}</div>')
    W = 870; box = f'<rect id="{p}-bx" x="300" y="{Y0 - 14}" width="{W}" height="94" rx="8" opacity="0" fill="{GOLD}" fill-opacity=".06" stroke="{GOLD}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    glow = ''.join(f'<rect id="{p}-gl{i}" x="300" y="{Y0 + i * GAP - 14}" width="{W}" height="94" rx="8" fill="{GOLD}" opacity="0"/>' for i in range(4))
    sc.svg(spine + glow + slots + box + content)
    sc.J(f"tl.fromTo('#{p}-sp',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.8,ease:'power2.out',immediateRender:false}},{tk + .3:.3f});")
    sc.sfx('tick', tsl, .3)
    for i in range(4):
        snap(sc, f'#{p}-sl{i}', tsl + i * .18, 'opacity:0,scale:.4,transformOrigin:"50% 50%"', .35)
    # "same things": the empty slots pulse once
    sc.J(f"tl.to('#{p}-sl0,#{p}-sl1,#{p}-sl2,#{p}-sl3',{{scale:1.18,transformOrigin:'50% 50%',duration:.18,yoyo:true,repeat:1,stagger:.08}},{tsm:.3f});")
    for i, (txt, ic, at) in enumerate(rows):
        snap(sc, f'#{p}-o{i}', at, 'opacity:0,x:-28', .35)
        snap(sc, f'#{p}-ic{i}', at, 'opacity:0,scale:.3,transformOrigin:"50% 50%"', .4, 'back.out(2)')
        sc.J(f"tl.to('#{p}-sl{i} circle',{{fill:'{GOLD}',fillOpacity:.35,duration:.25}},{at:.3f});")
        sc.sfx('click', at, .5)
        y = Y0 + i * GAP
        if i == 0:
            sc.J(f"tl.fromTo('#{p}-bx',{{strokeDashoffset:1,y:0,opacity:1}},{{strokeDashoffset:0,duration:.4,ease:'power2.out',immediateRender:false}},{at + .05:.3f});")
        else:
            sc.J(f"tl.to('#{p}-bx',{{y:{i * GAP},duration:.3,ease:'power3.out'}},{at:.3f});")
    # small life on the icons: thermometer pulse, fish wiggle, eye blinks, star spin + pulse
    t1 = rows[0][2]; t2 = rows[1][2]; t4 = rows[3][2]
    sc.J(f"tl.to('#{p}-ic0',{{scale:1.08,transformOrigin:'50% 50%',duration:.5,yoyo:true,repeat:{max(1, int((b - t1) / .5))},ease:'sine.inOut'}},{t1 + .4:.3f});"
         f"tl.to('#{p}-ic1',{{rotation:6,transformOrigin:'50% 50%',duration:.35,yoyo:true,repeat:{max(1, int((b - t2) / .35))},ease:'sine.inOut'}},{t2 + .4:.3f});"
         f"tl.fromTo('#{p}-stari',{{rotation:-30}},{{rotation:20,svgOrigin:'0 0',duration:{max(.5, b - t4):.2f},ease:'power1.out',immediateRender:false}},{t4:.3f});"
         f"tl.to('#{p}-bx',{{scale:1.02,transformOrigin:'50% 50%',strokeWidth:5,duration:.3,yoyo:true,repeat:3,ease:'sine.inOut'}},{t4 + .4:.3f});")
    for k, bt in enumerate((T(ctx, v, 'blink1'), T(ctx, v, 'blink2'))):
        blink(sc, f'#{p}-ey', bt)
    # "nothing else there can": all rows glow once together
    for i in range(4):
        sc.J(f"tl.fromTo('#{p}-gl{i}',{{opacity:0}},{{opacity:.16,duration:.25,yoyo:true,repeat:1,ease:'sine.inOut',immediateRender:false}},{tg + i * .07:.3f});")
    sc.sfx('shimmer', tg, .35)

# ================================================================ S02 the tier ladder (R09)
def s02_ladder(ctx, sc):
    p = sc.p; v = 's02_ladder'; a, b = sc.a, sc.b
    t0 = T(ctx, v, 'steps'); tc = T(ctx, v, 'croc'); tr = T(ctx, v, 'ring'); te = T(ctx, v, 'est'); ts = T(ctx, v, 'shadow')
    tb = T(ctx, v, 'boss'); tv = T(ctx, v, 'surv'); th = T(ctx, v, 'hang')
    SW = 285; L = [70 + i * SW for i in range(4)]; Y = [258 + i * 112 for i in range(4)]
    names = list(TIER)
    # giant shadow (behind the steps, clipped to above the top step)
    sc.defs.append(f'<clipPath id="{p}-shc"><rect x="0" y="0" width="1280" height="{Y[0] + 2}"/></clipPath>')
    shw = 480; shh = SHAPES['theropod'][1] * shw; k = shw / 1000; shx = L[0] - 60
    shadow = (f'<g clip-path="url(#{p}-shc)"><g id="{p}-sh"><g transform="translate({shx:.0f},{Y[0]:.0f}) scale({k:.4f})">'
              + shape_svg('theropod', '#8a7650', 2.5 / k, .55).replace('fill="#1a2429"', 'fill="#040705"').replace('class="shp"', 'class="shx"') +
              f'</g><circle id="{p}-she" cx="{shx + 915 * k:.0f}" cy="{Y[0] - 428 * k:.0f}" r="5" fill="{GOLD}" opacity="0"/></g></g>')
    steps = ''
    for i in range(4):
        x, y = L[i], Y[i]; col = TIER[names[i]]
        steps += (f'<g id="{p}-st{i}" opacity="0"><path d="M{x},{y} H{x + SW} V760 H{x} Z" fill="#0b1611"/>'
                  f'<path d="M{x},{y} H{x + SW}" stroke="{GOLD}" stroke-width="3"/><path d="M{x + SW},{y} V{y + 112}" stroke="{GOLD}" stroke-width="2" stroke-opacity=".6"/>'
                  f'<rect x="{x + 18}" y="{y + 18}" width="7" height="34" fill="{col}"/>'
                  f'<text x="{x + 36}" y="{y + 46}" class="an-svgk" style="font-size:27px;fill:{col if i == 3 else WARM}">{names[i]}</text></g>')
    sc.svg(shadow + steps)
    for i in range(4):
        snap(sc, f'#{p}-st{i}', t0 + .05 + i * .1, 'opacity:0,y:40', .4)
    sc.sfx('swoosh', t0 + .05, .3)
    sc.J(f"tl.to('#{p}-st3 text',{{opacity:.55,duration:1.2,yoyo:true,repeat:{max(1, int(sc.D / 1.2))},ease:'sine.inOut'}},{t0 + .6:.3f});")
    sc.J(f"tl.set('#{p}-sh',{{y:{shh + 40:.0f}}},{a:.3f});")
    # our croc (gape, facing left = up the ladder): cr = x/y, ra = rotation about the belly centre, rb = rotation about the front foot
    cw = 270; cs, ch = croc(ctx, f'{p}-ci', 'gape', 0, 0, cw)
    fx = (700 - 800) * cw / 1600
    def place(i, dx=0): return L[i] + SW / 2 + dx, Y[i] - ch / 2 + 6
    x0, y0 = place(0)
    sc.svg(f'<g transform="translate({x0:.1f},{y0:.1f})"><g id="{p}-cr"><g id="{p}-ra"><g id="{p}-rb">{cs}</g></g></g></g>')
    sc.J(f"tl.fromTo('#{p}-cr',{{opacity:0,y:-170}},{{opacity:1,y:0,duration:.42,ease:'power3.in',immediateRender:false}},{tc:.3f});"
         f"tl.fromTo('#{p}-ci',{{scaleY:.88,transformOrigin:'50% 100%'}},{{scaleY:1,duration:.3,ease:'back.out(3)',immediateRender:false}},{tc + .42:.3f});"
         f"tl.set('#{p}-cr',{{opacity:0}},{a:.3f});")
    sc.sfx('thud', tc + .42, .7)
    sc.J(f"tl.to('#{p}-ci image',{{scaleY:1.05,transformOrigin:'50% 100%',duration:.7,yoyo:true,repeat:{int(sc.D / .7)},ease:'sine.inOut'}},{tc + .8:.3f});")
    blink(sc, f'#{p}-ci-eye', tc + 1.3)
    # "top predator": gold ring pulses out (no flash: this is not a count)
    k_ = len(sc.fx)
    sc.fx.append(''.join(f'<circle id="{p}-tr{j}" cx="{x0:.0f}" cy="{Y[0] - 50:.0f}" r="10" fill="none" stroke="{GOLD}" stroke-width="{3 - j}" opacity="0"/>' for j in range(2)))
    for j in range(2):
        sc.J(f"tl.fromTo('#{p}-tr{j}',{{attr:{{r:20}},opacity:.95}},{{attr:{{r:{170 + 80 * j}}},opacity:0,duration:{1.0 + .3 * j},ease:'power2.out',immediateRender:false}},{tr + .12 * j:.3f});")
    sc.sfx('shimmer', tr, .55)
    lines = [('top predator', tr + .1, te - .15), ('someone else is the boss', ts + .1, tv - .15), ('it hangs on', th, b + 1)]
    for txt, t_in, t_out in lines:
        i_ = sc.line(txt, t_in, y=70, size=58, x=480, w=740, align='right')
        if t_out < b: sc.J(f"tl.to('#{i_}',{{opacity:0,y:-8,duration:.3}},{t_out:.3f});")
    def hop(i_from, i_to, t, dx=0):
        xa, ya = place(i_from); xb, yb = place(i_to, dx)
        sc.J(f"tl.to('#{p}-cr',{{x:{xb - x0:.1f},duration:.5,ease:'power1.inOut'}},{t:.3f});"
             f"tl.to('#{p}-cr',{{y:{min(ya, yb) - y0 - 60:.1f},duration:.22,ease:'power2.out'}},{t:.3f});"
             f"tl.to('#{p}-cr',{{y:{yb - y0:.1f},duration:.28,ease:'power2.in'}},{t + .22:.3f});")
        sc.sfx('thud', t + .5, .55)
    hop(0, 1, te + .05)
    # the shadow rises onto the top step
    sc.J(f"tl.to('#{p}-sh',{{y:0,duration:.9,ease:'power2.out'}},{ts:.3f});"
         f"tl.to('#{p}-sh',{{y:-6,duration:.6,yoyo:true,repeat:{max(1, int((b - tb) / .6))},ease:'sine.inOut'}},{tb:.3f});"
         f"tl.fromTo('#{p}-she',{{opacity:0}},{{opacity:1,duration:.2,immediateRender:false}},{tb:.3f});")
    sc.sfx('swoosh', ts, .4)
    # croc looks up at it (head on the left: clockwise lifts the head)
    sc.J(f"tl.to('#{p}-ra',{{rotation:10,svgOrigin:'0 {ch / 2:.1f}',duration:.35,ease:'power2.out'}},{tb:.3f});"
         f"tl.to('#{p}-ra',{{rotation:0,svgOrigin:'0 {ch / 2:.1f}',duration:.25,ease:'power2.inOut'}},{tv - .05:.3f});")
    blink(sc, f'#{p}-ci-eye', tb + .5)
    # down to SURVIVE, landing near the right edge (the drop to WIPED OUT)
    edge = L[2] + SW; land_dx = edge - (L[2] + SW / 2) - fx - 70
    hop(1, 2, tv + .05, land_dx)
    # hangs on: slides back over the edge, front claws on the lip, slips a little and holds
    xf, yf = place(2, edge - (L[2] + SW / 2) - fx - 4)
    sc.J(f"tl.to('#{p}-cr',{{x:{xf - x0:.1f},duration:.3,ease:'power2.in'}},{th - .15:.3f});"
         f"tl.to('#{p}-rb',{{rotation:26,svgOrigin:'{fx:.1f} {ch / 2:.1f}',duration:.35,ease:'power2.in'}},{th + .15:.3f});"
         f"tl.to('#{p}-cr',{{y:'+=10',duration:.3,ease:'power2.in'}},{th + .15:.3f});"
         f"tl.to('#{p}-rb',{{rotation:20,svgOrigin:'{fx:.1f} {ch / 2:.1f}',duration:.25,ease:'back.out(3)'}},{th + .5:.3f});"
         f"tl.to('#{p}-rb',{{rotation:23,svgOrigin:'{fx:.1f} {ch / 2:.1f}',duration:.45,yoyo:true,repeat:3,ease:'sine.inOut'}},{th + .75:.3f});")
    sc.sfx('scratch', th + .15, .45)
    blink(sc, f'#{p}-ci-eye', th + .8)
    blink(sc, f'#{p}-ci-eye', tc + 3.9)
    sc.dust(26, 7); sc.specks(26, 8, y0=60, y1=320)

# ================================================================ S03 bite force (C01-17)  (same geometry as anim_gauge "bars")
def s03_bite(ctx, sc):
    p = sc.p; v = 's03_bite'; a, b = sc.a, sc.b
    val = float(ctx.p('value', 16414)); unit = ctx.p('unit', 'N')
    tk = T(ctx, v, 'kick'); tam = T(ctx, v, 'amph'); tcl = T(ctx, v, 'close'); tou = T(ctx, v, 'our'); tco = T(ctx, v, 'count'); tla = T(ctx, v, 'land')
    sc.dust(36, 11)
    sc.kicker('Bite *force*', tk, y=78, x=110, w=900, align='left', size=28)
    L0, L1 = 360, 1110; ys = [300, 470]
    amph_x = L0 + (L1 - L0) * .2
    # row 0: big amphibians (line-art, no number: the script only says "nowhere close")
    g0, _ = glyph(ctx, f'{p}-g0', {'shape': 'amphibian'}, 210, ys[0] + 26, 190)
    cs, chh = croc(ctx, f'{p}-g1', 'gape', 210, ys[1] - 4, 200, flip=True)
    svg = ''
    for k, (gl, lab) in enumerate(((g0, 'BIG AMPHIBIANS'), (cs, 'OUR CROC'))):
        y = ys[k]; col = SOFT if k == 0 else GOLD
        svg += (f'<g id="{p}-r{k}" opacity="0">{gl}'
                f'<line x1="{L0}" y1="{y}" x2="{L1}" y2="{y}" stroke="{WARM}" stroke-opacity=".16" stroke-width="16" stroke-linecap="round"/>'
                f'<line id="{p}-b{k}" x1="{L0}" y1="{y}" x2="{L0}" y2="{y}" stroke="{col}" stroke-width="16" stroke-linecap="round"/>'
                f'<circle id="{p}-d{k}" cx="{L0}" cy="{y}" r="9" fill="{col}" opacity="0"/>'
                f'<line id="{p}-gl{k}" x1="{L0}" y1="{y}" x2="{L0 + 50}" y2="{y}" stroke="#fff6dc" stroke-width="6" stroke-linecap="round" opacity="0"/></g>')
        sc.add_html(f'<div id="{p}-l{k}" class="an-a an-k" style="left:60px;width:300px;text-align:center;top:{y + (52 if k == 0 else 64):.0f}px;font-size:24px;opacity:0">{lab}</div>')
    sc.svg(svg)
    for k, at in enumerate((tk + .25, tk + .55)):
        sc.J(f"tl.fromTo('#{p}-r{k}',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.35,ease:'power3.out',immediateRender:false}},{at:.3f});"
             f"tl.fromTo('#{p}-l{k}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.4,ease:'power2.out',immediateRender:false}},{at + .1:.3f});")
    # amphibian bar: grows a little and stops short
    sc.J(f"tl.fromTo('#{p}-b0',{{attr:{{x2:{L0}}}}},{{attr:{{x2:{amph_x:.0f}}},duration:.7,ease:'power2.out',immediateRender:false}},{tam:.3f});"
         f"tl.to('#{p}-b0',{{attr:{{x2:{amph_x + 8:.0f}}},duration:.12,yoyo:true,repeat:1}},{tam + .7:.3f});")
    sc.sfx('swoosh', tk + .25, .3); sc.sfx('ticks', tam, .3, .7)
    nc = sc.line('nowhere close', tcl - .2, y=ys[0] + 26, size=40, x=amph_x + 40, w=600, align='left')
    sc.J(f"tl.to('#{p}-g0',{{opacity:.55,duration:.5}},{tcl + .2:.3f});")
    # anticipation: our empty bar's start dot breathes; label turns gold on "Our"
    sc.J(f"tl.fromTo('#{p}-d1',{{opacity:.2,attr:{{r:7}}}},{{opacity:1,attr:{{r:13}},duration:.35,yoyo:true,repeat:{max(1, int((tco - tcl) / .35))},ease:'sine.inOut',immediateRender:false}},{tcl:.3f});"
         f"tl.to('#{p}-d1',{{opacity:0,duration:.1}},{tco:.3f});"
         f"tl.to('#{p}-l1',{{color:'{GOLD}',scale:1.1,duration:.3}},{tou:.3f});"
         f"tl.fromTo('#{p}-g1',{{x:0}},{{x:14,duration:.18,yoyo:true,repeat:1,ease:'power2.out',immediateRender:false}},{tou:.3f});")
    sc.sfx('tick', tcl, .3)
    blink(sc, f'#{p}-g1-eye', tou + .5)
    # count-up and land
    dur = max(.8, tla - tco)
    sc.J(f"tl.fromTo('#{p}-b1',{{attr:{{x2:{L0}}}}},{{attr:{{x2:{L1}}},duration:{dur:.2f},ease:'power2.in',immediateRender:false}},{tco:.3f});")
    y = ys[1]
    sc.add_html(f'<div id="{p}-n1" class="an-a an-big" style="left:{L1 - 470}px;top:{y + 44:.0f}px;width:500px;text-align:right;font-size:76px;opacity:0"></div>')
    fmt = f"v=>Math.round(v).toLocaleString('en-US')+'<i style=\"font-size:36px\"> {esc(unit)}</i>'"
    sc.J(f"tl.set('#{p}-n1',{{opacity:1}},{tco:.3f});counter('#{p}-n1',{tco:.3f},{dur:.2f},0,{val},{fmt},'power2.in');"
         f"tl.fromTo('#{p}-n1',{{scale:1.18,transformOrigin:'100% 50%'}},{{scale:1,duration:.4,ease:'power3.out',immediateRender:false}},{tla:.3f});"
         f"tl.fromTo('#{p}-g1',{{scale:1.12,transformOrigin:'50% 50%'}},{{scale:1,duration:.35,ease:'power3.out',immediateRender:false}},{tla:.3f});"
         f"tl.fromTo('#{p}-gl1',{{x:0,opacity:0}},{{x:{L1 - L0 - 50},opacity:.8,duration:1.0,ease:'sine.inOut',immediateRender:false}},{tla + .4:.3f});")
    sc.sfx('ticks_up', tco, .45, dur)
    sc.land(tla, L1, y)

# ================================================================ S04 fires, so it goes in the water (C01-21)
def s04_fire(ctx, sc):
    p = sc.p; v = 's04_fire'; a, b = sc.a, sc.b
    tf = [T(ctx, v, 'f1'), T(ctx, v, 'f2'), T(ctx, v, 'f3')]; tl_ = T(ctx, v, 'look'); tsl = T(ctx, v, 'slide'); tey = T(ctx, v, 'eyes')
    WY = 468
    # layered coal swamp: far tree ferns hazy, mid darker, near bank
    far = ''.join(f'<path d="M{x},{WY} C{x + 4},{WY - 120} {x - 6},{WY - 200} {x + 2},{WY - h}" stroke="#2c4a3b" stroke-width="10" fill="none"/>' + ''.join(f'<g transform="rotate({an} {x + 2} {WY - h})">' + frond(x + 2, WY - h, 120, 0, '#2c4a3b', 8) + '</g>' for an in (-125, -90, -55, 55, 90, 125))
                  for x, h in ((80, 300), (260, 340), (520, 280), (760, 330), (980, 300), (1180, 350)))
    mid = ''.join(f'<path d="M{x},{WY + 10} C{x + 6},{WY - 120} {x - 8},{WY - 220} {x},{WY - h}" stroke="#16291f" stroke-width="16" fill="none"/>' + ''.join(f'<g transform="rotate({an} {x} {WY - h})">' + frond(x, WY - h, 170, 0, '#16291f', 9) + '</g>' for an in (-128, -92, -56, 56, 92, 128))
                  for x, h in ((170, 380), (640, 420), (1100, 400)))
    sc.svg(f'<rect x="-100" y="0" width="1500" height="{WY}" fill="#2a4535" opacity=".25"/>' + far, drift=-14, sway=1.2)
    sc.defs.append(f'<radialGradient id="{p}-fg"><stop offset="0" stop-color="#e0902e" stop-opacity=".45"/><stop offset="1" stop-color="#e0902e" stop-opacity="0"/></radialGradient>'
                   f'<radialGradient id="{p}-smg"><stop offset="0" stop-color="#bdb7a2" stop-opacity=".9"/><stop offset=".6" stop-color="#bdb7a2" stop-opacity=".35"/><stop offset="1" stop-color="#bdb7a2" stop-opacity="0"/></radialGradient>')
    sc.svg(f'<ellipse id="{p}-fgl" cx="300" cy="{WY - 60}" rx="460" ry="200" fill="url(#{p}-fg)"/>')
    sc.J(f"tl.fromTo('#{p}-fgl',{{opacity:.6}},{{opacity:1,duration:.25,yoyo:true,repeat:{int(sc.D / .25)},ease:'sine.inOut'}},{a:.3f});")
    sc.svg(mid, drift=-26, sway=1.6)
    # bank (left) sloping into the water (right)
    bank = f'<path d="M-100,{WY - 30} C200,{WY - 46} 520,{WY - 40} 700,{WY - 14} C780,{WY} 820,{WY + 20} 860,{WY + 40} L860,760 L-100,760 Z" fill="#101d16"/><path d="M-100,{WY - 30} C200,{WY - 46} 520,{WY - 40} 700,{WY - 14} C780,{WY} 820,{WY + 20} 860,{WY + 40}" fill="none" stroke="#3b5a45" stroke-width="2"/>'
    flames = ''.join(flame(f'{p}-fl{i}', x, WY - 34 - (i % 2) * 4, s) for i, (x, s) in enumerate(((120, 1.0), (300, .85), (460, 1.1), (40, .8))))
    smoke = ''.join(f'<ellipse id="{p}-sm{i}" cx="{x}" cy="{WY - 150}" rx="{rx}" ry="{rx * .6:.0f}" fill="url(#{p}-smg)" opacity="0"/>' for i, (x, rx) in enumerate(((120, 70), (300, 60), (460, 80), (40, 60), (250, 110), (520, 120))))
    sc.svg(water_band(p + 'w', WY + 6, '#0b1a14'), lid=f'{p}-wat'); sc.glints(f'{p}-wat')
    sc.svg(smoke + bank + flames)
    # flames: first already burning, three more pop one per beat, all flicker
    for i in range(4):
        t_on = a if i == 3 else tf[i]
        snap(sc, f'#{p}-fl{i}', t_on, 'opacity:0,scale:.2,transformOrigin:"50% 100%"', .35, 'back.out(2)')
        sc.J(f"tl.to('#{p}-fl{i}f',{{scaleY:1.12,scaleX:.94,transformOrigin:'50% 100%',duration:.16 + {i * .03:.2f},yoyo:true,repeat:{int(sc.D / .16)},ease:'sine.inOut'}},{t_on:.3f});")
    for i in range(6):
        t_s = a + .1 + i * .35
        sc.J(f"tl.fromTo('#{p}-sm{i}',{{opacity:0,y:20,x:0,scale:.6,transformOrigin:'50% 50%'}},{{opacity:.55,y:-120,x:160,scale:1.8,duration:{max(1.0, b - t_s):.2f},ease:'power1.out',immediateRender:false}},{t_s:.3f});")
    # our croc on the bank, facing the water (right)
    cw = 330; cs, ch = croc(ctx, f'{p}-cr', 'gape', 0, 0, cw, flip=True)
    cx, cy = 600, WY - 40 - ch / 2 + 22
    sc.svg(f'<g transform="translate({cx},{cy:.1f})">{cs}</g>')
    snap(sc, f'#{p}-cr', a, 'opacity:0,x:-30', .4)
    # turns its head to the fire: tilt back, slow deadpan blink
    sc.J(f"tl.to('#{p}-cr',{{rotation:-5,svgOrigin:'0 {ch / 2:.0f}',duration:.35,ease:'power2.out'}},{tl_:.3f});"
         f"tl.to('#{p}-cr-eye',{{scaleY:.08,transformOrigin:'50% 50%',duration:.18,yoyo:true,repeat:1,repeatDelay:.3}},{tl_ + .3:.3f});"
         f"tl.to('#{p}-cr',{{rotation:0,duration:.3}},{tsl - .3:.3f});")
    sc.sfx('swoosh', a, .25)
    # slides in: splash ring
    sc.J(f"tl.to('#{p}-cr',{{x:330,y:70,rotation:8,duration:.6,ease:'power2.in'}},{tsl:.3f});tl.to('#{p}-cr',{{opacity:0,duration:.2}},{tsl + .45:.3f});")
    sx, sy = 960, WY + 14
    sc.svg(''.join(f'<ellipse id="{p}-rp{i}" cx="{sx}" cy="{sy}" rx="30" ry="7" fill="none" stroke="#e9dcc0" stroke-width="3" opacity="0"/>' for i in range(3))
           + ''.join(f'<circle id="{p}-dr{i}" cx="{sx + (i - 3) * 14}" cy="{sy}" r="5" fill="#cfe0c4" opacity="0"/>' for i in range(7)))
    for i in range(3):
        sc.J(f"tl.fromTo('#{p}-rp{i}',{{attr:{{rx:30,ry:7}},opacity:.9}},{{attr:{{rx:{150 + i * 60},ry:{20 + i * 6}}},opacity:0,duration:1.1,ease:'power2.out',immediateRender:false}},{tsl + .55 + i * .18:.3f});")
    for i in range(7):
        sc.J(f"tl.fromTo('#{p}-dr{i}',{{opacity:1,x:0,y:0}},{{opacity:0,x:{(i - 3) * 22},y:{-60 - (i % 3) * 20},duration:.55,ease:'power2.out',immediateRender:false}},{tsl + .55:.3f});")
    # only eyes and nostrils above the wave line
    ex = 1010
    bumps = (f'<g id="{p}-ey" opacity="0"><g transform="translate({ex},{WY}) scale(1.7) translate({-ex},{-WY})"><path d="M{ex - 60},{WY + 8} q12,-20 26,0 M{ex - 20},{WY + 8} q12,-20 26,0 M{ex + 70},{WY + 8} q8,-12 18,0" fill="#5d5a33" stroke="#c9a45c" stroke-width="2.5"/>'
             f'<g id="{p}-eyi"><ellipse cx="{ex - 47}" cy="{WY}" rx="5" ry="4" fill="#e2b453"/><ellipse cx="{ex - 7}" cy="{WY}" rx="5" ry="4" fill="#e2b453"/>'
             f'<ellipse cx="{ex - 47}" cy="{WY}" rx="1.2" ry="3.4" fill="#120e06"/><ellipse cx="{ex - 7}" cy="{WY}" rx="1.2" ry="3.4" fill="#120e06"/></g></g></g>'
             + f'<path d="{waterline(WY + 8, 880, 1200, 4, 60)} V{WY + 30} H900 Z" fill="#0b1a14"/>')
    sc.svg(bumps)
    sc.J(f"tl.fromTo('#{p}-ey',{{opacity:0,y:16}},{{opacity:1,y:0,duration:.45,ease:'power3.out',immediateRender:false}},{tey - .25:.3f});"
         f"tl.to('#{p}-ey',{{x:-12,duration:{max(.4, b - tey):.2f},ease:'sine.inOut'}},{tey + .2:.3f});")
    blink(sc, f'#{p}-eyi', tey + .35)
    # smoke rolls over the top
    sc.svg(f'<ellipse id="{p}-big" cx="200" cy="320" rx="520" ry="170" fill="url(#{p}-smg)" opacity="0"/>')
    sc.J(f"tl.fromTo('#{p}-big',{{opacity:0,x:0}},{{opacity:.5,x:520,duration:{max(.6, b - tey + .3):.2f},ease:'none',immediateRender:false}},{tey - .3:.3f});")
    sc.specks(22, 4, col='#f0b54a', y0=280, y1=440)

# ================================================================ S05 mud, then WATER | BANK (C02-21)
def s05_mud(ctx, sc):
    p = sc.p; v = 's05_mud'; a, b = sc.a, sc.b
    tw = T(ctx, v, 'waits'); tc = T(ctx, v, 'card'); tb = T(ctx, v, 'blink'); ts = T(ctx, v, 'split'); tr = T(ctx, v, 'rule'); tst = T(ctx, v, 'steps'); twk = T(ctx, v, 'walk')
    # --- part A: dry plain, cracked mud pool, sun / moon
    G = 470
    sky = f'<rect id="{p}-nt" x="-100" y="-100" width="1500" height="1000" fill="#020504" opacity="0"/>'
    sun = f'<g id="{p}-sun"><circle cx="0" cy="0" r="38" fill="#f0c766" opacity=".9"/><circle cx="0" cy="0" r="60" fill="#f0c766" opacity=".15"/></g>'
    moon = f'<g id="{p}-moon" opacity="0"><circle cx="0" cy="0" r="30" fill="#e9dcc0"/><circle cx="12" cy="-8" r="26" fill="#0c1712"/></g>'
    plain = (f'<path d="M-100,{G} C300,{G - 14} 900,{G + 8} 1400,{G - 6} L1400,760 L-100,760 Z" fill="#1c241a"/>'
             + reeds(31, 18, G - 2, G + 4, '#2a3a27', 20, 60))
    cracks = ''.join(f'<path d="M{x},{y} l{dx},{dy} l{dx2},{dy2}" stroke="#4b4232" stroke-width="2" fill="none"/>' for x, y, dx, dy, dx2, dy2 in
                     ((300, 560, 40, 20, 30, -10), (420, 610, -30, 30, 20, 20), (820, 570, 50, 10, 20, 30), (900, 640, -40, 20, -20, 30), (250, 650, 50, -10, 40, 20), (1000, 600, 30, 30, 50, -5)))
    pool = f'<g id="{p}-pool"><ellipse cx="640" cy="560" rx="380" ry="80" fill="#3a3326" stroke="#6b5c43" stroke-width="3"/><ellipse cx="640" cy="565" rx="300" ry="54" fill="#2b261c"/>{cracks}</g>'
    cw = 520; cs, ch = croc(ctx, f'{p}-cr', 'swim', 0, 0, cw, rot=15)
    sc.defs.append(f'<clipPath id="{p}-mc"><rect x="0" y="0" width="1280" height="556"/></clipPath>')
    crA = f'<g clip-path="url(#{p}-mc)"><g transform="translate(640,{556 + ch * .02:.0f})">{cs}</g></g>'
    mudline = f'<path d="M290,556 C420,548 860,550 990,558" stroke="#6b5c43" stroke-width="3" fill="none"/>'
    card = (f'<g id="{p}-card" opacity="0"><rect x="880" y="250" width="300" height="130" rx="10" fill="#0c1712" stroke="{GOLD}" stroke-width="3"/>'
            f'<rect x="896" y="266" width="64" height="64" rx="6" fill="none" stroke="{GOLD}" stroke-opacity=".6" stroke-width="2"/>'
            f'<g transform="translate(928,302) scale(.18)">{ICONS["croc"]}</g>'
            f'<text x="976" y="294" class="an-svgk" style="font-size:20px">HOBBIES</text>'
            f'<text x="976" y="340" style="font-family:\'Cormorant Garamond\',serif;font-style:italic;font-weight:600;font-size:40px" fill="{ITAL}">waiting</text></g>')
    sc.svg(f'<g id="{p}-A">{sky}{sun}{moon}{plain}{pool}{crA}{mudline}{card}</g>')
    snap(sc, f'#{p}-cr', a, 'opacity:0,y:30', .45)
    sc.J(f"tl.set('#{p}-sun',{{x:1060,y:150}},{a:.3f});tl.set('#{p}-moon',{{x:120,y:330}},{a:.3f});"
         f"tl.to('#{p}-cr',{{y:-5,duration:.8,yoyo:true,repeat:{int(sc.D / .8)},ease:'sine.inOut'}},{a + .5:.3f});")
    # two fast day-night cycles from "waits": sun sets right, moon arcs over, sun again
    cyc = .62
    for k in range(2):
        t = tw + k * cyc * 2
        sc.J(f"tl.to('#{p}-sun',{{keyframes:[{{x:1180,y:420,duration:{cyc * .5:.2f}}}],ease:'power1.in'}},{t:.3f});"
             f"tl.to('#{p}-nt',{{opacity:.55,duration:{cyc * .5:.2f}}},{t:.3f});"
             f"tl.set('#{p}-moon',{{x:120,y:430,opacity:1}},{t + cyc * .5:.3f});"
             f"tl.to('#{p}-moon',{{keyframes:[{{x:640,y:110,duration:{cyc * .5:.2f},ease:'power1.out'}},{{x:1180,y:430,duration:{cyc * .5:.2f},ease:'power1.in'}}]}},{t + cyc * .5:.3f});"
             f"tl.set('#{p}-sun',{{x:100,y:430}},{t + cyc * .5:.3f});"
             f"tl.to('#{p}-nt',{{opacity:0,duration:{cyc * .5:.2f}}},{t + cyc * 1.5:.3f});"
             f"tl.to('#{p}-sun',{{keyframes:[{{x:{640 if k == 0 else 1060},y:{110 if k == 0 else 150},duration:{cyc * .5:.2f}}}],ease:'power1.out'}},{t + cyc * 1.5:.3f});")
        sc.sfx('swoosh', t, .3)
    sc.J(f"tl.to('#{p}-pool',{{scaleX:.86,scaleY:.9,transformOrigin:'640px 560px',duration:{cyc * 4:.2f},ease:'power1.inOut'}},{tw:.3f});")
    sc.J(f"tl.fromTo('#{p}-card',{{opacity:0,scale:.6,transformOrigin:'1030px 315px'}},{{opacity:1,scale:1,duration:.4,ease:'back.out(2)',immediateRender:false}},{tc:.3f});"
         f"tl.to('#{p}-card',{{rotation:-2,svgOrigin:'1030 315',duration:.9,yoyo:true,repeat:3,ease:'sine.inOut'}},{tc + .4:.3f});")
    sc.sfx('click', tc, .55)
    sc.J(f"tl.to('#{p}-cr-eye',{{scaleY:.08,transformOrigin:'50% 50%',duration:.2,yoyo:true,repeat:1,repeatDelay:.25}},{tb:.3f});")
    blink(sc, f'#{p}-cr-eye', a + .9)
    sc.J(f"tl.to('#{p}-A',{{opacity:0,duration:.35}},{ts - .05:.3f});")
    # --- part B: WATER | BANK
    WYB = 430
    left = (f'<path d="{waterline(WYB, -100, 650, 6, 120)} V760 H-100 Z" fill="#0b1a14"/><path d="{waterline(WYB, -100, 650, 6, 120)}" fill="none" stroke="{SOFT}" stroke-width="2.5" stroke-opacity=".5"/>'
            + ''.join(f'<path class="gl" d="M{x},{y} h{w}" stroke="{SOFT}" stroke-width="2" stroke-linecap="round" opacity=".25"/>' for x, y, w in ((60, 520, 80), (300, 600, 110), (450, 480, 60), (120, 650, 90), (520, 690, 70))))
    cs2, ch2 = croc(ctx, f'{p}-cb', 'swim', 0, 0, 470, rot=15)
    sc.defs.append(f'<clipPath id="{p}-wc"><rect x="0" y="0" width="640" height="{WYB + 4}"/></clipPath>')
    crB = (f'<g id="{p}-cbw"><g clip-path="url(#{p}-wc)"><g transform="translate(330,{WYB + ch2 * .06:.0f})">{cs2}</g></g>'
           f'<g opacity=".35"><g transform="translate(330,{WYB + ch2 * .06 + 8:.0f})">{croc(ctx, p + "-cbg", "swim", 0, 0, 470, rot=15, eye=False)[0]}</g></g></g>')
    right = (f'<rect x="640" y="0" width="700" height="760" fill="#121a12" opacity=".5"/>'
             f'<path d="M640,{WYB} C800,{WYB - 10} 1000,{WYB - 4} 1400,{WYB - 12} L1400,760 L640,760 Z" fill="#1b2318"/>' + reeds(41, 12, WYB - 4, WYB + 2, '#2a3a27', 30, 80, 660, 1300))
    prints = ''.join(f'<g id="{p}-ap{i}" opacity="0">{three_toe(x, y, 1.3, r)}</g>' for i, (x, y, r) in enumerate(((720, 560, 80), (860, 650, 100), (1160, 560, 80))))
    cprint = f'<g id="{p}-cp" opacity="0">{croc_print(1005, 625, 1.2)}</g>'
    xmk = f'<path id="{p}-x" d="M955,575 L1055,675 M1055,575 L955,675" stroke="{GOLD}" stroke-width="9" stroke-linecap="round" fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    ring = f'<circle id="{p}-rg" cx="330" cy="{WYB}" r="10" fill="none" stroke="{GOLD}" stroke-width="3" opacity="0"/>'
    tick = f'<path id="{p}-tk" d="M300,250 l22,22 l44,-50" stroke="{GOLD}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    hair = f'<line id="{p}-hl" x1="640" y1="40" x2="640" y2="700" stroke="{GOLD}" stroke-width="2.5"/>'
    sc.svg(f'<g id="{p}-B" opacity="0">{left}{crB}{right}{prints}{cprint}{xmk}{ring}{tick}{hair}</g>')
    sc.add_html(f'<div id="{p}-kw" class="an-a an-k" style="left:0;width:640px;top:120px;text-align:center;font-size:30px;opacity:0">Water</div>'
                f'<div id="{p}-kb" class="an-a an-k" style="left:640px;width:640px;top:120px;text-align:center;font-size:30px;opacity:0">Bank</div>')
    sc.J(f"tl.set('#{p}-B',{{opacity:1}},{ts:.3f});"
         f"tl.fromTo('#{p}-hl',{{scaleY:0,transformOrigin:'640px 370px'}},{{scaleY:1,duration:.4,ease:'power3.out',immediateRender:false}},{ts:.3f});"
         f"tl.fromTo('#{p}-B > path, #{p}-B > rect, #{p}-B > g:not([id])',{{opacity:0}},{{opacity:1,duration:.35,immediateRender:false}},{ts + .05:.3f});"
         f"tl.fromTo('#{p}-cbw',{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.45,ease:'power3.out',immediateRender:false}},{ts + .1:.3f});"
         f"tl.to('#{p}-cbw',{{x:30,duration:{max(.5, b - ts):.2f},ease:'sine.inOut'}},{ts + .55:.3f});")
    snap(sc, f'#{p}-kw', ts + .1, 'opacity:0,y:10', .4); snap(sc, f'#{p}-kb', ts + .2, 'opacity:0,y:10', .4)
    sc.glints(f'{p}-L{sc.n}')
    sc.sfx('swoosh', ts, .35)
    # "rule the water": gold ring + tick
    sc.J(f"tl.fromTo('#{p}-rg',{{attr:{{r:20}},opacity:1}},{{attr:{{r:260}},opacity:0,duration:1.0,ease:'power2.out',immediateRender:false}},{tr:.3f});"
         f"tl.fromTo('#{p}-tk',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.35,ease:'power2.out',immediateRender:false}},{tr + .1:.3f});"
         f"tl.to('#{p}-kw',{{color:'{GOLD}',duration:.3}},{tr:.3f});")
    sc.flash(tr, .12); sc.sfx('tick', tr, .5)
    blink(sc, f'#{p}-cb-eye', tr + .9)
    # "never go for a walk": three Allosaurus prints stamp in, one croc print steps out, gold X
    for i in range(3):
        t = tst - .25 + i * .2
        sc.J(f"tl.fromTo('#{p}-ap{i}',{{opacity:0,scale:1.5,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.18,ease:'power3.in',immediateRender:false}},{t:.3f});")
    sc.J(f"tl.fromTo('#{p}-cp',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.3,ease:'power2.out',immediateRender:false}},{twk - .35:.3f});")
    sc.J(f"tl.fromTo('#{p}-x',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.3,ease:'power2.out',immediateRender:false}},{twk:.3f});"
         f"tl.to('#{p}-kb',{{opacity:.5,duration:.3}},{twk + .1:.3f});")
    sc.sfx('click', twk, .6)
    sc.dust(24, 9)

# ================================================================ S06 14 degrees (C03-14)
def s06_temp(ctx, sc):
    p = sc.p; v = 's06_temp'; a, b = sc.a, sc.b
    tk = T(ctx, v, 'kick'); tsb = T(ctx, v, 'sub'); tco = T(ctx, v, 'count'); tla = T(ctx, v, 'land'); tbe = T(ctx, v, 'below'); tbk = T(ctx, v, 'bank'); tfi = T(ctx, v, 'find')
    sc.dust(30, 19); sc.specks(24, 20, y0=120, y1=420)
    sc.kicker('What crocodiles *need*', tk, y=60, x=110, w=900, align='left', size=28)
    sc.line('an average year', tsb, y=108, size=40, x=110, w=700, align='left')
    sc.sfx('tick', tsb, .3)
    X, Y0, Y1, MX = 210, 600, 170, 30.0
    Yv = lambda q: Y0 - (Y0 - Y1) * q / MX
    y14 = Yv(14)
    # the region under the line: empty riverbank with reeds (frosts over)
    bank = (f'<g id="{p}-bk" opacity="0"><path d="M420,560 C640,540 860,552 1300,530 L1300,760 L420,760 Z" fill="#14231b"/>'
            f'<path d="{waterline(600, 420, 1300, 5, 110)} V760 H420 Z" fill="#0b1a14"/><path d="{waterline(600, 420, 1300, 5, 110)}" stroke="{SOFT}" stroke-opacity=".5" stroke-width="2" fill="none"/>'
            + reeds(51, 18, 548, 566, '#2b4535', 50, 120, 450, 1280) + '</g>')
    ghost_w = 300
    ghost = (f'<g id="{p}-gh" opacity="0"><g transform="translate(760,592) scale({ghost_w / 1000:.3f})">'
             + shape_svg('croc', WARM, 3 / (ghost_w / 1000), .9).replace('fill="#1a2429"', 'fill="none"').replace('class="shp"', f'class="shp" stroke-dasharray="{14 / (ghost_w / 1000):.0f} {10 / (ghost_w / 1000):.0f}"') + '</g></g>')
    sc.svg(bank + ghost, sway=1.4)
    # thermometer
    th = f'<g id="{p}-th" opacity="0"><rect x="{X - 28}" y="{Y1 - 20}" width="56" height="{Y0 - Y1 + 30}" rx="28" fill="{WARM}" fill-opacity=".06" stroke="{WARM}" stroke-opacity=".45" stroke-width="2.5"/>'
    th += f'<circle cx="{X}" cy="{Y0 + 40}" r="44" fill="#0c1712" stroke="{WARM}" stroke-opacity=".45" stroke-width="2.5"/><circle id="{p}-bulb" cx="{X}" cy="{Y0 + 40}" r="30" fill="{GOLD}"/>'
    for q in range(0, 31, 5):
        yy = Yv(q)
        th += f'<line x1="{X + 34}" y1="{yy:.0f}" x2="{X + 52}" y2="{yy:.0f}" stroke="{WARM}" stroke-opacity=".55" stroke-width="2"/><text x="{X + 62}" y="{yy + 8:.0f}" class="an-svgk" style="font-size:22px;letter-spacing:.05em;opacity:.75">{q}</text>'
    th += f'<line id="{p}-merc" x1="{X}" y1="{Y0 + 10}" x2="{X}" y2="{Y0 + 10}" stroke="{GOLD}" stroke-width="26" stroke-linecap="round"/></g>'
    line14 = f'<line id="{p}-l14" x1="{X + 30}" y1="{y14:.1f}" x2="1240" y2="{y14:.1f}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="14 9" opacity="0"/>'
    sc.svg(th + line14)
    snap(sc, f'#{p}-th', tk + .2, 'opacity:0,y:30', .45); sc.sfx('swoosh', tk + .2, .3)
    sc.J(f"tl.to('#{p}-bulb',{{attr:{{r:34}},duration:.5,yoyo:true,repeat:{max(1, int((tco - tk) / .5))},ease:'sine.inOut'}},{tk + .6:.3f});")
    # count 0 -> 14 and land
    dur = max(.8, tla - tco)
    sc.J(f"tl.fromTo('#{p}-merc',{{attr:{{y2:{Y0 + 10}}}}},{{attr:{{y2:{y14:.1f}}},duration:{dur:.2f},ease:'power2.in',immediateRender:false}},{tco:.3f});")
    sc.add_html(f'<div id="{p}-big" class="an-a an-big" style="left:430px;width:600px;top:{y14 - 150:.0f}px;font-size:120px;opacity:0"></div>')
    fmt = "v=>Math.round(v)+'<span class=\"deg\">&deg;</span><i style=\"font-size:60px\">C</i>'"
    sc.J(f"tl.set('#{p}-big',{{opacity:1}},{tco:.3f});counter('#{p}-big',{tco:.3f},{dur:.2f},0,14,{fmt},'power2.in');"
         f"tl.fromTo('#{p}-big',{{scale:1.18,transformOrigin:'0% 50%'}},{{scale:1,duration:.4,ease:'power3.out',immediateRender:false}},{tla:.3f});"
         f"tl.fromTo('#{p}-l14',{{opacity:1,scaleX:0,transformOrigin:'{X + 30}px {y14:.0f}px'}},{{scaleX:1,duration:.5,ease:'power3.out',immediateRender:false}},{tla + .05:.3f});")
    sc.sfx('ticks_up', tco, .45, dur); sc.land(tla, X, y14)
    # "Below that": frost creeps up from the bottom to the line
    fr = f'<rect id="{p}-fr" x="0" y="{y14:.1f}" width="1280" height="{720 - y14 + 40:.0f}" fill="url(#{p}-frg)" opacity="0"/>'
    sc.defs.append(f'<linearGradient id="{p}-frg" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#e6f0ec" stop-opacity=".5"/><stop offset=".7" stop-color="#d8e6e0" stop-opacity=".18"/><stop offset="1" stop-color="#d8e6e0" stop-opacity=".05"/></linearGradient>')
    r = random.Random(7); cr = ''
    for i in range(16):
        x = r.uniform(60, 1240); y = r.uniform(y14 + 40, 700); s = r.uniform(.12, .26)
        cr += f'<g id="{p}-ice{i}" opacity="0"><g transform="translate({x:.0f},{y:.0f}) scale({s:.2f})">{ICONS["snowflake"].replace("#fff", "#e8f2ee").replace("stroke-width=\"7\"", "stroke-width=\"9\"")}</g></g>'
    sc.svg(fr + cr)
    sc.J(f"tl.fromTo('#{p}-fr',{{opacity:0,scaleY:0,transformOrigin:'50% 100%'}},{{opacity:1,scaleY:1,duration:1.0,ease:'power2.out',immediateRender:false}},{tbe:.3f});")
    for i in range(16):
        sc.J(f"tl.fromTo('#{p}-ice{i}',{{opacity:0,scale:.2,transformOrigin:'50% 50%'}},{{opacity:.85,scale:1,duration:.35,ease:'back.out(2)',immediateRender:false}},{tbe + .1 + i * .07:.3f});"
             f"tl.to('#{p}-ice{i}',{{rotation:{30 if i % 2 else -30},transformOrigin:'50% 50%',duration:{max(.5, b - tbe - 1):.2f},ease:'none'}},{tbe + .5:.3f});")
    # empty riverbank under the line; a dashed croc outline shows, then fades: none here
    snap(sc, f'#{p}-bk', tbk - .5, 'opacity:0,y:30', .5)
    sc.J(f"tl.fromTo('#{p}-gh',{{opacity:0}},{{opacity:.75,duration:.3,immediateRender:false}},{tbk:.3f});"
         f"tl.to('#{p}-gh',{{opacity:0,x:20,duration:.6,ease:'power2.in'}},{tfi + .1:.3f});")
    sc.sfx('tick', tbk, .25)
    sc.J(f"tl.to('#{p}-big',{{color:'#e6f0ec',duration:.6}},{tbe:.3f});")

FN = {'s01_checks': s01_checks, 's02_ladder': s02_ladder, 's03_bite': s03_bite, 's04_fire': s04_fire, 's05_mud': s05_mud, 's06_temp': s06_temp}

def build(ctx):
    v = ctx.variant
    push = {'s04_fire': (1.0, 1.06, '70% 70%'), 's05_mud': (1.0, 1.04, '50% 60%')}.get(v, (1.0, 1.04, '50% 50%'))
    sc = Scene(ctx, push=push)
    FN[v](ctx, sc)
    return sc.done()
