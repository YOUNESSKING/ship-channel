"""Build the channel's approved music bed (owner-approved on Goose Green) for THIS video's length and chapters.

usage (from the project folder): python3 tools/make_music_bed.py
Reads audio/timing.json (duration) and the CHAPTERS list in tools/assemble_full.py (chapter start tags), and lays
the four approved Kevin MacLeod tracks (CC BY 4.0, in assets/media/music_src_*.mp3) over the video:
  hook + move 1      -> "Long Note One"   (tense drone)
  move 2             -> "Wounded"         (grim piano + strings)
  move 3             -> "Long Note Two"   (quiet, suspenseful)
  ending             -> "Anguish"         (reflective)
Each section is looped/trimmed to fit, joined with 5 s crossfades, normalised to -20 LUFS, 3 s fade-out.
Writes assets/media/music.wav (assemble_full.py mixes it at MUSIC_VOL, ducked under the voice).
Credit line for the description: Music by Kevin MacLeod (incompetech.com): "Long Note One", "Wounded",
"Long Note Two", "Anguish". Licensed under Creative Commons: By Attribution 4.0 License.
"""
import json, os, re, subprocess

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
os.chdir(ROOT)
M = "assets/media"
TRACKS = ["music_src_long-note-one.mp3", "music_src_wounded.mp3", "music_src_long-note-two.mp3", "music_src_anguish.mp3"]
XF = 5.0
T = json.load(open("audio/timing.json"))
total = T["duration"] + 6
starts = {p["tag"].split("|")[0].replace("MAP:", "").replace("ARCHIVE:", "").strip(): p["start"] for p in T["paragraphs"]}
chap = re.findall(r'\("([\w-]+)",\s*"[^"]*"\)', open("tools/assemble_full.py").read().split("CHAPTERS")[1].split("]")[0])
# section boundaries: move 2 start, move 3 start, ending start (chapters 3, 4, 5 of 5)
cuts = [starts[c] for c in chap[2:5]] if len(chap) >= 5 else [total * 0.4, total * 0.67, total * 0.92]
bounds = [0.0] + cuts + [total]
inputs, f = [], []
for i, tr in enumerate(TRACKS):
    need = bounds[i + 1] - bounds[i] + (XF if i < 3 else 0) + (XF if i > 0 else 0)
    inputs += ["-stream_loop", "-1", "-i", f"{M}/{tr}"]
    f.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{need:.2f},asetpts=PTS-STARTPTS[s{i}]")
f.append(f"[s0][s1]acrossfade=d={XF}:c1=tri:c2=tri[a1]")
f.append(f"[a1][s2]acrossfade=d={XF}:c1=tri:c2=tri[a2]")
f.append(f"[a2][s3]acrossfade=d={XF}:c1=tri:c2=tri,atrim=0:{total:.2f},loudnorm=I=-20:TP=-2:LRA=12,afade=t=out:st={total - 3:.2f}:d=3[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(f), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le",
                f"{M}/music.wav"], check=True)
print(f"wrote {M}/music.wav ({total:.0f} s); section starts:", [round(b) for b in bounds[:-1]])
