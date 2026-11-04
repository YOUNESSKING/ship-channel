#!/usr/bin/env python3
"""make_ice.py BASENAME  -> assets/media/ice_<sheet>.png (transparent 2880x1620, one per ice sheet) + ice_edges.json
Hand-placed, APPROXIMATE lat/lon outlines of the ice sheets ~20,000 years ago (Last Glacial Maximum), from general
knowledge of LGM extent (not a dataset). Edit POLYS to reuse for other sheets/periods. Uses assets/<BASENAME>.json projection."""
import sys, os, json, math, zlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt, gaussian_filter, zoom as ndzoom
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, "assets", sys.argv[1] + ".json")))
W, H = P["size"]; Z = P["zoom"]; ox, oy = P["origin_world_px"]; N = 256*2**Z
def px(lat, lon):
    return ((lon+180)/360*N - ox, (1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*N - oy)

POLYS = {  # (lat, lon) clockwise-ish; points beyond the frame are fine (clipped)
 "laurentide": [(48,-112),(46,-100),(41.5,-93),(39,-88),(39.5,-84),(40.5,-80.5),(41.2,-76.5),(40.6,-73),(41.3,-68),
                (42.6,-65),(43.4,-62.5),(44.6,-58.5),(46.6,-55.5),(47.6,-52.2),(50,-52.2),(53,-52),(56,-54.2),(59,-57),
                (61.5,-61),(62.5,-65),(64.5,-62.5),(66.5,-61.5),(69,-62.5),(72,-67),(74.5,-72),(77,-78),(80,-85),(80,-112)],
 "greenland":  [(59.6,-44.5),(60.4,-49.5),(63,-53.8),(66,-56.6),(69,-59.8),(72,-63.5),(75,-67),(79,-70),(83,-60),(83,-20),
                (79,-10),(75.5,-10),(72.5,-14),(70,-22),(67.5,-28),(65,-33),(63,-38),(61,-42.5)],
 "iceland":    [(63.3,-24.4),(63.2,-20),(63.5,-15.5),(64.4,-12.8),(65.8,-12.5),(66.7,-15.5),(66.9,-20),(66.6,-24.5),(65.5,-25.2),(64.4,-24.9)],
 "british":    [(51.6,-9.8),(52.8,-12.3),(54.6,-13.2),(56.6,-10.8),(58.6,-9.2),(60.2,-5.2),(61.2,-1),(60.2,2.5),(58.2,2.8),
                (56.6,2),(55.3,1.3),(54,0.4),(52.9,1.2),(52.4,-0.5),(52,-2.6),(51.8,-4.8),(51.3,-6.8),(51.3,-8.3)],
 "fenno":      [(58.5,3.5),(61,3),(63.5,4.8),(66,7.5),(68.5,10.5),(71,14.5),(74.5,17),(77,18),(80,25),(80,60),(75,60),(71,56),
                (68.5,50),(66,48.5),(63,45),(60.5,39),(57.5,34),(55,30.5),(53.2,26),(52.4,20.5),(52.2,15.5),(53.2,11.2),(54.6,9.6),
                (56.4,8.6),(57.3,6),(57.8,4.5)],
}
SEA_ICE = [(46.5,-56),(45.5,-49),(45,-42),(45.5,-34),(47,-27),(49,-21),(52,-15.5),(56,-13.5),(60,-11.5),(63,-10),(66.5,-8),(69.5,-3)]  # winter edge, rough

def chaikin(pts, n):   # closed Catmull-Rom (interpolating) spline, 2**n samples per segment
    pts = list(pts); L = len(pts); out = []; M = 2**n
    for i in range(L):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[(i+1) % L], pts[(i+2) % L]
        for j in range(M):
            t = j/M; t2, t3 = t*t, t*t*t
            out.append(tuple(0.5*((2*p1[c]) + (-p0[c]+p2[c])*t + (2*p0[c]-5*p1[c]+4*p2[c]-p3[c])*t2 + (-p0[c]+3*p1[c]-3*p2[c]+p3[c])*t3) for c in range(2)))
    return out
def wobble(pts, amp, seed):
    rng = np.random.default_rng(seed); n = len(pts)
    off = gaussian_filter(rng.normal(0, 1, n), 10, mode="wrap"); off = off/off.std()*amp
    out = []
    for i, (x, y) in enumerate(pts):
        a, b = pts[i-1], pts[(i+1) % n]; tx, ty = b[0]-a[0], b[1]-a[1]; l = math.hypot(tx, ty) or 1
        out.append((x - ty/l*off[i], y + tx/l*off[i]))
    return out
def fbm(h, w, seed, scales=(220, 90, 40)):
    rng = np.random.default_rng(seed); o = np.zeros((h, w), np.float32)
    for i, s in enumerate(scales):
        g = rng.normal(0, 1, (h//s+3, w//s+3)).astype(np.float32)
        o += ndzoom(g, s, order=3)[:h, :w] / (2**i)
    return o/ o.std()
tex = fbm(H, W, 3)
out = os.path.join(ROOT, "assets", "media"); os.makedirs(out, exist_ok=True)
allim = Image.new("RGBA", (W, H), (0, 0, 0, 0)); info = {}
SS = 2
for k, poly in POLYS.items():
    pts = chaikin([px(*p) for p in poly], 4)
    pts = wobble(pts, 5 if k != "iceland" else 2, zlib.crc32(k.encode()) % 1000)
    m = Image.new("L", (W*SS, H*SS), 0); ImageDraw.Draw(m).polygon([(x*SS, y*SS) for x, y in pts], fill=255)
    m = np.asarray(m.resize((W, H), Image.LANCZOS), np.float32)/255
    ins = m > 0.5
    d = distance_transform_edt(ins)
    a = 0.46 + 0.36*(1-np.exp(-d/(60 if k != "iceland" else 14)))
    a = a*(0.93+0.07*np.tanh(tex)) + np.where(d < 3, 0.22, 0)*ins
    a = np.clip(a, 0, 0.93)*gaussian_filter(m, 0.8)
    t = np.clip(d/90, 0, 1)[..., None]
    rgb = (1-t)*np.array([196, 224, 242]) + t*np.array([238, 247, 255])
    rgb = rgb + 6*np.tanh(tex)[..., None]
    im = np.dstack([np.clip(rgb, 0, 255), a*255]).astype(np.uint8)
    Image.fromarray(im, "RGBA").save(os.path.join(out, f"ice_{k}.png"))
    allim.alpha_composite(Image.fromarray(im, "RGBA"))
    xs, ys = zip(*pts); info[k] = {"centroid": [sum(xs)/len(xs), sum(ys)/len(ys)], "bbox": [min(xs), min(ys), max(xs), max(ys)]}
allim.save("/tmp/ice_all.png")
info["sea_ice_edge"] = [list(px(*p)) for p in chaikin_open(SEA_ICE) ] if False else [list(px(*p)) for p in SEA_ICE]
json.dump(info, open(os.path.join(out, "ice_edges.json"), "w"), indent=1)
print({k: [round(v) for v in i["centroid"]] for k, i in info.items() if k != "sea_ice_edge"})
