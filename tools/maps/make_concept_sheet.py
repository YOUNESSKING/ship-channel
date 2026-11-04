import glob, sys
from PIL import Image, ImageDraw, ImageFont
d = sys.argv[1]; out = sys.argv[2]
fs = sorted(glob.glob(d + "/frame-0[0-5]-*.png"))
W, H = 960, 540; sh = Image.new("RGB", (W*2, H*3), (10, 12, 16)); dr = ImageDraw.Draw(sh)
f = ImageFont.truetype("assets/fonts/../../tools/oswald-latin-700-normal.ttf", 22)
for i, p in enumerate(fs):
    sh.paste(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS), ((i % 2)*W, (i//2)*H))
    dr.text(((i % 2)*W + 14, (i//2)*H + H - 36), f"ice progress p = {i*0.2:.1f}", font=f, fill=(255, 235, 150))
sh.save(out, quality=90)
