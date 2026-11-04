#!/usr/bin/env python3
"""Test 4: the RICH version of the hook beat (test 1), copying Depth Theory's richness, in our warm palette:
6 parallax layers, light rays, drifting mist, fireflies, light rain, swaying leaves, an explorer with a head torch whose beam
sweeps and catches the tiger's eyeshine, a distance readout that ticks down, gold lock-on brackets, a heartbeat ring that speeds up,
the tiger emerging partly hidden by leaves. Sound: ElevenLabs recordings (sfx_el/) + our synth graphic sounds.
Also re-scores test 1 with the ElevenLabs sounds (t1b) for an old-vs-new sound comparison.
  python3 make_test4.py && ./render_test4.sh"""
import os, sys, math, subprocess, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TPL = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, TPL)
import make_tests as M
from blocks.common import fig, GOLD, WARM, SOFT
import sfx_voices as V
R = np.random.default_rng(4)
D = 12.0

def frond(x, y, L, a, col, n=9, sway=None):
    """A fern / palm frond: stem + paired leaflets. Returns svg <g>."""
    s = [f'<g class="sw" data-sway="{sway or 0}" transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})">',
         f'<path d="M0,0 Q{L*.15:.0f},{-L*.5:.0f} 0,{-L:.0f}" stroke="{col}" stroke-width="5" fill="none"/>']
    for k in range(1, n):
        t = k / n; py = -L * t; ll = L * .32 * math.sin(math.pi * t) + 10
        for sgn in (-1, 1):
            s.append(f'<path d="M0,{py:.0f} q{sgn*ll*.5:.0f},{-ll*.15:.0f} {sgn*ll:.0f},{ll*.25:.0f} q{-sgn*ll*.55:.0f},{ll*.05:.0f} {-sgn*ll:.0f},{-ll*.22:.0f}" fill="{col}"/>')
    return ''.join(s) + '</g>'

def broad(x, y, L, a, col, vein='#1f3a2c'):
    w = L * .42
    return (f'<g class="sw" transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})"><path d="M0,0 C{w:.0f},{-L*.25:.0f} {w*.8:.0f},{-L*.85:.0f} 0,{-L:.0f} C{-w*.8:.0f},{-L*.85:.0f} {-w:.0f},{-L*.25:.0f} 0,0 Z" fill="{col}"/>'
            f'<path d="M0,0 L0,{-L*.96:.0f}" stroke="{vein}" stroke-width="2.5" opacity=".7"/></g>')

def tree(x, w, top, col, canopy):
    s = f'<path d="M{x-w/2:.0f},720 C{x-w/2+6:.0f},500 {x-w*.35:.0f},{top+80:.0f} {x-w*.3:.0f},{top:.0f} L{x+w*.3:.0f},{top:.0f} C{x+w*.35:.0f},{top+80:.0f} {x+w/2-6:.0f},500 {x+w/2:.0f},720 Z" fill="{col}"/>'
    for _ in range(7):
        cx = x + R.uniform(-170, 170); cy = top + R.uniform(-60, 60); rr = R.uniform(70, 140)
        s += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rr*1.3:.0f}" ry="{rr*.8:.0f}" fill="{canopy}"/>'
    return s

def vine(x, top, L, col):
    d = f'M{x},{top} ' + ' '.join(f'Q{x+(18 if i%2 else -18)},{top+L*(i+.5)/6:.0f} {x},{top+L*(i+1)/6:.0f}' for i in range(6))
    leaves = ''.join(f'<ellipse cx="{x+(10 if i%2 else -10)}" cy="{top+L*i/7:.0f}" rx="12" ry="6" fill="{col}" transform="rotate({30 if i%2 else -30} {x+(10 if i%2 else -10)} {top+L*i/7:.0f})"/>' for i in range(1, 7))
    return f'<g class="vine" data-x="{x}" data-top="{top}"><path d="{d}" stroke="{col}" stroke-width="4" fill="none"/>{leaves}</g>'

def explorer(p, hx, hy, s):
    """Stick 'you' + hat + backpack + head torch (beam drawn separately)."""
    return (f'<g id="{p}-ex">{fig(p, hx, hy, s)}'
            f'<path d="M{hx-30*s:.0f},{hy-128*s:.0f} h{60*s:.0f} M{hx-18*s:.0f},{hy-128*s:.0f} q{18*s:.0f},{-26*s:.0f} {36*s:.0f},0" stroke="{WARM}" stroke-width="{6*s:.1f}" fill="#16120d" stroke-linecap="round"/>'
            f'<rect x="{hx-34*s:.0f}" y="{hy-82*s:.0f}" width="{26*s:.0f}" height="{48*s:.0f}" rx="{6*s:.0f}" fill="#16120d" stroke="{WARM}" stroke-width="{4*s:.1f}"/>'
            f'<circle cx="{hx+18*s:.0f}" cy="{hy-120*s:.0f}" r="{5*s:.1f}" fill="#fff6dc"/></g>')

def test4():
    hx, hy, s = 400, 520, .95
    lamp = (hx + 18 * s, hy - 120 * s)
    sky = ('<defs><radialGradient id="glow" cx="72%" cy="28%" r="60%"><stop offset="0" stop-color="#e6b062" stop-opacity=".22"/><stop offset=".5" stop-color="#3f6a4c" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
           '<linearGradient id="ray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3dca0" stop-opacity=".22"/><stop offset="1" stop-color="#f3dca0" stop-opacity="0"/></linearGradient>'
           '<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff3d2" stop-opacity=".55"/><stop offset="1" stop-color="#fff3d2" stop-opacity="0"/></linearGradient>'
           '<radialGradient id="eyeglow"><stop offset="0" stop-color="#ffe9a8" stop-opacity="1"/><stop offset=".35" stop-color="#e8b04a" stop-opacity=".7"/><stop offset="1" stop-color="#e8b04a" stop-opacity="0"/></radialGradient>'
           '<linearGradient id="mist" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9cfb9" stop-opacity="0"/><stop offset=".5" stop-color="#b9cfb9" stop-opacity=".10"/><stop offset="1" stop-color="#b9cfb9" stop-opacity="0"/></linearGradient></defs>'
           '<rect width="1280" height="720" fill="#0a1712"/><rect width="1280" height="720" fill="url(#glow)"/>')
    rays = '<g id="rays">' + ''.join(f'<path class="ray" d="M{x},-20 L{x+70},-20 L{x+260},740 L{x+120},740 Z" fill="url(#ray)"/>' for x in (700, 840, 1010)) + '</g>'
    L1 = '<g id="L1">' + ''.join(tree(x, R.uniform(30, 50), R.uniform(80, 200), '#244a39', '#20432f') for x in (120, 380, 640, 900, 1180, 1420)) + '</g>'
    mist1 = '<g id="mist1"><rect x="-300" y="380" width="2000" height="170" fill="url(#mist)"/></g>'
    L2 = '<g id="L2">' + ''.join(tree(x, R.uniform(60, 90), R.uniform(-40, 60), '#153024', '#13291f') for x in (40, 560, 1060, 1500)) + ''.join(vine(x, 0, R.uniform(260, 420), '#1d4030') for x in (220, 470, 760, 980, 1230)) + '</g>'
    L3 = '<g id="L3">' + ''.join(frond(R.uniform(-100, 1450), R.uniform(560, 640), R.uniform(150, 260), R.uniform(-55, 55), '#0e2419') for _ in range(18)) + '</g>'
    ground = '<path d="M-60,575 C260,560 760,585 1400,566 L1400,760 L-60,760 Z" fill="#08140f"/><path d="M-60,575 C260,560 760,585 1400,566" stroke="#2f5040" stroke-width="2" fill="none" opacity=".7"/>'
    eyes = (f'<g id="eyes" opacity="0"><circle cx="1010" cy="410" r="60" fill="url(#eyeglow)" opacity=".35"/>'
            f'<circle id="e1" cx="993" cy="410" r="9" fill="url(#eyeglow)"/><circle id="e2" cx="1027" cy="410" r="9" fill="url(#eyeglow)"/></g>')
    beam = f'<g id="beamg"><path id="beam" d="M{lamp[0]:.0f},{lamp[1]:.0f} L1300,{lamp[1]-150:.0f} L1300,{lamp[1]+170:.0f} Z" fill="url(#beam)"/></g>'
    you = explorer('u', hx, hy, s)
    br = (f'<g id="br" stroke="{GOLD}" stroke-width="4" fill="none"><path id="b1" d="M0,22 V0 H22"/><path id="b2" d="M0,-22 V0 H22"/><path id="b3" d="M0,22 V0 H-22"/><path id="b4" d="M0,-22 V0 H-22"/></g>'
          f'<circle id="hb" cx="{hx}" cy="{hy-60}" r="40" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0"/>')
    L5 = '<g id="L5">' + ''.join(broad(R.uniform(-80, 1400), R.uniform(700, 800), R.uniform(120, 210), R.uniform(-70, 70), '#06110b') for _ in range(11)) + ''.join(broad(R.uniform(-100, 1400), R.uniform(-60, 40), R.uniform(150, 240), R.uniform(140, 220), '#06110b') for _ in range(8)) + '</g>'
    flies = '<g id="flies">' + ''.join(f'<circle class="fly" cx="{R.uniform(0,1280):.0f}" cy="{R.uniform(150,600):.0f}" r="{R.uniform(1.4,3):.1f}" fill="#e4f29a"/>' for _ in range(34)) + '</g>'
    rain = '<g id="rain" opacity=".22">' + ''.join(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x-6:.0f}" y2="{y+26:.0f}" stroke="#cfe0d4" stroke-width="1.2"/>' for x, y in zip(R.uniform(0, 1400, 140), R.uniform(-720, 720, 140))) + '</g>'
    svg1 = f'<svg class="abs" style="left:0;top:0" width="1280" height="720" viewBox="0 0 1280 720">{sky}{rays}<g id="far">{L1}</g>{mist1}<g id="mid">{L2}</g>{eyes}{ground}</svg>'
    svg2 = f'<svg class="abs" style="left:0;top:0;overflow:visible" width="1280" height="720" viewBox="0 0 1280 720"><g id="near">{L3}</g>{beam}{you}{br}</svg>'
    svg3 = f'<svg class="abs" style="left:0;top:0" width="1280" height="720" viewBox="0 0 1280 720"><g id="front">{L5}</g>{flies}<g id="rainw">{rain}</g></svg>'
    hud = ('<div id="hud" class="abs" style="left:56px;top:46px;opacity:0;font:500 15px Jost;letter-spacing:.24em;color:#f6efe0">'
           'SUNDARBANS <span style="color:#c9a45c">&middot;</span> 02:14 <span style="opacity:.55">AM</span><div style="width:120px;height:1px;background:#c9a45c;margin-top:8px"></div></div>'
           f'<div id="dist" class="abs" style="left:{hx+90}px;top:{hy-210}px;opacity:0;font:500 15px Jost;letter-spacing:.2em;color:#c9a45c">'
           '<span id="dnum" class="big" style="font-size:30px;letter-spacing:0;color:#f6efe0">38</span> <i class="it" style="font-size:20px;letter-spacing:0">m</i><br>DISTANCE</div>'
           '<div id="t4k" class="abs kick" style="left:0;width:1280px;top:640px;text-align:center;opacity:0">IT ALREADY <span class="it" style="font-size:36px;letter-spacing:.02em;text-transform:none">sees</span> YOU</div>'
           '<div id="t4h" class="hair" style="left:560px;width:160px;top:684px;opacity:0"></div>'
           '<div class="abs" style="right:24px;bottom:16px;font:13px Jost;letter-spacing:.15em;color:#f6efe0;opacity:.35">TEST NUMBERS</div>')
    tg = M.tiger('tg', 1320, 368, 440, flip=False)
    body = (svg1 + svg2 + tg + svg3 + hud + '<div class="vig"></div><div id="fl" class="flash"></div>')
    # bracket centre
    cx, cy = hx, hy - 50
    js = f'''
tl.fromTo('#scene',{{opacity:0}},{{opacity:1,duration:.8,ease:'none'}},0);
tl.fromTo('#scene',{{scale:1.0}},{{scale:1.09,duration:{D},ease:'none',transformOrigin:'42% 58%'}},0);
tl.fromTo('#far',{{x:0}},{{x:-25,duration:{D},ease:'none'}},0);
tl.fromTo('#mid',{{x:0}},{{x:-55,duration:{D},ease:'none'}},0);
tl.fromTo('#near',{{x:0}},{{x:-110,duration:{D},ease:'none'}},0);
tl.fromTo('#front',{{x:0}},{{x:-190,duration:{D},ease:'none'}},0);
tl.fromTo('#mist1',{{x:-200}},{{x:120,duration:{D},ease:'none'}},0);
document.querySelectorAll('.ray').forEach((r,i)=>tl.fromTo(r,{{opacity:.5}},{{opacity:1,duration:2.2+i*.6,yoyo:true,repeat:5,ease:'sine.inOut'}},0));
document.querySelectorAll('#near .sw, #front .sw').forEach((l,i)=>{{const a=(i%2?2.2:-2.2);tl.fromTo(l,{{rotation:0,svgOrigin:l.getAttribute('transform').match(/translate\\(([-\\d.]+),([-\\d.]+)\\)/).slice(1).join(' ')}},{{rotation:a,duration:1.6+(i%5)*.3,yoyo:true,repeat:6,ease:'sine.inOut'}},(i%7)*.15);}});
document.querySelectorAll('.vine').forEach((v,i)=>tl.fromTo(v,{{rotation:-1.5,svgOrigin:v.dataset.x+' '+v.dataset.top}},{{rotation:1.5,duration:2.4+i*.2,yoyo:true,repeat:4,ease:'sine.inOut'}},0));
document.querySelectorAll('.fly').forEach((f,i)=>{{tl.fromTo(f,{{x:0,y:0}},{{x:(i%2?1:-1)*(20+i%9*6),y:-(15+i%7*5),duration:{D},ease:'sine.inOut'}},0);tl.fromTo(f,{{opacity:.15}},{{opacity:1,duration:.5+(i%6)*.25,yoyo:true,repeat:Math.round(6+i%5),ease:'sine.inOut'}},(i%10)*.2);}});
tl.fromTo('#rainw',{{y:0}},{{y:720,duration:1.4,ease:'none',repeat:Math.ceil({D}/1.4)}},0);
tl.fromTo('#hud',{{opacity:0,x:-10}},{{opacity:1,x:0,duration:.5,ease:'power2.out'}},.7);
pose('u',{hx},{hy},{s},{{aL:20,aR:-20,lL:14,lR:-14}});
tl.fromTo('#u-legL',{{rotation:16,svgOrigin:'{hx} {hy}'}},{{rotation:-16,svgOrigin:'{hx} {hy}',duration:.4,yoyo:true,repeat:7,ease:'sine.inOut'}},.3);
tl.fromTo('#u-legR',{{rotation:-16,svgOrigin:'{hx} {hy}'}},{{rotation:16,svgOrigin:'{hx} {hy}',duration:.4,yoyo:true,repeat:7,ease:'sine.inOut'}},.3);
tl.fromTo('#u-ex',{{x:-150}},{{x:0,duration:3.4,ease:'power1.out'}},.3);
tl.fromTo('#beamg',{{x:-150}},{{x:0,duration:3.4,ease:'power1.out'}},.3);
bob('#u-ex',.3,3.4,-4,.2);
tl.fromTo('#beam',{{rotation:14,svgOrigin:'{lamp[0]:.0f} {lamp[1]:.0f}',opacity:.6}},{{rotation:-6,svgOrigin:'{lamp[0]:.0f} {lamp[1]:.0f}',duration:2.4,ease:'sine.inOut'}},.6);
tl.to('#beam',{{rotation:-10,svgOrigin:'{lamp[0]:.0f} {lamp[1]:.0f}',duration:.6,ease:'power2.out'}},3.0);
tl.fromTo('#eyes',{{opacity:0}},{{opacity:1,duration:.12}},3.35);
tl.fromTo(['#e1','#e2'],{{attr:{{r:2}}}},{{attr:{{r:13}},duration:.25,ease:'power3.out'}},3.35);
tl.to(['#e1','#e2'],{{attr:{{r:9}},duration:.6,ease:'sine.out'}},3.6);
tl.fromTo('#dist',{{opacity:0,y:8}},{{opacity:1,y:0,duration:.35,ease:'power3.out'}},4.2);
counter('#dnum',4.2,1.9,38,12,v=>Math.round(v),'power1.inOut');
const C=[[{cx-160},{cy-200},{cx-70},{cy-122},'#b1'],[{cx-160},{cy+190},{cx-70},{cy+100},'#b2'],[{cx+160},{cy-200},{cx+70},{cy-122},'#b3'],[{cx+160},{cy+190},{cx+70},{cy+100},'#b4']];
C.forEach(c=>tl.fromTo(c[4],{{x:c[0],y:c[1],opacity:0}},{{x:c[2],y:c[3],opacity:1,duration:.3,ease:'power3.out'}},6.1));
C.forEach(c=>tl.to(c[4],{{x:c[2]+(c[2]<{cx}?-5:5),y:c[3]+(c[3]<{cy}?-5:5),duration:.45,yoyo:true,repeat:6,ease:'sine.inOut'}},6.45));
tl.to('#dist',{{opacity:0,duration:.3}},6.2);
tl.fromTo('#t4k',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.45,ease:'power2.out'}},6.45);
tl.fromTo('#t4h',{{scaleX:0,opacity:1,transformOrigin:'50% 50%'}},{{scaleX:1,duration:.5,ease:'power2.out'}},6.6);
[6.6,7.5,8.25,8.85,9.35,9.8,10.2].forEach(t=>tl.fromTo('#hb',{{attr:{{r:40}},opacity:.9}},{{attr:{{r:120}},opacity:0,duration:.7,ease:'power2.out'}},t));
tl.to('#eyes',{{opacity:0,duration:.25}},7.9);
tl.fromTo('#tg',{{x:0}},{{x:-520,duration:1.8,ease:'power2.out'}},7.9);
tl.fromTo('#fl',{{opacity:0}},{{opacity:.2,duration:.06,yoyo:true,repeat:1}},9.75);
tl.to('#scene',{{opacity:0,duration:.5}},{D-.5});
'''
    hb = [6.6, 7.5, 8.25, 8.85, 9.35, 9.8, 10.2]
    ev = [('el:jungle_bed', 0, .9, D), ('drone', 0, .35, D), ('el:leaves_rustle', 3.0, .8), ('el:tiger_chuff', 3.45, 1.0), ('ticks', 4.2, .3, 1.9),
          ('beep', 6.1, .45), ('el:tiger_growl', 7.7, 1.0), ('swoosh', 7.9, .35), ('thud', 9.75, .55)] + [('heart', t, .9) for t in hb]
    return D, M.page(D, body, js), ev

def load_el(name):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(HERE, 'sfx_el', name + '.mp3'), '-ac', '1', '-ar', str(V.SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768

def heart():
    n = int(.35 * V.SR); t = np.arange(n) / V.SR
    y = np.sin(2 * np.pi * 52 * t) * np.exp(-t * 18) + .6 * np.sin(2 * np.pi * 46 * (t - .14)) * np.exp(-np.maximum(t - .14, 0) * 18) * (t > .14)
    return V.nrm(y)

def audio(D, ev, path):
    import wave
    SR = V.SR; buf = np.zeros(int((D + .5) * SR))
    for e in ev:
        cue, at, g = e[0], e[1], e[2]; d = e[3] if len(e) > 3 else None
        if cue.startswith('el:'):
            x = load_el(cue[3:]); x = x / (np.max(np.abs(x)) + 1e-9)
            if d: x = x[:int(d * SR)]; fl = int(.8 * SR); x[-fl:] *= np.linspace(1, 0, fl); x[:int(.5*SR)] *= np.linspace(0, 1, int(.5*SR))
            V.put(buf, x, at, g)
        elif cue == 'heart': V.put(buf, heart(), at, g)
        else: V.put(buf, M.CUE[cue](d if d else D), at, g)
    buf = buf[:int(D * SR)]; buf = buf / (np.max(np.abs(buf)) + 1e-9) * .89
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([buf, buf], 1) * 32767).astype('<i2').tobytes())

def main():
    work = os.path.join(HERE, 'work')
    d = os.path.join(work, 't4'); os.makedirs(os.path.join(d, 'assets', 'fonts'), exist_ok=True)
    Dd, html, ev = test4()
    open(os.path.join(d, 'index.html'), 'w').write(html)
    for f in os.listdir(os.path.join(TPL, 'lib', 'fonts')): shutil.copy2(os.path.join(TPL, 'lib', 'fonts', f), os.path.join(d, 'assets', 'fonts', f))
    for f in ('hyperframes.json', 'package.json', 'meta.json'): shutil.copy2(os.path.join(TPL, 'lib', 'hf_template', f), os.path.join(d, f))
    shutil.copy2(os.path.join(HERE, 'tiger_fill.png'), os.path.join(d, 'assets', 'tiger_fill.png'))
    audio(Dd, ev, os.path.join(d, 'sfx.wav'))
    # test 1 with the new (ElevenLabs) sound, same picture
    ev1 = [('el:jungle_bed', 0, .9, 9.0), ('drone', 0, .35, 9.0), ('el:leaves_rustle', 1.8, .8), ('el:tiger_chuff', 2.05, 1.0), ('beep', 3.6, .45), ('tick', 3.6, .6),
           ('swoosh', 5.4, .35), ('el:tiger_growl', 5.6, 1.0), ('thud', 6.85, .5)]
    audio(9.0, ev1, os.path.join(work, 't1', 'sfx_el.wav'))
    print('built t4', Dd, 's,', len(ev), 'sound events; t1 new sound written')

if __name__ == '__main__': main()
