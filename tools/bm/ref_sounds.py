"""Synthesised 'Frontlines' sound-design set (the Mixkit wavs of frontlines-1m are not in git): whoosh, label pop, boom, reverse riser,
newspaper page, projector loop. Original (generated), no licence needed. Run from grant/: python3 tools/ref_sounds.py"""
import numpy as np, soundfile as sf
from scipy import signal
SR = 48000; rng = np.random.default_rng(11)
OUT = "assets/media/sfx_ref/"
def bp(x, lo, hi): b, a = signal.butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return signal.lfilter(b, a, x)
def lp(x, f): b, a = signal.butter(2, f / (SR / 2)); return signal.lfilter(b, a, x)
def norm(x, peak=0.8): return x / (np.abs(x).max() + 1e-9) * peak
def save(n, x): x = np.stack([x, np.roll(x, 40)], 1); sf.write(OUT + n, x.astype(np.float32), SR)
t = lambda d: np.arange(int(d * SR)) / SR
# whoosh: noise whose band sweeps up, bell envelope, 1.6 s
d = 1.6; x = rng.standard_normal(int(d * SR)); tt = t(d); env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 2
y = np.zeros_like(x)
for i, (lo, hi) in enumerate([(300, 900), (700, 2200), (1500, 5000)]): y += bp(x, lo, hi) * np.clip(np.sin(np.pi * np.clip((tt / d - i * 0.18) / 0.6, 0, 1)), 0, 1)
save("whoosh_cinematic_tunnel.wav", norm(y * env, 0.7))
# pop: short sine blip with a click
d = 0.18; tt = t(d); y = np.sin(2 * np.pi * (700 + 500 * np.exp(-tt * 60)) * tt) * np.exp(-tt * 28); save("label_pop_dry.wav", norm(y, 0.7))
# boom: low sine drop + noise tail, 2.2 s
d = 2.2; tt = t(d); y = np.sin(2 * np.pi * (55 + 90 * np.exp(-tt * 9)) * tt) * np.exp(-tt * 2.2) + lp(rng.standard_normal(len(tt)), 220) * np.exp(-tt * 3) * 0.5
save("boom_big_cinematic_impact.wav", norm(y, 0.9))
# reverse riser: filtered noise swell, 2.5 s
d = 2.5; tt = t(d); x = bp(rng.standard_normal(len(tt)), 400, 6000) * (tt / d) ** 2.2; x *= np.sin(2 * np.pi * (80 + 200 * tt / d) * tt) * 0.3 + 0.7; save("riser_reverse_swell.wav", norm(x, 0.7))
# newspaper page: rustle bursts, 1.4 s
d = 1.4; tt = t(d); x = bp(rng.standard_normal(len(tt)), 1800, 9000)
env = np.zeros(len(tt))
for c, w in [(0.05, 0.12), (0.22, 0.2), (0.5, 0.25), (0.8, 0.15)]: env += np.exp(-((tt - c) / w) ** 2)
save("paper_newspaper_big_page.wav", norm(x * np.clip(env, 0, 1) * (0.6 + 0.4 * rng.random(len(tt))), 0.6))
# projector loop: 24 Hz soft flutter + motor hum, 2.0 s seamless (integer cycles)
d = 2.0; tt = t(d); hum = np.sin(2 * np.pi * 48 * tt) * 0.15 + np.sin(2 * np.pi * 96 * tt) * 0.06
fl = (np.sin(2 * np.pi * 24 * tt) > 0.97).astype(float); fl = lp(fl, 600) * 3; gr = bp(rng.standard_normal(len(tt)), 3000, 8000) * (0.25 + 0.75 * (np.sin(2 * np.pi * 24 * tt) > 0.9)) * 0.3
save("projector_loop.wav", norm(hum + fl + gr, 0.6))
print("ref sounds written")
