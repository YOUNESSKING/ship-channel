#!/usr/bin/env python3
"""Makes lib/world_inset.json: the little world map (land + approximate Ice Age ice sheets) used by map_clip "inset" (rule 18).
Land = Natural Earth 110m (public domain), downloaded once. Ice sheets = hand-placed rough outlines of the last glacial maximum (like maps/tools/make_ice.py).
   python3 make_world_inset.py [ne_110m_land.geojson]"""
import json, os, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'demo', 'work', 'ne_110m_land.geojson')
URL = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson'
if not os.path.exists(SRC):
    os.makedirs(os.path.dirname(SRC), exist_ok=True); open(SRC, 'wb').write(urllib.request.urlopen(URL).read())
LAT0, LAT1 = 86.0, -60.0           # top and bottom latitude of the inset; x = lon + 180, y = LAT0 - lat  (1 unit = 1 degree)
W, H = 360, int(LAT0 - LAT1)
def P(lat, lon): return (lon + 180.0, LAT0 - lat)
def rdp(pts, eps):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]; dx, dy = x2 - x1, y2 - y1; n = (dx * dx + dy * dy) ** .5 or 1e-9
    best, bi = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
        if d > best: best, bi = d, i
    if best <= eps: return [pts[0], pts[-1]]
    return rdp(pts[:bi + 1], eps)[:-1] + rdp(pts[bi:], eps)
def path(rings, eps=0.45):
    out = []
    for r in rings:
        pp = [P(la, lo) for la, lo in r]
        if pp[0] == pp[-1]: pp = pp[:-1]
        k = max(range(len(pp)), key=lambda i: (pp[i][0] - pp[0][0]) ** 2 + (pp[i][1] - pp[0][1]) ** 2)
        pts = rdp(pp[:k + 1], eps)[:-1] + rdp(pp[k:] + [pp[0]], eps)[:-1]
        if len(pts) >= 3: out.append('M' + 'L'.join(f'{x:.0f},{y:.0f}' for x, y in pts) + 'Z')
    return ''.join(out)
def path_old(rings):
    d = []
    for r in rings:
        pts = [P(la, lo) for la, lo in r]
        d.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z')
    return ''.join(d)
land = []
for f in json.load(open(SRC))['features']:
    g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    for poly in polys:
        ring = poly[0]
        if all(lat < LAT1 - 1 for lon, lat in ring): continue
        land.append([(max(lat, LAT1), lon) for lon, lat in ring[::1]])
# last glacial maximum ice sheets, (lat, lon) outlines, rough
ICE = {
 'north_america': [(48,-123),(48,-112),(46,-100),(41.5,-93),(39,-88),(39.5,-84),(40.5,-80.5),(41.2,-76.5),(40.6,-73),(41.3,-68),(42.6,-65),(43.4,-62.5),(44.6,-58.5),(46.6,-55.5),(47.6,-52.2),(50,-52.2),(53,-52),(56,-54.2),(59,-57),(61.5,-61),(62.5,-65),(64.5,-62.5),(66.5,-61.5),(69,-62.5),(72,-67),(74.5,-72),(77,-78),(80,-85),(82,-100),(80,-112),(76,-118),(72,-122),(69,-130),(66,-138),(63,-143),(61,-148),(59,-141),(57,-136),(54,-132),(51,-128)],
 'greenland': [(59.6,-44.5),(60.4,-49.5),(63,-53.8),(66,-56.6),(69,-59.8),(72,-63.5),(75,-67),(79,-70),(83,-60),(83,-20),(79,-10),(75.5,-10),(72.5,-14),(70,-22),(67.5,-28),(65,-33),(63,-38),(61,-42.5)],
 'british_irish': [(51.6,-9.8),(52.8,-12.3),(54.6,-13.2),(56.6,-10.8),(58.6,-9.2),(60.2,-5.2),(61.2,-1),(60.2,2.5),(58.2,2.8),(56.6,2),(55.3,1.3),(54,0.4),(52.9,1.2),(52.4,-0.5),(52,-2.6),(51.8,-4.8),(51.3,-6.8),(51.3,-8.3)],
 'fennoscandia': [(58.5,3.5),(61,3),(63.5,4.8),(66,7.5),(68.5,10.5),(71,14.5),(74.5,17),(77,18),(80,25),(80,60),(75,95),(72,100),(70,90),(68,70),(68.5,50),(66,48.5),(63,45),(60.5,39),(57.5,34),(55,30.5),(53.2,26),(52.4,20.5),(52.2,15.5),(53.2,11.2),(54.6,9.6),(56.4,8.6),(57.3,6),(57.8,4.5)],
 'alps': [(45.4,6),(46.6,8),(47.6,11),(47.6,14.5),(46.6,14.5),(45.8,12),(45.3,8.5)],
 'patagonia': [(-37,-72),(-40,-72.8),(-44,-73.6),(-48,-75),(-52,-74.5),(-55.5,-70),(-54.5,-66),(-51,-69),(-47,-71.5),(-42,-71),(-39,-70.8)],
 'tibet': [(31,76),(34,80),(35,88),(33,95),(30,98),(28,92),(27.5,84),(29,78)],
 'siberia': [(68,88),(70,96),(71.5,106),(70,112),(67,108),(66,98),(66.5,90)],
 'new_zealand': [(-41,172),(-42.5,171),(-44.5,168),(-46,166.5),(-45,170),(-43,172.5)],
}
out = {'w': W, 'h': H, 'lat0': LAT0, 'land': path(land), 'ice': {k: path([v]) for k, v in ICE.items()}}
json.dump(out, open(os.path.join(HERE, 'lib', 'world_inset.json'), 'w'), separators=(',', ':'))
print('lib/world_inset.json', os.path.getsize(os.path.join(HERE, 'lib', 'world_inset.json')), 'bytes', len(land), 'land rings')
