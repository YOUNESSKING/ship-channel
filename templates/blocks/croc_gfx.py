"""Video 02 graphics (crocodile rivers): true-scale size charts with a 1.8 m human, rival line-ups, footprints, skull diagrams, counts.
Same style C as the other blocks: dark card, white/gold line art, Cormorant numbers, Jost caps."""
import math
from .common import *
META = dict(name='croc_gfx', about='Video 02 graphics: "size_chart" = rivals and our 5 m croc in lanes at true scale next to a 1.8 m human, metre grid, ruler + label per animal (rule 54); "lineup" = rival silhouettes in a row that fade out one by one; "footprints" = three-toed prints walk along a river bank; "heads" = phytosaur vs crocodile head profiles (nostril circles or a "not related" sign); "count" = N different crocodilian silhouettes pop in with a big number; "tooth_banana" = a Deinosuchus tooth next to a banana on a cm ruler; "teeth" = a blade-like serrated tooth next to a cone tooth; "debate" = two Spinosaurus silhouettes, wading vs swimming, with a big "?".',
  variants=['size_chart', 'lineup', 'footprints', 'heads', 'count', 'tooth_banana', 'teeth', 'debate'],
  params={'items': 'size_chart: list of {"shape":"croc|theropod|spino|snake|sawfish|fish|monitor|amphibian|slim|skull|bus|car","lane":"bank" (same lane = same ground line),"length_m":7,"min_m":4.5 (optional range),"name":"SMILOSUCHUS","label":"7 m","at":T,"ours":true (warm white = our croc)} drawn top to bottom; lineup: list of {"shape","name","fade_at":T}',
          'human_m': 'size_chart: human height (default 1.8)', 'human_label': 'size_chart: label under the human (default "human")',
          'kicker': 'small caps line top left', 'note': 'big italic gold line top right (e.g. "8x heavier")', 'note_at': 'when the note shows',
          'line': 'italic line at the bottom (lineup / footprints / heads / count)', 'line_at': 'when the line shows',
          'prints_at': 'footprints: time of the first print (prints follow every 0.35 s)', 'label': 'footprints / count: caps label',
          'mode': 'heads: "nostrils" (circles land on nostril_at / tip_at) or "unrelated" (a not-equal sign lands on line_at)',
          'nostril_at': 'heads: when the circle on the phytosaur nostrils lands', 'tip_at': 'heads: when the circle on the croc snout tip lands',
          'n': 'count: how many silhouettes (default 7)', 'number_at': 'count: when the big number lands', 'stagger': 'count / lineup: seconds between silhouettes',
          'a_at': 'tooth_banana / teeth / debate: when the first object shows', 'b_at': 'tooth_banana / teeth / debate: when the second object (or the "?") shows',
          'a_label': 'teeth / debate: label of the left object', 'b_label': 'teeth / debate: label of the right object'})

_F = 'fill="#1a2429" stroke-linejoin="round"'
def _snake():
    up = []; lo = []
    for i in range(0, 1001, 20):
        x = i; c = -70 - 34 * math.sin(2 * math.pi * x / 330)
        w = 30 * min(1.0, (x + 10) / 220.0, (1010 - x) / 70.0) + (10 if x > 930 else 0)
        up.append((x, c - w)); lo.append((x, c + w))
    pts = up + lo[::-1]
    return 'M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in pts) + ' Z'
SHAPES = {   # (svg path data in a 1000-wide box, facing right, ground/belly at y=0; top extent as a share of the length)
 'croc': ('<path d="M0,-34 C90,-40 190,-78 300,-100 C420,-124 540,-124 640,-120 C720,-118 790,-114 842,-118 L954,-120 C984,-118 1000,-106 1000,-92 L990,-78 C968,-70 930,-68 892,-70 C836,-68 786,-58 710,-50 L700,-14 L690,0 L610,0 L606,-30 C520,-26 440,-26 360,-30 L350,0 L270,0 L262,-34 C170,-28 80,-24 0,-34 Z"/>'
          '<path d="M300,-100 q20,-22 40,-4 M400,-118 q20,-22 40,-4 M500,-124 q20,-22 40,-4 M600,-122 q20,-22 40,-4" fill="none" stroke-width="6" stroke-opacity=".7"/><circle cx="850" cy="-128" r="8" class="eye"/>', .15),
 'slim': ('<path d="M0,-30 C90,-36 190,-66 300,-86 C420,-104 520,-106 620,-102 C680,-100 720,-98 750,-104 L800,-100 C880,-90 960,-86 1000,-80 L998,-70 C940,-66 860,-66 790,-62 C760,-60 730,-52 700,-46 L692,-12 L684,0 L612,0 L606,-28 C520,-24 440,-24 360,-28 L350,0 L276,0 L268,-30 C170,-26 80,-22 0,-30 Z"/><circle cx="745" cy="-104" r="7" class="eye"/>', .12),
 'amphibian': ('<path d="M0,-40 C120,-60 220,-70 320,-96 C440,-122 560,-124 660,-118 C740,-114 800,-118 850,-122 L950,-112 C985,-106 1000,-94 996,-80 C960,-70 900,-68 850,-66 C790,-62 740,-56 700,-50 L690,-14 L708,0 L620,0 L612,-30 C520,-28 430,-28 360,-32 L352,0 L272,0 L270,-36 C170,-26 80,-18 0,-40 Z"/>'
               '<path d="M0,-40 C60,-90 160,-98 300,-100" fill="none" stroke-width="5" stroke-opacity=".6"/><circle cx="868" cy="-118" r="8" class="eye"/>', .13),
 'monitor': ('<path d="M0,-28 C150,-40 300,-90 420,-120 C520,-150 640,-160 740,-150 C800,-145 840,-160 880,-170 C930,-180 980,-170 1000,-150 L995,-130 C960,-118 900,-118 860,-112 C800,-100 760,-90 720,-86 L742,-30 L776,0 L690,0 L676,-64 C600,-62 520,-66 470,-70 L476,-30 L506,0 L420,0 L404,-62 C300,-50 150,-30 0,-28 Z"/><circle cx="930" cy="-160" r="8" class="eye"/>'
             '<path d="M990,-140 l26,-6 m-26,6 l26,8" fill="none" stroke-width="4"/>', .18),
 'theropod': ('<path d="M490,-232 L466,-130 L436,-34 L496,-14 L496,0 L408,0 L408,-30 L430,-120 L440,-220 Z" fill-opacity=".7"/>'
              '<path d="M0,-262 C120,-270 300,-300 430,-340 C520,-370 620,-372 700,-360 C760,-352 800,-380 830,-420 C860,-450 930,-452 975,-438 L1000,-420 L996,-400 L940,-392 L990,-380 L985,-364 C930,-352 880,-350 850,-338 C800,-318 760,-296 720,-280 C660,-252 600,-236 560,-232 L540,-180 C548,-140 540,-110 520,-80 L500,-30 L560,-12 L560,0 L470,0 L470,-30 L490,-90 C470,-120 450,-160 450,-200 C380,-220 330,-240 290,-248 C190,-262 90,-258 0,-262 Z"/>'
              '<path d="M732,-282 l28,40 l16,-4" fill="none" stroke-width="9" stroke-linecap="round"/><circle cx="915" cy="-428" r="8" class="eye"/>', .46),
 'spino': ('<path d="M420,-330 C440,-560 560,-600 640,-560 C690,-530 720,-440 716,-356 Z" fill-opacity=".85"/>'
           '<path d="M490,-232 L466,-130 L436,-34 L496,-14 L496,0 L408,0 L408,-30 L430,-120 L440,-220 Z" fill-opacity=".7"/>'
           '<path d="M0,-250 C120,-262 300,-296 430,-336 C520,-366 620,-368 700,-356 C760,-350 790,-378 816,-404 C850,-434 900,-430 940,-418 C970,-412 990,-404 1000,-398 L996,-386 C960,-384 920,-384 880,-376 C850,-366 800,-330 760,-300 C700,-260 620,-240 560,-232 L540,-180 C548,-140 540,-110 520,-80 L500,-30 L560,-12 L560,0 L470,0 L470,-30 L490,-90 C470,-120 450,-160 450,-200 C380,-218 330,-232 290,-240 C190,-252 90,-246 0,-250 Z"/>'
           '<path d="M740,-292 l26,38 l16,-4" fill="none" stroke-width="9" stroke-linecap="round"/><circle cx="880" cy="-414" r="7" class="eye"/>', .58),
 'snake': (f'<path d="{_snake()}"/><circle cx="985" cy="-74" r="7" class="eye"/>', .14),
 'sawfish': ('<path d="M0,-150 L40,-230 L70,-150 C200,-120 340,-118 420,-130 L470,-220 L500,-134 C560,-130 620,-118 680,-100 L700,-96 L700,-74 C630,-56 560,-44 480,-40 L460,0 L430,-40 C320,-40 180,-60 70,-90 L30,-20 L36,-100 C20,-110 6,-128 0,-150 Z"/>'
             '<path d="M690,-92 L1000,-90 L1000,-80 L690,-78 Z"/><path d="M720,-92 v-12 M760,-92 v-12 M800,-92 v-12 M840,-92 v-12 M880,-92 v-12 M920,-92 v-12 M960,-92 v-12 M720,-78 v12 M760,-78 v12 M800,-78 v12 M840,-78 v12 M880,-78 v12 M920,-78 v12 M960,-78 v12" fill="none" stroke-width="5"/><circle cx="640" cy="-108" r="6" class="eye"/>', .23),
 'fish': ('<path d="M0,-200 L60,-150 C140,-230 300,-280 480,-280 C640,-280 800,-240 900,-200 C960,-176 1000,-150 1000,-130 C990,-100 950,-80 880,-60 C760,-30 620,-20 480,-22 C300,-24 140,-60 60,-110 L0,-60 L30,-130 Z"/>'
          '<path d="M420,-276 L470,-360 L540,-282 M430,-26 L470,40 L540,-24 M700,-240 L740,-300 L790,-228 M700,-36 L740,20 L790,-40" fill-opacity=".8"/><circle cx="900" cy="-170" r="10" class="eye"/>', .30),
 'elephant': ('<path d="M60,-380 C60,-560 250,-640 470,-640 C620,-640 700,-600 760,-560 C840,-640 960,-620 990,-520 C1005,-460 980,-400 940,-380 C930,-300 920,-200 900,-120 L880,-60 L860,-120 C880,-220 880,-300 860,-360 C840,-340 820,-330 800,-330 L790,0 L690,0 L680,-280 C560,-260 420,-260 300,-280 L290,0 L190,0 L170,-300 C110,-320 70,-340 60,-380 Z"/><path d="M60,-380 C40,-360 30,-300 40,-240" fill="none" stroke-width="10"/><circle cx="905" cy="-520" r="10" class="eye"/>'
              '<path d="M880,-400 C930,-330 990,-330 1000,-380" fill="none" stroke-width="16" stroke-linecap="round" stroke-opacity=".9"/>', .64),
 'elephant_straight': ('<path d="M60,-380 C60,-560 250,-640 470,-640 C620,-640 700,-600 760,-560 C840,-640 960,-620 990,-520 C1005,-460 980,-400 940,-380 C930,-300 920,-200 900,-120 L880,-60 L860,-120 C880,-220 880,-300 860,-360 C840,-340 820,-330 800,-330 L790,0 L690,0 L680,-280 C560,-260 420,-260 300,-280 L290,0 L190,0 L170,-300 C110,-320 70,-340 60,-380 Z"/><path d="M60,-380 C40,-360 30,-300 40,-240" fill="none" stroke-width="10"/><circle cx="905" cy="-520" r="10" class="eye"/>'
              '<path d="M880,-400 L1000,-250" fill="none" stroke-width="16" stroke-linecap="round" stroke-opacity=".9"/>', .64),
 'skull': ('<path d="M0,-150 C30,-200 110,-215 200,-205 C260,-198 300,-180 330,-170 C380,-200 430,-200 450,-170 C520,-140 700,-110 860,-80 C940,-66 990,-56 1000,-40 C990,-20 950,-12 900,-12 C760,-12 520,-14 300,-10 C180,-8 60,-20 20,-60 C0,-90 -6,-120 0,-150 Z"/>'
           '<ellipse cx="250" cy="-150" rx="42" ry="26" fill="#0b1013"/><ellipse cx="110" cy="-120" rx="48" ry="40" fill="#0b1013"/><circle cx="395" cy="-186" r="13" fill="#0b1013"/>'
           '<path d="M300,-12 l8,16 l8,-16 M380,-12 l8,16 l8,-16 M460,-12 l8,16 l8,-16 M540,-12 l8,16 l8,-16 M620,-12 l8,16 l8,-16 M700,-12 l8,16 l8,-16 M780,-12 l8,16 l8,-16 M860,-12 l8,16 l8,-16" fill="none" stroke-width="5"/>', .22),
 'bus': ('<path d="M0,-60 L0,-300 C0,-316 12,-326 28,-326 L960,-326 C985,-326 1000,-312 1000,-290 L1000,-60 Z"/>'
         '<path d="M40,-290 h120 v90 h-120 Z M190,-290 h120 v90 h-120 Z M340,-290 h120 v90 h-120 Z M490,-290 h120 v90 h-120 Z M640,-290 h120 v90 h-120 Z M800,-290 h160 v110 h-160 Z" fill="none" stroke-width="5"/>'
         '<circle cx="180" cy="-50" r="50" fill="#0b1013"/><circle cx="820" cy="-50" r="50" fill="#0b1013"/>', .33),
 'car': ('<path d="M0,-80 L0,-170 C0,-190 20,-200 60,-205 L220,-215 C270,-300 330,-330 450,-330 L650,-330 C730,-330 780,-300 840,-220 L950,-200 C985,-194 1000,-176 1000,-150 L1000,-80 Z"/>'
         '<path d="M270,-220 C310,-290 350,-305 450,-305 L540,-305 L540,-220 Z M570,-305 L650,-305 C700,-305 740,-280 790,-220 L570,-220 Z" fill="none" stroke-width="6"/>'
         '<circle cx="210" cy="-80" r="80" fill="#0b1013"/><circle cx="790" cy="-80" r="80" fill="#0b1013"/>', .33),
}
def shape_svg(name, stroke, sw=3, op=.9):
    d, _ = SHAPES[name]
    return f'<g {_F} stroke="{stroke}" stroke-opacity="{op}" stroke-width="{sw}" class="shp">{d}</g>'
def hr(name): return SHAPES[name][1]
CSS = '.shp .eye{fill:#f6efe0;stroke:none}'

def _grid(x0, x1, y0, y1, ppm):
    step = 1 if ppm >= 55 else (2 if ppm >= 26 else 5)
    s = ''; m = 0
    while x0 + m * ppm <= x1 + 1:
        x = x0 + m * ppm
        s += f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}" stroke="#7fa3b3" stroke-opacity="{.22 if m % (step * (5 if step == 1 else 2)) else .38}" stroke-width="1"/>'
        if m % step == 0: s += f'<text x="{x:.1f}" y="{y1 + 22}" text-anchor="middle" class="tbl" style="font-size:12px;letter-spacing:.1em">{m}</text>'
        m += 1
    s += f'<text x="{x0 + m * ppm - ppm + 18:.0f}" y="{y1 + 22}" class="tbl" style="font-size:12px;letter-spacing:.1em">M</text>'
    for k in range(int((y1 - y0) / ppm) + 1):
        y = y1 - k * ppm
        s += f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="#7fa3b3" stroke-opacity=".12" stroke-width="1"/>'
    return s

def size_chart(ctx):
    p = ctx.id; T = ctx.a; items = ctx.p('items', []); H = float(ctx.p('human_m', 1.8)); hl = ctx.p('human_label', 'human')
    if not items: raise KeyError('"items" (the animals of the size chart)')
    X0, X1 = 230, 1200; Y0, Y1 = 112, 640
    maxL = max(float(i['length_m']) for i in items)
    gap = 64
    lanes = []                       # items with the same "lane" share one ground line (overlapping, like a classic size chart)
    for k, it in enumerate(items):
        ln = it.get('lane', f'_{k}')
        if not lanes or lanes[-1][0] != ln: lanes.append((ln, []))
        lanes[-1][1].append(k)
    def lane_h(ks, last):
        top = max(hr(items[k].get('shape', 'croc')) * float(items[k]['length_m']) for k in ks)
        return max(top, H if last else 0)
    extra_r = lambda ks: 34 * (len(ks) - 1)
    hsum = sum(lane_h(ks, j == len(lanes) - 1) for j, (_, ks) in enumerate(lanes))
    ppm = min((X1 - X0) / maxL, (Y1 - Y0 - gap * len(lanes) - sum(extra_r(ks) for _, ks in lanes)) / max(hsum, .1), 170)
    svg = _grid(X0, X0 + math.ceil(maxL) * ppm if X0 + math.ceil(maxL) * ppm <= X1 + 2 else X1, Y0 - 10, Y1, ppm)
    js = []; y = Y0
    for j, (_, ks) in enumerate(lanes):
        y += gap + extra_r(ks) + lane_h(ks, j == len(lanes) - 1) * ppm
        base = min(y, Y1); last_base = base
        order = sorted(ks, key=lambda k: -float(items[k]['length_m']))
        for r_i, k in enumerate(order):
            it = items[k]; L = float(it['length_m']); sh = it.get('shape', 'croc')
            col = WARM if it.get('ours') else GOLD; at = ctx.t(it.get('at'), .2 + .5 * k)
            sc = L * ppm / 1000
            svg += f'<g id="{p}-a{k}" opacity="0"><g transform="translate({X0},{base:.1f}) scale({sc:.4f})">{shape_svg(sh, col if r_i == 0 else SOFT, 3 / max(sc, .05) * .9)}</g></g>'
            rx1 = X0 + L * ppm; ry = base - max(hr(items[q].get('shape', 'croc')) * float(items[q]['length_m']) for q in ks) * ppm - 18 - 34 * r_i
            col = col if r_i == 0 else SOFT
            lab = it.get('label') or (f'{it["min_m"]:g}–{L:g} m' if it.get('min_m') else f'{L:g} m')
            svg += (f'<g id="{p}-r{k}" opacity="0"><line x1="{X0}" y1="{ry:.1f}" x2="{rx1:.1f}" y2="{ry:.1f}" stroke="{col}" stroke-width="2.5"/>'
                    f'<line x1="{X0}" y1="{ry - 9:.1f}" x2="{X0}" y2="{ry + 9:.1f}" stroke="{col}" stroke-width="2.5"/><line x1="{rx1:.1f}" y1="{ry - 9:.1f}" x2="{rx1:.1f}" y2="{ry + 9:.1f}" stroke="{col}" stroke-width="2.5"/>')
            if it.get('min_m'):
                mx = X0 + float(it['min_m']) * ppm
                svg += f'<line x1="{mx:.1f}" y1="{ry - 9:.1f}" x2="{mx:.1f}" y2="{ry + 9:.1f}" stroke="{col}" stroke-width="2"/><line x1="{mx:.1f}" y1="{ry:.1f}" x2="{rx1:.1f}" y2="{ry:.1f}" stroke="{col}" stroke-width="6" stroke-opacity=".35"/>'
            roomy = rx1 + 14 + 17 * len(lab) < 1262
            tx, ty, anc = (rx1 + 14, ry + 12, 'start') if roomy else (rx1, ry - 16, 'end')
            svg += (f'<text x="{tx:.0f}" y="{ty:.0f}" text-anchor="{anc}" class="itsv" style="font-size:34px;fill:{ITAL if not it.get("ours") else WARM};paint-order:stroke;stroke:#0b1013;stroke-width:6px">{rich_svg(lab)}</text>'
                    f'<text x="{X0 + 4}" y="{ry - 14:.0f}" class="tbl" style="font-size:13px">{esc(it.get("name", "").upper())}</text></g>')
            js.append(f"tl.fromTo('#{p}-a{k}',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.6,ease:'power2.out'}},{at:.3f});fadeIn('#{p}-r{k}',{at + .35:.3f},.4);")
            ctx.sfx('swoosh', at, .22); ctx.sfx('click', at + .4, .4)
    s = ppm * H / 220; hx = X0 - 70; hy = last_base - 84 * s
    svg += f'<g id="{p}-hum">{fig(p, hx, hy, s, sw=max(5.0, 6.5) / max(s, .25) * .5)}</g><text x="{hx}" y="{last_base + 26:.0f}" text-anchor="middle" class="tbl" style="font-size:12px">{esc(hl.upper())} {H:g} M</text>'
    js.append(f"pose('{p}',{hx},{hy:.1f},{s:.3f},{{aL:12,aR:-12,lL:4,lR:-4}});")
    return svg, js

def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a; js = []; svg = ''; extra = ''
    kick = ctx.p('kicker', '')
    if v == 'size_chart':
        svg, js = size_chart(ctx)
    elif v == 'lineup':
        its = ctx.p('items', []); n = len(its); w = 1100 / max(n, 1); st = ctx.p('stagger', .12)
        for k, it in enumerate(its):
            sh = it.get('shape', 'croc'); cw = w * .86; sc = cw / 1000; base = 440 if hr(sh) < .3 else 470
            x = 90 + k * w + (w - cw) / 2
            svg += (f'<g id="{p}-l{k}"><g transform="translate({x:.0f},{base}) scale({sc:.4f})">{shape_svg(sh, GOLD, 3 / sc * .9)}</g>'
                    f'<text x="{x + cw / 2:.0f}" y="{base + 40}" text-anchor="middle" class="tbl" style="font-size:13px">{esc(it.get("name", "").upper())}</text></g>')
            js.append(f"tl.fromTo('#{p}-l{k}',{{opacity:0}},{{opacity:1,duration:.3}},{T + st * k:.3f});")
            if it.get('fade_at') is not None:
                fa = ctx.t(it['fade_at']); js.append(f"tl.to('#{p}-l{k}',{{opacity:.12,duration:.35}},{fa:.3f});"); ctx.sfx('tick', fa, .3)
    elif v == 'footprints':
        pa = ctx.t(ctx.p('prints_at'), .3); wy = 560
        svg += water(p, wy, .75)
        pr = '<path d="M0,40 C-14,36 -18,20 -10,4 L-34,-40 C-38,-50 -26,-54 -20,-46 L-2,-14 L0,-62 C0,-72 14,-72 14,-62 L12,-14 L30,-46 C36,-54 48,-50 44,-40 L20,4 C28,20 22,36 10,40 Z" fill="#10171b" stroke="#f6efe0" stroke-width="3.5" stroke-linejoin="round"/>'
        for k in range(5):
            x = 170 + k * 230; y = 300 + (40 if k % 2 else -20)
            svg += f'<g id="{p}-f{k}" transform="translate({x},{y}) rotate(80) scale(1.25)" opacity="0">{pr}</g>'
            js.append(f"tl.fromTo('#{p}-f{k}',{{opacity:0}},{{opacity:1,duration:.15}},{pa + .32 * k:.3f});"); ctx.sfx('thud_soft', pa + .32 * k, .25)
        lab = ctx.p('label', '')
        if lab: svg += f'<text x="640" y="{wy + 70}" text-anchor="middle" class="tbl" style="font-size:15px">{esc(lab)}</text>'
    elif v == 'heads':
        mode = ctx.p('mode', 'nostrils'); sc = .78
        def head(y, nm, nost, col):
            d = ('<path d="M0,0 C20,-70 120,-100 250,-100 C330,-100 380,-112 430,-120 C470,-126 520,-112 560,-100 C700,-80 880,-56 1000,-36 C1010,-20 990,-6 960,-4 C800,6 520,14 300,26 C170,30 60,30 0,0 Z"/>'
                 f'<circle cx="470" cy="-104" r="11" class="eye"/>')
            bump = '<path d="M520,-104 C540,-142 600,-142 618,-100" />' if nost == 'eyes' else ''
            return (f'<g transform="translate(150,{y}) scale({sc})"><g {_F} stroke="{col}" stroke-width="4" class="shp">{bump}{d}'
                    '<path d="M300,20 l10,18 l10,-18 M400,16 l10,18 l10,-18 M500,12 l10,18 l10,-18 M600,8 l10,18 l10,-18 M700,4 l10,18 l10,-18 M800,0 l10,18 l10,-18" fill="none" stroke-width="5"/></g></g>'
                    f'<text x="150" y="{y + 70}" class="tbl" style="font-size:15px">{esc(nm)}</text>')
        svg += head(250, 'PHYTOSAUR', 'eyes', GOLD) + head(520, 'CROCODILE', 'tip', WARM)
        if mode == 'nostrils':
            na = ctx.t(ctx.p('nostril_at'), .6); ta = ctx.t(ctx.p('tip_at'), 1.6)
            c1x, c1y = 150 + 569 * sc, 250 - 128 * sc; c2x, c2y = 150 + 985 * sc, 520 - 40 * sc
            svg += (f'<circle id="{p}-c1" cx="{c1x:.0f}" cy="{c1y:.0f}" r="44" fill="none" stroke="{GOLD}" stroke-width="4" opacity="0"/><text id="{p}-t1" x="{c1x + 60:.0f}" y="{c1y - 30:.0f}" class="itsv" style="font-size:36px" opacity="0">nostrils</text>'
                    f'<circle id="{p}-c2" cx="{c2x:.0f}" cy="{c2y:.0f}" r="40" fill="none" stroke="{GOLD}" stroke-width="4" opacity="0"/><text id="{p}-t2" x="{c2x - 20:.0f}" y="{c2y - 56:.0f}" text-anchor="end" class="itsv" style="font-size:36px" opacity="0">tip of the snout</text>')
            for k, a_ in ((1, na), (2, ta)):
                js.append(f"tl.fromTo('#{p}-c{k}',{{opacity:0,scale:1.6,svgOrigin:'{(c1x if k == 1 else c2x):.0f} {(c1y if k == 1 else c2y):.0f}'}},{{opacity:1,scale:1,duration:.3,ease:'power2.out'}},{a_:.3f});fadeIn('#{p}-t{k}',{a_ + .15:.3f},.4);")
                ctx.sfx('click', a_, .5)
        else:
            la = ctx.t(ctx.p('line_at'), .8)
            svg += f'<g id="{p}-neq" opacity="0"><text x="1090" y="430" text-anchor="middle" class="cg" style="font-size:150px;fill:{GOLD}">&#8800;</text></g>'
            js.append(f"tl.fromTo('#{p}-neq',{{opacity:0,scale:1.4,svgOrigin:'1090 380'}},{{opacity:1,scale:1,duration:.3}},{la:.3f});"); ctx.sfx('thud', la, .5)
    elif v == 'count':
        n = int(ctx.p('n', 7)); st = ctx.p('stagger', .16); na = ctx.t(ctx.p('number_at'), .3)
        shp = ['croc', 'slim', 'croc', 'amphibian', 'slim', 'croc', 'monitor', 'croc', 'slim']
        lens = [1.0, .8, .6, .9, .7, .5, .75, .65, .85]
        for k in range(n):
            col_ = k % 4; row = k // 4; w = 250 * lens[k % 9]; x = 110 + col_ * 270 + (250 - w) / 2; y = 330 + row * 190
            sh = shp[k % 9] if shp[k % 9] != 'monitor' else 'croc'
            svg += f'<g id="{p}-c{k}" opacity="0"><g transform="translate({x:.0f},{y}) scale({w / 1000:.4f})">{shape_svg(sh, GOLD if k else WARM, 3 / (w / 1000) * .9)}</g></g>'
            js.append(f"tl.fromTo('#{p}-c{k}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.3}},{na - .2 + st * k:.3f});"); ctx.sfx('tick', na - .2 + st * k, .3)
        svg += f'<text id="{p}-n" x="1120" y="560" text-anchor="middle" class="cg" style="font-size:190px;fill:{WARM}" opacity="0">{n}</text>'
        js.append(f"tl.fromTo('#{p}-n',{{opacity:0}},{{opacity:1,duration:.5}},{na + st * n:.3f});"); ctx.sfx('thud', na + st * n, .6)
        lab = ctx.p('label', '')
        if lab: svg += f'<text x="640" y="660" text-anchor="middle" class="tbl" style="font-size:14px">{esc(lab)}</text>'
    elif v in ('tooth_banana', 'teeth'):
        aa = ctx.t(ctx.p('a_at'), .2); ba = ctx.t(ctx.p('b_at'), .8)
        if v == 'tooth_banana':
            cm = 24; y0 = 560; x_r = 250
            rul = f'<line x1="{x_r}" y1="{y0}" x2="{x_r}" y2="{y0 - 20 * cm}" stroke="{GOLD}" stroke-width="2"/>'
            for c in range(0, 21):
                L_ = 18 if c % 5 == 0 else 9
                rul += f'<line x1="{x_r - L_}" y1="{y0 - c * cm}" x2="{x_r}" y2="{y0 - c * cm}" stroke="{GOLD}" stroke-width="1.5"/>'
                if c % 5 == 0: rul += f'<text x="{x_r - 28}" y="{y0 - c * cm + 5}" text-anchor="end" class="tbl" style="font-size:13px;letter-spacing:.05em">{c}</text>'
            rul += f'<text x="{x_r - 28}" y="{y0 - 21 * cm}" text-anchor="end" class="tbl" style="font-size:13px">CM</text><line x1="{x_r}" y1="{y0}" x2="1100" y2="{y0}" stroke="{SOFT}" stroke-opacity=".4"/>'
            H_ = 18 * cm
            tooth = (f'<g id="{p}-a" opacity="0"><path d="M470,{y0} C440,{y0 - H_ * .45} 470,{y0 - H_ * .85} 520,{y0 - H_} C570,{y0 - H_ * .85} 600,{y0 - H_ * .45} 570,{y0} Z" fill="#1a2429" stroke="{WARM}" stroke-width="4"/>'
                     f'<path d="M455,{y0 - H_ * .35} C495,{y0 - H_ * .32} 545,{y0 - H_ * .32} 585,{y0 - H_ * .35}" fill="none" stroke="{WARM}" stroke-opacity=".5" stroke-width="3"/>'
                     f'<text x="520" y="{y0 + 40}" text-anchor="middle" class="tbl" style="font-size:14px">DEINOSUCHUS TOOTH</text></g>')
            ban = (f'<g id="{p}-b" opacity="0"><path d="M800,{y0} C740,{y0 - H_ * .3} 735,{y0 - H_ * .75} 770,{y0 - H_} L790,{y0 - H_ + 6} C775,{y0 - H_ * .7} 800,{y0 - H_ * .3} 850,{y0 - 6} Z" fill="#1a2429" stroke="{GOLD}" stroke-width="4"/>'
                   f'<path d="M770,{y0 - H_} l-6,-16 l18,4 Z" fill="{GOLD}"/><text x="790" y="{y0 + 40}" text-anchor="middle" class="tbl" style="font-size:14px">BANANA · ABOUT 18 CM</text></g>')
            svg += rul + tooth + ban
        else:
            y0 = 520; H_ = 330
            cone = (f'<g id="{p}-b" opacity="0"><path d="M780,{y0} C770,{y0 - H_ * .6} 820,{y0 - H_ * .95} 850,{y0 - H_} C880,{y0 - H_ * .95} 930,{y0 - H_ * .6} 920,{y0} Z" fill="#1a2429" stroke="{WARM}" stroke-width="4"/>'
                    f'<text x="850" y="{y0 + 44}" text-anchor="middle" class="tbl" style="font-size:14px">{esc(ctx.p("b_label", "OUR CROC: ROUND CONE"))}</text></g>')
            ser = ''.join(f'l7,-4 l-3,-8 ' for _ in range(18))
            blade = (f'<g id="{p}-a" opacity="0"><path d="M300,{y0} C330,{y0 - H_ * .5} 380,{y0 - H_ * .9} 470,{y0 - H_} C455,{y0 - H_ * .7} 470,{y0 - H_ * .35} 500,{y0} Z" fill="#1a2429" stroke="{GOLD}" stroke-width="4"/>'
                     f'<path d="M470,{y0 - H_} C455,{y0 - H_ * .7} 470,{y0 - H_ * .35} 500,{y0}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="3 6"/>'
                     f'<text x="400" y="{y0 + 44}" text-anchor="middle" class="tbl" style="font-size:14px">{esc(ctx.p("a_label", "QUINKANA: FLAT BLADE, SERRATED"))}</text></g>')
            svg += blade + cone
        js.append(f"tl.fromTo('#{p}-a',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5}},{aa:.3f});tl.fromTo('#{p}-b',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5}},{ba:.3f});")
        ctx.sfx('click', aa, .4); ctx.sfx('click', ba, .4)
    elif v == 'debate':
        aa = ctx.t(ctx.p('a_at'), .2); ba = ctx.t(ctx.p('b_at'), 1.2); wy = 470
        svg += f'<line x1="640" y1="110" x2="640" y2="650" stroke="{GOLD}" stroke-opacity=".5" stroke-width="2"/>'
        svg += (f'<rect x="40" y="{wy}" width="560" height="110" fill="#2e5566" fill-opacity=".35"/><rect x="680" y="{wy - 170}" width="560" height="280" fill="#2e5566" fill-opacity=".35"/>'
                f'<path d="M40,{wy} H600" stroke="{SOFT}" stroke-width="3" stroke-dasharray="14 10"/><path d="M680,{wy - 170} H1240" stroke="{SOFT}" stroke-width="3" stroke-dasharray="14 10"/>')
        svg += f'<g id="{p}-a" opacity="0"><g transform="translate(70,{wy + 60}) scale(.5)">{shape_svg("spino", GOLD, 6)}</g><text x="320" y="610" text-anchor="middle" class="lblm" style="font-size:18px">{esc(ctx.p("a_label", "WADER?"))}</text></g>'
        svg += f'<g id="{p}-b" opacity="0"><g transform="translate(1225,560) scale(-.5,.5)"><g transform="rotate(10 500 -200)">{shape_svg("spino", GOLD, 6)}</g></g><text x="960" y="610" text-anchor="middle" class="lblm" style="font-size:18px">{esc(ctx.p("b_label", "SWIMMER?"))}</text></g>'
        svg += f'<text id="{p}-q" x="640" y="400" text-anchor="middle" class="cg" style="font-size:170px;fill:{ITAL};paint-order:stroke;stroke:#0b1013;stroke-width:14px" opacity="0">?</text>'
        js.append(f"fadeIn('#{p}-a',{aa:.3f},.4);fadeIn('#{p}-b',{aa + .5:.3f},.4);tl.fromTo('#{p}-q',{{opacity:0,scale:1.5,svgOrigin:'640 340'}},{{opacity:1,scale:1,duration:.35}},{ba:.3f});")
        ctx.sfx('click', aa, .4); ctx.sfx('tok', ba, .5)
    if kick: extra += f'<div class="jo gold" style="position:absolute;left:90px;top:48px;font-size:16px">{rich(kick)}</div>'
    note = ctx.p('note')
    if note:
        extra += f'<div id="{p}-note" class="cg op0" style="position:absolute;right:80px;top:40px;font-size:64px;color:{ITAL}"><i>{rich(note)}</i></div>'
        js.append(f"write('#{p}-note',{ctx.t(ctx.p('note_at'), 1.0):.3f},.6);"); ctx.sfx('tok', ctx.t(ctx.p('note_at'), 1.0), .5)
    line = ctx.p('line')
    if line and v != 'heads':
        extra += f'<div id="{p}-line" class="cg op0" style="position:absolute;left:0;width:1280px;text-align:center;top:640px;font-size:44px;color:{ITAL}"><i>{rich(line)}</i></div>'
        js.append(f"write('#{p}-line',{ctx.t(ctx.p('line_at'), 1.0):.3f},.6);")
    elif line:
        extra += f'<div id="{p}-line" class="cg op0" style="position:absolute;right:60px;width:420px;text-align:center;top:470px;font-size:40px;color:{ITAL};white-space:normal"><i>{rich(line)}</i></div>'
        js.append(f"write('#{p}-line',{ctx.t(ctx.p('line_at'), 1.0) + .2:.3f},.6);")
    js.append(f"kb('#{p}-kb',{T:.3f},{ctx.b:.3f},1.0,1.035,'50% 55%');")
    ctx.js.append('\n'.join(js))
    return dict(html=ctx.shot_div(f'<div class="card"></div><div id="{p}-kb" class="kb"><svg width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg>{extra}</div>', 'stick'), css=CSS)
