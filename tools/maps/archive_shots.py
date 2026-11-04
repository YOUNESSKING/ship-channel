"""Archive paragraphs as fast, moving shots (owner feedback on Gavin: photos held too long, never moving; use film).

A paragraph in archive.json can be a list of shot dicts instead of plain file names:
  {"film": "assets/film/clips/x.mp4", "ss": 1.0, "label": "SICILY · JULY 1943"}
  {"photo": "assets/media/x.jpg", "move": "in"|"out"|"left"|"right"|"up"|"down", "focus": [0.5, 0.3], "label": "..."}
  {"photo": "...", "parallax": true, "move": "in"}   (subject cut out with rembg, moves over a blurred background: 2.5D)
Optional "dur" per shot; otherwise the paragraph time is shared out evenly (aim: 3-5 s per shot).
Photos are rendered frame by frame with sub-pixel crops (smooth, no zoompan jitter): push-ins ~18 %, pans ~12 % of the frame.
A small lower-third label (Oswald, gold rule) fades in for the first ~2.6 s of a shot. Hard cuts between shots.
"""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FPS = 30
FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oswald-latin-700-normal.ttf")
_vig = {}


def vignette(W, H):
    if (W, H) not in _vig:
        y, x = np.mgrid[0:H, 0:W]
        r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
        _vig[(W, H)] = np.clip(1.0 - 0.32 * np.clip(r - 0.55, 0, 1) ** 1.5, 0, 1)[..., None]
    return _vig[(W, H)]


def label_layer(text, W, H):
    s = H / 1080
    f = ImageFont.truetype(FONT, int(40 * s))
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    tw = d.textlength(text, font=f); x, y = int(70 * s), int(H - 150 * s)
    d.rectangle([x - 18 * s, y - 12 * s, x + tw + 22 * s, y + 58 * s], fill=(18, 16, 12, 205))
    d.rectangle([x - 18 * s, y - 12 * s, x - 10 * s, y + 58 * s], fill=(201, 180, 138, 255))
    d.text((x, y - 2 * s), text, font=f, fill=(247, 243, 234, 255))
    return im


def headline_layer(year, text, W, H):
    """'Frontlines'-style date card: big gold year, a thin rule, the headline in spaced capitals (left third, over footage)"""
    s = H / 1080
    fy, ft = ImageFont.truetype(FONT, int(150 * s)), ImageFont.truetype(FONT, int(46 * s))
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # soft dark gradient on the left so the type reads over any footage
    g = np.zeros((H, W, 4), np.uint8); g[..., 3] = (np.clip(1 - np.linspace(0, 1, W) / 0.55, 0, 1) ** 1.5 * 170).astype(np.uint8)[None, :]
    im = Image.alpha_composite(im, Image.fromarray(g)); d = ImageDraw.Draw(im)
    x, y = int(120 * s), int(H * 0.36)
    d.text((x, y), year, font=fy, fill=(214, 186, 120, 255))
    d.rectangle([x, y + 190 * s, x + 520 * s, y + 194 * s], fill=(214, 186, 120, 255))
    d.text((x, y + 212 * s), text, font=ft, fill=(247, 243, 234, 255), spacing=int(10 * s))
    return im


def cover(img, W, H, scale=1.0):
    """resize so the image covers W*scale x H*scale"""
    k = max(W * scale / img.width, H * scale / img.height)
    return img.resize((max(1, int(img.width * k)), max(1, int(img.height * k))), Image.LANCZOS)


def boxes(move, focus, iw, ih, W, H):
    """start/end crop boxes (x0, y0, w, h) in source pixels for a camera move"""
    ar = W / H
    w_full = min(iw, ih * ar); h_full = w_full / ar
    fx, fy = focus
    def box(zoom, cx, cy):
        w, h = w_full / zoom, h_full / zoom
        x0 = min(max(cx * iw - w / 2, 0), iw - w); y0 = min(max(cy * ih - h / 2, 0), ih - h)
        return np.array([x0, y0, w, h], float)
    if move == "in":  return box(1.0, 0.5, 0.5), box(1.22, fx, fy)
    if move == "out": return box(1.22, fx, fy), box(1.0, 0.5, 0.5)
    pan = {"left": (0.62, 0.38, 0.5, 0.5), "right": (0.38, 0.62, 0.5, 0.5), "up": (0.5, 0.5, 0.62, 0.38), "down": (0.5, 0.5, 0.38, 0.62)}[move]
    return box(1.14, pan[0], pan[2]), box(1.14, pan[1], pan[3])


_depth_sess = None


def depth_map(img):
    """relative depth (1 = near) with Depth Anything V2 Small (Apache 2.0, ONNX, CPU ~0.6 s); smoothed for warping"""
    global _depth_sess
    import onnxruntime as ort
    if _depth_sess is None:
        so = ort.SessionOptions(); so.log_severity_level = 3
        _depth_sess = ort.InferenceSession("/opt/models/depth_anything_v2_small.onnx", so, providers=["CPUExecutionProvider"])
    x = np.asarray(img.convert("RGB").resize((518, 518)), np.float32) / 255
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    d = _depth_sess.run(None, {"pixel_values": x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)
    return Image.fromarray((d * 255).astype(np.uint8)).resize(img.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(max(2, img.width // 200)))


def ease(t):
    return t * t * (3 - 2 * t)


def photo_shot(sh, dur, out, W, H, enc):
    src = Image.open(sh["photo"]).convert("RGB")
    tr = sh.get("trim", 0.03)  # cut scan borders / film edges (fraction per side, or [left, top, right, bottom])
    tr = [tr] * 4 if isinstance(tr, (int, float)) else tr
    src = src.crop((int(src.width * tr[0]), int(src.height * tr[1]), int(src.width * (1 - tr[2])), int(src.height * (1 - tr[3]))))
    if src.width < W * 1.25:  # upscale small photos once so sub-pixel crops stay smooth
        src = src.resize((int(src.width * W * 1.25 / src.width), int(src.height * W * 1.25 / src.width)), Image.LANCZOS)
    move, focus = sh.get("move", "in"), sh.get("focus", [0.5, 0.42])
    b0, b1 = boxes(move, focus, src.width, src.height, W, H)
    fg = None
    if sh.get("parallax"):
        cut = sh["photo"].rsplit(".", 1)[0] + "_cut.png"
        if not os.path.exists(cut):
            from rembg import new_session, remove
            remove(Image.open(sh["photo"]).convert("RGB"), session=new_session("isnet-general-use")).save(cut)
        fg = Image.open(cut).convert("RGBA")
        fg = fg.crop((int(fg.width * tr[0]), int(fg.height * tr[1]), int(fg.width * (1 - tr[2])), int(fg.height * (1 - tr[3])))).resize(src.size, Image.LANCZOS)
        # background without the subject: fill the (dilated) subject area with a heavy blur, so the moving cut-out leaves no ghost
        m = fg.split()[3].point(lambda v: 255 if v > 30 else 0).filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(12))
        hole = src.filter(ImageFilter.GaussianBlur(src.width // 25))
        bg = Image.composite(hole, src, m).filter(ImageFilter.GaussianBlur(max(2, src.width // 500)))
        src = Image.blend(bg, Image.new("RGB", src.size, (20, 18, 14)), 0.2)
    lab = label_layer(sh["label"], W, H) if sh.get("label") else None
    dep = depth_map(src) if sh.get("depth") else None
    GY, GX = np.mgrid[0:H, 0:W].astype(np.float32)
    n = max(2, int(round(dur * FPS)))
    vig = vignette(W, H)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-frames:v", str(n), *enc, out], stdin=subprocess.PIPE)
    for k in range(n):
        t = ease(k / (n - 1))
        x0, y0, w, h = b0 + (b1 - b0) * t
        frame = src.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC)
        if dep is not None:  # 3D Ken Burns: near pixels zoom/slide further than far ones (inverse warp on the depth map)
            import cv2
            dm = np.asarray(dep.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC), np.float32) / 255
            ez = 1 + 0.07 * t * dm
            sx = {"left": -1, "right": 1}.get(move, 0) * 28 * t * (dm - 0.5); sy = {"up": -1, "down": 1}.get(move, 0) * 20 * t * (dm - 0.5)
            mx = (W / 2 + (GX - W / 2) / (1.05 * ez) - sx).astype(np.float32); my = (H / 2 + (GY - H / 2) / (1.05 * ez) - sy).astype(np.float32)
            frame = Image.fromarray(cv2.remap(np.asarray(frame), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT))
        if fg is not None:  # foreground moves ~60 % further than the background: depth
            fx0, fy0, fw, fh = b0 + (b1 - b0) * t * 1.3
            layer = fg.transform((W, H), Image.EXTENT, (fx0, fy0, fx0 + fw, fy0 + fh), Image.BICUBIC)
            frame = frame.convert("RGBA"); frame.alpha_composite(layer); frame = frame.convert("RGB")
        if lab is not None:
            a = min(1, k / 9) * (1 if k / FPS < 2.4 else max(0, 1 - (k / FPS - 2.4) / 0.4))
            if a > 0:
                fr = frame.convert("RGBA"); l2 = lab.copy(); l2.putalpha(l2.split()[3].point(lambda v: int(v * a))); fr.alpha_composite(l2); frame = fr.convert("RGB")
        arr = (np.asarray(frame, float) * vig).clip(0, 255).astype(np.uint8)
        p.stdin.write(arr.tobytes())
    p.stdin.close(); p.wait()


def film_crop(path):
    """content box of a clip (drops the black pillar/letterbox bars the clips were padded with)"""
    r = subprocess.run(["ffmpeg", "-ss", "1", "-t", "2", "-i", path, "-vf", "cropdetect=24:2:0", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = [l.split("crop=")[1].split()[0] for l in r.splitlines() if "crop=" in l]
    return m[-1] if m else None


def film_shot(sh, dur, out, W, H, enc):
    """film fills the whole 16:9 frame (4:3 film is cropped top/bottom, never shown with black side bars).
    "restored": true / "tint": true use the restore_film.py pass (cached in build/frontlines/); "headline": [year, text]."""
    if sh.get("restored") or sh.get("tint"):
        name = os.path.basename(sh["film"])[:-4]
        rp = f"build/frontlines/r_{name}{'_tint' if sh.get('tint') else ''}.mp4"
        if not os.path.exists(rp):
            from restore_film import restore
            os.makedirs("build/frontlines", exist_ok=True); restore(sh["film"], rp, tint=bool(sh.get("tint")))
        sh = dict(sh, film=rp)
    c = film_crop(sh["film"])
    vf = ([f"crop={c}"] if c else []) + [f"scale={W}:{H}:force_original_aspect_ratio=increase", f"crop={W}:{H}",
          f"tpad=stop_mode=clone:stop_duration={dur:.2f}"]
    tmp = out + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{sh.get('ss', 0):.2f}", "-i", sh["film"], "-t", f"{dur:.3f}", "-vf", ",".join(vf),
                    "-t", f"{dur:.3f}", *enc, tmp], check=True)
    if sh.get("frame"):  # merged-style test: film inside a rounded projector frame on a dark blurred copy, teal-orange grade
        from PIL import Image as _I, ImageDraw as _D, ImageFilter as _F
        fw, fh = int(W * 0.78) // 2 * 2, int(H * 0.78) // 2 * 2
        mp = out + ".mask.png"; m = _I.new("L", (fw, fh), 0); _D.Draw(m).rounded_rectangle((6, 6, fw - 6, fh - 6), radius=int(fh * 0.06), fill=255)
        m.filter(_F.GaussianBlur(3)).save(mp)
        t2 = out + ".f.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-loop", "1", "-i", mp, "-filter_complex",
                        f"[0:v]split[a][b];[b]scale={W}:{H},boxblur=40:2,eq=brightness=-0.32:saturation=0.35,colorbalance=bs=0.12:gs=0.04:rs=-0.06[bg];"
                        f"[a]scale={fw}:{fh},colorbalance=rs=-0.06:gs=0.01:bs=0.09:rh=0.07:gh=0.02:bh=-0.05,eq=contrast=1.08:saturation=1.1[fg];"
                        f"[1:v]format=gray[mk];[fg][mk]alphamerge[fgm];[bg][fgm]overlay=(W-w)/2:(H-h)/2:shortest=1,vignette=PI/4.5",
                        "-t", f"{dur:.3f}", *enc, t2], check=True)
        os.replace(t2, tmp); os.remove(mp)
    if sh.get("headline"):
        hp = out + ".head.png"; headline_layer(sh["headline"][0], sh["headline"][1], W, H).save(hp)
        t2 = out + ".h.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-loop", "1", "-i", hp, "-filter_complex",
                        f"[1:v]format=rgba,fade=t=in:st=0.15:d=0.5:alpha=1,fade=t=out:st={max(1.0, dur - 0.7):.2f}:d=0.5:alpha=1[h];"
                        "[0:v][h]overlay=x='-40+40*min(1\\,t/0.7)':y=0:shortest=1",
                        "-t", f"{dur:.3f}", *enc, t2], check=True)
        os.replace(t2, tmp); os.remove(hp)
    if sh.get("label"):
        lp = out + ".label.png"; label_layer(sh["label"], W, H).save(lp)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-loop", "1", "-i", lp, "-filter_complex",
                        "[1:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st=2.4:d=0.4:alpha=1[l];[0:v][l]overlay=0:0:shortest=1",
                        "-t", f"{dur:.3f}", *enc, out], check=True)
        os.remove(tmp); os.remove(lp)
    else:
        os.replace(tmp, out)


def build(shots, dur, out, W, H, enc):
    """render one archive paragraph (list of shot dicts) to `out`, exactly `dur` seconds"""
    fixed = sum(s.get("dur", 0) for s in shots); free = [s for s in shots if not s.get("dur")]
    each = (dur - fixed) / max(1, len(free))
    parts, t = [], 0.0
    for n, sh in enumerate(shots):
        d = sh.get("dur", each)
        if n == len(shots) - 1:
            d = dur - t
        fr0, fr1 = int(round(t * FPS)), int(round((t + d) * FPS)); d = (fr1 - fr0) / FPS; t += d
        part = f"{out[:-4]}_{n}.mp4"
        (film_shot if "film" in sh else photo_shot)(sh, d, part, W, H, enc)
        parts.append(part)
    lst = out[:-4] + "_list.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
