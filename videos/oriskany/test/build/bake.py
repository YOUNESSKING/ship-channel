"""Sea-first basemaps from AWS Terrarium tiles (land + bathymetry, open data).
Writes two Web-Mercator rasters with their pixel bounds: wide Gulf (z6) and panhandle (z10)."""
import io, json, math, os, urllib.request, numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "maps"); os.makedirs(OUT, exist_ok=True)
CACHE = os.path.join(HERE, ".tiles"); os.makedirs(CACHE, exist_ok=True)
def tile(z, x, y):
    p = f"{CACHE}/{z}_{x}_{y}.png"
    if not os.path.exists(p):
        urllib.request.urlretrieve(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png", p)
    a = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
def lonlat_to_px(lon, lat, z):
    n = 256 * 2 ** z; x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y
def bake(name, z, lon0, lat0, lon1, lat1):
    x0, y0 = lonlat_to_px(lon0, lat1, z); x1, y1 = lonlat_to_px(lon1, lat0, z)
    tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int(x1 // 256), int(y1 // 256)
    H = np.vstack([np.hstack([tile(z, tx, ty) for tx in range(tx0, tx1 + 1)]) for ty in range(ty0, ty1 + 1)])
    # colour: sea by depth (deep navy -> shelf teal), land muted olive/sand with hillshade
    sea = H <= 0; d = np.clip(-H, 0, 4000)
    t = np.sqrt(d / 4000.0)[..., None]
    shallow = np.array([46, 92, 110], np.float32); deep = np.array([8, 20, 38], np.float32)
    seacol = shallow * (1 - t) + deep * t
    gy, gx = np.gradient(H); m = 1.0 if z >= 9 else 0.25
    shade = np.clip(1 + (-gx + gy) * (0.004 / m) * (2 ** (z - 6)), 0.6, 1.4)[..., None]
    e = np.clip(H / 120.0, 0, 1)[..., None]
    land = (np.array([92, 98, 72], np.float32) * (1 - e) + np.array([120, 112, 84], np.float32) * e) * shade
    seashade = np.clip(1 + (-gx + gy) * 0.0015 * (2 ** (z - 6)) / 4, 0.85, 1.15)[..., None]
    img = np.where(sea[..., None], seacol * seashade, land)
    # coastline highlight
    edge = np.asarray(Image.fromarray((sea * 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES)) > 0
    img[edge] = [196, 186, 150]
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(f"{OUT}/{name}.png")
    json.dump({"z": z, "px0": tx0 * 256, "py0": ty0 * 256, "w": H.shape[1], "h": H.shape[0]}, open(f"{OUT}/{name}.json", "w"))
    print(name, H.shape, "depth range", float(H.min()), float(H.max()))
bake("gulf_z6", 6, -98.5, 17.5, -79.0, 32.5)
bake("pan_z10", 10, -89.2, 28.9, -84.9, 31.3)
