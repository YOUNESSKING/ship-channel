"""Turn ONE rendered scene into a finished test clip: picture + its narration + music + that scene's SFX.

usage (from the project folder): python3 tools/make_clip.py SCENE [--small] [--from PARA --to PARA]
Reads scenes/SCENE/renders/SCENE.mp4 and scenes/SCENE/timing.js (abs_start, duration), cuts the same span
from audio/voice.wav and assets/media/music.wav, renders only this scene's sound cues, normalizes to -14 LUFS.
Writes build/clip-SCENE.mp4 (--small: 960x540 for sending in chat).
"""
import html, json, os, re, subprocess, sys, glob
import numpy as np, soundfile as sf

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
os.chdir(ROOT)
sys.path.insert(0, "tools")
name, small = sys.argv[1], "--small" in sys.argv
tjs = open(f"scenes/{name}/timing.js").read()
st = json.loads(tjs[tjs.index("=") + 1:].strip().rstrip(";"))
a0, dur = st["abs_start"], st["duration"]
off = 0.0  # optional sub-range: --from PARA --to PARA (paragraph ids inside this scene)
if "--from" in sys.argv:
    fr, to = sys.argv[sys.argv.index("--from") + 1], sys.argv[sys.argv.index("--to") + 1]
    off, end = st["paras"][fr][0], st["paras"][to][1] + 0.6
    a0, dur = a0 + off, end - off
CHROME = (glob.glob("/root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell"))[0]
dom = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files", "--virtual-time-budget=3000",
                      "--dump-dom", "file://" + os.path.abspath(f"scenes/{name}/index.html")], capture_output=True, text=True, timeout=120).stdout
m = re.search(r'<html[^>]*data-sfx="([^"]*)"', dom)
cues = [[t - off, k, name] for k, t in (json.loads(html.unescape(m.group(1))) if m else []) if off <= t <= off + dur]
os.makedirs("build", exist_ok=True)
# reuse sfx_mix with this scene's cues and a scene-length timeline
import sfx_mix_lib as M
M.render(cues, dur, f"build/clip-{name}-sfx.wav")
voice, sr = sf.read("audio/voice_owner.wav" if os.path.exists("audio/voice_owner.wav") else "audio/voice.wav", dtype="float32")
seg = voice[int(a0 * sr):int((a0 + dur) * sr)]
sf.write(f"build/clip-{name}-voice.wav", seg, sr)
inputs = ["-ss", f"{off:.2f}", "-i", f"scenes/{name}/renders/{name}.mp4", "-i", f"build/clip-{name}-voice.wav", "-i", f"build/clip-{name}-sfx.wav"]
f = ["[1:a]aresample=48000,asplit=3[vo][key][key2]", "[2:a]aresample=48000[sx]", "[sx][key2]sidechaincompress=threshold=0.03:ratio=3:attack=10:release=300[sfx]"]
if os.path.exists("assets/media/music.wav"):
    inputs += ["-ss", f"{a0:.2f}", "-t", f"{dur:.2f}", "-i", "assets/media/music.wav"]
    f += ["[3:a]aresample=48000,volume=0.08,afade=t=in:d=1.5[mus]", "[mus][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[musd]",
          "[vo][musd][sfx]amix=inputs=3:normalize=0,alimiter=limit=0.5:level=false,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"]
else:
    f += ["[key]anullsink", "[vo][sfx]amix=inputs=2:normalize=0,alimiter=limit=0.5:level=false,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"]
vf = ["-vf", "scale=960:540", "-c:v", "libx264", "-preset", "slow", "-crf", "26"] if small else ["-c:v", "libx264", "-crf", "18", "-preset", "medium"]
out = f"build/clip-{name}{'-small' if small else ''}.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(f), "-map", "0:v", "-map", "[aout]", "-t", f"{dur:.2f}",
                *vf, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
print("wrote", out, f"{dur:.1f}s", len(cues), "cues")
