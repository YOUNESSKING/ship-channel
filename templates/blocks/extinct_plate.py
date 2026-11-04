from .common import *
META = dict(name='extinct_plate', about='Gold-framed plate on a clip: EXTINCT + date (rule 15c, rule 6). Also works for other one-fact plates (e.g. "UNKNOWN").',
  variants=['right', 'center', 'left'],
  params={'word': 'big word, default "EXTINCT"', 'date': 'italic line, e.g. "3.6 million years ago"', 'at': 'when the plate fades in (time spec; default 0.4 s)',
          'sound': 'false = no stamp sound'})
def build(ctx):
    v = ctx.variant; p = ctx.id
    word = ctx.p('word', 'EXTINCT'); date = ctx.p('date', ''); at = ctx.t(ctx.p('at'), .4)
    pos = {'right': (760, 470, 440, 'scrimR'), 'center': (380, 470, 520, 'scrimBR'), 'left': (80, 470, 440, 'scrimLB')}[v]
    inner = (f'<div class="{pos[3]}"></div><div id="{p}-plate" class="plate op0" style="left:{pos[0]}px;top:{pos[1]}px;width:{pos[2]}px">'
             f'<div class="cg" style="font-size:{min(60, int(60 * 8 / max(8, len(word))))}px;letter-spacing:.3em;margin-right:-.3em;color:{GOLD}">{rich(word.upper())}</div><div class="gr" style="margin:14px auto"></div>'
             f'<div class="cg" style="font-size:28px"><i>{rich(date)}</i></div></div>')
    ctx.js.append(f"tl.fromTo('#{p}-plate',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.9,ease:'power2.out'}},{at:.3f});")
    if ctx.p('sound', True): ctx.sfx('stamp', at + .15, .9)
    return dict(html=ctx.video((1.0, 1.05, '50% 50%')) + ctx.overlay(inner, 12))
