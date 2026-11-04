"""Video 02 fix pass, batch C (GOLD rules 95-100): the animated scenes of ch09-ch12 + final (plan: videos/video02/plan/fixpass/PLAN.md, S14-S19)
plus the Kem Kem scientist quote (C12-03, breaks the long AI run of ch12).

Custom scenes (beats are tied to the V02 narration words, wNNN = videos/video02/voice/words.json):
  special_move  S14 C09-17  two gold-framed cards: OUR CROC / special move vs DEINOSUCHUS, which does it bigger
  death_roll    S15 C10-16  our croc death-rolls, Sarcosuchus slides in, "Death roll" = only weapon, balance slams down: 8x heavier
  bite_gauge    S16 C11-16  the S03 bite gauge (v02_anim_a s03_bite geometry) returns + three copies of our bar end to end: at least 3x
  not_noticed   S17 C12-22  underwater cross-section, breath timer, the predator's lock-on sweeps over our croc and fails (no beep)
  hides_eats    S18 C12-27  the generic anim_options "list" + fish shoal, row icons (reeds + eyes, fish, bank footprints + X), rows glow
  cold_enemy    S19 F13     gold line-up of the non-croc predators dims, a snowflake falls, the 14 C thermometer + frost
  kemkem_quote  C12-03      the scientist at the Kem Kem beds, fossil teeth glow, his quote types in word by word
The hero croc is drawn in true colours from templates/lib/anim_assets (PhyloPic CC0, recoloured); rivals are line art or backlit silhouettes."""
import os, random
from .common import fig, esc, rich, GOLD, WARM, SOFT, ITAL, ICONS
from .croc_gfx import SHAPES, shape_svg
from .anim_common import (Scene, BG, BG_NIGHT, INK, kick_html, water_band, waterline, reeds, trees, person, posed, crowd)
from . import anim_options

V = ['special_move', 'death_roll', 'bite_gauge', 'not_noticed', 'hides_eats', 'cold_enemy', 'kemkem_quote']
LONG_OK = tuple(V)   # animation scenes hold 5-12 s (rule 98)
META = dict(name='v02_anim_c', about='Video 02 fix-pass scenes, batch C (S14-S19 + Kem Kem quote). Beats are fixed to the V02 narration words. '
            'hides_eats passes its params to anim_options/list.',
  variants=V,
  params={'ours': 'bite_gauge: our bite (default 16414)', 'value': 'bite_gauge: Purussaurus bite (default 50000, shown with "+")', 'unit': 'bite_gauge: default N',
          'max': 'bite_gauge: value at the full bar (default 52000)', 'row_at': 'bite_gauge: Purussaurus row', 'count_at': 'bite_gauge: count start', 'land_at': 'bite_gauge: land',
          'items': 'hides_eats: as anim_options', 'title': 'hides_eats: as anim_options', 'title_at': 'hides_eats: as anim_options', 'numbered': 'hides_eats: as anim_options',
          'subline': 'hides_eats: italic line at the bottom ("in a river full of *fish*")', 'subline_at': 'hides_eats: when it shows',
          'thicken_at': 'hides_eats: when the fish shoal thickens', 'glow_at': 'hides_eats: when all rows glow',
          'copies_at': 'bite_gauge: times of the three copies of our bar'})

ASSETS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'anim_assets'))
CROC = {'swim': (os.path.join(ASSETS, 'croc_porosus_swim.png'), 675 / 1600), 'gape': (os.path.join(ASSETS, 'croc_porosus_gape.png'), 758 / 1600)}
ICE = '#e6f0ee'
SIL = 'filter:brightness(.16) drop-shadow(0 0 2px rgba(233,220,192,.85)) drop-shadow(0 0 10px rgba(224,162,74,.35))'   # backlit silhouette mode

def recol(svg, fill): return svg.replace('fill="#1a2429"', f'fill="{fill}"')

def croc_img(ctx, gid, kind, cx, cy, w, rot=None, flip=False, style='', op=1.0):
    """True-colour croc image centred at (cx,cy), w px wide. swim: rot 15 levels the body (head right). Returns svg."""
    path, asp = CROC[kind]; src = ctx.asset(path); h = w * asp
    if rot is None: rot = (15 if kind == 'swim' else 0) * (-1 if flip else 1)
    return (f'<g id="{gid}" opacity="{op}"><g transform="translate({cx:.0f},{cy:.0f}) rotate({rot}) scale({-1 if flip else 1},1)">'
            f'<image href="{src}" x="{-w / 2:.0f}" y="{-h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" style="{style}"/></g></g>')

def swim_pts(cx, cy, w):
    """(snout, eye) of a levelled swim croc (head right)."""
    return (cx + .533 * w, cy - .056 * w), (cx + .372 * w, cy - .086 * w)

def J_from(sel, frm, to, t, dur=.4, ease='power3.out'):
    return f"tl.fromTo('{sel}',{{{frm}}},{{{to},duration:{dur},ease:'{ease}',immediateRender:false}},{t:.3f});"

def fish_svg(x, y, s, col=SOFT, op=.5, fid=''):
    return (f'<g {fid} transform="translate({x:.0f},{y:.0f}) scale({s:.2f})" opacity="{op}"><path d="M-20,0 C-10,-10 8,-10 16,0 C8,10 -10,10 -20,0 Z" fill="{col}"/>'
            f'<path d="M16,0 L26,-8 L26,8 Z" fill="{col}"/></g>')

# ====================================================================== S14 special_move
def card_html(p, cid, x, y, w, h, title, sub, body_svg, rows_html):
    return (f'<div id="{cid}" class="an-a" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;opacity:0">'
            f'<svg class="an-ly" style="left:0;top:0;width:{w}px;height:{h}px" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="12" fill="#0b1812" fill-opacity=".9" stroke="{GOLD}" stroke-width="2.5"/>'
            f'<rect x="12" y="12" width="{w - 24}" height="{h - 24}" rx="8" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>{body_svg}</svg>'
            f'<div class="an-a an-k" style="left:0;width:{w}px;text-align:center;top:26px;font-size:36px;letter-spacing:.16em">{esc(title)}</div>'
            f'<div id="{cid}-sub" class="an-a an-it" style="left:0;width:{w}px;text-align:center;top:74px;font-size:36px">{rich(sub)}</div>'
            f'{rows_html}</div>')

def special_move(ctx):
    sc = Scene(ctx, push=(1.0, 1.05, '50% 45%')); p = sc.p; a, b = sc.a, sc.b; T = ctx.t
    sc.dust(34, 21)
    wl = sc.svg(water_band(p, 640, col='#0a1913', line='#cfe0c4', lines=3), drift=-30); sc.glints(wl)
    W, H = 440, 400; AX, BX, Y = 90, 750, 150
    # ---- card A: our croc
    seaA = (f'<g clip-path="url(#{p}-rcA)"><path d="M28,326 q15,-10 30,0 t30,0 t30,0" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="2 9" stroke-linecap="round"/>'
            f'<path d="M118,318 l12,8 l-12,8" fill="none" stroke="{GOLD}" stroke-width="3"/></g>')
    bodyA = (f'<defs><clipPath id="{p}-rcA"><rect id="{p}-rcAr" x="20" y="300" width="0" height="50"/></clipPath></defs>'
             + croc_img(ctx, f'{p}-cA', 'swim', W / 2, 190, 330)
             + f'<line id="{p}-stA" x1="125" y1="98" x2="315" y2="94" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
             + f'<g id="{p}-saA" opacity="0"><circle id="{p}-saAg" cx="60" cy="268" r="26" fill="{GOLD}" opacity=".25"/><g transform="translate(60,268) scale(.30)">{ICONS["salt"]}</g></g>' + seaA)
    rowsA = (f'<div id="{p}-slA" class="an-a an-k" style="left:104px;top:252px;font-size:25px;opacity:0">SALT GLANDS</div>'
             f'<div id="{p}-olA" class="an-a an-k" style="left:150px;top:312px;font-size:25px;opacity:0">OCEAN TRAVEL</div>')
    sc.add_html(card_html(p, f'{p}-A', AX, Y, W, H, 'OUR CROC', '*special move*', bodyA, rowsA))
    sc.J(J_from(f'#{p}-A', 'opacity:0,x:330,rotationY:-95,transformPerspective:900,transformOrigin:"50% 50%"', 'opacity:1,x:330,rotationY:0', a + .05, .45))
    sc.J(f"tl.to('#{p}-A',{{y:-5,duration:1.3,yoyo:true,repeat:{int(sc.D / 1.3)},ease:'sine.inOut'}},{a + .6:.3f});")
    sc.J(f"tl.fromTo('#{p}-cA',{{y:0}},{{y:-6,duration:1.1,yoyo:true,repeat:{int(sc.D / 1.1)},ease:'sine.inOut',immediateRender:false}},{a + .3:.3f});")
    sc.sfx('swoosh', a + .05, .35)
    ts = T('w1763')
    sc.J(J_from(f'#{p}-saA', 'opacity:0,scale:.3,transformOrigin:"50% 50%"', 'opacity:1,scale:1', ts, .35) + J_from(f'#{p}-slA', 'opacity:0,x:-12', 'opacity:1,x:0', ts + .08, .35)
         + f"tl.fromTo('#{p}-saAg',{{opacity:.6,attr:{{r:20}}}},{{opacity:.15,attr:{{r:34}},duration:.9,yoyo:true,repeat:{int((b - ts) / .9)},ease:'sine.inOut',immediateRender:false}},{ts:.3f});")
    sc.sfx('click', ts, .45)
    to = T('w1766')
    sc.J(J_from(f'#{p}-rcAr', 'attr:{width:0}', 'attr:{width:130}', to, .7, 'power1.inOut') + J_from(f'#{p}-olA', 'opacity:0,x:-12', 'opacity:1,x:0', to + .2, .35))
    sc.sfx('swoosh', to, .3)
    # "not special here": strike the subline
    tn = T('w1770')
    pass
    sc.J(J_from(f'#{p}-stA', 'strokeDashoffset:1', 'strokeDashoffset:0', tn, .35, 'power1.inOut') + f"tl.to('#{p}-A-sub',{{opacity:.45,duration:.3}},{tn + .25:.3f});")
    sc.sfx('scratch', tn, .8)
    # ---- card B: Deinosuchus (same icons; its route runs along both coasts of a seaway)
    seaB = (f'<g id="{p}-mapB" opacity="0"><path d="M24,302 C40,318 34,336 46,356 M96,302 C84,320 92,338 82,356" fill="none" stroke="{SOFT}" stroke-width="3" stroke-opacity=".7"/>'
            f'<path d="M50,302 C52,326 50,338 56,356 L72,356 C72,334 76,322 76,302 Z" fill="#cfe0c4" fill-opacity=".12"/></g>'
            f'<g clip-path="url(#{p}-rcB)"><path d="M28,352 C40,330 30,312 20,290 M92,352 C82,332 92,312 100,290" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="2 8" stroke-linecap="round"/></g>')
    bodyB = (f'<defs><clipPath id="{p}-rcB"><rect id="{p}-rcBr" x="0" y="352" width="130" height="0"/></clipPath></defs>'
             + croc_img(ctx, f'{p}-cB', 'gape', W / 2 + 10, 180, 250, style='filter:brightness(.82) saturate(.8)')
             + f'<g id="{p}-saB" opacity="0"><circle cx="60" cy="268" r="26" fill="{GOLD}" opacity=".25"/><g transform="translate(60,268) scale(.30)">{ICONS["salt"]}</g></g>' + seaB)
    rowsB = (f'<div id="{p}-slB" class="an-a an-k" style="left:104px;top:252px;font-size:25px;opacity:0">SALT WATER TOO</div>'
             f'<div id="{p}-olB" class="an-a an-k" style="left:150px;top:312px;font-size:25px;opacity:0">BOTH COASTS</div>')
    sc.add_html(card_html(p, f'{p}-B', BX, Y, W, H, 'DEINOSUCHUS', '*the terror crocodile*', bodyB, rowsB))
    tb = T('w1772') - .3
    sc.J(J_from(f'#{p}-B', 'opacity:0,x:420', 'opacity:1,x:0', tb, .45) + f"tl.to('#{p}-A',{{x:0,duration:.45,ease:'power3.out'}},{tb:.3f});")
    sc.J(f"tl.fromTo('#{p}-cB',{{y:0}},{{y:-5,duration:1.0,yoyo:true,repeat:4,ease:'sine.inOut',immediateRender:false}},{tb + .5:.3f});")
    sc.sfx('swoosh', tb, .4)
    tal = T('w1773')
    sc.J(J_from(f'#{p}-saB', 'opacity:0,scale:.3,transformOrigin:"50% 50%"', 'opacity:1,scale:1', tal, .35) + J_from(f'#{p}-slB', 'opacity:0,x:-12', 'opacity:1,x:0', tal + .08, .35)
         + J_from(f'#{p}-mapB', 'opacity:0', 'opacity:1', tal + .3, .3) + J_from(f'#{p}-rcBr', 'attr:{y:352,height:0}', 'attr:{y:286,height:70}', tal + .45, .6, 'power1.inOut')
         + J_from(f'#{p}-olB', 'opacity:0,x:-12', 'opacity:1,x:0', tal + .6, .35))
    sc.sfx('click', tal, .45)
    # ---- "Bigger.": B scales up, ours drops back
    tg = T('w1776')
    sc.J(f"tl.to('#{p}-B',{{scale:1.24,x:-70,y:10,duration:.4,ease:'back.out(1.6)'}},{tg:.3f});"
         f"tl.to('#{p}-A',{{scale:.78,x:-30,y:70,opacity:.55,duration:.4,ease:'power3.out'}},{tg:.3f});")
    sc.land(tg + .05, BX + W / 2 - 70, Y + H / 2 + 10, r1=300, r2=380)
    return sc.done()

# ====================================================================== S15 death_roll
def death_roll(ctx):
    sc = Scene(ctx, push=(1.0, 1.05, '45% 55%')); p = sc.p; a, b = sc.a, sc.b; T = ctx.t
    SY = 380   # water surface
    r = random.Random(4); far = ''; x = -60
    while x < 1400:
        w = r.uniform(70, 150); h = r.uniform(80, 170); far += f'<ellipse cx="{x:.0f}" cy="{SY - 20 - h * .3:.0f}" rx="{w:.0f}" ry="{h * .7:.0f}" fill="#24493a"/>'; x += w * 1.05
    sc.defs.append(f'<radialGradient id="{p}-sun" cx="78%" cy="18%" r="45%"><stop offset="0" stop-color="#f3dca0" stop-opacity=".22"/><stop offset="1" stop-color="#f3dca0" stop-opacity="0"/></radialGradient>')
    g1 = sc.svg(f'<rect x="-100" y="-100" width="1480" height="920" fill="url(#{p}-sun)"/>' + far + f'<rect x="-100" y="{SY - 30}" width="1500" height="40" fill="#24493a"/>', drift=-18, lid=f'{p}-far')
    sc.svg(reeds(5, 30, SY - 4, SY + 6, '#1a3b2b', 50, 120), drift=-30, sway=1.2, lid=f'{p}-rd')
    wl = sc.svg(water_band(p, SY, col='#0a1913', line='#cfe0c4', lines=5), drift=-40, lid=f'{p}-wat'); sc.glints(wl)
    # our croc + the prey limb (both roll together)
    CX, CY, CW = 290, SY - 12, 450
    (snx, sny), (ex, ey) = swim_pts(CX, CY, CW)
    limb = (f'<path d="M{snx - 30:.0f},{sny + 4:.0f} L{snx + 90:.0f},{sny - 26:.0f} L{snx + 150:.0f},{sny - 18:.0f}" stroke="#5c4a2e" stroke-width="16" stroke-linecap="round" fill="none"/>'
            f'<path d="M{snx + 60:.0f},{sny - 18:.0f} l14,-30" stroke="#5c4a2e" stroke-width="9" stroke-linecap="round"/>')
    sc.svg(f'<g id="{p}-our">{limb}{croc_img(ctx, p + "-oc", "swim", CX, CY, CW)}</g>', lid=f'{p}-ourL')
    # Sarcosuchus: backlit silhouette, ~1.8x the length
    sc.svg(croc_img(ctx, f'{p}-sar', 'gape', 1010, SY - 8, 700, style=SIL), lid=f'{p}-sarL')
    # water in front (lower halves under the surface)
    sc.svg(f'<g id="{p}-wf"><path d="{waterline(SY + 14)} V760 H-200 Z" fill="#0a1913" opacity=".72"/><path d="{waterline(SY + 14)}" fill="none" stroke="#cfe0c4" stroke-width="2" stroke-opacity=".45"/></g>', drift=-55, lid=f'{p}-front')
    # roll arcs + spray
    arcs = ''.join(f'<ellipse id="{p}-arc{i}" cx="{CX + 30}" cy="{CY - 10}" rx="{270 + i * 30}" ry="{70 + i * 16}" fill="none" stroke="{GOLD}" stroke-width="{4 - i}" '
                   f'pathLength="1" stroke-dasharray=".55 .45" stroke-dashoffset="0" opacity="0"/>' for i in range(2))
    spray = ''.join(f'<circle id="{p}-sp{i}" cx="{CX + r.uniform(-160, 200):.0f}" cy="{SY:.0f}" r="{r.uniform(3, 7):.1f}" fill="#dfeee4" opacity="0"/>' for i in range(16))
    sc.svg(arcs + spray, lid=f'{p}-fxL')
    tc = T('w1929')
    sc.J(f"tl.fromTo('#{p}-our',{{scaleY:1,transformOrigin:'50% 50%'}},{{scaleY:-1,duration:.2,ease:'power1.inOut',yoyo:true,repeat:3,immediateRender:false}},{tc:.3f});"
         f"tl.fromTo('#{p}-our',{{y:0}},{{y:-8,duration:.2,yoyo:true,repeat:3,ease:'sine.inOut',immediateRender:false}},{tc:.3f});")
    for i in range(2):
        sc.J(f"tl.fromTo('#{p}-arc{i}',{{opacity:0,strokeDashoffset:0}},{{opacity:1,strokeDashoffset:{-2 if i == 0 else 2},duration:.9,ease:'power1.inOut',immediateRender:false}},{tc + i * .08:.3f});"
             f"tl.to('#{p}-arc{i}',{{opacity:0,duration:.4}},{tc + .9:.3f});")
    for i in range(16):
        dx = r.uniform(-80, 80); dy = -r.uniform(60, 150)
        sc.J(f"tl.fromTo('#{p}-sp{i}',{{opacity:.9,x:0,y:0}},{{opacity:0,x:{dx:.0f},y:{dy:.0f},duration:.7,ease:'power2.out',immediateRender:false}},{tc + r.uniform(0, .7):.3f});")
    sc.sfx('swoosh', tc, .4)
    sc.J(f"bob('#{p}-our',{tc + 1.0:.3f},{max(.5, T('w1945') - tc - 1.0):.3f},-4,.9);")
    ts = T('w1933') - .15
    sc.J(f"tl.set('#{p}-sar',{{x:640}},{a:.3f});tl.to('#{p}-sar',{{x:0,duration:1.0,ease:'power2.out'}},{ts:.3f});"
         f"tl.to('#{p}-sar',{{y:-5,duration:1.2,yoyo:true,repeat:3,ease:'sine.inOut'}},{ts + 1.0:.3f});")
    sc.sfx('swoosh', ts, .35)
    # list row: "Death roll" = only real weapon
    td = T('w1935')
    sc.add_html(f'<div id="{p}-row" class="an-a an-big" style="left:470px;top:96px;font-size:48px;opacity:0">1. Death roll</div>'
                f'<svg class="an-ly" width="1280" height="720" viewBox="0 0 1280 720"><rect id="{p}-box" x="446" y="84" width="300" height="74" rx="6" fill="none" stroke="{GOLD}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>'
                f'<div id="{p}-only" class="an-a an-it" style="left:770px;top:104px;font-size:40px;opacity:0">only real weapon</div>')
    sc.J(J_from(f'#{p}-row', 'opacity:0,x:-24', 'opacity:1,x:0', td, .3) + J_from(f'#{p}-box', 'strokeDashoffset:1', 'strokeDashoffset:0', td + .2, .45, 'power2.out')
         + J_from(f'#{p}-only', 'opacity:0,x:-10', 'opacity:1,x:0', T('w1940'), .4))
    sc.sfx('click', td, .5)
    # ---- balance: not enough against something eight times heavier
    tn = T('w1945') - .1
    for sel in (f'{p}-far', f'{p}-rd', f'{p}-wat', f'{p}-ourL', f'{p}-sarL', f'{p}-front', f'{p}-fxL'):
        sc.J(f"tl.to('#{sel}',{{opacity:0,duration:.35,ease:'power1.in'}},{tn:.3f});")
    sc.J(f"tl.to(['#{p}-row','#{p}-box','#{p}-only'],{{y:-20,opacity:0,duration:.3}},{tn:.3f});")
    PX, PY = 640, 470
    beam = (f'<g id="{p}-beam"><line x1="{PX - 470}" y1="{PY}" x2="{PX + 470}" y2="{PY}" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="{PX - 470}" y1="{PY - 14}" x2="{PX - 470}" y2="{PY + 14}" stroke="{GOLD}" stroke-width="5"/><line x1="{PX + 470}" y1="{PY - 14}" x2="{PX + 470}" y2="{PY + 14}" stroke="{GOLD}" stroke-width="5"/>'
            + croc_img(ctx, f'{p}-bo', 'swim', PX - 300, PY - 44, 300) + croc_img(ctx, f'{p}-bs', 'gape', PX + 250, PY - 116, 520, style=SIL) + '</g>')
    base = (f'<path d="M{PX},{PY + 4} L{PX - 70},{PY + 150} L{PX + 70},{PY + 150} Z" fill="#0b1812" stroke="{GOLD}" stroke-width="4" stroke-linejoin="round"/>'
            f'<circle cx="{PX}" cy="{PY}" r="10" fill="{GOLD}"/><line x1="{PX - 200}" y1="{PY + 150}" x2="{PX + 200}" y2="{PY + 150}" stroke="{SOFT}" stroke-opacity=".5" stroke-width="2"/>')
    sc.svg(f'<g id="{p}-bal" opacity="0">{base}{beam}</g>', lid=f'{p}-balL')
    sc.add_html(f'<div id="{p}-lb1" class="an-a an-k" style="left:{PX - 470}px;width:300px;text-align:center;top:{PY + 40}px;font-size:25px;opacity:0">OUR CROC</div>'
                f'<div id="{p}-lb2" class="an-a an-k" style="left:{PX + 110}px;width:300px;text-align:center;top:{PY + 40}px;font-size:25px;opacity:0">SARCOSUCHUS</div>')
    sc.J(J_from(f'#{p}-bal', 'opacity:0,y:40', 'opacity:1,y:0', tn + .2, .4) + J_from(f'#{p}-lb1', 'opacity:0', 'opacity:1', tn + .4, .3) + J_from(f'#{p}-lb2', 'opacity:0', 'opacity:1', tn + .4, .3)
         + f"tl.fromTo('#{p}-beam',{{rotation:-2,svgOrigin:'{PX} {PY}'}},{{rotation:2,svgOrigin:'{PX} {PY}',duration:.4,yoyo:true,repeat:2,ease:'sine.inOut',immediateRender:false}},{tn + .3:.3f});")
    sc.sfx('swoosh', tn + .2, .3)
    te = T('w1949')
    sc.J(f"tl.to('#{p}-beam',{{rotation:13,svgOrigin:'{PX} {PY}',duration:.25,ease:'power4.in'}},{te - .05:.3f});"
         f"tl.to('#{p}-beam',{{rotation:11.5,svgOrigin:'{PX} {PY}',duration:.18,yoyo:true,repeat:1,ease:'sine.out'}},{te + .2:.3f});"
         f"tl.to('#{p}-bo',{{y:-36,duration:.22,yoyo:true,repeat:1,ease:'power2.out'}},{te + .18:.3f});"
         f"tl.to('#{p}-lb1',{{y:-88,duration:.25,ease:'power4.in'}},{te - .05:.3f});tl.to('#{p}-lb2',{{y:110,duration:.25,ease:'power4.in'}},{te - .05:.3f});")
    sc.add_html(f'<div id="{p}-8x" class="an-a an-big" style="left:700px;top:96px;width:400px;text-align:right;font-size:110px;opacity:0">8&times;<i style="font-size:48px"> heavier</i></div>')
    sc.J(J_from(f'#{p}-8x', 'opacity:0,scale:1.25,transformOrigin:"100% 50%"', 'opacity:1,scale:1', te + .2, .35))
    sc.land(te + .2, 960, 156, r1=180, r2=250)
    return sc.done()

# ====================================================================== S16 bite_gauge (anim_gauge bars + 3 copies of our bar)
def _wrap(mod, ctx, variant, extra):
    old = mod.Scene
    class Ext(Scene):
        def done(self, cls='anim'):
            extra(self); return Scene.done(self, cls)
    mod.Scene = Ext; saved = ctx.variant; ctx.variant = variant
    try: return mod.build(ctx)
    finally: mod.Scene = old; ctx.variant = saved

def bite_gauge(ctx):
    """S16: the S03 bite gauge (v02_anim_a s03_bite geometry: bars x 360-1110 at y 300/470, 24 px caps labels, 76 px hero number, land)
    returns: our croc's bar already full at 16,414 N, Purussaurus counts past it to 50,000+ N, three copies of our bar end to end = at least 3x."""
    try: from .v02_anim_a import croc as a_croc
    except Exception: a_croc = None
    from .anim_common import glyph
    sc = Scene(ctx, push=(1.0, 1.04, '50% 50%')); p = sc.p; a, b = sc.a, sc.b; T = ctx.t
    ours = float(ctx.p('ours', 16414)); val = float(ctx.p('value', 50000)); mx = float(ctx.p('max', 52000)); unit = ctx.p('unit', 'N')
    L0, L1 = 360, 1110; ys = [300, 470]; X = lambda v_: L0 + (L1 - L0) * min(1.0, v_ / mx)
    xo, xp = X(ours), X(val)
    sc.dust(36, 11)
    sc.kicker('Bite *force*', a + .05, y=78, x=110, w=900, align='left', size=28)
    if a_croc: g0, _ = a_croc(ctx, f'{p}-g0', 'gape', 210, ys[0] - 4, 200, flip=True)
    else: g0 = croc_img(ctx, f'{p}-g0', 'gape', 210, ys[0] - 4, 200, flip=True)
    g1, _ = glyph(ctx, f'{p}-g1', {'shape': 'croc'}, 210, ys[1] + 26, 190)
    svg = ''
    for k, (gl, lab, col) in enumerate(((g0, 'OUR CROC', GOLD), (g1, 'PURUSSAURUS', SOFT))):
        y = ys[k]
        svg += (f'<g id="{p}-r{k}" opacity="0">{gl}'
                f'<line x1="{L0}" y1="{y}" x2="{L1}" y2="{y}" stroke="{WARM}" stroke-opacity=".16" stroke-width="16" stroke-linecap="round"/>'
                f'<line id="{p}-b{k}" x1="{L0}" y1="{y}" x2="{L0}" y2="{y}" stroke="{col}" stroke-width="16" stroke-linecap="round"/>'
                f'<circle id="{p}-d{k}" cx="{L0}" cy="{y}" r="9" fill="{col}" opacity="0"/>'
                f'<line id="{p}-gl{k}" x1="{L0}" y1="{y}" x2="{L0 + 50}" y2="{y}" stroke="#fff6dc" stroke-width="6" stroke-linecap="round" opacity="0"/></g>')
        sc.add_html(f'<div id="{p}-l{k}" class="an-a an-k" style="left:60px;width:300px;text-align:center;top:{y + (64 if k == 0 else 52):.0f}px;font-size:24px;opacity:0;{"color:" + GOLD if k == 0 else ""}">{lab}</div>')
    sc.svg(svg)
    tr1 = T(ctx.p('row_at', 'w2093')); tan = T('w2094'); tco = T(ctx.p('count_at', 'w2098')); tla = T(ctx.p('land_at', 'w2101'))
    for k, at in enumerate((a + .1, tr1)):
        sc.J(f"tl.fromTo('#{p}-r{k}',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.35,ease:'power3.out',immediateRender:false}},{at:.3f});"
             f"tl.fromTo('#{p}-l{k}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.4,ease:'power2.out',immediateRender:false}},{at + .1:.3f});")
        sc.sfx('swoosh', at, .3)
    # our bar: already full (fills fast), its number beside it
    sc.J(f"tl.fromTo('#{p}-b0',{{attr:{{x2:{L0}}}}},{{attr:{{x2:{xo:.0f}}},duration:.45,ease:'power2.out',immediateRender:false}},{a + .2:.3f});")
    sc.add_html(f'<div id="{p}-n0" class="an-a an-big" style="left:{xo + 16:.0f}px;top:{ys[0] + 22}px;font-size:44px;opacity:0">{ours:,.0f}<i style="font-size:26px"> {esc(unit)}</i></div>')
    sc.J(J_from(f'#{p}-n0', 'opacity:0,x:-10', 'opacity:1,x:0', a + .45, .35))
    # anticipation on the Purussaurus bar, then the count and the land
    sc.J(f"tl.fromTo('#{p}-d1',{{opacity:.2,attr:{{r:7}}}},{{opacity:1,attr:{{r:13}},duration:.35,yoyo:true,repeat:{max(1, int((tco - tan) / .35))},ease:'sine.inOut',immediateRender:false}},{tan:.3f});"
         f"tl.to('#{p}-d1',{{opacity:0,duration:.1}},{tco:.3f});")
    sc.sfx('tick', tan, .3)
    dur = max(.8, tla - tco)
    sc.J(f"tl.fromTo('#{p}-b1',{{attr:{{x2:{L0}}}}},{{attr:{{x2:{xp:.0f}}},duration:{dur:.2f},ease:'power2.in',immediateRender:false}},{tco:.3f});")
    y = ys[1]
    sc.add_html(f'<div id="{p}-n1" class="an-a an-big" style="left:{L1 - 470}px;top:{y + 44:.0f}px;width:500px;text-align:right;font-size:76px;opacity:0"></div>')
    fmt = f"v=>Math.round(v).toLocaleString('en-US')+(v>={val:g}?'+':'')+'<i style=\\\"font-size:36px\\\"> {esc(unit)}</i>'"
    sc.J(f"tl.set('#{p}-n1',{{opacity:1}},{tco:.3f});counter('#{p}-n1',{tco:.3f},{dur:.2f},0,{val},{fmt},'power2.in');"
         f"tl.fromTo('#{p}-n1',{{scale:1.18,transformOrigin:'100% 50%'}},{{scale:1,duration:.4,ease:'power3.out',immediateRender:false}},{tla:.3f});"
         f"tl.fromTo('#{p}-gl1',{{x:0,opacity:0}},{{x:{xp - L0 - 50:.0f},opacity:.8,duration:1.0,ease:'sine.inOut',immediateRender:false}},{tla + .4:.3f});")
    sc.sfx('ticks_up', tco, .45, dur)
    sc.land(tla, xp, y)
    # at least three times ours: three copies of our bar end to end, gold bracket
    wb = xo - L0; yc = 392; s_ = ''
    for k in range(3):
        x0 = L0 + k * wb
        s_ += f'<line id="{p}-cp{k}" x1="{x0 + 10:.0f}" y1="{yc}" x2="{x0 + wb - 10:.0f}" y2="{yc}" stroke="{GOLD}" stroke-width="12" stroke-linecap="round" opacity="0"/>'
    s_ += f'<path id="{p}-brk" d="M{L0},{yc + 16} v12 H{L0 + 3 * wb:.0f} v-12" fill="none" stroke="{GOLD}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    sc.svg(s_)
    cts = [T(x) for x in (ctx.p('copies_at') or ['w2104', 'w2105', 'w2106'])]
    for k, t in enumerate(cts):
        sc.J(f"tl.fromTo('#{p}-cp{k}',{{opacity:0,y:-30}},{{opacity:.85,y:0,duration:.35,ease:'power3.out',immediateRender:false}},{t:.3f});")
        sc.sfx('click', t, .5)
    bt = cts[-1] + .35
    sc.add_html(f'<div id="{p}-3x" class="an-a an-k" style="left:{L1 - 420}px;width:420px;text-align:right;top:{yc - 84}px;font-size:25px;opacity:0">AT LEAST <span class="an-ki" style="font-size:56px;letter-spacing:0">3&times;</span></div>')
    sc.J(J_from(f'#{p}-brk', 'strokeDashoffset:1', 'strokeDashoffset:0', bt, .4, 'power1.out') + J_from(f'#{p}-3x', 'opacity:0,y:10', 'opacity:1,y:0', bt + .1, .35))
    sc.sfx('marker', bt, .45)
    sc.J(f"tl.to('#{p}-g0-eye',{{scaleY:.1,transformOrigin:'50% 50%',duration:.07,yoyo:true,repeat:1}},{a + 1.2:.3f});")
    return sc.done()

# ====================================================================== S17 not_noticed (reverse lock-on: the lock fails)
def not_noticed(ctx):
    sc = Scene(ctx, bg='linear-gradient(180deg,#1d3b2d 0%,#173126 30%,#0c1a13 36%,#06100b 100%)', push=(1.0, 1.06, '50% 70%')); p = sc.p; a, b = sc.a, sc.b; T = ctx.t
    SY, BED = 250, 610
    r = random.Random(11); far = ''; x = -60
    while x < 1400:
        w = r.uniform(60, 130); h = r.uniform(60, 140); far += f'<ellipse cx="{x:.0f}" cy="{SY - 25 - h * .3:.0f}" rx="{w:.0f}" ry="{h * .7:.0f}" fill="#2a5241"/>'; x += w * 1.1
    sc.defs.append(f'<radialGradient id="{p}-sun" cx="70%" cy="0%" r="60%"><stop offset="0" stop-color="#f3dca0" stop-opacity=".3"/><stop offset="1" stop-color="#f3dca0" stop-opacity="0"/></radialGradient>'
                   f'<linearGradient id="{p}-ray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe6c8" stop-opacity=".16"/><stop offset="1" stop-color="#cfe6c8" stop-opacity="0"/></linearGradient>'
                   f'<linearGradient id="{p}-uw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#123326"/><stop offset="1" stop-color="#050d09"/></linearGradient>')
    sc.svg(f'<rect x="-100" y="-100" width="1480" height="{SY + 100}" fill="url(#{p}-sun)"/>' + far + f'<rect x="-100" y="{SY - 34}" width="1500" height="40" fill="#2a5241"/>', drift=-15)
    # Spinosaurus wading (backlit silhouette), walking left; legs under the surface
    L = 520; hs = SHAPES['spino'][1] * L
    spino = (f'<g id="{p}-spi"><g transform="translate({960:.0f},{SY + 90:.0f}) scale(-1,1) translate({-L / 2:.0f},0)"><g transform="scale({L / 1000:.3f})">'
             + recol(shape_svg("spino", SOFT, 3 / (L / 1000), .55), "#07120d") + '</g></g></g>')
    sc.svg(spino, lid=f'{p}-spL')
    sc.J(f"tl.fromTo('#{p}-spi',{{x:0}},{{x:-300,duration:{sc.D:.3f},ease:'none'}},{a:.3f});bob('#{p}-spi',{a:.3f},{sc.D:.3f},-5,.55);")
    # underwater body of water (in front of the legs, translucent)
    rays = ''.join(f'<path class="{p}-ray" d="M{x0},{SY} L{x0 + 60},{SY} L{x0 + 200},{BED} L{x0 + 90},{BED} Z" fill="url(#{p}-ray)"/>' for x0 in (180, 470, 760, 1010))
    sc.svg(f'<path d="{waterline(SY)} V760 H-200 Z" fill="url(#{p}-uw)" opacity=".86"/><path d="{waterline(SY)}" fill="none" stroke="#cfe0c4" stroke-width="2.5" stroke-opacity=".55"/>' + rays, drift=-20)
    sc.J(f"document.querySelectorAll('.{p}-ray').forEach((r,i)=>tl.fromTo(r,{{opacity:.35}},{{opacity:1,duration:1.6+i*.4,yoyo:true,repeat:Math.ceil({sc.D:.2f}/1.6),ease:'sine.inOut'}},{a:.3f}));")
    sc.specks(30, 12, '#cfe6c8', SY + 20, BED - 10, .8, 2.0)
    # river bed + weeds
    bed = (f'<path d="M-100,{BED} C200,{BED - 12} 500,{BED + 8} 800,{BED - 6} C1000,{BED - 14} 1200,{BED + 4} 1400,{BED} V760 H-100 Z" fill="#0a1510"/>'
           f'<path d="M-100,{BED} C200,{BED - 12} 500,{BED + 8} 800,{BED - 6} C1000,{BED - 14} 1200,{BED + 4} 1400,{BED}" fill="none" stroke="#2f5040" stroke-width="2"/>'
           + ''.join(f'<ellipse cx="{x0}" cy="{BED + 6}" rx="{rx}" ry="{rx * .45:.0f}" fill="#0f1d16" stroke="#2f5040" stroke-width="1.5"/>' for x0, rx in ((140, 40), (980, 55), (1150, 30))))
    sc.svg(bed + reeds(14, 14, BED + 4, BED + 10, '#173527', 70, 170, -40, 300) + reeds(15, 12, BED + 4, BED + 10, '#173527', 60, 160, 900, 1320), drift=-30, sway=2.2)
    # our croc lying on the bottom, dim
    CX, CY, CW = 600, BED - 30, 460
    (snx, sny), (ex, ey) = swim_pts(CX, CY, CW)
    sc.svg(croc_img(ctx, f'{p}-oc', 'swim', CX, CY, CW, rot=8, style='filter:brightness(.72) saturate(.85)')
           + f'<g id="{p}-eye"><circle cx="{ex + 6:.0f}" cy="{ey + 14:.0f}" r="5" fill="#f3dca0" opacity=".9"/></g>', lid=f'{p}-ocL')
    sc.J(f"bob('#{p}-oc',{a:.3f},{sc.D:.3f},-2,1.6);")
    for t in (a + 1.4, T('w2349') + .1):
        sc.J(f"tl.to('#{p}-eye',{{scaleY:.1,transformOrigin:'50% 50%',duration:.08,yoyo:true,repeat:1}},{t:.3f});")
    # bubbles from the nostrils
    bub = ''.join(f'<circle id="{p}-bb{i}" cx="{snx - 30:.0f}" cy="{sny - 4:.0f}" r="{3 + i % 3}" fill="none" stroke="#dfeee4" stroke-width="1.5" opacity="0"/>' for i in range(6))
    sc.svg(bub)
    for i in range(6):
        t = a + .8 + i * .2 + (2.6 if i >= 3 else 0)
        sc.J(f"tl.fromTo('#{p}-bb{i}',{{opacity:.8,y:0,x:0}},{{opacity:0,y:{-(BED - SY) + 60},x:{(-1) ** i * 14},duration:2.2,ease:'power1.out',immediateRender:false}},{t:.3f});")
    # breath timer ring
    RX, RY = CX + 40, CY - 150
    sc.svg(f'<g id="{p}-tm" opacity="0"><circle cx="{RX}" cy="{RY}" r="34" fill="#0b1812" fill-opacity=".7" stroke="{WARM}" stroke-opacity=".2" stroke-width="6"/>'
           f'<circle id="{p}-tmr" cx="{RX}" cy="{RY}" r="34" fill="none" stroke="{GOLD}" stroke-width="6" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 {RX} {RY})"/>'
           f'<line id="{p}-tmh" x1="{RX}" y1="{RY}" x2="{RX}" y2="{RY - 24}" stroke="{WARM}" stroke-width="3" stroke-linecap="round"/></g>')
    sc.add_html(f'<div id="{p}-tml" class="an-a an-k" style="left:{RX + 52}px;top:{RY - 18}px;font-size:25px;opacity:0">HOLDING ITS <span class="an-ki">breath</span></div>')
    tu = T('w2330')
    sc.J(J_from(f'#{p}-tm', 'opacity:0,scale:.5,transformOrigin:"50% 50%"', 'opacity:1,scale:1', tu, .35) + J_from(f'#{p}-tml', 'opacity:0,x:-10', 'opacity:1,x:0', tu + .1, .35)
         + f"tl.fromTo('#{p}-tmr',{{strokeDashoffset:1}},{{strokeDashoffset:.12,duration:{b - tu:.3f},ease:'none',immediateRender:false}},{tu:.3f});"
         f"tl.fromTo('#{p}-tmh',{{rotation:0,svgOrigin:'{RX} {RY}'}},{{rotation:317,svgOrigin:'{RX} {RY}',duration:{b - tu:.3f},ease:'none',immediateRender:false}},{tu:.3f});")
    sc.sfx('tick', tu, .35)
    sc.heartbeat_rings([t for t in (T('w2334'), T('w2334') + 1.6, T('w2334') + 3.2, T('w2334') + 4.8) if t < b - .3], CX, CY - 10, 60, 200, gain=.45)
    # the predator's lock-on: searches, passes over the croc, flickers, can't lock, drifts away (no beep)
    k = f'{p}-lk'; hw, hh = 110, 70
    br = ''.join(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="square"/>' for d in
                 (f'M{-hw},{-hh + 26} V{-hh} H{-hw + 26}', f'M{hw - 26},{-hh} H{hw} V{-hh + 26}', f'M{-hw},{hh - 26} V{hh} H{-hw + 26}', f'M{hw - 26},{hh} H{hw} V{hh - 26}'))
    sc.svg(f'<g id="{k}" opacity="0" transform="translate(0,0)"><g id="{k}i">{br}<circle cx="0" cy="0" r="3" fill="{GOLD}"/></g></g>')
    tw = T('w2340'); tn = T('w2347'); tz = T('w2349')
    path = [(tw, 230, 380), (tw + .55, 430, 330), (tw + 1.1, 920, 420), (tn - .5, 760, 520), (tn, CX + 60, CY - 20)]
    sc.J(f"tl.set('#{k}',{{x:{path[0][1]},y:{path[0][2]}}},{a:.3f});" + J_from(f'#{k}', 'opacity:0', 'opacity:1', tw, .2, 'none')
         + J_from(f'#{k}i', 'scale:1.6', 'scale:1', tw, .32))
    for (t0, x0, y0), (t1, x1, y1) in zip(path, path[1:]):
        sc.J(f"tl.to('#{k}',{{x:{x1},y:{y1},duration:{t1 - t0 - .05:.3f},ease:'power2.inOut'}},{t0:.3f});")
        if t0 == tw: sc.sfx('tick', t0, .3)
    # flicker + failed squeeze over the croc
    sc.J(f"tl.to('#{k}',{{opacity:.25,duration:.06,yoyo:true,repeat:7,ease:'none'}},{tn + .05:.3f});"
         f"tl.to('#{k}i',{{scale:.72,duration:.25,ease:'power2.in'}},{tn + .05:.3f});tl.to('#{k}i',{{scale:1.15,duration:.3,ease:'power2.out'}},{tn + .32:.3f});"
         f"tl.to('#{k}',{{x:'+=10',duration:.05,yoyo:true,repeat:5}},{tn + .05:.3f});")
    sc.J(f"tl.to('#{k}',{{x:1180,y:340,opacity:0,duration:{max(.5, b - tz - .1):.3f},ease:'power1.in'}},{tz:.3f});")
    return sc.done()

# ====================================================================== S18 hides_eats (anim_options list + shoal + icons)
def hides_eats(ctx):
    items = ctx.params.get('items') or []
    num = ctx.params.get('numbered', True)
    texts = [(f'{i + 1}. ' if num else '') + it['text'] for i, it in enumerate(items)]
    size, gap, top0 = 48, 84, 230
    tw = [len(t) * size * .43 + 10 for t in texts]; bw = max(tw) + 50; L = int(640 - bw / 2 + 24)
    IX = L - 24 + bw + 120
    sub = ctx.p('subline', ''); sat = ctx.t(ctx.p('subline_at'), 2.4); tht = ctx.t(ctx.p('thicken_at'), 3.5); glt = ctx.t(ctx.p('glow_at'), ctx.dur - .7)
    ats = [ctx.t(it.get('at'), .9 + i * .45) for i, it in enumerate(items)]
    def extra(sc):
        p = sc.p; a, b = sc.a, sc.b; r = random.Random(3)
        # fish shoal behind the list; thickens on "fish"
        f1 = ''.join(fish_svg(r.uniform(-50, 1350), r.uniform(120, 660), r.uniform(.8, 1.5), SOFT, .14) for _ in range(22))
        f2 = ''.join(fish_svg(r.uniform(-50, 1350), r.uniform(120, 660), r.uniform(.8, 1.6), SOFT, .2) for _ in range(30))
        sc.svg(f'<g id="{p}-sh1">{f1}</g>', drift=-120)
        sc.svg(f'<g id="{p}-sh2" opacity="0">{f2}</g>', drift=-170)
        sc.J(f"bob('#{p}-sh1',{a:.3f},{sc.D:.3f},-8,1.3);" + J_from(f'#{p}-sh2', 'opacity:0', 'opacity:1', tht, .6, 'power1.out') + f"bob('#{p}-sh2',{tht:.3f},{max(.5, b - tht):.3f},6,1.1);")
        sc.sfx('swoosh', tht, .2)
        if sub: sc.line(sub, sat, y=600, size=44)
        # row icons
        ys = [top0 + i * gap + size * .55 for i in range(len(items))]
        ic = []
        ic.append(f'<g transform="translate({IX},{ys[0]:.0f})"><path d="M-50,22 q12,-6 25,0 t25,0 t25,0 t25,0" fill="none" stroke="#cfe0c4" stroke-width="2.5" stroke-opacity=".7"/>'
                  + ''.join(f'<path d="M{x0},24 Q{x0 + 4},-6 {x0 + bd},-34" stroke="#3f7a57" stroke-width="5" fill="none" stroke-linecap="round"/>' for x0, bd in ((-44, -6), (-30, 8), (26, 4), (40, 14)))
                  + f'<g id="{p}-ie"><circle cx="-8" cy="16" r="5" fill="#f3dca0"/><circle cx="10" cy="16" r="5" fill="#f3dca0"/></g></g>')
        ic.append(f'<g transform="translate({IX},{ys[1]:.0f})"><g id="{p}-if"><g transform="scale(.42)">{ICONS["fish"].replace("#fff", SOFT)}</g></g></g>')
        prints = ''.join(f'<g transform="translate({x0},{y0}) rotate(-20)"><path d="M0,0 l-9,-14 M0,0 l0,-17 M0,0 l9,-14" stroke="{SOFT}" stroke-width="3.5" stroke-linecap="round" fill="none"/></g>'
                         for x0, y0 in ((-8, -22), (26, -30), (58, -40)))
        ic.append(f'<g transform="translate({IX - 30},{ys[2]:.0f})"><path d="M-40,26 h40 l30,-26 h60" fill="none" stroke="{SOFT}" stroke-width="3" stroke-opacity=".7"/>'
                  f'<path d="M-40,26 h-30" stroke="#cfe0c4" stroke-width="2.5" stroke-opacity=".7"/>{prints}'
                  f'<path id="{p}-ip" d="M-60,22 C-30,16 -6,8 12,-6" fill="none" stroke="{WARM}" stroke-width="3" stroke-dasharray="3 6" stroke-linecap="round"/>'
                  f'<path id="{p}-ix" d="M-22,-6 l28,28 m0,-28 l-28,28" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></g>')
        sc.svg(''.join(f'<g id="{p}-ic{i}" opacity="0"><g transform="translate({IX},{ys[i]:.0f}) scale(1.45) translate({-IX},{-ys[i]:.0f})">{s}</g></g>' for i, s in enumerate(ic)))
        # before the rows: a 5 m gold measuring bracket, then ambush eyes at a waterline in the middle of it
        t5 = ctx.t('w2375'); tam = ctx.t('w2376'); tout = ats[0] - .35; cy = 380
        mid = (f'<g id="{p}-mm" opacity="0"><path d="M390,{cy - 14} v14 H890 v-14" fill="none" stroke="{GOLD}" stroke-width="3"/></g>'
               f'<g id="{p}-me" opacity="0"><path d="M470,{cy - 46} q20,-8 40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0" fill="none" stroke="#cfe0c4" stroke-width="2.5" stroke-opacity=".7"/>'
               f'<path d="M610,{cy - 50} q30,-22 60,0" fill="#0a1913" stroke="#2f5040" stroke-width="2"/><g id="{p}-mee"><circle cx="626" cy="{cy - 58}" r="7" fill="url(#{p}-eg)"/><circle cx="654" cy="{cy - 58}" r="7" fill="url(#{p}-eg)"/></g></g>')
        sc.svg(mid)
        sc.add_html(f'<div id="{p}-m5" class="an-a an-big" style="left:540px;width:200px;text-align:center;top:{cy + 10}px;font-size:64px;opacity:0">5<i style="font-size:34px"> m</i></div>')
        sc.J(J_from(f'#{p}-mm', 'opacity:0,scaleX:0,transformOrigin:"50% 50%"', 'opacity:1,scaleX:1', t5, .4) + J_from(f'#{p}-m5', 'opacity:0,y:10', 'opacity:1,y:0', t5 + .1, .35)
             + J_from(f'#{p}-me', 'opacity:0,y:16', 'opacity:1,y:0', tam, .35)
             + f"tl.to('#{p}-mee',{{scaleY:.1,transformOrigin:'50% 50%',duration:.07,yoyo:true,repeat:1}},{tam + 1.2:.3f});"
             + f"tl.to(['#{p}-mm','#{p}-m5','#{p}-me'],{{opacity:0,y:-20,duration:.3}},{tout:.3f});")
        sc.sfx('tick', t5, .35)
        for i, t in enumerate(ats):
            sc.J(J_from(f'#{p}-ic{i}', 'opacity:0,x:24', 'opacity:1,x:0', t + .1, .35))
        sc.J(f"tl.to('#{p}-ie',{{scaleY:.1,transformOrigin:'50% 50%',duration:.07,yoyo:true,repeat:1}},{ats[0] + .9:.3f});bob('#{p}-if',{ats[1]:.3f},{max(.5, b - ats[1]):.3f},-5,.5);")
        tx = ats[2] + .45
        sc.J(J_from(f'#{p}-ix', 'strokeDashoffset:1', 'strokeDashoffset:0', tx, .3, 'power1.out')); sc.sfx('click', tx, .5)
        # all rows glow together on "bank."
        sc.J(f"tl.to('[id^=\"{p}-bx\"]',{{opacity:1,strokeDashoffset:0,duration:.25}},{glt:.3f});"
             f"tl.fromTo('[id^=\"{p}-o\"]',{{textShadow:'0 0 0px rgba(201,164,92,0)'}},{{textShadow:'0 0 22px rgba(201,164,92,.95)',duration:.35,yoyo:true,repeat:1,immediateRender:false}},{glt:.3f});")
        sc.sfx('shimmer', glt, .4)
    return _wrap(anim_options, ctx, 'list', extra)

# ====================================================================== S19 cold_enemy
def cold_enemy(ctx):
    sc = Scene(ctx, push=(1.0, 1.06, '40% 55%')); p = sc.p; a, b = sc.a, sc.b; T = ctx.t
    sc.dust(36, 31)
    G = 480
    cast = [('theropod', 210, 'Allosaurus'), ('theropod', 260, 'T. rex'), ('snake', 240, 'Titanoboa'), ('theropod', 250, 'Carcharodontosaurus'), ('spino', 250, 'Spinosaurus')]
    x = 30; s = ''; names = ''
    for i, (sh, w, nm) in enumerate(cast):
        sc_ = w / 1000
        s += (f'<g id="{p}-m{i}" opacity="0"><g transform="translate({x},{G}) scale({sc_:.3f})">{recol(shape_svg(sh, GOLD, 3.2 / sc_, .95), INK)}</g></g>')
        ny = G + 22 if i % 2 == 0 else G + 72
        names += f'<div id="{p}-n{i}" class="an-a an-it" style="left:{x + w / 2 - 210:.0f}px;width:420px;text-align:center;top:{ny}px;font-size:38px;opacity:0">{esc(nm)}</div>'
        x += w + 12
    sc.svg(f'<g id="{p}-row"><line x1="-100" y1="{G}" x2="1800" y2="{G}" stroke="{SOFT}" stroke-opacity=".35" stroke-width="2"/>{s}</g>', lid=f'{p}-rowL')
    sc.add_html(f'<div id="{p}-nm" class="an-a" style="left:0;top:0;width:1800px;height:720px">{names}</div>')
    for i in range(len(cast)):
        t = a + .05 + i * .16
        sc.J(J_from(f'#{p}-m{i}', 'opacity:0,x:160', 'opacity:1,x:0', t, .45) + J_from(f'#{p}-n{i}', 'opacity:0,y:10', 'opacity:1,y:0', t + .15, .35))
        if i == 0: sc.sfx('swoosh', t, .3)
        sc.J(f"tl.to('#{p}-m{i}',{{y:-4,duration:{.9 + i * .1:.2f},yoyo:true,repeat:{int(sc.D / .9)},ease:'sine.inOut'}},{t + .5:.3f});")
    sc.kicker('The *biggest* enemy', a + .3, y=74, x=90, w=700, align='left', size=28)
    th = T('w2498')
    sc.J(f"tl.to(['#{p}-rowL','#{p}-nm'],{{x:-24,duration:{T('w2502') - th + .2:.3f},ease:'power1.inOut'}},{th - .3:.3f});")
    # "wasn't another predator": each one dims
    tw = T('w2499')
    for i in range(len(cast)):
        t = tw + i * .17
        sc.J(f"tl.to('#{p}-m{i}',{{opacity:.16,duration:.2}},{t:.3f});tl.to('#{p}-n{i}',{{opacity:.2,duration:.2}},{t:.3f});")
        sc.sfx('tick', t, .25)
    # one snowflake falls and grows
    ti = T('w2502'); tc = T('w2505')
    sc.svg(f'<g id="{p}-sf" opacity="0"><g transform="translate(980,0)"><g id="{p}-sfi">{ICONS["snowflake"].replace("#fff", ICE)}</g></g></g>')
    sc.J(f"tl.fromTo('#{p}-sf',{{opacity:0,y:-40,scale:.25,transformOrigin:'980px 0px'}},{{opacity:1,y:230,scale:.9,duration:{tc - ti + .3:.3f},ease:'power1.out',immediateRender:false}},{ti:.3f});"
         f"tl.fromTo('#{p}-sfi',{{rotation:0,svgOrigin:'0 0'}},{{rotation:150,svgOrigin:'0 0',duration:{b - ti:.3f},ease:'none',immediateRender:false}},{ti:.3f});")
    sc.sfx('swoosh', ti, .2)
    # the 14 C thermometer slides up; the reading sits below the mark and drops; frost creeps over the frame
    TX, TT, TB = 640, 170, 560; MK = 300
    therm = (f'<g id="{p}-th" opacity="0"><rect x="{TX - 22}" y="{TT}" width="44" height="{TB - TT}" rx="22" fill="#0b1812" stroke="{WARM}" stroke-width="3"/>'
             f'<circle cx="{TX}" cy="{TB + 24}" r="40" fill="#0b1812" stroke="{WARM}" stroke-width="3"/><circle cx="{TX}" cy="{TB + 24}" r="28" fill="{GOLD}"/>'
             f'<line id="{p}-hg" x1="{TX}" y1="{TB + 10}" x2="{TX}" y2="{MK + 60}" stroke="{GOLD}" stroke-width="18" stroke-linecap="round"/>'
             f'<line x1="{TX - 70}" y1="{MK}" x2="{TX + 70}" y2="{MK}" stroke="{GOLD}" stroke-width="4"/></g>')
    sc.svg(therm)
    sc.add_html(f'<div id="{p}-14" class="an-a an-big" style="left:{TX + 90}px;top:{MK - 52}px;font-size:96px;opacity:0">{rich("14°C")}</div>'
                f'<div id="{p}-14s" class="an-a an-it" style="left:{TX + 96}px;top:{MK + 52}px;font-size:40px;opacity:0">what it needs</div>')
    sc.J(J_from(f'#{p}-th', 'opacity:0,y:160', 'opacity:1,y:0', tc - .12, .4) + J_from(f'#{p}-14', 'opacity:0,x:-14', 'opacity:1,x:0', tc + .05, .35)
         + J_from(f'#{p}-14s', 'opacity:0', 'opacity:1', tc + .35, .35)
         + f"tl.to('#{p}-hg',{{attr:{{y2:{TB - 40}}},duration:{max(.6, b - tc - .2):.2f},ease:'power2.out'}},{tc + .2:.3f});")
    sc.land(tc + .05, TX, MK, r1=220, r2=330)
    r = random.Random(9); cr = ''
    for _ in range(26):   # frost crystals from the edges
        side = r.choice('lrtb'); L = r.uniform(60, 170)
        x0, y0, ang = {'l': (0, r.uniform(0, 720), r.uniform(-30, 30)), 'r': (1280, r.uniform(0, 720), 180 + r.uniform(-30, 30)),
                       't': (r.uniform(0, 1280), 0, 90 + r.uniform(-30, 30)), 'b': (r.uniform(0, 1280), 720, -90 + r.uniform(-30, 30))}[side]
        cr += (f'<g transform="translate({x0:.0f},{y0:.0f}) rotate({ang:.0f})" stroke="{ICE}" stroke-width="2" stroke-linecap="round" fill="none">'
               f'<path d="M0,0 H{L:.0f} M{L * .35:.0f},0 l{L * .18:.0f},{-L * .14:.0f} M{L * .35:.0f},0 l{L * .18:.0f},{L * .14:.0f} M{L * .65:.0f},0 l{L * .14:.0f},{-L * .1:.0f} M{L * .65:.0f},0 l{L * .14:.0f},{L * .1:.0f}"/></g>')
    sc.defs.append(f'<radialGradient id="{p}-fg" cx="50%" cy="50%" r="72%"><stop offset=".55" stop-color="{ICE}" stop-opacity="0"/><stop offset=".85" stop-color="{ICE}" stop-opacity=".28"/><stop offset="1" stop-color="{ICE}" stop-opacity=".7"/></radialGradient>')
    sc.top.append(f'<svg id="{p}-fr" class="an-ly" width="1280" height="720" viewBox="0 0 1280 720" style="opacity:0;pointer-events:none"><rect x="0" y="0" width="1280" height="720" fill="url(#{p}-fg)"/><g id="{p}-crs" opacity=".8">{cr}</g></svg>')
    sc.J(f"tl.fromTo('#{p}-fr',{{opacity:0}},{{opacity:1,duration:.9,ease:'power2.out',immediateRender:false}},{tc:.3f});"
         f"tl.fromTo('#{p}-crs',{{scale:.6,transformOrigin:'50% 50%'}},{{scale:1,duration:{max(.6, b - tc):.2f},ease:'power1.out',immediateRender:false}},{tc:.3f});")
    return sc.done()

# ====================================================================== C12-03 kemkem_quote
QUOTE = [('arguably', 'w2187'), ('the', 'w2188'), ('most', 'w2189'), ('|*dangerous*', 'w2190'), ('place', 'w2191'), ('|in', 'w2192'), ('the', 'w2193'), ('history', 'w2194'),
         ('|of', 'w2195'), ('planet', 'w2196'), ('Earth.', 'w2197')]
def kemkem_quote(ctx):
    sc = Scene(ctx, push=(1.0, 1.06, '35% 60%')); p = sc.p; a, b = sc.a, sc.b; T = ctx.t
    G = 540
    sc.defs.append(f'<radialGradient id="{p}-sun" cx="80%" cy="20%" r="55%"><stop offset="0" stop-color="#f3dca0" stop-opacity=".3"/><stop offset=".5" stop-color="#e0a24a" stop-opacity=".08"/><stop offset="1" stop-color="#e0a24a" stop-opacity="0"/></radialGradient>')
    sc.svg(f'<rect x="-100" y="-100" width="1480" height="920" fill="url(#{p}-sun)"/><circle cx="1030" cy="130" r="40" fill="#f3dca0" opacity=".5"/>')
    # far escarpment (lighter, hazy) + near escarpment with strata (darker)
    far = f'<path d="M-100,330 L120,300 L260,318 L420,280 L640,296 L820,262 L1010,290 L1200,270 L1400,286 V{G} H-100 Z" fill="#2c5644"/>'
    far += ''.join(f'<path d="M-100,{y} C300,{y - 8} 800,{y + 6} 1400,{y - 4}" stroke="#3a6a55" stroke-width="2" fill="none" opacity=".6"/>' for y in (340, 372, 404))
    sc.svg(far, drift=-20)
    near = f'<path d="M-100,410 L180,392 L330,404 L520,380 L700,396 L900,372 L1100,392 L1400,380 V{G + 200} H-100 Z" fill="#163628"/>'
    near += ''.join(f'<path d="M-100,{y} C300,{y + 6} 800,{y - 8} 1400,{y + 4}" stroke="#24493a" stroke-width="3" fill="none"/>' for y in (430, 462, 498))
    teeth = [(840, 446, 1.0), (980, 474, .8), (1120, 440, 1.1)]
    for i, (tx, ty, k) in enumerate(teeth):
        near += (f'<g id="{p}-tt{i}" opacity=".35"><circle cx="{tx}" cy="{ty}" r="{30 * k:.0f}" fill="{GOLD}" opacity=".18"/>'
                 f'<path d="M{tx - 10 * k:.0f},{ty + 16 * k:.0f} C{tx - 8 * k:.0f},{ty - 4 * k:.0f} {tx - 2 * k:.0f},{ty - 16 * k:.0f} {tx + 10 * k:.0f},{ty - 22 * k:.0f} C{tx + 8 * k:.0f},{ty - 6 * k:.0f} {tx + 10 * k:.0f},{ty + 6 * k:.0f} {tx + 10 * k:.0f},{ty + 16 * k:.0f} Z" fill="{SOFT}" stroke="{GOLD}" stroke-width="2"/></g>')
    near += f'<line x1="-100" y1="{G}" x2="1400" y2="{G}" stroke="#2f5040" stroke-width="2"/><rect x="-100" y="{G}" width="1500" height="200" fill="#0b1812"/>'
    sc.svg(near, drift=-45)
    sc.kicker('Kem Kem beds · *Morocco*', a + .25, y=50, x=56, w=700, align='left', size=26); sc.sfx('swoosh', a + .25, .25)
    # the scientist (stick figure + lab coat, glasses, clipboard)
    hx, hy, s = 300, G - 84, 1.0
    svg, fx, fy, fs = person(p, 'scientist', hx, hy, s)
    sc.svg(f'<g id="{p}-you">{svg}</g>')
    sc.J(f"pose('{p}',{fx},{fy},{fs},{{aL:20,aR:-20,lL:14,lR:-14}});")
    sc.walk(p, fx, fy, fs, a + .1, .9, dx=160, sel=f'#{p}-you')
    st = T('w2182')
    sc.J(f"tl.to('#{p}-armL',{{rotation:-95,svgOrigin:'{hx} {hy - 78 * s:.0f}',duration:.35,ease:'power3.out'}},{st:.3f});"
         f"tl.to('#{p}-armL',{{rotation:-20,svgOrigin:'{hx} {hy - 78 * s:.0f}',duration:.4,ease:'power2.inOut'}},{T('w2186'):.3f});")
    for i, w in enumerate(('w2182', 'w2183', 'w2184')):
        t = T(w) + .05
        sc.J(f"tl.to('#{p}-tt{i}',{{opacity:1,duration:.3,ease:'power2.out'}},{t:.3f});tl.fromTo('#{p}-tt{i}',{{scale:1.25,transformOrigin:'50% 50%'}},{{scale:1,duration:.4,ease:'power3.out',immediateRender:false}},{t:.3f});")
        sc.sfx('tick', t, .35)
    sc.blink(p, [a + 1.4, T('w2186'), T('w2194')])
    sc.J(f"tl.to('#{p}-you',{{y:-3,duration:.8,yoyo:true,repeat:{int(sc.D / .8)},ease:'sine.inOut'}},{a + 1.1:.3f});")
    # the quote, word by word
    tq = T('w2187')
    QX, QY = 520, 150
    sc.add_html(f'<div id="{p}-qp" class="an-a" style="left:{QX - 40}px;top:{QY - 50}px;width:760px;height:390px;border-radius:14px;background:rgba(4,9,7,.62);'
                f'box-shadow:0 0 60px 20px rgba(4,9,7,.5);opacity:0"></div>'
                f'<div id="{p}-q1" class="an-a an-big" style="left:{QX - 10}px;top:{QY - 60}px;font-size:150px;color:{GOLD};opacity:0">&ldquo;</div>')
    lines = [[]]
    for wd, at in QUOTE:
        if wd.startswith('|'): lines.append([]); wd = wd[1:]
        lines[-1].append((wd, at))
    html = ''; n = 0
    for li, ln in enumerate(lines):
        html += f'<div class="an-a an-big" style="left:{QX + 70}px;top:{QY + 10 + li * 72}px;font-size:58px;font-style:italic">'
        for wd, at in ln:
            html += f'<span id="{p}-w{n}" style="opacity:0;display:inline-block">{rich(wd)}</span> '
            sc.J(J_from(f'#{p}-w{n}', 'opacity:0,y:12', 'opacity:1,y:0', T(at), .3, 'power2.out')); n += 1
        html += '</div>'
    sc.add_html(html + f'<div id="{p}-q2" class="an-a an-big" style="left:{QX + 560}px;top:{QY + 200}px;font-size:150px;color:{GOLD};opacity:0">&rdquo;</div>')
    sc.J(J_from(f'#{p}-qp', 'opacity:0', 'opacity:1', tq - .1, .35, 'power1.out') + J_from(f'#{p}-q1', 'opacity:0,scale:1.4,transformOrigin:"50% 50%"', 'opacity:1,scale:1', tq - .05, .35))
    sc.sfx('click', tq, .45)
    te = T('w2197') + .25
    sc.J(J_from(f'#{p}-q2', 'opacity:0,scale:1.4,transformOrigin:"50% 50%"', 'opacity:1,scale:1', te, .35)); sc.sfx('thud', te, .4)
    return sc.done()

def build(ctx):
    return {'special_move': special_move, 'death_roll': death_roll, 'bite_gauge': bite_gauge, 'not_noticed': not_noticed,
            'hides_eats': hides_eats, 'cold_enemy': cold_enemy, 'kemkem_quote': kemkem_quote}[ctx.variant](ctx)
