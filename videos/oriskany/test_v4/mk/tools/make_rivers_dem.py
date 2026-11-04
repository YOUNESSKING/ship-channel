"""Rivers and streams traced from the HD elevation (water flows downhill; D8 flow accumulation with pysheds) - offline fallback for
OpenStreetMap waterways (map-detail test, owner 2026-10-06). usage: python3 tools/make_rivers_dem.py BASE
-> assets/src/BASE_dem_rivers.json: [{"order": 1|2|3, "pts": [[x, y], ...]}] in HD px (2x map px)."""
import json, sys
import numpy as np
if not hasattr(np, "in1d"): np.in1d = np.isin  # pysheds 0.5 on numpy 2
from affine import Affine
from pysheds.grid import Grid
from pysheds.sview import Raster, ViewFinder
base = sys.argv[1]
e = np.load(f"assets/src/{base}_hd_elev.npy").astype(np.float64)
land = e > 0.5
e = np.where(land, e, -50.0)  # the sea drains everything
vf = ViewFinder(affine=Affine(1, 0, 0, 0, 1, 0), shape=e.shape, nodata=-9999.0)
dem = Raster(e, viewfinder=vf); g = Grid(viewfinder=vf)
d = g.resolve_flats(g.fill_depressions(g.fill_pits(dem)))
fdir = g.flowdir(d); acc = np.asarray(g.accumulation(fdir))
out = []
for order, thr in ((1, 900), (2, 9000), (3, 60000)):
    fc = g.extract_river_network(fdir, Raster(((acc > thr) & land).astype(bool), viewfinder=ViewFinder(affine=vf.affine, shape=e.shape, nodata=False)))
    for f in fc["features"]:
        pts = f["geometry"]["coordinates"]
        if len(pts) > 3: out.append({"order": order, "pts": [[round(x, 1), round(y, 1)] for x, y in pts]})
    print("order", order, "segments", sum(1 for o in out if o["order"] == order), flush=True)
json.dump(out, open(f"assets/src/{base}_dem_rivers.json", "w"))
