"""Scene-relative time of a spoken phrase (same estimate as B.at in lib/battle.js), for picking snapshot times.
usage: python3 tools/phrase_t.py SCENE "para-id:phrase" ...   (SCENE must be built: reads scenes/SCENE/timing.js)"""
import json, sys
tjs = open(f"scenes/{sys.argv[1]}/timing.js").read()
T = json.loads(tjs[tjs.index("=") + 1:].strip().rstrip(";"))
for a in sys.argv[2:]:
    k, ph = a.split(":", 1)
    s0, s1 = T["paras"][k]; txt = T["text"][k]
    i = txt.index(ph) if ph else 0
    print(f"{s0 + (s1 - s0) * i / len(txt):.1f}", k, ph)
