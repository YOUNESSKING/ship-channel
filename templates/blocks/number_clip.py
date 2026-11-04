import re
from .common import *
META = dict(name='number_clip',
  about='Big number over a clip: kicker + number + hairline + italic subline (rule 15a). Number can count or be struck out and replaced.',
  variants=['right', 'center_bars', 'left_stack', 'strike_swap'],
  params={'kicker': 'small caps line above the number, e.g. "Near the ice"',
          'number': 'the big number text, e.g. "0°C" or "15-30" (use ° for degrees)', 'unit': 'italic word after the number, e.g. "minutes"',
          'subline': 'small line under the number', 'number_at': 'when the number appears (time spec; default 0.6 s after shot start)',
          'subline_at': 'when the subline appears', 'size': 'number size in px',
          'side': 'variant right: "right" (default) or "left"',
          'count': '{"from":0,"to":-1.8,"decimals":1,"dur":1.2,"suffix":"°C"} - animate the number instead of showing it fixed',
          'jump_at': 'time of an instant zoom step on the clip', 'jump_scale': 'zoom after the step (default 1.2)',
          'dim': 'variant center_bars/strike_swap: dark shade strength "dk" (default) or "lt"',
          'lead1': 'strike_swap: first small line ("The water")', 'lead2': 'strike_swap: second small line ("Salt water freezes at")',
          'old': 'strike_swap: the number that gets struck out ("0°C")', 'new': 'strike_swap: the true number ("-1.8°C")',
          'show_at': 'strike_swap: when lead1 + old number appear', 'swap_at': 'strike_swap: when lead1 changes to lead2',
          'strike_at': 'strike_swap: when the line strikes out the old number', 'new_count': 'strike_swap: true = new number counts from 0 to its value'})

def _fmt_js(cnt):
    d = int(cnt.get('decimals', 0)); suf = rich(cnt.get('suffix', '')).replace("'", "\\'")
    return f"(v)=>(v<0?'&minus;':'')+Math.abs(v).toFixed({d})+'{suf}'"

def build(ctx):
    v = ctx.variant; p = ctx.id
    if v == 'strike_swap': return _strike(ctx)
    kick = ctx.p('kicker'); big = ctx.p('number'); unit = ctx.p('unit'); sub = ctx.p('subline')
    cnt = ctx.p('count'); at = ctx.t(ctx.p('number_at'), .6); sat = ctx.t(ctx.p('subline_at'), 1.6)
    shown = big
    if cnt:
        d = int(cnt.get('decimals', 0)); fv = cnt['from']
        shown = (('-' if fv < 0 else '') + f'{abs(fv):.{d}f}' + cnt.get('suffix', ''))
    js = []
    if v == 'right':
        size = ctx.p('size', 112); side = ctx.p('side', 'right')
        scrim = 'scrimR' if side == 'right' else 'scrimLB'
        x, al = (760, 'right') if side == 'right' else (80, 'left')
        inner = f'<div class="{scrim}"></div>' + block(f'{p}-blk', x, 440, 440 if side == 'right' else 520,
            (f'<div class="jo gold">{rich(kick)}</div>' if kick else '') + num(f'{p}-n', shown, unit, size, int(size * .7), 'margin-top:10px')
            + (f'<div class="gr{" l" if side=="left" else ""}"></div><div id="{p}-sub" class="it" style="font-size:34px">{rich(sub)}</div>' if sub else ''), al)
        h = ctx.video((1.0, 1.08, '30% 50%')) + ctx.overlay(inner)
        js.append(f"drop('#{p}-blk',{ctx.t(None, .15):.3f});pop('#{p}-n',{at - .05:.3f});")
        if sub: js.append(f"write('#{p}-sub',{sat:.3f},.9);")
        ctx.sfx('click', at, .4)
    elif v == 'center_bars':
        size = ctx.p('size', 124); dk = 'shade dk' if ctx.p('dim', 'dk') == 'dk' else 'shade'
        inner = f'<div class="{dk}"></div>' + bars() + block(f'{p}-blk', 0, 250, 1280,
            (f'<div class="jo gold" style="margin-bottom:14px">{rich(kick)}</div>' if kick else '') + num(f'{p}-n', shown, unit, size, size)
            + (f'<div id="{p}-u" class="gr"></div><div id="{p}-sub" class="jo" style="font-size:22px">{rich(sub)}</div>' if sub else ''))
        h = ctx.video((1.0, 1.1, '50% 50%')) + ctx.overlay(inner)
        js.append(f"drop('#{p}-blk',{at - .12:.3f});")
        if sub: js.append(f"write('#{p}-sub',{sat:.3f},.8);underline('#{p}-u',{at + .18:.3f},.8);")
        ctx.sfx('thud', at - .02, .9)
    else:  # left_stack
        size = ctx.p('size', 130)
        inner = '<div class="scrimL"></div>' + block(f'{p}-blk', 80, 230, 700,
            (f'<div class="jo gold">{rich(kick)}</div>' if kick else '') + num(f'{p}-n', shown, unit, size, int(size * .62), 'margin-top:16px')
            + f'<div class="gr l"></div><div id="{p}-sub" class="it" style="font-size:36px">{rich(sub or "")}</div>', 'left')
        h = ctx.video((1.0, 1.06, '70% 50%')) + ctx.overlay(inner)
        js.append(f"drop('#{p}-blk',{at - .05:.3f});write('#{p}-sub',{sat:.3f},.8);")
        ctx.sfx('click', at, .5)
    if cnt:
        t0 = ctx.t(cnt.get('at'), at - ctx.a)
        js.append(f"counter('#{p}-n span',{t0:.3f},{cnt.get('dur', 1.2)},{cnt['from']},{cnt['to']},{_fmt_js(cnt)});")
    if ctx.p('jump_at') is not None:
        js.append(f"jump('#{p}_v',{ctx.t(ctx.p('jump_at')):.3f},{ctx.p('jump_scale', 1.2)});")
    ctx.js.append('\n'.join(js))
    return dict(html=h)

def _strike(ctx):
    p = ctx.id
    l1 = ctx.p('lead1', 'The water'); l2 = ctx.p('lead2', 'Salt water freezes at'); old = ctx.p('old', '0°C'); new = ctx.p('new', '-1.8°C')
    sub = ctx.p('subline', 'salt lowers the freezing point')
    show = ctx.t(ctx.p('show_at'), .5); swap = ctx.t(ctx.p('swap_at'), 1.4); strike = ctx.t(ctx.p('strike_at'), 2.2); sat = ctx.t(ctx.p('subline_at'), 3.4)
    plain = re.sub(r'[^0-9A-Za-z.\-]', '', old); wpx = max(190, len(plain) * 56 + 60)
    x0, x1 = 640 - wpx / 2, 640 + wpx / 2
    dk = 'shade dk' if ctx.p('dim', 'dk') == 'dk' else 'shade'
    inner = f'''<div class="{dk}"></div>{bars()}
<div id="{p}-all" class="op0" style="position:absolute;left:0;top:0;width:1280px;height:720px">
 <div id="{p}-q1" class="jo abs" style="top:150px">{rich(l1)}</div><div id="{p}-q2" class="jo abs" style="top:150px">{rich(l2)}</div>
 <div id="{p}-z" class="cg abs" style="top:222px;font-size:112px">{rich(old)}</div>
 <svg id="{p}-s" width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;left:0;top:0"><path id="{p}-sp" pathLength="1" d="M{x0:.0f},276 L{x1:.0f},270" stroke="{GOLD}" stroke-width="10" stroke-linecap="round" fill="none" stroke-dasharray="1" stroke-dashoffset="1"/></svg>
 <div id="{p}-n" class="cg abs" style="top:326px;font-size:150px"><span>{rich(new)}</span></div>
 <div id="{p}-h" class="it abs" style="top:505px;font-size:40px">{rich(sub)}</div></div>'''
    h = ctx.video((1.0, 1.08, '50% 50%')) + ctx.overlay(inner)
    js = f"""drop('#{p}-all',{show - .05:.3f});
tl.to('#{p}-q1',{{opacity:0,duration:.15}},{swap - .15:.3f});
tl.fromTo('#{p}-q2',{{opacity:0}},{{opacity:1,duration:.2}},{swap - .1:.3f});
underline('#{p}-sp',{strike - .12:.3f},.25);
tl.to('#{p}-z',{{opacity:.45,y:-48,scale:.5,transformOrigin:'50% 50%',duration:.6,ease:'power2.inOut'}},{strike + .1:.3f});
tl.to('#{p}-s',{{y:-48,scale:.5,transformOrigin:'640px 278px',duration:.6,ease:'power2.inOut'}},{strike + .1:.3f});
tl.fromTo('#{p}-n',{{opacity:0,y:14}},{{opacity:1,y:0,duration:1.0,ease:'power2.out'}},{strike + .25:.3f});
write('#{p}-h',{sat:.3f},.9);"""
    if ctx.p('new_count'):
        m = re.search(r'-?\d+(\.\d+)?', new.replace('−', '-')); val = float(m.group(0)); dec = len(m.group(0).split('.')[1]) if '.' in m.group(0) else 0
        js += f"\ncounter('#{p}-n span',{strike + .25:.3f},.9,0,{val},{_fmt_js({'decimals': dec, 'suffix': new[m.end():]})});"
    ctx.js.append(js)
    ctx.sfx('click', ctx.a, .5); ctx.sfx('scratch', strike - .05, .45); ctx.sfx('ding_hi', strike + .35, .4)
    return dict(html=h)
