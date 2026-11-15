"""Hook hero: THEN / NOW wipe. 1936 Army Air Corps aerial of Mallows Bay (NARA 18-AA-70-44, rotated 90 deg so north is up) wiping into
today's USGS/USDA NAIP orthophoto of the same shoreline (same diagonal shore, same creek). Slow push on both; a white divider sweeps
left -> right; labels 1936 / TODAY (Oswald, white, dark scrim). Out: segments/h_c01_thennow.mp4 (DUR s, 30 fps)."""
import os, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE)
PH = os.path.join(FULL, "../footage/src/photos"); FONT = os.path.join(FULL, "mk/tools/oswald-latin-700-normal.ttf")
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0; FPS = 30; W, H = 1920, 1080; S = 1.12
a = Image.open(os.path.join(PH, "aerial_1936_full.jpg")).rotate(90, expand=True).crop((60, 400, 2240, 1626)).convert("RGB")
A = ImageEnhance.Contrast(a.resize((int(W * S), int(H * S)), Image.LANCZOS)).enhance(1.15)
b = Image.open(os.path.join(PH, "naip_mallows_bay_008.jpg")).convert("RGB").crop((1300, 0, 3840, 1430)).resize((int(W * S), int(H * S)), Image.LANCZOS)
bb = np.asarray(b, float); lo, hi = np.percentile(bb, 0.5), np.percentile(bb, 99.7); B = Image.fromarray((((bb - lo) / (hi - lo)).clip(0, 1) ** 1.05 * 255).astype("uint8"))
f = ImageFont.truetype(FONT, 72)
def label(d, x, y, t):
    bx = d.textbbox((x, y), t, font=f); d.rectangle((bx[0] - 18, bx[1] - 10, bx[2] + 18, bx[3] + 12), fill=(10, 14, 20, 200)); d.text((x, y), t, font=f, fill=(245, 242, 234))
ease = lambda u: 0.5 - 0.5 * np.cos(np.pi * min(1, max(0, u)))
out = os.path.join(FULL, "segments/h_c01_thennow.mp4")
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "medium", out], stdin=subprocess.PIPE)
N = int(round(DUR * FPS)); w0, w1 = 0.26 * DUR, 0.52 * DUR
for i in range(N):
    t = i / FPS; z = 1 + 0.06 * t / DUR                       # slow push
    def frame(img):
        cw, ch = int(W * S / z), int(H * S / z); x0 = (img.width - cw) // 2; y0 = (img.height - ch) // 2
        return img.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
    fa, fb = frame(A), frame(B); k = ease((t - w0) / (w1 - w0)); xw = int(k * W)
    im = fa.copy(); im.paste(fb.crop((0, 0, xw, H)), (0, 0)) if xw > 0 else None
    d = ImageDraw.Draw(im, "RGBA")
    if 0 < xw < W: d.rectangle((xw - 3, 0, xw + 3, H), fill=(245, 242, 234, 235))
    if xw < W - 260: label(d, max(xw + 40, 60), 900, "1936")
    if xw > 300: label(d, 60, 900, "TODAY")
    p.stdin.write(im.tobytes())
p.stdin.close(); p.wait(); print("wrote", out, DUR)
