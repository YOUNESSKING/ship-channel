"""Video 02 stick gags (crocodile rivers): white line art on near-black, the stick croc (and the stick figure where a person is the joke),
each gag carries a number, a timer bar, a labelled icon, a tally or a measured distance (rules 9-14)."""
from .common import *
from .croc_gfx import shape_svg, SHAPES, CSS
META = dict(name='croc_stick', about='Video 02 stick gags with the line-art croc: checklist (icons on their words), run_away (person runs from a labelled millipede), bite_car (car lands on the tooth row + number), mud_timer (croc in a mud pool + the timer bar), tally (two counters), lizard_car (lizard grows to car length), swim_route (dotted sea route between two river mouths + distance), temp_bar (body temperature falls in steps, labels on words), days_bar (the timer bar for a cold snap; can run off the edge), wrap (snake loops round the croc, two lengths), thermo (thermometer rises into the danger zone + number), eight (eight small crocs = one giant), roll (croc tries to roll, "?"), bite_bars (bar chart of two bite forces), eyes (only the eyes above water while a giant walks past on the bank), buffet (a giant croc with a fork, a small croc served on a plate).',
  variants=['checklist', 'run_away', 'bite_car', 'mud_timer', 'tally', 'lizard_car', 'swim_route', 'temp_bar', 'days_bar', 'wrap', 'thermo', 'eight', 'roll', 'bite_bars', 'eyes', 'buffet'],
  params={'kicker': 'small caps line (top)', 'number': 'big number', 'unit': 'italic unit after the number', 'number_at': 'when the number lands',
          'line': 'italic line', 'line_at': 'when the italic line shows', 'label': 'caps / italic label of the main object', 'label_at': 'when the label shows',
          'items': 'checklist: [{"icon":"thermometer","label":"TEMPERATURE","at":T}]; temp_bar: [{"label":"can\'t warm up","at":T}]; bite_bars: [{"label":"OUR CROC","value":16000,"max":null,"text":"16,000 N","at":T}]',
          'labels': 'mud_timer / days_bar: the four timer-bar labels', 'from_stop': 'timer start stop 0-3', 'to_stop': 'timer end stop 0-3, or 4 = run off the right edge',
          'move_at': 'when the marker / croc / snake / lizard starts moving', 'move_dur': 'how long the move takes',
          'a': 'tally: {"label":"AMERICAN CROCODILES","from":0,"to":151,"at":T}', 'b': 'tally: {"label":"ALLIGATORS","value":0}', 'at2': 'second beat (run_away: "(probably)"; roll: "?")'})

DARK = '#26262c'
def croc(x, y, w, col='#fff', flip=False, op=1.0):
    sc = w / 1000
    f = f' translate({w:.0f},0) scale(-1,1)' if flip else ''
    return f'<g transform="translate({x:.0f},{y:.0f}){f} scale({sc:.4f})" opacity="{op}">{shape_svg("croc", col, 4 / sc)}</g>'
def txt(i, x, y, s, size, cls='itsv', anchor='middle', extra=''):
    return f'<text id="{i}" x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" class="{cls}" style="font-size:{size}px;{extra}" opacity="0">{rich_svg(s) if cls == "itsv" else esc(s)}</text>'

def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a; B = ctx.b; D = ctx.dur
    svg = ''; js = []; over = ''
    kick = ctx.p('kicker', ''); number = ctx.p('number', ''); unit = ctx.p('unit', '')
    nat = ctx.t(ctx.p('number_at'), .5); line = ctx.p('line', ''); lat = ctx.t(ctx.p('line_at'), 1.2)
    lab = ctx.p('label', ''); labt = ctx.t(ctx.p('label_at'), .6); mat = ctx.t(ctx.p('move_at'), .2); mdur = ctx.p('move_dur')
    numpos = (900, 250)
    if v == 'checklist':
        svg += croc(80, 470, 420) + f'<text x="290" y="520" text-anchor="middle" class="lblm" style="font-size:16px">OUR CROC</text>'
        its = ctx.p('items', [])
        for k, it in enumerate(its):
            x = 680 + k * 260; y = 330; at = ctx.t(it.get('at'), .3 + .6 * k)
            svg += (f'<g id="{p}-i{k}" opacity="0"><g transform="translate({x},{y}) scale(.9)">{icon(it["icon"])}</g>'
                    f'<text x="{x}" y="{y + 120}" text-anchor="middle" class="lblm" style="font-size:18px">{esc(it.get("label", ""))}</text>'
                    f'<path d="M{x - 30},{y + 160} l18,18 l36,-40" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" id="{p}-k{k}" opacity="0"/></g>')
            js.append(f"pop('#{p}-i{k}',{at - .08:.3f},.3);fadeIn('#{p}-k{k}',{at + .3:.3f},.15);"); ctx.sfx('click', at, .5); ctx.sfx('tick', at + .3, .3)
    elif v == 'run_away':
        hx, hy, s = 760, 470, 1.15
        svg += f'<line x1="0" y1="{hy + 84 * s:.0f}" x2="1280" y2="{hy + 84 * s:.0f}" stroke="{SOFT}" stroke-opacity=".5" stroke-width="2"/>'
        svg += f'<g id="{p}-run">{fig(p, hx, hy, s)}</g>'
        seg = ''
        for k in range(16):
            cx = 40 + k * 26
            seg += f'<ellipse cx="{cx}" cy="{hy + 70 * s:.0f}" rx="17" ry="13" fill="{DARK}" stroke="#fff" stroke-width="4"/><path d="M{cx - 6},{hy + 82 * s:.0f} l-6,14 M{cx + 6},{hy + 82 * s:.0f} l6,14" stroke="#fff" stroke-width="3" fill="none"/>'
        seg += f'<path d="M454,{hy + 64 * s:.0f} q16,-16 26,-4 M456,{hy + 70 * s:.0f} q20,-6 26,8" stroke="#fff" stroke-width="3" fill="none"/>'
        svg += f'<g id="{p}-mil">{seg}<text id="{p}-lb" x="250" y="{hy + 10:.0f}" text-anchor="middle" class="lblm" style="font-size:22px" opacity="0">{esc(lab or "VEGETARIAN")}</text>'
        svg += f'<text id="{p}-pb" x="250" y="{hy + 50:.0f}" text-anchor="middle" class="itsv" style="font-size:36px" opacity="0">(probably)</text></g>'
        svg += f'<text x="250" y="{hy + 150:.0f}" text-anchor="middle" class="tbl" style="font-size:13px">ARTHROPLEURA · 2.5 M</text>'
        js.append(f"pose('{p}',{hx},{hy},{s},{{aL:60,aR:-60,lL:25,lR:-25}});flail('{p}',{hx},{hy},{s},{T:.3f},{D:.3f},-40,70,.16);bob('#{p}-run',{T:.3f},{D:.3f},-10,.16);")
        js.append(f"tl.fromTo('#{p}-run',{{x:0}},{{x:560,duration:{D:.3f},ease:'power1.in'}},{T:.3f});tl.fromTo('#{p}-mil',{{x:-200}},{{x:120,duration:{D:.3f},ease:'none'}},{T:.3f});")
        js.append(f"pop('#{p}-lb',{labt:.3f},.4);pop('#{p}-pb',{ctx.t(ctx.p('at2'), 1.4):.3f},.4);"); ctx.sfx('click', labt, .4); ctx.sfx('tok', ctx.t(ctx.p('at2'), 1.4), .5)
    elif v == 'bite_car':
        jaw = (f'<g fill="{DARK}" stroke="#fff" stroke-width="5" stroke-linejoin="round"><path d="M120,560 C260,520 520,500 760,500 L1000,500 C1040,500 1060,520 1060,545 L1060,560 Z"/>'
               f'<path d="M120,600 C300,620 600,630 900,620 L1060,610 L1060,580 L120,580 Z"/></g>'
               '<path d="M300,560 l14,-26 l14,26 M380,560 l14,-28 l14,28 M460,560 l14,-30 l14,30 M540,560 l14,-30 l14,30 M620,560 l14,-30 l14,30 M700,560 l14,-30 l14,30 M780,560 l14,-28 l14,28 M860,560 l14,-26 l14,26 M940,560 l14,-24 l14,24" fill="#fff" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>')
        jaw += (f'<path d="M930,502 C940,462 1010,462 1020,502" fill="{DARK}" stroke="#fff" stroke-width="5"/><circle cx="975" cy="488" r="8" fill="#fff"/>'
                f'<path d="M150,548 q14,-10 28,-2" fill="none" stroke="#fff" stroke-width="4"/>')
        svg += jaw + f'<text x="590" y="670" text-anchor="middle" class="tbl" style="font-size:14px">ONE ROW OF TEETH</text>'
        svg += f'<g id="{p}-car"><g transform="translate(400,530) scale(.42)">{shape_svg("car", "#fff", 10)}</g></g>'
        js.append(f"tl.fromTo('#{p}-car',{{y:-560}},{{y:0,duration:.45,ease:'power3.in'}},{mat:.3f});tl.to('#{p}-car',{{y:-6,duration:.08,yoyo:true,repeat:1}},{mat + .45:.3f});")
        ctx.sfx('thud', mat + .45, .8)
        numpos = (640, 200)
    elif v == 'mud_timer':
        svg += f'<ellipse cx="560" cy="470" rx="420" ry="70" fill="#2a2420" stroke="{SOFT}" stroke-opacity=".6" stroke-width="3"/>' + croc(260, 470, 600)
        svg += '<path d="M180,470 q40,-12 80,0 t80,0 M760,472 q40,-12 80,0 t80,0" stroke="#8b7a62" stroke-width="4" fill="none"/>'
        svg += f'<text x="560" y="575" text-anchor="middle" class="tbl" style="font-size:13px">{esc(lab or "MUD POOL")}</text>'
        svg += timer_bar(p, ctx.p('labels', ['LAST MEAL', 'WEEKS', '1 MONTH', 'MONTHS']))
        f_, t_ = ctx.p('from_stop', 0), ctx.p('to_stop', 3)
        js.append(f"mark('{p}',{mat:.3f},{X0[f_]},{X0[t_]},{mdur or max(.6, D - 1.2):.2f});")
        numpos = (900, 200)
    elif v == 'tally':
        a = ctx.p('a', {}); b = ctx.p('b', {}); aat = ctx.t(a.get('at'), .6)
        svg += f'<g transform="translate(330,190) scale(1.1)">{icon("croc")}</g><g transform="translate(950,190) scale(1.1)">{icon("croc")}</g>'
        svg += f'<text id="{p}-na" x="330" y="440" text-anchor="middle" class="cg" style="font-size:150px;fill:{WARM}">{a.get("from", 0)}</text>'
        svg += f'<text x="330" y="500" text-anchor="middle" class="lblm" style="font-size:18px">{esc(a.get("label", ""))}</text>'
        svg += f'<text x="950" y="440" text-anchor="middle" class="cg" style="font-size:150px;fill:{WARM};opacity:.85">{b.get("value", 0)}</text>'
        svg += f'<text x="950" y="500" text-anchor="middle" class="lblm" style="font-size:18px">{esc(b.get("label", ""))}</text><line x1="640" y1="170" x2="640" y2="520" stroke="{GOLD}" stroke-opacity=".6" stroke-width="2"/>'
        js.append(f"(function(){{const o={{v:{a.get('from', 0)}}},el=document.getElementById('{p}-na');tl.fromTo(o,{{v:{a.get('from', 0)}}},{{v:{a.get('to', 0)},duration:{a.get('dur', 1.4)},ease:'power2.out',immediateRender:false,onUpdate:()=>{{el.textContent=Math.round(o.v)}}}},{aat:.3f});}})();")
        ctx.sfx('tick', aat, .3); ctx.sfx('thud', aat + a.get('dur', 1.4), .7)
    elif v == 'lizard_car':
        gy = 520
        svg += f'<line x1="80" y1="{gy}" x2="1200" y2="{gy}" stroke="{SOFT}" stroke-opacity=".5" stroke-width="2"/>'
        svg += f'<g transform="translate(700,{gy}) scale(.45)">{shape_svg("car", "#fff", 9)}</g><text x="925" y="{gy + 40}" text-anchor="middle" class="lblm" style="font-size:16px">CAR · 4.5 M</text>'
        svg += f'<g id="{p}-liz"><g transform="translate(130,{gy}) scale(.45)">{shape_svg("monitor", GOLD, 9)}</g></g><text id="{p}-ll" x="355" y="{gy + 40}" text-anchor="middle" class="lblm" style="font-size:16px">{esc(lab or "KOMODO DRAGON")}</text>'
        js.append(f"tl.fromTo('#{p}-liz',{{scale:.55,svgOrigin:'130 {gy}'}},{{scale:1,svgOrigin:'130 {gy}',duration:{mdur or 1.2},ease:'power2.inOut'}},{mat:.3f});")
        ctx.sfx('swoosh', mat, .3)
        numpos = (640, 200)
    elif v == 'swim_route':
        coast = 'M-20,250 C150,230 260,300 380,270 C520,236 600,320 760,300 C900,282 1000,240 1300,260'
        svg += f'<path d="{coast} L1300,-10 L-20,-10 Z" fill="#20262a" stroke="{SOFT}" stroke-width="3"/>'
        svg += f'<g transform="translate(250,200) scale(.55)">{icon("river")}</g><g transform="translate(1030,200) scale(.55)">{icon("river")}</g>'
        route = 'M250,300 C420,420 860,430 1030,300'
        svg += f'<path id="{p}-rt" d="{route}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="2 14" stroke-linecap="round"/>'
        svg += f'<g id="{p}-cr"><g transform="translate(-55,-20) scale(.55)">{icon("croc")}</g></g>'
        svg += f'<text x="640" y="560" text-anchor="middle" class="tbl" style="font-size:13px">{esc(lab or "TAGGED SALTWATER CROC")}</text>'
        js.append(f"(function(){{const path=document.getElementById('{p}-rt'),L=path.getTotalLength(),o={{v:0}},g=document.getElementById('{p}-cr');const up=()=>{{const q=path.getPointAtLength(L*o.v);g.setAttribute('transform','translate('+q.x+','+q.y+')');}};up();"
                  f"tl.fromTo(o,{{v:0}},{{v:1,duration:{mdur or max(.8, D - .3):.2f},ease:'power1.inOut',immediateRender:false,onUpdate:up}},{mat:.3f});}})();")
        numpos = (640, 470)
    elif v == 'temp_bar':
        svg += croc(120, 500, 560) + f'<g transform="translate(400,250) scale(.6)">{icon("snowflake")}</g>'
        bx, by0, by1 = 900, 150, 520
        svg += f'<rect x="{bx - 22}" y="{by0}" width="44" height="{by1 - by0}" rx="22" fill="{DARK}" stroke="#fff" stroke-width="4"/><circle cx="{bx}" cy="{by1 + 30}" r="44" fill="{DARK}" stroke="#fff" stroke-width="4"/>'
        svg += f'<rect id="{p}-fill" x="{bx - 12}" y="{by0 + 20}" width="24" height="{by1 + 10 - by0 - 20}" fill="{GOLD}"/><circle cx="{bx}" cy="{by1 + 30}" r="32" fill="{GOLD}"/>'
        svg += f'<text x="{bx}" y="{by0 - 20}" text-anchor="middle" class="tbl" style="font-size:13px">BODY TEMPERATURE</text>'
        its = ctx.p('items', []); n = len(its) + 1; cur = by0 + 20
        for k, it in enumerate(its):
            at = ctx.t(it.get('at'), .5 + .8 * k); ny = by0 + 20 + (by1 - by0 - 40) * (k + 1) / n
            js.append(f"tl.to('#{p}-fill',{{attr:{{y:{ny:.0f},height:{by1 + 10 - ny:.0f}}},duration:.3,ease:'power2.out'}},{at - .1:.3f});")
            svg += txt(f'{p}-l{k}', bx + 70, ny + 12, it['label'], 40, anchor='start')
            js.append(f"pop('#{p}-l{k}',{at:.3f},.4);"); ctx.sfx('click', at, .45)
    elif v == 'days_bar':
        svg += timer_bar(p, ctx.p('labels', ['START', '10 DAYS', '1 MONTH', '3 MONTHS']))
        svg += croc(100, 520, 380, op=.9) + f'<g transform="translate(560,430) scale(.55)">{icon("snowflake")}</g>'
        f_, t_ = ctx.p('from_stop', 0), ctx.p('to_stop', 1)
        tx = X0[t_] if t_ < 4 else 1400
        js.append(f"mark('{p}',{mat:.3f},{X0[f_]},{tx},{mdur or 1.0:.2f});")
        if t_ >= 4: js.append(f"tl.to('#{p}-kb',{{x:-80,duration:{mdur or 1.0:.2f},ease:'power1.in'}},{mat:.3f});")
        numpos = (900, 250)
    elif v == 'wrap':
        svg += croc(290, 430, 700)
        loop = 'M180,520 C180,300 1080,300 1080,420 C1080,560 300,560 300,400 C300,250 980,240 1000,380'
        svg += f'<path id="{p}-sn" d="{loop}" fill="none" stroke="{GOLD}" stroke-width="30" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" stroke-opacity=".9"/>'
        svg += txt(f'{p}-a', 1130, 300, '13 m', 56) + txt(f'{p}-b', 640, 640, '5 m', 44, extra=f'fill:{WARM}')
        svg += f'<text x="1130" y="335" text-anchor="middle" class="tbl" style="font-size:12px">TITANOBOA</text><text x="640" y="670" text-anchor="middle" class="tbl" style="font-size:12px">OUR CROC</text>'
        js.append(f"tl.fromTo('#{p}-sn',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{mdur or 1.2},ease:'power1.inOut'}},{mat:.3f});pop('#{p}-a',{labt:.3f},.4);pop('#{p}-b',{labt + .25:.3f},.4);")
        ctx.sfx('swoosh_rope', mat, .4); ctx.sfx('click', labt, .4)
    elif v == 'thermo':
        svg += croc(80, 520, 520)
        bx, by0, by1 = 760, 120, 540; zone = by0 + 120
        svg += f'<rect x="{bx - 22}" y="{by0}" width="44" height="{by1 - by0}" rx="22" fill="{DARK}" stroke="#fff" stroke-width="4"/><circle cx="{bx}" cy="{by1 + 30}" r="44" fill="{DARK}" stroke="#fff" stroke-width="4"/>'
        svg += f'<rect x="{bx - 21}" y="{by0 + 4}" width="42" height="{zone - by0 - 4}" rx="18" fill="{GOLD}" fill-opacity=".22"/><line x1="{bx - 40}" y1="{zone}" x2="{bx + 60}" y2="{zone}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="8 8"/>'
        svg += f'<rect id="{p}-fill" x="{bx - 12}" y="{by1 - 120}" width="24" height="130" fill="{GOLD}"/><circle cx="{bx}" cy="{by1 + 30}" r="32" fill="{GOLD}"/>'
        svg += f'<text x="{bx}" y="{by0 - 20}" text-anchor="middle" class="tbl" style="font-size:13px">BODY TEMPERATURE</text>'
        svg += txt(f'{p}-z', bx + 80, zone - 40, lab or 'trouble', 40, anchor='start')
        js.append(f"tl.to('#{p}-fill',{{attr:{{y:{zone - 30},height:{by1 + 10 - zone + 30}}},duration:{mdur or 1.6},ease:'power1.inOut'}},{mat:.3f});pop('#{p}-z',{labt:.3f},.4);")
        ctx.sfx('click', labt, .4)
        numpos = (1050, 330)
    elif v == 'eight':
        svg += f'<g transform="translate(140,300) scale(1.0)">{shape_svg("croc", GOLD, 4)}</g><text x="640" y="335" text-anchor="middle" class="lblm" style="font-size:16px">{esc(lab or "SARCOSUCHUS")}</text>'
        for k in range(8):
            x = 120 + k * 132; at = mat + .12 * k
            svg += f'<g id="{p}-c{k}" opacity="0">{croc(x, 520, 118)}</g>'
            js.append(f"tl.fromTo('#{p}-c{k}',{{opacity:0,y:-14}},{{opacity:1,y:0,duration:.2}},{at:.3f});"); ctx.sfx('tick', at, .3)
        svg += f'<text x="640" y="575" text-anchor="middle" class="lblm" style="font-size:15px">OUR CROC x 8</text>'
        numpos = (640, 660)
    elif v == 'roll':
        cx, cy = 640, 400
        svg += f'<g id="{p}-cr">{croc(cx - 300, cy + 40, 600)}</g>'
        svg += f'<path d="M{cx + 330},{cy + 40} A330,150 0 1 1 {cx + 300},{cy - 70}" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="14 12"/><path d="M{cx + 300},{cy - 70} l-34,-6 m34,6 l-8,32" stroke="{GOLD}" stroke-width="5" fill="none"/>'
        svg += txt(f'{p}-q', cx, cy - 160, '?', 200, cls='itsv')
        a2 = ctx.t(ctx.p('at2'), D - .9)
        js.append(f"tl.to('#{p}-cr',{{rotation:-35,svgOrigin:'{cx} {cy}',duration:.35,ease:'power2.out',yoyo:true,repeat:3}},{mat:.3f});pop('#{p}-q',{a2:.3f},.4);")
        ctx.sfx('swoosh', mat, .3); ctx.sfx('tok', a2, .5)
        numpos = (640, 640)
    elif v == 'bite_bars':
        its = ctx.p('items', []); mx = max(max(i['value'], i.get('max') or 0) for i in its)
        for k, it in enumerate(its):
            y = 260 + k * 170; at = ctx.t(it.get('at'), .3 + .9 * k); w1 = 820 * it['value'] / mx; w2 = 820 * (it.get('max') or it['value']) / mx
            col = WARM if k == 0 else GOLD
            svg += f'<text x="140" y="{y - 22}" class="lblm" style="font-size:16px">{esc(it["label"])}</text>'
            svg += f'<rect id="{p}-b{k}" x="140" y="{y}" width="{w1:.0f}" height="56" fill="{col}" fill-opacity=".85"/>'
            if it.get('max'): svg += f'<rect id="{p}-e{k}" x="{140 + w1:.0f}" y="{y}" width="{w2 - w1:.0f}" height="56" fill="{col}" fill-opacity=".3" stroke="{col}" stroke-dasharray="6 6"/>'
            svg += f'<text id="{p}-t{k}" x="{150 + w2:.0f}" y="{y + 42}" class="itsv" style="font-size:36px;fill:{col if k else WARM}" opacity="0">{rich_svg(it.get("text", ""))}</text>'
            js.append(f"tl.fromTo('#{p}-b{k}',{{scaleX:0,svgOrigin:'140 {y}'}},{{scaleX:1,svgOrigin:'140 {y}',duration:.6,ease:'power2.out'}},{at:.3f});fadeIn('#{p}-t{k}',{at + .5:.3f},.3);"
                      + (f"tl.fromTo('#{p}-e{k}',{{opacity:0}},{{opacity:1,duration:.3}},{at + .5:.3f});" if it.get('max') else ''))
            ctx.sfx('swoosh', at, .25); ctx.sfx('click', at + .55, .4)
        numpos = (1120, 170)
    elif v == 'eyes':
        wy = 470
        svg += f'<path d="M-20,250 L1300,250" stroke="{SOFT}" stroke-opacity=".5" stroke-width="2"/>'
        svg += f'<g id="{p}-sp"><g transform="translate(0,250) scale(.36)">{shape_svg("spino", GOLD, 9)}</g></g>'
        svg += f'<text x="640" y="290" text-anchor="middle" class="tbl" style="font-size:12px">THE BANK</text>'
        svg += water(p, wy, .85)
        svg += (f'<g id="{p}-ey"><path d="M560,{wy + 4} q30,-40 60,0 M660,{wy + 4} q30,-40 60,0" fill="{DARK}" stroke="#fff" stroke-width="4"/>'
                f'<circle cx="590" cy="{wy - 14}" r="6" fill="#fff"/><circle cx="690" cy="{wy - 14}" r="6" fill="#fff"/></g>')
        js.append(f"tl.fromTo('#{p}-sp',{{x:-380}},{{x:1300,duration:{D:.3f},ease:'none'}},{T:.3f});drift('#{p}-water',{T:.3f},{D:.3f},-120);bob('#{p}-ey',{T:.3f},{D:.3f},3,.6);")
        svg += txt(f'{p}-lb', 640, 620, lab or 'hours underwater', 46)
        js.append(f"pop('#{p}-lb',{labt:.3f},.4);"); ctx.sfx('tok', labt, .4)
    elif v == 'buffet':
        svg += f'<g id="{p}-big">{croc(60, 470, 640, col=GOLD)}</g><text x="380" y="520" text-anchor="middle" class="lblm" style="font-size:15px">{esc(lab or "PURUSSAURUS")}</text>'
        svg += f'<ellipse cx="960" cy="455" rx="230" ry="44" fill="{DARK}" stroke="#fff" stroke-width="5"/><ellipse cx="960" cy="450" rx="170" ry="26" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="3"/>'
        svg += f'<g id="{p}-sm" opacity="0">{croc(860, 444, 200)}</g>'
        svg += f'<g id="{p}-fk"><path d="M720,250 V330 M700,250 V300 M740,250 V300 M700,300 Q720,320 740,300" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/><path d="M720,330 L720,420" stroke="#fff" stroke-width="8" stroke-linecap="round"/></g>'
        js.append(f"tl.fromTo('#{p}-sm',{{opacity:0,y:-60}},{{opacity:1,y:0,duration:.35,ease:'power2.in'}},{mat:.3f});tl.fromTo('#{p}-fk',{{rotation:0,svgOrigin:'720 420'}},{{rotation:-12,svgOrigin:'720 420',duration:.25,yoyo:true,repeat:3}},{mat + .4:.3f});")
        ctx.sfx('thud_soft', mat + .35, .5)
        svg += txt(f'{p}-lb', 960, 560, 'on the menu', 44); js.append(f"pop('#{p}-lb',{labt:.3f},.4);"); ctx.sfx('tok', labt, .5)
    # shared: kicker, number, italic line
    if kick: over += f'<div class="jo gold" style="position:absolute;left:90px;top:48px;font-size:16px">{rich(kick)}</div>'
    if number:
        nx, ny = numpos
        over += f'<div id="{p}-num" class="cg op0" style="position:absolute;left:{nx - 400}px;width:800px;text-align:center;top:{ny - 90}px;font-size:110px">{rich(number)}{f"<i style=font-size:64px> {rich(unit)}</i>" if unit else ""}</div>'
        js.append(f"pop('#{p}-num',{nat:.3f},.4);"); ctx.sfx('thud', nat, .6)
    if line:
        over += f'<div id="{p}-line" class="cg op0" style="position:absolute;left:0;width:1280px;text-align:center;top:{640 if v not in ("eyes", "bite_car", "lizard_car") else 600}px;font-size:42px;color:{ITAL}"><i>{rich(line)}</i></div>'
        js.append(f"write('#{p}-line',{lat:.3f},.6);")
    js.insert(0, f"kb('#{p}-kb',{T:.3f},{B:.3f},1.0,1.04,'50% 50%');")
    ctx.js.append('\n'.join(js))
    return dict(html=ctx.shot_div(f'<div id="{p}-kb" class="kb"><svg width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg>{over}</div>', 'stick'), css=CSS)
