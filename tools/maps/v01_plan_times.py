#!/usr/bin/env python3
"""Reads the Video 01 chapter plans (videos/video01/plan/ch*.json, final.json) + voice/words.json and writes tools/v01_map_plan.json:
for each MAP shot its length, planned pin (1280x720), and clip-local times of the gauge / name / date (so the bakes move in sync with the template overlays)."""
import json, glob, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PLAN = os.path.join(ROOT, "videos/video01/plan")
out = {}
for f in sorted(glob.glob(PLAN + "/ch*.json")) + [PLAN + "/final.json"]:
    d = json.load(open(f)); words = json.load(open(os.path.normpath(os.path.join(PLAN, d["words"])))); off = float(d.get("audio_offset", 0))
    def T(spec, base=0.0):
        if spec is None: return None
        if isinstance(spec, (int, float)): return float(spec)
        s = str(spec); o = 0.0; m = re.search(r"([+-]\d+(?:\.\d+)?)$", s)
        if m and not re.fullmatch(r"[+-]?\d+(\.\d+)?", s): o = float(m.group(1)); s = s[:m.start()].strip()
        if s == "start": return base + o
        mm = re.fullmatch(r"w(\d+)(e?)", s)
        if mm: w = words[int(mm.group(1))]; return (w["end"] if mm.group(2) else w["start"]) - off + o
        return None
    shots = d["shots"]; starts = []
    for i, s in enumerate(shots):
        st = s.get("start", 0.0); starts.append(float(st) if isinstance(st, (int, float)) else T(st))
    for i, s in enumerate(shots):
        if s["template"] != "map_clip": continue
        mid = os.path.splitext(os.path.basename(s["clip"]["file"]))[0]; a = starts[i]; p = s.get("params", {}); dur = s["plan"]["dur"]
        L = lambda spec: None if T(spec, a) is None else round(T(spec, a) - a, 3)
        g = p.get("gauge")
        out[mid] = dict(chapter=d["key"], shot=s["id"], variant=s["variant"], dur=dur, pin=p.get("pin"), name_at=L(p.get("name_at")), date_at=L(p.get("date_at")),
                        gauge=None if not g else dict(g, at_local=L(g.get("at")), **{"from": g["from"], "to": g["to"]}))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "v01_map_plan.json"), "w"), indent=1)
print(len(out), "map shots")
for k, v in out.items(): print(k, v["dur"], v["pin"], v["name_at"], v["gauge"] and (v["gauge"]["from"], v["gauge"]["to"], v["gauge"]["at_local"], v["gauge"]["dur"]))
