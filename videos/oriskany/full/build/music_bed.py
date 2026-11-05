"""Music bed for the full video, v2 (critic B S1, S2, S3, N1). Chris Zabriskie, Music from Neptune Flux (CC BY 4.0):
  main    "Stories About the World That Once Was" (neptuneflux-01, 6:55)  0 s -> c06 start, folding back into itself at the
          c03/c04 chapter cut (360 s: "Then, in two thousand three, Congress changed the rules"), BEFORE the track's own outro
          (which starts ~368 s and left a music hole at 384-400 s in v1: S2)
  tension "Your Mother's Daughter" (neptuneflux-03, 3:34)                c06 (the fish test) -> last 60 s
  outro   "I Should Have Been More Human" (neptuneflux-09, 3:44)          last 60 s of narration + 18 s end screen
v2 changes (mix_clip.py still plays the bed at the LOCKED MUSIC_VOL 0.08 + MUSIC_TRIM_DB -6, ducked under the voice):
  S1  each piece is set to the same integrated loudness (TARGET, linear gain per piece) BEFORE the 5 s crossfades; v1 ran one
      dynamic loudnorm over the whole bed, which left "Your Mother's Daughter" ~3 dB under the main theme.
      TARGET is chosen so the whole-video music under voice stays at or under v1's -24.1 dB (owner: no louder music).
  S3  a -12 dB dip 538.46-540.6 s so "Then she was gone" lands in (near) silence.
  N1  end screen (after the last word, 866.8 s): +8 dB so it does not sound dead (fade-out kept).
  Hook (0-48.6 s, owner-approved): the v1 bed samples are kept verbatim up to 48.0 s (audio/music_bed_v1.wav, saved on the
      first run), with a 2 s gain crossfade into the v2 bed (same source, same alignment).
Writes audio/music_bed.wav (float) + build/music_bed.json."""
import json, os, shutil, subprocess, numpy as np, soundfile as sf, pyloudnorm as pyln
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
Z = os.path.join(ROOT, "assets/music/candidates/zabriskie")
CH = {c["key"]: c for c in json.load(open(os.path.join(FULL, "chapters.json")))["chapters"]}
SR = 48000
TOTAL = round(CH["c07"]["end"] + 18.0, 3)
XF = 5.0
TARGET = float(os.environ.get("MUSIC_TARGET_LUFS", "-20.5"))
SW_TENSION = CH["c06"]["start"]
SW_OUTRO = 806.312   # v2 value (= last 60 s of the v2 narration); v3 keeps the outro entering on the same words, "So that is why..." + 4 s
SW_LOOP = 360.0
DIP = (538.46, 540.6, -12.0)
END_LIFT = (CH["c07"]["voice_end"] + 0.9, 8.0)        # 866.8 s (after "comments." + 1 s)
HOOK_KEEP = CH["c02"]["start"] - 0.6                    # 48.0 s
P = [("neptuneflux-01.m4a", "Stories About the World That Once Was", 0.0, 0.0),
     ("neptuneflux-01.m4a", "Stories About the World That Once Was", 90.0, SW_LOOP),
     ("neptuneflux-03.m4a", "Your Mother's Daughter", 0.0, SW_TENSION),
     ("neptuneflux-03.m4a", "Your Mother's Daughter", 25.0, SW_TENSION + 200.0),
     ("neptuneflux-09.m4a", "I Should Have Been More Human", 0.0, SW_OUTRO)]
LEN = {"neptuneflux-01.m4a": 414.6, "neptuneflux-03.m4a": 214.0, "neptuneflux-09.m4a": 223.5}


def dec(path, ss, dur):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", path, "-t", f"{dur:.3f}", "-ac", "2", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


meter = pyln.Meter(SR)
n = int(round(TOTAL * SR)); bed = np.zeros((n, 2), np.float32); plan = []
bounds = [p[3] for p in P] + [TOTAL]
for i, (tr, title, ss, sw) in enumerate(P):
    a = 0.0 if i == 0 else sw - XF / 2
    b = TOTAL if i == len(P) - 1 else bounds[i + 1] + XF / 2
    x = dec(os.path.join(Z, tr), ss, b - a)
    L0 = meter.integrated_loudness(x); g = 10 ** ((TARGET - L0) / 20); x = x * g
    m = len(x); env = np.ones(m, np.float32); f = int(XF * SR)
    if i > 0: env[:f] = np.linspace(0, 1, f)
    if i < len(P) - 1: env[-f:] = np.minimum(env[-f:], np.linspace(1, 0, f))
    i0 = int(round(a * SR)); m = min(m, n - i0)
    bed[i0:i0 + m] += x[:m] * env[:m, None]
    plan.append(dict(track=tr, title=title, src_start=ss, plays_from=round(a, 3), plays_to=round(b, 3), src_end=round(ss + b - a, 2),
                     loudness_before=round(L0, 2), gain_db=round(TARGET - L0, 2)))
    assert ss + b - a <= LEN[tr] + 0.05, plan[-1]
# automation: S3 dip, N1 end-screen lift, final 3 s fade
t = np.arange(n) / SR
gdb = np.zeros(n, np.float32)
a, b, d = DIP; r = 0.25
gdb += d * np.clip(np.minimum((t - (a - r)) / r, ((b + r) - t) / r), 0, 1)
t0, up = END_LIFT; gdb += up * np.clip((t - t0) / 1.0, 0, 1)
bed *= (10 ** (gdb / 20))[:, None]
bed *= np.clip((TOTAL - t) / 3.0, 0, 1)[:, None].astype(np.float32)
# hook: v1 samples verbatim to 48.0 s, 2 s crossfade into the v2 bed
V1 = os.path.join(FULL, "audio/music_bed_v1.wav")
if not os.path.exists(V1) and os.path.exists(os.path.join(FULL, "audio/music_bed.wav")):
    shutil.copy2(os.path.join(FULL, "audio/music_bed.wav"), V1)
v1, sr1 = sf.read(V1, dtype="float32", frames=int((HOOK_KEEP + 2.0) * SR)); assert sr1 == SR
k0, k1 = int(HOOK_KEEP * SR), int((HOOK_KEEP + 2.0) * SR)
w = np.clip((t[:k1] - HOOK_KEEP) / 2.0, 0, 1)[:, None].astype(np.float32)
bed[:k1] = v1[:k1] * (1 - w) + bed[:k1] * w
out = os.path.join(FULL, "audio", "music_bed.wav")
sf.write(out, bed, SR, subtype="FLOAT")
peak = 20 * np.log10(np.abs(bed).max() + 1e-9)
lv = lambda x, y: round(meter.integrated_loudness(bed[int(x * SR):int(y * SR)]), 2)
rep = {"total": TOTAL, "crossfade_s": XF, "target_lufs": TARGET, "dip": DIP, "end_lift": END_LIFT, "hook_v1_until": HOOK_KEEP,
       "pieces": plan, "peak_dbfs": round(float(peak), 2),
       "loudness": {"0-48.6 hook": lv(0, 48.6), "0-360": lv(0, 360), "360-566": lv(360, 566), "566-806": lv(566, 806), "806-866": lv(806, 866.8),
                    "end screen": lv(866.8, TOTAL - 3)}}
json.dump(rep, open(os.path.join(HERE, "music_bed.json"), "w"), indent=1)
print(json.dumps(rep, indent=1))
