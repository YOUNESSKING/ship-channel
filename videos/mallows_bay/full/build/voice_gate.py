"""v8 pronunciation gate: the whisper transcript of every Archive chunk (build/voice_gate.json, written by voice.py) against
the script. Digits whisper prints are spelled out first, then both sides are compared word by word; every difference is
listed for listening. usage: python3 build/voice_gate.py [model]   (no model = the cached small.en timing transcript; small.en /
medium.en = a fresh, stricter transcript of audio/voice_archive.wav per chunk)"""
import difflib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE)
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n):
    n = int(n)
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000: return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    if n < 1000000: return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + say(n % 1000))
    return say(n // 1000000) + " million" + ("" if n % 1000000 == 0 else " " + say(n % 1000000))


def year(n):
    n = int(n)
    if 1900 <= n < 2000: return say(n // 100) + " " + (say(n % 100) if n % 100 >= 10 else ("hundred" if n % 100 == 0 else "oh " + say(n % 100)))
    if 2000 <= n < 2010: return "two thousand" + ("" if n == 2000 else " " + say(n % 10))
    if 2010 <= n < 2100: return "twenty " + say(n % 100)
    return say(n)


def words(s):
    s = s.replace("%", " percent").replace("$", " dollars ")
    s = re.sub(r"(\d),(\d{3})", r"\1\2", s)
    s = re.sub(r"\b(\d+)(st|nd|rd|th)\b", r"\1", s)
    s = re.sub(r"\b(1[89]\d\d|20\d\d)s\b", lambda m: year(m.group(1)) + "s", s)
    s = re.sub(r"\b(1[89]\d\d|20\d\d)\b", lambda m: year(m.group(1)), s)
    s = re.sub(r"\b\d+\b", lambda m: say(m.group(0)), s)
    s = s.replace("-", " ").lower()
    return [re.sub(r"[^a-z']", "", w).strip("'") for w in s.split() if re.sub(r"[^a-z]", "", w)]


ORD = {"first": "one", "second": "two", "third": "three", "twelfth": "twelve", "eighteenth": "eighteen", "ninth": "nine",
       "seventeenth": "seventeen", "twentysecond": "twentytwo", "twentysixth": "twentysix", "thirteenth": "thirteen"}
def canon(ws):
    out = []
    for w in ws:
        w = w.replace("'", "")
        out.append(ORD.get(w, w))
    return out


if __name__ == "__main__":
    G = json.load(open(os.path.join(HERE, "voice_gate.json")))
    model = sys.argv[1] if len(sys.argv) > 1 else "timing"   # "timing" = the cached small.en transcript voice.py made
    if model != "timing":
        import numpy as np, soundfile as sf
        from faster_whisper import WhisperModel
        m = WhisperModel(model, device="cpu", compute_type="int8")
        C = json.load(open(os.path.join(HERE, "chunks.json")))["chunks"]
        v, sr = sf.read(os.path.join(FULL, "audio/voice_archive.wav"), dtype="float32")
        for g, c in zip(G, C):
            seg = v[int(c["start"] * sr): int(c["end"] * sr)]
            seg = np.interp(np.arange(0, len(seg), sr / 16000), np.arange(len(seg)), seg).astype(np.float32)
            g["heard"] = " ".join(s.text.strip() for s in m.transcribe(seg, language="en", beam_size=5)[0])
    bad = []
    for g in G:
        a, b = canon(words(g["text"])), canon(words(g["heard"]))
        A, Bq = "".join(a), "".join(b)
        if A == Bq: continue
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        diffs = [(" ".join(a[i1:i2]), " ".join(b[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
        diffs = [d for d in diffs if d[0].replace(" ", "") != d[1].replace(" ", "")]
        if diffs: bad.append(dict(i=g["i"], start=g["start"], text=g["text"], heard=g["heard"], diffs=diffs))
    json.dump(bad, open(os.path.join(HERE, f"voice_gate_diff_{model}.json"), "w"), indent=1, ensure_ascii=False)
    for x in bad: print(f"{x['start']:7.2f} #{x['i']:3d}  {x['diffs']}   | heard: {x['heard']}")
    print(len(bad), "of", len(G), "chunks differ")
