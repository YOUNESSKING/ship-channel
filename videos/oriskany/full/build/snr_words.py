"""SFX_FIX_v6 measurements on the REAL mix buses (critic S7: the isolated per-cue renders skip the bus EQ).

1. Speech-band SNR per word: voice_bus over the effects buses (sfx_bus + punch_bus + beds_bus), both band-passed 1-4 kHz
   (4th-order Butterworth), RMS over each word. Below ~+3 dB a word is at risk of being masked.
2. --env MASTER.mp4 T0 T1: 30 ms RMS envelope (dBFS) of the master's audio in [T0, T1] (the hook-blast window).
usage: python3 build/snr_words.py OUT.json [--env MASTER.mp4 17.5 18.6]"""
import json, os, subprocess, sys, tempfile
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); MIX = os.environ.get("MIX_WORK", os.path.join(FULL, "audio", "mix"))
WORDS = json.load(open(os.path.join(HERE, "words.json"))); WORDS = WORDS["words"] if isinstance(WORDS, dict) else WORDS
REGIONS = {  # name: (t0, t1)  critic CRITIQUE_SFX_v5 M2, M3, S1-S4
    "M2 hook 'she was gone.' (impact@19.85 + flood@19.90)": (19.80, 20.40),
    "S1 groan@26.25 'millions to put'": (26.20, 27.80),
    "S2 thump@28.70 'sea floor?'": (28.60, 29.60),
    "S4 whoosh@45.80 'About thirteen nautical miles'": (45.80, 47.30),
    "M3 jet@232.11": (232.10, 233.60),
    "M3 jet@235.89": (235.85, 237.40),
    "M3 jet@325.94": (325.90, 327.50),
    "S3 flood@537.69 'Then she was gone.'": (537.60, 539.10),
}
SOS = butter(4, [1000, 4000], btype="band", fs=48000, output="sos")


def rd(name, t0, t1):
    with sf.SoundFile(os.path.join(MIX, name)) as f:
        f.seek(int(t0 * f.samplerate)); return f.read(int((t1 - t0) * f.samplerate), dtype="float64", always_2d=True).mean(axis=1)


def snr():
    out = {}
    for name, (t0, t1) in REGIONS.items():
        a, b = t0 - 0.5, t1 + 0.5          # filter warm-up margin
        v = sosfilt(SOS, rd("voice_bus.wav", a, b))
        fx = sosfilt(SOS, sum(rd(n, a, b) for n in ("sfx_bus.wav", "punch_bus.wav", "beds_bus.wav")))
        rows = []
        for w in WORDS:
            if w["start"] >= t0 and w["start"] < t1:
                i0, i1 = int((w["start"] - a) * 48000), int((min(w["end"], b) - a) * 48000)
                if i1 - i0 < 480: continue
                r = lambda x: np.sqrt((x[i0:i1] ** 2).mean()) + 1e-12
                rows.append({"w": w["w"], "t": round(w["start"], 2), "snr_1_4k": round(20 * np.log10(r(v) / r(fx)), 1)})
        out[name] = {"words": rows, "min": min(r["snr_1_4k"] for r in rows) if rows else None}
    return out


def env(mp4, t0, t1):
    tmp = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0 - 0.1), "-i", mp4, "-t", str(t1 - t0 + 0.2), "-vn", "-ac", "1", "-c:a", "pcm_f32le", tmp], check=True)
    a, sr = sf.read(tmp); os.remove(tmp)
    rows = []
    for t in np.arange(t0, t1 + 1e-6, 0.03):
        i = int((t - t0 + 0.1) * sr); seg = a[i: i + int(0.03 * sr)]
        rows.append([round(float(t), 2), round(20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-12), 1)])
    return rows


if __name__ == "__main__":
    res = {"snr": snr()}
    if "--env" in sys.argv:
        i = sys.argv.index("--env"); res["env"] = env(sys.argv[i + 1], float(sys.argv[i + 2]), float(sys.argv[i + 3]))
    json.dump(res, open(sys.argv[1], "w"), indent=1)
    for k, v in res["snr"].items():
        print(f"{k:55s} min {v['min']:+6.1f} | " + " ".join(f"{r['w']}:{r['snr_1_4k']:+.1f}" for r in v["words"]))
    if "env" in res: print("env", " ".join(f"{t:.2f}:{d}" for t, d in res["env"]))
