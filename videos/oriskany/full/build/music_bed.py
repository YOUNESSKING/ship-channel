"""Music bed for the full video (tools/sound/make_music_bed.py method: 5 s triangular crossfades, loudnorm -20 LUFS,
3 s fade-out; mix_clip.py then plays it at MUSIC_VOL 0.08 + MUSIC_TRIM_DB -6, ducked under the voice), with the cue points
of RENDER_PLAN "Sound": all Chris Zabriskie, Music from Neptune Flux (CC BY 4.0), as test v4 + assets/music/MUSIC_OPTIONS.md.
  main    "Stories About the World That Once Was" (neptuneflux-01, 6:55)  0 s -> c06 start (565.9 s), one internal
          crossfade back into the track at 90 s (the track is 6:55, the stretch is 9:26: no hard loop)
  tension "Your Mother's Daughter" (neptuneflux-03, 3:34)                c06 (the fish test, the reversal) -> last 60 s
  outro   "I Should Have Been More Human" (neptuneflux-09, 3:44)          last 60 s of narration + 18 s end screen
(album file numbers identified by length: 01 = 414.7 s, 03 = 214.1 s, 09 = 223.5 s, each unique on the album.)
Each crossfade is centred on its switch point. Writes audio/music_bed.wav + build/music_bed.json."""
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
Z = os.path.join(ROOT, "assets/music/candidates/zabriskie")
CH = {c["key"]: c for c in json.load(open(os.path.join(FULL, "chapters.json")))["chapters"]}
TOTAL = round(CH["c07"]["end"] + 18.0, 3)
XF = 5.0
SW_TENSION = CH["c06"]["start"]                       # 565.9
SW_OUTRO = round(CH["c07"]["voice_end"] - 60.0, 3)    # last 60 s of narration
SW_LOOP = 405.0                                       # main theme folds back into itself (crossfade 402.5-407.5)
# (track, title, source start s, switch time at which this piece is fully in)
P = [("neptuneflux-01.m4a", "Stories About the World That Once Was", 0.0, 0.0),
     ("neptuneflux-01.m4a", "Stories About the World That Once Was", 90.0, SW_LOOP),
     ("neptuneflux-03.m4a", "Your Mother's Daughter", 0.0, SW_TENSION),
     ("neptuneflux-03.m4a", "Your Mother's Daughter", 25.0, SW_TENSION + 200.0),
     ("neptuneflux-09.m4a", "I Should Have Been More Human", 0.0, SW_OUTRO)]
bounds = [p[3] for p in P] + [TOTAL]
inputs, f, plan = [], [], []
for i, (tr, title, ss, sw) in enumerate(P):
    a = 0.0 if i == 0 else sw - XF / 2              # this piece starts sounding (crossfade start)
    b = TOTAL if i == len(P) - 1 else bounds[i + 1] + XF / 2
    need = b - a
    inputs += ["-ss", f"{ss:.2f}", "-i", os.path.join(Z, tr)]
    f.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{need:.3f},asetpts=PTS-STARTPTS[s{i}]")
    plan.append(dict(track=tr, title=title, src_start=ss, plays_from=round(a, 3), plays_to=round(b, 3), src_end=round(ss + need, 2)))
cur = "s0"
for i in range(1, len(P)):
    f.append(f"[{cur}][s{i}]acrossfade=d={XF}:c1=tri:c2=tri[a{i}]"); cur = f"a{i}"
f.append(f"[{cur}]atrim=0:{TOTAL:.3f},loudnorm=I=-20:TP=-2:LRA=12,afade=t=out:st={TOTAL - 3:.3f}:d=3[out]")
out = os.path.join(FULL, "audio", "music_bed.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(f), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le", out], check=True)
for p in plan: assert p["src_end"] <= {"neptuneflux-01.m4a": 414.6, "neptuneflux-03.m4a": 214.0, "neptuneflux-09.m4a": 223.5}[p["track"]], p
json.dump({"total": TOTAL, "crossfade_s": XF, "pieces": plan}, open(os.path.join(HERE, "music_bed.json"), "w"), indent=1)
d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]).decode())
print("wrote", out, f"{d:.2f} s (want {TOTAL})"); [print(p) for p in plan]
