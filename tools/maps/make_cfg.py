import json, sys
for i in sys.argv[1:]:
    J = json.load(open(f"assets/{i}_lgm.json"))
    open(f"scenes-src/_cfg_{i}.js", "w").write(f'const CFG = {{ id: "{i}", zoom: {J["zoom"]}, ox: {J["origin_world_px"][0]}, oy: {J["origin_world_px"][1]}, mpp: {J["meters_per_px"]}, credit: "Terrain: Mapzen / AWS Terrain Tiles" }};\n')
