"""One colour grade for every archive source in a ship video (Oriskany test v3 critique: "five colour looks").

1950s B&W film, 1960s Kodachrome / Ektachrome film, 2006 digital Navy photos and the teal/gold maps must look like one series.
The grade has two stages, both plain ffmpeg filters (no LUT file needed, no external tools):

  1. NORMALISE (per source, measured): neutralise the colour cast of the mid-tones (the warm/sepia cast of the 2006 sunset photos,
     the cyan/magenta drift of faded film), set black / white points to the same levels, and pull saturation toward one target
     (Kodachrome is toned down, flat digital photos are lifted a little). Near-monochrome sources (B&W film, sepia prints) are
     made fully neutral grey: no sepia, no blue tint.
  2. LOOK (fixed, the same for everything): `LOOK` below: a light teal in the shadows and warm-cream highlights to sit with the
     map-kit palette (teal sea, cream #f3eee2 / gold #c9b48a type), a touch of contrast, matched black level. No grain, no blur,
     no heavy vignette (house rule: no film look). Maps are NOT graded: they are the reference the archive is pulled toward.

Use:
  from ship_grade import grade_filter
  vf = grade_filter("clip.mp4", ss=1.0, dur=3.0)     # or grade_filter("photo.jpg")  -> "colorchannelmixer=...,colorlevels=...,eq=...,LOOK"
  tools/maps/archive_shots.py applies it when a shot has "grade": "ship" (or env ARCHIVE_GRADE=ship).
  templates/grade/ship_archive.vf holds LOOK alone (for build_chapter.py GRADE=ship_archive on clips that were not normalised).
CLI (before / after sheet):  python3 tools/grade/ship_grade.py --sheet OUT.jpg [--map MAP.mp4] SRC[@ss] SRC ...
"""
import os, subprocess, sys
import numpy as np

LOOK = ("colorbalance=rs=-0.035:gs=0.005:bs=0.045:rm=-0.005:gm=0:bm=0.01:rh=0.03:gh=0.012:bh=-0.025,"
        "eq=contrast=1.05:saturation=0.96")
TARGET_SAT, BLACK, WHITE = 0.26, 0.035, 0.94


def _frames_video(path, ss=0.0, dur=None, n=6, w=192, h=108):
    """n small RGB frames spread over [ss, ss+dur] (float 0..1)"""
    if dur is None:
        try: dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode()) - ss
        except Exception: dur = 3.0
    out = []
    for k in range(n):
        t = ss + dur * (k + 0.5) / n
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1", "-vf", f"scale={w}:{h}",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
        if len(r.stdout) == w * h * 3: out.append(np.frombuffer(r.stdout, np.uint8).reshape(h, w, 3) / 255.0)
    return out


def _content(a):
    """drop black pillar / letterbox bars (rows / columns that are nearly black) so they don't skew the stats"""
    lum = a.mean(axis=2)
    rows = np.where(lum.mean(axis=1) > 0.04)[0]; cols = np.where(lum.mean(axis=0) > 0.04)[0]
    if len(rows) > 4 and len(cols) > 4: a = a[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    return a


def measure(path, ss=0.0, dur=None):
    if path.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff")):
        from PIL import Image
        im = Image.open(path).convert("RGB"); im.thumbnail((320, 320)); fr = [np.asarray(im) / 255.0]
    else:
        fr = _frames_video(path, ss, dur)
    px = np.concatenate([_content(f).reshape(-1, 3) for f in fr])
    lum = px @ np.array([0.2126, 0.7152, 0.0722])
    mid = px[(lum > 0.2) & (lum < 0.8)]
    if len(mid) < 50: mid = px
    mx, mn = px.max(axis=1), px.min(axis=1)
    sat = np.where(mx > 0.05, (mx - mn) / np.maximum(mx, 1e-6), 0)
    return {"mid_rgb": mid.mean(axis=0), "black": float(np.percentile(lum, 1.0)), "white": float(np.percentile(lum, 99.5)),
            "sat": float(np.mean(sat[(lum > 0.1) & (lum < 0.9)])) if np.any((lum > 0.1) & (lum < 0.9)) else float(sat.mean())}


def normalise_filter(st, strength=0.75):
    m = st["mid_rgb"]; g = m.mean() / np.maximum(m, 1e-3); g = 1 + strength * (g - 1)
    g = g / (np.array([0.2126, 0.7152, 0.0722]) @ g)             # keep luminance
    g = np.clip(g, 0.78, 1.28)
    mono = st["sat"] < 0.085
    b, w = min(st["black"], 0.25), max(st["white"], st["black"] + 0.3)
    if (WHITE - BLACK) / (w - b) > 1.2: w = b + (WHITE - BLACK) / 1.2       # never stretch a flat source more than 1.2x (blown skies)
    lv = (f"colorlevels=rimin={b:.3f}:gimin={b:.3f}:bimin={b:.3f}:rimax={w:.3f}:gimax={w:.3f}:bimax={w:.3f}"
          f":romin={BLACK}:gomin={BLACK}:bomin={BLACK}:romax={WHITE}:gomax={WHITE}:bomax={WHITE}")
    if mono:   # B&W film / sepia print: neutral grey, no tint
        return f"hue=s=0,{lv}"
    s = float(np.clip((TARGET_SAT / max(st['sat'], 0.02)) ** 0.6, 0.72, 1.15))
    return f"colorchannelmixer=rr={g[0]:.3f}:gg={g[1]:.3f}:bb={g[2]:.3f},{lv},eq=saturation={s:.3f}"


def grade_filter(path, ss=0.0, dur=None, strength=0.75):
    """the full grade for one source: measured normalisation + the fixed LOOK"""
    return normalise_filter(measure(path, ss, dur), strength) + "," + LOOK


def _still(path, ss, vf, w=640, h=360):
    """one frame (video at ss, or the photo) scaled to fill w x h, optional filter -> RGB array"""
    chain = (vf + "," if vf else "") + f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    args = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.2f}"] if ss else []) + ["-i", path, "-frames:v", "1", "-vf", chain, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    r = subprocess.run(args, capture_output=True); return np.frombuffer(r.stdout, np.uint8).reshape(h, w, 3)


def sheet(out, srcs, map_clip=None):
    """before | after rows for each source, plus the map (reference, never graded)"""
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../maps/oswald-latin-700-normal.ttf"), 26)
    rows = []
    for spec in srcs:
        path, ss = (spec.rsplit("@", 1) + [0])[:2] if "@" in spec else (spec, 0); ss = float(ss)
        vf = grade_filter(path, ss, 2.0 if ss else None)
        a, b = _still(path, ss, ""), _still(path, ss, vf)
        rows.append((os.path.basename(path), a, b, vf))
    if map_clip: m = _still(map_clip, 1.0, ""); rows.append((os.path.basename(map_clip) + " (map: reference, not graded)", m, m, ""))
    W, H = 640, 360; im = Image.new("RGB", (2 * W + 30, len(rows) * (H + 50) + 60), (11, 20, 28)); d = ImageDraw.Draw(im)
    d.text((10, 14), "BEFORE (as delivered)", font=font, fill=(201, 180, 138)); d.text((W + 30, 14), "AFTER (normalise + ship LOOK)", font=font, fill=(201, 180, 138))
    for i, (name, a, b, vf) in enumerate(rows):
        y = 60 + i * (H + 50)
        im.paste(Image.fromarray(a), (10, y)); im.paste(Image.fromarray(b), (W + 20, y))
        d.text((10, y + H + 6), name, font=font, fill=(247, 243, 234))
    im.save(out, quality=86); print("wrote", out)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--sheet":
        out = a[1]; rest = a[2:]; mp = None
        if "--map" in rest: i = rest.index("--map"); mp = rest[i + 1]; rest = rest[:i] + rest[i + 2:]
        sheet(out, rest, mp)
    else:
        for p in a: print(p, "->", grade_filter(p))
