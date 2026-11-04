#!/usr/bin/env python3
"""bake_polar.py NAME [EXAG]  (NEW, not in the kit) - SOUTH-POLAR stereographic dark relief from AWS Terrarium tiles (z5), for Antarctica.
Web-Mercator tiles cannot show a pole, so the elevation is re-projected: r = 2R*tan(colat/2) (2R = 2170.5 px at 2880 scale), 0 deg lon up, east clockwise.
Writes assets/NAME_hd_ref.jpg (5760x3240, shown at 2880x1620) + assets/NAME.json {"proj":"polar_south",...}. Antarctica gets an ice grade."""
import sys, os, json, math
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bake import tile
name = sys.argv[1]; exag = float(sys.argv[2]) if len(sys.argv) > 2 else 2.5
Z = 5; N = 256*2**Z; S = 2; W, H = 2880*S, 1620*S; CX, CY = 1440, 810; TWO_R = 790/math.tan(math.radians(20))
from concurrent.futures import ThreadPoolExecutor
rows = list(range(14, 32)); cols = list(range(32))
with ThreadPoolExecutor(12) as ex:
    tl = list(ex.map(lambda a: tile(Z, a[0], a[1]).astype(np.float32), [(x, y) for y in rows for x in cols]))
mos = np.vstack([np.hstack(tl[i*32:(i+1)*32]) for i in range(len(rows))]); y_off = rows[0]*256
jj, ii = np.mgrid[0:H, 0:W].astype(np.float32)
dx = (ii+0.5)/S - CX; dy = (jj+0.5)/S - CY; r = np.hypot(dx, dy)
colat = 2*np.arctan(r/TWO_R); lon = np.degrees(np.arctan2(dx, -dy)); lat = -90 + np.degrees(colat)
wx = ((lon+180)/360*N) % N; wy = (1-np.arcsinh(np.tan(np.radians(lat)))/math.pi)/2*N
wy = np.clip(wy, y_off, N-1.01) - y_off
elev = ndimage.map_coordinates(mos, [wy, wx], order=1, mode="nearest").astype(np.float32)
# Terrarium holds BEDROCK under Antarctica (West Antarctica < 0 m), so the ice sheet is taken as everything shallower than the shelf edge (~ -450 m),
# which is also what the LGM ice sheet did. The cap beyond the Mercator limit (lat < -85) is filled with a plateau.
cap = np.clip((-lat - 80)/4, 0, 1)
elev = elev*(1-cap) + 2400*cap
# Antarctic land + ice-shelf outline from Natural Earth 10m (public domain): assets/src/ne/ne_10m_land.geojson
from PIL import ImageDraw
def proj_ring(ring):
    out = []
    for lo, la in ring:
        if la > -55: continue
        c = math.radians(90 + la); r = TWO_R*math.tan(c/2); l = math.radians(lo)
        out.append(((CX + r*math.sin(l))*S, (CY - r*math.cos(l))*S))
    return out
mk = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(mk)
for ft in json.load(open("assets/src/ne/ne_10m_land.geojson"))["features"]:
    g = ft["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    for poly in polys:
        if min(pt[1] for pt in poly[0]) > -60: continue
        dr.polygon(proj_ring(poly[0]), fill=255)
        for hole in poly[1:]: dr.polygon(proj_ring(hole), fill=0)
for ft in json.load(open("assets/src/ne/ne_10m_antarctic_ice_shelves_polys.geojson"))["features"]:
    g = ft["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    for poly in polys:
        dr.polygon(proj_ring(poly[0]), fill=255)
icesheet = ndimage.binary_closing(np.asarray(mk) > 127, iterations=3)
dist = ndimage.distance_transform_edt(icesheet)
dome = np.clip(dist/ (0.9*dist.max()), 0, 1)**0.7*2900                 # synthetic ice-sheet dome (m) from distance to the coast
rough = ndimage.gaussian_filter(np.maximum(elev, 0), 14)*0.6                # mountain ranges from the DEM (Transantarctics, Peninsula)
elev = np.where(icesheet, dome + rough + 30, np.where(elev > 0.5, elev, np.minimum(elev, -5)))
mpp = (6371000*(1+np.cos(colat))/(TWO_R/2)/S).astype(np.float32)
land = (elev > 0.5) | icesheet; le = np.where(land, np.maximum(elev, 0), 0)
sm = ndimage.gaussian_filter(le, 1.2); gy, gx = np.gradient(sm*exag, 1.0); gx /= mpp; gy /= mpp
# rotate gradient into screen axes is not needed: gx, gy are already screen-space (image pixels)
slope, aspect = np.arctan(np.hypot(gx, gy)), np.arctan2(-gx, gy)
def shade(az, alt):
    az, alt = math.radians(az), math.radians(alt)
    return np.clip(np.sin(alt)*np.cos(slope) + np.cos(alt)*np.sin(slope)*np.cos(az-aspect), 0, 1)
hs = 0.45*shade(315, 38) + 0.25*shade(260, 45) + 0.18*shade(15, 50) + 0.12*shade(135, 60)
ao = np.clip((ndimage.gaussian_filter(le, 18) - le)/40, -1, 1)
light = np.clip(0.42 + 0.72*hs - 0.18*np.clip(ao, 0, 1) + 0.08*np.clip(-ao, 0, 1), 0, 1.25)
hi = max(np.percentile(le[land], 99.5), 1); t = np.clip(le/hi, 0, 1)
a = np.clip(light*0.85 + t*0.12, 0, 1)**1.15
dark, lite = np.array([16, 22, 22], np.float32), np.array([138, 154, 140], np.float32)
rgb = dark + (lite-dark)*a[..., None]
ice = (lat < -60) & land                                       # Antarctica: cold white-blue ice grade
_k = (np.clip((ndimage.gaussian_filter(light, 3)-0.32)*1.25 + 0.2*t, 0, 1)**1.1)[..., None]
icol = np.array([96, 124, 158], np.float32) + (np.array([240, 247, 255], np.float32)-np.array([96, 124, 158], np.float32))*_k
rgb = np.where(ice[..., None], icol, rgb)
coast = ndimage.gaussian_filter(land.astype(np.float32), 2.0)[..., None]
dd = np.clip(-elev/4500, 0, 1)[..., None]**0.6
sea_c = np.array([30, 52, 62], np.float32)*(1-dd) + np.array([9, 16, 24], np.float32)*dd
halo = ndimage.gaussian_filter(land.astype(np.float32), 8)[..., None]*(1-coast)
sea_c = sea_c + halo*np.array([14, 26, 28], np.float32)
rgb = sea_c*(1-coast) + rgb*coast
rng = np.random.default_rng(218); g = np.asarray(Image.fromarray(rng.normal(128, 40, (H//2, W//2)).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32)
rgb = rgb + (g[..., None]-128)*0.07
os.makedirs("assets", exist_ok=True)
Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).save(f"assets/{name}_hd_ref.jpg", quality=90)
np.save(f"assets/src/{name}_hd_elev.npy", elev); np.save(f"assets/src/{name}_hd_ice.npy", icesheet.astype(np.uint8))
json.dump({"name": name, "proj": "polar_south", "center_px": [CX, CY], "two_r": TWO_R, "size": [2880, 1620], "hd_scale": S, "sea_level": 0.0,
           "meters_per_px": 5870.0, "credit": "Terrain: Mapzen / AWS Terrain Tiles (open data)"}, open(f"assets/{name}_hd_ref.json", "w"), indent=1)
print("wrote", name)
