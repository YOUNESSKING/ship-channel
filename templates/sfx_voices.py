# SFX voices copied from the approved v9 build (videos/test2/build/gen_audio.py). All synthesised, royalty-free.
import numpy as np
SR = 44100
rng = np.random.default_rng(11)
def _onepole(x, a):
    L = int(min(len(x), 12 / (1 - a))); h = (1 - a) * a ** np.arange(L)
    n = len(x) + L; m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(h, m), m)[:len(x)]
def lp(x, fc, order=2):
    a = np.exp(-2 * np.pi * fc / SR); y = x
    for _ in range(order): y = _onepole(y, a)
    return y
def hp(x, fc, order=1): return x - lp(x, fc, order)
def bp(x, lo, hi): return lp(hp(x, lo), hi)
def put(buf, sig, at, gain=1.0):
    i = int(at * SR)
    if i < 0 or i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += sig[:j - i] * gain
def noise(n): return rng.standard_normal(n)
def nrm(x): return x / (np.max(np.abs(x)) + 1e-9)
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def expenv(n, tau, atk=0.004):
    tt = np.arange(n) / SR; e = np.exp(-tt / tau); na = max(1, int(atk * SR)); e[:na] *= np.linspace(0, 1, na); return e

# ------------------------------------------------------------------ SFX voices
def thud(dur=1.4, f0=38, sweep=90):
    n = int(dur * SR); tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(f0 + sweep * np.exp(-tt * 14)) / SR) * np.exp(-tt * 3.2)
    y += lp(noise(n), 300, 2) * 4 * np.exp(-tt * 18); return nrm(y)
def taiko(dur=1.2):
    n = int(dur * SR); tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(55 + 70 * np.exp(-tt * 22)) / SR) * np.exp(-tt * 4.5)
    y += 0.5 * np.sin(2 * np.pi * 110 * tt) * np.exp(-tt * 9) + lp(noise(n), 900, 2) * 3 * np.exp(-tt * 30)
    return nrm(y)
def click():
    n = int(0.05 * SR); tt = np.arange(n) / SR
    y = hp(noise(n), 800) * np.exp(-tt * 140) + np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 200); return nrm(y)
def tok():  # dry wood-block
    n = int(0.25 * SR); tt = np.arange(n) / SR
    return nrm(np.sin(2 * np.pi * 820 * tt) * np.exp(-tt * 38) + .4 * np.sin(2 * np.pi * 1500 * tt) * np.exp(-tt * 60))
def swoosh(dur=0.5, lo=300, hi=3000):
    n = int(dur * SR); tt = np.arange(n) / SR
    return nrm(bp(noise(n), lo, hi) * np.sin(np.pi * tt / dur) ** 2)
def downsweep(dur=1.6, f0=400):
    n = int(dur * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 * np.exp(-tt * 1.6) + 40) / SR) * (1 - tt / dur) ** 1.5
def slide_down(dur=0.7, f0=1400, f1=200):   # slide-whistle drop
    n = int(dur * SR); f = np.geomspace(f0, f1, n)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + .15 * np.sin(2 * np.pi * 9 * np.arange(n) / SR))
    return y * np.minimum(1, np.arange(n) / (.02 * SR)) * (1 - np.arange(n) / n) ** .5 * .8
def ding(f=1320):
    n = int(.8 * SR); tt = np.arange(n) / SR
    return nrm(np.sin(2 * np.pi * f * tt) * np.exp(-tt * 6) + .35 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 14))
def gasp(dur=0.42):   # cartoon inhale: noise swept up
    n = int(dur * SR); tt = np.arange(n) / SR; x = noise(n)
    a = bp(x, 600, 2500) * np.linspace(0.2, 1, n) ** 1.5; b = bp(x, 1800, 5000) * np.linspace(0, 1, n) ** 3
    return nrm((a + b * .8) * np.sin(np.pi * np.minimum(1, tt / dur * .9 + .05)) ** .6)
def splash(dur=0.55):
    n = int(dur * SR); tt = np.arange(n) / SR
    y = bp(noise(n), 400, 3500) * np.exp(-tt * 7) * (1 + .6 * np.sin(2 * np.pi * 22 * tt))
    y += np.sin(2 * np.pi * np.cumsum(300 + 500 * np.exp(-tt * 18)) / SR) * np.exp(-tt * 14) * .4; return nrm(y)
def scratch(dur=0.35):  # pencil strike-through
    n = int(dur * SR); tt = np.arange(n) / SR
    y = hp(noise(n), 2500) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 18 * tt))) * np.sin(np.pi * tt / dur); return nrm(y)
def heli(dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    ph = (tt * 11) % 1
    y = lp(noise(n), 500, 2) * (np.exp(-ph * 9) * 2.5 + .3) + np.sin(2 * np.pi * 70 * tt) * .5
    return nrm(y * np.minimum(1, tt / .5))
def wind(dur, g=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = bp(noise(n), 120, 1100) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * tt + 1)) + lp(noise(n), 250, 2) * 1.4
    return nrm(x) * g
def ocean(dur):
    n = int(dur * SR); tt = np.arange(n) / SR; x = noise(n); sw = .55 + .45 * np.sin(2 * np.pi * .17 * tt)
    return nrm(lp(x, 400, 2) * 3 * sw + (lp(x, 1800, 1) - lp(x, 400, 1)) * 1.2 * sw ** 2)
def bubbles(dur, dens=9):
    n = int(dur * SR); y = np.zeros(n)
    for _ in range(int(dur * dens)):
        f = rng.uniform(500, 1500); d = rng.uniform(.04, .09); m = int(d * SR); tt = np.arange(m) / SR
        put(y, np.sin(2 * np.pi * np.cumsum(f * (1 + 6 * tt)) / SR) * np.exp(-tt * 45), rng.uniform(0, dur - .1), rng.uniform(.2, .6))
    return nrm(y)
def icecrunch(dur):
    n = int(dur * SR); y = lp(noise(n), 700, 2) * .5
    for _ in range(int(dur * 22)):
        m = int(rng.uniform(.01, .03) * SR); tt = np.arange(m) / SR
        put(y, hp(noise(m), 1500) * np.exp(-tt * 160), rng.uniform(0, dur - .05), rng.uniform(.3, 1))
    return nrm(y)


# ------------------------------------------------------------------ graphic + mood voices for the animation blocks (GOLD rule 99 layer 4;
# ported from templates/tests_anim/make_tests.py CUE and make_test4.py heart, approved in test 7). All synthesised.
def tick2():   # count-up tick: short bright transient (make_tests.tick)
    n = int(.03 * SR); tt = np.arange(n) / SR; return nrm(hp(noise(n), 2500) * np.exp(-tt * 250))
def ticks(d=1.0, accel=False):   # a counter running: 16 ticks over d s, slowing down (accel=True: speeding up, for a meter that climbs)
    out = np.zeros(int((d + .1) * SR)); k = 0; at = 0.0
    while at < d:
        put(out, tick2(), at, .6); k += 1; at = d * (k / 16) ** (0.5 if accel else 1.6)
    return out
def beep(d=1.2, f=1180):   # lock-on: pure ~1.2 kHz tone held d s
    n = int(d * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * f * tt) * np.minimum(1, tt / .01) * np.minimum(1, (d - tt) / .12) * .5
def shimmer(d=1.4):   # gold ring / count-up lands
    n = int(d * SR); tt = np.arange(n) / SR
    return nrm(sum(np.sin(2 * np.pi * f * tt) for f in (1568, 2093, 2637))) * np.exp(-tt * 3) * .5
def marker():   # felt marker drawing the gold circle
    n = int(.4 * SR); tt = np.arange(n) / SR; return nrm(bp(noise(n), 1500, 6000) * np.sin(np.pi * tt / .4) ** 2) * .6
def heart():   # one lub-dub (make_test4.heart)
    n = int(.35 * SR); tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 18) + .6 * np.sin(2 * np.pi * 46 * (tt - .14)) * np.exp(-np.maximum(tt - .14, 0) * 18) * (tt > .14)
    return nrm(y)
def heart_run(d, bpm0=72, bpm1=112):   # heartbeat that speeds up over d s (tense beat)
    out = np.zeros(int((d + .4) * SR)); at = 0.0
    while at < d:
        q = at / max(d, .1); put(out, heart(), at, .7 + .3 * q); at += 60.0 / (bpm0 + (bpm1 - bpm0) * q)
    return out
def hit(dur=2.2):   # deep hit (reveal; no music dip): sub drop + soft body, long tail
    n = int(dur * SR); tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(30 + 70 * np.exp(-tt * 9)) / SR) * np.exp(-tt * 1.8)
    y += lp(noise(n), 160, 2) * 3 * np.exp(-tt * 6) + .25 * np.sin(2 * np.pi * 62 * tt) * np.exp(-tt * 5); return nrm(y)
