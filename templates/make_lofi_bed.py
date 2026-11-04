#!/usr/bin/env python3
"""Self-made lo-fi bed (the placeholder music for the body chapters; v9 keeps its own music).

  python3 make_lofi_bed.py OUT.wav --dur 130 [--var 0] [--seed 100]

Same generator as the first Video 01 preview / v9 (Rhodes chords, bass, drums, pluck, vinyl crackle; variant 0 = 84 BPM Dm9 G13 Cmaj9 Am7).
Writes ONE wav (mono 44.1 kHz). It is the single music input of mix_audio.py (--music OUT.wav): when the owner's YouTube Audio Library track
arrives, pass that file instead and re-run mix_audio.py + mux.sh; nothing else changes. The bed starts on a downbeat at 0 s."""
import numpy as np, sys, os, wave, argparse
SR = 44100
rng = np.random.default_rng(7)
def _op(x, a):
    L = int(min(len(x), 12 / (1 - a))); h = (1 - a) * a ** np.arange(L); n = len(x) + L; m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(h, m), m)[:len(x)]
def lp(x, fc, order=2):
    a = np.exp(-2 * np.pi * fc / SR); y = x
    for _ in range(order): y = _op(y, a)
    return y
def hp(x, fc, order=1): return x - lp(x, fc, order)
def bp(x, lo, hi): return lp(hp(x, lo), hi)
def put(buf, sig, at, gain=1.0):
    i = int(at * SR)
    if i < 0 or i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += (sig[:j - i] * gain).astype(buf.dtype)
def noise(n): return rng.standard_normal(n)
def nrm(x): return x / (np.max(np.abs(x)) + 1e-9)
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def expenv(n, tau, atk=0.004):
    tt = np.arange(n) / SR; e = np.exp(-tt / tau); na = max(1, int(atk * SR)); e[:na] *= np.linspace(0, 1, na); return e
# ---- lo-fi bed with per-chapter variation ----
PROG = [([[50, 53, 57, 60, 64], [43, 59, 62, 65, 69], [48, 55, 59, 62, 64], [45, 55, 60, 64, 67]], [38, 31, 36, 33]),      # Dm9 G13 Cmaj9 Am7
        ([[53, 57, 60, 64, 67], [52, 55, 59, 62, 66], [50, 53, 57, 60, 64], [48, 52, 55, 59, 62]], [41, 40, 38, 36]),      # Fmaj9 Em7 Dm9 Cmaj7
        ([[45, 52, 55, 60, 64], [41, 48, 53, 57, 60], [43, 50, 55, 59, 62], [48, 52, 55, 59, 64]], [33, 29, 31, 36]),      # Am9 Fmaj7 G6 Cmaj9
        ([[46, 53, 57, 60, 64], [51, 55, 58, 62, 65], [48, 55, 58, 62, 65], [43, 50, 55, 58, 62]], [34, 39, 36, 31]),      # Bbmaj9 Ebmaj7 Cm9 Gm9
        ([[47, 54, 57, 61, 66], [45, 52, 56, 59, 64], [42, 49, 52, 57, 61], [40, 47, 50, 54, 59]], [35, 33, 30, 28]),      # Bm9 Amaj7 F#m7 Em9
        ([[52, 55, 59, 62, 66], [50, 54, 57, 61, 64], [47, 54, 57, 59, 62], [45, 52, 55, 59, 62]], [40, 38, 35, 33])]      # Em9 D6 Bm7 Am7
VAR = [dict(bpm=84, prog=0, mel=True, pad=False, sw=.12), dict(bpm=78, prog=2, mel=False, pad=True, sw=.14), dict(bpm=88, prog=1, mel=True, pad=False, sw=.1),
       dict(bpm=76, prog=3, mel=False, pad=True, sw=.15), dict(bpm=90, prog=4, mel=True, pad=False, sw=.08), dict(bpm=82, prog=5, mel=True, pad=True, sw=.12),
       dict(bpm=86, prog=1, mel=False, pad=False, sw=.12), dict(bpm=80, prog=0, mel=True, pad=True, sw=.13), dict(bpm=92, prog=2, mel=True, pad=False, sw=.09),
       dict(bpm=78, prog=4, mel=False, pad=True, sw=.14), dict(bpm=84, prog=3, mel=True, pad=False, sw=.11), dict(bpm=72, prog=5, mel=False, pad=True, sw=.15)]
def rhodes(m, dur=1.6):
    n = int(dur * SR); tt = np.arange(n) / SR; f = midi(m); y = np.zeros(n)
    for dt, g in ((-0.05, 1), (0.05, .8)):
        ff = f * 2 ** (dt / 12 / 4); y += g * (np.sin(2 * np.pi * ff * tt) + .22 * np.sin(2 * np.pi * ff * 2 * tt) * np.exp(-tt * 3) + .5 * np.sin(2 * np.pi * ff * 7.1 * tt) * np.exp(-tt * 28))
    return y * expenv(n, .75, .006)
def kick():
    n = int(.4 * SR); tt = np.arange(n) / SR
    return nrm(lp(np.sin(2 * np.pi * np.cumsum(46 + 90 * np.exp(-tt * 28)) / SR) * np.exp(-tt * 9) + hp(noise(n), 2000) * np.exp(-tt * 300) * .15, 900, 1))
def snare():
    n = int(.3 * SR); tt = np.arange(n) / SR
    return nrm(lp(bp(noise(n), 900, 7000) * np.exp(-tt * 20) + np.sin(2 * np.pi * 185 * tt) * np.exp(-tt * 25) * .6, 5500, 1))
def hat(op=False):
    n = int((.25 if op else .07) * SR); tt = np.arange(n) / SR
    return nrm(hp(noise(n), 6500) * np.exp(-tt * (14 if op else 70)))
def pluck(m):
    n = int(.7 * SR); tt = np.arange(n) / SR; f = midi(m)
    return (np.sin(2 * np.pi * f * tt) + .3 * np.sin(2 * np.pi * f * 4 * tt) * np.exp(-tt * 20)) * expenv(n, .18, .003)
def reverb(x, wet=.2, rt=.38, seed=3):
    """Small warm room: exponentially decaying noise impulse response, low-passed. Makes the Rhodes lush instead of dry."""
    g = np.random.default_rng(seed); L = int(1.2 * SR); tt = np.arange(L) / SR
    ir = lp(g.standard_normal(L), 3200, 1) * np.exp(-tt / rt); ir[:int(.012 * SR)] *= np.linspace(0, 1, int(.012 * SR)); ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
    m = 1 << (len(x) + L - 1).bit_length(); return x + wet * np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
def lofi(dur, v, seed, bars=None, tail=0.0, rev=False):
    """dur seconds (default) or `bars` whole bars + `tail` s of ring-out (chords decay, no new drums), used to join sections at bar lines."""
    if bars is not None: dur = bars * 4 * 60 / v['bpm'] + tail
    r = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR; BEAT = 60 / v['bpm']; CHm, ROOT = PROG[v['prog']]
    rch = np.zeros(n); drm = np.zeros(n); bass = np.zeros(n); mel = np.zeros(n)
    PENT = [62, 65, 67, 69, 72, 74]; mp = r.integers(0, 6, 64)
    for bar in range(bars if bars is not None else int(dur / (4 * BEAT)) + 1):
        b0 = bar * 4 * BEAT; ci = bar % 4
        for pos, vel in ((0, 1.0), (1.75, .55), (2.5, .7)):
            if bar % 4 == 3 and pos == 2.5: continue
            for k, m in enumerate(CHm[ci]): put(rch, rhodes(m), b0 + pos * BEAT + k * .018, vel * (.75 + .08 * (k % 3)))
        if v['pad']:
            for m in CHm[ci][:4]:
                nn = int(4 * BEAT * SR); tt = np.arange(nn) / SR; put(rch, np.sin(2 * np.pi * midi(m) * tt) * np.minimum(1, tt / .8) * np.minimum(1, (4 * BEAT - tt) / .8) * .12, b0, 1)
        for pos, ln_ in ((0, 1.2), (1.5, .8), (2.5, .8), (3.5, .5)):
            m = int(ln_ * BEAT * SR); tt = np.arange(m) / SR; f = midi(ROOT[ci]); put(bass, (np.sin(2 * np.pi * f * tt) + .25 * np.sin(2 * np.pi * f * 2 * tt)) * expenv(m, .4, .01), b0 + pos * BEAT, .9)
        for pos, g in ((0, 1.0), (2.5, .8), (3.25 if bar % 2 else 1.75, .5)): put(drm, kick(), b0 + pos * BEAT, g)
        for pos in (1, 3): put(drm, snare(), b0 + pos * BEAT + .004, .7)
        for e_ in range(8): put(drm, hat(), b0 + (e_ * .5 + (v['sw'] if e_ % 2 else 0)) * BEAT, (.55 if e_ % 2 else .8) * r.uniform(.6, 1))
        put(drm, hat(True), b0 + 3.5 * BEAT + v['sw'] * BEAT, .4)
        if v['mel'] and bar >= 1:
            for j in range(8):
                if r.random() < .45: put(mel, pluck(PENT[mp[(bar * 8 + j) % 64]]), b0 + j * .5 * BEAT + (v['sw'] * BEAT if j % 2 else 0), .5)
    rch = lp(rch, 2400, 2) * (1 + .15 * np.sin(2 * np.pi * 4.3 * t)); mel = lp(mel, 3500, 1)
    if rev: rch = reverb(rch, .22); mel = reverb(mel, .3, seed=5)
    mus = rch + bass * .85 + drm * .7 + mel * .22
    cr = np.zeros(n); idx = r.integers(0, n, int(dur * 45)); cr[idx] = r.uniform(-1, 1, len(idx)) * r.uniform(.1, .6, len(idx)) ** 2
    vin = lp(noise(n), 6000, 1) * .02 + lp(cr, 7000, 1) * .06
    return (nrm(mus)).astype(np.float32), vin.astype(np.float32)

SECTIONS = [dict(prog=0, mel=True, pad=False), dict(prog=2, mel=False, pad=True), dict(prog=1, mel=True, pad=False), dict(prog=3, mel=False, pad=True),
            dict(prog=0, mel=True, pad=True), dict(prog=5, mel=True, pad=False), dict(prog=2, mel=True, pad=True), dict(prog=4, mel=False, pad=True)]
def long_bed(total, bpm=84, bars_per_section=16, seed=100):
    """ONE continuous bed for the whole video body (rule 31): constant tempo, a new chord family every 16 bars (about 46 s) so it never feels like one 4-chord loop,
    sections joined on bar lines (chords ring over the join), one vinyl-noise layer over everything. Bed second 0 = the start of chapter 2 (video 66.4 s)."""
    BAR = 4 * 60 / bpm; nsec = int(total / (bars_per_section * BAR)) + 1; N = int((nsec * bars_per_section * BAR + 3) * SR); out = np.zeros(N); tail = 2.4
    for k in range(nsec):
        sc = SECTIONS[k % len(SECTIONS)]; v = dict(bpm=bpm, sw=.12 + .01 * (k % 3), **sc)
        m, _ = lofi(0, v, seed + 17 * k, bars=bars_per_section, tail=tail, rev=True)
        m = m.astype(float); fo = int(1.4 * SR); m[-fo:] *= np.cos(np.linspace(0, np.pi / 2, fo)) ** 2      # ring-out tapers away
        if k == 0: m[:int(.02 * SR)] *= np.linspace(0, 1, int(.02 * SR))
        put(out, m, k * bars_per_section * BAR)
    t = np.arange(N) / SR; rr = np.random.default_rng(seed + 999); cr = np.zeros(N); idx = rr.integers(0, N, int(N / SR * 45)); cr[idx] = rr.uniform(-1, 1, len(idx)) * rr.uniform(.1, .6, len(idx)) ** 2
    vin = lp(rr.standard_normal(N), 6000, 1) * .02 + lp(cr, 7000, 1) * .06
    x = nrm(nrm(out) * .9 + vin); return x[:int(total * SR)]
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--dur', type=float, default=130.0); ap.add_argument('--var', type=int, default=0); ap.add_argument('--seed', type=int, default=100); ap.add_argument('--long', action='store_true', help='one continuous bed with a new chord family every 16 bars (use for the whole video body)')
    a = ap.parse_args()
    if a.long:
        x = long_bed(a.dur, seed=a.seed)
        with wave.open(a.out, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767 * .9).astype(np.int16).tobytes())
        print('wrote', a.out, a.dur, 's long bed, 84 BPM'); return
    m, vn = lofi(a.dur, VAR[a.var % len(VAR)], a.seed)
    x = nrm(m * .9 + vn)          # vinyl noise rides on the bed so it stays one file
    with wave.open(a.out, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767 * .9).astype(np.int16).tobytes())
    print('wrote', a.out, a.dur, 's', VAR[a.var % len(VAR)]['bpm'], 'BPM')
if __name__ == '__main__': main()
