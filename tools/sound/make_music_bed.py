"""Music bed (port of battle-maps tools/make_music_bed.py): fit the track(s) to the video length, 5 s crossfades,
loudnorm to -20 LUFS, 3 s fade-out. mix_clip.py then plays it at MUSIC_VOL 0.08, ducked under the voice.
usage: python3 make_music_bed.py OUT.wav TOTAL_SECONDS TRACK1 [START1] [TRACK2 START2 ...]  (start = seconds into the track)"""
import subprocess, sys
out, total = sys.argv[1], float(sys.argv[2]); a = sys.argv[3:]
tracks = [(a[i], float(a[i + 1]) if i + 1 < len(a) else 0.0) for i in range(0, len(a), 2)]
XF = 5.0
inputs, f = [], []
n = len(tracks); seg = total / n
for i, (tr, ss) in enumerate(tracks):
    need = seg + (XF if i < n - 1 else 0) + (XF if i > 0 else 0)
    inputs += ["-stream_loop", "-1", "-ss", f"{ss:.2f}", "-i", tr]
    f.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{need:.2f},asetpts=PTS-STARTPTS[s{i}]")
cur = "s0"
for i in range(1, n):
    f.append(f"[{cur}][s{i}]acrossfade=d={XF}:c1=tri:c2=tri[a{i}]"); cur = f"a{i}"
f.append(f"[{cur}]atrim=0:{total:.2f},loudnorm=I=-20:TP=-2:LRA=12,afade=t=out:st={total - 3:.2f}:d=3[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(f), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le", out], check=True)
print("wrote", out, f"{total:.1f} s")
