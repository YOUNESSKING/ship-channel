"""v8 time map between the v7 narration (am_michael take, build/words_v7.json, v3 timeline) and the v8 Archive take
(build/words.json). Both carry the same script words in the same order, so every word start / end is a knot of a monotonic
piecewise-linear map. Used where v1-v7 build rules were written as absolute seconds (sfx_full.py, music_bed.py, the hook):
  new(t_v7) -> v8 seconds,  old(t_v8) -> v7 seconds."""
import json, os, re, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
_n = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
_O = json.load(open(os.path.join(HERE, "words_v7.json")))
_N = json.load(open(os.path.join(HERE, "words.json")))
assert [_n(w["w"]) for w in _O] == [_n(w["w"]) for w in _N], "v7 and v8 word lists differ"
_ko, _kn = [0.0], [0.0]
for a, b in zip(_O, _N):
    for k in ("start", "end"):
        if a[k] > _ko[-1] + 1e-4 and b[k] > _kn[-1] + 1e-4: _ko.append(a[k]); _kn.append(b[k])
_ko, _kn = np.array(_ko), np.array(_kn)


def new(t):
    t = float(t)
    return float(np.interp(t, _ko, _kn)) if t <= _ko[-1] else float(_kn[-1] + (t - _ko[-1]))


def old(t):
    t = float(t)
    return float(np.interp(t, _kn, _ko)) if t <= _kn[-1] else float(_ko[-1] + (t - _kn[-1]))
