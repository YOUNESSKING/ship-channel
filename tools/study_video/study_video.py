#!/usr/bin/env python3
"""Study a competitor video: download (study only, never reuse), transcript, frames, sound design map.

Usage (on the owner's own computer; YouTube blocks cloud machines):
    python3 tools/study_video/study_video.py URL [URL ...] [--minutes 3] [--stems]

Output per video in research/video_study/<id>/ :
    info.json, video.mp4 (git-ignored), audio.wav (git-ignored)
    transcript.txt / transcript.srt   (YouTube captions if any, else local Whisper, free)
    frames/ 1 frame per second for the first N minutes + every scene cut, contact_*.jpg sheets
    sound/loudness.csv   short-term loudness every 0.1 s (LUFS)
    sound/events.csv     hits (sudden loud onsets), silences / music drops, risers (rising loudness ramps)
    sound/sound_map.png  loudness curve with cuts, hits, silences, risers and the spoken words
    sound/stems/         voice / music / sfx-ish split (only with --stems, needs demucs)
    REPORT.md            numbers to paste into the study (cuts per minute, hits per minute, silences, LUFS)
Free: yt-dlp, ffmpeg, faster-whisper, numpy, matplotlib. No paid API.
"""
import argparse, csv, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "video_study"


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run(cmd, check=True, text=True, **kw)


def download(url, d):
    d.mkdir(parents=True, exist_ok=True)
    run(["yt-dlp", "-f", "bv*[height<=1080]+ba/b[height<=1080]", "--merge-output-format", "mp4",
         "-o", str(d / "video.%(ext)s"), "--write-info-json", "--write-subs", "--write-auto-subs",
         "--sub-langs", "en.*,en", "--sub-format", "vtt", "--convert-subs", "srt", url])
    info = next(d.glob("video.info.json"))
    info.rename(d / "info.json")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(d / "video.mp4"), "-ac", "1", "-ar", "16000", str(d / "audio.wav")])


def transcript(d):
    srt = sorted(d.glob("video*.en*.srt"))
    if srt:
        srt[0].rename(d / "transcript.srt")
        text = re.sub(r"\d+\n[\d:,]+ --> [\d:,]+\n", "", (d / "transcript.srt").read_text())
        lines = []
        for l in text.splitlines():
            l = re.sub(r"<[^>]+>", "", l).strip()
            if l and (not lines or lines[-1] != l):
                lines.append(l)
        (d / "transcript.txt").write_text(" ".join(lines))
        return "YouTube captions"
    from faster_whisper import WhisperModel
    model = WhisperModel("small.en", compute_type="int8")
    import numpy as np  # decode with ffmpeg ourselves (avoids PyAV version issues)
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(d / "audio.wav"), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    segs, _ = model.transcribe(np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768, word_timestamps=False)
    def ts(t):
        h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
        return f"{h:02}:{m:02}:{s:06.3f}".replace(".", ",")
    srt, txt = [], []
    for i, s in enumerate(segs, 1):
        srt.append(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n")
        txt.append(s.text.strip())
    (d / "transcript.srt").write_text("\n".join(srt))
    (d / "transcript.txt").write_text(" ".join(txt))
    return "local Whisper small.en"


def srt_lines(d):
    out = []
    p = d / "transcript.srt"
    if not p.exists():
        return out
    for b in p.read_text().split("\n\n"):
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+) -->", b)
        if m:
            t = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) + int(m[4]) / 1000
            out.append((t, re.sub(r"<[^>]+>", "", b.split("\n")[-1]).strip()))
    return out


def frames(d, minutes):
    f = d / "frames"
    f.mkdir(exist_ok=True)
    secs = minutes * 60
    run(["ffmpeg", "-y", "-loglevel", "error", "-t", str(secs), "-i", str(d / "video.mp4"),
         "-vf", "fps=1,scale=640:-2", str(f / "s%04d.jpg")])
    # scene cuts over the whole video, with timestamps
    r = subprocess.run(["ffmpeg", "-i", str(d / "video.mp4"), "-vf", "select='gt(scene,0.3)',showinfo,scale=320:-2",
                        "-vsync", "vfr", str(f / "cut%04d.jpg")], capture_output=True, text=True)
    cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]
    (f / "cuts.txt").write_text("\n".join(f"{c:.2f}" for c in cuts))
    for i in range(0, secs, 60):
        run(["ffmpeg", "-y", "-loglevel", "error", "-start_number", str(i + 1), "-i", str(f / "s%04d.jpg"),
             "-frames:v", "1", "-vf", "tile=10x6", str(f / f"contact_{i // 60:02}min.jpg")])
    return cuts


def sound(d, minutes, stems):
    import numpy as np
    s = d / "sound"
    s.mkdir(exist_ok=True)
    # short-term loudness every 0.1 s
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(d / "video.mp4"), "-af", "ebur128=metadata=1,ametadata=print:key=lavfi.r128.S",
                        "-f", "null", "-"], capture_output=True, text=True)
    t, lufs = [], []
    cur = None
    for line in r.stderr.splitlines():
        m = re.search(r"pts_time:([\d.]+)", line)
        if m:
            cur = float(m[1])
        m = re.search(r"lavfi.r128.S=(-?[\d.inf]+)", line)
        if m and cur is not None:
            v = float(m[1]) if "inf" not in m[1] else -70.0
            t.append(cur); lufs.append(max(v, -70.0))
    integ = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    t, lufs = np.array(t), np.array(lufs)
    with open(s / "loudness.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["t", "lufs_short"]); w.writerows(zip(t.round(2), lufs.round(2)))
    # hits: sharp onsets in raw energy (20 ms frames)
    # hits = deep impacts/booms: only the band under 150 Hz, where the voice has almost no energy
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(d / "audio.wav"), "-af", "lowpass=f=150,lowpass=f=150",
                          "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    full = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(d / "audio.wav"), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                          capture_output=True).stdout
    b = np.frombuffer(full, dtype=np.int16).astype(np.float32) / 32768
    hop = 320
    n = min(len(a), len(b)) // hop
    db = lambda x: 10 * np.log10(np.maximum((x[: n * hop].reshape(n, hop) ** 2).mean(1), 1e-10))
    e, ef = db(a), db(b)
    bassy = e - ef > -4  # most of the energy is bass: a boom, not a voice
    et = np.arange(n) * hop / 16000
    base = np.convolve(e, np.ones(50) / 50, mode="same")  # 1 s moving average
    top = np.percentile(e, 99)  # a hit must reach near the loudest bass in the video
    events, last = [], -9
    for i in range(1, n):
        if e[i] - base[i] > 12 and e[i] - e[i - 1] > 6 and e[i] > top - 15 and bassy[i] and et[i] - last > 0.5:
            events.append((round(et[i], 2), "hit", round(float(e[i] - base[i]), 1))); last = et[i]
    # silences / music drops
    r = subprocess.run(["ffmpeg", "-i", str(d / "audio.wav"), "-af", "silencedetect=n=-45dB:d=0.3", "-f", "null", "-"],
                       capture_output=True, text=True)
    st = re.findall(r"silence_start: ([\d.]+)", r.stderr); du = re.findall(r"silence_duration: ([\d.]+)", r.stderr)
    for a0, dd in zip(st, du):
        events.append((round(float(a0), 2), "silence", round(float(dd), 2)))
    # risers: loudness climbing >= 8 LU over 1-4 s
    for i in range(len(t)):
        for j in range(i + 10, min(i + 40, len(t))):
            if lufs[j] - lufs[i] >= 8 and np.all(np.diff(lufs[i:j + 1]) > -0.8):
                events.append((round(float(t[i]), 2), "riser", round(float(t[j] - t[i]), 1))); break
    events.sort()
    ded, lastr = [], -9
    for ev in events:
        if ev[1] == "riser":
            if ev[0] - lastr < 3: continue
            lastr = ev[0]
        ded.append(ev)
    with open(s / "events.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["t", "type", "value (hit dB over 1s avg / silence s / riser s)"]); w.writerows(ded)
    if stems:
        run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-o", str(s / "stems"), str(d / "audio.wav")])
    return t, lufs, ded, (float(integ[-1]) if integ else None)


def plot(d, minutes, t, lufs, events, cuts, lines):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    end = minutes * 60
    rows = max(1, minutes)
    fig, axs = plt.subplots(rows, 1, figsize=(20, 3.2 * rows), squeeze=False)
    for r in range(rows):
        ax = axs[r][0]; a0, a1 = r * 60, (r + 1) * 60
        m = (t >= a0) & (t < a1)
        ax.plot(t[m], lufs[m], color="black", lw=1)
        for c in cuts:
            if a0 <= c < a1: ax.axvline(c, color="0.75", lw=0.8)
        for ev in events:
            if not a0 <= ev[0] < a1: continue
            if ev[1] == "hit": ax.axvline(ev[0], color="red", lw=1.4)
            elif ev[1] == "silence": ax.axvspan(ev[0], ev[0] + ev[2], color="blue", alpha=0.2)
            elif ev[1] == "riser": ax.axvspan(ev[0], ev[0] + ev[2], color="orange", alpha=0.3)
        for lt, txt in lines:
            if a0 <= lt < a1: ax.text(lt, -12, txt[:38], fontsize=6, rotation=90, va="top")
        ax.set_xlim(a0, a1); ax.set_ylim(-60, -5); ax.set_ylabel("LUFS (S)")
    axs[0][0].set_title(f"{d.name}: loudness. grey=cut, red=hit, blue=silence/drop, orange=riser, text=voice")
    fig.tight_layout(); fig.savefig(d / "sound" / "sound_map.png", dpi=90)


def report(d, src, cuts, events, integ, minutes):
    info = json.loads((d / "info.json").read_text())
    dur = info.get("duration") or 1
    hits = [e for e in events if e[1] == "hit"]; sil = [e for e in events if e[1] == "silence"]; ris = [e for e in events if e[1] == "riser"]
    first = lambda xs, a, b: sum(1 for x in xs if a <= (x if isinstance(x, float) else x[0]) < b)
    words = len((d / "transcript.txt").read_text().split()) if (d / "transcript.txt").exists() else 0
    md = f"""# {info.get('title')} ({info.get('id')})
Channel {info.get('channel')} | uploaded {info.get('upload_date')} | {dur // 60}:{dur % 60:02} | views {info.get('view_count')} | likes {info.get('like_count')} | comments {info.get('comment_count')}
Transcript: {src}, {words} words, {words / (dur / 60):.0f} words/min.

| | whole video | first 30 s | first {minutes} min |
|---|---|---|---|
| scene cuts | {len(cuts)} ({len(cuts) / (dur / 60):.1f}/min) | {first(cuts, 0, 30)} | {first(cuts, 0, minutes * 60)} |
| hits | {len(hits)} ({len(hits) / (dur / 60):.1f}/min) | {first(hits, 0, 30)} | {first(hits, 0, minutes * 60)} |
| silences / drops (>=0.3 s) | {len(sil)} | {first(sil, 0, 30)} | {first(sil, 0, minutes * 60)} |
| risers | {len(ris)} | {first(ris, 0, 30)} | {first(ris, 0, minutes * 60)} |

Integrated loudness: {integ} LUFS (ours: -14).
Look at: sound/sound_map.png (loudness + cuts + hits + words), frames/contact_*.jpg, sound/events.csv.
Detection is automatic: check the hits and risers by ear before quoting them.
"""
    (d / "REPORT.md").write_text(md)
    print(md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--minutes", type=int, default=3, help="minutes of 1 fps frames and sound map (default 3)")
    ap.add_argument("--stems", action="store_true", help="split voice vs music+sfx with demucs (slow, pip install demucs)")
    a = ap.parse_args()
    for url in a.urls:
        vid = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url)
        d = OUT / (vid[1] if vid else re.sub(r"\W", "_", url)[-20:])
        if not (d / "video.mp4").exists():
            download(url, d)
        src = transcript(d) if not (d / "transcript.txt").exists() else "existing"
        cuts = frames(d, a.minutes)
        t, lufs, events, integ = sound(d, a.minutes, a.stems)
        plot(d, a.minutes, t, lufs, events, cuts, srt_lines(d))
        report(d, src, cuts, events, integ, a.minutes)


if __name__ == "__main__":
    main()
