import json, math, sys, os, urllib.request
from concurrent.futures import ThreadPoolExecutor
cfg = [("beringia",63,-175,6),("doggerland",55,4,6),("black_sea",43.5,34,7),("mediterranean",40.2,4,7),("red_sea",20.5,40,6),("carpentaria",-9,140,6),("gulf_mexico",26.5,-88,7),("sundaland",2,108,6),("world",25,80,4)]
need = set()
for n, la, lo, z in cfg:
    N = 256*2**z; cx = (lo+180)/360*N; cy = (1-math.asinh(math.tan(math.radians(la)))/math.pi)/2*N
    x0, y0 = int(cx-1440), int(cy-810); z2 = z+1; x0, y0 = x0*2, y0*2
    for ty in range(y0//256, (y0+3240)//256+1):
        for tx in range(x0//256, (x0+5760)//256+1): need.add((z2, tx % 2**z2, ty))
def get(a):
    z, x, y = a; f = f"tools/.tiles/{z}_{x}_{y}.png"
    if os.path.exists(f): return
    for _ in range(3):
        try: open(f, "wb").write(urllib.request.urlopen(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png", timeout=30).read()); return
        except Exception: pass
os.makedirs("tools/.tiles", exist_ok=True)
with ThreadPoolExecutor(16) as ex: list(ex.map(get, sorted(need)))
print("prefetched", len(need))
