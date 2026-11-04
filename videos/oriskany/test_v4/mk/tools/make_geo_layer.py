"""Draw OpenStreetMap geography onto a basemap as a transparent layer (map-detail test, owner 2026-10-06).
usage: python3 tools/make_geo_layer.py BASE [STYLE=ref|parchment] [SKIP="NAME1,NAME2"]
-> assets/media/BASE_geo_STYLE.png (2x: 5760x3240, shown at 2880x1620): forests (subtle), lakes, rivers + canals (width by type),
   streams (thin), villages (small dot + name) and towns (bigger); names in SKIP are left to the scene's own labels.
-> assets/media/BASE_rivers.json: simplified river polylines (map px) for the shimmer.  Data (c) OpenStreetMap contributors (ODbL)."""
import json, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
base = sys.argv[1]; style = sys.argv[2] if len(sys.argv) > 2 else "ref"; skip = set((sys.argv[3] if len(sys.argv) > 3 else "").upper().split(","))
J = json.load(open(f"assets/{base}.json")); O = json.load(open(f"assets/src/{base}_osm.json"))
z, (ox, oy), S = J["zoom"], J["origin_world_px"], 2
W, H = J["size"][0] * S, J["size"][1] * S
def P(lat, lon):
    n = 256 * 2 ** z; r = math.radians(lat); return (((lon + 180) / 360 * n - ox) * S, ((1 - math.asinh(math.tan(r)) / math.pi) / 2 * n - oy) * S)
C = {"ref": dict(forest=(34, 58, 40, 110), water=(16, 27, 34, 255), river=(96, 150, 190, 245), stream=(80, 128, 160, 150), ink=(240, 236, 226), halo=(10, 14, 16)),
     "parchment": dict(forest=(118, 128, 84, 70), water=(168, 186, 184, 255), river=(110, 140, 150, 235), stream=(110, 140, 150, 120), ink=(52, 46, 34), halo=(236, 226, 196))}[style]
im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
geom = lambda el: [P(g["lat"], g["lon"]) for g in el.get("geometry", []) if g]
# forests (filled, slightly soft), lakes
fl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fl)
for el in O.get("forest", []):
    g = geom(el)
    if len(g) > 3: fd.polygon(g, fill=C["forest"])
im.alpha_composite(fl.filter(ImageFilter.GaussianBlur(1.5)))
for el in O.get("lakes", []):
    g = geom(el)
    if len(g) > 3: d.polygon(g, fill=C["water"])
for el in O.get("streams", []):
    g = geom(el)
    if len(g) > 1: d.line(g, fill=C["stream"], width=2, joint="curve")
rivers = []
import os
if not O.get("rivers") and os.path.exists(f"assets/src/{base}_dem_rivers.json"):  # offline fallback: rivers traced from the HD elevation
    for seg in json.load(open(f"assets/src/{base}_dem_rivers.json")):
        g = [tuple(q) for q in seg["pts"]]; o = seg["order"]
        d.line(g, fill=C["stream"] if o == 1 else C["river"], width={1: 2, 2: 4, 3: 7}[o], joint="curve")
        if o == 3: sim = g[::6] + [g[-1]]; rivers.append([[round(x / S, 1), round(y / S, 1)] for x, y in sim])
for el in O.get("rivers", []):
    g = geom(el)
    if len(g) > 1:
        big = el.get("tags", {}).get("waterway") == "canal" or el.get("tags", {}).get("name", "") in ("La Vire", "L'Orne", "La Douve", "Vire", "Orne", "Douve", "La Seine", "Seine", "La Taute", "Le Merderet", "Merderet")
        d.line(g, fill=C["river"], width=6 if big else 4, joint="curve")
        sim = g[::4] + [g[-1]]; rivers.append([[round(x / S, 1), round(y / S, 1)] for x, y in sim])
json.dump(rivers, open(f"assets/media/{base}_rivers.json", "w"))
# places: villages small, towns bigger (dot + name with a soft halo)
F = "assets/fonts/oswald-latin-500-normal.woff2"
try: fv, ft = ImageFont.truetype("tools/oswald-latin-700-normal.ttf", 30), ImageFont.truetype("tools/oswald-latin-700-normal.ttf", 42)
except Exception: fv = ft = ImageFont.load_default()
txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(txt); halo = Image.new("RGBA", (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(halo)
# 1944 names: modern merged communes (2016-2019 "communes nouvelles") back to the wartime town names
HIST = {"Cherbourg-en-Cotentin": "Cherbourg", "Carentan-les-Marais": "Carentan", "Picauville": "Picauville", "Isigny-sur-Mer": "Isigny", "Formigny La Bataille": "Formigny", "Graignes-Mesnil-Angot": "Graignes", "Grandcamp-Maisy": "Grandcamp", "Le Molay-Littry": "Le Molay"}
def popn(el):
    try: return int(str(el.get("tags", {}).get("population", "0")).replace(" ", ""))
    except ValueError: return 0
pl = []
for el in O.get("places", []):
    nm = el.get("tags", {}).get("name", ""); nm = HIST.get(nm, nm)
    if not nm or nm.upper() in skip: continue
    if (nm.startswith(("St ", "Saint ")) and "-" not in nm) or (el["lon"] < -1.9 and el["lat"] < 49.55): continue  # Channel Islands (Jersey, Guernsey...)  # Channel Islands (English-style names), not part of the story
    x, y = P(el["lat"], el["lon"])
    if 0 <= x < W and 0 <= y < H: pl.append((el.get("tags", {}).get("place") in ("city", "town"), popn(el), nm, x, y))
MINPOP = int(sys.argv[5]) if len(sys.argv) > 5 else 0   # owner 2026-10-06: "just the big towns" -> towns above MINPOP, no villages (MAXV 0)
SUBURBS = {"Hérouville-Saint-Clair", "Ifs", "Mondeville", "Montivilliers"}
pl = [q for q in pl if q[0] and q[1] >= MINPOP and q[2] not in SUBURBS] if MINPOP else pl
pl.sort(key=lambda q: (not q[0], -q[1]))   # towns first, then villages by population
taken, MAXV, nv = [], int(sys.argv[4]) if len(sys.argv) > 4 else 40, 0
def free(b): return all(b[2] < a[0] or b[0] > a[2] or b[3] < a[1] or b[1] > a[3] for a in taken)
for town, pop, nm, x, y in pl:
    r = 6 if town else 4; f = ft if town else fv; lab = nm.upper() if town else nm
    tb = td.textbbox((x + r + 6, y), lab, font=f, anchor="lm"); b = (tb[0] - 10, tb[1] - 8, tb[2] + 10, tb[3] + 8)
    show = (town or nv < MAXV) and free(b) and free((x - r - 8, y - r - 8, x + r + 8, y + r + 8))
    if show:
        td.ellipse((x - r, y - r, x + r, y + r), fill=C["ink"] + (235,)); hd.ellipse((x - r - 2, y - r - 2, x + r + 2, y + r + 2), fill=C["halo"] + (170,))
        taken.append(b); nv += 0 if town else 1
        hd.text((x + r + 6, y), lab, font=f, fill=C["halo"] + (220,), anchor="lm"); td.text((x + r + 6, y), lab, font=f, fill=C["ink"] + (240 if town else 225,), anchor="lm")
halo = halo.filter(ImageFilter.GaussianBlur(4))
im.alpha_composite(halo); im.alpha_composite(txt)
out = f"assets/media/{base}_geo_{style}.png"; im.save(out, optimize=True)
print("wrote", out, {k: len(O.get(k, [])) for k in ("places", "rivers", "lakes", "streams", "forest")}, "river paths", len(rivers))
