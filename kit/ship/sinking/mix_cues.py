"""Mix the sound cues a ShipSink page exported (OUT.cues.json from tools/render_frames.js) with the in-house kit sounds
(kit/ship/sfx/out/*.wav; run sfx/make_sfx.py first) and mux them onto the silent render. Preview mix only (-16 LUFS);
real videos go through the channel mixer (templates/mix_audio.py + mux.sh, -14 LUFS).
python3 kit/ship/sinking/mix_cues.py out/sinking_preview_noaudio.mp4 out/sinking_preview.mp4"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "sfx"))
from make_sfx import SR, lufs, fade, secs   # noqa: E402
SFX = os.path.join(HERE, "..", "sfx", "out")
GAIN = {"swell_bed": 0.9, "underwater_bed": 1.0, "charges_seq": 0.9, "hull_groan": 0.8, "sink_whoomp": 1.0, "metal_creak": 0.7, "sonar_ping": 0.8, "number_land": 1.0}
src, dst = sys.argv[1], sys.argv[2]
info = json.load(open(src.replace(".mp4", ".cues.json")))
D = info["duration"]; mix = np.zeros((secs(D + 0.05), 2))
for c in info["cues"]:
    x, sr = sf.read(os.path.join(SFX, c["kind"] + ".wav")); assert sr == SR
    if c.get("bed"):
        x = fade(x[: secs(c["until"] - c["t"] + 0.6)], 0.6, 0.6)
    g = c.get("gain", 1.0) * GAIN.get(c["kind"].rsplit("_", 1)[0], 1.0)
    i = secs(c["t"]); j = min(len(mix), i + len(x)); mix[i:j] += x[: j - i] * g
mix *= 10 ** ((-16 - lufs(mix)) / 20); mix = np.tanh(mix / 0.9) * 0.9
wav = dst.replace(".mp4", ".wav"); sf.write(wav, mix.astype(np.float32), SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", dst], check=True)
print("wrote", dst, f"({lufs(mix):.1f} LUFS)")
