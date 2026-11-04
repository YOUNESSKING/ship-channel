"""Build land masks for the territory tint (locked "E" look): assets/<map>_land.png, white = land, 2880x1620 RGBA.

usage: python3 tools/make_land.py [MAP ...]   (default: every basemap in assets/*.json; run from anywhere)
Same rule as bake.py (elev > 0.5 = land), same tiles (fetched into tools/.tiles if missing), like
goosegreen/assets/isthmus_land.png. Use as K.frontTint({ ..., mask: "assets/<map>_land.png" }).
Chosin Reservoir is ~1,070 m up (elev > 0.5), so where assets/<map>_water.png exists its water is cut out too.
"""
import glob, json, os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
sys.path.insert(0, HERE)
from bake import tile  # noqa: E402  (downloads + caches Terrarium tiles, returns elevation in m)


def build(name):
    P = json.load(open(f"{ASSETS}/{name}.json"))
    z, (x0, y0), (W, H) = P["zoom"], P["origin_world_px"], P["size"]
    tx0, ty0, tx1, ty1 = x0 // 256, y0 // 256, (x0 + W) // 256, (y0 + H) // 256
    mosaic = np.vstack([np.hstack([tile(z, tx, ty) for tx in range(tx0, tx1 + 1)]) for ty in range(ty0, ty1 + 1)])
    elev = mosaic[y0 - ty0 * 256:y0 - ty0 * 256 + H, x0 - tx0 * 256:x0 - tx0 * 256 + W]
    land = elev > P.get("sea_below", 0.5)  # same rule as bake.py (SEA_BELOW for polders)
    wp = f"{ASSETS}/{name}_water.png"
    if os.path.exists(wp):
        land &= np.asarray(Image.open(wp).convert("RGBA"))[..., 3] <= 40
    out = np.zeros((H, W, 4), np.uint8)
    out[land] = (255, 255, 255, 255)
    Image.fromarray(out, "RGBA").save(f"{ASSETS}/{name}_land.png", optimize=True)
    print(f"{name}_land.png  land {land.mean():.0%}")


if __name__ == "__main__":
    names = sys.argv[1:] or sorted(os.path.basename(p)[:-5] for p in glob.glob(f"{ASSETS}/*.json") if not p.endswith("msr_roads.json"))
    for n in names:
        build(n)
