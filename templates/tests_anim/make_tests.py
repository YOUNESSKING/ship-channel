#!/usr/bin/env python3
"""Three animation tests in our style C (gold line art on warm dark), after studying Depth Theory's animation grammar
(research/depththeory-spermwhale-study.md): fast snap-in + slow drift, count-up that lands with flash + ring, a mini scene per idea,
constant small motion, one sound per graphic event. Numbers are TEST values (to be checked against the V03 fact sheet, rule 82).
Tiger drawing: PhyloPic 70b87132 by Andy Wilson, CC0 (public domain).

  python3 make_tests.py            # writes work/t1..t3 (HyperFrames projects) + audio, then:
  ./render_tests.sh                # renders, mixes, muxes -> out/test1_lockon.mp4 ... + out/ALL_TESTS.mp4
"""
import os, re, sys, json, shutil, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TPL = os.path.dirname(HERE)
sys.path.insert(0, TPL)
from blocks.common import fig, ICONS, GOLD, WARM, SOFT, ITAL
import sfx_voices as V

W, H = 1280, 720

def tiger(i, x, y, w, flip=True, op=1):
    """Tiger (PhyloPic 70b87132, CC0), recoloured: amber body, dark stripes, warm rim (tiger_fill.png, 2304x1055). Faces right when flip=True."""
    h = w * 1055 / 2304
    return (f'<div id="{i}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;opacity:{op}">'
            f'<img src="assets/tiger_fill.png" style="width:100%;height:100%;display:block;{"transform:scaleX(-1)" if flip else ""}"></div>')

CSS = '''
html,body,#root{margin:0;width:1280px;height:720px;background:#000;overflow:hidden}
.abs{position:absolute}
#scene{position:absolute;left:0;top:0;width:1280px;height:720px;overflow:hidden;background:radial-gradient(ellipse at 55% 45%,#221c14 0%,#120f0b 55%,#070605 100%)}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0) 45%,rgba(0,0,0,.75) 100%);pointer-events:none}
.kick{font-family:Jost;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:#f6efe0;font-size:22px}
.big{font-family:"Cormorant Garamond";font-weight:600;color:#f6efe0}
.it{font-family:"Cormorant Garamond";font-style:italic;color:#d9bd7e}
.hair{position:absolute;height:2px;background:#c9a45c}
.flash{position:absolute;inset:0;background:#fff3d6;opacity:0;mix-blend-mode:screen}
'''

def page(dur, body, js, bg='radial-gradient(ellipse at 55% 45%,#173126 0%,#0c1712 55%,#040806 100%)'):
    fonts = open(os.path.join(TPL, 'lib', 'fonts_face.css')).read()
    rt = open(os.path.join(TPL, 'lib', 'runtime.js')).read()
    return f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width={W}, height={H}"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>{fonts}{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="{W}" data-height="{H}">
<div id="scene" class="clip" data-start="0" data-duration="{dur}" data-track-index="0" style="background:{bg}">{body}</div></div>
<script>{rt}
{js}
window.__timelines = window.__timelines || {{}}; window.__timelines['main'] = tl;</script></body></html>'''

def leaves(i, seed, n, y0, y1, scale, col, op):
    r = np.random.default_rng(seed); out = [f'<g id="{i}" opacity="{op}">']
    for _ in range(n):
        x = r.uniform(-150, 1450); y = r.uniform(y0, y1); a = r.uniform(-70, 70); L = r.uniform(90, 220) * scale; wd = L * r.uniform(.22, .34)
        out.append(f'<g transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})"><path d="M0,0 C{wd:.0f},{-L*.3:.0f} {wd*.6:.0f},{-L*.8:.0f} 0,{-L:.0f} C{-wd*.6:.0f},{-L*.8:.0f} {-wd:.0f},{-L*.3:.0f} 0,0 Z" fill="{col}"/>'
                   f'<path d="M0,0 L0,{-L*.95:.0f}" stroke="#2c4d3a" stroke-width="2" opacity=".6"/></g>')
    return ''.join(out) + '</g>'

# ------------------------------------------------------------------ TEST 1: lock-on (hook style)
def test1():
    D = 9.0
    body = (f'<svg class="abs" style="left:0;top:0" width="1280" height="720" viewBox="0 0 1280 720">'
            f'<ellipse cx="900" cy="300" rx="420" ry="260" fill="#e0a24a" opacity=".10"/>'
            f'<g id="back">{leaves("lb", 1, 70, 60, 700, .9, "#1e3d2e", 1)}</g>'
            f'<g id="eyes" opacity="0"><g transform="translate(960,318)"><ellipse id="eL" cx="-17" cy="0" rx="9" ry="6" fill="#e8b04a"/><ellipse id="eR" cx="17" cy="0" rx="9" ry="6" fill="#e8b04a"/>'
            f'<ellipse cx="-17" cy="0" rx="2.2" ry="5" fill="#120f0b"/><ellipse cx="17" cy="0" rx="2.2" ry="5" fill="#120f0b"/></g>'
            f'<ellipse cx="960" cy="318" rx="70" ry="30" fill="#e8b04a" opacity=".10"/></g>'
            f'<path d="M-50,560 C300,548 800,566 1350,552 L1350,720 L-50,720 Z" fill="#08140e"/>'
            f'<g id="you">{fig("u", 430, 480, .95)}</g>'
            f'<g id="br" stroke="{GOLD}" stroke-width="4" fill="none" stroke-linecap="square">'
            f'<path id="b1" d="M0,22 V0 H22"/><path id="b2" d="M0,-22 V0 H22"/><path id="b3" d="M0,22 V0 H-22"/><path id="b4" d="M0,-22 V0 H-22"/></g>'
            f'<g id="front">{leaves("lf", 7, 26, 600, 760, 1.6, "#0a1a12", 1)}{leaves("lf2", 9, 10, -40, 120, 1.5, "#0a1a12", 1)}</g></svg>'
            + tiger('tg', 1300, 330, 470, flip=False)
            + f'<svg class="abs" style="left:0;top:0" width="1280" height="720"><g>{leaves("lf3", 21, 9, 560, 740, 1.7, "#07140e", 1)}</g></svg>'
            + '<div id="t1k" class="abs kick" style="left:0;width:1280px;top:612px;text-align:center;opacity:0">IT ALREADY <span class="it" style="font-size:34px;letter-spacing:.02em;text-transform:none">sees</span> YOU</div>'
            + '<div id="t1h" class="hair" style="left:560px;width:160px;top:655px;opacity:0"></div><div class="vig"></div><div id="fl" class="flash"></div>')
    hx, hy = 430, 430   # bracket centre (around the figure)
    js = f'''
tl.fromTo('#scene',{{opacity:0}},{{opacity:1,duration:.6,ease:'none'}},0);
tl.fromTo('#scene',{{scale:1}},{{scale:1.06,duration:{D},ease:'none',transformOrigin:'40% 55%'}},0);
tl.fromTo('#back',{{x:0}},{{x:-30,duration:{D},ease:'none'}},0);
tl.fromTo('#front',{{x:0}},{{x:-90,duration:{D},ease:'none'}},0);
pose('u',430,480,.95,{{aL:20,aR:-20,lL:16,lR:-16}});
tl.fromTo('#u-legL',{{rotation:16,svgOrigin:'430 480'}},{{rotation:-16,svgOrigin:'430 480',duration:.38,yoyo:true,repeat:9,ease:'sine.inOut'}},0.2);
tl.fromTo('#u-legR',{{rotation:-16,svgOrigin:'430 480'}},{{rotation:16,svgOrigin:'430 480',duration:.38,yoyo:true,repeat:9,ease:'sine.inOut'}},0.2);
tl.fromTo('#you',{{x:-120}},{{x:0,duration:3.6,ease:'power1.out'}},0.2);
bob('#you',0.2,3.6,-4,.19);
tl.fromTo('#eyes',{{opacity:0}},{{opacity:1,duration:.12}},2.0);
tl.fromTo(['#eL','#eR'],{{scaleY:0,transformOrigin:'50% 50%'}},{{scaleY:1,duration:.18,ease:'power2.out'}},2.0);
tl.to(['#eL','#eR'],{{scaleY:.1,duration:.07,yoyo:true,repeat:1,transformOrigin:'50% 50%'}},3.05);
const C=[[{hx-150},{hy-190},{hx-62},{hy-118},'#b1'],[{hx-150},{hy+150},{hx-62},{hy+70},'#b2'],[{hx+150},{hy-190},{hx+62},{hy-118},'#b3'],[{hx+150},{hy+150},{hx+62},{hy+70},'#b4']];
C.forEach(c=>{{tl.fromTo(c[4],{{x:c[0],y:c[1],opacity:0}},{{x:c[2],y:c[3],opacity:1,duration:.32,ease:'power3.out'}},3.6);}});
C.forEach(c=>{{tl.to(c[4],{{x:c[2]+(c[2]<{hx}?-6:6),y:c[3]+(c[3]<{hy}?-6:6),duration:.5,yoyo:true,repeat:5,ease:'sine.inOut'}},3.95);}});
tl.fromTo('#t1k',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.45,ease:'power2.out'}},4.05);
tl.fromTo('#t1h',{{scaleX:0,opacity:1,transformOrigin:'50% 50%'}},{{scaleX:1,duration:.5,ease:'power2.out'}},4.2);
tl.to('#eyes',{{opacity:0,duration:.3}},5.3);
tl.fromTo('#tg',{{x:0}},{{x:-560,duration:1.5,ease:'power2.out'}},5.4);
tl.fromTo('#fl',{{opacity:0}},{{opacity:.18,duration:.06,yoyo:true,repeat:1}},6.85);
tl.to('#scene',{{opacity:0,duration:.4}},{D-.4});
'''
    ev = [('jungle', 0, .55, D), ('drone', 0, .5, D), ('growl', 2.0, .55), ('beep', 3.6, .5), ('tick', 3.6, .7), ('swoosh', 5.4, .5), ('growl', 6.2, .9), ('thud', 6.85, .55)]
    return D, page(D, body, js), ev

# ------------------------------------------------------------------ TEST 2: gauge (count-up lands with flash + ring)
def test2():
    D = 9.0; L0, L1 = 330, 1110   # bar from x to x
    hand = ICONS['hand']
    body = ('<div id="k2" class="abs kick" style="left:110px;top:92px;opacity:0">Bite force</div><div id="k2h" class="hair" style="left:110px;top:130px;width:220px;opacity:0"></div>'
            f'<svg class="abs" style="left:0;top:0" width="1280" height="720" viewBox="0 0 1280 720">'
            f'<g id="r1" opacity="0"><g transform="translate(205,272) scale(.55)">{hand}</g>'
            f'<line x1="{L0}" y1="272" x2="{L1}" y2="272" stroke="{WARM}" stroke-opacity=".18" stroke-width="16" stroke-linecap="round"/>'
            f'<line id="bar1" x1="{L0}" y1="272" x2="{L0}" y2="272" stroke="{SOFT}" stroke-width="16" stroke-linecap="round"/></g>'
            f'<g id="r2" opacity="0"><line x1="{L0}" y1="452" x2="{L1}" y2="452" stroke="{WARM}" stroke-opacity=".18" stroke-width="16" stroke-linecap="round"/>'
            f'<line id="bar2" x1="{L0}" y1="452" x2="{L0}" y2="452" stroke="{GOLD}" stroke-width="16" stroke-linecap="round"/></g>'
            f'<circle id="ring" cx="{L1}" cy="452" r="10" fill="none" stroke="{GOLD}" stroke-width="3" opacity="0"/>'
            f'<circle id="ring2" cx="{L1}" cy="452" r="10" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0"/>'
            f'<path id="circ" d="M1060,532 C1150,530 1196,552 1192,580 C1188,612 1100,622 1020,618 C950,614 912,596 918,570 C924,544 990,534 1080,536" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
            f'</svg>'
            + tiger('tg2', 92, 400, 220, op=0)
            + '<div id="l1" class="abs kick" style="left:110px;top:316px;opacity:0;font-size:18px">You</div>'
            + '<div id="l2" class="abs kick" style="left:110px;top:510px;opacity:0;font-size:18px">Tiger</div>'
            + f'<div id="n1" class="abs big" style="left:{L0}px;top:296px;font-size:40px;opacity:0"></div>'
            + '<div id="n2" class="abs big" style="left:930px;top:520px;width:240px;text-align:right;font-size:64px;opacity:0"></div>'
            + '<div id="it2" class="abs it" style="left:0;width:1280px;top:630px;text-align:center;font-size:36px;opacity:0">more than six times yours</div>'
            + '<div class="abs" style="right:24px;bottom:16px;font:13px Jost;letter-spacing:.15em;color:#f6efe0;opacity:.35">TEST NUMBERS</div>'
            + '<div class="vig"></div><div id="fl2" class="flash"></div>')
    x1 = L0 + (L1 - L0) * 160 / 1050
    js = f'''
tl.fromTo('#scene',{{opacity:0}},{{opacity:1,duration:.4,ease:'none'}},0);
tl.fromTo('#scene',{{scale:1}},{{scale:1.04,duration:{D},ease:'none'}},0);
pop('#k2',.2); tl.fromTo('#k2h',{{scaleX:0,opacity:1,transformOrigin:'0 50%'}},{{scaleX:1,duration:.5,ease:'power2.out'}},.35);
tl.fromTo('#r1',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.35,ease:'power3.out'}},.9); pop('#l1',1.0);
tl.fromTo('#bar1',{{attr:{{x2:{L0}}}}},{{attr:{{x2:{x1:.0f}}},duration:.7,ease:'power2.out'}},1.3);
tl.set('#n1',{{opacity:1,x:0}},1.3); tl.to('#n1',{{x:{x1-L0+24:.0f},duration:.7,ease:'power2.out'}},1.3);
counter('#n1',1.3,.7,0,160,v=>Math.round(v)+'<i class="it" style="font-size:24px"> psi</i>','power2.out');
tl.fromTo('#r2',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.35,ease:'power3.out'}},2.6);
tl.fromTo('#tg2',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.35,ease:'power3.out'}},2.6); pop('#l2',2.7);
tl.fromTo('#bar2',{{attr:{{x2:{L0}}}}},{{attr:{{x2:{L1}}},duration:1.5,ease:'power2.in'}},3.1);
tl.set('#n2',{{opacity:1}},3.1); counter('#n2',3.1,1.5,0,1050,v=>Math.round(v).toLocaleString('en-US')+'<i class="it" style="font-size:30px"> psi</i>','power2.in');
tl.fromTo('#fl2',{{opacity:0}},{{opacity:.28,duration:.05}},4.6); tl.to('#fl2',{{opacity:0,duration:.45}},4.65);
tl.fromTo('#ring',{{attr:{{r:10}},opacity:1}},{{attr:{{r:170}},opacity:0,duration:.9,ease:'power2.out'}},4.6);
tl.fromTo('#ring2',{{attr:{{r:10}},opacity:.8}},{{attr:{{r:260}},opacity:0,duration:1.3,ease:'power2.out'}},4.7);
tl.fromTo('#n2',{{scale:1.18,transformOrigin:'100% 50%'}},{{scale:1,duration:.4,ease:'power3.out'}},4.6);
tl.fromTo('#circ',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.4,ease:'power1.out'}},5.5);
tl.fromTo('#it2',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.6,ease:'power2.out'}},6.1);
tl.to('#scene',{{opacity:0,duration:.4}},{D-.4});
'''
    ev = [('drone', 0, .5, D), ('swoosh', .9, .3), ('ticks', 1.3, .35, .7), ('swoosh', 2.6, .3), ('ticks_up', 3.1, .45, 1.5), ('thud', 4.6, 1.0), ('shimmer', 4.6, .35), ('marker', 5.5, .5), ('growl', 4.75, .35)]
    return D, page(D, body, js), ev

# ------------------------------------------------------------------ TEST 3: options list -> mini scene -> strike
def test3():
    D = 10.0
    items = ['1. Run', '2. Climb a tree', '3. Stare it down']
    lst = ''.join(f'<div id="o{i}" class="abs big" style="left:420px;top:{240+i*82}px;font-size:46px;opacity:0">{t}</div>' for i, t in enumerate(items))
    tree = (f'<g id="tree" opacity="0" stroke="{WARM}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="#11241a">'
            f'<path d="M560,600 C566,480 552,360 570,200 L604,200 C596,360 610,480 616,600 Z"/>'
            f'<path d="M584,330 C640,300 700,296 760,270 M580,260 C520,232 470,230 420,206 M590,214 C600,170 586,140 600,110" fill="none"/>'
            f'<path d="M380,210 C360,150 420,90 500,100 C540,40 650,40 690,100 C770,90 820,160 790,220 C820,270 760,300 700,280 C640,310 520,300 470,270 C410,280 360,260 380,210 Z" fill="#16301f" stroke-width="5" opacity=".95"/></g>')
    body = ('<div id="q" class="abs kick" style="left:0;width:1280px;top:140px;text-align:center;opacity:0;font-size:24px">What would you do?</div>'
            '<div id="qh" class="hair" style="left:560px;width:160px;top:182px;opacity:0"></div>'
            f'<div id="lst">{lst}<svg class="abs" style="left:0;top:0;overflow:visible" width="1280" height="720">'
            f'<rect id="box" x="396" y="316" width="440" height="68" rx="6" fill="none" stroke="{GOLD}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
            f'<line id="strike" x1="410" y1="352" x2="820" y2="348" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg></div>'
            f'<div id="mini" style="position:absolute;inset:0;opacity:0"><svg class="abs" style="left:0;top:0" width="1280" height="720" viewBox="0 0 1280 720">'
            f'<path d="M-20,600 C300,594 900,606 1300,598" fill="none" stroke="{SOFT}" stroke-width="3" opacity=".6"/>{tree}'
            f'<g id="you3">{fig("v", 690, 240, .62)}</g>'
            f'<line id="hgt" x1="300" y1="600" x2="300" y2="250" stroke="{GOLD}" stroke-width="3" opacity="0"/>'
            f'<path id="hgt2" d="M288,250 h24 M288,600 h24" stroke="{GOLD}" stroke-width="3" opacity="0"/></svg>'
            + tiger('tg3', 1300, 445, 380, flip=False)
            + '<div id="hl" class="abs" style="left:210px;top:395px;opacity:0"><span class="big" style="font-size:44px">5</span><i class="it" style="font-size:26px"> m</i></div>'
            + '<div id="lab3" class="abs kick" style="left:0;width:1280px;top:650px;text-align:center;opacity:0">Tigers leap</div></div>'
            + '<div id="bad" class="abs it" style="left:0;width:1280px;top:560px;text-align:center;font-size:40px;opacity:0">Bad plan.</div>'
            + '<div class="abs" style="right:24px;bottom:16px;font:13px Jost;letter-spacing:.15em;color:#f6efe0;opacity:.35">TEST NUMBERS</div><div class="vig"></div>')
    js = f'''
tl.fromTo('#scene',{{opacity:0}},{{opacity:1,duration:.4,ease:'none'}},0);
pop('#q',.25); tl.fromTo('#qh',{{scaleX:0,opacity:1,transformOrigin:'50% 50%'}},{{scaleX:1,duration:.5,ease:'power2.out'}},.4);
['#o0','#o1','#o2'].forEach((s,i)=>tl.fromTo(s,{{opacity:0,x:-24}},{{opacity:1,x:0,duration:.3,ease:'power3.out'}},.9+i*.38));
tl.fromTo('#box',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.45,ease:'power2.out'}},2.3);
tl.to(['#o0','#o2'],{{opacity:.35,duration:.3}},2.4);
tl.to('#lst',{{opacity:0,x:-60,duration:.35,ease:'power2.in'}},3.0); tl.to(['#q','#qh'],{{opacity:0,duration:.3}},3.0);
tl.fromTo('#mini',{{opacity:0}},{{opacity:1,duration:.35}},3.2);
tl.fromTo('#tree',{{opacity:0,y:20}},{{opacity:1,y:0,duration:.4,ease:'power3.out'}},3.25);
tl.fromTo('#you3',{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.35,ease:'power3.out'}},3.45);
pose('v',690,240,.62,{{aL:150,aR:-150,lL:30,lR:-30}});
tl.fromTo('#tg3',{{x:0}},{{x:-540,duration:1.6,ease:'power2.out'}},3.6);
tl.to('#tg3',{{x:-610,y:-175,rotation:22,duration:.42,ease:'power2.out',transformOrigin:'70% 80%'}},5.6);
tl.to('#tg3',{{y:-150,duration:.6,ease:'sine.inOut'}},6.02);
tl.set('#v-eyes',{{opacity:0}},5.7); tl.set('#v-eyesX',{{opacity:1}},5.7); tl.set('#v-mouth',{{opacity:0}},5.7); tl.set('#v-mouthO',{{opacity:1}},5.7);
tl.fromTo('#you3',{{x:0}},{{x:-4,duration:.05,yoyo:true,repeat:9}},5.7);
tl.fromTo('#hgt',{{opacity:1,attr:{{y2:600}}}},{{attr:{{y2:250}},duration:.5,ease:'power2.out'}},5.75); tl.to('#hgt2',{{opacity:1,duration:.2}},6.1);
tl.fromTo('#hl',{{opacity:0,x:-10}},{{opacity:1,x:0,duration:.35,ease:'power3.out'}},6.2);
pop('#lab3',6.3);
tl.to('#mini',{{opacity:0,duration:.35}},7.6);
tl.to('#lst',{{opacity:1,x:0,duration:.35,ease:'power2.out'}},7.8);
tl.fromTo('#strike',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.35,ease:'power1.inOut'}},8.25);
tl.to('#o1',{{opacity:.45,duration:.3}},8.5);
tl.fromTo('#bad',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.5,ease:'power2.out'}},8.75);
tl.to('#scene',{{opacity:0,duration:.4}},{D-.4});
'''
    ev = [('drone', 0, .5, D), ('click', .9, .5), ('click', 1.28, .5), ('click', 1.66, .5), ('tok', 2.3, .7), ('swoosh', 3.1, .4), ('jungle', 3.2, .35, 4.4),
          ('growl', 4.2, .5), ('swoosh', 5.55, .55), ('growl', 5.6, .95), ('thud', 5.98, .5), ('tick', 6.2, .4), ('swoosh', 7.7, .3), ('scratch', 8.25, .8), ('tok', 8.75, .6)]
    return D, page(D, body, js), ev

# ------------------------------------------------------------------ sound (all synthesised, like sfx_voices)
SR = V.SR
def jungle(d):
    n = int(d * SR); t = np.arange(n) / SR; y = V.bp(V.noise(n), 3800, 6500) * .25 * (0.6 + .4 * np.sin(2 * np.pi * 13 * t) ** 8)
    for k in range(int(d * 2.2)):   # cricket / frog chirps
        a = V.rng.uniform(0, d - .3); f = V.rng.uniform(2600, 5200); m = int(.18 * SR); tt = np.arange(m) / SR
        ch = np.sin(2 * np.pi * f * tt) * (np.sin(2 * np.pi * 38 * tt) > .2) * np.sin(np.pi * tt / .18) * .12
        V.put(y, ch, a)
    y += V.lp(V.noise(n), 260, 2) * .5
    return y * np.minimum(1, t / .8) * np.minimum(1, (d - t) / .8)
def drone(d):
    n = int(d * SR); t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * 55 * t) + .6 * np.sin(2 * np.pi * 82.4 * t + .3) + .35 * np.sin(2 * np.pi * 110 * t)) * (0.75 + .25 * np.sin(2 * np.pi * .21 * t))
    y = V.lp(y + .3 * V.lp(V.noise(n), 180), 400) ; return V.nrm(y) * np.minimum(1, t / 1.5) * np.minimum(1, (d - t) / 1.0)
def growl(d=1.3):
    n = int(d * SR); t = np.arange(n) / SR
    y = V.bp(V.noise(n), 70, 520) * (0.55 + .45 * np.sin(2 * np.pi * 27 * t)) * np.sin(np.pi * np.minimum(t / d, 1)) ** .7
    y += .5 * np.sin(2 * np.pi * np.cumsum(70 + 18 * np.sin(2 * np.pi * 3 * t)) / SR) * np.sin(np.pi * t / d)
    return V.nrm(V.lp(y, 700))
def beep(d=1.0):
    n = int(d * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1180 * t) * np.minimum(1, t / .01) * np.minimum(1, (d - t) / .12) * .5
def tick(): n = int(.03 * SR); t = np.arange(n) / SR; return V.nrm(V.hp(V.noise(n), 2500) * np.exp(-t * 250))
def ticks(d, accel=False):
    out = np.zeros(int((d + .1) * SR)); k = 0; tt = 0
    while tt < d:
        V.put(out, tick(), tt, .6); k += 1
        tt = d * (k / 16) ** (0.5 if accel else 1.6) if True else 0
    return out
def shimmer(d=1.4):
    n = int(d * SR); t = np.arange(n) / SR
    return V.nrm(sum(np.sin(2 * np.pi * f * t) for f in (1568, 2093, 2637))) * np.exp(-t * 3) * .5
def marker():
    n = int(.4 * SR); t = np.arange(n) / SR; return V.nrm(V.bp(V.noise(n), 1500, 6000) * np.sin(np.pi * t / .4) ** 2) * .6

CUE = {'jungle': lambda d: jungle(d), 'drone': lambda d: drone(d), 'growl': lambda d: growl(), 'beep': lambda d: beep(1.0), 'tick': lambda d: tick(),
       'ticks': lambda d: ticks(d), 'ticks_up': lambda d: ticks(d, True), 'swoosh': lambda d: V.swoosh(.45), 'thud': lambda d: V.thud(),
       'shimmer': lambda d: shimmer(), 'marker': lambda d: marker(), 'click': lambda d: V.click(), 'tok': lambda d: V.tok(), 'scratch': lambda d: V.scratch()}

def audio(D, ev, path):
    import wave
    buf = np.zeros(int((D + .5) * SR))
    for e in ev:
        cue, at, g = e[0], e[1], e[2]; d = e[3] if len(e) > 3 else None
        V.put(buf, CUE[cue](d if d else D), at, g)
    buf = buf[:int(D * SR)]; buf = buf / (np.max(np.abs(buf)) + 1e-9) * .89
    st = np.stack([buf, buf], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())

def main():
    work = os.path.join(HERE, 'work'); os.makedirs(work, exist_ok=True)
    for k, fn in (('t1', test1), ('t2', test2), ('t3', test3)):
        d = os.path.join(work, k); os.makedirs(os.path.join(d, 'assets', 'fonts'), exist_ok=True)
        D, html, ev = fn()
        open(os.path.join(d, 'index.html'), 'w').write(html)
        for f in os.listdir(os.path.join(TPL, 'lib', 'fonts')): shutil.copy2(os.path.join(TPL, 'lib', 'fonts', f), os.path.join(d, 'assets', 'fonts', f))
        for f in ('hyperframes.json', 'package.json', 'meta.json'): shutil.copy2(os.path.join(TPL, 'lib', 'hf_template', f), os.path.join(d, f))
        shutil.copy2(os.path.join(HERE, 'tiger_fill.png'), os.path.join(d, 'assets', 'tiger_fill.png'))
        audio(D, ev, os.path.join(d, 'sfx.wav'))
        print('built', k, D, 's,', len(ev), 'sound events')

if __name__ == '__main__': main()
