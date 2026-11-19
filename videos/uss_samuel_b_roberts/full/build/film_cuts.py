"""Scene cuts of every source film used in beats.FILMS (ffmpeg scdet), cached in build/film_cuts.json.
make_shotlists splits every FILMS window at these cuts (pieces < 1.6 s dropped), so a shot never crosses a cut."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from beats import FILMS
FT = os.path.join(HERE, "../../footage/src/film"); OUT = os.path.join(HERE, "film_cuts.json")
cuts = json.load(open(OUT)) if os.path.exists(OUT) else {}
for reel in sorted({v[0] for v in FILMS.values()}):
    if reel in cuts: continue
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", os.path.join(FT, reel + ".mp4"), "-vf", "scale=320:-2,scdet=threshold=12", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    cuts[reel] = [round(float(x), 2) for x in re.findall(r"lavfi\.scd\.time: ([\d.]+)", r.stderr)]
    print(reel, len(cuts[reel]), flush=True)
    json.dump(cuts, open(OUT, "w"))
