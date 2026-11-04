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
 ("f04_island", "b3_island_34_1966.mp4", 1.9, 2.15, None),          # 7.98-9.98 the "34" (S-2 "13" is before 1.9 s)
 ("f16_anchor", "b2_oriskany_at_anchor_1952.mp4", 0.4, 2.35, None), # 32.70-34.90 "buried in her past"
 ("f19_stacks", "b10_ssus_stacks.mp4", 0.6, 2.15, None),            # 39.55-41.55 "the ocean liner"
 ("f20_bow", "b10_ssus_bow_letters.mp4", 0.15, 3.2, None),          # 41.55-44.65 (scene cut at 3.4 s in the clip: stay before it)
 ("f20b_side", "b10_ssus_underway_side.mp4", 0.5, 1.3, None),      # 44.65-45.80
]
only = sys.argv[1:]
for fid, src, ss, dur, label in FILMS:
    if only and fid not in only: continue
    sh = {"film": os.path.join(CL, src), "ss": ss}
    if label: sh["label"] = label
    A.film_shot(sh, dur, os.path.join(OUT, fid + ".mp4"), 1920, 1080, ENC)
    print(fid, "ok", flush=True)
