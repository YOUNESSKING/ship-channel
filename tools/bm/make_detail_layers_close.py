"""DETAIL TEST (owner 2026-10-30): accurate rivers, swamps and trees for a basemap, as transparent layers on the HD grid (5760x3240).
usage: python3 tools/make_detail_layers.py BASE   (BASE has assets/BASE.json + BASE_hd_lift.jpg)
Data: USGS National Hydrography (NHD: flowlines, waterbodies, areas incl. swamp/marsh) + ESA WorldCover 2021 10 m (trees, wetland, water).
Writes assets/media/BASE_det_{riv,tree,swamp}.png and assets/src/BASE_det_meta.json. NOTE: land cover is 2021, not 1863 (see report)."""
import json, math, os, sys, urllib.parse, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
import rasterio
from rasterio.windows import from_bounds
base = sys.argv[1]; S = 2
SIMPLE = os.environ.get('SIMPLE') == '1'; SUF = 'S' if SIMPLE else ''
J = json.load(open(f"assets/{base}.json")); z = J["zoom"]; ox, oy = J["origin_world_px"]; W, H = J["size"][0] * S, J["size"][1] * S
n = 256 * 2 ** z
def px2ll(i, j):
    x = ox + i / S; y = oy + j / S
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))), x / n * 360 - 180
def ll2px(lat, lon):
    return ((((lon + 180) / 360 * n) - ox) * S, (((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n) - oy) * S)
n_lat, w_lon = px2ll(0, 0); s_lat, e_lon = px2ll(W, H)
print("bounds", s_lat, w_lon, n_lat, e_lon, flush=True)
# ---- ESA WorldCover mosaic over the bounds
RES = 1 / 12000
pad = 0.002; bl, bb, br, bt = w_lon - pad, s_lat - pad, e_lon + pad, n_lat + pad
NR, NC = int(round((bt - bb) / RES)), int(round((br - bl) / RES)); WC = np.zeros((NR, NC), np.uint8)
for tl in range(math.floor(bb / 3) * 3, math.ceil(bt / 3) * 3, 3):
    for tn in range(math.floor(bl / 3) * 3, math.ceil(br / 3) * 3, 3):
        name = f"ESA_WorldCover_10m_2021_v200_{'N' if tl >= 0 else 'S'}{abs(tl):02d}{'E' if tn >= 0 else 'W'}{abs(tn):03d}_Map.tif"
        with rasterio.open("/vsicurl/https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/" + name) as ds:
            b = (max(bl, tn), max(bb, tl), min(br, tn + 3), min(bt, tl + 3))
            a = ds.read(1, window=from_bounds(*b, ds.transform))
            r0 = int(round((bt - b[3]) / RES)); c0 = int(round((b[0] - bl) / RES)); WC[r0:r0 + a.shape[0], c0:c0 + a.shape[1]] = a[:NR - r0, :NC - c0]
print("worldcover", WC.shape, dict(zip(*[x.tolist() for x in np.unique(WC, return_counts=True)])), flush=True)
# resample onto the HD grid (nearest) via per-axis lat/lon lookup (mercator: lon linear in x, lat by y)
cols = np.clip(((np.array([px2ll(i, 0)[1] for i in range(W)]) - bl) / RES).astype(int), 0, NC - 1)
rows = np.clip(((bt - np.array([px2ll(0, j)[0] for j in range(H)])) / RES).astype(int), 0, NR - 1)
CL = WC[np.ix_(rows, cols)]
# ---- NHD (USGS)
def nhd(layer, fields="FCode,FType,GNIS_Name"):
    out, off = [], 0
    while True:
        q = {"geometry": f"{w_lon},{s_lat},{e_lon},{n_lat}", "geometryType": "esriGeometryEnvelope", "inSR": 4326, "outSR": 4326, "spatialRel": "esriSpatialRelIntersects",
             "outFields": fields, "returnGeometry": "true", "f": "geojson", "resultOffset": off, "resultRecordCount": 1000}
        u = f"https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/{layer}/query?" + urllib.parse.urlencode(q)
        for k in range(4):
            try: d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "battle-maps-detail-test"}), timeout=90)); break
            except Exception as e: print("retry", layer, e, flush=True); d = None
        if not d: break
        fs = d.get("features", []); out += fs; off += len(fs)
        if len(fs) < 1000 and not d.get("exceededTransferLimit"): break
    return out
flow = nhd(6); body = nhd(12); area = nhd(9)
print("nhd flowlines", len(flow), "waterbodies", len(body), "areas", len(area), flush=True)
def polys(f):
    g = f["geometry"]
    if not g: return []
    return g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]] if g["type"] == "Polygon" else []
def lines(f):
    g = f["geometry"]
    if not g: return []
    return g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]] if g["type"] == "LineString" else []
# ---- NLCD 2021 (USGS/MRLC WMS, 30 m): woody wetland (90) + emergent herbaceous wetland (95) = swamp that WorldCover misses
NL = {11: (70, 107, 159), 21: (222, 197, 197), 22: (217, 146, 130), 23: (235, 0, 0), 24: (171, 0, 0), 31: (179, 172, 159), 41: (104, 171, 95), 42: (28, 95, 44), 43: (181, 197, 143),
      52: (204, 184, 121), 71: (223, 223, 194), 81: (220, 217, 57), 82: (171, 108, 40), 90: (184, 217, 235), 95: (112, 163, 186)}
LC = np.array(list(NL.values()), np.int32); LK = np.array(list(NL.keys()))
EXT = 20037508.342789244
def m3857(i, j): return ((ox + i / S) / n - 0.5) * 2 * EXT, (0.5 - (oy + j / S) / n) * 2 * EXT
NLW = np.zeros((H, W), bool); TW, TH = 1440, 810
import io
for tj in range(0, H, TH):
    for ti in range(0, W, TW):
        x0, y1 = m3857(ti, tj); x1, y0 = m3857(ti + TW, tj + TH)
        u = ("https://www.mrlc.gov/geoserver/mrlc_display/wms?service=WMS&version=1.1.1&request=GetMap&layers=NLCD_2021_Land_Cover_L48&styles=&srs=EPSG:3857"
             f"&bbox={x0},{y0},{x1},{y1}&width={TW}&height={TH}&format=image/png&transparent=false")
        im = None
        for k in range(4):
            try: im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "battle-maps-detail-test"}), timeout=120).read())).convert("RGB"); break
            except Exception as e: print("nlcd retry", e, flush=True)
        if im is None: continue
        a = np.array(im).astype(np.int32).reshape(-1, 3)
        idx = np.argmin(((a[:, None, :] - LC[None, :, :]) ** 2).sum(2), axis=1); cls = LK[idx].reshape(TH, TW)
        NLW[tj:tj + TH, ti:ti + TW] = (cls == 90) | (cls == 95)
print("nlcd wetland px", int(NLW.sum()), flush=True)
# ---- rivers layer
riv = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(riv)
WATER = (96, 140, 168); EDGE = (52, 80, 100)
for f in area + body:
    ft = (f["properties"].get("FType") or 0)
    if ft == 466: continue
    if SIMPLE and f in body:
        g0 = polys(f)
        if g0 and len(g0[0][0]) < 40: continue  # drop small ponds  # swamp/marsh goes to the swamp layer
    for pg in polys(f):
        for k, ring in enumerate(pg):
            pts = [ll2px(la, lo) for lo, la in ring]
            if k == 0: d.polygon(pts, fill=WATER + (235,), outline=EDGE + (255,))
for f in flow:
    p = f["properties"]; named = bool(p.get("GNIS_Name")); fc = p.get("FCode") or 46006
    if SIMPLE and not named: continue
    w = 4 if named else 2
    if fc in (46003, 46007): w = 1  # intermittent: hairline
    for ln in lines(f):
        pts = [ll2px(la, lo) for lo, la in ln]
        if len(pts) > 1: d.line(pts, fill=EDGE + (150,), width=w + 1, joint="curve"); d.line(pts, fill=WATER + (225,), width=max(w, 1), joint="curve")
riv.save(f"assets/media/{base}_det_riv{SUF}.png")
# ---- swamp layer: WorldCover herbaceous wetland (90) + NHD swamp/marsh polygons; hatched blue-green marsh pattern
sw = (CL == 90) | (CL == 95)
sm = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(sm)
for f in area + body:
    if (f["properties"].get("FType") or 0) == 466:
        for pg in polys(f): sd.polygon([ll2px(la, lo) for lo, la in pg[0]], fill=255)
sw |= np.array(sm) > 0
sw |= ndimage.binary_closing(NLW, iterations=2)
sw = ndimage.binary_opening(sw, iterations=1)
yy, xx = np.mgrid[0:H, 0:W]
def noise(sig, seed):
    r = np.random.default_rng(seed).normal(size=(H, W)).astype(np.float32); r = ndimage.gaussian_filter(r, sig); return (r - r.mean()) / (r.std() + 1e-6)
swl = np.zeros((H, W, 4), np.uint8)
swl[sw] = (70, 124, 124, 58)  # light teal wash (the trees stay visible through it)
edge = sw & ~ndimage.binary_erosion(sw, iterations=2); swl[edge] = (40, 92, 100, 150)
if SIMPLE:
    lab, nl = ndimage.label(sw); sz = ndimage.sum(sw, lab, range(1, nl + 1)); keepm = np.isin(lab, [i + 1 for i, v in enumerate(sz) if v > 12000]); sw = sw & keepm
    swl = np.zeros((H, W, 4), np.uint8); swl[sw] = (70, 124, 124, 48); e2 = sw & ~ndimage.binary_erosion(sw, iterations=2); swl[e2] = (40, 92, 100, 120)
# irregular reed marks: local maxima of noise inside the wetland, small three-stroke tufts
pk = noise(1.6, 11); mx = (pk == ndimage.maximum_filter(pk, size=15)) & (pk > 0.3) & sw & (not SIMPLE)
rim = Image.fromarray(swl); rd = ImageDraw.Draw(rim)
for y, x in zip(*np.nonzero(mx)):
    rd.line((x - 4, y + 2, x - 2, y - 3), fill=(46, 104, 110, 190), width=1); rd.line((x, y + 3, x, y - 4), fill=(52, 112, 116, 200), width=1); rd.line((x + 4, y + 2, x + 2, y - 3), fill=(46, 104, 110, 190), width=1)
    rd.line((x - 5, y + 3, x + 5, y + 3), fill=(120, 170, 150, 140), width=1)
swl = np.array(rim)
Image.fromarray(swl).save(f"assets/media/{base}_det_swamp{SUF}.png")
# ---- tree layer: canopy mottle on tree cover (10) (+ shrub 20 lighter); built-up/crop/grass left open
tree = (CL == 10)
tree = ndimage.binary_opening(tree, iterations=2)
rng = np.random.default_rng(7)
def noise_(sig, seed):
    r = np.random.default_rng(seed).normal(size=(H, W)).astype(np.float32); r = ndimage.gaussian_filter(r, sig); return (r - r.mean()) / (r.std() + 1e-6)
m = 0.6 * noise(3, 1) + 0.4 * noise(7, 2)
al = (np.clip(0.50 + 0.08 * m, 0.35, 0.65) if SIMPLE else np.clip(0.55 + 0.22 * m, 0.3, 0.85)) * ndimage.gaussian_filter(tree.astype(np.float32), 6.0 if SIMPLE else 2.0)
tl_ = np.zeros((H, W, 4), np.uint8)
g = np.clip(0.5 + 0.35 * m, 0, 1)
tl_[..., 0] = (22 + 26 * g).astype(np.uint8); tl_[..., 1] = (46 + 40 * g).astype(np.uint8); tl_[..., 2] = (24 + 22 * g).astype(np.uint8)
tl_[..., 3] = (al * (105 if SIMPLE else 150)).astype(np.uint8)
Image.fromarray(tl_).save(f"assets/media/{base}_det_tree{SUF}.png")
# crown stipple (bolder option): irregular tree crowns = local maxima of a noise field, small dark discs with a lit edge
cr = np.zeros((H, W, 4), np.uint8)
pk = noise(2.2, 5); mx = (pk == ndimage.maximum_filter(pk, size=9)) & (pk > 0.2) & tree
ys, xs = np.nonzero(mx); cim = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(cim)
for y, x in zip(ys, xs):
    r = 3 + int(rng.random() * 2)
    cd.ellipse((x - r + 1, y - r + 1, x + r + 1, y + r + 1), fill=(130, 165, 100, 55))
    cd.ellipse((x - r, y - r, x + r, y + r), fill=(14, 34, 18, 120))
cr = np.array(cim)
Image.fromarray(cr).save(f"assets/media/{base}_det_crown{SUF}.png")
json.dump({"classes": {str(k): int(v) for k, v in zip(*np.unique(CL, return_counts=True))}, "flow": len(flow), "body": len(body), "area": len(area), "swamp_px": int(sw.sum())}, open(f"assets/src/{base}_det_meta.json", "w"))
print("done", base, flush=True)
