"""Check film / photo segments (or a whole render) for the picture faults the Oriskany test v3 critic found by eye:

  CUT     an internal film cut or dissolve inside one shot segment (ffmpeg scene score > 0.28) -> ghosting / jump
  BLOB    an obstruction: one dark connected blob covering > 25 % of the picture for > 5 frames in a row
          (out-of-focus foreground, a hand, a film-gate shadow). Black pillar / letter bars are ignored.
  FLASH   a film-burn / flash glitch: the frame brightness jumps by > 0.22 against both neighbours, or > 40 % of the frame
          blows out to near-white, for 1-6 frames (real explosions in a shot you WANT can be whitelisted with --allow-flash)

  python3 tools/film/check_clips.py videos/oriskany/test_v3/segments/f*.mp4            # one report line per problem
  python3 tools/film/check_clips.py --no-cuts oriskany_test_v3.mp4                     # a full video: cuts are expected there
Exit code 1 if anything is found. Fast: frames are analysed at 160x90.
"""
import subprocess, sys
import numpy as np
from scipy import ndimage

W, H = 160, 90


def frames(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H},format=rgb24", "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    n = len(a) // (W * H * 3)
    fps = 30.0
    try:
        num, den = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", path]).decode().strip().split("/")
        fps = float(num) / float(den)
    except Exception: pass
    return a[: n * W * H * 3].reshape(n, H, W, 3).astype(np.float32) / 255.0, fps


def bars_mask(lum):
    """columns / rows that stay black through the whole clip (pillarbox / letterbox)"""
    mx = lum.max(axis=0)
    cols = mx.max(axis=0) < 0.08; rows = mx.max(axis=1) < 0.08
    m = np.zeros((H, W), bool); m[:, cols] = True; m[rows, :] = True
    return m


def runs(flags, min_len=1, max_len=10 ** 9):
    out, s = [], None
    for i, f in enumerate(list(flags) + [False]):
        if f and s is None: s = i
        if not f and s is not None:
            if min_len <= i - s <= max_len: out.append((s, i - 1))
            s = None
    return out


def check(path, cuts=True, allow_flash=False, blob_frac=0.25, blob_frames=6):
    fr, fps = frames(path)
    if not len(fr): return [f"{path}: cannot read"]
    lum = fr @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    bars = bars_mask(lum); area = (~bars).sum()
    probs = []
    # BLOB: largest dark connected component inside the picture area
    big = np.zeros(len(fr), bool); share = np.zeros(len(fr))
    for i, l in enumerate(lum):
        dark = (l < 0.16) & ~bars
        lab, n = ndimage.label(dark)
        if n:
            sz = np.bincount(lab.ravel())[1:].max(); share[i] = sz / area
            big[i] = share[i] > blob_frac
    for a, b in runs(big, blob_frames):
        probs.append(f"BLOB  {a / fps:6.2f}-{(b + 1) / fps:6.2f}s  dark blob up to {share[a:b + 1].max() * 100:.0f}% of the frame")
    # FLASH: short brightness spikes or blow-outs
    if not allow_flash:
        m = np.array([l[~bars].mean() for l in lum]); white = np.array([(l[~bars] > 0.92).mean() for l in lum])
        sp = np.zeros(len(m), bool)
        for i in range(len(m)):
            lo, hi = max(0, i - 4), min(len(m), i + 5)
            base = np.median(np.r_[m[lo:i], m[i + 1:hi]]) if hi - lo > 1 else m[i]
            sp[i] = (m[i] - base > 0.22) or (white[i] > 0.4 and np.median(white[lo:hi]) < 0.2)
        for a, b in runs(sp, 1, 6):
            probs.append(f"FLASH {a / fps:6.2f}-{(b + 1) / fps:6.2f}s  brightness spike / burn ({(b - a + 1)} frames)")
    # CUT: scene score
    if cuts:
        e = subprocess.run(["ffmpeg", "-v", "info", "-i", path, "-an", "-vf", "scale=320:-2,select='gt(scene,0.28)',metadata=print", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        ts = [float(l.split("pts_time:")[1].split()[0]) for l in e.splitlines() if "pts_time:" in l]
        last = -1
        for t in ts:
            if t - last > 0.25: probs.append(f"CUT   {t:6.2f}s       internal cut / dissolve inside the segment")
            last = t
    return [f"{path}: {p}" for p in probs]


if __name__ == "__main__":
    a = sys.argv[1:]; cuts = "--no-cuts" not in a; af = "--allow-flash" in a
    files = [x for x in a if not x.startswith("--")]
    allp = []
    for f in files:
        p = check(f, cuts, af); allp += p
        print("\n".join(p) if p else f"{f}: OK", flush=True)
    sys.exit(1 if allp else 0)
