"""v8 hook re-time (the voice changed, so the hook is no longer frame-locked to test v4).

The approved test-v4 hook (test_v4/chapter/c01.json + test_v4/segments) is kept shot for shot, look for look; only its timing
follows the Archive voice:
  - every fixed shot start / label time ("t17.98") keeps its lead on the word it lands on (next word within 0.6 s), else it moves
    through the v7 -> v8 word map (build/warp_v8.py); snapped to a frame;
    "@word" times are resolved by the chapter builder against the new build/words.json as before;
  - every hook clip is re-timed to its new shot length: output frame k shows the source frame at the mapped time. The map is
    linear per shot between its cut points, plus a knot on the word a baked event lands on (hero_a: hull touches on "floor";
    dive: "Gulf"; endmap: "thirteen"), so the motion inside a shot keeps an even speed and the baked events stay on their words.
Writes segments_hook/*.mp4 and chapter/c01.json (clips_dir ../segments_hook). Render with build/render_all.sh c01."""
import json, os, subprocess, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
sys.path.insert(0, HERE)
import warp_v8 as WP
T4 = os.path.join(ROOT, "videos/oriskany/test_v4")
OUTD = os.path.join(FULL, "segments_hook"); os.makedirs(OUTD, exist_ok=True)
FPS, PAD = 30, 0.3
W8 = json.load(open(os.path.join(HERE, "words.json")))
W7 = json.load(open(os.path.join(HERE, "words_v7.json")))
CH = {c["key"]: c for c in json.load(open(os.path.join(FULL, "chapters.json")))["chapters"]}
c1 = json.load(open(os.path.join(T4, "chapter/c01.json")))
EVENT = {"hero_a.mp4": ["floor?"], "dive.mp4": ["Gulf"], "endmap.mp4": ["thirteen"]}
OLD_END = 48.625            # the hook's end in v7 (= c02 start)
snap = lambda t: round(round(t * FPS) / FPS, 4)

ostart = []
for s in c1["shots"]:
    st = s.get("start", 0)
    ostart.append(float(st) if isinstance(st, (int, float)) else float(st[1:]))
oend = ostart[1:] + [OLD_END]
def cut_new(t):
    """a cut keeps its lead on the word it lands on (the next word starting within 0.6 s); otherwise the plain word map"""
    nxt = next((x for x in W7 if x["start"] >= t - 1e-3), None)
    if nxt and nxt["start"] - t < 0.6:
        i = W7.index(nxt); return W8[i]["start"] - (nxt["start"] - t)
    return WP.new(t)


nstart = [0.0] + [snap(cut_new(t)) for t in ostart[1:]]
nend = nstart[1:] + [CH["c02"]["start"]]


def wword(w, a, b):   # v7 time of word w inside [a, b)
    return next((x["start"] for x in W7 if a - 1e-3 <= x["start"] < b and x["w"] == w), None)


def retime(src, dst, knots_old, knots_new, out_len):
    """frame k of dst (k / FPS) shows src at the old local time mapped back through the knots"""
    probe = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                     "-of", "csv=p=0", src]).decode().strip().split(",")
    w, h = int(probe[0]), int(probe[1])
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-r", str(FPS), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    n = int(round(out_len * FPS))
    tn = np.arange(n) / FPS
    to = np.interp(tn, knots_new, knots_old, right=None)
    over = tn > knots_new[-1]; to[over] = knots_old[-1] + (tn[over] - knots_new[-1])   # past the last knot: speed 1
    idx = np.clip(np.round(to * FPS).astype(int), 0, len(fr) - 1)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "veryfast", dst], stdin=subprocess.PIPE)
    for i in idx: p.stdin.write(fr[i].tobytes())
    p.stdin.close(); assert p.wait() == 0, dst
    return len(fr) / FPS, idx


rep = []
for i, s in enumerate(c1["shots"]):
    a0, b0, a1, b1 = ostart[i], oend[i], nstart[i], nend[i]
    for key in ("clip", "bg_clip"):
        f = (s.get(key) or {}).get("file")
        if not f: continue
        ko, kn = [0.0], [0.0]
        for wd in EVENT.get(f, []):
            t7 = wword(wd, a0, b0)
            if t7 is not None: ko.append(t7 - a0); kn.append(WP.new(t7) - a1)
        ko.append(b0 - a0); kn.append(b1 - a1)
        src = os.path.join(T4, "segments", f); dst = os.path.join(OUTD, f)
        srclen, idx = retime(src, dst, np.array(ko), np.array(kn), (b1 - a1) + PAD)
        rep.append(dict(shot=s["id"], file=f, old=[a0, b0], new=[a1, b1], speed=round((b0 - a0) / (b1 - a1), 3),
                        knots_old=[round(x, 3) for x in ko], knots_new=[round(x, 3) for x in kn], src_len=round(srclen, 3),
                        last_src_frame=int(idx[-1])))
        print(rep[-1], flush=True)
    if i > 0: s["start"] = f"t{a1 + 0.5 / FPS:.4f}"   # half a frame past the frame (as test v4's 17.65): a cut exactly on a frame time
                                                     # rendered one frame late and lost the first (white) frame of the flash
    for k, v in list(s.get("params", {}).items()):
        if isinstance(v, str) and v.startswith("t") and v[1:].replace(".", "").isdigit(): s["params"][k] = f"t{snap(cut_new(float(v[1:]))):.4f}"
    if s.get("template") == "anim_xray" and s["params"].get("image", "").startswith("../assets/"):
        s["params"]["image"] = "../../test_v4/assets/" + s["params"]["image"][len("../assets/"):]
c1.update(title="Oriskany full · Hook (test v4 look, re-timed to the Archive voice, v8)", words="../build/words.json", audio_offset=0.0,
          clips_dir="../segments_hook", duration=round(CH["c02"]["start"], 3), fade_out=0.0)
json.dump(c1, open(os.path.join(FULL, "chapter", "c01.json"), "w"), indent=1, ensure_ascii=False)
json.dump(dict(old_starts=ostart, new_starts=nstart, clips=rep), open(os.path.join(HERE, "hook_v8.json"), "w"), indent=1)
print("hook", OLD_END, "->", CH["c02"]["start"], "s;", len(rep), "clips re-timed")
