"""Sound for test v2: narration + channel music (swappable) ducked under the voice + engineered ship SFX (kit/ship/sfx only),
events timed to the picture/word timings. Master: -14 LUFS integrated (measured, one linear trim) + true-peak limit -1 dBTP."""
import json, os, subprocess, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
SR = 48000; DUR = 53.6
MUSIC = os.environ.get("MUSIC", os.path.join(ROOT, "assets/music/candidates/zabriskie/neptuneflux-01.m4a"))   # main theme (swap here)
MUSIC_IN = float(os.environ.get("MUSIC_IN", 0.0))     # start offset inside the track
SFX = os.path.join(ROOT, "kit/ship/sfx/out")
def load(path, sr=SR):
    a = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(a, np.float32).copy()
db = lambda d: 10 ** (d / 20)
N = int(DUR * SR); out_sfx = np.zeros(N, np.float32)
voice = load(os.path.join(HERE, "../audio/voice.wav")); voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
# events: (t, file, gain dB, optional fade-out end)
EV = [
 (0.00, "swell_bed_1", -2, 4.6), (0.30, "number_land_1", -8, None),
 (2.72, "dive_whoosh_2", -4, None), (3.46, "riser_4s_1", -3, None),
 (5.0, "swell_bed_2", -6, 7.0),
 (6.86, "charges_seq_3", 0, None), (7.46, "reveal_hit_1", -2, None), (7.50, "sink_whoomp_1", -4, None),
 (8.30, "hull_groan_1", -3, None), (10.45, "metal_creak_2", -5, None),
 (12.78, "number_land_2", -5, None), (13.80, "flood_rush_1", -3, None), (14.20, "sink_whoomp_2", -3, None),
 (15.66, "number_land_3", -7, None),
 (17.35, "underwater_bed_2", -1, 20.6), (17.75, "hull_groan_2", -5, None), (18.40, "sonar_ping_3", -9, None),
 (19.31, "number_land_1", -3, None),
 (20.55, "horn_distant_1", -6, 24.0),
 (20.40, "riser_4s_2", -4, None), (24.33, "text_slam_1", -2, None), (24.52, "reveal_hit_2", -3, None),
 (26.25, "number_land_2", -6, None), (27.57, "number_land_3", -6, None),
 (34.04, "dive_whoosh_3", -9, None), (35.96, "number_land_1", -11, None), (37.68, "number_land_2", -11, None), (39.05, "number_land_3", -11, None),
 (40.15, "strike_scrape_1", -6, None), (40.40, "strike_scrape_2", -6, None), (40.65, "reveal_hit_3", -7, None),
 (41.14, "underwater_bed_1", -2, 44.6), (41.30, "metal_creak_1", -6, None), (42.62, "sonar_ping_1", -7, None),
 (44.52, "dive_whoosh_2", -7, None), (46.10, "horn_distant_2", -7, 51.0), (46.25, "sonar_ping_2", -11, None),
 (51.32, "text_slam_2", -3, None), (51.36, "reveal_hit_1", -6, None),
]
for t, name, g, until in EV:
    a = load(os.path.join(SFX, name + ".wav")) * db(g); i = int(t * SR)
    if until: n = int((until - t) * SR); a = a[:n]; f = min(len(a), int(0.6 * SR)); a[-f:] *= np.linspace(1, 0, f)
    a = a[:max(0, N - i)]; out_sfx[i:i + len(a)] += a
# music: ducked by the voice envelope (fast attack, slow release); -24 dB under speech, -15 dB in gaps
m = load(MUSIC); m = m[int(MUSIC_IN * SR):][:N]; m = np.pad(m, (0, N - len(m)))
env = np.sqrt(np.convolve(voice ** 2, np.ones(int(0.05 * SR)) / int(0.05 * SR), "same")); env = (env > 0.01).astype(np.float32)
sm = np.zeros_like(env); a_up, a_dn = 1 - np.exp(-1 / (0.06 * SR)), 1 - np.exp(-1 / (0.45 * SR)); v = 0.0
for k in range(0, N, 48):   # control rate 1 kHz
    tgt = env[k]; v += ((a_up if tgt > v else a_dn) * 48) * (tgt - v); sm[k:k + 48] = v
mg = db(-15) + (db(-24) - db(-15)) * np.clip(sm, 0, 1)
fi, fo = int(1.2 * SR), int(2.5 * SR); mg[:fi] *= np.linspace(0, 1, fi); mg[-fo:] *= np.linspace(1, 0, fo)
mix = voice * db(-1) + m * mg * db(4) + out_sfx
fo2 = int(0.6 * SR); mix[-fo2:] *= np.linspace(1, 0, fo2)
pre = os.path.join(HERE, "../audio/premix.wav"); sf.write(pre, mix.astype(np.float32), SR, subtype="FLOAT")
# measured loudness -> one linear trim to -14 LUFS, then true-peak limiter at -1 dBTP
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", pre, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(json.loads(r[r.rindex("{"):])["input_i"]); trim = -14.0 - I
fin = os.path.join(HERE, "../audio/mix.wav")
def meas(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "loudnorm=I=-14:TP=-1:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(r[r.rindex("{"):]); return float(j["input_i"]), float(j["input_tp"])
for it in range(4):   # trim -> limit -> re-measure (the limiter eats loudness, so the trim converges in 2-3 passes)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af", f"volume={trim:.2f}dB,alimiter=limit=0.76:level=false:attack=2:release=80,aresample=48000",
                    "-c:a", "pcm_s16le", fin], check=True)
    Ii, tp = meas(fin); print(f"pass {it}: trim {trim:+.2f} dB -> I {Ii:.2f} LUFS, TP {tp:.2f} dBTP")
    if abs(Ii + 14) <= 0.3 and tp <= -1.0: break
    trim += (-14.0 - Ii)
