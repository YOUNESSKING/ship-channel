from .common import *
META = dict(name='stick_land', about='Story gag: the figure falls from the top of the picture (as if dropped offshore) and lands on dry ground instead of water: soft thud, dust puff, a label on its word. Same figure and line style as stick_water (gap T4).',
  variants=['grass', 'snow'],
  params={'label': 'word that appears after the landing (default "grass" / "snow")', 'label_at': 'when the label shows (time spec)', 'land_at': 'when the feet touch the ground (time spec; default 1.1 s)',
          'result': 'optional italic line under the figure (e.g. "dry")', 'result_at': 'when the result line shows', 'water_hint': 'true = a faint dashed wave where the water should have been, which vanishes on landing (default true)'})
def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a; D = ctx.dur
    land = ctx.t(ctx.p('land_at'), 1.1); lab = ctx.p('label', 'grass' if v == 'grass' else 'snow'); lat = ctx.t(ctx.p('label_at'), (land - T) + .5)
    res = ctx.p('result', ''); rat = ctx.t(ctx.p('result_at'), (land - T) + 1.2); hint = ctx.p('water_hint', True)
    s = 1.15; gy = 548; hx = 470; hy = gy - 84 * s; col = '#8a9a62' if v == 'grass' else '#f6efe0'
    ground = f'<path d="M-100,{gy} H1400 V800 H-100 Z" fill="#101a1f" fill-opacity=".85"/><line x1="-100" y1="{gy}" x2="1400" y2="{gy}" stroke="{col}" stroke-width="3.5" stroke-linecap="round"/>'
    if v == 'grass':
        for i in range(-2, 36): x = i * 38 + (i % 3) * 7; ground += f'<path d="M{x},{gy} l-5,-15 M{x},{gy} l1,-20 M{x},{gy} l6,-14" stroke="{col}" stroke-width="3" stroke-linecap="round" fill="none"/>'
    else:
        for i in range(-1, 14): x = i * 112 + (i % 2) * 30; ground += f'<path d="M{x},{gy} q30,-26 60,0" stroke="{col}" stroke-width="3" fill="#1b252a" stroke-linecap="round"/>'
    ghost = f'<path id="{p}-ghost" d="{waterline(gy - 6, 1500, 8, 110)}" fill="none" stroke="{GOLD}" stroke-width="2.5" stroke-dasharray="4 12" stroke-linecap="round" stroke-opacity=".6"/>' if hint else ''
    puff = ''.join(f'<circle id="{p}-pf{k}" cx="{hx}" cy="{gy - 8}" r="{10 + (k % 3) * 4}" fill="{col}" fill-opacity=".55" opacity="0"/>' for k in range(7))
    svg = (f'<g id="{p}-all">{ghost}<g id="{p}-figw"><g id="{p}-sq">{fig(p, hx, hy, s)}</g></g>{ground}{puff}'
           f'<g id="{p}-lbl" opacity="0"><text x="{hx + 250}" y="{gy + 86}" class="itsv" style="font-size:64px">{rich_svg(lab)}</text><path d="M{hx + 236},{gy + 62} C{hx + 170},{gy + 40} {hx + 110},{gy + 26} {hx + 60},{gy + 14}" stroke="{GOLD}" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M{hx + 60},{gy + 14} l16,-2 M{hx + 60},{gy + 14} l8,14" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" fill="none"/></g></g>')
    html = ctx.shot_div(f'<div id="{p}-kb" class="kb"><svg width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg></div>'
                        + (f'<div id="{p}-a" class="it op0" style="position:absolute;left:0;width:1280px;text-align:center;top:112px;font-size:46px;z-index:40">{rich(res)}</div>' if res else ''), 'stick')
    fall = 0.78; x0 = hy + 112 * s + 40
    ctx.js.append(f"""pose('{p}',{hx},{hy},{s},{{aL:150,aR:-150,lL:22,lR:-22}});
gsap.set('#{p}-mouth',{{opacity:0}});gsap.set('#{p}-mouthO',{{opacity:1}});
gsap.set('#{p}-figw',{{y:{-(hy + 190):.0f}}});
tl.to('#{p}-figw',{{y:0,duration:{fall},ease:'power2.in'}},{land - fall:.3f});
tl.fromTo('#{p}-armL',{{rotation:150,svgOrigin:'{hx} {hy - 78 * s:.1f}'}},{{rotation:120,svgOrigin:'{hx} {hy - 78 * s:.1f}',duration:.2,yoyo:true,repeat:{int(fall / .2)},ease:'sine.inOut'}},{land - fall:.3f});
tl.fromTo('#{p}-armR',{{rotation:-150,svgOrigin:'{hx} {hy - 78 * s:.1f}'}},{{rotation:-120,svgOrigin:'{hx} {hy - 78 * s:.1f}',duration:.2,yoyo:true,repeat:{int(fall / .2)},ease:'sine.inOut'}},{land - fall + .1:.3f});
tl.set('#{p}-mouthO',{{opacity:0}},{land:.3f});tl.set('#{p}-mouth',{{opacity:1}},{land:.3f});
tl.to('#{p}-armL',{{rotation:12,svgOrigin:'{hx} {hy - 78 * s:.1f}',duration:.25,ease:'power2.out'}},{land + .02:.3f});tl.to('#{p}-armR',{{rotation:-12,svgOrigin:'{hx} {hy - 78 * s:.1f}',duration:.25,ease:'power2.out'}},{land + .02:.3f});
tl.to('#{p}-legL',{{rotation:6,svgOrigin:'{hx} {hy}',duration:.2}},{land:.3f});tl.to('#{p}-legR',{{rotation:-6,svgOrigin:'{hx} {hy}',duration:.2}},{land:.3f});
tl.fromTo('#{p}-sq',{{scaleY:1,svgOrigin:'{hx} {gy}'}},{{scaleY:.9,svgOrigin:'{hx} {gy}',duration:.07,yoyo:true,repeat:1,ease:'power2.out'}},{land:.3f});
{''.join(f"tl.fromTo('#{p}-pf{k}',{{x:0,y:0,scale:.4,opacity:.7}},{{x:{(k - 3) * 42},y:{-12 - (k % 3) * 9},scale:{1.6 + (k % 3) * .4},opacity:0,duration:.7,ease:'power2.out',transformOrigin:'{hx}px {gy - 8}px'}},{land:.3f});" for k in range(7))}
{f"tl.to('#{p}-ghost',{{opacity:0,duration:.15}},{land - .05:.3f});" if hint else ''}
pop('#{p}-lbl',{lat:.3f},.5);
{f"write('#{p}-a',{rat:.3f},.6);" if res else ''}""")
    ctx.sfx('thud_soft', land, .55); ctx.sfx('tok', land + .05, .3); ctx.sfx('click', lat, .3)
    return dict(html=html)
