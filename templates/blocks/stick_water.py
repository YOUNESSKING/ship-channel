from .common import *
META = dict(name='stick_water', about='Stick figure treading water, then a chain of beats in one shot: "you" label, crossed-out items (NO BOAT), measured distance to shore (rule 9, 10).',
  variants=['sea', 'ice'],
  params={'beats': 'list of beats: {"kind":"you","label":"you","label_at":T} | {"kind":"items","at":T,"items":[{"icon":"boat","label":"NO BOAT","at":T}]} | '
                   '{"kind":"distance","at":T,"label":"100 yards","label_at":T}. "at" = when the beat (a cut + zoom) starts. Icons: boat, wetsuit, lifering, bottle, flame, phone, fish, rope, hand ...',
          'cross': 'items: draw a gold X on each item 0.3 s later (default true)', 'shore_label': 'text on the pale shore (default "ICE")', 'shore': '"palm" (sea default: warm island) or "ice" (pale cold shore with shore_label; ice default). Use "ice" for any cold or inland scene: no palm trees in the Ice Age'})
def _ipos(n): return {1: [940], 2: [300, 980], 3: [240, 440, 1040]}[n]   # one item sits beside the figure, not on its head
def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a; D = ctx.dur; B = ctx.b
    beats = ctx.p('beats') or [{'kind': 'you', 'label': 'you'}]
    cross = ctx.p('cross', True)
    ats = [ctx.t(b.get('at'), 0.0) if i else T for i, b in enumerate(beats)] + [B]
    parts = []; js = []
    shore_lab = ctx.p('shore_label', 'ICE')
    if ctx.p('shore', 'palm' if v == 'sea' else 'ice') == 'palm':
        shore = (f'<g id="{p}-shore" opacity="0"><path d="M1010,470 C1060,440 1180,436 1300,448 L1300,520 L1010,520 Z" fill="#2a2d30" stroke="#e9dcc0" stroke-width="3"/>'
                 '<g stroke="#e9dcc0" stroke-width="5" stroke-linecap="round" fill="none"><path d="M1170,446 C1176,400 1168,370 1160,350"/><path d="M1160,350 q-40,-8 -62,22 M1160,350 q-10,-44 -52,-46 M1160,350 q30,-36 66,-26 M1160,350 q44,0 60,36"/></g></g>')
    else:
        shore = (f'<g id="{p}-shore" opacity="0"><path d="M1000,474 L1040,420 L1130,412 L1190,430 L1300,424 L1300,520 L1000,520 Z" fill="#cfd8dc" fill-opacity=".9" stroke="#e9dcc0" stroke-width="3"/>'
                 f'<text x="1150" y="470" text-anchor="middle" class="lblm" style="fill:#16262b;stroke:none">{esc(shore_lab)}</text></g>')
    items_html = ''; dist_html = ''; you_html = ''
    hid = []
    js.append(f"""pose('{p}',640,520,1.15,{{aL:78,aR:-78,lL:10,lR:-10}});
flail('{p}',640,520,1.15,{T:.3f},{D:.3f},72,104,.34);
bob('#{p}-figw',{T:.3f},{D:.3f},9,.5);drift('#{p}-water',{T:.3f},{D:.3f},-220);
gsap.set('#{p}-kb',{{scale:1,transformOrigin:'640px 440px'}});""")
    for i, b in enumerate(beats):
        a, e = ats[i], ats[i + 1]; kind = b['kind']
        if kind == 'you':
            lab = b.get('label', 'you')
            you_html += (f'<g id="{p}-you{i}" opacity="0"><text x="640" y="262" text-anchor="middle" class="itsv" style="font-size:56px">{esc(lab)}</text>'
                         f'<path d="M640,282 v54 M640,336 l-14,-18 M640,336 l14,-18" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" fill="none"/></g>')
            hid.append(f'#{p}-you{i}')
            js.append(f"tl.to('#{p}-kb',{{scale:1.05,duration:{e - a:.3f},ease:'none',transformOrigin:'640px 440px'}},{a:.3f});" if i == 0 else
                      f"tl.set('#{p}-kb',{{scale:1,transformOrigin:'640px 440px'}},{a:.3f});tl.to('#{p}-kb',{{scale:1.05,duration:{e - a:.3f},ease:'none',transformOrigin:'640px 440px'}},{a:.3f});")
            js.append(f"pop('#{p}-you{i}',{ctx.t(b.get('label_at'), (a - T) + .3):.3f},.3);tl.set('#{p}-you{i}',{{opacity:0}},{e:.3f});")
            ctx.sfx('splash', a, .35)
        elif kind == 'items':
            its = b['items']; xs = _ipos(len(its)); grp = []
            js.append(f"tl.set('#{p}-kb',{{scale:1.3,transformOrigin:'640px 440px'}},{a:.3f});")
            for j, (it, x) in enumerate(zip(its, xs)):
                ia = ctx.t(it.get('at'), (a - T) + .3 + .8 * j)
                items_html += (f'<g id="{p}-i{i}_{j}" transform="translate({x},330)"><g id="{p}-i{i}_{j}in" opacity="0">{icon(it["icon"])}</g></g>'
                               + (xmark(f'{p}-x{i}_{j}', x, 330) if cross else '')
                               + f'<text id="{p}-l{i}_{j}" x="{x}" y="440" text-anchor="middle" class="lblm" opacity="0">{esc(it.get("label", ""))}</text>')
                hid += [f'#{p}-x{i}_{j}'] if cross else []
                js.append(f"pop('#{p}-i{i}_{j}in',{ia - .1:.3f},.22,{{icon:true,from:.2,svgOrigin:'0 0'}});fadeIn('#{p}-l{i}_{j}',{ia:.3f},.2);")
                if cross:
                    js.append(f"pop('#{p}-x{i}_{j}',{ia + .3:.3f},.14,{{icon:true,from:.3,svgOrigin:'{x} 330'}});")
                    ctx.sfx('click', ia + .3, .6)
                grp += [f'#{p}-i{i}_{j}', f'#{p}-x{i}_{j}', f'#{p}-l{i}_{j}'] if cross else [f'#{p}-i{i}_{j}', f'#{p}-l{i}_{j}']
            js.append(f"tl.set({grp!r},{{opacity:0}},{e:.3f});")
        elif kind == 'distance':
            lab = b.get('label', '100 yards')
            dist_html += (f'<g id="{p}-dist{i}" opacity="0"><line x1="380" y1="400" x2="1000" y2="400" stroke="{GOLD}" stroke-width="2" stroke-dasharray="3 12" stroke-linecap="round"/>'
                          f'<path d="M390,400 l20,-9 v18 Z M990,400 l-20,-9 v18 Z" fill="{GOLD}"/><text x="690" y="378" text-anchor="middle" class="itsv" style="font-size:48px">{esc(lab)}</text></g>')
            hid.append(f'#{p}-dist{i}')
            js.append(f"tl.set('#{p}-kb',{{scale:1,transformOrigin:'640px 440px'}},{a:.3f});tl.set('#{p}-figw',{{x:-380}},{a:.3f});"
                      f"tl.to('#{p}-kb',{{scale:1.05,duration:{e - a:.3f},ease:'none',transformOrigin:'640px 440px'}},{a:.3f});tl.set('#{p}-shore',{{opacity:1}},{a:.3f});"
                      f"pop('#{p}-dist{i}',{ctx.t(b.get('label_at'), (a - T) + .5):.3f},.3);")
            ctx.sfx('splash', a + .5, .25)
    svg = (f'<g id="{p}-all"><g id="{p}-figw">{fig(p, 640, 520, 1.15)}</g>{water(p, 458)}{shore}{dist_html}{you_html}{items_html}</g>')
    js.insert(1, f"hidden({hid!r});hidden('#{p}-shore');" if hid else f"hidden('#{p}-shore');")
    html = ctx.shot_div(f'<div id="{p}-kb" class="kb"><svg width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg></div>', 'stick')
    ctx.js.append('\n'.join(js))
    return dict(html=html)
