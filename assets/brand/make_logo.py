"""Channel logo: "Fleet's End" (@FleetsEnd). Icon = a carrier's bow rising out of the sea as she goes under
(the channel's signature image, from the Oriskany F1 thumbnail), drawn flat so it reads at 48 px.
Outputs: avatar 800x800 (YouTube profile, shown as a circle), wordmark 1600x400, banner 2560x1440."""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ANTON = os.path.join(ROOT, "tools", "fonts", "Anton-Regular.ttf")
OSWALD = os.path.join(ROOT, "tools", "maps", "oswald-latin-700-normal.ttf")
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE
NAME = os.environ.get("CHANNEL_NAME", "FLEET'S END")

NAVY = (9, 19, 32)
SEA_TOP = (36, 92, 140)
SEA_BOT = (12, 40, 70)
HULL = (236, 232, 222)
RED = (224, 53, 43)
GOLD = (212, 175, 90)


def carrier_layer(L):
    """Side profile of an Essex-class carrier (bow right): flight deck, hull, island, mast. RGBA, bow at right."""
    H = int(L * 0.58)
    lay = Image.new("RGBA", (L, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    dk = int(H * 0.52)                  # flight deck height
    th = max(3, L // 55)                # deck thickness
    # hull: below the deck, bow raked forward, stern square
    hull = [(L * 0.04, dk + th), (L * 0.97, dk + th), (L * 0.90, H * 0.92), (L * 0.10, H * 0.92)]
    d.polygon(hull, fill=(178, 184, 190, 255))
    # flight deck (overhangs both ends)
    d.rectangle([0, dk, L, dk + th], fill=HULL + (255,))
    # island + funnel + mast (starboard side, a bit forward of midships)
    ix = L * 0.56
    d.rectangle([ix, dk - H * 0.20, ix + L * 0.10, dk], fill=HULL + (255,))
    d.rectangle([ix + L * 0.02, dk - H * 0.30, ix + L * 0.075, dk - H * 0.20], fill=HULL + (255,))
    d.line([(ix + L * 0.05, dk - H * 0.30), (ix + L * 0.05, dk - H * 0.48)], fill=HULL + (255,), width=max(2, L // 140))
    d.line([(ix + L * 0.025, dk - H * 0.40), (ix + L * 0.075, dk - H * 0.40)], fill=HULL + (255,), width=max(2, L // 160))
    return lay


def icon(size):
    """Square icon art (shown inside a circle): an aircraft carrier going down stern-first."""
    s = size
    im = Image.new("RGBA", (s, s), NAVY + (255,))
    wl = int(s * 0.62)  # waterline
    ship = carrier_layer(int(s * 0.80)).rotate(22, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(ship, (int(s * 0.07), int(wl - ship.height * 0.80)))
    d = ImageDraw.Draw(im)
    # sea drawn over the ship, so the stern is under water
    for y in range(wl, s):
        t = (y - wl) / (s - wl)
        c = tuple(int(SEA_TOP[i] * (1 - t) + SEA_BOT[i] * t) for i in range(3))
        d.line([(0, y), (s, y)], fill=c + (255,))
    d.rectangle([0, wl - s * 0.010, s, wl + s * 0.010], fill=RED + (255,))
    for k, (x0, x1) in enumerate([(0.14, 0.40), (0.58, 0.86), (0.30, 0.70)]):
        y = wl + s * (0.08 + 0.07 * k)
        d.line([(s * x0, y), (s * x1, y)], fill=(170, 200, 225, 255), width=max(2, s // 140))
    return im.convert("RGB")


def circle_mask(size):
    m = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(m).ellipse([0, 0, size * 4 - 1, size * 4 - 1], fill=255)
    return m.resize((size, size), Image.LANCZOS)


def avatar():
    s = 800
    im = icon(s)
    # thin gold ring, inside YouTube's circle crop
    ring = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([18, 18, s - 18, s - 18], outline=GOLD + (255,), width=10)
    im = Image.alpha_composite(im.convert("RGBA"), ring)
    im.convert("RGB").save(f"{OUT}/logo_avatar_800.png")
    # circular preview with transparency + small sizes YouTube actually shows
    c = im.copy()
    c.putalpha(circle_mask(s))
    c.save(f"{OUT}/logo_avatar_round.png")
    prev = Image.new("RGB", (800 + 40, 260), (255, 255, 255))
    x = 20
    for px in (176, 98, 48, 24):
        t = c.resize((px, px), Image.LANCZOS)
        prev.paste(t, (x, 20), t)
        x += px + 40
    dark = Image.new("RGB", (prev.width, 260), (15, 15, 15))
    x = 20
    for px in (176, 98, 48, 24):
        t = c.resize((px, px), Image.LANCZOS)
        dark.paste(t, (x, 20), t)
        x += px + 40
    both = Image.new("RGB", (prev.width, 520))
    both.paste(prev, (0, 0))
    both.paste(dark, (0, 260))
    both.save(f"{OUT}/logo_sizes_preview.png")


def wordmark(w=1600, h=400, bg=NAVY):
    im = Image.new("RGB", (w, h), bg)
    ic = icon(h - 60)
    m = circle_mask(h - 60)
    im.paste(ic, (30, 30), m)
    ImageDraw.Draw(im).ellipse([30, 30, h - 30, h - 30], outline=GOLD, width=max(3, h // 80))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(ANTON, int(h * 0.42))
    word = NAME.split(" ")
    x = h + 10
    y = int(h * 0.62)
    d.text((x, y), word[0], font=f, fill=(255, 255, 255), anchor="ls")
    x2 = x + d.textlength(word[0] + " ", font=f)
    d.text((x2, y), " ".join(word[1:]), font=f, fill=RED, anchor="ls")
    sub = ImageFont.truetype(OSWALD, int(h * 0.11))
    d.text((x + 4, int(h * 0.84)), "WHAT HAPPENED TO THE SHIPS", font=sub, fill=GOLD, anchor="ls")
    return im


def banner():
    W, H = 2560, 1440
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    for y in range(int(H * 0.62), H):
        t = (y - H * 0.62) / (H * 0.38)
        c = tuple(int(SEA_TOP[i] * (1 - t) + SEA_BOT[i] * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    # the safe area for all devices is the centre 1546 x 423
    wm = wordmark(1546, 386, bg=NAVY)
    im.paste(wm, ((W - 1546) // 2, int(H * 0.62) - 386 - 14))
    d.rectangle([0, int(H * 0.62) - 4, W, int(H * 0.62) + 4], fill=RED)
    im.save(f"{OUT}/banner_2560x1440.png")


avatar()
wordmark().save(f"{OUT}/logo_wordmark.png")
banner()
