"""'What would you do?' options list (GOLD rule 98; look of templates/tests_anim test3): title, rows click in one by one, the current row
gets a gold box, finished rows a gold strike-through (scratch), optional verdict line; optional built-in mini scenes per row
(run / climb / hide / swim / stand) with the stick figure, simple props and an optional animal."""
from .common import fig, rich, esc, GOLD, WARM, SOFT
from .anim_common import Scene, glyph, broad, kick_html, waterline

LONG_OK = ('bars', 'meter', 'jungle', 'river', 'eyes_room', 'list', 'side', 'human', 'animal')   # animation scenes hold 5-12 s (rule 98)
META = dict(name='anim_options', about='"What would you do?" spine: title + rows that click in, gold box on the current row, gold strike-through on finished rows, verdict line. '
            '"list" = centred list; a row\'s mini scene replaces the list for its time, then the list comes back. "side" = list on the left, mini scenes play in a gold-framed panel on the right.',
  variants=['list', 'side'],
  params={'title': 'caps title, *word* = gold italic (default "What would you do?")', 'title_at': 'default 0.25',
          'items': '[{"text":"Run","at":T,"box_at":T,"strike_at":T,"scene":{"type":"run|climb|hide|swim|stand","at":T,"dur":3,"label":"TIGERS RUN 60 KM/H","animal":{"image":"tiger.png"} | {"shape":"croc"}}}]',
          'numbered': 'true = "1. Run" (default true)', 'verdict': 'italic line at the end (e.g. "Bad plan.")', 'verdict_at': 'when the verdict shows'})

LEFT = {'list': 400, 'side': 90}

# ------------------------------------------------------------------ mini scenes (drawn in a 1280x720 local box, mapped by (ox, oy, k))
def mini(sc, ctx, q, kind, M, t0, t1, label, animal):
    ox, oy, k = M; X = lambda x: ox + k * x; Y = lambda y: oy + k * y
    W = lambda body: f'<g transform="translate({ox:.1f},{oy:.1f}) scale({k:.4f})">{body}</g>'
    D = t1 - t0; back = ''; front = ''; J = sc.J
    ground = f'<path d="M140,600 C400,594 900,606 1140,598" fill="none" stroke="{SOFT}" stroke-width="3" opacity=".6"/>'
    s = k * 1.0
    def anim_svg(cx, gy, w, flip=False):
        if not animal: return ''
        g, _ = glyph(ctx, f'{q}-an', animal, cx, gy, w, flip=flip or bool(animal.get('flip')))
        return g
    if kind == 'run':
        hx, hy = X(600), Y(516)
        dashes = ''.join(f'<line x1="{x}" y1="618" x2="{x + 34}" y2="618" stroke="{SOFT}" stroke-width="3" stroke-linecap="round" opacity=".45"/>' for x in range(140, 2200, 90))
        speed = ''.join(f'<line id="{q}-sl{i}" x1="{470 - i * 18}" y1="{400 + i * 46}" x2="{390 - i * 18}" y2="{400 + i * 46}" stroke="{WARM}" stroke-width="3" stroke-linecap="round" opacity=".5"/>' for i in range(3))
        back = W(ground + f'<g id="{q}-gd">{dashes}</g>' + speed + anim_svg(-20, 600, float((animal or {}).get('w', 340))))
        figure = f'<g id="{q}-you">{fig(q, hx, hy, s)}</g>'
        J(f"pose('{q}',{hx:.1f},{hy:.1f},{s:.3f},{{aL:60,aR:-60,lL:25,lR:-25}});flail('{q}',{hx:.1f},{hy:.1f},{s:.3f},{t0:.3f},{D:.3f},-40,70,.16);bob('#{q}-you',{t0:.3f},{D:.3f},{-10 * k:.1f},.16);"
          f"tl.fromTo('#{q}-gd',{{x:0}},{{x:-900,duration:{D:.3f},ease:'none'}},{t0:.3f});")
        for i in range(3): J(f"tl.fromTo('#{q}-sl{i}',{{x:0,opacity:.6}},{{x:-60,opacity:0,duration:.4,repeat:{int(D / .4)},ease:'power1.out'}},{t0 + i * .12:.3f});")
        if animal: J(f"tl.fromTo('#{q}-an',{{x:0}},{{x:{float(animal.get('reach', 280)):.0f},duration:{D * .8:.3f},ease:'power1.inOut'}},{t0 + .2:.3f});bob('#{q}-an',{t0:.3f},{D:.3f},-8,.22);")
    elif kind == 'climb':
        tree = (f'<g stroke="{WARM}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="#11241a">'
                f'<path d="M560,600 C566,480 552,360 570,200 L604,200 C596,360 610,480 616,600 Z"/>'
                f'<path d="M584,330 C640,300 700,296 760,270 M580,260 C520,232 470,230 420,206 M590,214 C600,170 586,140 600,110" fill="none"/>'
                f'<path class="sw" data-o="{X(590):.0f} {Y(200):.0f}" d="M380,210 C360,150 420,90 500,100 C540,40 650,40 690,100 C770,90 820,160 790,220 C820,270 760,300 700,280 C640,310 520,300 470,270 C410,280 360,260 380,210 Z" fill="#16301f" stroke-width="5" opacity=".95"/></g>')
        back = W(ground + tree + anim_svg(1500, 600, float((animal or {}).get('w', 340)), flip=False))
        hx, hy = X(588), Y(516); s = k * .62
        figure = f'<g id="{q}-you">{fig(q, hx, hy, s)}</g>'
        rise = (516 - 250) * k
        J(f"pose('{q}',{hx:.1f},{hy:.1f},{s:.3f},{{aL:150,aR:-150,lL:30,lR:-30}});"
          f"tl.fromTo('#{q}-you',{{y:0}},{{y:{-rise:.1f},duration:{min(D * .6, 2.2):.3f},ease:'power1.inOut'}},{t0 + .3:.3f});"
          f"tl.fromTo('#{q}-armL',{{rotation:130,svgOrigin:'{hx:.1f} {hy - 78 * s:.1f}'}},{{rotation:170,svgOrigin:'{hx:.1f} {hy - 78 * s:.1f}',duration:.25,yoyo:true,repeat:{int(min(D * .6, 2.2) / .25)},ease:'sine.inOut',immediateRender:false}},{t0 + .3:.3f});"
          f"tl.fromTo('#{q}-armR',{{rotation:-170,svgOrigin:'{hx:.1f} {hy - 78 * s:.1f}'}},{{rotation:-130,svgOrigin:'{hx:.1f} {hy - 78 * s:.1f}',duration:.25,yoyo:true,repeat:{int(min(D * .6, 2.2) / .25)},ease:'sine.inOut',immediateRender:false}},{t0 + .3:.3f});")
        if animal: J(f"tl.fromTo('#{q}-an',{{x:0}},{{x:{-760:.0f},duration:1.4,ease:'power2.out'}},{t0 + D * .45:.3f});")
    elif kind == 'hide':
        bush = ''.join(broad(x, 612, L, ang, col) for x, L, ang, col in
                       [(470, 200, -50, '#0f2a1d'), (540, 240, -20, '#12301f'), (620, 260, 5, '#0f2a1d'), (700, 240, 25, '#12301f'), (780, 200, 50, '#0f2a1d'), (580, 180, -35, '#163a27'), (690, 190, 35, '#163a27')])
        bush = bush.replace('<g class="sw" data-o="', '<g class="sw" data-o="')
        back = W(ground + anim_svg(1500, 600, float((animal or {}).get('w', 320))))
        hx, hy = X(640), Y(516)
        figure = f'<g id="{q}-you">{fig(q, hx, hy, s)}</g>'
        front = f'<g id="{q}-bush">' + W(bush) + '</g>'
        J(f"pose('{q}',{hx:.1f},{hy:.1f},{s:.3f},{{aL:30,aR:-30,lL:40,lR:-40}});"
          f"tl.fromTo('#{q}-you',{{y:0}},{{y:{55 * k:.1f},duration:.35,ease:'power3.out',immediateRender:false}},{t0 + .5:.3f});"
          f"tl.to('#{q}-legL',{{rotation:70,svgOrigin:'{hx:.1f} {hy:.1f}',duration:.35,ease:'power3.out'}},{t0 + .5:.3f});tl.to('#{q}-legR',{{rotation:-70,svgOrigin:'{hx:.1f} {hy:.1f}',duration:.35,ease:'power3.out'}},{t0 + .5:.3f});"
          f"tl.to('#{q}-you',{{y:{45 * k:.1f},duration:.6,yoyo:true,repeat:{max(1, int((D - 1) / .6))},ease:'sine.inOut'}},{t0 + .9:.3f});"
          f"tl.fromTo('#{q}-bush',{{x:0}},{{x:{4 * k:.1f},duration:.08,yoyo:true,repeat:5,immediateRender:false}},{t0 + .5:.3f});")
        if animal: J(f"tl.fromTo('#{q}-an',{{x:0}},{{x:{-2000:.0f},duration:{max(2.0, D - .6):.3f},ease:'none'}},{t0 + .4:.3f});")
    elif kind == 'swim':
        back = W(f'<path d="{waterline(470, 100, 1180, 8, 120)} V700 H100 Z" fill="#0b1a14"/>' + anim_svg(1500, 500, float((animal or {}).get('w', 420))))
        hx, hy = X(380), Y(560)
        figure = f'<g id="{q}-you">{fig(q, hx, hy, s)}</g>'
        front = W(f'<g id="{q}-wf"><path d="{waterline(472, 100, 1180, 8, 120)} V700 H100 Z" fill="#0b1a14" opacity=".96"/><path d="{waterline(472, 100, 1180, 8, 120)}" fill="none" stroke="#cfe0c4" stroke-width="3" stroke-opacity=".6"/></g>'
                  f'<ellipse id="{q}-rp" cx="380" cy="474" rx="40" ry="8" fill="none" stroke="#cfe0c4" stroke-width="2.5" opacity="0"/>')
        sy = hy - 78 * s
        J(f"pose('{q}',{hx:.1f},{hy:.1f},{s:.3f},{{aL:0,aR:0,lL:10,lR:-10}});"
          f"tl.fromTo('#{q}-armL',{{rotation:-170,svgOrigin:'{hx:.1f} {sy:.1f}'}},{{rotation:190,svgOrigin:'{hx:.1f} {sy:.1f}',duration:.9,repeat:{int(D / .9)},ease:'none',immediateRender:false}},{t0:.3f});"
          f"tl.fromTo('#{q}-armR',{{rotation:10,svgOrigin:'{hx:.1f} {sy:.1f}'}},{{rotation:370,svgOrigin:'{hx:.1f} {sy:.1f}',duration:.9,repeat:{int(D / .9)},ease:'none',immediateRender:false}},{t0:.3f});"
          f"tl.fromTo('#{q}-you',{{x:0}},{{x:{300 * k:.1f},duration:{D:.3f},ease:'none'}},{t0:.3f});bob('#{q}-you',{t0:.3f},{D:.3f},{6 * k:.1f},.45);"
          f"tl.fromTo('#{q}-rp',{{attr:{{rx:30,ry:6}},opacity:.7,x:0}},{{attr:{{rx:90,ry:14}},opacity:0,x:60,duration:.9,repeat:{int(D / .9)},ease:'power1.out',immediateRender:false}},{t0:.3f});"
          f"tl.fromTo('#{q}-wf',{{x:0}},{{x:-40,duration:1.6,yoyo:true,repeat:{int(D / 1.6) + 1},ease:'sine.inOut'}},{t0:.3f});")
        if animal: J(f"tl.fromTo('#{q}-an',{{x:0}},{{x:{-520:.0f},duration:{D * .85:.3f},ease:'power1.out'}},{t0 + .2:.3f});")
    else:   # stand: make yourself big, the animal faces you
        back = W(ground + anim_svg(1500, 600, float((animal or {}).get('w', 360)), flip=False))
        hx, hy = X(430), Y(516)
        figure = f'<g id="{q}-you">{fig(q, hx, hy, s)}</g>'
        sy = hy - 78 * s
        J(f"pose('{q}',{hx:.1f},{hy:.1f},{s:.3f},{{aL:120,aR:-120,lL:28,lR:-28}});"
          f"tl.fromTo('#{q}-armL',{{rotation:110,svgOrigin:'{hx:.1f} {sy:.1f}'}},{{rotation:150,svgOrigin:'{hx:.1f} {sy:.1f}',duration:.3,yoyo:true,repeat:{int(D / .3)},ease:'sine.inOut',immediateRender:false}},{t0 + .3:.3f});"
          f"tl.fromTo('#{q}-armR',{{rotation:-150,svgOrigin:'{hx:.1f} {sy:.1f}'}},{{rotation:-110,svgOrigin:'{hx:.1f} {sy:.1f}',duration:.3,yoyo:true,repeat:{int(D / .3)},ease:'sine.inOut',immediateRender:false}},{t0 + .3:.3f});"
          f"bob('#{q}-you',{t0:.3f},{D:.3f},{-8 * k:.1f},.3);")
        if animal: J(f"tl.fromTo('#{q}-an',{{x:0}},{{x:{-640:.0f},duration:1.3,ease:'power2.out'}},{t0 + .3:.3f});tl.to('#{q}-an',{{x:{-700:.0f},duration:.25,yoyo:true,repeat:3,ease:'power2.inOut'}},{t0 + D * .55:.3f});")
    J(f"pose_blink=1;tl.to('#{q}-eyes',{{scaleY:.1,transformOrigin:'50% 50%',duration:.07,yoyo:true,repeat:1}},{t0 + D * .5:.3f});".replace('pose_blink=1;', ''))
    lab = ''
    if label:
        lab = (f'<div id="{q}-lb" class="an-a an-k" style="left:{X(140):.0f}px;width:{1000 * k:.0f}px;text-align:center;top:{Y(640) if k > .9 else Y(630) + 14:.0f}px;font-size:{26 if k > .8 else 25}px;opacity:0">{kick_html(label)}</div>')
        J(f"tl.fromTo('#{q}-lb',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.45,ease:'power2.out',immediateRender:false}},{t0 + min(1.0, D * .4):.3f});")
        sc.sfx('tick', t0 + min(1.0, D * .4), .35)
    return back + figure + front, lab

def build(ctx):
    v = ctx.variant; sc = Scene(ctx, push=(1.0, 1.04, '50% 50%')); p = sc.p; a = sc.a; b = sc.b
    sc.dust(34, 13)
    items = ctx.p('items') or []
    if not items: raise KeyError('"items" (the options)')
    num = ctx.p('numbered', True)
    title = ctx.p('title', 'What would you do?'); tat = ctx.t(ctx.p('title_at'), .25)
    L = LEFT[v]; size = 48 if v == 'list' else 44; gap = 84 if v == 'list' else 82
    top0 = 230 if v == 'list' else 220
    texts = [(f'{i + 1}. ' if num else '') + it['text'] for i, it in enumerate(items)]
    tw = [len(t) * size * .43 + 10 for t in texts]
    bw = max(tw) + 50 if v == 'list' else min(max(tw) + 50, 520)
    if v == 'list': L = int(640 - bw / 2 + 24)
    rows = ''; svg = ''
    for i, t in enumerate(texts):
        y = top0 + i * gap
        rows += f'<div id="{p}-o{i}" class="an-a an-big" style="left:{L}px;top:{y}px;font-size:{size}px;opacity:0">{rich(t)}</div>'
        svg += (f'<rect id="{p}-bx{i}" x="{L - 24}" y="{y - 12}" width="{bw:.0f}" height="{size + 26}" rx="6" fill="none" stroke="{GOLD}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
                f'<line id="{p}-st{i}" x1="{L - 10}" y1="{y + size * .58:.0f}" x2="{L + tw[i] + 6:.0f}" y2="{y + size * .54:.0f}" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
    tx = None if v == 'list' else 90
    head = (f'<div id="{p}-q" class="an-a an-k" style="left:{0 if v == "list" else 90}px;width:{1280 if v == "list" else 560}px;top:{132 if v == "list" else 120}px;text-align:{"center" if v == "list" else "left"};font-size:28px;opacity:0">{kick_html(title)}</div>'
            f'<div id="{p}-qh" class="an-hair" style="left:{560 if v == "list" else 90}px;width:160px;top:{178 if v == "list" else 166}px;opacity:0"></div>')
    sc.add_html(f'<div id="{p}-head">{head}</div><div id="{p}-lst" class="an-a" style="left:0;top:0;width:1280px;height:720px">{rows}<svg class="an-ly" width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg></div>')
    sc.J(f"tl.fromTo('#{p}-q',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.45,ease:'power2.out',immediateRender:false}},{tat:.3f});"
         f"tl.fromTo('#{p}-qh',{{scaleX:0,opacity:1,transformOrigin:'{'50% 50%' if v == 'list' else '0 50%'}'}},{{scaleX:1,duration:.5,ease:'power2.out',immediateRender:false}},{tat + .15:.3f});")
    sc.sfx('swoosh', tat, .25)
    # ---- events per row
    struck = set(); boxes = []
    for i, it in enumerate(items):
        at = ctx.t(it.get('at'), .9 + i * .45)
        sc.J(f"tl.fromTo('#{p}-o{i}',{{opacity:0,x:-24}},{{opacity:1,x:0,duration:.3,ease:'power3.out',immediateRender:false}},{at:.3f});"); sc.sfx('click', at, .5)
        scn = it.get('scene'); s_at = ctx.t(scn.get('at'), (at - a) + 1.0) if scn else None
        box = it.get('box_at'); st = it.get('strike_at')
        bat = ctx.t(box) if box is not None else (s_at - .6 if scn else (ctx.t(st) - .8 if st is not None else None))
        if bat is not None: boxes.append((bat, i))
        if st is not None:
            sat = ctx.t(st)
            sc.J(f"tl.fromTo('#{p}-st{i}',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.35,ease:'power1.inOut',immediateRender:false}},{sat:.3f});"
                 f"tl.to('#{p}-o{i}',{{opacity:.45,duration:.3}},{sat + .25:.3f});")
            sc.sfx('scratch', sat, .8)
    boxes.sort()
    for j, (bat, i) in enumerate(boxes):
        sc.J(f"tl.fromTo('#{p}-bx{i}',{{strokeDashoffset:1,opacity:1}},{{strokeDashoffset:0,duration:.45,ease:'power2.out',immediateRender:false}},{bat:.3f});"
             f"tl.fromTo('#{p}-o{i}',{{scale:1.06,transformOrigin:'0 50%'}},{{scale:1,duration:.35,ease:'power3.out',immediateRender:false}},{bat:.3f});")
        if j + 1 < len(boxes): sc.J(f"tl.to('#{p}-bx{i}',{{opacity:0,duration:.25}},{boxes[j + 1][0]:.3f});")
        sc.sfx('marker', bat, .35)
    # ---- mini scenes
    panel = ''
    if v == 'side':
        PX, PY, PW, PH = 650, 150, 560, 330; k_ = .55; M = (PX - k_ * 131, PY - k_ * 30, k_)
        sc.defs.append(f'<clipPath id="{p}-clip"><rect x="{PX:.0f}" y="{PY:.0f}" width="{PW:.0f}" height="{PH:.0f}" rx="8"/></clipPath>')
        panel = f'<rect id="{p}-pan" x="{PX:.0f}" y="{PY:.0f}" width="{PW:.0f}" height="{PH:.0f}" rx="8" fill="#0a1611" fill-opacity=".55" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.5" opacity="0"/>'
        first = min((ctx.t(it['scene'].get('at'), .0) for it in items if it.get('scene')), default=None)
        if first is not None:
            sc.J(f"tl.fromTo('#{p}-pan',{{opacity:0,scale:.96,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.4,ease:'power3.out',immediateRender:false}},{first - .3:.3f});")
    else:
        M = (0, 0, 1.0)
    scenes = ''; labs = ''
    sl = [(i, it['scene']) for i, it in enumerate(items) if it.get('scene')]
    for n_, (i, scn) in enumerate(sl):
        t0 = ctx.t(scn.get('at'), 1.0 + i)
        nxt = ctx.t(sl[n_ + 1][1].get('at'), 99) if n_ + 1 < len(sl) else b
        t1 = min(t0 + float(scn.get('dur', 3.0)), nxt - .05) if (scn.get('dur') or v == 'list') else nxt - (.05 if n_ + 1 < len(sl) else -.4)
        q = f'{p}-m{i}'
        body, lab = mini(sc, ctx, q, scn.get('type', 'run'), M, t0, t1, scn.get('label', ''), scn.get('animal'))
        scenes += f'<g id="{q}" opacity="0">{body}</g>'; labs += lab
        sc.J(f"tl.fromTo('#{q}',{{opacity:0,y:{14 if v == 'side' else 20}}},{{opacity:1,y:0,duration:.35,ease:'power3.out',immediateRender:false}},{t0:.3f});"
             f"tl.to('#{q}',{{opacity:0,duration:.3}},{t1 - .3:.3f});")
        if lab: sc.J(f"tl.to('#{q}-lb',{{opacity:0,duration:.3}},{t1 - .3:.3f});")
        sc.sfx('swoosh', t0, .35)
        if v == 'list':
            sc.J(f"tl.fromTo('#{p}-lst',{{opacity:1,x:0}},{{opacity:0,x:-60,duration:.35,ease:'power2.in',immediateRender:false}},{t0 - .25:.3f});"
                 f"tl.fromTo('#{p}-head',{{opacity:1}},{{opacity:0,duration:.3,immediateRender:false}},{t0 - .25:.3f});"
                 f"tl.fromTo('#{p}-lst',{{opacity:0,x:-60}},{{opacity:1,x:0,duration:.35,ease:'power2.out',immediateRender:false}},{t1:.3f});"
                 f"tl.fromTo('#{p}-head',{{opacity:0}},{{opacity:1,duration:.3,immediateRender:false}},{t1:.3f});")
            sc.sfx('swoosh', t1, .25)
    clip = f' clip-path="url(#{p}-clip)"' if v == 'side' else ''
    sc.svg(f'{panel}<g{clip}>{scenes}</g>', sway=1.8)
    sc.add_html(labs)
    ver = ctx.p('verdict', '')
    if ver:
        vt = ctx.t(ctx.p('verdict_at'), max(.5, ctx.dur - 1.6))
        if v == 'list': sc.line(ver, vt, y=top0 + len(items) * gap + 40, size=46)
        else: sc.line(ver, vt, y=top0 + len(items) * gap + 30, size=44, x=90, w=520, align='left')
        sc.sfx('thud', vt, .4)
    return sc.done()
