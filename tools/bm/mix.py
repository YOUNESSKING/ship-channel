"""Final test mix: map render + voice + ducked music + sfx -> build/ridgway-test.mp4"""
import json, os, subprocess
T = json.load(open("audio/timing.json")); dur = T["duration"]
P = {p["tag"].split("|")[0].replace("MAP:", "").strip(): p for p in T["paragraphs"]}
M = "assets/media"
cues = [("sfx_whoosh.wav", P["shot-2"]["start"] - 0.4, 0.8), ("sfx_thud.wav", P["shot-3"]["start"] + 0.9, 1.0),
        ("sfx_boom.wav", 12.0, 0.5)]
cues = [c for c in cues if os.path.exists(f"{M}/{c[0]}")]
inputs = ["-i", "scenes/test/renders/test.mp4", "-i", "audio/voice.wav"]
has_music = os.path.exists(f"{M}/music.wav")
if has_music: inputs += ["-i", f"{M}/music.wav"]
for c in cues: inputs += ["-i", f"{M}/{c[0]}"]
f, mixes, idx = [], ["[vo]"], 2
f.append("[1:a]aresample=48000,volume=1.0,asplit=2[vo][vokey]")
if has_music:
    f.append(f"[2:a]aresample=48000,atrim=0:{dur + 1},volume=0.55,afade=t=out:st={dur - 2}:d=2[mus]")
    f.append("[mus][vokey]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[musd]")
    mixes.append("[musd]"); idx = 3
else:
    f[0] = "[1:a]aresample=48000,volume=1.0[vo]"
for i, (name, t, vol) in enumerate(cues):
    f.append(f"[{idx + i}:a]aresample=48000,volume={vol},adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]"); mixes.append(f"[s{i}]")
f.append(f"{''.join(mixes)}amix=inputs={len(mixes)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
os.makedirs("build", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(f), "-map", "0:v", "-map", "[aout]",
                "-t", f"{dur:.2f}", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "build/ridgway-test.mp4"], check=True)
print("ok", dur, "music" if has_music else "no music", [c[0] for c in cues])
