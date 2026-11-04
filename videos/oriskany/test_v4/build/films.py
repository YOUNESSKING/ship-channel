"""v3 VIDEO-FIRST: real NARA film shots (US Navy, public domain) cut from footage/src/clips with the archive_shots film engine
(4:3 film fills the 16:9 frame, Oswald lower-third labels). Labels only where FOOTAGE_LIST.md confirms ship + year."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/maps"))
import archive_shots as A
CL = os.path.join(ROOT, "videos/oriskany/footage/src/clips")
OUT = os.path.join(HERE, "../segments"); os.makedirs(OUT, exist_ok=True)
ENC = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "veryfast", "-r", "30"]
FILMS = [  # v4: id, clip, start in clip (s), dur (s, incl. pad), label   (no internal cuts: checked with scene>0.35)
 ("f03_catapult", "b3_a4_catapult_1966.mp4", 0.6, 1.75, "USS ORISKANY · OFF VIETNAM, 1966"),  # 6.38-7.98 "No enemy sank her."
 ("f04_island", "b3_island_34_1966.mp4", 2.55, 1.45, None),   # the "34" only (2.5 s on); slowed x1.45 below to 2.1 s          # 7.98-9.98 the "34" (S-2 "13" is before 1.9 s)
 ("f16_anchor", "b2_oriskany_at_anchor_1952.mp4", 0.4, 2.35, None), # 32.70-34.90 "buried in her past"
 ("f19_stacks", "b10_ssus_stacks.mp4", 0.6, 2.15, None),            # 39.55-41.55 "the ocean liner"
 ("f20_bow", "b10_ssus_underway_side.mp4", 0.05, 2.2, None),       # 41.55-43.70 bow with the "UNITED STATES" lettering (scene cut at 2.2 s)
 ("f20b_profile", "b10_ssus_profile.mp4", 0.5, 2.15, None),       # 43.70-45.80 the whole liner, funnels smoking
]
only = sys.argv[1:]
for fid, src, ss, dur, label in FILMS:
    if only and fid not in only: continue
    sh = {"film": os.path.join(CL, src), "ss": ss}
    if label: sh["label"] = label
    A.film_shot(sh, dur, os.path.join(OUT, fid + ".mp4"), 1920, 1080, ENC)
    print(fid, "ok", flush=True)

# f04: the "34" section is only 1.45 s long: slow it to 2.1 s (film looks natural at 0.69x), no repeat, no "13"
if not only or "f04_island" in only:
    import subprocess
    p = os.path.join(OUT, "f04_island.mp4"); tmp = p + ".slow.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf", "setpts=1.45*PTS,fps=30", *ENC, "-t", "2.1", tmp], check=True)
    os.replace(tmp, p); print("f04_island slowed")
