"""Gold X-ray cutaway (GOLD rule 97 mode; look of templates/tests_anim test6): the body turns into gold line art, one organ / zone glows and
pulses, a scan line sweeps, readout labels with gold leader lines pop in on their times."""
from .common import rich, GOLD, WARM, SOFT
from .anim_common import Scene, person, xray_human, xray_shape, organ_svg, kick_html, img_aspect
from .croc_gfx import SHAPES

LONG_OK = ('bars', 'meter', 'jungle', 'river', 'eyes_room', 'list', 'side', 'human', 'animal')   # animation scenes hold 5-12 s (rule 98)
META = dict(name='anim_xray', about='Gold X-ray mode: "human" = the stick figure "you" switches to a gold X-ray body; "animal" = a line-art animal (croc_gfx shapes: croc, monitor, theropod, fish ...) '
            'or a tinted image as a gold X-ray. One organ glows and pulses (heart beats with the heart sound, lungs breathe), a scan line sweeps, readouts pop in with leader lines.',
  variants=['human', 'animal'],
  params={'organ': 'heart | lungs | brain | gut | gland | dot (default heart)', 'organ_pos': 'animal: [fx, fy] = share of the length from the tail end, share of the height above the belly',
          'organ_size': 'organ radius px (default by variant)', 'organ_label': 'caps label next to the organ (e.g. "SALT GLANDS")', 'organ_at': 'when the organ lights up (default xray_at + 0.5)',
          'xray_at': 'human: when the normal figure turns into the X-ray (default 0.6; 0 = X-ray from the start)', 'who': 'human: the role before the switch (you | scientist | ...)',
          'shape': 'animal: croc_gfx shape (default croc)', 'image': 'animal: optional image path drawn gold-tinted instead of the shape', 'animal_w': 'animal: length px (default 980)',
          'bpm': 'heart beat rate (default 70; beats get the heart sound)', 'heart_sound': 'false = no heart sound', 'scan': 'false = no scan line',
          'readouts': '[{"text":"HEART RATE *40 bpm*","at":T}] labels with leader lines', 'kicker': 'caps title top left, *word* = italic', 'kicker_at': 'default 0.2',
          'line': 'italic line at the bottom', 'line_at': 'when the line shows'})

ANIMAL_ORGANS = {'heart': (.40, .42), 'lungs': (.45, .58), 'brain': (.84, .78), 'gut': (.52, .32), 'gland': (.90, .45), 'dot': (.5, .5)}

def build(ctx):
    v = ctx.variant; p = ctx.id; a = ctx.a; b = ctx.b
    organ = ctx.p('organ', 'heart')
    xat = ctx.t(ctx.p('xray_at'), .6) if v == 'human' else a + .1
    if v == 'human':
        hx, hy, s = 400, 392, 2.0
        body, (ox, oy), orr = xray_human(p, hx, hy, s, organ)
        orr = float(ctx.p('organ_size', orr))
        top, bot = hy - 150 * s, hy + 90 * s; left, right = hx - 90 * s, hx + 90 * s
    else:
        sh = ctx.p('shape', 'croc'); W = float(ctx.p('animal_w', 980)); x0 = (1280 - W) / 2; gy = 520
        img = ctx.p('image')
        if img:
            src = ctx.asset(img); asp = img_aspect(ctx.B.resolve(img)); H = W * asp
            body = (f'<g id="{p}-xb"><image href="{src}" x="{x0:.0f}" y="{gy - H:.0f}" width="{W:.0f}" height="{H:.0f}" opacity=".42" style="filter:sepia(1) saturate(1.6) brightness(1.15) hue-rotate(-8deg)"/></g>')
        else:
            H = SHAPES[sh][1] * W; body = xray_shape(p, sh, x0, gy, W)
        fx, fy = ctx.p('organ_pos') or ANIMAL_ORGANS.get(organ, (.5, .5))
        ox, oy = x0 + fx * W, gy - fy * H; orr = float(ctx.p('organ_size', max(18, H * .16)))
        top, bot, left, right = gy - H - 30, gy + 20, x0 - 20, x0 + W + 20
    sc = Scene(ctx, push=(1.0, 1.07, f'{ox / 12.8:.0f}% {oy / 7.2:.0f}%')); sc.dust(36, 17)
    # ---- before: plain figure, then the switch
    if v == 'human' and xat > a + .25:
        svgf, fxx, fyy, fs = person(f'{p}n', ctx.p('who', 'you'), hx, hy, s)
        sc.svg(f'<g id="{p}-plain">{svgf}</g>')
        sc.J(f"pose('{p}n',{fxx},{fyy},{fs},{{aL:22,aR:-22,lL:12,lR:-12}});tl.fromTo('#{p}-plain',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.4,ease:'power3.out',immediateRender:false}},{a + .05:.3f});"
             f"tl.to('#{p}-plain',{{opacity:0,duration:.35}},{xat:.3f});")
        sc.blink(f'{p}n', [a + .3])
    glow = f'<circle id="{p}-og" cx="{ox:.1f}" cy="{oy:.1f}" r="{orr * 3.2:.1f}" fill="url(#{p}-og)" opacity="0"/>'
    org = f'<g id="{p}-org" opacity="0">{organ_svg(organ, ox, oy, orr)}</g>'
    scan = (f'<g id="{p}-scan" opacity="0"><rect x="{left:.0f}" y="{top - 60:.0f}" width="{right - left:.0f}" height="60" fill="url(#{p}-scg)"/>'
            f'<line x1="{left:.0f}" y1="{top:.0f}" x2="{right:.0f}" y2="{top:.0f}" stroke="{GOLD}" stroke-width="2.5" opacity=".85"/></g>')
    sc.svg(f'<g id="{p}-xr" opacity="0">{body}</g>{glow}{org}' + (scan if ctx.p('scan', True) else ''))
    sc.J(f"tl.fromTo('#{p}-xr',{{opacity:0,y:{12 if v == 'human' else 0}}},{{opacity:1,y:0,duration:.45,ease:'power3.out',immediateRender:false}},{xat:.3f});")
    if xat > a + .25: sc.flash(xat, .14)
    sc.sfx('shimmer', xat, .45); sc.sfx('swoosh', xat, .25)
    if ctx.p('scan', True):
        n = max(1, int((b - xat - .3) / 1.8))
        sc.J(f"tl.fromTo('#{p}-scan',{{opacity:0}},{{opacity:1,duration:.2,immediateRender:false}},{xat + .1:.3f});"
             f"tl.fromTo('#{p}-scan',{{y:0}},{{y:{bot - top:.0f},duration:1.8,yoyo:true,repeat:{n},ease:'sine.inOut',immediateRender:false}},{xat + .1:.3f});")
    # ---- organ lights up and pulses
    oat = ctx.t(ctx.p('organ_at'), xat - a + .5)
    sc.J(f"tl.fromTo('#{p}-org',{{opacity:0,scale:.3,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.4,ease:'back.out(2)',immediateRender:false}},{oat:.3f});"
         f"tl.fromTo('#{p}-og',{{opacity:0}},{{opacity:1,duration:.4,immediateRender:false}},{oat:.3f});")
    sc.sfx('thud', oat, .35)
    if organ == 'heart':
        per = 60.0 / float(ctx.p('bpm', 70)); t = oat + .5; snd = ctx.p('heart_sound', True)
        while t < b - .2:
            sc.J(f"tl.fromTo('#{p}-org',{{scale:1}},{{scale:1.28,transformOrigin:'50% 50%',duration:.1,yoyo:true,repeat:1,ease:'power2.out',immediateRender:false}},{t:.3f});"
                 f"tl.fromTo('#{p}-og',{{opacity:.6}},{{opacity:1,duration:.1,yoyo:true,repeat:1,immediateRender:false}},{t:.3f});")
            if snd: sc.sfx('heart', t, .55)
            t += per
    else:
        per = 1.6 if organ == 'lungs' else 1.2
        n = max(1, int((b - oat - .5) / per))
        sc.J(f"tl.fromTo('#{p}-org',{{scale:1}},{{scale:{1.14 if organ == 'lungs' else 1.08},transformOrigin:'50% 50%',duration:{per},yoyo:true,repeat:{n},ease:'sine.inOut',immediateRender:false}},{oat + .45:.3f});"
             f"tl.fromTo('#{p}-og',{{opacity:.55}},{{opacity:1,duration:{per},yoyo:true,repeat:{n},ease:'sine.inOut',immediateRender:false}},{oat + .45:.3f});")
    # ---- labels
    rl = list(ctx.p('readouts') or [])
    if ctx.p('organ_label'): rl.insert(0, {'text': ctx.p('organ_label'), 'at': ctx.p('organ_at'), '_rel': oat - a + .35})
    lines = ''
    for i, r_ in enumerate(rl):
        at = ctx.t(r_.get('at'), r_.get('_rel', oat - a + .8 + i * .9)) if r_.get('at') is not None else a + r_.get('_rel', oat - a + .8 + i * .9)
        if v == 'human': lx, ly = 720, max(110, oy - 70) + i * 78
        else: lx, ly = min(860, ox + 80), max(80, top - 150) + i * 64
        import re as _re
        tw = len(_re.sub(r'[*]', '', r_['text'])) * 21
        if v == 'animal' and ox > lx + tw: lx = min(lx, ox - tw - 60); e1, e0 = lx + tw + 14, lx + tw + 44
        else: e1, e0 = lx - 12, lx - 40
        lines += (f'<path id="{p}-ld{i}" d="M{ox + (orr * .9 if e1 > ox else -orr * .4):.0f},{oy - (0 if e1 > ox else orr * .4):.0f} L{e0:.0f},{ly + 18:.0f} L{e1:.0f},{ly + 18:.0f}" fill="none" stroke="{GOLD}" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
                  f'<circle id="{p}-lc{i}" cx="{ox:.0f}" cy="{oy:.0f}" r="4" fill="{GOLD}" opacity="0"/>')
        sc.add_html(f'<div id="{p}-r{i}" class="an-a an-k" style="left:{lx:.0f}px;top:{ly:.0f}px;font-size:26px;opacity:0">{kick_html(r_["text"])}</div>')
        sc.J(f"tl.fromTo('#{p}-ld{i}',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.3,ease:'power2.out',immediateRender:false}},{at:.3f});"
             f"tl.fromTo('#{p}-lc{i}',{{opacity:0}},{{opacity:1,duration:.1,immediateRender:false}},{at:.3f});"
             f"tl.fromTo('#{p}-r{i}',{{opacity:0,x:-14}},{{opacity:1,x:0,duration:.35,ease:'power3.out',immediateRender:false}},{at + .2:.3f});")
        sc.sfx('tick', at + .2, .45)
    if lines: sc.svg(lines)
    kick = ctx.p('kicker', '')
    if kick: sc.kicker(kick, ctx.t(ctx.p('kicker_at'), .2), y=56, x=90, w=1100, align='left', size=28)
    ln = ctx.p('line', '')
    if ln: sc.line(ln, ctx.t(ctx.p('line_at'), max(.6, ctx.dur - 1.8)), y=630 if v == 'animal' else 640, size=42, x=None if v == 'animal' else 560, w=700, align='center' if v == 'animal' else 'left')
    return sc.done()
