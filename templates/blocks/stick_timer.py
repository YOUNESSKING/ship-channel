from .common import *
META = dict(name='stick_timer', about='Stick-figure body gag with the timer bar (rule 3, 9, 14): gasp (1 min), hand (10 min), lights_out (30 min). Same bar in every chapter.',
  variants=['gasp', 'hand', 'lights_out'],
  params={'kicker': 'small caps line ("Cold shock")', 'number': 'big number ("1")', 'unit': 'italic unit ("minute")', 'line': 'italic line ("can\'t control your breathing")',
          'line_at': 'when the italic line appears (time spec)', 'from_stop': 'timer start stop 0-3 (default per variant: gasp 0, hand 1, lights_out 2)',
          'to_stop': 'timer end stop 0-3', 'labels': 'four labels for the bar, default ["START","1 MIN","10 MIN","30 MIN"]; change them for heat/thirst/salt chains',
          'gasp_words': 'gasp: the two shout words (default ["gasp","gasp"])', 'gasp_at': 'gasp: list of 2 time specs',
          'sink_at': 'lights_out: when the figure starts to sink', 'dim_at': 'lights_out: when the screen dims', 'dim_to': 'lights_out: final darkness 0-1 (default .72)'})

def _text(ctx, p, kick, number, unit, line, nsize, usize, lsize, x, y, w, align='left'):
    return block(f'{p}-txt', x, y, w, (f'<div class="jo gold">{rich(kick)}</div>' if kick else '') + num(f'{p}-n', number, unit, nsize, usize, 'margin-top:16px')
                 + f'<div class="gr{" l" if align=="left" else ""}"></div><div id="{p}-h" class="it" style="font-size:{lsize}px">{rich(line)}</div>', align)

def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a; D = ctx.dur
    kick = ctx.p('kicker', ''); number = ctx.p('number', ''); unit = ctx.p('unit', ''); line = ctx.p('line', '')
    lat = ctx.t(ctx.p('line_at'), .8); labels = ctx.p('labels')
    f0, f1 = {'gasp': (0, 1), 'hand': (1, 2), 'lights_out': (2, 3)}[v]
    f0 = ctx.p('from_stop', f0); f1 = ctx.p('to_stop', f1)
    mk = f"mark('{p}',{T:.3f},{X0[f0]},{X0[f1]},{.45 if v != 'hand' else .4});"
    if v == 'gasp':
        ga = ctx.p('gasp_at'); g1 = ctx.t(ga[0] if ga else None, .15); g2 = ctx.t(ga[1] if ga else None, 1.3); gw = ctx.p('gasp_words', ['gasp', 'gasp'])
        svg = (f'<g id="{p}-all"><g id="{p}-figw"><g id="{p}-fig0">{fig(p, 380, 470, 1.25)}</g></g>{water(p, 432)}</g>'
               f'<text id="{p}-gasp" x="300" y="215" text-anchor="middle" class="itsv" style="font-size:60px" opacity="0">{esc(gw[0])}</text>'
               f'<text id="{p}-gasp2" x="300" y="215" text-anchor="middle" class="itsv" style="font-size:60px" opacity="0">{esc(gw[1])}</text>{timer_bar(p, labels)}')
        txt = _text(ctx, p, kick, number, unit, line, 130, 80, 34, 660, 110, 560)
        js = f"""pose('{p}',380,470,1.25,{{aL:140,aR:-140,lL:10,lR:-10}});
flail('{p}',380,470,1.25,{T:.3f},{D:.3f},118,152,.22);
gsap.set('#{p}-mouth',{{opacity:0}});gsap.set('#{p}-mouthO',{{opacity:1}});
bob('#{p}-fig0',{T:.3f},{D:.3f},10,.3);drift('#{p}-water',{T:.3f},{D:.3f},-220);
kb('#{p}-kb',{T:.3f},{ctx.b:.3f},1.0,1.05,'30% 50%');
{mk}
drop('#{p}-txt',{T + .05:.3f});write('#{p}-h',{lat:.3f},1.0);
tl.fromTo('#{p}-gasp',{{opacity:0}},{{keyframes:[{{opacity:1,duration:.12}},{{opacity:1,duration:.6}},{{opacity:0,duration:.15}}]}},{g1:.3f});
tl.fromTo('#{p}-gasp2',{{opacity:0}},{{keyframes:[{{opacity:1,duration:.12}},{{opacity:1,duration:.5}},{{opacity:0,duration:.15}}]}},{g2:.3f});"""
        ctx.sfx('tok', T, .3); ctx.sfx('gasp', g1, .8); ctx.sfx('gasp', g2, .8)
        cls = ''
    elif v == 'hand':
        fingers = ''.join(f'<g id="{p}-f{i}"><line x1="{x}" y1="-10" x2="{x}" y2="-{10+l}" stroke="#000" stroke-width="30"/><line x1="{x}" y1="-10" x2="{x}" y2="-{10+l}" stroke="#fff" stroke-width="21"/></g>'
                          for i, (x, l) in enumerate([(-38, 80), (-13, 100), (13, 96), (38, 72)]))
        svg = (f'<g id="{p}-all"><g id="{p}-figw">{fig(p, 250, 470, 1.0)}</g>{water(p, 440)}</g>'
               f'<g id="{p}-zoom"><path d="M330,330 L742,290 M330,330 L742,540" stroke="#fff" stroke-opacity=".5" stroke-width="3" stroke-dasharray="6 10" fill="none"/>'
               f'<circle cx="900" cy="400" r="175" fill="#0b0b0e" stroke="#e9dcc0" stroke-width="3"/><g transform="translate(900,430)"><g id="{p}-hand">{fingers}'
               f'<circle cx="0" cy="26" r="58" fill="#fff" stroke="#000" stroke-width="5"/><g id="{p}-thumb"><line x1="40" y1="40" x2="92" y2="2" stroke="#000" stroke-width="30" stroke-linecap="round"/>'
               f'<line x1="40" y1="40" x2="92" y2="2" stroke="#fff" stroke-width="21" stroke-linecap="round"/></g></g></g></g>{timer_bar(p, labels)}')
        txt = _text(ctx, p, kick, number, unit, line, 112, 70, 36, 70, 50, 520)
        lat = ctx.t(ctx.p('line_at'), 1.0)
        fl = ''
        for i, (x, d) in enumerate(zip([-38, -13, 13, 38], [1, 1, -1, -1])):
            o = f'{x} -10'; c = d * 66
            fl += (f"tl.to('#{p}-f{i}',{{rotation:{c},svgOrigin:'{o}',duration:.28,ease:'power2.out'}},{T + .55 + i * .03:.3f});"
                   f"tl.to('#{p}-f{i}',{{rotation:{c * .15},svgOrigin:'{o}',duration:.22,ease:'power1.in'}},{T + .95 + i * .03:.3f});"
                   f"tl.to('#{p}-f{i}',{{rotation:{c * .75},svgOrigin:'{o}',duration:.2,ease:'power2.out'}},{T + 1.25 + i * .03:.3f});"
                   f"tl.to('#{p}-f{i}',{{rotation:{-c * .35},svgOrigin:'{o}',duration:.35,ease:'power1.inOut'}},{T + 1.6 + i * .03:.3f});\n")
        js = f"""pose('{p}',250,470,1.0,{{aL:20,aR:-148,lL:10,lR:-10}});
flail('{p}',250,470,1.0,{T:.3f},{D:.3f},10,22,.5);gsap.set('#{p}-armR',{{rotation:-148}});
bob('#{p}-figw',{T:.3f},{D:.3f},7,.5);drift('#{p}-water',{T:.3f},{D:.3f},-200);
{mk}
drop('#{p}-txt',{T + .05:.3f});write('#{p}-h',{lat:.3f},.8);
{fl}tl.fromTo('#{p}-hand',{{x:0}},{{x:4,duration:.06,yoyo:true,repeat:30,ease:'none'}},{T + .3:.3f});"""
        ctx.sfx('click', T, .5)
    else:  # lights_out
        sink = ctx.t(ctx.p('sink_at'), .3); dim = ctx.t(ctx.p('dim_at'), (sink - T) + 1.0); dto = ctx.p('dim_to', .72)
        bub = ''.join(f'<circle cx="{380+dx}" cy="{440+dy}" r="{r}"/>' for dx, dy, r in [(-12, 0, 9), (14, -40, 6), (-4, -90, 12), (20, -140, 7)])
        svg = (f'<g id="{p}-all"><g id="{p}-figw"><g id="{p}-fig0">{fig(p, 380, 440, 1.25)}</g></g>{water(p, 432, .8)}</g>'
               f'<g id="{p}-bub" fill="none" stroke="{WARM}" stroke-opacity=".7" stroke-width="2" opacity="0">{bub}</g>{timer_bar(p, labels)}')
        txt = _text(ctx, p, kick, number, unit, line, 130, 80, 38, 660, 110, 560)
        lat = ctx.t(ctx.p('line_at'), 1.5)
        js = f"""pose('{p}',380,440,1.25,{{aL:40,aR:-40,lL:6,lR:-6}});gsap.set('#{p}-mouth',{{opacity:1}});
drift('#{p}-water',{T:.3f},{D:.3f},-200);
{mk}
drop('#{p}-txt',{T + .05:.3f});write('#{p}-h',{lat:.3f},.8);
bob('#{p}-fig0',{T:.3f},.6,8,.3);
tl.to('#{p}-fig0',{{y:200,duration:1.9,ease:'power1.in'}},{sink:.3f});
tl.to('#{p}-eyes',{{opacity:0,duration:.01}},{sink:.3f});tl.to('#{p}-eyesX',{{opacity:1,duration:.01}},{sink:.3f});
tl.to('#{p}-armL',{{rotation:10,svgOrigin:'380 {440 - 78 * 1.25}',duration:1,ease:'power1.in'}},{sink:.3f});
tl.to('#{p}-armR',{{rotation:-10,svgOrigin:'380 {440 - 78 * 1.25}',duration:1,ease:'power1.in'}},{sink:.3f});
tl.fromTo('#{p}-bub',{{opacity:0,y:40}},{{keyframes:[{{opacity:1,y:0,duration:.2}},{{opacity:0,y:-200,duration:1.3}}]}},{dim + .3:.3f});
tl.fromTo('#{p}-dim',{{opacity:0}},{{opacity:{dto},duration:1.3,ease:'power1.in'}},{dim:.3f});"""
        ctx.sfx('ding_low', T, .25); ctx.sfx('downsweep', T + .1, .35)
    dimmer = f'<div id="{p}-dim" class="dimmer"></div>' if v == 'lights_out' else ''
    html = ctx.shot_div(f'<div id="{p}-kb" class="kb"><svg width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg>{txt}</div>{dimmer}', 'stick')
    ctx.js.append(js)
    return dict(html=html)
