from .common import *
META = dict(name='stick_rope', about='Story gag: a thrower in a boat throws a rope, it arcs over, then slips away. Two beats (rule 13).',
  variants=['rope_slip'],
  params={'label': 'word on the rope ("rope")', 'result': 'final line ("can\'t hold it")', 'throw_at': 'when the arm throws and the rope draws (time spec)',
          'label_at': 'when the label shows', 'slip_at': 'when the rope slips away and the arm drops', 'result_at': 'when the final line shows'})
def build(ctx):
    p = ctx.id; T = ctx.a; D = ctx.dur
    thr = ctx.t(ctx.p('throw_at'), .75); lab = ctx.t(ctx.p('label_at'), .95); slip = ctx.t(ctx.p('slip_at'), 2.56); res = ctx.t(ctx.p('result_at'), 2.2)
    svg = f'''<g id="{p}-all">
  <g id="{p}-figw">{fig(p, 330, 490, 1.15)}</g>{water(p, 450)}
  <g transform="translate(1030,486)"><g id="{p}-boatg"><path d="M-170,-30 L170,-30 L120,50 L-120,50 Z" fill="#26262c" stroke="#fff" stroke-width="7" stroke-linejoin="round"/>
    <g id="{p}-thrower">{fig(p + 't', 40, -112, .95)}</g></g></g>
  <g id="{p}-rope" fill="none" stroke="#d9b278" stroke-width="9" stroke-linecap="round"><path id="{p}-ropep" d="M1012,300 C900,110 560,120 376,342" stroke-dasharray="620" stroke-dashoffset="620"/></g>
  <text id="{p}-lbl" x="640" y="130" text-anchor="middle" class="itsv" style="font-size:56px" opacity="0">{esc(ctx.p('label', 'rope'))}</text>
 </g>'''
    html = ctx.shot_div(f'<div id="{p}-kb" class="kb"><svg width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg></div>'
        f'<div id="{p}-a" class="it op0" style="position:absolute;left:0;width:1280px;text-align:center;top:610px;font-size:46px;z-index:40">{rich(ctx.p("result", "can't hold it"))}</div>', 'stick')
    ctx.js.append(f"""pose('{p}',330,490,1.15,{{aL:25,aR:-150,lL:10,lR:-10}});
pose('{p}t',40,-112,.95,{{aL:145,aR:-20,lL:6,lR:-6}});
bob('#{p}-figw',{T:.3f},{D:.3f},8,.5);drift('#{p}-water',{T:.3f},{D:.3f},-200);
tl.fromTo('#{p}-boatg',{{y:0}},{{y:6,duration:.7,yoyo:true,repeat:5,ease:'sine.inOut'}},{T:.3f});
tl.to('#{p}t-armL',{{rotation:60,svgOrigin:'40 {-112 - 78 * .95}',duration:.25,ease:'power2.out'}},{thr - .05:.3f});
fadeIn('#{p}-lbl',{lab:.3f},.25);
tl.to('#{p}-ropep',{{attr:{{'stroke-dashoffset':0}},duration:.8,ease:'power1.out'}},{thr - .1:.3f});
tl.set('#{p}-lbl',{{opacity:0}},{res:.3f});
tl.to('#{p}-rope',{{y:190,x:-20,rotation:14,opacity:0,duration:.75,ease:'power2.in',svgOrigin:'376 342'}},{slip - .02:.3f});
tl.to('#{p}-armR',{{rotation:-35,svgOrigin:'330 {490 - 78 * 1.15}',duration:.5,ease:'power2.in'}},{res - .05:.3f});
write('#{p}-a',{res:.3f},.6);""")
    ctx.sfx('swoosh_rope', T + .35, .4); ctx.sfx('slide_down', slip, .35)
    return dict(html=html)
