"""Archive photo shots for test v2 with the battle-maps archive_shots.py engine (3D depth Ken Burns via Depth Anything V2,
smooth sub-pixel moves, Oswald lower-third labels). Optional "shake": [t, amp_px, dur] = decaying camera shake (charges)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/maps"))
import archive_shots as A
PH = os.path.join(ROOT, "videos/oriskany/footage/src/photos")
OUT = os.path.join(HERE, "../segments"); os.makedirs(OUT, exist_ok=True)
ENC = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "veryfast", "-r", "30"]
W, H = 1920, 1080
SHOTS = [  # id, NARA id, dur (s, incl. 0.4 pad), move, focus, depth, label, shake
 ("p01_afloat", 6698606, 3.3, "in", [0.5, 0.5], True, None, None),
 ("p03_eod", 6698615, 2.7, "right", [0.5, 0.5], True, "NAVY EOD TEAM · MAY 17, 2006", None),
 ("p04_blast", 6698617, 1.7, "in", [0.3, 0.62], False, None, [0.61, 26, 0.9]),
 ("p05_smoke", 6698618, 2.7, "out", [0.5, 0.45], True, None, None),
 ("p05b_smoke2", 6698619, 2.15, "in", [0.55, 0.5], True, None, None),
 ("p06_list", 6698621, 2.05, "in", [0.5, 0.5], True, None, None),
 ("p07_stern", 6698623, 1.35, "up", [0.5, 0.5], False, None, None),
 ("p08_gone", 6698626, 0.95, "in", [0.5, 0.5], False, None, None),
 ("p10_bw", 7578422, 2.1, "in", [0.5, 0.5], True, "USS ORISKANY · 1950s", None),
 ("p11_tow", 6698598, 2.45, "left", [0.5, 0.5], True, "PENSACOLA · MAY 2006", None),
 ("p12_slam", 6698624, 2.1, "in", [0.5, 0.45], False, None, None),
 ("p13_cut", 6698569, 1.7, "in", [0.5, 0.45], True, None, None),
 ("p14_sparks", 6698580, 2.25, "in", [0.5, 0.45], True, None, None),
 ("p15_aerial", 6698599, 2.6, "right", [0.5, 0.5], True, None, None),
 ("p16_crowd", 6698586, 4.1, "left", [0.5, 0.5], True, None, None),
 ("p18_porthole", 6698555, 1.85, "in", [0.5, 0.5], False, None, None),
]
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
