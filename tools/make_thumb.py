#!/usr/bin/env python3
"""Thumbnail compositor, Fossil (@fossilvideos) style, v2.

The AI picture has NO text; the text is added here.

Usage:
  make_thumb.py picture.png out.jpg "LINE" ["LINE" ...] [options]

A LINE is one or more coloured words joined with "+":
  "15|red+Minutes|white"      -> one line: red "15", white "Minutes"
  "Too|white"  "Easy?|red"    -> two stacked lines
Colour names: white, red (Fossil's pure red #fc0101), or any #hex.

Options (defaults = measured on Fossil's 1280x720 thumbnails, Oct 2026):
  --cap 120      cap height in px (Fossil: 110-150 px = 15-21 % of the height)
  --x 1240       anchor x; with --align right (default) this is the right edge
  --y 50         top of the first line
  --align right|left|center   (stacked lines: use center, like Fossil's "Too / Easy?")
  --lh 1.4       line pitch as a multiple of the cap height (Fossil leaves a clear gap)
  --stretch 1.0  horizontal stretch. Measured: Fossil's letters have Anton's proportions
                 ("Too" width/cap = 1.53 on Fossil, 1.57 in Anton), so no stretch is needed.
  --stroke 3     thin black outline (Fossil: 2-4 px, not a thick sticker outline)
  --glow 16      blur radius of the soft black shadow/glow behind the letters
  --plate        heavy black glow "plate" behind the text (Fossil's 9 Minutes look)
  --grit 1.0     Fossil's over-processed finish on the picture: upscaled-and-oversharpened
                 paint texture, halo edges, saturation boost, crushed blacks. 0 = off
  --ramp 0       dark fade on the right side of the picture (0 = off; e.g. 0.6)
Writes out.jpg (1280x720, q95) and out_168.png (168x94 phone-size preview).
Font: Anton (SIL OFL, free for commercial use)."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "Anton-Regular.ttf")
COL = {"white": "#ffffff", "red": "#fc0101"}


def fit_169(im):
    w, h = im.size
    if w / h > 16 / 9:
        cw = int(h * 16 / 9); l = (w - cw) // 2; im = im.crop((l, 0, l + cw, h))
    elif w / h < 16 / 9:
        ch = int(w * 9 / 16); t = (h - ch) // 2; im = im.crop((0, t, w, t + ch))
    return im.resize((1280, 720), Image.LANCZOS)


def grit(im, k):
    """Fossil's finish: their pictures look like a small AI/painted image that was upscaled
    and then hard-sharpened (smeared paint texture + bright halo edges, no fine hairlines),
    with boosted colour and crushed blacks. We copy that: downscale, upscale, big-radius
    unsharp mask, saturation, black crush. k=1 is the measured match; 0 = off."""
    if k <= 0:
        return im
    w, h = im.size
    s = max(0.2, 1 - 0.55 * k)
    im = im.resize((int(w * s), int(h * s)), Image.LANCZOS).resize((w, h), Image.BICUBIC)
    im = im.filter(ImageFilter.UnsharpMask(radius=5, percent=int(140 * k), threshold=2))
    im = ImageEnhance.Color(im).enhance(1 + 0.2 * k)
    a = np.asarray(im).astype(float) / 255
    a = np.clip((a - 0.03 * k) / (1 - 0.03 * k), 0, 1)
    return Image.fromarray((a * 255).astype("uint8"))


def render_word(text, font, stretch, color, stroke):
    """Render one word on its own RGBA layer, stretched horizontally."""
    l, t, r, b = font.getbbox(text, stroke_width=stroke)
    lay = Image.new("RGBA", (r - l + 4, b - t + 4), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((2 - l, 2 - t), text, font=font, fill=color, stroke_width=stroke, stroke_fill="black")
    if stretch != 1:
        lay = lay.resize((int(lay.width * stretch), lay.height), Image.LANCZOS)
    return lay, t


def main():
    a = sys.argv[1:]
    pic, out = a[0], a[1]
    opt = {"cap": 120, "x": 1240, "y": 50, "align": "right", "stretch": 1.0, "stroke": 3,
           "glow": 16, "grit": 1.0, "ramp": 0.0, "lh": 1.4}
    plate, lines, i = False, [], 2
    while i < len(a):
        if a[i] == "--plate":
            plate = True; i += 1
        elif a[i].startswith("--"):
            k = a[i][2:]; v = a[i + 1]
            opt[k] = v if k == "align" else float(v); i += 2
        else:
            segs = []
            for s in a[i].split("+"):
                t, c = s.rsplit("|", 1); segs.append((t, COL.get(c, c)))
            lines.append(segs); i += 1

    im = grit(fit_169(Image.open(pic).convert("RGB")), opt["grit"])
    if opt["ramp"] > 0:
        arr = np.asarray(im).astype(float)
        ramp = np.clip((np.arange(1280) - 700) / 400, 0, 1) * opt["ramp"]
        im = Image.fromarray((arr * (1 - ramp[None, :, None])).astype("uint8"))

    # Anton cap height is 0.86 of the font size (measured)
    size = int(opt["cap"] / 0.86)
    font = ImageFont.truetype(FONT, size)
    stroke = int(opt["stroke"])
    space = int(opt["cap"] * 0.2)  # Fossil word gap ~0.2-0.25 cap
    text = Image.new("RGBA", im.size, (0, 0, 0, 0))
    y = int(opt["y"])
    for segs in lines:
        words = [render_word(t, font, opt["stretch"], c, stroke) for t, c in segs]
        width = sum(w.width for w, _ in words) + space * (len(words) - 1)
        x = {"right": opt["x"] - width, "left": opt["x"], "center": opt["x"] - width / 2}[opt["align"]]
        top = min(t for _, t in words)
        for w, t in words:
            text.alpha_composite(w, (int(x), int(y + t - top)))
            x += w.width + space
        y += int(opt["cap"] * opt["lh"])

    alpha = text.split()[3]
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    if plate:  # dense black rounded glow behind the words
        m = alpha.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(10))
        sh.putalpha(m.point(lambda v: min(255, int(v * 1.6))))
    else:      # soft dark glow + slight drop shadow
        m = alpha.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(opt["glow"]))
        sh.putalpha(m.point(lambda v: min(255, int(v * 1.3))))
    base = Image.alpha_composite(im.convert("RGBA"), sh)
    base = Image.alpha_composite(base, text).convert("RGB")
    base.save(out, quality=95)
    base.resize((168, 94), Image.LANCZOS).save(out.rsplit(".", 1)[0] + "_168.png")


if __name__ == "__main__":
    main()
