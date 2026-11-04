from .common import *
META = dict(name='stick_walk', about='Story gag: the figure walks across a dry crossing between two places (two caps labels, a dashed path, a label on its word, then an italic result word). "channel" = a dry valley between two cliffs (England-France), "bridge" = a flat land bridge (gap T5).',
  variants=['channel', 'bridge'],
  params={'from_label': 'caps label on the left land (default "ENGLAND")', 'to_label': 'caps label on the right land (default "FRANCE")', 'label': 'italic label over the crossing (e.g. "Channel Tunnel")',
          'label_at': 'when the label shows (time spec)', 'result': 'big italic result word at the end (e.g. "walking")', 'result_at': 'when the result lands',
          'walk_at': 'when the figure starts walking (default 0.3 s)', 'walk_end': 'when the figure arrives (default: 0.4 s before the end of the shot)'})
def _ground(v, x):
    if v == 'channel':
        if x < 300: return 400
        if x < 440: return 400 + (x - 300) / 140 * 120
        if x < 840: return 520
        if x < 980: return 520 - (x - 840) / 140 * 120
        return 400
    return 440 - 14 * (1 if 300 < x < 980 else 0) * (1 - abs(x - 640) / 340 if 300 < x < 980 else 0)
def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a; B = ctx.b
    fl = ctx.p('from_label', 'ENGLAND'); tl_ = ctx.p('to_label', 'FRANCE'); lab = ctx.p('label', ''); lat = ctx.t(ctx.p('label_at'), 1.2)
    res = ctx.p('result', ''); rat = ctx.t(ctx.p('result_at'), (B - T) - .9); w0 = ctx.t(ctx.p('walk_at'), .3); w1 = ctx.t(ctx.p('walk_end'), (B - T) - .4)
    s = .95; xs = [i * 20 for i in range(-1, 66)]
    pts = ' L'.join(f'{x},{_ground(v, x):.0f}' for x in xs)
    terr = f'<path d="M{pts} L1320,800 L-20,800 Z" fill="#101a1f" fill-opacity=".9"/><path d="M{pts}" fill="none" stroke="#e9dcc0" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
    gx0, gx1 = 190, 1090
    path = ' L'.join(f'{x:.0f},{_ground(v, x) - 4:.0f}' for x in range(gx0, gx1 + 1, 20))
    cross = f'<path id="{p}-dash" d="M{path}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="3 12" stroke-linecap="round" opacity="0"/>'
    ghost = ''
    if v == 'channel': ghost = f'<path d="{waterline(470, 1500, 7, 110)}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="4 12" stroke-linecap="round" stroke-opacity=".45"/>'
    else: ghost = f'<path d="{waterline(452, 1500, 7, 110)}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="4 12" stroke-linecap="round" stroke-opacity=".45"/>'
    labs = (f'<text x="150" y="{_ground(v, 150) + 70}" text-anchor="middle" class="lblm" style="font-size:26px">{esc(fl)}</text>'
            f'<text x="1130" y="{_ground(v, 1130) + 70}" text-anchor="middle" class="lblm" style="font-size:26px">{esc(tl_)}</text>')
    mid = (f'<g id="{p}-lab" opacity="0"><text x="640" y="278" text-anchor="middle" class="itsv" style="font-size:60px">{rich_svg(lab)}</text>'
           f'<path d="M640,298 v58 M640,356 l-13,-17 M640,356 l13,-17" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" fill="none"/></g>') if lab else ''
    hx = gx0; hy0 = _ground(v, gx0) - 84 * s
    svg = f'<g id="{p}-all">{ghost}{terr}{labs}{cross}{mid}<g id="{p}-figw">{fig(p, hx, hy0, s)}</g></g>'
    html = ctx.shot_div(f'<div id="{p}-kb" class="kb"><svg width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg></div>'
                        + (f'<div id="{p}-r" class="it op0" style="position:absolute;left:0;width:1280px;text-align:center;top:590px;font-size:76px;z-index:40">{rich(res)}</div>' if res else ''), 'stick')
    # walk keyframes along the ground
    n = 30; kf = []
    for i in range(1, n + 1):
        x = gx0 + (gx1 - gx0) * i / n; kf.append(f"{{x:{x - gx0:.0f},y:{_ground(v, x) - _ground(v, gx0):.0f},duration:{(w1 - w0) / n:.3f},ease:'none'}}")
    per = .36
    sy = hy0 - 78 * s; nstep = max(1, int((w1 - w0) / per))
    ctx.js.append(f"""pose('{p}',{hx},{hy0:.1f},{s},{{aL:14,aR:-14,lL:0,lR:0}});
tl.to('#{p}-figw',{{keyframes:[{','.join(kf)}]}},{w0:.3f});
tl.fromTo('#{p}-legL',{{rotation:-24,svgOrigin:'{hx} {hy0:.1f}'}},{{rotation:24,svgOrigin:'{hx} {hy0:.1f}',duration:{per},yoyo:true,repeat:{nstep},ease:'sine.inOut'}},{w0:.3f});
tl.fromTo('#{p}-legR',{{rotation:24,svgOrigin:'{hx} {hy0:.1f}'}},{{rotation:-24,svgOrigin:'{hx} {hy0:.1f}',duration:{per},yoyo:true,repeat:{nstep},ease:'sine.inOut'}},{w0:.3f});
tl.fromTo('#{p}-armL',{{rotation:22,svgOrigin:'{hx} {sy:.1f}'}},{{rotation:-22,svgOrigin:'{hx} {sy:.1f}',duration:{per},yoyo:true,repeat:{nstep},ease:'sine.inOut'}},{w0:.3f});
tl.fromTo('#{p}-armR',{{rotation:-22,svgOrigin:'{hx} {sy:.1f}'}},{{rotation:22,svgOrigin:'{hx} {sy:.1f}',duration:{per},yoyo:true,repeat:{nstep},ease:'sine.inOut'}},{w0:.3f});
fadeIn('#{p}-dash',{w0:.3f},.4);
{f"pop('#{p}-lab',{lat:.3f},.5);" if lab else ''}
{f"tl.fromTo('#{p}-r',{{opacity:0,y:14,scale:.92}},{{opacity:1,y:0,scale:1,duration:.7,ease:'power2.out'}},{rat:.3f});" if res else ''}""")
    ctx.sfx('click', lat, .35)
    if res: ctx.sfx('tok', rat, .5)
    return dict(html=html)
