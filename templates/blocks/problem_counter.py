from .common import *
META = dict(name='problem_counter', about='"Problem one / problem two" counter overlay on a clip or plain dark (rule 55). The deciding problem can be marked gold.',
  variants=['corner_badge', 'center_line', 'pips'],
  params={'n': 'which problem: 1, 2 or 3', 'total': 'how many problems this chapter (default 2)', 'title': 'short italic name, e.g. "the cold"',
          'at': 'when it appears (time spec; default 0.3 s)', 'decider': 'true = this is the problem that decides: gold ring + "THE DECIDING PROBLEM"',
          'word': 'override the caps word (default "PROBLEM ONE" / "PROBLEM TWO")', 'plain': 'true = no clip, dark background'})
WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
def build(ctx):
    v = ctx.variant; p = ctx.id; n = int(ctx.p('n', 1)); tot = int(ctx.p('total', 2)); title = ctx.p('title', ''); at = ctx.t(ctx.p('at'), .3)
    dec = ctx.p('decider', False); word = ctx.p('word') or ('PROBLEM ' + WORDS[n].upper()); h = ''
    if ctx.clip.get('file'): h = ctx.video((1.0, 1.06, '50% 50%'))
    else: h = ctx.shot_div('', 'dark').replace('class="clip shot dark"', 'class="clip shot" style="background:#050505"')
    sub = 'THE DECIDING PROBLEM' if dec else ''
    if v == 'corner_badge':
        inner = ('<div style="position:absolute;left:0;top:0;width:1000px;height:560px;background:radial-gradient(ellipse at 8% 8%,rgba(0,0,0,.72),rgba(0,0,0,0) 68%)"></div>' + block(f'{p}-blk', 70, 62, 560,
                 f'<div class="jo gold" style="font-size:20px">{esc(word)}</div>'
                 f'<div class="cg" style="font-size:96px;margin-top:6px"><span>{n}</span><i style="font-size:48px;color:{ITAL}"> of {tot}</i></div><div class="gr l"></div>'
                 + (f'<div id="{p}-t" class="it" style="font-size:38px">{rich(title)}</div>' if title else '')
                 + (f'<div class="jo gold" style="font-size:14px;margin-top:12px">{sub}</div>' if sub else ''), 'left'))
        js = f"drop('#{p}-blk',{at:.3f});"
    elif v == 'center_line':
        inner = '<div class="scrimB"></div>' + block(f'{p}-blk', 0, 520, 1280,
                 f'<div class="jo gold" style="font-size:21px">{esc(word)}</div>' + (f'<div id="{p}-t" class="cg" style="font-size:62px;margin-top:10px"><i>{rich(title)}</i></div>' if title else '')
                 + (f'<div class="gr"></div><div class="jo" style="font-size:14px">{sub}</div>' if sub else ''))
        js = f"drop('#{p}-blk',{at:.3f});"
    else:  # pips
        pips = ''.join(f'<circle cx="{i*34}" cy="0" r="9" fill="{GOLD if i < n else "none"}" stroke="{GOLD}" stroke-width="2"/>' for i in range(tot))
        w = (tot - 1) * 34
        inner = ('<div class="scrimB"></div>' + block(f'{p}-blk', 0, 586, 1280,
                 f'<svg width="{w+40}" height="30" viewBox="{-20} -15 {w+40} 30" style="display:block;margin:0 auto 14px">{pips}</svg>'
                 f'<div class="jo gold" style="font-size:20px">{esc(word)}</div>' + (f'<div id="{p}-t" class="it" style="font-size:42px;margin-top:8px">{rich(title)}</div>' if title else '')))
        js = f"drop('#{p}-blk',{at:.3f});"
    ctx.js.append(js); ctx.sfx('click', at + .05, .5)
    return dict(html=h + ctx.overlay(inner))
