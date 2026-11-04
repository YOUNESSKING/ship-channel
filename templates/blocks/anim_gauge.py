"""Animated count-up gauge (GOLD rule 98, look of templates/tests_anim test2): anticipation, a ~1.4 s count, lands with flash + expanding
gold ring + deep hit, rings keep pulsing softly; labels, unit, optional gold marker circle and italic comparison line."""
from .common import esc, rich, GOLD, WARM, SOFT
from .anim_common import Scene, glyph, kick_html

LONG_OK = ('bars', 'meter', 'jungle', 'river', 'eyes_room', 'list', 'side', 'human', 'animal')   # animation scenes hold 5-12 s (rule 98)
META = dict(name='anim_gauge', about='Count-up gauge on green ink. "bars" = 2-4 horizontal bars (e.g. you vs the animal), each with an icon / line-art / image and a label; '
            'the hero bar (last, or "hero":true) counts ~1.4 s and lands with flash + gold ring + deep hit. "meter" = one tall meter with reference marks '
            '(e.g. conversation / jet engine) that fills to the value and lands the same way.',
  variants=['bars', 'meter'],
  params={'kicker': 'small caps title top left, *word* = gold italic (e.g. "Bite force")', 'kicker_at': 'when the kicker shows (default 0.2)',
          'unit': 'italic unit after every number (e.g. "psi")', 'decimals': 'decimals of the numbers (default 0)', 'max': 'value at the full bar / meter top (default: largest value)',
          'items': 'bars: [{"label":"YOU","value":160,"glyph":{"person":"you"} | {"shape":"croc"} | {"icon":"hand"} | {"image":"path.png"},"at":T,"count_at":T,"dur":1.4,"hero":true}]',
          'value': 'meter: the value counted to', 'label': 'meter: caps label under the big number', 'glyph': 'meter: optional glyph next to the big number (as items)',
          'count_at': 'meter: when the count starts (default 1.6)', 'dur': 'meter: count length (default 1.4)',
          'marks': 'meter: reference marks [{"value":60,"label":"CONVERSATION","at":T}]',
          'note': 'italic comparison line at the bottom (e.g. "more than six times yours")', 'note_at': 'when the note shows (default land + 1.3)',
          'circle': 'true = a gold marker circle is drawn round the hero number after the land', 'circle_at': 'when the circle draws (default land + 0.8)'})

def _fmt(unit, d, size):
    u = f"+'<i style=\"font-size:{size}px\"> {esc(unit)}</i>'" if unit else ''
    return f"v=>(v).toLocaleString('en-US',{{minimumFractionDigits:{d},maximumFractionDigits:{d}}}){u}"

def build(ctx):
    v = ctx.variant; sc = Scene(ctx, push=(1.0, 1.04, '50% 50%')); p = sc.p; a = sc.a
    sc.dust(36, 11)
    kick = ctx.p('kicker', ''); unit = ctx.p('unit', ''); d = int(ctx.p('decimals', 0))
    if kick:
        kt = ctx.t(ctx.p('kicker_at'), .2)
        sc.kicker(kick, kt, y=78, x=110, w=900, align='left', size=28)
    land = None; hero_box = None
    if v == 'bars':
        items = ctx.p('items') or []
        if len(items) < 1: raise KeyError('"items" (the bars)')
        n = len(items); L0, L1 = 360, 1110
        hero = next((k for k, it in enumerate(items) if it.get('hero')), n - 1)
        mx = float(ctx.p('max') or max(float(it['value']) for it in items))
        ys = [300, 470] if n == 2 else [250 + k * (330 / max(1, n - 1)) for k in range(n)] if n > 1 else [380]
        svg = ''
        for k, it in enumerate(items):
            y = ys[k]; at = ctx.t(it.get('at'), .7 + k * 1.6); hk = k == hero
            cat = ctx.t(it.get('count_at'), (at - a) + (.6 if not hk else .9)); dur = float(it.get('dur', 1.4 if hk else .7))
            val = float(it['value']); x1 = L0 + (L1 - L0) * min(1.0, val / mx)
            col = GOLD if hk else SOFT
            g = it.get('glyph')
            gsv = ''; lab_y = y + 38
            if g:
                gw = float(it.get('glyph_w', 150 if not (isinstance(g, dict) and g.get('person')) else 130))
                _, gh = glyph(ctx, f'{p}-g{k}', g, 210, 0, gw)
                gb = y + 28 if gh <= 56 else y + gh / 2 - 20
                gsv, _ = glyph(ctx, f'{p}-g{k}', g, 210, gb, gw); lab_y = max(y + 38, gb + 8)
            svg += (f'<g id="{p}-r{k}" opacity="0">{gsv}'
                    f'<line x1="{L0}" y1="{y}" x2="{L1}" y2="{y}" stroke="{WARM}" stroke-opacity=".16" stroke-width="16" stroke-linecap="round"/>'
                    f'<line id="{p}-b{k}" x1="{L0}" y1="{y}" x2="{L0}" y2="{y}" stroke="{col}" stroke-width="16" stroke-linecap="round"/>'
                    f'<circle id="{p}-d{k}" cx="{L0}" cy="{y}" r="9" fill="{col}" opacity="0"/>'
                    f'<line id="{p}-gl{k}" x1="{L0}" y1="{y}" x2="{L0 + 50}" y2="{y}" stroke="#fff6dc" stroke-width="6" stroke-linecap="round" opacity="0"/></g>')
            sc.add_html(f'<div id="{p}-l{k}" class="an-a an-k" style="left:60px;width:300px;text-align:center;top:{lab_y:.0f}px;font-size:26px;opacity:0">{kick_html(it.get("label", ""))}</div>')
            sc.J(f"tl.fromTo('#{p}-r{k}',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.35,ease:'power3.out',immediateRender:false}},{at:.3f});"
                 f"tl.fromTo('#{p}-l{k}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.4,ease:'power2.out',immediateRender:false}},{at + .1:.3f});")
            sc.sfx('swoosh', at, .3)
            # anticipation: the empty bar's start dot breathes until the count
            if cat - at > .5:
                sc.J(f"tl.fromTo('#{p}-d{k}',{{opacity:.2,attr:{{r:7}}}},{{opacity:1,attr:{{r:12}},duration:.35,yoyo:true,repeat:{max(1, int((cat - at - .3) / .35))},ease:'sine.inOut',immediateRender:false}},{at + .3:.3f});"
                     f"tl.to('#{p}-d{k}',{{opacity:0,duration:.1}},{cat:.3f});")
            ease = "'power2.in'" if hk else "'power2.out'"
            sc.J(f"tl.fromTo('#{p}-b{k}',{{attr:{{x2:{L0}}}}},{{attr:{{x2:{x1:.0f}}},duration:{dur},ease:{ease},immediateRender:false}},{cat:.3f});")
            if hk:
                sc.add_html(f'<div id="{p}-n{k}" class="an-a an-big" style="left:{L1 - 470}px;top:{y + 44:.0f}px;width:500px;text-align:right;font-size:76px;opacity:0"></div>')
                sc.J(f"tl.set('#{p}-n{k}',{{opacity:1}},{cat:.3f});counter('#{p}-n{k}',{cat:.3f},{dur},0,{val},{_fmt(unit, d, 36)},'power2.in');"
                     f"tl.fromTo('#{p}-n{k}',{{scale:1.18,transformOrigin:'100% 50%'}},{{scale:1,duration:.4,ease:'power3.out',immediateRender:false}},{cat + dur:.3f});")
                sc.sfx('ticks_up', cat, .45, dur)
                land = (cat + dur, x1, y); wn = len(f'{val:,.{d}f}') * 76 * .5 + (len(unit) * 36 * .42 + 14 if unit else 0); hero_box = (L1 + 30 - wn / 2, y + 84, wn)
                n_g = max(1, int((ctx.b - cat - dur - 1) / 2.2))
                sc.J(f"tl.fromTo('#{p}-gl{k}',{{x:0,opacity:0}},{{x:{x1 - L0 - 50:.0f},opacity:.8,duration:1.1,ease:'sine.inOut',repeat:{n_g},repeatDelay:1.1,immediateRender:false}},{cat + dur + .6:.3f});")
            else:
                sc.add_html(f'<div id="{p}-n{k}" class="an-a an-big" style="left:{L0}px;top:{y + 22:.0f}px;font-size:44px;opacity:0"></div>')
                sc.J(f"tl.set('#{p}-n{k}',{{opacity:1,x:0}},{cat:.3f});tl.to('#{p}-n{k}',{{x:{x1 - L0 + 10:.0f},duration:{dur},ease:'power2.out'}},{cat:.3f});"
                     f"counter('#{p}-n{k}',{cat:.3f},{dur},0,{val},{_fmt(unit, d, 26)},'power2.out');"
                     f"tl.fromTo('#{p}-b{k}',{{opacity:1}},{{opacity:.75,duration:.3,immediateRender:false}},{cat + dur + .2:.3f});")
                sc.sfx('ticks', cat, .35, dur); sc.sfx('thud', cat + dur, .35)
        sc.svg(svg)
    else:   # meter
        val = float(ctx.p('value', 100)); mx = float(ctx.p('max') or val * 1.15); marks = ctx.p('marks') or []
        X, Y0, Y1 = 330, 610, 150
        Y = lambda q: Y0 - (Y0 - Y1) * min(1.0, float(q) / mx)
        cat = ctx.t(ctx.p('count_at'), 1.6); dur = float(ctx.p('dur', 1.4))
        svg = f'<g id="{p}-m" opacity="0"><rect x="{X - 26}" y="{Y1 - 10}" width="52" height="{Y0 - Y1 + 20}" rx="26" fill="{WARM}" fill-opacity=".07" stroke="{WARM}" stroke-opacity=".3" stroke-width="2"/>'
        step = mx / 5
        for q in range(6):
            yy = Y(q * step)
            svg += f'<line x1="{X - 46}" y1="{yy:.0f}" x2="{X - 32}" y2="{yy:.0f}" stroke="{WARM}" stroke-opacity=".5" stroke-width="2"/>'
            sc.add_html(f'<div class="an-a an-k" style="left:{X - 260}px;width:200px;text-align:right;top:{yy - 16:.0f}px;font-size:24px;letter-spacing:.08em;opacity:.7">{q * step:,.0f}</div>')
        svg += f'<line id="{p}-fill" x1="{X}" y1="{Y0}" x2="{X}" y2="{Y0}" stroke="{GOLD}" stroke-width="30" stroke-linecap="round"/>'
        svg += f'<circle id="{p}-dot" cx="{X}" cy="{Y0}" r="10" fill="{GOLD}"/></g>'
        sc.J(f"tl.fromTo('#{p}-m',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:'power3.out',immediateRender:false}},{a + .3:.3f});"
             f"tl.fromTo('#{p}-dot',{{attr:{{r:8}}}},{{attr:{{r:14}},duration:.35,yoyo:true,repeat:{max(1, int((cat - a - .7) / .35))},ease:'sine.inOut',immediateRender:false}},{a + .7:.3f});")
        sc.sfx('swoosh', a + .3, .3)
        for k, m in enumerate(marks):
            yy = Y(m['value']); at = ctx.t(m.get('at'), .7 + k * .45)
            svg += f'<g id="{p}-mk{k}" opacity="0"><line x1="{X + 34}" y1="{yy:.0f}" x2="{X + 120}" y2="{yy:.0f}" stroke="{SOFT}" stroke-width="2" stroke-dasharray="6 6"/></g>'
            sc.add_html(f'<div id="{p}-mt{k}" class="an-a an-k" style="left:{X + 135}px;top:{yy - 17:.0f}px;font-size:25px;opacity:0">{kick_html(m.get("label", ""))} '
                        f'<span class="an-ki" style="font-size:34px">{m["value"]:,}</span></div>')
            sc.J(f"tl.fromTo('#{p}-mk{k}',{{opacity:0}},{{opacity:1,duration:.3,immediateRender:false}},{at:.3f});tl.fromTo('#{p}-mt{k}',{{opacity:0,x:-16}},{{opacity:1,x:0,duration:.35,ease:'power3.out',immediateRender:false}},{at:.3f});")
            sc.sfx('click', at, .4)
        yv = Y(val)
        sc.J(f"tl.fromTo('#{p}-fill',{{attr:{{y2:{Y0}}}}},{{attr:{{y2:{yv:.0f}}},duration:{dur},ease:'power2.in',immediateRender:false}},{cat:.3f});"
             f"tl.fromTo('#{p}-dot',{{attr:{{cy:{Y0}}}}},{{attr:{{cy:{yv:.0f}}},duration:{dur},ease:'power2.in',immediateRender:false}},{cat:.3f});")
        sc.add_html(f'<div id="{p}-big" class="an-a an-big" style="left:800px;width:440px;top:170px;font-size:96px;opacity:0"></div>')
        lab = ctx.p('label', '')
        if lab: sc.add_html(f'<div id="{p}-lab" class="an-a an-k" style="left:804px;top:282px;font-size:28px;opacity:0">{kick_html(lab)}</div>')
        sc.J(f"tl.set('#{p}-big',{{opacity:1}},{cat:.3f});counter('#{p}-big',{cat:.3f},{dur},0,{val},{_fmt(unit, d, 46)},'power2.in');"
             f"tl.fromTo('#{p}-big',{{scale:1.18,transformOrigin:'0% 50%'}},{{scale:1,duration:.4,ease:'power3.out',immediateRender:false}},{cat + dur:.3f});")
        if lab: sc.J(f"tl.fromTo('#{p}-lab',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.4,ease:'power2.out',immediateRender:false}},{cat + dur + .2:.3f});")
        g = ctx.p('glyph')
        if g:
            gs, gh = glyph(ctx, f'{p}-gm', g, 960, 560, 300)
            sc.svg(gs); sc.J(f"tl.fromTo('#{p}-gm',{{opacity:0,x:40}},{{opacity:1,x:0,duration:.4,ease:'power3.out',immediateRender:false}},{cat + dur + .3:.3f});")
        sc.sfx('ticks_up', cat, .45, dur)
        svg_all = svg
        sc.svg(svg_all)
        wn = len(f'{val:,.{d}f}') * 96 * .5 + (len(unit) * 46 * .42 + 14 if unit else 0); land = (cat + dur, X, yv); hero_box = (800 + wn / 2, 218, wn)
    lt, lx, ly = land
    sc.land(lt, lx, ly)
    if ctx.p('circle'):
        cx, cy, hw = hero_box
        ct = ctx.t(ctx.p('circle_at'), lt - a + .8)
        rx, ry = hw / 2 + 34, 58
        sc.svg(f'<path id="{p}-circ" d="M{cx + rx * .3:.0f},{cy - ry:.0f} C{cx + rx * 1.05:.0f},{cy - ry * .95:.0f} {cx + rx * 1.08:.0f},{cy + ry * .9:.0f} {cx:.0f},{cy + ry:.0f} '
               f'C{cx - rx * 1.05:.0f},{cy + ry * 1.0:.0f} {cx - rx * 1.06:.0f},{cy - ry * .9:.0f} {cx + rx * .05:.0f},{cy - ry * 1.04:.0f}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
        sc.J(f"tl.fromTo('#{p}-circ',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.4,ease:'power1.out',immediateRender:false}},{ct:.3f});")
        sc.sfx('marker', ct, .5)
    note = ctx.p('note', '')
    if note:
        nt = ctx.t(ctx.p('note_at'), lt - a + 1.3)
        sc.line(note, nt, y=622, size=42)
    return sc.done()
