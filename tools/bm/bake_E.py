"""Bake the owner-approved balanced detail look "E" (owner 2026-10-30) into the basemaps: assets/<m>_hd_lift.jpg = plain + treeS + swampS + rivS.
Keeps assets/<m>_hd_lift_plain.jpg as the backup (the plain basemap is always the source). usage: python3 tools/bake_E.py [map ...] [--preview]"""
import os, shutil, sys
from PIL import Image
M = "assets/media/"
maps = [a for a in sys.argv[1:] if not a.startswith("--")] or ["ga", "chatt", "corridor", "tunnel", "ringgold", "pickett"]
for m in maps:
    plain = f"assets/{m}_hd_lift_plain.jpg"
    if not os.path.exists(plain): shutil.copy(f"assets/{m}_hd_lift.jpg", plain)
    im = Image.open(plain).convert("RGBA")
    for l in ("treeS", "swampS", "rivS"): im = Image.alpha_composite(im, Image.open(M + f"{m}_det_{l}.png").convert("RGBA").resize(im.size))
    out = f"build/E-preview-{m}.jpg" if "--preview" in sys.argv else f"assets/{m}_hd_lift.jpg"
    im.convert("RGB").save(out, quality=92); print(out, im.size)
