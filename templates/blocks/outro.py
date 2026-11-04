from .common import *
from .tier_board import board, TIERS
META = dict(name='outro', about='Outro (gap T3). "question" = "Do you agree?" over the finished board (dimmed) with a gold italic line; "card" = the same on a dark picture without the board; "end_screen" = the 12 s end-screen layout (2 video slots + subscribe circle, music only, fades to black).',
  variants=['question', 'card', 'end_screen'], 
  params={'question': 'big line (default "Do you agree?")', 'line': 'gold italic line (default "Tell me where you would put it")', 'line_at': 'when the italic line shows (time spec; default 1.2 s)',
          'board': 'question: true = show the finished board dimmed behind the text (default true; needs "placed")', 'placed': 'tiles on the board: list of {"name","image","tier"}',
          'tiers': 'list of [name, colour] (default: the 6 final tiers, Days first)', 'title': 'board title (default "How long would you last in each Ice Age ocean?")',
          'bg': 'end_screen: "board" (dimmed finished board, default) or "dark"', 'slot_a': 'end_screen: caps label under the left video slot (default "WATCH NEXT")',
          'slot_b': 'end_screen: caps label under the right video slot (default "MORE ICE AGE")', 'thanks': 'end_screen: italic line on top (default "Thanks for watching")',
          'subscribe': 'end_screen: caps label under the subscribe circle (default "SUBSCRIBE")', 'fade_s': 'end_screen: fade to black at the end, seconds (default 1.2)', 'slots': 'end_screen: false = no video slots, only the thanks line and the subscribe circle in the middle (default true)',
          'end_screen_s': 'ignored (kept for old plans): use a separate end_screen shot'})
LONG_OK = {'end_screen'}
FINAL_TIERS = [('Days', '#4f7a86'), ('Overnight', '#5f7f6a'), ('Hours', '#8a9a62'), ('An hour', '#b39a55'), ('Minutes', '#b8794d'), ('Seconds', '#9a4f4a')]
def _bg(ctx, dim):
    placed = ctx.p('placed', []); tiers = [tuple(x) for x in ctx.p('tiers', FINAL_TIERS)]; title = ctx.p('title', 'How long would you last in each Ice Age ocean?')
    g = dict(top0=52, step=104, rh=96, pool=(0, 0, 0, 0), ts=.9, lab_fs=30, ttl=20)
    body, _ = board(ctx, g, tiers, title, placed, None, pool=False)
    return f'<div class="kb board" style="background:#1b1d20">{body}</div><div class="shade" style="background:rgba(0,0,0,{dim})"></div>'
def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a; B = ctx.b; D = ctx.dur
    ctx.p('end_screen_s')
    for k_ in ('placed', 'tiers', 'title', 'board', 'bg'): ctx.params.get(k_); ctx._used.add(k_)
    if v == 'end_screen':
        bg = ctx.p('bg', 'board'); fs = float(ctx.p('fade_s', 1.2))
        base = _bg(ctx, .93) if bg == 'board' else '<div class="shade dk"></div>'
        sl = ''; slots = ctx.p('slots', True) not in (False, 'false', 0)
        cy, ty = (590, 50) if slots else (450, 200)
        for i, (x, key, d) in enumerate([(90, 'slot_a', 'WATCH NEXT'), (690, 'slot_b', 'MORE ICE AGE')] if slots else []):
            sl += (f'<g id="{p}-sl{i}" opacity="0"><rect x="{x}" y="200" width="500" height="281" fill="rgba(0,0,0,.35)" stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.5" stroke-dasharray="2 8" stroke-linecap="round"/>'
                   f'<path d="M{x},{200+26} V200 H{x+26} M{x+474},200 H{x+500} V{200+26} M{x+500},{481-26} V481 H{x+474} M{x+26},481 H{x} V{481-26}" stroke="{GOLD}" stroke-width="3" fill="none"/>'
                   f'<text x="{x+250}" y="{481+40}" text-anchor="middle" class="tbl" style="font-size:15px">{esc(ctx.p(key, d))}</text></g>')
        sub = (f'<g id="{p}-sub" opacity="0"><circle id="{p}-subr" cx="640" cy="{cy}" r="70" fill="none" stroke="{GOLD}" stroke-width="2" stroke-opacity=".5"/><circle cx="640" cy="{cy}" r="58" fill="rgba(0,0,0,.4)" stroke="{GOLD}" stroke-width="2.5"/>'
               f'<text x="640" y="{cy + 96}" text-anchor="middle" class="tbl" style="font-size:15px">{esc(ctx.p("subscribe", "SUBSCRIBE"))}</text></g>')
        hdr = f'<div id="{p}-th" class="it op0" style="position:absolute;left:0;width:1280px;text-align:center;top:{ty}px;font-size:60px;z-index:20">{rich(ctx.p("thanks", "Thanks for watching"))}</div><div class="gr" style="position:absolute;left:608px;top:{ty + 84}px;margin:0"></div>'
        ctx.js.append(f"pop('#{p}-th',{T + .2:.3f},.6);" + (f"fadeIn('#{p}-sl0',{T + .6:.3f},.6);fadeIn('#{p}-sl1',{T + 1.0:.3f},.6);" if slots else '') + f"fadeIn('#{p}-sub',{T + (1.5 if slots else .8):.3f},.6);"
                      f"tl.fromTo('#{p}-subr',{{scale:1,opacity:.6,svgOrigin:'640 {cy}'}},{{scale:1.35,opacity:0,duration:1.6,repeat:{max(1, int(D / 1.6))},ease:'power1.out',svgOrigin:'640 {cy}'}},{T + 2:.3f});"
                      f"gsap.set('#{p}-fd',{{opacity:0}});tl.to('#{p}-fd',{{opacity:1,duration:{fs},ease:'none'}},{B - fs:.3f});")
        html = ctx.shot_div(base + f'<svg width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;left:0;top:0">{sl}{sub}</svg>{hdr}'
                            f'<div id="{p}-fd" style="position:absolute;left:0;top:0;width:1280px;height:720px;background:#000;opacity:0;z-index:50"></div>', 'board')
        return dict(html=html)
    q = ctx.p('question', 'Do you agree?'); line = ctx.p('line', 'Tell me where you would put it'); lat = ctx.t(ctx.p('line_at'), 1.2)
    if v == 'question' and ctx.p('board', True): base = _bg(ctx, .66)
    else: base = '<div class="kb board" style="background:#101418"></div><div class="shade dk"></div>'
    txt = (f'<div id="{p}-q" class="cg op0" style="position:absolute;left:0;width:1280px;text-align:center;top:236px;font-size:128px;letter-spacing:.02em;z-index:20">{rich(q)}</div>'
           f'<div class="gr op0" id="{p}-g" style="position:absolute;left:608px;top:404px;margin:0;z-index:20"></div>'
           f'<div id="{p}-l" class="it op0" style="position:absolute;left:0;width:1280px;text-align:center;top:436px;font-size:54px;z-index:20">{rich(line)}</div>')
    ctx.js.append(f"drop('#{p}-q',{T + .15:.3f});underline('#{p}-g',{lat - .1:.3f},.6);write('#{p}-l',{lat:.3f},.8);kb('#{p}-kb',{T:.3f},{B:.3f},1.0,1.03,'50% 50%');")
    ctx.sfx('thud_soft', T + .15, .35); ctx.sfx('tok', lat, .35)
    return dict(html=ctx.shot_div(f'<div id="{p}-kb" class="kb">{base}{txt}</div>', 'board'))
