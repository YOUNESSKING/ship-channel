"""v3 VIDEO-FIRST: real NARA film shots (US Navy, public domain) cut from footage/src/clips with the archive_shots film engine
(4:3 film fills the 16:9 frame, Oswald lower-third labels). Labels only where FOOTAGE_LIST.md confirms ship + year."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/maps"))
import archive_shots as A
CL = os.path.join(ROOT, "videos/oriskany/footage/src/clips")
OUT = os.path.join(HERE, "../segments"); os.makedirs(OUT, exist_ok=True)
ENC = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "veryfast", "-r", "30"]
FILMS = [  # id, clip, start in clip (s), dur (s, incl. pad), label
 ("f06_service", "b3_carrier_aerial_1966.mp4", 0.3, 2.8, None),   # the DECOMMISSIONED 1976 lower third carries the caption
 ("f07_bow", "b3_bow_on_underway_1966.mp4", 0.5, 1.9, None),
 ("f10_aerial", "b3_aerial_underway_1969.mp4", 0.4, 2.5, None),
 ("f12_launch", "b3_a4e_launch_1968.mp4", 0.6, 2.0, "USS ORISKANY · 1968"),
 ("f13_island", "b3_island_34_1966.mp4", 2.3, 2.35, None),   # the big "34" (the S-2 "13" comes first in the clip)
 ("f15_anchor", "b2_oriskany_at_anchor_1952.mp4", 0.4, 1.85, None),
 ("f18_catapult", "b3_a4_catapult_1966.mp4", 0.6, 2.75, "USS ORISKANY · OFF VIETNAM, 1966"),
 ("f19_aerial_launch", "b3_aerial_launching.mp4", 0.5, 2.4, None),
 ("f20_bg", "b3_aerial_underway2_1969.mp4", 0.2, 5.5, None),
 ("f21_deck", "b3_deck_parked_1968.mp4", 0.8, 1.8, None),
 ("f23_ss1", "b10_ssus_bow_wave.mp4", 0.6, 2.65, "SS UNITED STATES · 1968"),
 ("f23_ss2", "b10_ssus_stacks.mp4", 0.6, 1.85, None),
 ("f23_ss3", "b10_ssus_profile.mp4", 1.0, 1.2, None),
]
only = sys.argv[1:]
for fid, src, ss, dur, label in FILMS:
    if only and fid not in only: continue
    sh = {"film": os.path.join(CL, src), "ss": ss}
    if label: sh["label"] = label
    A.film_shot(sh, dur, os.path.join(OUT, fid + ".mp4"), 1920, 1080, ENC)
    print(fid, "ok", flush=True)
