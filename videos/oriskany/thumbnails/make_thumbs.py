"""Oriskany thumbnails: real NARA 2006 photos (public domain), crop + light grade + 1-3 true words. No AI, nothing added to the ship."""
import sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter

SRC = "/home/user/ship-channel/videos/oriskany/footage/src/photos"
OUT = sys.argv[1] if len(sys.argv) > 1 else __import__('os').path.dirname(__file__)
FONT = "/home/user/ship-channel/tools/fonts/Anton-Regular.ttf"
W, H = 1280, 720
WHITE = (246, 241, 230)
GOLD = (212, 175, 90)


def crop(img, cx, cy, frac_w):
    """Crop 16:9 centred on (cx, cy) as fractions, width = frac_w of image width."""
    iw, ih = img.size
    cw = int(iw * frac_w)
    ch = int(cw * 9 / 16)
    if ch > ih:
        ch = ih
        cw = int(ch * 16 / 9)
    x = min(max(int(iw * cx - cw / 2), 0), iw - cw)
    y = min(max(int(ih * cy - ch / 2), 0), ih - ch)
    return img.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS)


def grade(img):
    img = ImageEnhance.Contrast(img).enhance(1.15)
    img = ImageEnhance.Color(img).enhance(1.05)
    return img


def shade(img, side):
    """Soft dark gradient on one side (left/right/top) for text."""
    g = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(g)
    if side in ("left", "right"):
        for x in range(W):
            t = x / W if side == "right" else 1 - x / W
            a = max(0.0, (t - 0.35) / 0.65)
            d.line([(x, 0), (x, H)], fill=int(200 * a ** 1.3))
    else:
        for y in range(H):
            a = max(0.0, 1 - y / (H * 0.55))
            d.line([(0, y), (W, y)], fill=int(190 * a ** 1.2))
    black = Image.new("RGB", (W, H), (6, 10, 16))
    return Image.composite(black, img, g)


def text(img, lines, x, y, size, anchor="la", underline_first=False, gap=0.95):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, size)
    yy = y
    for i, ln in enumerate(lines):
        # soft shadow
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x + 4, yy + 5), ln, font=f, fill=(0, 0, 0, 200), anchor=anchor)
        img.paste(sh.filter(ImageFilter.GaussianBlur(6)), (0, 0), sh.filter(ImageFilter.GaussianBlur(6)))
        d.text((x, yy), ln, font=f, fill=WHITE, anchor=anchor)
        if underline_first and i == 0:
            bb = d.textbbox((x, yy), ln, font=f, anchor=anchor)
            d.rectangle([bb[0], bb[3] + 10, bb[2], bb[3] + 18], fill=GOLD)
        yy += int(size * gap)
    return img


def save(img, name):
    img.save(f"{OUT}/{name}.jpg", quality=92)
    img.resize((168, 94), Image.LANCZOS).save(f"{OUT}/{name}_sidebar.png")


# 1: bow standing vertical, 17 May 2006 (NARA 6698624, portrait source)
a = Image.open(f"{SRC}/nara_6698624.jpg").convert("RGB")
t1 = shade(grade(crop(a, 0.42, 0.33, 1.0)), "right")
t1 = text(t1, ["ON", "PURPOSE"], 1220, 150, 190, anchor="ra", gap=1.0)
save(t1, "thumb_A_on_purpose")

# 2: scuttling charges, smoke from the hull (NARA 6698618)
b = Image.open(f"{SRC}/nara_6698618.jpg").convert("RGB")
t2 = shade(grade(crop(b, 0.48, 0.42, 0.85)), "right")
t2 = text(t2, ["NAVY", "DID THIS"], 1230, 70, 165, anchor="ra", gap=1.0)
d = ImageDraw.Draw(t2)
f = ImageFont.truetype(FONT, 165)
bb = d.textbbox((1230, 70), "NAVY", font=f, anchor="ra")
d.rectangle([bb[0], bb[3] + 12, bb[2], bb[3] + 20], fill=GOLD)
save(t2, "thumb_B_navy_did_this")

# 3: bow slipping under (NARA 6698625)
c = Image.open(f"{SRC}/nara_6698625.jpg").convert("RGB")
t3 = shade(grade(crop(c, 0.56, 0.47, 0.80)), "top")
t3 = text(t3, ["WHY SINK HER?"], 60, 30, 165)
save(t3, "thumb_C_why_sink_her")

# feed strip: all three at sidebar size + 2x for a quick look
strip = Image.new("RGB", (3 * 336 + 40, 188 + 20), (15, 15, 15))
for i, n in enumerate(["thumb_A_on_purpose", "thumb_B_navy_did_this", "thumb_C_why_sink_her"]):
    strip.paste(Image.open(f"{OUT}/{n}.jpg").resize((336, 188), Image.LANCZOS), (10 + i * 346, 10))
strip.save(f"{OUT}/feed_strip.png")
