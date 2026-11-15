"""Usable film windows for the full video. For every vetted clip in footage/cut_clips.sh, re-read the SAME continuous
shot from the NARA reel (+-10 s around the clip, stopping at the first cut / flash / blob on either side), so a shot can
run longer or start elsewhere without ever crossing into an unvetted shot. Out: build/film_windows.json
{clip: {"reel": id, "clip_in": s, "windows": [[reel_t0, reel_t1], ...]}} (reel seconds, clean, >= 1.2 s)."""
import json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
FT = os.path.join(ROOT, "videos/oriskany/footage"); sys.path.insert(0, os.path.join(ROOT, "tools/film"))
import numpy as np
import check_clips as C
cuts = re.findall(r"^cut (\d+)\s+(\d+(?:\.\d+)?) (\d+) (\S+)", open(os.path.join(FT, "cut_clips.sh")).read(), re.M)
PAD = 10.0; out = {}
for reel, t_in, dur, name in cuts:
    t_in = float(t_in); dur = float(dur); a = max(0.0, t_in - PAD); b = t_in + dur + PAD
    src = os.path.join(FT, f"src/film/nara_{reel}.mp4")
    pre = "crop=1440:1080:240:0," if reel == "39085" else ""
    tmp = os.path.join(tempfile.gettempdir(), f"fw_{name}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-i", src, "-t", str(b - a), "-vf",
                    pre + "scale='iw*sar':'ih',setsar=1,scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2:black,fps=30",
                    "-an", "-c:v", "libx264", "-crf", "28", tmp], check=True)
    fr, fps = C.frames(tmp); lum = fr.mean(axis=3); n = len(fr)
    bad = np.zeros(n, bool)
    # cuts / dissolves: scene score from ffmpeg
    sc = subprocess.run(["ffmpeg", "-v", "error", "-i", tmp, "-vf", "select='gt(scene,0.28)',metadata=print:file=-", "-f", "null", "-"], capture_output=True, text=True).stdout
    for m in re.finditer(r"pts_time:([\d.]+)", sc):
        i = int(float(m.group(1)) * fps); bad[max(0, i - 3): i + 4] = True
    # flashes
    ml = lum.mean(axis=(1, 2))
    for i in range(1, n - 1):
        if (ml[i] - ml[i - 1] > 0.22 and ml[i] - ml[i + 1] > 0.22) or (lum[i] > 0.92).mean() > 0.4: bad[max(0, i - 3): i + 4] = True
    # dark blobs (ignore pillar bars)
    bm = C.bars_mask(lum)
    for i in range(n):
        d = (lum[i] < 0.06) & ~bm
        lab, k = C.ndimage.label(d)
        if k and np.bincount(lab.ravel())[1:].max() > 0.25 * (~bm).sum(): bad[i] = True
    os.remove(tmp)
    # the continuous run that contains the vetted clip's centre
    centre = int((t_in + dur / 2 - a) * fps)
    win = []; i = 0
    while i < n:
        if bad[i]: i += 1; continue
        j = i
        while j < n and not bad[j]: j += 1
        if (j - i) / fps >= 1.2: win.append([round(a + i / fps, 2), round(a + j / fps, 2)])
        i = j
    # keep only windows that overlap the vetted clip span (same shot as vetted); others are unvetted shots
    win = [w for w in win if w[1] > t_in + 0.1 and w[0] < t_in + dur - 0.1]
    out[name] = {"reel": reel, "clip_in": t_in, "clip_dur": dur, "windows": win,
                 "longest": round(max([w[1] - w[0] for w in win] or [0]), 2)}
    print(f"{name:34s} reel {reel} in {t_in:6.1f}  windows {win}", flush=True)
json.dump(out, open(os.path.join(HERE, "film_windows.json"), "w"), indent=1)
print("total clean film s:", round(sum(sum(w[1] - w[0] for w in v["windows"]) for v in out.values()), 1))
