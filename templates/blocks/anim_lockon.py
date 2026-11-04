"""Lock-on scene (GOLD rules 96-98; look of templates/tests_anim test1 + test4): layered night scene, the stick figure walks in,
eyes open in the dark, gold brackets snap round the target with a held beep, a kicker line ("IT ALREADY *sees* YOU"), heartbeat rings,
then the animal (image or line-art) slides in."""
import random
from .common import GOLD, WARM, SOFT
from .anim_common import (Scene, BG_NIGHT, person, explorer, leaves, fronds, broads, trees, vine, reeds, water_band, waterline, glyph, kick_html)

LONG_OK = ('bars', 'meter', 'jungle', 'river', 'eyes_room', 'list', 'side', 'human', 'animal')   # animation scenes hold 5-12 s (rule 98)
META = dict(name='anim_lockon', about='Lock-on hook scene: "jungle" = night jungle (parallax trees, vines, fronds, light rays, mist, fireflies); '
            '"river" = night river bank (far tree line, reeds, water with glints, eyes on the water surface); "eyes_room" = dark room that fills with blinking eyes. '
            'The figure walks in, eyes appear, gold brackets lock on with a held beep, kicker line, heartbeat rings, optional animal slides in.',
  variants=['jungle', 'river', 'eyes_room'],
  params={'who': 'the target: you | explorer (head torch beam) | scientist | hunter | honey | worker | child (default you)',
          'target_x': 'where the figure stops (x px, default 400 / 330)', 'walk_dur': 'walk-in seconds (default up to the lock; 0 = already standing)',
          'eyes_at': 'when the eyes open (default 1.8)', 'eyes': '[x,y] of the eyes (default by variant)', 'lock_at': 'when the brackets snap (default 3.2)',
          'beep': 'held beep length in s (default 1.0)', 'kicker': 'caps line, *word* = gold italic (default "IT ALREADY *sees* YOU"; "" = none)', 'kicker_at': 'default lock + 0.45',
          'animal': 'optional {"image":"path.png"} | {"shape":"croc"} (+ "w": width px, "y": ground y) sliding in from the right', 'animal_at': 'default lock + 1.8',
          'heart': 'true = heartbeat rings speeding up after the lock (heart sound), or a list of times', 'hud': 'small place/time caption top left (e.g. "SUNDARBANS · 02:14 AM")',
          'distance': 'optional readout {"from":38,"to":12,"unit":"m","label":"DISTANCE","at":T,"dur":1.9}', 'rain': 'true = light rain (jungle)'})

def build(ctx):
    v = ctx.variant; sc = Scene(ctx, bg=BG_NIGHT if v != 'eyes_room' else 'radial-gradient(ellipse at 50% 55%,#12261c 0%,#07100c 55%,#020403 100%)',
                                push=(1.0, 1.08, '42% 58%')); p = sc.p; a = sc.a; b = sc.b
    who = ctx.p('who', 'you'); s = .95
    hx = float(ctx.p('target_x', 400 if v == 'jungle' else (330 if v == 'river' else 640)))
    hy = 520 if v != 'eyes_room' else 470
    lock = ctx.t(ctx.p('lock_at'), 3.2); eat = ctx.t(ctx.p('eyes_at'), 1.8)
    wd = ctx.p('walk_dur'); wd = (max(0.0, lock - a - .6) if v != 'eyes_room' else 0.0) if wd is None else float(wd)
    ex, ey = ctx.p('eyes') or ((990, 400) if v == 'jungle' else ((880, 482) if v == 'river' else (900, 300)))
    sp = 34 if v != 'eyes_room' else 26     # eye spacing
    # ---------------- background layers
    if v == 'jungle':
        sc.svg(f'<defs><radialGradient id="{p}-sky" cx="72%" cy="28%" r="60%"><stop offset="0" stop-color="#e6b062" stop-opacity=".22"/><stop offset=".5" stop-color="#3f6a4c" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
               f'<linearGradient id="{p}-ray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3dca0" stop-opacity=".2"/><stop offset="1" stop-color="#f3dca0" stop-opacity="0"/></linearGradient>'
               f'<linearGradient id="{p}-mist" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9cfb9" stop-opacity="0"/><stop offset=".5" stop-color="#b9cfb9" stop-opacity=".10"/><stop offset="1" stop-color="#b9cfb9" stop-opacity="0"/></linearGradient></defs>'
               f'<rect x="-100" y="-100" width="1480" height="920" fill="url(#{p}-sky)"/>'
               + ''.join(f'<path class="{p}-ray" d="M{x},-20 L{x+70},-20 L{x+260},740 L{x+120},740 Z" fill="url(#{p}-ray)"/>' for x in (700, 840, 1010)))
        sc.J(f"document.querySelectorAll('.{p}-ray').forEach((r,i)=>tl.fromTo(r,{{opacity:.45}},{{opacity:1,duration:2.2+i*.6,yoyo:true,repeat:Math.ceil({sc.D:.2f}/2.2),ease:'sine.inOut'}},{a:.3f}));")
        sc.svg(trees(1, (120, 380, 640, 900, 1180, 1420), 30, 50, 80, 200, '#244a39', '#20432f'), drift=-25)
        sc.svg(f'<rect x="-300" y="380" width="2000" height="170" fill="url(#{p}-mist)"/>', lid=f'{p}-mist1')
        sc.J(f"tl.fromTo('#{p}-mist1',{{x:-200}},{{x:120,duration:{sc.D:.3f},ease:'none'}},{a:.3f});")
        r = random.Random(2)
        sc.svg(trees(2, (40, 560, 1060, 1500), 60, 90, -40, 60, '#153024', '#13291f') + ''.join(vine(x, 0, r.uniform(260, 420), '#1d4030') for x in (220, 470, 760, 980, 1230)), drift=-55, sway=1.4)
    elif v == 'river':
        sc.svg(f'<defs><radialGradient id="{p}-sky" cx="70%" cy="22%" r="55%"><stop offset="0" stop-color="#e6b062" stop-opacity=".26"/><stop offset=".45" stop-color="#3f6a4c" stop-opacity=".14"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
               f'<linearGradient id="{p}-mist" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9cfb9" stop-opacity="0"/><stop offset=".5" stop-color="#b9cfb9" stop-opacity=".12"/><stop offset="1" stop-color="#b9cfb9" stop-opacity="0"/></linearGradient></defs>'
               f'<rect x="-100" y="-100" width="1480" height="920" fill="url(#{p}-sky)"/><circle cx="900" cy="150" r="34" fill="#f3dca0" opacity=".55"/><circle cx="900" cy="150" r="70" fill="#f3dca0" opacity=".08"/>')
        r = random.Random(7); far = ''
        x = -60
        while x < 1400:
            w = r.uniform(60, 140); h = r.uniform(70, 160)
            far += f'<ellipse cx="{x:.0f}" cy="{420 - h * .3:.0f}" rx="{w:.0f}" ry="{h * .7:.0f}" fill="#1f4232"/>'; x += w * 1.1
        sc.svg(far + f'<rect x="-100" y="400" width="1500" height="40" fill="#1f4232"/>', drift=-20)
        sc.svg(reeds(3, 40, 420, 440, '#173527', 40, 110), drift=-35, sway=1.2)
        wl = sc.svg(water_band(p, 440, col='#0a1913', line='#cfe0c4', lines=6) + f'<path d="M560,{441} L760,441 L1300,760 L300,760 Z" fill="#f3dca0" opacity=".05"/>', drift=-50)
        sc.glints(wl)
        sc.svg(f'<rect x="-300" y="400" width="2000" height="120" fill="url(#{p}-mist)"/>', lid=f'{p}-mist1')
        sc.J(f"tl.fromTo('#{p}-mist1',{{x:-200}},{{x:140,duration:{sc.D:.3f},ease:'none'}},{a:.3f});")
    # ---------------- eyes (behind the near layers)
    if v == 'eyes_room':
        r = random.Random(9); pairs = []
        spots = [(ex, ey)] + [(r.uniform(80, 1200), r.uniform(80, 560)) for _ in range(16)]
        spots = [q for q in spots if abs(q[0] - hx) > 160 or abs(q[1] - (hy - 40)) > 190]
        e = ''
        for k, (x, y) in enumerate(spots):
            sz = 1.3 if k == 0 else r.uniform(.75, 1.2)
            e += (f'<g id="{p}-e{k}" opacity="0"><circle cx="{x:.0f}" cy="{y:.0f}" r="{46 * sz:.0f}" fill="url(#{p}-eg)" opacity=".25"/>'
                  f'<g id="{p}-ee{k}"><circle cx="{x - 13 * sz:.0f}" cy="{y:.0f}" r="{7 * sz:.1f}" fill="url(#{p}-eg)"/><circle cx="{x + 13 * sz:.0f}" cy="{y:.0f}" r="{7 * sz:.1f}" fill="url(#{p}-eg)"/></g></g>')
            at = eat + k * .32 + r.uniform(0, .15)
            if at > b - .8: continue
            sc.J(f"tl.fromTo('#{p}-e{k}',{{opacity:0,scale:.4,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.25,ease:'power3.out',immediateRender:false}},{at:.3f});")
            bt = at + r.uniform(.8, 1.8)
            while bt < b - .3:
                sc.J(f"tl.to('#{p}-ee{k}',{{scaleY:.1,transformOrigin:'50% 50%',duration:.07,yoyo:true,repeat:1}},{bt:.3f});"); bt += r.uniform(1.6, 3.0)
            if k < 6: sc.sfx('tick', at, .25)
        sc.svg(e)
        sc.svg(f'<path d="M-50,{hy + 84 * s + 4:.0f} C300,{hy + 78 * s:.0f} 900,{hy + 92 * s:.0f} 1350,{hy + 80 * s:.0f}" stroke="#2f5040" stroke-width="2" fill="none"/>')
    else:
        sc.svg(f'<g id="{p}-eyes" opacity="0">' + (f'<path d="M{ex - 50},{ey + 12} q50,-22 100,0" stroke="#0a1913" stroke-width="12" fill="none"/>'
               f'<ellipse id="{p}-rip" cx="{ex}" cy="{ey + 12}" rx="60" ry="9" fill="none" stroke="#cfe0c4" stroke-width="2" opacity="0"/>' if v == 'river' else '') + f'<circle cx="{ex}" cy="{ey}" r="60" fill="url(#{p}-eg)" opacity=".35"/>'
               f'<g id="{p}-ee"><circle id="{p}-e1" cx="{ex - sp / 2}" cy="{ey}" r="9" fill="url(#{p}-eg)"/><circle id="{p}-e2" cx="{ex + sp / 2}" cy="{ey}" r="9" fill="url(#{p}-eg)"/></g>'
               + '</g>')
        sc.J(f"tl.fromTo('#{p}-eyes',{{opacity:0}},{{opacity:1,duration:.12,immediateRender:false}},{eat:.3f});"
             f"tl.fromTo(['#{p}-e1','#{p}-e2'],{{attr:{{r:2}}}},{{attr:{{r:13}},duration:.25,ease:'power3.out',immediateRender:false}},{eat:.3f});"
             f"tl.to(['#{p}-e1','#{p}-e2'],{{attr:{{r:9}},duration:.6,ease:'sine.out'}},{eat + .25:.3f});")
        bt = eat + 1.1
        while bt < b - .3:
            sc.J(f"tl.to('#{p}-ee',{{scaleY:.1,transformOrigin:'50% 50%',duration:.07,yoyo:true,repeat:1}},{bt:.3f});"); bt += 2.3
        if v == 'river':
            rt = eat
            while rt < b - .5:
                sc.J(f"tl.fromTo('#{p}-rip',{{attr:{{rx:30,ry:5}},opacity:.7}},{{attr:{{rx:110,ry:16}},opacity:0,duration:1.4,ease:'power1.out',immediateRender:false}},{rt:.3f});"); rt += 1.5
        if v == 'jungle':
            sc.svg('<path d="M-60,575 C260,560 760,585 1400,566 L1400,760 L-60,760 Z" fill="#08140f"/><path d="M-60,575 C260,560 760,585 1400,566" stroke="#2f5040" stroke-width="2" fill="none" opacity=".7"/>')
            sc.svg(fronds(4, 18, 560, 640, '#0e2419'), drift=-110, sway=2.2)
        else:
            sc.svg(f'<path d="M-80,{hy + 64} C120,{hy + 52} 420,{hy + 60} 620,{hy + 90} C700,{hy + 110} 760,{hy + 160} 780,760 L-80,760 Z" fill="#0a170f"/>'
                   f'<path d="M-80,{hy + 64} C120,{hy + 52} 420,{hy + 60} 620,{hy + 90} C700,{hy + 110} 760,{hy + 160} 780,760" stroke="#2f5040" stroke-width="2" fill="none"/>', drift=-60)
    # ---------------- the animal (behind the near leaves, in front of the far layers)
    an = ctx.p('animal')
    if an:
        aw = float(an.get('w', 460 if v == 'jungle' else 520)); gy = float(an.get('y', 590 if v == 'jungle' else 498))
        gs, gh = glyph(ctx, f'{p}-an', an, 1280 + aw / 2 + 40, gy, aw, flip=bool(an.get('flip', False)))
        sc.svg(gs)
        if v == 'river':   # water in front of the swimming animal
            sc.svg(f'<path d="{waterline(gy - 30)} V760 H-200 Z" fill="#0a1913" opacity=".82"/><path d="{waterline(gy - 30)}" fill="none" stroke="#cfe0c4" stroke-width="2" stroke-opacity=".35"/>'
                   f'<path d="M-80,{hy + 64} C120,{hy + 52} 420,{hy + 60} 620,{hy + 90} C700,{hy + 110} 760,{hy + 160} 780,760 L-80,760 Z" fill="#0a170f"/>', drift=-60)
        aat = ctx.t(ctx.p('animal_at'), lock - a + 1.8)
        tx = float(an.get('x', 960 if v == 'jungle' else 930))
        sc.J(f"tl.fromTo('#{p}-an',{{x:0}},{{x:{tx - (1280 + aw / 2 + 40):.0f},duration:1.6,ease:'power2.out',immediateRender:false}},{aat:.3f});")
        if v != 'eyes_room': sc.J(f"tl.to('#{p}-eyes',{{opacity:0,duration:.25}},{aat:.3f});")
        sc.J(f"tl.to('#{p}-an',{{y:-4,duration:.9,yoyo:true,repeat:{max(1, int((b - aat - 1.6) / .9))},ease:'sine.inOut'}},{aat + 1.6:.3f});")
        sc.sfx('swoosh', aat, .35); sc.sfx('thud', aat + 1.5, .45); sc.flash(aat + 1.5, .16)
    # ---------------- the figure
    svgf, fx, fy, fs = person(p, who, hx, hy, s)
    beam = ''
    if who == 'explorer':
        lx, ly = hx + 18 * s, hy - 120 * s
        sc.defs.append(f'<linearGradient id="{p}-bm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff3d2" stop-opacity=".5"/><stop offset="1" stop-color="#fff3d2" stop-opacity="0"/></linearGradient>')
        beam = f'<g id="{p}-bmg"><path id="{p}-beam" d="M{lx:.0f},{ly:.0f} L1300,{ly - 150:.0f} L1300,{ly + 170:.0f} Z" fill="url(#{p}-bm)"/></g>'
        sc.J(f"tl.fromTo('#{p}-beam',{{rotation:14,svgOrigin:'{lx:.0f} {ly:.0f}'}},{{rotation:-6,svgOrigin:'{lx:.0f} {ly:.0f}',duration:{max(1.0, eat - a):.2f},ease:'sine.inOut'}},{a + .3:.3f});"
             f"tl.to('#{p}-beam',{{rotation:{-8 if v == 'jungle' else -2},svgOrigin:'{lx:.0f} {ly:.0f}',duration:.5,ease:'power2.out'}},{eat - .2:.3f});")
    sc.svg(f'{beam}<g id="{p}-you">{svgf}</g>')
    sc.J(f"pose('{p}',{fx},{fy},{fs},{{aL:20,aR:-20,lL:14,lR:-14}});")
    if wd > 0:
        sc.walk(p, fx, fy, fs, a + .2, wd, dx=150, sel=f'#{p}-you')
        if beam: sc.J(f"tl.fromTo('#{p}-bmg',{{x:-150}},{{x:0,duration:{wd:.3f},ease:'power1.out'}},{a + .2:.3f});")
    else:
        sc.idle(f'#{p}-you')
    sc.blink(p, [x for x in (a + 1.0, eat + .4, lock + 1.6, lock + 3.6) if x < b - .2])
    if v == 'eyes_room':   # the figure looks round
        sc.J(f"tl.to('#{p}-head',{{x:-5,duration:.5,yoyo:true,repeat:{max(1, int((b - a - 1) / .5))},ease:'sine.inOut'}},{a + .8:.3f});")
    # ---------------- near layers
    if v == 'jungle':
        sc.svg(broads(5, 11, 700, 800, 120, 210, -70, 70, '#06110b') + broads(6, 8, -60, 40, 150, 240, 140, 220, '#06110b'), drift=-190, sway=2.0)
        sc.specks(34, 4, '#e4f29a', 150, 600)
        if ctx.p('rain'):
            r = random.Random(8)
            rn = ''.join(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - 6:.0f}" y2="{y + 26:.0f}" stroke="#cfe0d4" stroke-width="1.2"/>' for x, y in ((r.uniform(0, 1400), r.uniform(-720, 720)) for _ in range(140)))
            sc.svg(f'<g id="{p}-rn" opacity=".22">{rn}</g>')
            sc.J(f"tl.fromTo('#{p}-rn',{{y:0}},{{y:720,duration:1.4,ease:'none',repeat:Math.ceil({sc.D:.2f}/1.4)}},{a:.3f});")
    elif v == 'river':
        sc.svg(reeds(12, 22, 700, 760, '#06110b', 160, 300, -60, 560) + reeds(13, 8, 720, 760, '#06110b', 120, 240, 1050, 1340), drift=-160, sway=2.0)
        sc.specks(26, 6, '#e4f29a', 150, 430)
    else:
        sc.dust(28, 7)
    # ---------------- lock-on + text
    cy = fy - 26 * fs; hh = 118 * fs; hw = 72 * fs
    sc.brackets(lock, fx, cy, hw, hh, beep=float(ctx.p('beep', 1.0)))
    sc.sfx('tick', lock, .5)
    if ctx.p('hud'): sc.hud(ctx.p('hud'), a + .6)
    kick = ctx.p('kicker', 'IT ALREADY *sees* YOU')
    if kick: sc.kicker(kick, ctx.t(ctx.p('kicker_at'), lock - a + .45), y=628, size=30)
    dist = ctx.p('distance')
    if dist:
        dt = ctx.t(dist.get('at'), eat - a + .8); dd = float(dist.get('dur', 1.9))
        sc.add_html(f'<div id="{p}-dist" class="an-a an-k" style="left:{fx + 95:.0f}px;top:{fy - 230:.0f}px;font-size:22px;color:{GOLD};opacity:0">'
                    f'<span id="{p}-dn" class="an-big" style="font-size:44px;letter-spacing:0">{dist.get("from", 38)}</span> <span class="an-ki">{dist.get("unit", "m")}</span><br>{kick_html(dist.get("label", "DISTANCE"))}</div>')
        sc.J(f"tl.fromTo('#{p}-dist',{{opacity:0,y:8}},{{opacity:1,y:0,duration:.35,ease:'power3.out',immediateRender:false}},{dt:.3f});"
             f"counter('#{p}-dn',{dt:.3f},{dd},{dist.get('from', 38)},{dist.get('to', 12)},v=>Math.round(v),'power1.inOut');")
        if lock > dt + dd: sc.J(f"tl.to('#{p}-dist',{{opacity:0,duration:.3}},{lock + .1:.3f});")
        sc.sfx('ticks', dt, .3, dd)
    hb = ctx.p('heart')
    if hb:
        if hb is True:
            ts = []; t = lock + .5; gap = .9
            while t < b - .3: ts.append(t); t += gap; gap = max(.42, gap * .85)
        else: ts = [ctx.t(x) for x in hb]
        sc.heartbeat_rings(ts, fx, fy - 60 * fs)
    return sc.done()
