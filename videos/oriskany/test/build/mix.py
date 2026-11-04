"""Voice + music bed + SFX, ducked mix, -14 LUFS with a measured trim + limiter; muxed onto the render."""
import json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "../src"); R = os.path.join(HERE, "../renders")
C = {c["id"]: c["start"] for c in json.load(open(os.path.join(HERE, "timing.json")))["chunks"]}
DUR = json.load(open(os.path.join(HERE, "timing.json")))["duration"] + 0.4
SFX = [("zoom_whoosh", 0.25, -14), ("whoosh", C["c02"] - 0.15, -12), ("hit", C["c08"], -8), ("hit", C["c09"], -14),
       ("explosion_near_1", C["c10"] + 1.7, -6), ("whoosh", C["c12"] - 0.1, -10), ("hit", C["c14"], -14),
       ("hit", C["c18"] + 1.6, -12), ("whoosh", C["c20"], -14), ("hit", C["c21"], -12)]
ins = ["-i", f"{R}/../audio/voice.wav", "-i", f"{SRC}/music_src_long-note-one.mp3"]
for n, _, _ in SFX: ins += ["-i", f"{SRC}/{n}.wav"]
fc = [f"[0:a]aresample=48000,apad,atrim=0:{DUR}[v]",
      f"[1:a]aresample=48000,atrim=0:{DUR},volume=-21dB,afade=t=in:d=1.5,afade=t=out:st={DUR-1.5}:d=1.5[m]"]
for i, (n, t, g) in enumerate(SFX):
    fc.append(f"[{i+2}:a]aresample=48000,volume={g}dB,adelay={int(t*1000)}|{int(t*1000)}[s{i}]")
fc.append("[m][v]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md]")  # duck music under voice
fc.append("[v]asplit[v1][v2]")
fc[-2] = "[m][v2]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md]"
fc.append("[v1][md]" + "".join(f"[s{i}]" for i in range(len(SFX))) + f"amix=inputs={len(SFX)+2}:normalize=0:duration=first[mix]")
graph = ";".join([fc[0], fc[1]] + fc[2:2+len(SFX)] + [fc[-1], fc[-2], fc[-3] if False else fc[-1]])
graph = ";".join([fc[0], fc[1]] + fc[2:2+len(SFX)] + ["[v]asplit[v1][v2]", "[m][v2]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md]",
                  "[v1][md]" + "".join(f"[s{i}]" for i in range(len(SFX))) + f"amix=inputs={len(SFX)+2}:normalize=0:duration=first[mix]"])
pre = f"{R}/mix_pre.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", graph, "-map", "[mix]", "-ac", "2", pre], check=True)
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", pre, "-af", "loudnorm=I=-14:TP=-1:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.search(r'"input_i" : "([-\d.]+)"', m).group(1)); gain = -14.0 - I
print(f"measured {I:.2f} LUFS -> gain {gain:+.2f} dB")
fin = f"{R}/mix_final.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af", f"volume={gain}dB,alimiter=limit=0.89:level=false", fin], check=True)
m2 = subprocess.run(["ffmpeg", "-hide_banner", "-i", fin, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print("final:", re.findall(r"I:\s+([-\d.]+) LUFS", m2)[-1], "LUFS; true peak", re.findall(r"Peak:\s+([-\d.]+) dBFS", m2)[-1])
out = os.path.join(HERE, "../oriskany_test_1min.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/video_noaudio.mp4", "-i", fin, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
print("wrote", out)
