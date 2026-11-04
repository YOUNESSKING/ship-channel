"""PNG previews of every SVG in kit/ship/svg (cairosvg, 640 px wide, transparent) -> kit/ship/preview/png/.
Run after `node kit/ship/make_svgs.js`."""
import glob, os, cairosvg
HERE = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(HERE, "preview", "png"); os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(os.path.join(HERE, "svg", "*.svg"))):
    cairosvg.svg2png(url=f, write_to=os.path.join(out, os.path.basename(f)[:-4] + ".png"), output_width=640)
print("wrote", len(os.listdir(out)), "PNGs to", out)
