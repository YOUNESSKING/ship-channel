from .common import *
META = dict(name='stick_gag', about='Generic stick gag that carries information: stick figure + big number + icon (+ optional timer bar). Use when none of the special gags fits (rule 9).',
  variants=['text_right', 'icon_pair'],
  params={'pose': '"tread" (default), "gasp", "float" or "sink"', 'kicker': 'small caps line', 'number': 'big number', 'unit': 'italic unit', 'line': 'italic line under the number',
          'number_at': 'when the number shows (time spec)', 'line_at': 'when the line shows', 'icon': 'icon name (boat, wetsuit, lifering, bottle, flame, phone, fish, snowflake, thermometer, clock, hand, rope, shore, shark, penguin, person, orca, salt, mussel, dice, hut, bowl, river, tree, croc) or raw svg',
          'icon_label': 'caps label under the icon', 'icon_at': 'when the icon pops', 'cross': 'draw a gold X over the icon 0.3 s later',
          'timer': '{"from":0,"to":1,"labels":[...]} - show the timer bar and move the marker'})
def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a; D = ctx.dur
    pose = ctx.p('pose', 'tread'); kick = ctx.p('kicker', ''); number = ctx.p('number', ''); unit = ctx.p('unit', ''); line = ctx.p('line', '')
    nat = ctx.t(ctx.p('number_at'), .4); lat = ctx.t(ctx.p('line_at'), 1.0); ic = ctx.p('icon'); il = ctx.p('icon_label', ''); iat = ctx.t(ctx.p('icon_at'), .5)
    cross = ctx.p('cross', False); tm = ctx.p('timer')
    if v == 'text_right': hx, hy, s, wy, ix, iy = 380, 470, 1.25, 432, 380, 190
    else: hx, hy, s, wy, ix, iy = 330, 490, 1.15, 450, 900, 400
    pj = {'tread': (78, -78, 72, 104, .34), 'gasp': (140, -140, 118, 152, .22), 'float': (70, -70, 40, 60, .6), 'sink': (40, -40, 10, 20, .6)}[pose]
    svg = f'<g id="{p}-all"><g id="{p}-figw"><g id="{p}-fig0">{fig(p, hx, hy, s)}</g></g>{water(p, wy, .8)}'
    js = [f"pose('{p}',{hx},{hy},{s},{{aL:{pj[0]},aR:{pj[1]},lL:10,lR:-10}});flail('{p}',{hx},{hy},{s},{T:.3f},{D:.3f},{pj[2]},{pj[3]},{pj[4]});",
          f"bob('#{p}-fig0',{T:.3f},{D:.3f},9,.45);drift('#{p}-water',{T:.3f},{D:.3f},-200);kb('#{p}-kb',{T:.3f},{ctx.b:.3f},1.0,1.05,'30% 50%');"]
    if pose == 'gasp': js.append(f"gsap.set('#{p}-mouth',{{opacity:0}});gsap.set('#{p}-mouthO',{{opacity:1}});")
    if ic:
        sc = .8 if v == 'text_right' else 1.0
        svg += f'<g id="{p}-ic" transform="translate({ix},{iy}) scale({sc})"><g id="{p}-icin" opacity="0">{icon(ic)}</g></g>'
        if cross: svg += xmark(f'{p}-x', ix, iy, int((64 if v == 'text_right' else 78)))
        if il: svg += f'<text id="{p}-icl" x="{ix}" y="{iy + (96 if v == "icon_pair" else 90)}" text-anchor="middle" class="lblm" opacity="0">{esc(il)}</text>'
        js.append(f"pop('#{p}-icin',{iat - .1:.3f},.22,{{icon:true,from:.2,svgOrigin:'0 0'}});" + (f"fadeIn('#{p}-icl',{iat:.3f},.2);" if il else ''))
        if cross: js.append(f"hidden('#{p}-x');pop('#{p}-x',{iat + .3:.3f},.14,{{icon:true,from:.3,svgOrigin:'{ix} {iy}'}});"); ctx.sfx('click', iat + .3, .6)
        else: ctx.sfx('click', iat, .4)
    svg += '</g>'
    txt = ''
    if tm:
        svg += timer_bar(p, tm.get('labels')); js.append(f"mark('{p}',{T:.3f},{X0[tm.get('from', 0)]},{X0[tm.get('to', 1)]},.45);")
    if v == 'text_right':
        txt = block(f'{p}-txt', 660, 110, 560, (f'<div class="jo gold">{rich(kick)}</div>' if kick else '') + (num(f'{p}-n', number, unit, 130, 80, 'margin-top:16px') if number else '')
                    + (f'<div class="gr l"></div><div id="{p}-h" class="it" style="font-size:36px">{rich(line)}</div>' if line else ''), 'left')
        js.append(f"drop('#{p}-txt',{nat:.3f});" + (f"write('#{p}-h',{lat:.3f},.8);" if line else ''))
    else:
        if number or kick:
            svg2 = (f'<text id="{p}-k" x="900" y="150" text-anchor="middle" class="tbl" style="font-size:18px" opacity="0">{esc(kick.upper())}</text>' if kick else '')
            svg2 += (f'<text id="{p}-nn" x="900" y="232" text-anchor="middle" class="itsv" style="font-size:78px" opacity="0">{rich(str(number) + (" " + unit if unit else ""))}</text>' if number else '')
            svg = svg.replace(f'<g id="{p}-all">', f'<g id="{p}-all">' + svg2, 1)
            js.append(f"pop('#{p}-k',{nat - .1:.3f},.4);pop('#{p}-nn',{nat:.3f},.4);")
        if line: txt = f'<div id="{p}-h" class="it op0" style="position:absolute;left:0;width:1280px;text-align:center;top:590px;font-size:44px;z-index:40">{rich(line)}</div>'; js.append(f"write('#{p}-h',{lat:.3f},.6);")
    html = ctx.shot_div(f'<div id="{p}-kb" class="kb"><svg width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg>{txt if v == "text_right" else ""}</div>{txt if v != "text_right" else ""}', 'stick')
    ctx.js.append('\n'.join(js))
    return dict(html=html)
