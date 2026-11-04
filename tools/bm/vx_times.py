"""vx agent: print the scene time of every at(P, "phrase") constant in tools/vx_body_<scene>.js (same formula as B.at)."""
import json, re, sys
sc, first = sys.argv[1], sys.argv[2]
T = json.load(open("audio/timing.json")); PP = {p["tag"].split("|")[0].replace("MAP:", "").strip(): p for p in T["paragraphs"]}
t0 = PP[first]["start"]; s = open(f"tools/vx_body_{sc}.js").read()
V = dict(re.findall(r'(P\w*) = "([\w-]+)"', s))
for name, p, ph in re.findall(r'(T_\w+) = at\((P\w*), "([^"]+)"\)', s):
    q = PP[V[p]]; i = q["text"].index(ph); print(f"{name:10s} {q['start'] - t0 + (q['end'] - q['start']) * i / len(q['text']):7.2f}  {ph}")
