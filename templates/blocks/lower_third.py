from .common import *
META = dict(name='lower_third', about='One-word / short italic lower third on a clip (rule 15b). For jokes and one-word labels.',
  variants=['italic_word', 'two_part', 'kicker_line'],
  params={'text': 'main text', 'at': 'when it appears (time spec; default 0.3 s)', 'size': 'text size px (default 46, two_part 40)',
          'aside': 'two_part: the italic aside, e.g. "(45 minutes away)"', 'aside_at': 'two_part: when the aside appears',
          'kicker': 'kicker_line: small caps line', 'kicker_at': 'plain card: the kicker appears on its own at this time (before the text)', 'jump_at': 'instant zoom step on the clip', 'jump_scale': 'zoom after the step (default 1.14)',
          'joke_sound': 'two_part: dry "tok" on the aside (default true)',
          'plain': 'true (or "card": true in the shot, with no clip) = a text card on a dark picture, text in the middle, bigger'})
def build(ctx):
    v = ctx.variant; p = ctx.id; text = ctx.p('text', ''); at = ctx.t(ctx.p('at'), .3)
    h = ctx.video((1.0, 1.06, '50% 40%'))
    js = []; pl = ctx.plain      # text card without a clip ("card": true in the shot or "plain": true in params): the text sits in the middle, bigger
    if pl:
        size = ctx.p('size', 84 if v != 'two_part' else 70); k = ctx.p('kicker', ''); aside = ctx.p('aside', ''); aat = ctx.t(ctx.p('aside_at'), at - ctx.a + .6)
        kat = ctx.p('kicker_at'); kat = ctx.t(kat) if (kat is not None and k) else None   # kicker shows first, on its own
        inner = block(f'{p}-blk', 0, 270, 1280, (f'<div id="{p}-k" class="jo gold{" op0" if kat is not None else ""}" style="margin-bottom:18px">{rich(k)}</div>' if k else '')
            + f'<span id="{p}-t" class="it" style="font-size:{size}px">{rich(text)}</span>' + (f'<span id="{p}-b" class="it" style="font-size:{size}px;color:#f6efe0;margin-left:.35em">{rich(aside)}</span>' if aside else '') + '<div class="gr op0" id="' + p + '-g"></div>')
        if kat is not None: js.append(f"tl.set('#{p}-blk',{{opacity:1}},{min(kat, at) - .1:.3f});drop('#{p}-k',{kat - .1:.3f});")
        js.append((f"drop('#{p}-blk',{at - .1:.3f});" if kat is None else '') + f"write('#{p}-t',{at:.3f},.4);underline('#{p}-g',{at + .3:.3f},.6);" + (f"write('#{p}-b',{aat:.3f},.6);" if aside else ''))
        if aside and ctx.p('joke_sound', True): ctx.sfx('tok', aat + .1, .9)
        ctx.js.append('\n'.join(js)); return dict(html=h + ctx.overlay(inner))
    if v == 'italic_word':
        size = ctx.p('size', 46)
        inner = '<div class="scrimB"></div>' + block(f'{p}-blk', 0, 618, 1280, f'<span id="{p}-t" class="it" style="font-size:{size}px">{rich(text)}</span>')
        js.append(f"drop('#{p}-blk',{at - .1:.3f});write('#{p}-t',{at:.3f},.4);")
    elif v == 'two_part':
        size = ctx.p('size', 40); aside = ctx.p('aside', ''); aat = ctx.t(ctx.p('aside_at'), at - ctx.a + .6)
        inner = '<div class="scrimB"></div>' + block(f'{p}-blk', 0, 618, 1280,
            f'<span id="{p}-a" class="cg" style="font-size:{size}px;text-shadow:0 2px 16px #000">{rich(text)}</span> <span id="{p}-b" class="it" style="font-size:{size}px">{rich(aside)}</span>')
        js.append(f"drop('#{p}-blk',{at - .05:.3f});write('#{p}-a',{at + .1:.3f},.55);write('#{p}-b',{aat + .05:.3f},.8);")
        if ctx.p('joke_sound', True): ctx.sfx('tok', aat + .1, .9)
    else:
        size = ctx.p('size', 44); k = ctx.p('kicker', '')
        kat = ctx.p('kicker_at'); kat = ctx.t(kat) if (kat is not None and k) else None   # v2: the kicker (e.g. a source line) shows first, on its own
        inner = '<div class="scrimLB"></div>' + block(f'{p}-blk', 90, 540, 760,
            (f'<div class="jo gold" style="margin-bottom:12px">{rich(k)}</div>' if k else '') + f'<div id="{p}-t" class="it{" op0" if kat is not None else ""}" style="font-size:{size}px">{rich(text)}</div>', 'left')
        if kat is not None and kat < at - .2: js.append(f"drop('#{p}-blk',{kat - .1:.3f});write('#{p}-t',{at:.3f},.6);")
        else: js.append(f"drop('#{p}-blk',{at - .1:.3f});write('#{p}-t',{at:.3f},.6);")
    if ctx.p('jump_at') is not None:
        js.append(f"jump('#{p}_v',{ctx.t(ctx.p('jump_at')):.3f},{ctx.p('jump_scale', 1.14)},'50% 40%');")
    ctx.js.append('\n'.join(js))
    return dict(html=h + ctx.overlay(inner))
