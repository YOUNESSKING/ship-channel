from .common import *
META = dict(name='map_clip', about='Plays a pre-baked map video (any mp4) and, if you want, adds the style C overlays: pin ring + place name, date line, sea-level gauge (rules 1, 18-21).',
  variants=['baked', 'labeled', 'gauge'],
  params={'pin': '{"x":640,"y":330,"track":[[t,x,y],...]}  pin position in the 1280x720 picture (labeled variant); track = positions over the clip seconds when the bake moves (Video 02 map jsons)', 'name': 'place name, e.g. "North Atlantic"', 'name_at': 'when the pin + name appear (time spec)',
          'date': 'bottom line, e.g. "LAST GLACIAL MAXIMUM · SEA LEVEL -120 M" (every variant)', 'date_at': 'when the bottom line shows',
          'gauge': '{"from":0,"to":-120,"at":"@four","dur":1.7,"x":930,"y":120,"label_ft":"(-400 ft)"}  sea-level gauge (gauge variant)',
          'credits': 'small credits line bottom right (default none; maps baked by the map-kit already have it)', 'pins': '[{"x":246,"y":240,"x0":251,"y0":245,"label":"","at":T}] many small gold pins that drift with the bake (pins_dur = bake seconds)', 'pins_dur': 'seconds the pins take to drift from x0,y0 to x,y (default: the shot)',
          'zoom': '[from,to] slow zoom, default [1.0,1.0] (the baked map already moves)',
          'measure': '{"from":{"x":640,"y":210},"to":{"x":640,"y":520},"label":"1,000 km","at":"@thousand","dur":0.9,"label_side":"right"}  gold measure bar that draws between two points on a word (gap T8)',
          'inset': '{"pin":{"lat":20,"lon":38.5},"corner":"tl"|"tr"|"bl"|"br","w":300,"at":0.3,"label":"ICE AGE ICE SHEETS"}  small world map with the Ice Age ice sheets and a gold pin on the place (rule 18, gap T10); for places far from the ice',
          'polar': '{"center":[640,360],"two_r":1011,"pin":{"lat":-62,"lon":-40},"pin_name":"","rings":[{"lat":-60,"label":"TODAY\'S WINTER EDGE","at":T,"label_lon":90},{"lat":-50,"label":"ICE AGE EDGE","at":T,"grow_from":-60,"dur":1.6}]}  overlays for the south-polar stereographic bake (gap T9): rings drawn by latitude (dashed gold), pin by lat/lon. two_r = 2*R in frame pixels (kit: 2170.5 at 2880 px wide, so about 1011 at zoom 1.05 in a 1280 frame)'})
def pin_svg(p, x, y):
    return (f'<g id="{p}-pin" opacity="0"><circle id="{p}-pr2" cx="{x}" cy="{y}" r="34" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y}" r="22" fill="rgba(0,0,0,.45)" stroke="{GOLD}" stroke-width="3"/><circle cx="{x}" cy="{y}" r="5.5" fill="{GOLD}"/></g>')
def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a
    z = ctx.p('zoom', [1.0, 1.0])
    h = ctx.video((z[0], z[1], '50% 50%') if z[0] != z[1] else None)
    parts = ''; js = []
    cred = ctx.p('credits'); defs = {}
    ms = ctx.p('measure'); ins = ctx.p('inset'); pol = ctx.p('polar')
    if cred: parts += f'<div class="jo" style="position:absolute;right:30px;bottom:18px;font-size:11px;letter-spacing:.06em;text-transform:none;opacity:.8">{esc(cred)}</div>'
    if v == 'labeled':
        pin = ctx.p('pin', {'x': 640, 'y': 330}); name = ctx.p('name', ''); nat = ctx.t(ctx.p('name_at'), .5)
        nm_y = pin['y'] + 48 if pin['y'] < 520 else pin['y'] - 150
        pw = (f'<svg width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;left:0;top:0">{pin_svg(p, pin["x"], pin["y"])}</svg>'
              + block(f'{p}-name', 0, nm_y, 1280, f'<div class="cg" style="font-size:48px;letter-spacing:.08em;text-transform:uppercase;text-shadow:0 2px 20px rgba(0,0,0,.85)">{rich(name)}</div><div class="gr" style="margin-top:10px"></div>'))
        tr = pin.get('track')
        if tr:   # the bake moves: the pin (and its name) follow the tracked position; times are seconds of the clip, from clip "in"
            cin = float(ctx.clip.get('in', 0.0)); fx, fy = pin['x'], pin['y']
            pts = [(float(q[0]) - cin, float(q[1]) - fx, float(q[2]) - fy) for q in tr if float(q[0]) >= cin - 1e-6] or [(0.0, 0.0, 0.0)]
            js.append(f"gsap.set('#{p}-pw',{{x:{pts[0][1]:.1f},y:{pts[0][2]:.1f}}});")
            for (t0, x0_, y0_), (t1, x1_, y1_) in zip(pts, pts[1:]):
                if t1 - t0 > 1e-3: js.append(f"tl.to('#{p}-pw',{{x:{x1_:.1f},y:{y1_:.1f},duration:{t1 - t0:.3f},ease:'none'}},{T + t0:.3f});")
        parts += f'<div id="{p}-pw" style="position:absolute;left:0;top:0;width:1280px;height:720px">{pw}</div>'
        js.append(f"pop('#{p}-pin',{nat - .2:.3f},.5);tl.fromTo('#{p}-pr2',{{scale:1,transformOrigin:'{pin['x']}px {pin['y']}px'}},{{scale:1.5,opacity:0,duration:1.4,ease:'power1.out',repeat:2,transformOrigin:'{pin['x']}px {pin['y']}px'}},{nat:.3f});"
                  f"write('#{p}-name',{nat:.3f},.9);")
        ctx.sfx('title', nat, .7)
    pins = ctx.p('pins')
    if pins:   # many small pins (e.g. the 12 rivers on the world map); each drifts from (x0,y0) to (x,y) over pins_dur seconds
        pdur = float(ctx.p('pins_dur', ctx.dur)); sv = ''
        for k, q in enumerate(pins):
            x0_, y0_ = q.get('x0', q['x']), q.get('y0', q['y']); pa = ctx.t(q.get('at'), .3 + .15 * k)
            sv += (f'<g id="{p}-q{k}" opacity="0"><circle cx="0" cy="0" r="16" fill="none" stroke="{GOLD}" stroke-opacity=".45" stroke-width="2"/><circle cx="0" cy="0" r="7" fill="{GOLD}" stroke="#000" stroke-width="1.5"/>'
                   + (f'<text x="0" y="-22" text-anchor="middle" class="lblm" style="font-size:13px;letter-spacing:.12em">{esc(q["label"])}</text>' if q.get('label') else '') + '</g>')
            js.append(f"gsap.set('#{p}-q{k}',{{x:{x0_},y:{y0_}}});tl.to('#{p}-q{k}',{{x:{q['x']},y:{q['y']},duration:{pdur:.3f},ease:'none'}},{T:.3f});tl.fromTo('#{p}-q{k}',{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:.25,ease:'power2.out'}},{pa:.3f});")
            ctx.sfx('tick', pa, .3)
        parts += f'<svg width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;left:0;top:0">{sv}</svg>'
    if ctx.p('date'):
        dat = ctx.t(ctx.p('date_at'), 1.5)
        parts += (f'<div id="{p}-date" class="op0" style="position:absolute;left:290px;width:700px;top:628px;text-align:center;border-top:1px solid {GOLD};padding-top:12px">'
                  f'<span class="jo" style="font-size:15px;letter-spacing:.28em">{rich(ctx.p("date"))}</span></div>')
        js.append(f"write('#{p}-date',{dat:.3f},.9);")
    if v == 'gauge':
        g = ctx.p('gauge', {}); gx = g.get('x', 930); gy = g.get('y', 150); frm = g.get('from', 0); to = g.get('to', -120); dur = g.get('dur', 1.7)
        gat = ctx.t(g.get('at'), .5); lab_ft = g.get('label_ft', ''); span = 250
        import re as _re
        _m = _re.search(r'(\d+)', lab_ft or ''); ft_full = int(_m.group(1)) if _m else 0   # feet shown at the final depth; scaled during the count
        flat = (frm == to)      # already at the final level: the marker sits at the bottom, scale runs 0 -> |to|
        t0_ = 0 if flat else frm
        ticks = ''.join(f'<line x1="0" y1="{span*(i/3):.0f}" x2="-12" y2="{span*(i/3):.0f}" stroke="{WARM}" stroke-width="1.5"/><text x="-22" y="{span*(i/3)+5:.0f}" text-anchor="end" class="tbl" style="font-size:13px;letter-spacing:.1em">{abs(round(t0_ + (to-t0_)*(i/3)))}</text>' for i in range(4))
        parts += (f'<svg width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;left:0;top:0"><g id="{p}-g" transform="translate({gx},{gy})" opacity="0">'
                  f'<text x="0" y="-46" text-anchor="middle" class="tbl" style="font-size:12px">SEA LEVEL</text>'
                  f'<rect x="-5" y="0" width="10" height="{span}" rx="5" fill="rgba(0,0,0,.45)" stroke="{WARM}" stroke-opacity=".6" stroke-width="1.5"/>'
                  f'<rect id="{p}-gf" x="-3" y="0" width="6" height="0" rx="3" fill="#6f95a6" fill-opacity=".8"/>{ticks}'
                  f'<g id="{p}-gm"><line x1="-16" y1="0" x2="190" y2="0" stroke="{GOLD}" stroke-width="1.5"/><text id="{p}-gt" x="24" y="-10" class="cg" style="font-size:28px;fill:{WARM};paint-order:stroke;stroke:rgba(0,0,0,.85);stroke-width:6px;stroke-linejoin:round"></text></g></g></svg>')
        fmt = f"(v)=>(Math.round(v)===0?'':'&minus;')+Math.abs(Math.round(v))+' m '+'<i style=\"font-size:21px;color:{ITAL}\">{lab_ft}</i>'"
        js.append(f"""tl.fromTo('#{p}-g',{{opacity:0}},{{opacity:1,duration:.5}},{gat - .4:.3f});
gsap.set('#{p}-gm',{{y:0}});
(function(){{const o={{v:{frm}}},el=document.getElementById('{p}-gt'),gm=document.getElementById('{p}-gm'),gf=document.getElementById('{p}-gf');
 const upd=()=>{{const f={'1' if flat else f'(o.v-({frm}))/({to}-({frm}))'};gm.setAttribute('transform','translate(0,'+({span}*f)+')');gf.setAttribute('height',{span}*f);const t=Math.abs(Math.round(o.v));const ft={ft_full};const ftv=Math.round(ft*t/Math.max(1,Math.abs({to}),Math.abs({frm}))/10)*10;el.innerHTML=(t===0?'':'&minus;')+t+' m '+({'true' if ft_full else 'false'}?'<tspan style="font-size:20px;font-style:italic;fill:{ITAL}">('+(ftv===0?'':'&minus;')+ftv+' ft)</tspan>':'');}};
 upd();tl.fromTo(o,{{v:{frm}}},{{v:{to},duration:{dur},ease:'power2.inOut',immediateRender:false,onUpdate:upd}},{gat:.3f});}})();""")
        ctx.sfx('swoosh', gat, .3)
    if ms:
        a_, b_ = ms['from'], ms['to']; mat = ctx.t(ms.get('at'), .5); md = ms.get('dur', .9); mx, my = (a_['x'] + b_['x']) / 2, (a_['y'] + b_['y']) / 2
        import math
        L_ = math.hypot(b_['x'] - a_['x'], b_['y'] - a_['y']) or 1; nx, ny = -(b_['y'] - a_['y']) / L_, (b_['x'] - a_['x']) / L_
        tk = lambda q: f'<line x1="{q["x"]-nx*14:.1f}" y1="{q["y"]-ny*14:.1f}" x2="{q["x"]+nx*14:.1f}" y2="{q["y"]+ny*14:.1f}" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>'
        side = ms.get('label_side', 'right'); lx = mx + (30 if side == 'right' else -30 if side == 'left' else 0); ly = my + (8 if side in ('right', 'left') else -26 if side == 'top' else 56)
        anc = 'start' if side == 'right' else 'end' if side == 'left' else 'middle'
        parts += (f'<svg width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;left:0;top:0"><g id="{p}-ms" opacity="0">'
                  f'<path id="{p}-msl" d="M{a_["x"]},{a_["y"]} L{b_["x"]},{b_["y"]}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" stroke="{GOLD}" stroke-width="3.5" stroke-linecap="round" fill="none"/>'
                  f'<g id="{p}-mse" opacity="0">{tk(a_)}{tk(b_)}</g>'
                  f'<text id="{p}-mst" x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anc}" class="itsv" style="font-size:50px;paint-order:stroke;stroke:rgba(0,0,0,.85);stroke-width:7px;stroke-linejoin:round" opacity="0">{rich_svg(ms.get("label", ""))}</text></g></svg>')
        js.append(f"gsap.set('#{p}-ms',{{opacity:1}});tl.fromTo('#{p}-msl',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{md},ease:'power2.inOut'}},{mat:.3f});"
                  f"fadeIn('#{p}-mse',{mat:.3f},.2);fadeIn('#{p}-mst',{mat + md * .6:.3f},.5);")
        ctx.sfx('swoosh', mat, .3); ctx.sfx('click', mat + md, .45)
    if ins:
        import json as _j, os as _o
        W_ = _j.load(open(_o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), 'lib', 'world_inset.json')))
        defs['wi'] = (f'<path id="wi-land" d="{W_["land"]}"/>' + ''.join(f'<path id="wi-ice-{k}" d="{v}"/>' for k, v in W_['ice'].items()))
        w_ = ins.get('w', 300); sc_ = w_ / W_['w']; h_ = W_['h'] * sc_; cn = ins.get('corner', 'tl'); mg = 34
        ix = mg if cn in ('tl', 'bl') else 1280 - mg - w_; iy = mg + 18 if cn in ('tl', 'tr') else 720 - mg - h_ - 30
        pin_ = ins['pin']; ppx = (pin_['lon'] + 180) * sc_; ppy = (W_['lat0'] - pin_['lat']) * sc_; iat = ctx.t(ins.get('at'), .3)
        lab_ = ins.get('label', 'ICE AGE ICE SHEETS · 20,000 YEARS AGO')
        parts += (f'<svg width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;left:0;top:0"><g id="{p}-in" transform="translate({ix:.0f},{iy:.0f})" opacity="0">'
                  f'<rect x="-8" y="-8" width="{w_+16:.0f}" height="{h_+16:.0f}" fill="rgba(4,9,14,.78)" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2"/>'
                  f'<g transform="scale({sc_:.4f})"><use href="#wi-land" fill="#3a444a" stroke="#6c777c" stroke-width="{.5/sc_:.2f}" stroke-opacity=".6"/>'
                  + ''.join(f'<use href="#wi-ice-{k}" fill="#dfeaf1" fill-opacity=".8"/>' for k in W_['ice']) + '</g>'
                  f'<circle id="{p}-inr" cx="{ppx:.1f}" cy="{ppy:.1f}" r="9" fill="none" stroke="{GOLD}" stroke-width="1.5" style="transform-box:fill-box;transform-origin:center"/><circle cx="{ppx:.1f}" cy="{ppy:.1f}" r="4.5" fill="{GOLD}" stroke="#000" stroke-width="1.2"/>'
                  f'<text x="{w_/2:.0f}" y="{h_+30:.0f}" text-anchor="middle" class="tbl" style="font-size:10.5px;letter-spacing:.2em">{esc(lab_)}</text></g></svg>')
        js.append(f"tl.fromTo('#{p}-in',{{opacity:0}},{{opacity:1,duration:.5}},{iat:.3f});tl.fromTo('#{p}-inr',{{scale:1,opacity:.9}},{{scale:2.2,opacity:0,duration:1.3,repeat:3,ease:'power1.out'}},{iat + .4:.3f});")
    if pol:
        import math
        cx_, cy_ = pol.get('center', [640, 360]); two_r = pol.get('two_r', 1011)
        P_ = lambda lat, lon: (cx_ + two_r * math.tan(math.radians(90 + lat) / 2) * math.sin(math.radians(lon)), cy_ - two_r * math.tan(math.radians(90 + lat) / 2) * math.cos(math.radians(lon)))
        R_ = lambda lat: two_r * math.tan(math.radians(90 + lat) / 2)
        sv = ''
        for k, rg in enumerate(pol.get('rings', [])):
            rat = ctx.t(rg.get('at'), .5); r1 = R_(rg['lat']); r0 = R_(rg['grow_from']) if 'grow_from' in rg else r1; dd = rg.get('dur', 1.6)
            sv += (f'<circle id="{p}-pr{k}" cx="{cx_}" cy="{cy_}" r="{r0:.1f}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="10 14" stroke-opacity=".9" opacity="0"/>')
            lx_, ly_ = P_(rg['lat'], rg.get('label_lon', 90))
            sv += f'<text id="{p}-prt{k}" x="{lx_+16:.0f}" y="{ly_+5:.0f}" class="tbl" style="font-size:13px" opacity="0">{esc(rg.get("label", ""))}</text>'
            js.append(f"fadeIn('#{p}-pr{k}',{rat:.3f},.5);fadeIn('#{p}-prt{k}',{rat + .3:.3f},.5);" + (f"tl.to('#{p}-pr{k}',{{attr:{{r:{r1:.1f}}},duration:{dd},ease:'power2.inOut'}},{rat:.3f});" if r0 != r1 else ''))
        if pol.get('pin'):
            px_, py_ = P_(pol['pin']['lat'], pol['pin']['lon']); sv += pin_svg(p + 'p', px_, py_)
            js.append(f"pop('#{p}p-pin',{ctx.t(pol.get('pin_at'), 1.0):.3f},.5);tl.fromTo('#{p}p-pr2',{{scale:1,transformOrigin:'{px_:.0f}px {py_:.0f}px'}},{{scale:1.5,opacity:0,duration:1.4,repeat:2,transformOrigin:'{px_:.0f}px {py_:.0f}px'}},{ctx.t(pol.get('pin_at'), 1.0):.3f});")
            if pol.get('pin_name'): sv += f'<text x="{px_+34:.0f}" y="{py_+7:.0f}" class="lblm" style="font-size:18px">{esc(pol["pin_name"])}</text>'
        parts += f'<svg width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;left:0;top:0">{sv}</svg>'
    ctx.js.append('\n'.join(js))
    return dict(html=h + (ctx.overlay(parts) if parts else ''), defs=defs)
