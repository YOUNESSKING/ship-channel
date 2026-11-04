#!/usr/bin/env python3
"""Test 6: the supporting cast, after Depth Theory's people system (research/video_study/people/sheet.jpg):
our plain stick figure stays 'you'; side characters = the same figure + ONE prop that says the role; modes for ideas
(backlit silhouette, gold X-ray cutaway); crowds as tiny repeated figures.
  python3 make_test6.py && (cd work/t6 && npx -y hyperframes@0.8.188 render ...)"""
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); TPL = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, TPL)
import make_tests as M
from blocks.common import fig, GOLD, WARM
D = 9.0
S = .85
LW = 'stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"'

def scientist(hx, hy, s=S):
    sy = hy - 78 * s
    return (f'<path d="M{hx-26*s:.0f},{sy-4*s:.0f} L{hx+26*s:.0f},{sy-4*s:.0f} L{hx+32*s:.0f},{hy+30*s:.0f} L{hx-32*s:.0f},{hy+30*s:.0f} Z" fill="#e9e4d6" stroke="#0d0b08" stroke-width="2"/>'
            f'<path d="M{hx:.0f},{sy-4*s:.0f} L{hx-6*s:.0f},{hy+30*s:.0f} M{hx:.0f},{sy-4*s:.0f} L{hx+6*s:.0f},{hy+30*s:.0f}" stroke="#b7b09e" stroke-width="2"/>'
            f'<g fill="none" stroke="#0d0b08" stroke-width="{2.4*s:.1f}"><circle cx="{hx-9*s:.0f}" cy="{hy-117*s:.0f}" r="{7*s:.0f}" fill="#fff" fill-opacity=".25"/><circle cx="{hx+9*s:.0f}" cy="{hy-117*s:.0f}" r="{7*s:.0f}" fill="#fff" fill-opacity=".25"/><path d="M{hx-2*s:.0f},{hy-117*s:.0f} h{4*s:.0f}"/></g>'
            f'<rect x="{hx+22*s:.0f}" y="{sy+20*s:.0f}" width="{26*s:.0f}" height="{34*s:.0f}" rx="3" fill="#8a6e45" stroke="#0d0b08" stroke-width="2"/><rect x="{hx+26*s:.0f}" y="{sy+26*s:.0f}" width="{18*s:.0f}" height="{22*s:.0f}" fill="#f6efe0"/>')

def honey_collector(hx, hy, s=S):
    """Sundarbans honey collectors wear a face mask on the BACK of the head (tigers attack from behind)."""
    return (f'<ellipse cx="{hx-22*s:.0f}" cy="{hy-113*s:.0f}" rx="{9*s:.0f}" ry="{19*s:.0f}" fill="#d9b278" stroke="#0d0b08" stroke-width="2"/>'
            f'<circle cx="{hx-25*s:.0f}" cy="{hy-119*s:.0f}" r="{2.6*s:.1f}" fill="#0d0b08"/><path d="M{hx-27*s:.0f},{hy-106*s:.0f} q{3*s:.0f},{3*s:.0f} {5*s:.0f},0" stroke="#0d0b08" stroke-width="1.8" fill="none"/>'
            f'<path d="M{hx-24*s:.0f},{hy-138*s:.0f} q{24*s:.0f},{-16*s:.0f} {48*s:.0f},{0}" stroke="#c84f2e" stroke-width="{7*s:.0f}" fill="none" stroke-linecap="round"/>'
            f'<g transform="translate({hx+34*s:.0f},{hy-10*s:.0f})"><path d="M-14,-8 q14,-14 28,0 v20 q-14,10 -28,0 z" fill="#9b6a35" stroke="#0d0b08" stroke-width="2"/><path d="M-14,-8 h28" stroke="#5a3a1c" stroke-width="3"/></g>')

def hunter(hx, hy, s=S):
    return (f'<path d="M{hx-30*s:.0f},{hy-128*s:.0f} q{30*s:.0f},{-8*s:.0f} {60*s:.0f},0 M{hx-22*s:.0f},{hy-128*s:.0f} q{22*s:.0f},{-34*s:.0f} {44*s:.0f},0 z" fill="#d8c9a3" stroke="#0d0b08" stroke-width="2"/>'
            f'<path d="M{hx-30*s:.0f},{hy-128*s:.0f} h{60*s:.0f}" stroke="#d8c9a3" stroke-width="{6*s:.0f}" stroke-linecap="round"/>'
            f'<path d="M{hx+6*s:.0f},{hy-60*s:.0f} L{hx+78*s:.0f},{hy-96*s:.0f}" stroke="#6b4a2a" stroke-width="{7*s:.0f}" stroke-linecap="round"/><path d="M{hx+48*s:.0f},{hy-81*s:.0f} L{hx+92*s:.0f},{hy-103*s:.0f}" stroke="#2a2a2a" stroke-width="{4*s:.0f}" stroke-linecap="round"/>'
            f'<path d="M{hx-18*s:.0f},{hy-80*s:.0f} L{hx+18*s:.0f},{hy-30*s:.0f}" stroke="#7a5a32" stroke-width="{5*s:.0f}"/>')

def child(hx, hy):
    return fig('kid', hx, hy, .58) + f'<path d="M{hx-14},{hy-80} q14,-14 28,0" fill="none" stroke="{GOLD}" stroke-width="0"/>'

def xray(hx, hy, s=S):
    sy = hy - 78 * s
    return (f'<g id="xr" fill="none" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
            f'<circle cx="{hx}" cy="{hy-112*s:.0f}" r="{24*s:.0f}" stroke-opacity=".8"/>'
            f'<path d="M{hx-26*s:.0f},{sy:.0f} Q{hx},{sy-10*s:.0f} {hx+26*s:.0f},{sy:.0f} L{hx+22*s:.0f},{hy:.0f} L{hx-22*s:.0f},{hy:.0f} Z" stroke-opacity=".8"/>'
            f'<path d="M{hx-26*s:.0f},{sy:.0f} l-6,{56*s:.0f} M{hx+26*s:.0f},{sy:.0f} l6,{56*s:.0f} M{hx-12*s:.0f},{hy:.0f} v{84*s:.0f} M{hx+12*s:.0f},{hy:.0f} v{84*s:.0f}" stroke-opacity=".8"/>'
            f'<path d="M{hx-16*s:.0f},{sy+14*s:.0f} v{30*s:.0f} M{hx+16*s:.0f},{sy+14*s:.0f} v{30*s:.0f}" stroke-opacity=".35"/>'
            f'<path id="heart" d="M{hx+4*s:.0f},{sy+26*s:.0f} c-4,-8 -16,-6 -14,4 c2,8 14,14 14,14 c0,0 12,-6 14,-14 c2,-10 -10,-12 -14,-4 z" fill="{GOLD}" fill-opacity=".85" stroke="none"/></g>'
            f'<line id="scan" x1="{hx-60}" y1="{hy-150}" x2="{hx+60}" y2="{hy-150}" stroke="{GOLD}" stroke-width="2" opacity=".7"/>')

def backlit(hx, hy):
    return (f'<defs><radialGradient id="disc"><stop offset="0" stop-color="#f3dca0" stop-opacity=".75"/><stop offset=".55" stop-color="#e0a24a" stop-opacity=".25"/><stop offset="1" stop-color="#e0a24a" stop-opacity="0"/></radialGradient></defs>'
            f'<circle id="disc" cx="{hx}" cy="{hy-40}" r="110" fill="url(#disc)"/>'
            f'<g fill="none" stroke="#050403" stroke-width="7" stroke-linecap="round"><circle cx="{hx}" cy="{hy-95}" r="20" fill="#050403"/><path d="M{hx},{hy-75} V{hy} M{hx},{hy-66} l-24,40 M{hx},{hy-66} l24,40 M{hx},{hy} l-16,70 M{hx},{hy} l16,70"/></g>')

def crowd_boat(x, y):
    figs = ''.join(f'<g stroke="{WARM}" stroke-width="2.4" stroke-linecap="round"><circle cx="{x-50+i*20}" cy="{y-26}" r="5" fill="{WARM}"/><path d="M{x-50+i*20},{y-21} v14"/></g>' for i in range(6))
    return (f'<path d="M{x-80},{y-6} h160 l-18,22 h-124 z" fill="#4a3824" stroke="#0d0b08" stroke-width="2"/>{figs}'
            f'<path d="M{x-90},{y+18} q20,-6 40,0 t40,0 t40,0 t40,0 t40,0" stroke="#7fa595" stroke-width="2.5" fill="none" opacity=".7"/>')

def test6():
    hy = 250
    cols = [(150, 'You', fig('you', 150, hy, S)), (370, 'Scientist', fig('sci', 370, hy, S) + scientist(370, hy)),
            (590, 'Honey collector', fig('hon', 590, hy, S) + honey_collector(590, hy)), (810, 'Hunter, 1900s', fig('hun', 810, hy, S) + hunter(810, hy)),
            (1030, 'Child', fig('kid', 1030, hy + 36, .58)), (1190, '', '')]
    row1 = ''.join(f'<g id="c{i}" opacity="0">{svg}</g>' for i, (x, l, svg) in enumerate(cols) if svg)
    labs = ''.join(f'<div id="l{i}" class="abs kick" style="left:{x-110}px;width:220px;top:{hy+96}px;text-align:center;font-size:15px;opacity:0">{l}</div>' for i, (x, l, svg) in enumerate(cols) if l)
    modes = (f'<g id="m0" opacity="0">{backlit(300, 560)}</g>'
             f'<g id="m1" opacity="0">{xray(640, 560)}</g>'
             f'<g id="m2" opacity="0">{crowd_boat(990, 600)}</g>')
    mlabs = ''.join(f'<div id="ml{i}" class="abs kick" style="left:{x-140}px;width:280px;top:{y}px;text-align:center;font-size:15px;opacity:0">{t}</div>'
                    for i, (x, y, t) in enumerate([(300, 662, 'Mode: backlit'), (640, 662, 'Mode: gold X-ray'), (990, 662, 'Crowd: tiny figures')]))
    body = (f'<svg class="abs" style="left:0;top:0;overflow:visible" width="1280" height="720" viewBox="0 0 1280 720">'
            f'<path d="M40,{hy+84*S:.0f} H1240" stroke="#2f5040" stroke-width="2"/>{row1}</svg>'
            f'<svg class="abs" style="left:0;top:0;overflow:visible" width="1280" height="720" viewBox="0 0 1280 720">{modes}</svg>'
            + labs + mlabs +
            '<div class="abs kick" style="left:0;width:1280px;top:40px;text-align:center;font-size:20px">The supporting cast <span class="it" style="font-size:28px;letter-spacing:0;text-transform:none">one figure, one prop</span></div><div class="vig"></div>')
    js = "tl.fromTo('#scene',{opacity:0},{opacity:1,duration:.4},0);"
    js += f"pose('you',150,{hy},{S},{{aL:24,aR:-24,lL:14,lR:-14}});pose('sci',370,{hy},{S},{{aL:18,aR:-58,lL:10,lR:-10}});"
    js += f"pose('hon',590,{hy},{S},{{aL:20,aR:-42,lL:12,lR:-12}});pose('hun',810,{hy},{S},{{aL:-62,aR:-80,lL:14,lR:-14}});pose('kid',1030,{hy+36},.58,{{aL:30,aR:-30,lL:12,lR:-12}});"
    for i in range(5):
        js += f"tl.fromTo('#c{i}',{{opacity:0,y:18}},{{opacity:1,y:0,duration:.3,ease:'power3.out'}},{.5+i*.45});pop('#l{i}',{.6+i*.45});"
        js += f"tl.fromTo('#c{i}',{{y:0}},{{y:-3,duration:1.1,yoyo:true,repeat:5,ease:'sine.inOut'}},{.9+i*.45});"
    for i in range(3):
        js += f"tl.fromTo('#m{i}',{{opacity:0,y:18}},{{opacity:1,y:0,duration:.35,ease:'power3.out'}},{3.2+i*.6});pop('#ml{i}',{3.3+i*.6});"
    js += f"tl.fromTo('#heart',{{scale:1,transformOrigin:'50% 50%'}},{{scale:1.25,duration:.25,yoyo:true,repeat:15,ease:'power2.out'}},3.9);"
    js += f"tl.fromTo('#scan',{{y:0}},{{y:200,duration:1.6,yoyo:true,repeat:2,ease:'sine.inOut'}},3.9);"
    js += f"tl.fromTo('#disc',{{opacity:.6}},{{opacity:1,duration:1,yoyo:true,repeat:4,ease:'sine.inOut'}},3.3);"
    js += f"tl.to('#scene',{{opacity:0,duration:.4}},{D-.4});"
    ev = [('drone', 0, .35, D)] + [('click', .5 + i * .45, .5) for i in range(5)] + [('swoosh', 3.2 + i * .6, .3) for i in range(3)]
    return D, M.page(D, body, js), ev

def main():
    import make_test4 as T4
    d = os.path.join(HERE, 'work', 't6'); os.makedirs(os.path.join(d, 'assets', 'fonts'), exist_ok=True)
    Dd, html, ev = test6()
    open(os.path.join(d, 'index.html'), 'w').write(html)
    for f in os.listdir(os.path.join(TPL, 'lib', 'fonts')): shutil.copy2(os.path.join(TPL, 'lib', 'fonts', f), os.path.join(d, 'assets', 'fonts', f))
    for f in ('hyperframes.json', 'package.json', 'meta.json'): shutil.copy2(os.path.join(TPL, 'lib', 'hf_template', f), os.path.join(d, f))
    T4.audio(Dd, ev, os.path.join(d, 'sfx.wav'))
    print('built t6')

if __name__ == '__main__': main()
