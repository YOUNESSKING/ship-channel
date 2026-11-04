"""Ship-channel SFX kit, synthesized in-house (numpy + scipy only, no downloads, no samples).

    python3 kit/ship/sfx/make_sfx.py            # every sound + the listening reel (about 1-2 min on 4 cores)
    python3 kit/ship/sfx/make_sfx.py horn sonar  # only the families whose name starts with these words

Writes 48 kHz / 24-bit stereo WAVs to kit/ship/sfx/out/ (git-ignored), loudness-normalised per family (BS.1770 integrated
loudness, levels table below and in kit/ship/sfx/levels.json), plus out/listening_reel.wav (git-ignored) and
kit/ship/sfx/listening_reel.mp3 (committed preview) with reel_cues.txt (what plays when).

Every sound is built from layers: oscillators with pitch curves, filtered noise, modal (resonant metal) banks, Minnaert bubbles,
envelopes, synthetic-impulse convolution reverb and low-pass "underwater" versions. Seeds are fixed, so a re-run gives the
same files. Change a recipe below and re-run to tweak it.
"""
import json, math, os, subprocess, sys
import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

# ------------------------------------------------------------------ DSP toolkit
def secs(t): return int(round(t * SR))
def tvec(n): return np.arange(n) / SR

def noise(n, rng, color="white"):
    """white / pink / brown noise via the FFT (so it is also perfectly circular = loopable)."""
    spec = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR); f[0] = f[1]
    if color == "pink": spec /= np.sqrt(f)
    elif color == "brown": spec /= f
    spec[0] = 0   # no DC
    x = np.fft.irfft(spec, n)
    return x / (np.std(x) + 1e-12)

def band_noise(n, rng, lo, hi, color="white"):
    """circular band-limited noise (FFT mask with soft edges): loop-safe."""
    spec = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); f[0] = 1
    if color == "pink": spec /= np.sqrt(f)
    elif color == "brown": spec /= f
    m = 1 / (1 + (lo / f) ** 4) / (1 + (f / hi) ** 4)
    x = np.fft.irfft(spec * m, n)
    return x / (np.std(x) + 1e-12)

def sos(kind, f, order=4):
    if kind == "bp": return signal.butter(order, [f[0], f[1]], "bandpass", fs=SR, output="sos")
    return signal.butter(order, f, {"lp": "lowpass", "hp": "highpass"}[kind], fs=SR, output="sos")
def lp(x, f, o=4): return signal.sosfilt(sos("lp", f, o), x, axis=0)
def hp(x, f, o=4): return signal.sosfilt(sos("hp", f, o), x, axis=0)
def bp(x, lo, hi, o=2): return signal.sosfilt(sos("bp", (lo, hi), o), x, axis=0)

def tv_lp(x, cut):
    """time-varying one-pole-ish low-pass (cutoff curve in Hz, same length as x), done as a 2x cascaded one-pole."""
    a = np.exp(-2 * np.pi * np.clip(cut, 10, SR * 0.45) / SR)
    y = np.empty_like(x); z1 = z2 = 0.0
    for i in range(len(x)):
        z1 = (1 - a[i]) * x[i] + a[i] * z1
        z2 = (1 - a[i]) * z1 + a[i] * z2
        y[i] = z2
    return y

def osc(freq, shape="sine", phase0=0.0):
    """oscillator from a frequency curve (array, Hz)."""
    ph = phase0 + 2 * np.pi * np.cumsum(freq) / SR
    if shape == "sine": return np.sin(ph)
    if shape == "saw":   # band-limited-ish additive saw
        out = np.zeros_like(ph); fmax = float(np.max(freq))
        for k in range(1, max(2, int(9000 / max(fmax, 20)))):
            out += np.sin(k * ph) / k
        return out * 0.6
    raise ValueError(shape)

def env_adsr(n, a, d, s, r, curve=2.0):
    na, nd, nr = secs(a), secs(d), secs(r); ns = max(0, n - na - nd - nr)
    e = np.concatenate([np.linspace(0, 1, max(1, na)) ** curve, 1 - (1 - s) * np.linspace(0, 1, max(1, nd)),
                        np.full(ns, s), s * (1 - np.linspace(0, 1, max(1, nr))) ** curve])
    return np.pad(e, (0, max(0, n - len(e))))[:n]

def exp_dec(n, tau, delay=0.0):
    t = tvec(n) - delay
    return np.where(t < 0, 0, np.exp(-np.maximum(t, 0) / tau))

def smooth_rand(n, rng, rate, lo=0.0, hi=1.0):
    """slow random curve (control signal) with about `rate` changes per second."""
    k = max(2, int(n / SR * rate) + 2)
    pts = rng.uniform(lo, hi, k)
    return np.interp(np.linspace(0, k - 1, n), np.arange(k), pts)

def modal_ir(dur, modes, rng=None, jitter=0.0):
    """impulse response of a bank of resonant modes [(freq, decay_s, amp)] = struck / rubbed metal."""
    n = secs(dur); t = tvec(n); ir = np.zeros(n)
    for f, dec, a in modes:
        if rng is not None and jitter: f *= 1 + rng.uniform(-jitter, jitter)
        ir += a * np.sin(2 * np.pi * f * t + (rng.uniform(0, 6.28) if rng is not None else 0)) * np.exp(-t / dec)
    return ir

def conv(x, ir): return signal.fftconvolve(x, ir)[:len(x)]

def reverb_ir(t60, rng, damp=4000.0, predelay=0.01, early=6, dark_end=800.0, size=1.0):
    """synthetic room / water impulse: early taps + exponentially decaying noise that gets darker with time. Stereo (2 columns)."""
    n = secs(t60 * 1.1 + predelay + 0.05)
    t = tvec(n)
    out = np.zeros((n, 2))
    for ch in range(2):
        nz = rng.standard_normal(n)
        tail = nz * np.exp(-6.9 * t / t60)
        # darken over time: crossfade a bright and a dark copy
        bright, dark = lp(tail, damp, 2), lp(tail, dark_end, 2)
        mix = np.clip(t / (t60 * 0.6), 0, 1)
        tail = bright * (1 - mix) + dark * mix
        pd = secs(predelay)
        tail = np.concatenate([np.zeros(pd), tail])[:n]
        for k in range(early):
            d = secs(predelay * 0.3 + rng.uniform(0.004, 0.06) * size)
            if d < n: tail[d] += rng.uniform(0.2, 0.6) * rng.choice([-1, 1])
        out[:, ch] = tail
    return out / np.max(np.abs(out))

def add_reverb(x, ir, wet=0.3, dry=1.0):
    """x mono or stereo -> stereo with reverb."""
    if x.ndim == 1: x = np.stack([x, x], 1)
    n = len(x) + len(ir)
    xp = np.pad(x, ((0, len(ir)), (0, 0)))
    w = np.stack([signal.fftconvolve(xp[:, c], ir[:, c])[:n] for c in range(2)], 1)
    w /= (np.sqrt(np.sum(ir ** 2, 0)) + 1e-9)
    return xp * dry + w * wet

def underwater(x, cut=700.0, res=True):
    """the 'heard through water' version: low-pass, a soft resonant bump, a little slap-back."""
    y = lp(x, cut, 4)
    if res:
        y = y + 0.35 * bp(x, cut * 0.35, cut * 0.75, 2)
    return y

def stereo(x, width=0.3, rng=None, delay_ms=11):
    if x.ndim == 2: return x
    d = secs(delay_ms / 1000)
    r = np.concatenate([np.zeros(d), x])[:len(x)]
    return np.stack([x, x * (1 - width) + r * width], 1)

def place(dst, src, t0, gain=1.0):
    """mix src (mono/stereo) into dst (stereo) at t0 seconds."""
    if src.ndim == 1: src = np.stack([src, src], 1)
    i = secs(t0); j = min(len(dst), i + len(src))
    if j > i: dst[i:j] += src[: j - i] * gain
    return dst

def place_circ(dst, src, t0, gain=1.0):
    """mix with wrap-around (for loopable beds)."""
    if src.ndim == 1: src = np.stack([src, src], 1)
    n = len(dst); idx = (secs(t0) + np.arange(len(src))) % n
    np.add.at(dst, idx, src * gain)
    return dst

def fade(x, a=0.005, r=0.05):
    n = len(x); e = np.ones(n)
    na, nr = min(n, secs(a)), min(n, secs(r))
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] = np.minimum(e[-nr:], np.linspace(1, 0, nr))
    return x * (e[:, None] if x.ndim == 2 else e)

def trim_tail(x, thresh_db=-70):
    a = np.max(np.abs(x), 1) if x.ndim == 2 else np.abs(x)
    th = np.max(a) * 10 ** (thresh_db / 20)
    idx = np.nonzero(a > th)[0]
    return x[: (idx[-1] + secs(0.05)) if len(idx) else len(x)]

def soft_limit(x, ceiling=0.89):
    return np.tanh(x / ceiling) * ceiling

# ------------------------------------------------------------------ bubbles
def bubble(rng, r_mm=None, f=None, dur=None, rise=0.25):
    """one Minnaert bubble: a damped sine whose pitch rises as it resonates (f ~ 3.26 m/s / radius)."""
    if f is None: f = 3260.0 / max(r_mm, 0.3)
    dur = dur or min(0.12, 6.0 / f + 0.02)
    n = secs(dur); t = tvec(n)
    fr = f * (1 + rise * t / dur)
    damp = 0.13 * f / 8   # bigger bubbles ring longer
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * (20 + damp))
    return x * np.minimum(1, t / 0.0015)

def bubble_stream(n, rng, rate_curve, rmin=1.5, rmax=12.0, gain=0.4):
    """random bubbles; rate_curve = bubbles per second over time (array len n)."""
    out = np.zeros(n); t = 0.0
    while True:
        i = min(n - 1, secs(t)); rate = max(rate_curve[i], 0.5)
        t += rng.exponential(1 / rate)
        if t >= n / SR: break
        r = math.exp(rng.uniform(math.log(rmin), math.log(rmax)))
        b = bubble(rng, r) * gain * rng.uniform(0.3, 1.0) * (r / rmax) ** 0.3
        i = secs(t); j = min(n, i + len(b)); out[i:j] += b[: j - i]
    return out

# ------------------------------------------------------------------ loudness (ITU-R BS.1770-4, integrated, gated)
def lufs(x):
    if x.ndim == 1: x = np.stack([x, x], 1)
    # K-weighting at 48 kHz (BS.1770 reference coefficients)
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    y = signal.lfilter(b2, a2, signal.lfilter(b1, a1, x, axis=0), axis=0)
    blk, hop = secs(0.4), secs(0.1)
    if len(y) < blk: y = np.pad(y, ((0, blk - len(y)), (0, 0)))
    ms = np.array([np.sum(np.mean(y[i:i + blk] ** 2, 0)) for i in range(0, len(y) - blk + 1, hop)])
    L = -0.691 + 10 * np.log10(ms + 1e-12)
    g = ms[L > -70]
    if not len(g): return -70.0
    rel = -0.691 + 10 * np.log10(np.mean(g)) - 10
    g = ms[(L > -70) & (L > rel)]
    return float(-0.691 + 10 * np.log10(np.mean(g)))

def normalize(x, target, peak_db=-1.0):
    x = x / (np.max(np.abs(x)) + 1e-12) * 0.5
    ceil = 10 ** (peak_db / 20)
    for _ in range(4):   # gain to target; if the peak goes over, soft-limit and try again
        x = x * 10 ** ((target - lufs(x)) / 20)
        if np.max(np.abs(x)) <= ceil: break
        x = soft_limit(x, ceil * 0.98)
    if np.max(np.abs(x)) > ceil: x *= ceil / np.max(np.abs(x))
    return x

# ------------------------------------------------------------------ the sounds
# Each recipe: f(rng, v) -> stereo array; v = variation index (0, 1, 2).

def horn(rng, v, distant=False):
    f0 = [73.0, 62.0, 87.0][v]               # big-ship horn fundamentals (deep)
    blasts = [(0.0, 3.6)] if v != 2 else [(0.0, 1.5), (2.0, 1.5)]   # v2 = two short blasts
    total = (blasts[-1][0] + blasts[-1][1]) + 0.2
    n = secs(total); x = np.zeros(n)
    for t0, L in blasts:
        m = secs(L); t = tvec(m)
        bend = 1 - 0.07 * np.exp(-t / 0.12)                          # pitch scoops up as the air builds
        drop = 1 - 0.03 * np.clip((t - (L - 0.35)) / 0.35, 0, 1)      # sags as the valve closes
        vib = 1 + 0.004 * np.sin(2 * np.pi * 4.7 * t) + 0.002 * smooth_rand(m, rng, 6, -1, 1)
        fr = f0 * bend * drop * vib
        tone = osc(fr, "saw") + 0.5 * osc(fr * 2.003, "saw") * 0.5
        if v == 1: tone += 0.55 * osc(fr * 1.335, "saw")              # v1 = two-tone chord (liner style)
        # body: diaphragm/trumpet formants
        body = bp(tone, f0 * 1.6, f0 * 7, 2) + 0.6 * bp(tone, 380, 900, 2) + 0.25 * bp(tone, 1400, 2600, 2)
        sub = 0.5 * osc(fr, "sine")
        breath = 0.07 * bp(noise(m, rng, "pink"), 300, 2500, 2)
        e = env_adsr(m, 0.28, 0.2, 0.85, 0.5, 1.5)
        part = np.tanh(1.6 * (body + sub + breath)) * e
        x[secs(t0):secs(t0) + m] += part
    if distant:
        x = lp(x, 900, 2) + 0.4 * lp(x, 300, 2)                       # air absorption
        ir = reverb_ir(4.5, rng, damp=1800, predelay=0.04, early=4, dark_end=400, size=4)
        y = add_reverb(x, ir, wet=1.1, dry=0.45)
        echo = np.pad(lp(x, 600), (secs(0.62), 0))[:len(x)]          # slap off the shore / hull
        y[: len(echo)] += np.stack([echo * 0.25, echo * 0.3], 1)
    else:
        ir = reverb_ir(1.6, rng, damp=5000, predelay=0.012, early=8, dark_end=900, size=1.5)
        y = add_reverb(stereo(x, 0.2), ir, wet=0.32, dry=1.0)
    return trim_tail(fade(y, 0.01, 0.4))

def hull_groan(rng, v):
    dur = [5.0, 6.5, 4.0][v]; n = secs(dur); t = tvec(n)
    base = [41.0, 34.0, 52.0][v]
    # stick-slip excitation: an irregular pulse train whose rate glides (steel plates grinding)
    rate = base * 0.5 * (1 + 0.6 * smooth_rand(n, rng, 1.2, -1, 1)) * (1 + 0.5 * np.sin(np.pi * t / dur))
    ph = np.cumsum(rate) / SR; pulses = np.diff(np.floor(ph), prepend=0) > 0
    exc = pulses * rng.uniform(0.5, 1.0, n) + 0.04 * noise(n, rng, "brown")
    modes = [(base * k * (1 + 0.013 * k * k), rng.uniform(0.25, 0.9), 1 / k ** 0.7) for k in (1, 1.53, 2.21, 2.94, 3.87, 5.12, 6.6, 8.3)]
    body = conv(exc, modal_ir(1.5, modes, rng, 0.02))
    # slow bending tone (the hull 'moaning') + sub
    fr = base * (1 + 0.12 * smooth_rand(n, rng, 0.8, -1, 1))
    moan = (osc(fr, "saw") * 0.3 + osc(fr * 0.5) * 0.6) * smooth_rand(n, rng, 2.0, 0.2, 1.0)
    x = body / (np.std(body) + 1e-9) * 0.6 + moan * 0.5
    x *= env_adsr(n, 0.9, 0.5, 0.8, 1.6, 1.3)
    x = underwater(x, 1100)
    ir = reverb_ir(3.5, rng, damp=1200, predelay=0.03, early=5, dark_end=300, size=3)
    return trim_tail(fade(add_reverb(x, ir, wet=0.7, dry=0.8), 0.02, 0.5))

def metal_creak(rng, v):
    dur = [1.8, 2.6, 1.3][v]; n = secs(dur); t = tvec(n)
    # rate sweeps (tight -> loose = creak glides up), with jitter
    r0, r1 = [(28, 110), (18, 70), (60, 150)][v]
    rate = (r0 + (r1 - r0) * (t / dur) ** 1.4) * (1 + 0.25 * smooth_rand(n, rng, 9, -1, 1))
    ph = np.cumsum(rate) / SR; pulses = (np.diff(np.floor(ph), prepend=0) > 0).astype(float)
    amp = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.6 * smooth_rand(n, rng, 5, 0.4, 1.0)
    exc = pulses * amp * rng.uniform(0.6, 1, n)
    f1 = [310, 240, 420][v]
    modes = [(f1 * k, rng.uniform(0.03, 0.12), 1 / k ** 0.5) for k in (1, 1.71, 2.63, 3.4, 4.9, 6.8, 8.1)]
    x = conv(exc, modal_ir(0.4, modes, rng, 0.03))
    # rivet pops: sharp ticks through high, short modes
    for _ in range([3, 2, 4][v]):
        t0 = rng.uniform(0.1, dur - 0.2); pop = np.zeros(secs(0.25)); pop[0] = 1
        pr = conv(pop, modal_ir(0.25, [(rng.uniform(1800, 4200) * k, 0.02, 1 / k) for k in (1, 1.4, 2.3)], rng))
        x[secs(t0):secs(t0) + len(pr)] += pr[: max(0, min(len(pr), n - secs(t0)))] * 1.8
    x = hp(x, 120, 2)
    ir = reverb_ir(1.4, rng, damp=3500, predelay=0.008, early=8, dark_end=700, size=1)
    return trim_tail(fade(add_reverb(stereo(x, 0.4), ir, wet=0.45), 0.003, 0.2))

def sink_whoomp(rng, v):
    dur = [6.0, 7.0, 5.0][v]; n = secs(dur); t = tvec(n); x = np.zeros(n)
    # 1) the whoomp: hull pushes the water away (low pitch drop + sub + muffled noise swell)
    f = [52, 44, 60][v] * (1 + 0.9 * np.exp(-t / 0.18))
    who = osc(f) * exp_dec(n, 0.55) * np.minimum(1, t / 0.02)
    who += 0.6 * lp(noise(n, rng, "brown"), 180) * exp_dec(n, 0.8) * np.minimum(1, t / 0.05)
    x += who * 2.2
    # 2) air release: turbulent roaring vent that peaks ~1 s in
    vent_env = np.clip((t - 0.35) / 0.9, 0, 1) ** 1.5 * np.exp(-np.maximum(t - 1.25, 0) / [1.8, 2.5, 1.2][v])
    vent = bp(noise(n, rng, "pink"), 150, 1400, 2) * (0.6 + 0.4 * smooth_rand(n, rng, 14, 0, 1)) * vent_env
    x += underwater(vent, 900) * 0.7
    # 3) rising bubbles: dense big glugs first, then smaller and sparser
    rate = 220 * np.exp(-np.maximum(t - 0.4, 0) / [1.6, 2.2, 1.2][v]) * np.clip((t - 0.25) / 0.4, 0, 1) + 6
    x += bubble_stream(n, rng, rate, rmin=2.5, rmax=[22, 26, 16][v], gain=0.55)
    x += 0.5 * bubble_stream(n, rng, rate * 0.4, rmin=12, rmax=40, gain=0.6)   # big low glugs
    x = lp(x, 3200, 2)
    ir = reverb_ir(2.8, rng, damp=1500, predelay=0.02, early=5, dark_end=350, size=2)
    return trim_tail(fade(add_reverb(x, ir, wet=0.55, dry=0.9), 0.003, 0.6))

def charge_thump(rng, size=1.0, dist=0.0):
    """one muffled underwater demolition charge. size 0.5-1.5, dist 0 (close) - 1 (far)."""
    n = secs(2.2); t = tvec(n)
    f = (48 / size ** 0.3) * (1 + 1.8 * np.exp(-t / 0.05))
    body = osc(f) * exp_dec(n, 0.16 * size) * np.minimum(1, t / 0.002)
    crack = lp(noise(n, rng), 1600 - 900 * dist) * exp_dec(n, 0.03)
    rumble = lp(noise(n, rng, "brown"), 120) * exp_dec(n, 0.3 * size, 0.02)
    x = body * 1.2 + crack * 0.6 + rumble * 0.4
    return lp(x, 900 - 450 * dist, 2) * (1 - 0.55 * dist)

def charges_seq(rng, v):
    """demolition charges going off in a sequence along the hull, heard underwater."""
    count, spread, dist = [(8, 0.42, 0.15), (5, 0.7, 0.75), (12, 0.2, 0.35)][v]
    times = np.cumsum(rng.uniform(spread * 0.6, spread * 1.4, count)); times -= times[0]; times += 0.05
    n = secs(times[-1] + 3.5); y = np.zeros((n, 2))
    for k, tt in enumerate(times):
        th = charge_thump(rng, rng.uniform(0.7, 1.3), np.clip(dist + rng.uniform(-0.1, 0.15), 0, 1))
        pan = rng.uniform(-0.6, 0.6)
        place(y, np.stack([th * (1 - pan * 0.5), th * (1 + pan * 0.5)], 1), tt)
    # shock rattles the water: a few bubbles after each blast
    rate = np.zeros(n)
    for tt in times: rate += 60 * exp_dec(n, 0.3, tt + 0.08)
    b = bubble_stream(n, rng, rate + 2, rmin=3, rmax=20, gain=0.18)
    y += stereo(lp(b, 2000), 0.5)
    ir = reverb_ir(2.2, rng, damp=1000, predelay=0.03, early=4, dark_end=250, size=4)
    return trim_tail(fade(add_reverb(y, ir, wet=0.4, dry=1.0), 0.002, 0.8))

def flood_rush(rng, v):
    dur = [4.5, 5.5, 3.5][v]; n = secs(dur); t = tvec(n)
    turb = smooth_rand(n, rng, 18, 0.3, 1.0) * smooth_rand(n, rng, 3, 0.5, 1.0)
    e = env_adsr(n, [0.25, 1.2, 0.05][v], 0.3, 0.85, 1.0, 1.5)
    rush = bp(noise(n, rng, "pink"), 180, 4200, 2) * turb
    roar = lp(noise(n, rng, "brown"), 140) * 0.9
    glug = bubble_stream(n, rng, np.full(n, 90.0), rmin=6, rmax=35, gain=0.5)
    x = (rush * 0.8 + roar + glug) * e
    if v == 0:    # inside the hull: metallic room colour (comb + hangar reverb)
        d = secs(1 / 92.0); x = x + 0.5 * np.concatenate([np.zeros(d), x])[:n]
        ir = reverb_ir(2.2, rng, damp=2500, predelay=0.015, early=10, dark_end=500, size=2)
        y = add_reverb(x, ir, wet=0.5)
    elif v == 1:  # heard from underwater
        ir = reverb_ir(2.6, rng, damp=1100, predelay=0.02, early=4, dark_end=300, size=2)
        y = add_reverb(underwater(x, 650), ir, wet=0.6)
    else:         # close burst: a hatch gives way
        burst = bp(noise(n, rng), 300, 6000, 2) * exp_dec(n, 0.25) * 1.4
        ir = reverb_ir(1.2, rng, damp=4000, predelay=0.01, early=8, dark_end=700, size=1)
        y = add_reverb(stereo(x + burst, 0.5), ir, wet=0.3)
    return trim_tail(fade(y, 0.01, 0.6))

def swell_bed(rng, v):
    """60 s ocean swell, seamlessly loopable (all noise is circular, every modulator has a whole number of cycles in 60 s)."""
    L = 60.0; n = secs(L); t = tvec(n); y = np.zeros((n, 2))
    waves = [(8, 1.0), (5, 0.6), (11, 0.35)] if v == 0 else [(6, 1.0), (10, 0.4), (4, 0.5)]   # cycles per 60 s
    def cyc(k, ph=0.0, sharp=2.0): return (0.5 + 0.5 * np.sin(2 * np.pi * k * t / L + ph)) ** sharp
    swell = sum(a * cyc(k, rng.uniform(0, 6.28)) for k, a in waves); swell /= swell.max()
    bands = [(35, 140, "brown", 0.9, 0.0), (140, 500, "pink", 0.7, 0.3), (500, 1800, "pink", 0.45, 0.6), (1800, 7000, "white", 0.12, 0.9)]
    for ch in range(2):
        for lo, hi, col, g, lag in bands:
            nz = band_noise(n, rng, lo, hi, col)
            shift = secs(lag * 1.2)
            m = np.roll(swell, shift) ** (1 + lag)     # foam / hiss peaks a moment after the swell
            y[:, ch] += nz * g * (0.25 + 0.75 * m)
    if v == 1:   # calmer: water lapping on a hull (wrapped so the loop stays seamless)
        for k in range(14):
            t0 = rng.uniform(0, L); m = secs(0.5); tt = tvec(m)
            slap = (bp(noise(m, rng), 200, 1600, 2) * np.exp(-tt / 0.09) + 0.6 * np.sin(2 * np.pi * 95 * tt) * np.exp(-tt / 0.07))
            place_circ(y, stereo(slap, 0.6), t0, rng.uniform(0.3, 0.7))
    return y   # no fades: it loops

def underwater_bed(rng, v):
    """60 s muffled underwater ambience (pressure, distant rumble, rare far creaks + bubble clusters), loopable."""
    L = 60.0; n = secs(L); t = tvec(n); y = np.zeros((n, 2))
    for ch in range(2):
        press = band_noise(n, rng, 18, [380, 260][v], "brown")
        rumble = band_noise(n, rng, 22, 70, "white")
        k1, k2 = [(3, 7), (2, 5)][v]
        sw = 0.6 + 0.25 * np.sin(2 * np.pi * k1 * t / L + rng.uniform(0, 6)) + 0.15 * np.sin(2 * np.pi * k2 * t / L + rng.uniform(0, 6))
        fizz = band_noise(n, rng, 1800, 5000, "white") * 0.012
        y[:, ch] = press * 0.8 * sw + rumble * 0.45 * (1.2 - sw) + fizz
    for k in range([5, 3][v]):    # distant bubble clusters
        m = secs(1.6); b = bubble_stream(m, rng, np.full(m, 40.0) * np.exp(-tvec(m) / 0.5), rmin=4, rmax=18, gain=0.25)
        place_circ(y, stereo(lp(b, 900), 0.7), rng.uniform(0, L), 0.6)
    for k in range([2, 3][v]):    # far metal stress
        m = secs(2.5); tt = tvec(m)
        fr = rng.uniform(70, 130) * (1 + 0.15 * np.sin(2 * np.pi * 0.4 * tt))
        g = lp(osc(fr, "saw"), 400) * np.sin(np.pi * tt / 2.5) ** 2
        place_circ(y, stereo(g, 0.8), rng.uniform(0, L), 0.12)
    return y

def sonar_ping(rng, v):
    f0 = [1450.0, 1180.0, 1720.0][v]; n = secs(0.5); t = tvec(n)
    fr = f0 * (1 - 0.015 * t / 0.5)
    p = (np.sin(2 * np.pi * np.cumsum(fr) / SR) + 0.15 * np.sin(2 * np.pi * np.cumsum(fr * 2.01) / SR)) * np.exp(-t / 0.11) * np.minimum(1, t / 0.004)
    total = secs(3.8); x = np.zeros(total); x[:n] += p
    if v != 2:   # faint return echo
        d = secs([1.05, 1.4][v]); x[d:d + n] += lp(p, 1600) * 0.22
    ir = reverb_ir(2.6, rng, damp=2200, predelay=0.03, early=3, dark_end=600, size=5)
    return trim_tail(fade(add_reverb(stereo(x, 0.3), ir, wet=0.55), 0.002, 0.8))

def dive_whoosh(rng, v):
    """map / camera dive that sounds wet: a splash in, a down-sweeping muffled rush, bubbles trailing, a low swell."""
    dur = [1.8, 2.4, 1.3][v]; n = secs(dur); t = tvec(n)
    shape = np.clip(t / (dur * 0.35), 0, 1) ** 1.5 * np.exp(-np.maximum(t - dur * 0.35, 0) / (dur * 0.3))
    cut = 3200 * np.exp(-t / (dur * 0.35)) + 220
    rush = tv_lp(noise(n, rng, "pink"), cut) * shape * 1.6
    splash = bp(noise(n, rng), 900, 6000, 2) * exp_dec(n, 0.06) * [0.9, 0.6, 1.0][v]
    swell = osc(70 * (1 - 0.3 * t / dur)) * shape * 0.5
    bub = bubble_stream(n, rng, 160 * np.exp(-np.maximum(t - 0.1, 0) / 0.5) + 4, rmin=2, rmax=14, gain=0.35)
    x = rush + splash + swell + lp(bub, 2500)
    ir = reverb_ir(1.8, rng, damp=1500, predelay=0.015, early=4, dark_end=350, size=2)
    return trim_tail(fade(add_reverb(stereo(x, 0.5), ir, wet=0.5), 0.002, 0.3))

def number_land(rng, v):
    """number-landing hit: a low TONAL boom (pitched, inharmonic overtone) with a water tail."""
    f0 = [55.0, 49.0, 65.4][v]; n = secs(3.2); t = tvec(n)
    fr = f0 * (1 + 0.6 * np.exp(-t / 0.035))
    tone = osc(fr) * exp_dec(n, 0.9) + 0.35 * osc(fr * 2.0) * exp_dec(n, 0.45) + 0.12 * osc(fr * 2.76) * exp_dec(n, 0.35)
    sub = 0.6 * osc(fr * 0.5) * exp_dec(n, 0.7)
    click = lp(noise(n, rng), 2200) * exp_dec(n, 0.012) * 0.8
    wash = underwater(lp(noise(n, rng, "pink"), 900) * np.clip(t / 0.15, 0, 1) * exp_dec(n, 0.7, 0.05), 700) * 0.4
    bub = lp(bubble_stream(n, rng, 70 * exp_dec(n, 0.45, 0.06) + 1, rmin=3, rmax=18, gain=0.25), 1800)
    x = np.tanh(1.3 * (tone + sub)) + click + wash + bub
    ir = reverb_ir(2.4, rng, damp=1300, predelay=0.02, early=4, dark_end=300, size=3)
    return trim_tail(fade(add_reverb(stereo(x, 0.25), ir, wet=0.45), 0.001, 0.6))

STEEL = [(98, 1.2, 1.0), (231, 0.9, 0.8), (377, 0.7, 0.6), (542, 0.55, 0.5), (781, 0.4, 0.45), (1187, 0.3, 0.35), (1730, 0.22, 0.25), (2570, 0.15, 0.2), (3420, 0.1, 0.12)]
def text_slam(rng, v):
    """heavy steel impact for a text card: thump + a big plate's modes + hangar room."""
    n = secs(2.6); t = tvec(n)
    scale = [1.0, 0.78, 1.25][v]
    exc = np.zeros(n); exc[0] = 1; exc[:secs(0.004)] += rng.standard_normal(secs(0.004)) * 0.3
    modes = [(f * scale, d * (0.6 if v == 1 else 1.0), a) for f, d, a in STEEL]
    ring = conv(exc, modal_ir(2.0, modes, rng, 0.015)); ring /= np.max(np.abs(ring))
    thump = osc(52 * (1 + 1.2 * np.exp(-t / 0.03))) * exp_dec(n, 0.22)
    crack = hp(noise(n, rng), 1500) * exp_dec(n, 0.01) * 0.5
    x = thump * 1.1 + ring * [0.6, 0.35, 0.75][v] + crack
    if v == 2:    # double-hit: the plate lands then bounces once
        x += np.concatenate([np.zeros(secs(0.11)), x * 0.45])[:n]
    ir = reverb_ir(1.5, rng, damp=4500, predelay=0.012, early=10, dark_end=800, size=2.5)
    return trim_tail(fade(add_reverb(stereo(np.tanh(1.2 * x), 0.3), ir, wet=0.35), 0.001, 0.4))

def strike_scrape(rng, v):
    """strike-out: a blade / steel edge dragged across plate (friction through metal modes), ending on a small clink."""
    dur = [0.8, 1.0, 0.6][v]; n = secs(dur + 0.6); t = tvec(n)
    move = (t < dur).astype(float) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.5
    rate = (55 + 40 * t / dur) * (1 + 0.3 * smooth_rand(n, rng, 20, -1, 1))
    ph = np.cumsum(rate) / SR; pulses = (np.diff(np.floor(ph), prepend=0) > 0).astype(float)
    exc = pulses * move * 0.5 + bp(noise(n, rng), 1500, 7000, 2) * move * 0.08
    modes = [(f * [1.9, 1.5, 2.4][v], d * 0.3, a) for f, d, a in STEEL]
    x = conv(exc, modal_ir(0.6, modes, rng, 0.03))
    hiss = tv_lp(bp(noise(n, rng), 2000, 9000, 2), 2500 + 4000 * t / dur) * move * 0.3
    x = x / (np.max(np.abs(x)) + 1e-9) + hiss
    clink = np.zeros(n); clink[secs(dur)] = 1
    x += conv(clink, modal_ir(0.5, [(f * 3.1, d * 0.25, a) for f, d, a in STEEL[2:]], rng)) * 0.5
    ir = reverb_ir(1.0, rng, damp=5000, predelay=0.008, early=8, dark_end=900, size=1)
    return trim_tail(fade(add_reverb(stereo(x, 0.4), ir, wet=0.3), 0.002, 0.2))

def riser(rng, v, dur):
    """tension build: rising detuned drone, swelling filtered noise, a heartbeat that speeds up, a groaning hull layer,
    a reverse-reverb swell into a hard stop (so the next hit lands cleanly)."""
    n = secs(dur); t = tvec(n); u = t / dur
    f0 = [41.2, 36.7][v]
    drone = np.zeros(n)
    for det in (-0.006, 0.0, 0.007):
        drone += osc(f0 * (1 + det) * 2 ** (1.2 * u ** 2), "saw")
    drone = tv_lp(drone, 180 + 2600 * u ** 2.2) * (0.2 + 0.8 * u ** 1.4)
    air = tv_lp(noise(n, rng, "pink"), 400 + 6000 * u ** 2) * u ** 2.2 * 0.7
    beat = np.zeros(n); tt = 0.0
    while tt < dur - 0.15:
        m = secs(0.35); b = osc(np.full(m, 48.0)) * exp_dec(m, 0.08)
        i = secs(tt); j = min(n, i + m); beat[i:j] += b[: j - i] * (0.4 + 0.6 * tt / dur)
        tt += 0.9 - 0.65 * (tt / dur)
    x = drone * 0.7 + air + beat * 0.9
    if v == 1:  # metal layer: hull stress rising
        g = hull_groan(rng, 2)[:, 0]
        g = np.pad(g, (0, max(0, n - len(g))))[:n]
        x += g * 0.5 * u
    # reverse reverb swell on the last 1.2 s
    ir = reverb_ir(1.5, rng, damp=3000, predelay=0.0, early=0, dark_end=600)
    rev = signal.fftconvolve(x[::-1], ir[:, 0])[:n][::-1]
    x = x + 0.25 * rev / (np.max(np.abs(rev)) + 1e-9) * np.clip((u - 0.6) / 0.4, 0, 1)
    y = stereo(x, 0.5)
    y[-secs(0.012):] *= np.linspace(1, 0, secs(0.012))[:, None]   # hard stop
    return y

def reveal_hit(rng, v):
    n = secs(4.5); t = tvec(n)
    boom = osc(38 * (1 + 1.4 * np.exp(-t / 0.06))) * exp_dec(n, 1.1)
    mid = osc(110 * (1 + 0.3 * np.exp(-t / 0.02))) * exp_dec(n, 0.35) * 0.4
    exc = np.zeros(n); exc[0] = 1
    clang = conv(exc, modal_ir(3.0, [(f * [0.62, 0.5, 0.75][v], d * 1.5, a) for f, d, a in STEEL], rng)); clang /= np.max(np.abs(clang))
    crack = lp(noise(n, rng), 3000) * exp_dec(n, 0.02) * 0.6
    x = np.tanh(1.4 * (boom * 1.2 + mid)) + clang * [0.35, 0.2, 0.5][v] + crack
    if v != 2:   # water tail
        x += underwater(lp(noise(n, rng, "pink"), 800) * exp_dec(n, 1.2, 0.08), 600) * 0.35
        x += lp(bubble_stream(n, rng, 90 * exp_dec(n, 0.8, 0.1) + 1, rmin=3, rmax=25, gain=0.3), 2000)
    ir = reverb_ir(3.4, rng, damp=1600, predelay=0.02, early=6, dark_end=300, size=4)
    return trim_tail(fade(add_reverb(stereo(x, 0.3), ir, wet=0.5), 0.001, 0.8))

def catapult(rng, v):
    """steam catapult launch: shuttle clank, a rising steam/jet rush down the deck, the water-brake slam, steam hiss tail."""
    dur = 4.2; n = secs(dur); t = tvec(n); x = np.zeros(n)
    exc = np.zeros(n); exc[secs(0.02)] = 1
    x += conv(exc, modal_ir(0.5, [(f * 1.3, d * 0.3, a) for f, d, a in STEEL], rng)) * 0.5
    run = [1.9, 2.3][v]
    sh = np.clip(t / run, 0, 1)
    rush_env = (sh ** 2) * (t < run) + (t >= run) * np.exp(-np.maximum(t - run, 0) / 0.15)
    rush = tv_lp(noise(n, rng, "pink"), 300 + 4500 * sh ** 2) * rush_env
    jet = bp(noise(n, rng, "pink"), 250, 3000, 2) * (0.4 + 0.6 * sh) * np.exp(-np.maximum(t - run, 0) / 1.2)
    x += rush * 1.1 + jet * 0.5
    slam = np.zeros(n); slam[secs(run)] = 1
    x += conv(slam, modal_ir(1.0, STEEL[:6], rng)) * 0.35 + osc(np.full(n, 45.0)) * exp_dec(n, 0.25, run) * 0.9
    hiss = hp(noise(n, rng), 2500) * np.clip((t - run) / 0.1, 0, 1) * np.exp(-np.maximum(t - run, 0) / 0.9) * 0.4
    x += hiss
    ir = reverb_ir(1.4, rng, damp=5000, predelay=0.01, early=6, dark_end=900, size=3)
    return trim_tail(fade(add_reverb(stereo(x, 0.5), ir, wet=0.3), 0.002, 0.5))

# ------------------------------------------------------------------ the kit table: family -> (variations, recipe, target LUFS, loop?, what)
LEVELS_NOTE = "integrated LUFS per file; beds -30, subtle cues -24, hits / one-shots -18, risers -20 (peaks <= -1 dBFS)"
KIT = [
    ("horn_close",       3, lambda r, v: horn(r, v, False), -18, False, "deep ship horn, close (v1 two-tone, v2 two short blasts)"),
    ("horn_distant",     3, lambda r, v: horn(r, v, True),  -22, False, "deep ship horn far across the water (air absorption, long echo)"),
    ("hull_groan",       3, hull_groan,    -20, False, "underwater hull groan / metal stress"),
    ("metal_creak",      3, metal_creak,   -22, False, "rivet / plate creak with rivet pops"),
    ("sink_whoomp",      3, sink_whoomp,   -18, False, "the hull goes under: whoomp + air release + rising bubbles"),
    ("charges_seq",      3, charges_seq,   -18, False, "demolition charges, muffled underwater thumps in sequence (v1 distant, v2 rapid cascade)"),
    ("flood_rush",       3, flood_rush,    -20, False, "water rush / flooding (v0 inside the hull, v1 from underwater, v2 hatch bursts)"),
    ("swell_bed",        2, swell_bed,     -30, True,  "ocean swell bed, 60 s seamless loop (v1 calmer, water lapping the hull)"),
    ("underwater_bed",   2, underwater_bed,-30, True,  "underwater ambience, 60 s seamless loop, muffled pressure (v1 deeper)"),
    ("sonar_ping",       3, sonar_ping,    -26, False, "subtle sonar ping for the depth gauge (v0/v1 with a faint return)"),
    ("dive_whoosh",      3, dive_whoosh,   -20, False, "wet map / camera dive: splash in, muffled down-sweep, bubble trail"),
    ("number_land",      3, number_land,   -18, False, "number-landing hit: low tonal boom (A1 / G1 / C2) with a water tail"),
    ("text_slam",        3, text_slam,     -18, False, "text slam: heavy steel impact (v1 muted, v2 double hit)"),
    ("strike_scrape",    3, strike_scrape, -21, False, "strike-out: steel edge scraped across plate, small clink"),
    ("riser_4s",         2, lambda r, v: riser(r, v, 4.0), -20, False, "tension riser, 4 s, hard stop (v1 with hull groan)"),
    ("riser_8s",         2, lambda r, v: riser(r, v, 8.0), -20, False, "tension riser, 8 s, hard stop (v1 with hull groan)"),
    ("reveal_hit",       3, reveal_hit,    -17, False, "reveal hit: sub boom + steel clang + water tail (v2 dry)"),
    ("catapult_launch",  2, catapult,      -18, False, "steam catapult launch: clank, rush, water-brake slam, hiss"),
]

def build(only=None):
    os.makedirs(OUT, exist_ok=True)
    levels = {}
    for fam, nv, fn, target, loop, what in KIT:
        if only and not any(fam.startswith(o) for o in only): continue
        for v in range(nv):
            rng = np.random.default_rng(abs(hash_str(fam)) % (2 ** 31) + 101 * v)
            y = fn(rng, v)
            if y.ndim == 1: y = np.stack([y, y], 1)
            if not loop: y = fade(signal.sosfiltfilt(sos("hp", 18, 2), y, axis=0), 0.001, 0.02)   # DC / sub-rumble blocker
            y = normalize(y, target)
            name = f"{fam}_{v + 1}.wav"
            sf.write(os.path.join(OUT, name), y.astype(np.float32), SR, subtype="PCM_24")
            levels[name] = {"lufs": round(lufs(y), 1), "peak_db": round(20 * math.log10(np.max(np.abs(y))), 1),
                            "seconds": round(len(y) / SR, 2), "loop": loop, "what": what}
            print(f"{name:24s} {levels[name]['seconds']:5.1f} s  {levels[name]['lufs']:6.1f} LUFS  peak {levels[name]['peak_db']:5.1f} dB", flush=True)
    old = {}
    p = os.path.join(HERE, "levels.json")
    if only and os.path.exists(p): old = json.load(open(p))
    old.update(levels); json.dump({"note": LEVELS_NOTE, **{k: v for k, v in old.items() if k != "note"}}, open(p, "w"), indent=1)

def hash_str(s):
    h = 0
    for c in s: h = (h * 131 + ord(c)) % 2147483647
    return h

# ------------------------------------------------------------------ the listening reel (~45 s, one variation of each, gaps between)
REEL = [("horn_close_1", 2.4), ("horn_distant_2", 2.4), ("hull_groan_1", 2.2), ("metal_creak_1", 1.5), ("sink_whoomp_1", 2.6),
        ("charges_seq_1", 2.8), ("flood_rush_1", 2.0), ("swell_bed_1", 2.0), ("underwater_bed_1", 2.0), ("sonar_ping_1", 1.6),
        ("dive_whoosh_1", 1.7), ("number_land_1", 2.0), ("text_slam_1", 1.4), ("strike_scrape_1", 1.1), ("riser_4s_1", 4.0),
        ("reveal_hit_1", 2.3), ("catapult_launch_1", 2.9)]
GAP = 0.45

def reel():
    parts, cues, tpos = [], [], 0.4
    out = [np.zeros((secs(0.4), 2))]
    for name, L in REEL:
        x, sr = sf.read(os.path.join(OUT, name + ".wav")); assert sr == SR
        x = x[: secs(L)]
        x = fade(x, 0.004, 0.35 if len(x) >= secs(L) else 0.05)
        x = x * (10 ** ((-18 - lufs(x)) / 20)) if "bed" in name else x   # beds lifted to the one-shot level so they are audible
        x = np.clip(x, -0.89, 0.89)
        cues.append(f"{tpos:5.1f} s  {name}")
        out += [x, np.zeros((secs(GAP), 2))]; tpos += len(x) / SR + GAP
    y = np.concatenate(out)
    wav = os.path.join(OUT, "listening_reel.wav"); sf.write(wav, y.astype(np.float32), SR, subtype="PCM_24")
    mp3 = os.path.join(HERE, "listening_reel.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libmp3lame", "-b:a", "128k", mp3], check=True)
    open(os.path.join(HERE, "reel_cues.txt"), "w").write(
        f"Listening reel ({len(y) / SR:.1f} s, one variation of each family, {GAP} s gap between sounds; beds lifted to -18 LUFS for the reel only)\n"
        + "\n".join(cues) + "\n")
    print("reel", f"{len(y) / SR:.1f} s ->", mp3)

if __name__ == "__main__":
    only = sys.argv[1:] or None
    build(only)
    if not only or "reel" in only:
        reel()
