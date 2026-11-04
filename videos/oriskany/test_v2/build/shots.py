"""Archive photo shots for test v2 with the battle-maps archive_shots.py engine (3D depth Ken Burns via Depth Anything V2,
smooth sub-pixel moves, Oswald lower-third labels). Optional "shake": [t, amp_px, dur] = decaying camera shake (charges)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/maps"))
import archive_shots as A
PH = os.path.join(HERE, "../assets/photos")   # copies of the footage downloads
OUT = os.path.join(HERE, "../segments"); os.makedirs(OUT, exist_ok=True)
ENC = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "veryfast", "-r", "30"]
W, H = 1920, 1080
SHOTS = [  # id, NARA id, dur (s, incl. pad), move, focus, depth, label, shake   (only vetted items from footage/FOOTAGE_LIST.md)
 ("p01_helo", 6698609, 3.3, "in", [0.5, 0.45], True, None, None),
 ("p03_detcord", 6698576, 2.7, "in", [0.5, 0.5], True, "NAVY EOD TEAM · MAY 2006", None),
 ("p03b_plume", 6698616, 0.95, "in", [0.5, 0.5], False, None, None),
 ("p04_blast", 6698617, 1.45, "in", [0.3, 0.62], False, None, [0.07, 26, 0.9]),
 ("p05_smoke", 6698618, 1.45, "out", [0.5, 0.45], True, None, None),
 ("p05b_smoke2", 6698619, 1.55, "in", [0.55, 0.5], True, None, None),
 ("p05c_settle", 6698620, 1.9, "in", [0.5, 0.5], True, None, None),
 ("m1", 6698621, 0.45, "in", [0.5, 0.5], False, None, None),
 ("m2", 6698622, 0.45, "in", [0.5, 0.5], False, None, None),
 ("m3", 6698610, 0.45, "in", [0.5, 0.5], False, None, None),
 ("m4", 6698611, 0.45, "in", [0.5, 0.5], False, None, None),
 ("m5", 6698624, 0.45, "in", [0.5, 0.4], False, None, None),
 ("p07_bowhigh", 6698612, 0.75, "in", [0.5, 0.5], False, None, None),
 ("p08_slip", 6698625, 1.0, "in", [0.5, 0.5], False, None, None),
 ("p08b_boil", 6698627, 1.0, "in", [0.5, 0.5], False, None, None),
 ("p11_leave", 6698597, 2.45, "left", [0.5, 0.5], True, "LEAVING PENSACOLA · MAY 15, 2006", None),
 ("p12_slam", 6698628, 2.1, "in", [0.5, 0.45], False, None, None),
 ("p13_cut", 6698569, 1.7, "in", [0.5, 0.45], True, None, None),
 ("p14_weld", 6698553, 2.25, "in", [0.5, 0.45], True, None, None),
 ("p15_tow", 6698600, 2.6, "right", [0.5, 0.5], True, None, None),
 ("p16_seaward", 6698583, 4.1, "left", [0.5, 0.5], True, None, None),
 ("p18_porthole", 6698555, 1.85, "in", [0.5, 0.5], False, None, None),
]
MONTAGE = ("m37_sequence", ["m1", "m2", "m3", "m4", "m5"], 0.33)   # "37 minutes" told in ~1.7 s of real stills
FILMS = [("f10_vietnam", "b3_a4_catapult_1966.mp4", 2.1, "USS ORISKANY · OFF VIETNAM, 1966")]
only = sys.argv[1:]
for sid, nid, dur, move, focus, depth, label, shake in SHOTS:
    if only and sid not in only: continue
    out = os.path.join(OUT, sid + ".mp4")
    sh = {"photo": os.path.join(PH, f"nara_{nid}.jpg"), "move": move, "focus": focus, "depth": depth}
    if label: sh["label"] = label
    A.photo_shot(sh, dur, out, W, H, ENC)
    if shake:
        t0, amp, sd = shake; pad = amp + 4
        # decaying shake: crop window jitters for sd seconds after t0, then scale back to 1920x1080
        ex = f"{pad}+{amp}*sin(t*83)*exp(-(t-{t0})*4)*between(t,{t0},{t0 + sd})"
        ey = f"{pad}+{amp * 0.7:.1f}*cos(t*71)*exp(-(t-{t0})*4)*between(t,{t0},{t0 + sd})"
        tmp = out + ".s.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf", f"crop={W - 2 * pad}:{H - 2 * pad}:x='{ex}':y='{ey}',scale={W}:{H}", *ENC, tmp], check=True)
        os.replace(tmp, out)
    print(sid, "ok", flush=True)

# montage: hard cuts through the sinking sequence
mid, parts, each = MONTAGE
if not only or mid in only:
    lst = os.path.join(OUT, mid + ".txt")
    open(lst, "w").write("".join(f"file '{p}.mp4'\nduration {each}\n" for p in parts) + f"file '{parts[-1]}.mp4'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-vf", "fps=30", *ENC, "-t", str(each * len(parts) + 0.3), os.path.join(OUT, mid + ".mp4")], check=True)
    print(mid, "ok")
# archive film: fills the 16:9 frame (the 4:3 pillarbox is cropped), Oswald label
for fid, src, dur, label in FILMS:
    if only and fid not in only: continue
    A.film_shot({"film": os.path.join(HERE, "../assets/clips", src), "ss": 0.6, "label": label}, dur, os.path.join(OUT, fid + ".mp4"), W, H, ENC)
    print(fid, "ok")
