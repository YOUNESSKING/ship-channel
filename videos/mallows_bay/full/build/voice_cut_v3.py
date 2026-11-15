"""v3 ending cut (owner decision 2026-11-05, option A): three passages removed from the narration, no re-voicing.

  cut 1  "Nobody would take her whole. Nobody could make a scrap deal stick. And the PCBs were in her wiring, where only taking
         her apart could reach them."                     (chunks 214-216)
  cut 2  "By the Navy's own sums, it was also the cheapest." (chunk 218)
  cut 3  "She is nine hundred and ninety feet long. No explosives this time. They will flood her." (chunks 222-224)

Each cut removes [first_start, next_start - (P - pause_before)) where P = the longer of the two original pauses around the passage (so a paragraph
pause stays a paragraph pause); the cut points sit in silence between chunks and get 10 ms crossfades. Inputs are the v2 files
(audio/voice_v2.wav, build/words_v2.json, build/chunks_v2.json, chapters_v2.json; saved on the first run). Writes audio/voice.wav,
build/words.json, build/chunks.json, chapters.json and build/cuts_v3.json (cut map: v2 time -> v3 time)."""
import json, os, shutil, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE)
P = lambda *a: os.path.join(FULL, *a)
for a, b in [("audio/voice.wav", "audio/voice_v2.wav"), ("build/words.json", "build/words_v2.json"),
             ("build/chunks.json", "build/chunks_v2.json"), ("chapters.json", "build/chapters_v2.json")]:
    if not os.path.exists(P(b)): shutil.copy2(P(a), P(b))
voice, sr = sf.read(P("audio/voice_v2.wav"), dtype="float32")
W = json.load(open(P("build/words_v2.json"))); CJ = json.load(open(P("build/chunks_v2.json"))); C = CJ["chunks"]
CUTS = [(214, 216), (218, 218), (222, 224)]
cuts = []
for a, b in CUTS:
    prev_end, nxt = C[a - 1]["end"], C[b + 1]["start"]
    pause = max(C[a]["start"] - prev_end, nxt - C[b]["end"])
    gap_before = C[a]["start"] - prev_end   # keep that pause, and as much of the pause after as makes it `pause` long
    cuts.append(dict(t0=C[a]["start"], t1=round(nxt - (pause - gap_before), 3), text=" ".join(C[i]["text"] for i in range(a, b + 1))))
for c in cuts: c["dur"] = round(c["t1"] - c["t0"], 3)
def shift(t):
    """v2 time -> v3 time (a time inside a cut maps to the cut point)"""
    d = 0.0
    for c in cuts:
        if t >= c["t1"]: d += c["dur"]
        elif t > c["t0"]: return round(c["t0"] - d, 3)
    return round(t - d, 3)
# audio: keep the pieces, 10 ms crossfade at each join
F = int(0.010 * sr); out = []; pos = 0
for c in cuts:
    out.append(voice[pos:int(round(c["t0"] * sr))]); pos = int(round(c["t1"] * sr)) - F   # both crossfade halves in the pauses
out.append(voice[pos:])
res = out[0]
for seg in out[1:]:
    r = np.linspace(1, 0, F, dtype=np.float32); x = res[-F:] * r + seg[:F] * (1 - r)
    res = np.concatenate([res[:-F], x, seg[F:]])
sf.write(P("audio/voice.wav"), res, sr, subtype="PCM_16")
inside = lambda t: any(c["t0"] <= t < c["t1"] for c in cuts)
W3 = [dict(w=x["w"], start=shift(x["start"]), end=shift(x["end"])) for x in W if not inside(x["start"])]
json.dump(W3, open(P("build/words.json"), "w"), indent=0)
C3 = [dict(c, start=shift(c["start"]), end=shift(c["end"])) for i, c in enumerate(C) if not any(a <= i <= b for a, b in CUTS)]
json.dump(dict(CJ, duration=shift(CJ["duration"]), chunks=C3), open(P("build/chunks.json"), "w"), indent=1)
CH = json.load(open(P("build/chapters_v2.json")))
for c in CH["chapters"]:
    for k in ("start", "end", "voice_end"): c[k] = shift(c[k])
    c["duration"] = round(c["end"] - c["start"], 3)
    if c["key"] == "c07": c["words"] = sum(len(x["text"].split()) for x in C3 if x["chapter"] == "c07")
CH["duration"] = shift(CH["duration"])
json.dump(CH, open(P("chapters.json"), "w"), indent=1)
json.dump(dict(cuts=cuts, removed=round(sum(c["dur"] for c in cuts), 3)), open(P("build/cuts_v3.json"), "w"), indent=1)
print(json.dumps(cuts, indent=1)); print("removed", round(sum(c["dur"] for c in cuts), 3), "s; voice", len(voice) / sr, "->", len(res) / sr)
print("c07", [c for c in CH["chapters"] if c["key"] == "c07"])
