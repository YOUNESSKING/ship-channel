from .common import *
META = dict(name='tier_board', about='Tier board (rules 7, 43, 58). "roadmap" = the empty board with ALL chapter tiles listed by name; "drop" = the tile is dragged and dropped on the verdict word (optionally a new tier row slides in first); "final" = the finished board with a slow camera move and glowing rows / lifted tiles; "final_wide" = the finished board, whole, fixed camera.',
  variants=['roadmap', 'drop', 'final', 'final_wide'],
  params={'title': 'board title (default "How long would you last in each Ice Age ocean?")', 'tiers': 'list of [name, colour]; default Overnight/Hours/An hour/Minutes/Seconds',
          'tiles': 'roadmap: list of {"name":"North Atlantic","image":"thumb.jpg"} - every chapter, in order (image optional)',
          'placed': 'tiles already on the board: list of {"name","image","tier"}', 'reveal_at': 'roadmap: time spec of the first tile (default 0.5 s)',
          'glow': 'roadmap: {"name":"Southern Ocean","at":T} - that tile gets a gold ring and lifts on its word (join.md: the next ocean glows on "south")',
          'stagger': 'roadmap: seconds between tiles (default 0.18), or give "reveal_times": [specs]', 'reveal_times': 'roadmap: one time spec per tile',
          'tile': 'drop: {"name":"North Atlantic","image":"thumb.jpg"}', 'tier': 'drop: tier the tile lands in (e.g. "Minutes")',
          'drop_at': 'drop: time spec of the verdict word (the thud)', 'note': 'drop: small italic line next to the landed tile, e.g. "*in the water"', 'note_at': 'drop: when the note shows (default 0.5 s after the drop)', 'slot_x': 'drop: x of the landing spot (default: next free place in the row)',
          'cursor': 'drop: show the cursor (default true)', 'n_total': 'drop: total chapters, picks the compact board when more than 6 (default 5)',
          'add_tier_at': 'drop: time spec. A new tier row (the FIRST entry of "tiers", or "new_tier") slides in on top of the board at this moment, then the tile drops into it (gap T2: the "Days" row at chapter 9). Pass "tiers" with the new tier first.',
          'new_tier': 'drop: name of the tier that slides in (default: first of "tiers")',
          'verdict': 'drop: big verdict word shown on the drop (about 12 % of frame height, Cormorant, warm white, gold underline; style review 04/07)',
          'sting': 'drop: "full" = music dips out 0.8 s before the word, riser, deep hit on the word (4 key verdicts only); "thud" = deep hit only (default when verdict is set)',
          'highlight_row': 'final: tier name whose row glows gold (default none)', 'highlight_at': 'final: when the row glows (default 0.4 s)',
          'highlight_tiles': 'final: list of {"name":"Bering Sea","at":T} - the tile lifts and gets a gold ring on its word, soft click; stays lifted',
          'pan': 'final: camera move "bottom_to_top", "top_to_bottom", "focus" (stay on the highlighted row) or "none" (default: focus when a row is highlighted, else bottom_to_top)',
          'zoom': 'final: camera zoom (default 1.45)', 'focus_row': 'final: tier name to centre on when pan is "focus" (default: highlight_row)'})
LONG_OK = {'final', 'final_wide'}
TIERS = [('Overnight', '#5f7f6a'), ('Hours', '#8a9a62'), ('An hour', '#b39a55'), ('Minutes', '#b8794d'), ('Seconds', '#9a4f4a')]

def geom(n, rows=5):
    if rows >= 6: return dict(top0=48, step=68, rh=62, pool=(90, 470, 1100, 230), ts=.88 if n <= 14 else .7, lab_fs=22, ttl=16)
    if n <= 6: return dict(top0=64, step=98, rh=92, pool=(90, 582, 1100, 116), ts=.88, lab_fs=28, ttl=26)
    return dict(top0=58, step=78, rh=72, pool=(90, 456, 1100, 248), ts=.88 if n <= 14 else .7, lab_fs=24, ttl=18)

def tile(i, name, image, x, y, sc, ctx, abs_pos=True, extra=''):
    img = (ctx.asset(image) if image else '') or 'assets/icy_sea.jpg'
    return (f'<div id="{i}" class="tile" style="{extra}"><div class="ph2" style="background:url({img}) center/cover"></div><div class="cap">{esc(name)}</div></div>')

def board(ctx, g, tiers, title, placed, new_row=None, pool=True):
    p = ctx.id; rows = ''
    for i, (nm, col) in enumerate(tiers):
        rows += (f'<div id="{p}-row{i}" class="trow {p}-{"new" if i == new_row else "grp"}" style="top:{g["top0"]+i*g["step"]}px;height:{g["rh"]}px"><div class="tlabel" style="background:{col};height:{g["rh"]-2}px;font-size:{g["lab_fs"]}px">{esc(nm)}</div><div class="tzone"></div></div>')
    x0, y0, w, h = g['pool']
    out = f'<div class="tl-title" style="top:{g["ttl"]}px">{rich(title)}</div>{rows}' + (f'<div class="pool" style="left:{x0}px;top:{y0}px;width:{w}px;height:{h}px"></div>' if pool else '')
    cnt = {}
    names = [t[0].lower() for t in tiers]
    for k, t in enumerate(placed):
        r = names.index(t['tier'].lower()); n = cnt.get(r, 0); cnt[r] = n + 1
        sc = min(g['ts'], (g['rh'] - 6) / 100.0)
        x = 300 + n * (150 * sc + 8); y = g['top0'] + r * g['step'] + (g['rh'] - 100 * sc) / 2
        out += tile(f'{p}-pl{k}', t['name'], t.get('image'), x, y, sc, ctx, extra=f'left:{x:.0f}px;top:{y:.0f}px;transform:scale({sc});transform-origin:0 0')
        if r != new_row: out = out.replace(f'<div id="{p}-pl{k}" class="tile"', f'<div id="{p}-pl{k}" class="tile {p}-grp"', 1)
    return out, cnt

def build_final(ctx, tiers, title, placed):
    """Finished board: all tiles placed; camera move; a row glows; tiles lift on their words (gap T1)."""
    v = ctx.variant; p = ctx.id; T = ctx.a; B = ctx.b
    g = dict(top0=52, step=104, rh=96, pool=(0, 0, 0, 0), ts=.9, lab_fs=30, ttl=20)
    body, cnt = board(ctx, g, tiers, title, placed, None, pool=False)
    names = [t[0].lower() for t in tiers]; Hb = g['top0'] + (len(tiers) - 1) * g['step'] + g['rh']
    hr = ctx.p('highlight_row'); hat = ctx.t(ctx.p('highlight_at'), .4); hts = ctx.p('highlight_tiles', [])
    pan = ctx.p('pan') or ('none' if v == 'final_wide' else ('focus' if hr else 'bottom_to_top')); z = ctx.p('zoom', 1.45) if v == 'final' and pan != 'none' else 1.0
    js = []
    if pan != 'none':
        tx = -50 * z; lo = -(Hb * z - 700); hi = 0.0
        def ty_for(name):
            r = names.index(name.lower()); cy = g['top0'] + r * g['step'] + g['rh'] / 2; return max(lo, min(hi, 360 - cy * z))
        if pan == 'focus':
            fr = ctx.p('focus_row') or hr or tiers[-1][0]; y0 = ty_for(fr); y1 = y0 + (14 if y0 < hi - 14 else -0) 
            js.append(f"gsap.set('#{p}-cam',{{scale:{z},x:{tx:.0f},y:{y0:.0f},transformOrigin:'0 0'}});tl.to('#{p}-cam',{{y:{y1:.0f},scale:{z * 1.03:.3f},duration:{B - T:.3f},ease:'none'}},{T:.3f});")
        else:
            a_, b_ = (lo, hi) if pan == 'bottom_to_top' else (hi, lo)
            js.append(f"gsap.set('#{p}-cam',{{scale:{z},x:{tx:.0f},y:{a_:.0f},transformOrigin:'0 0'}});tl.to('#{p}-cam',{{y:{b_:.0f},duration:{(B - T):.3f},ease:'power1.inOut'}},{T:.3f});")
    else:
        js.append(f"kb('#{p}-cam',{T:.3f},{B:.3f},1.0,1.04,'50% 50%');")
    if hr:
        r = names.index(hr.lower())
        js.append(f"tl.to('#{p}-row{r}',{{borderColor:'#c9a45c',boxShadow:'0 0 0 2px #c9a45c, 0 0 28px rgba(201,164,92,.55)',duration:.5}},{hat:.3f});"
                  f"tl.to('#{p}-row{r} .tzone',{{backgroundColor:'rgba(201,164,92,.16)',duration:.5}},{hat:.3f});")
        ctx.sfx('tick', hat, .3)
    sc = min(g['ts'], (g['rh'] - 6) / 100.0)
    for h_ in hts:
        k = next((i for i, t in enumerate(placed) if t['name'].lower() == h_['name'].lower()), None)
        if k is None: raise KeyError(f'highlight_tiles: "{h_["name"]}" is not in "placed"')
        ha = ctx.t(h_.get('at'), .6)
        js.append(f"tl.to('#{p}-pl{k}',{{scale:{sc * 1.22:.3f},x:{-(150 * sc * .11):.1f},y:{-(100 * sc * .11):.1f},boxShadow:'0 0 0 3px #c9a45c, 0 14px 30px rgba(0,0,0,.75)',zIndex:20,duration:.2,ease:'power2.out'}},{ha:.3f});"
                  f"tl.to('#{p}-pl{k}',{{scale:{sc * 1.12:.3f},x:{-(150 * sc * .06):.1f},y:{-(100 * sc * .06):.1f},duration:.35,ease:'power2.inOut'}},{ha + .2:.3f});")
        ctx.sfx('click', ha, .5)
    ctx.js.append('\n'.join(js))
    return dict(html=ctx.shot_div(f'<div id="{p}-kb" class="kb"><div id="{p}-cam" style="position:absolute;left:0;top:0;width:1280px;height:720px">{body}</div></div>', 'board'))

def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a; D = ctx.dur
    tiers = [tuple(x) for x in ctx.p('tiers', TIERS)]; title = ctx.p('title', 'How long would you last in each Ice Age ocean?')
    placed = ctx.p('placed', [])
    if v == 'roadmap':
        tiles = ctx.p('tiles', []); n = len(tiles)
        if n == 0: raise KeyError('"tiles" (the list of all chapter tiles)')
        g = geom(n, len(tiers)); body, cnt = board(ctx, g, tiers, title, placed)
        sc = g['ts']; per = (1100 + 12) // (150 * sc + 12) if n <= 6 else None
        x0, y0, w, h = g['pool']; tw = 150 * sc; th = 100 * sc
        if n <= 6: rows_ = [list(range(n))]
        else: half = (n + 1) // 2; rows_ = [list(range(half)), list(range(half, n))]
        pos = {}
        for ri, idxs in enumerate(rows_):
            tot = len(idxs) * tw + (len(idxs) - 1) * 12; sx = x0 + (w - tot) / 2; sy = y0 + (h - (len(rows_) * th + (len(rows_) - 1) * 12)) / 2 + ri * (th + 12)
            for k, i in enumerate(idxs): pos[i] = (sx + k * (tw + 12), sy)
        ids = []
        for i, t in enumerate(tiles):
            x, y = pos[i]; ids.append(f'#{p}-t{i}')
            body += tile(f'{p}-t{i}', t['name'], t.get('image'), x, y, sc, ctx, extra=f'left:{x:.0f}px;top:{y:.0f}px;transform:scale({sc});transform-origin:0 0')
        rt = ctx.p('reveal_times'); st = ctx.t(ctx.p('reveal_at'), .5); step = ctx.p('stagger', .18)
        js = [f"hidden({ids!r});"]
        for i in range(n):
            ti = ctx.t(rt[i]) if rt else st + i * step
            js.append(f"tl.fromTo('#{p}-t{i}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.4,ease:'power2.out'}},{ti:.3f});")
            ctx.sfx('tick', ti, .25)
        gl = ctx.p('glow')
        if gl:
            k = next((i for i, t in enumerate(tiles) if t['name'].lower() == gl['name'].lower()), None)
            if k is None: raise KeyError(f'glow: "{gl["name"]}" is not in "tiles"')
            ga = ctx.t(gl.get('at'), 1.0)
            js.append(f"tl.to('#{p}-t{k}',{{scale:{sc * 1.18:.3f},x:{-(150 * sc * .09):.1f},y:{-(100 * sc * .09):.1f},boxShadow:'0 0 0 3px #c9a45c, 0 0 26px rgba(201,164,92,.7)',zIndex:20,duration:.25,ease:'power2.out'}},{ga:.3f});")
            ctx.sfx('click', ga, .4)
        js.append(f"kb('#{p}-kb',{T:.3f},{ctx.b:.3f},1.0,1.04,'50% 60%');")
        ctx.js.append('\n'.join(js))
        return dict(html=ctx.shot_div(f'<div id="{p}-kb" class="kb">{body}</div>', 'board'))
    # ---- drop (port of v9 s18)
    if v in ('final', 'final_wide'): return build_final(ctx, tiers, title, placed)
    tl_ = ctx.p('tile', {}); n_total = ctx.p('n_total', 5); g = geom(n_total if n_total else 5, len(tiers))
    tier = ctx.p('tier', 'Minutes'); names = [t[0].lower() for t in tiers]; r = names.index(tier.lower())
    add_at = ctx.p('add_tier_at'); new_name = ctx.p('new_tier', tiers[0][0]); new_row = names.index(new_name.lower()) if add_at is not None else None
    body, cnt = board(ctx, g, tiers, title, placed, new_row)
    body += tile(f'{p}-tile', tl_.get('name', ''), tl_.get('image'), 0, 0, 1, ctx)
    cur = ctx.p('cursor', True)
    if cur: body += (f'<svg id="{p}-cursor" class="cursor" width="34" height="44" viewBox="0 0 34 44"><path d="M3,2 L3,34 L11,27 L17,41 L23,38 L17,25 L28,25 Z" fill="#f6efe0" stroke="#000" stroke-width="2" stroke-linejoin="round"/></svg><div id="{p}-ring" class="ring"></div>')
    tc = ctx.t(ctx.p('drop_at'), D - 1.5)
    S0 = g['ts'] if g['rh'] >= 92 else min(g['ts'], (g['rh'] - 6) / 100.0); px, py = 104, g['pool'][1] + 8
    ytile = lambda k: g['top0'] + k * g['step'] - 4 + (0 if g['rh'] >= 92 else (g['rh'] - 100 * S0) / 2 + 4 - (100 - 100 * S0) / 2)
    sx = ctx.p('slot_x', 300 + cnt.get(r, 0) * (150 * S0 + 8) - (150 - 150 * S0) / 2 + (0 if cnt.get(r, 0) else 0))
    sy = ytile(r)
    hov = [(430, ytile(k)) for k in range(1, r)] or [(430, max(sy - 90, g['top0'] - 4))]
    CX, CY = 75, 50
    js = [f"gsap.set('#{p}-tile',{{x:{px},y:{py},scale:{S0},rotation:-2}});",
          f"kb('#{p}-kb',{T:.3f},{ctx.b:.3f},1.0,1.04,'30% 40%');"]
    if add_at is not None:   # the new tier row slides in on top of the board; the other rows move down one step
        ta = ctx.t(add_at, 0.0); st_ = g['step']
        js.append(f"gsap.set('.{p}-grp',{{y:{-st_}}});gsap.set('.{p}-new',{{y:{-st_ - 30},opacity:0}});"
                  f"tl.to('.{p}-grp',{{y:0,duration:.75,ease:'power3.inOut'}},{ta:.3f});tl.to('.{p}-new',{{y:0,opacity:1,duration:.75,ease:'power3.inOut'}},{ta:.3f});"
                  f"tl.fromTo('.{p}-new .tzone',{{backgroundColor:'rgba(201,164,92,.5)'}},{{backgroundColor:'rgba(201,164,92,0)',duration:.9,immediateRender:false}},{ta + .7:.3f});")
        ctx.sfx('slide_down', ta, .5); ctx.sfx('click', ta + .72, .5)
    if cur:
        js += [f"gsap.set('#{p}-cursor',{{x:1130,y:650,opacity:0,transformOrigin:'0 0'}});gsap.set('#{p}-ring',{{opacity:0}});",
               f"tl.to('#{p}-cursor',{{opacity:1,duration:.1}},{T + .05:.3f});tl.to('#{p}-cursor',{{x:{px + CX},y:{py + CY},duration:.5,ease:'power2.inOut'}},{T + .05:.3f});",
               f"tl.fromTo('#{p}-ring',{{x:{px + CX},y:{py + CY},scale:.3,opacity:.9,immediateRender:false}},{{scale:1.6,opacity:0,duration:.3}},{T + .58:.3f});tl.to('#{p}-cursor',{{scale:.86,duration:.08}},{T + .58:.3f});"]
    js.append(f"tl.to('#{p}-tile',{{scale:{S0 * 1.08:.3f},rotation:-3,duration:.1}},{T + .6:.3f});")
    def drag(tx, ty, at, d, ease='power2.inOut'):
        s = f"tl.to('#{p}-tile',{{x:{tx:.0f},y:{ty:.0f},duration:{d},ease:'{ease}'}},{at:.3f});"
        if cur: s += f"tl.to('#{p}-cursor',{{x:{tx + CX:.0f},y:{ty + CY:.0f},duration:{d},ease:'{ease}'}},{at:.3f});"
        return s
    seq = [(T + .75, .5, hov[0][0], hov[0][1], 'power2.inOut'), (T + 1.25, .22, hov[0][0] + 40, hov[0][1] - 8, 'sine.inOut')]
    for m, (hx, hy) in enumerate(hov[1:]): seq.append((T + 1.5 + .7 * m, .38, hx - 10, hy, 'power2.inOut'))
    for (at_, d_, x_, y_, e_) in seq:
        if at_ + d_ < tc - .25: js.append(drag(x_, y_, at_, d_, e_))
    js.append(drag(sx, sy, tc - .2, .2, 'power3.in'))
    js.append(f"tl.to('#{p}-tile',{{scale:{S0 * 1.16:.3f},duration:.05}},{tc - .02:.3f});tl.to('#{p}-tile',{{scale:{S0},rotation:1.5,duration:.25,ease:'back.out(3)'}},{tc + .03:.3f});")
    if cur:
        js.append(f"tl.to('#{p}-cursor',{{scale:1,duration:.08}},{tc:.3f});tl.fromTo('#{p}-ring',{{x:{sx + CX:.0f},y:{sy + CY:.0f},scale:.3,opacity:.9,immediateRender:false}},{{scale:1.9,opacity:0,duration:.35}},{tc:.3f});")
        js.append(f"tl.to('#{p}-cursor',{{x:760,y:470,opacity:0,duration:.9,ease:'power1.in'}},{tc + .5:.3f});")
    js.append(f"tl.fromTo('#{p}-row{r} .tzone',{{backgroundColor:'rgba(201,164,92,0)'}},{{backgroundColor:'rgba(201,164,92,.4)',duration:.15,yoyo:true,repeat:1,immediateRender:false}},{tc:.3f});")
    note = ctx.p('note')
    if note:   # small asterisk line next to the landed tile (e.g. "*in the water")
        nat_ = ctx.t(ctx.p('note_at'), tc + .5 - T)
        body += f'<div id="{p}-note" class="cg op0" style="position:absolute;left:{sx + 150 * S0 + 26:.0f}px;top:{sy + 22:.0f}px;font-size:34px;color:#d9bd7e"><i>{rich(note)}</i></div>'
        js.append(f"write('#{p}-note',{nat_:.3f},.6);"); ctx.sfx('tok', nat_, .45)
    vw = ctx.p('verdict')
    if vw:   # big verdict word: the largest text on screen, fast in (rule 15 exception for verdicts only), holds ~1.6 s
        hold = max(.8, min(1.6, ctx.b - tc - .35))
        body += (f'<div id="{p}-vs" style="position:absolute;left:0;top:0;width:1280px;height:720px;opacity:0;z-index:30;background:radial-gradient(ellipse at 50% 46%,rgba(0,0,0,.72) 0%,rgba(0,0,0,.5) 45%,rgba(0,0,0,.15) 100%)"></div>'
                 f'<div id="{p}-vw" class="cg" style="position:absolute;left:0;width:1280px;top:262px;text-align:center;font-size:96px;letter-spacing:1px;opacity:0;z-index:31">{esc(vw)}</div>'
                 f'<div id="{p}-vu" style="position:absolute;left:490px;top:380px;width:300px;height:3px;background:#c9a45c;transform:scaleX(0);transform-origin:50% 50%;z-index:31;opacity:0"></div>')
        js.append(f"tl.to('#{p}-vs',{{opacity:1,duration:.12}},{tc:.3f});tl.fromTo('#{p}-vw',{{opacity:0,scale:1.14}},{{opacity:1,scale:1,duration:.16,ease:'power3.out',immediateRender:false}},{tc:.3f});"
                  f"tl.set('#{p}-vu',{{opacity:1}},{tc + .12:.3f});tl.to('#{p}-vu',{{scaleX:1,duration:.4,ease:'power2.out'}},{tc + .12:.3f});"
                  f"tl.to(['#{p}-vs','#{p}-vw','#{p}-vu'],{{opacity:0,duration:.35,ease:'power1.in'}},{tc + hold:.3f});")
        st = ctx.p('sting', 'thud')
        if st == 'full': ctx.sfx('duck', tc - .8, 1.0); ctx.events[-1]['dur'] = 1.4; ctx.sfx('riser', tc - .75, .55)
        ctx.sfx('vhit', tc, .8 if st == 'full' else .55)
    ctx.js.append('\n'.join(js))
    ctx.sfx('click', T + .55, .55); ctx.sfx('click', tc, .9); ctx.sfx('thud_soft', tc, .35)
    return dict(html=ctx.shot_div(f'<div id="{p}-kb" class="kb">{body}</div>', 'board'))
