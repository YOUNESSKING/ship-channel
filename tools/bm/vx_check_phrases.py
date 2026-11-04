"""vx agent: every at(PARA, "phrase") in tools/vx_body_<scene>.js must be in that paragraph's spoken text (case-sensitive)."""
import json, re, sys
T = json.load(open("audio/timing.json")); TX = {p["tag"].split("|")[0].replace("MAP:", "").strip(): p["text"] for p in T["paragraphs"]}
for sc in sys.argv[1:]:
    s = open(f"tools/vx_body_{sc}.js").read(); V = dict(re.findall(r'(P\w*) = "([\w-]+)"', s)); V.update(dict(re.findall(r', (P\w*) = "([\w-]+)"', s)))
    bad = [(p, ph) for p, ph in re.findall(r'at\((P\w*), "([^"]+)"\)', s) if ph not in TX[V[p]]]
    print(sc, "OK" if not bad else bad)
