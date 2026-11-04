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
SHOTS = [  # v4 HOOK_v1: id, NARA id, dur (s, incl. pad), move, focus, depth, label, shake
 ("p02_blast", 6698617, 2.25, "in", [0.45, 0.55], True, None, [0.03, 30, 1.0]),     # 4.30-6.38  WOW 1, held 2.1 s
 ("p05_foam", 6698627, 1.7, "in", [0.5, 0.5], True, None, None),                   # 9.98-11.50 "On purpose."
 ("p06_detcord", 6698576, 2.4, "in", [0.5, 0.45], True, None, None),   # label is a lower_third on "divers"  # 11.50-13.75
 ("p07_inside", 6698573, 2.35, "in", [0.45, 0.4], True, None, None),               # 13.75-15.95
 ("p08_helo", 6698609, 1.85, "in", [0.5, 0.45], True, None, None),                  # 15.95-17.70
 ("p09_smoke", 6698619, 0.5, "out", [0.55, 0.5], False, None, [0.02, 22, 0.45]),   # 17.70-18.40 second blast in the clear
 ("m1", 6698610, 0.7, "in", [0.5, 0.5], False, None, None),
 ("m2", 6698611, 0.7, "in", [0.5, 0.5], False, None, None),
 ("m3", 6698612, 0.8, "in", [0.5, 0.5], False, None, None),
 ("p11_bow", 6698624, 0.8, "in", [0.5, 0.35], False, None, None),                 # 19.85-20.55
 ("p11b_foam", 6698626, 0.85, "in", [0.5, 0.5], False, None, None),               # 20.55-21.25
 ("p12_cut", 6698569, 2.75, "in", [0.5, 0.45], True, None, None),                 # 21.25-23.84
 ("p13_weld", 6698553, 2.3, "in", [0.5, 0.45], True, None, None),                 # 23.84-26.00
]
MONTAGE = ("m37_sequence", ["m1", "m2", "m3"], 0.63)   # "Thirty-seven minutes later," 18.40-19.85
FILMS = []
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
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-vf", "fps=30", *ENC, "-t", str(each * len(parts) + 0.15), os.path.join(OUT, mid + ".mp4")], check=True)
    print(mid, "ok")
# archive film: fills the 16:9 frame (the 4:3 pillarbox is cropped), Oswald label
for fid, src, dur, label in FILMS:
    if only and fid not in only: continue
    A.film_shot({"film": os.path.join(HERE, "../assets/clips", src), "ss": 0.6, "label": label}, dur, os.path.join(OUT, fid + ".mp4"), W, H, ENC)
    print(fid, "ok")
