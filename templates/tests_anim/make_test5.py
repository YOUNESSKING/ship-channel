#!/usr/bin/env python3
"""Test 5: three options for the 'you' character (replacing the stick figure), with a real walk cycle (hip/knee, shoulder/elbow).
A = Explorer (flat colour), B = Silhouette (dark figure, warm rim), C = Field researcher (most detail).
  python3 make_test5.py && (cd work/t5 && npx -y hyperframes@0.8.188 render --fps 30 --quality high --output ../../out/t5.silent.mp4)"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); TPL = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, TPL)
import make_tests as M
from blocks.common import GOLD, WARM
D = 8.0

# local coordinates: feet on y=0, hip at (0,-100), shoulder at (0,-160), head centre (0,-190); facing right
def person(p, kind):
    if kind == 'B':
        skin = shirt = shirt2 = pants = boots = hat = pack = '#0b0907'; st = f'stroke="{WARM}" stroke-width="2.6" stroke-linejoin="round"'
    elif kind == 'A':
        skin, shirt, shirt2, pants, boots, hat, pack = '#c99b78', '#b89b6a', '#9c8257', '#3d3b2e', '#1d1712', '#8a7350', '#5b4a33'; st = 'stroke="#0d0b08" stroke-width="2" stroke-linejoin="round"'
    else:
        skin, shirt, shirt2, pants, boots, hat, pack = '#c99b78', '#a9b08a', '#8c9470', '#4a4535', '#1d1712', '#7d6a4a', '#6b5638'; st = 'stroke="#0d0b08" stroke-width="2" stroke-linejoin="round"'
    def leg(side, col):
        sh = col
        return (f'<g id="{p}-th{side}"><path d="M-9,-102 h18 l-2,52 h-14 z" fill="{sh}" {st}/>'
                f'<g id="{p}-sn{side}"><path d="M-8,-52 h14 l-1,44 h-12 z" fill="{sh}" {st}/>'
                f'<path d="M-8,-10 h14 q14,0 16,8 v4 h-30 z" fill="{boots}" {st}/></g></g>')
    def arm(side, sleeve):
        return (f'<g id="{p}-ua{side}"><path d="M-7,-158 h14 l-1,42 h-12 z" fill="{sleeve}" {st}/>'
                f'<g id="{p}-fa{side}"><path d="M-6,-118 h12 l-1,36 h-10 z" fill="{skin if kind != "B" else skin}" {st}/>'
                f'<circle cx="0" cy="-80" r="7" fill="{skin}" {st}/></g></g>')
    back_arm = arm('B', shirt2); back_leg = leg('B', '#2c2a20' if kind != 'B' else pants)
    torso = f'<path d="M-20,-164 q0,-6 8,-6 h24 q8,0 8,6 l2,64 h-44 z" fill="{shirt}" {st}/>'
    detail = ''
    if kind == 'C':
        detail = (f'<path d="M-20,-160 l40,0 l2,58 h-44 z" fill="none"/><path d="M-16,-160 v56 M16,-160 v56" stroke="#5f6648" stroke-width="2"/>'
                  f'<rect x="-14" y="-140" width="10" height="9" fill="#7c8462" {st}/><rect x="5" y="-140" width="10" height="9" fill="#7c8462" {st}/>'
                  f'<rect x="-14" y="-122" width="10" height="9" fill="#7c8462" {st}/><rect x="5" y="-122" width="10" height="9" fill="#7c8462" {st}/>'
                  f'<path d="M-18,-166 L22,-104" stroke="#3b2d1d" stroke-width="5"/><rect x="14" y="-112" width="18" height="16" rx="3" fill="#6b5638" {st}/>'
                  f'<g transform="translate(-2,-150)"><rect x="-8" y="0" width="7" height="11" rx="2" fill="#222" /><rect x="1" y="0" width="7" height="11" rx="2" fill="#222"/></g>')
    elif kind == 'A':
        detail = f'<path d="M0,-166 v62" stroke="#8a7048" stroke-width="2"/><path d="M-20,-112 h42" stroke="#4a3a25" stroke-width="5"/>'
    pack_svg = f'<rect x="-36" y="-162" width="20" height="52" rx="6" fill="{pack}" {st}/>' if kind != 'B' else f'<rect x="-36" y="-162" width="20" height="52" rx="6" fill="{pack}" {st}/>'
    face = ''
    if kind != 'B':
        face = (f'<circle cx="8" cy="-192" r="2.2" fill="#0d0b08"/>'
                + (f'<path d="M4,-198 l7,-1" stroke="#3a2a1c" stroke-width="2" stroke-linecap="round"/><path d="M15,-188 l3,4 l-3,1" stroke="#8a5f44" stroke-width="1.6" fill="none"/>' if kind == 'C' else ''))
    head = (f'<g id="{p}-head"><rect x="-5" y="-176" width="10" height="10" fill="{skin}" {st}/><circle cx="0" cy="-190" r="17" fill="{skin}" {st}/>{face}'
            f'<path d="M-26,-201 h52 q-4,-4 -12,-5 q-2,-16 -14,-16 q-12,0 -14,16 q-8,1 -12,5 z" fill="{hat}" {st}/>'
            f'<rect x="10" y="-207" width="8" height="6" rx="1.5" fill="#e9e2cc" {st}/><circle cx="18" cy="-204" r="2.6" fill="#fff6dc"/></g>')
    return f'<g id="{p}">{back_arm}{back_leg}{pack_svg}{leg("F", pants)}{torso}{detail}{head}{arm("F", shirt)}</g>'

def walk_js(p, t0, dur, per=.5):
    n = int(dur / per)
    return f'''
tl.fromTo('#{p}-thF',{{rotation:-24,svgOrigin:'0 -100'}},{{rotation:24,svgOrigin:'0 -100',duration:{per},yoyo:true,repeat:{n},ease:'sine.inOut'}},{t0});
tl.fromTo('#{p}-thB',{{rotation:24,svgOrigin:'0 -100'}},{{rotation:-24,svgOrigin:'0 -100',duration:{per},yoyo:true,repeat:{n},ease:'sine.inOut'}},{t0});
tl.fromTo('#{p}-snF',{{rotation:4,svgOrigin:'0 -52'}},{{rotation:30,svgOrigin:'0 -52',duration:{per/2},yoyo:true,repeat:{2*n+1},ease:'sine.inOut'}},{t0});
tl.fromTo('#{p}-snB',{{rotation:30,svgOrigin:'0 -52'}},{{rotation:4,svgOrigin:'0 -52',duration:{per/2},yoyo:true,repeat:{2*n+1},ease:'sine.inOut'}},{t0});
tl.fromTo('#{p}-uaF',{{rotation:20,svgOrigin:'0 -158'}},{{rotation:-20,svgOrigin:'0 -158',duration:{per},yoyo:true,repeat:{n},ease:'sine.inOut'}},{t0});
tl.fromTo('#{p}-uaB',{{rotation:-20,svgOrigin:'0 -158'}},{{rotation:20,svgOrigin:'0 -158',duration:{per},yoyo:true,repeat:{n},ease:'sine.inOut'}},{t0});
tl.fromTo(['#{p}-faF','#{p}-faB'],{{rotation:-8,svgOrigin:'0 -118'}},{{rotation:-26,svgOrigin:'0 -118',duration:{per},yoyo:true,repeat:{n},ease:'sine.inOut'}},{t0});
tl.fromTo('#{p}-body',{{y:0}},{{y:-4,duration:{per/2},yoyo:true,repeat:{2*n+1},ease:'sine.inOut'}},{t0});
'''

def test5():
    xs = (260, 640, 1020); names = ('A  Explorer', 'B  Silhouette', 'C  Field researcher')
    bg = M.leaves('lb', 3, 60, 40, 640, .9, '#1e3d2e', 1)
    figs = ''.join(f'<g transform="translate({x},560) scale(1.55)"><g id="{k}-body">{person(k, k)}</g></g>' for k, x in zip('ABC', xs))
    ground = '<path d="M-20,560 C300,556 900,566 1300,558 L1300,740 L-20,740 Z" fill="#08140e"/><path id="gl" d="M-20,560 C300,556 900,566 1300,558" stroke="#2f5040" stroke-width="2" fill="none"/>'
    dashes = '<g id="dash">' + ''.join(f'<rect x="{x}" y="575" width="30" height="3" fill="#2f5040"/>' for x in range(-200, 1500, 90)) + '</g>'
    labels = ''.join(f'<div class="abs kick" style="left:{x-160}px;width:320px;top:604px;text-align:center;font-size:18px">{n}</div>' for x, n in zip(xs, names))
    body = (f'<svg class="abs" style="left:0;top:0" width="1280" height="720" viewBox="0 0 1280 720"><g id="bgl">{bg}</g>{ground}{dashes}{figs}</svg>'
            + labels + '<div class="abs kick" style="left:0;width:1280px;top:60px;text-align:center;font-size:20px;opacity:.8">Pick the new <span class="it" style="font-size:30px;letter-spacing:0;text-transform:none">you</span></div><div class="vig"></div>')
    js = f"tl.fromTo('#scene',{{opacity:0}},{{opacity:1,duration:.5}},0);tl.fromTo('#bgl',{{x:0}},{{x:-120,duration:{D},ease:'none'}},0);tl.fromTo('#dash',{{x:0}},{{x:-90,duration:.9,ease:'none',repeat:{int(D/.9)}}},0);"
    js += ''.join(walk_js(k, .3, D - .6) for k in 'ABC')
    return D, M.page(D, body, js), [('el:jungle_bed', 0, .7, D)]

def main():
    import make_test4 as T4
    d = os.path.join(HERE, 'work', 't5'); os.makedirs(os.path.join(d, 'assets', 'fonts'), exist_ok=True)
    Dd, html, ev = test5()
    open(os.path.join(d, 'index.html'), 'w').write(html)
    for f in os.listdir(os.path.join(TPL, 'lib', 'fonts')): shutil.copy2(os.path.join(TPL, 'lib', 'fonts', f), os.path.join(d, 'assets', 'fonts', f))
    for f in ('hyperframes.json', 'package.json', 'meta.json'): shutil.copy2(os.path.join(TPL, 'lib', 'hf_template', f), os.path.join(d, f))
    T4.audio(Dd, ev, os.path.join(d, 'sfx.wav'))
    print('built t5')

if __name__ == '__main__': main()
