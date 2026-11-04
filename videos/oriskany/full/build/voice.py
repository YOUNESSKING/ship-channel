"""Full Oriskany narration: Kokoro am_michael exactly as test v4 (0.95; question sentences 0.88; Oriskany phonemes),
per-sentence chunks cached in audio/chunks/ (resumable), pauses: 0.3 s between sentences, 0.6 s between paragraphs,
0.9 s at chapter breaks. Hook = test v4's exact chunk list (approved take). Word timing: faster-whisper per chunk,
mapped onto the script words. Out: audio/voice.wav (raw, the mix applies the voice-stem chain), build/words.json,
build/chunks.json, chapters.json."""
import hashlib, json, os, re, sys, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
NARR = os.path.join(ROOT, "videos/oriskany/script/NARRATION_v2.txt")
VOICE, SPEED, QSPEED, LEAD, TAIL = "am_michael", 0.95, 0.88, 0.35, 1.0
GAP_S, GAP_P, GAP_C = 0.3, 0.6, 0.9
TEXT_FIX = {"MiG-fifteens": "Mig fifteens", "MiG": "Mig"}   # "my-gee" -> mig (order matters)
PHON_FIX = {"ˈɔːɹɪskəni": "ɔːɹˈɪskəni",                           # Oriskany: or-ISS-kuh-nee
            "ˈoʊkɐlˌuːsə": "ˌoʊkɐlˈuːsə",                          # Okaloosa: oh-kuh-LOO-suh
            "pˈɔːɹdʒiz": "pˈɔːɹɡiz"}                               # porgies: hard g
HOOK = [  # test v4 build/voice.py CHUNKS, verbatim (approved take)
 ("Right now, two hundred and twelve feet under the Gulf of Mexico,", 0.08, None),
 ("lies an aircraft carrier.", 0.45, None), ("No enemy sank her.", 0.3, None), ("The United States Navy did.", 0.25, None),
 ("On purpose.", 0.6, None), ("Navy demolition divers set off twenty-two charges inside the USS Oriskany.", 0.55, None),
 ("Thirty-seven minutes later,", 0.1, None), ("she was gone.", 0.5, None),
 ("Getting her ready to sink took over three years", 0.08, None), ("and about twenty million dollars.", 0.5, None),
 ("So why pay millions to put a carrier on the sea floor?", 0.35, 0.88), ("Why not keep her?", 0.2, 0.88),
 ("Why not scrap her?", 0.5, 0.88), ("The answer is buried in her past.", 0.3, None),
 ("And in what was still inside her when she sank.", 0.5, None), ("And it matters right now.", 0.4, None),
 ("On November twelfth, the ocean liner SS United States is scheduled to follow her down.", 0.2, None),
 ("About thirteen nautical miles away.", GAP_C, None)]
# chapter = first words of its first paragraph (SCRIPT_v2 chapters; the short ending is merged into c07)
CHAPTERS = [("c01", "Hook", "Right now"), ("c02", "Nobody Wanted Her", "Start with the day"),
            ("c03", "The Mighty O", "Her keel was laid"), ("c04", "The Bargain", "In November two thousand three"),
            ("c05", "Thirty-Seven Minutes", "On the twenty-second of March"), ("c06", "The Fish Test", "Not all of the PCBs"),
            ("c07", "The Real Reason + Ending", "To answer that")]

paras = [p.strip() for p in open(NARR).read().split("\n\n") if p.strip()]
starts = {c[2]: c[0] for c in CHAPTERS}
chunks = []   # (text, gap_after, speed, chapter)
cur = None; hook_done = False
for pi, p in enumerate(paras):
    for k_, v in starts.items():
        if p.startswith(k_): cur = v
    if cur == "c01":
        if not hook_done: chunks += [(t, g, s, "c01") for t, g, s in HOOK]; hook_done = True
        continue
    sents = re.findall(r"[^.?!]+[.?!]+(?:\s|$)", p + " ")
    sents = [s.strip() for s in sents if s.strip()]
    assert " ".join(sents).replace("  ", " ") == p, ("split", p[:50])
    nxt_ch = pi + 1 < len(paras) and any(paras[pi + 1].startswith(k_) for k_ in starts)
    for si, s in enumerate(sents):
        last = si == len(sents) - 1
        gap = (GAP_C if nxt_ch else GAP_P) if last else GAP_S
        if pi == len(paras) - 1 and last: gap = TAIL
        chunks.append((s, gap, QSPEED if s.endswith("?") else None, cur))

from kokoro_onnx import Kokoro
k = Kokoro(os.path.join(ROOT, "tts/kokoro-v1.0.onnx"), os.path.join(ROOT, "tts/voices-v1.0.bin"))
CD = os.path.join(FULL, "audio/chunks"); os.makedirs(CD, exist_ok=True)
sr = 24000; parts = [np.zeros(int(sr * LEAD), np.float32)]; t = LEAD; spans = []
fixes = set()
for i, (text, gap, spd, ch) in enumerate(chunks):
    say = text
    for a_, b_ in TEXT_FIX.items(): say = say.replace(a_, b_)
    sp = spd or SPEED
    key = hashlib.md5(f"{VOICE}|{sp}|{say}|{sorted(PHON_FIX.items())}".encode()).hexdigest()[:12]
    cf = os.path.join(CD, f"{i:03d}_{key}.wav")
    if os.path.exists(cf):
        a, _ = sf.read(cf, dtype="float32")
    else:
        ph = k.tokenizer.phonemize(say, "en-us"); fixed = ph
        for a_, b_ in PHON_FIX.items(): fixed = fixed.replace(a_, b_)
        if fixed != ph:
            fixes.add(text[:40]); a, _ = k.create(fixed, voice=VOICE, speed=sp, lang="en-us", is_phonemes=True)
        else:
            a, _ = k.create(say, voice=VOICE, speed=sp, lang="en-us")
        a = a.astype(np.float32)
        nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 240): nz[-1] + 480]
        sf.write(cf, a, sr)
    d = len(a) / sr; spans.append((text, t, t + d, ch))
    parts += [a, np.zeros(int(sr * gap), np.float32)]; t += d + gap
    if i % 20 == 0: print(i, "/", len(chunks), round(t, 1), flush=True)
voice = np.concatenate(parts)
sf.write(os.path.join(FULL, "audio/voice.wav"), voice, sr)
print("duration", round(t, 2), "chunks", len(chunks), "phoneme-fixed:", sorted(fixes))

# word timing: whisper per chunk (cached), mapped onto the script words
from faster_whisper import WhisperModel
m = WhisperModel("base.en", device="cpu", compute_type="int8")
WC = os.path.join(FULL, "audio/chunks/whisper.json")
cache = json.load(open(WC)) if os.path.exists(WC) else {}
words = []; nprop = 0
for ci, (text, t0, t1, ch) in enumerate(spans):
    kk = f"{ci}|{text}|{round(t1 - t0, 3)}"
    if kk not in cache:
        seg = voice[int(t0 * sr): int(t1 * sr)]
        seg = np.interp(np.arange(0, len(seg), sr / 16000), np.arange(len(seg)), seg).astype(np.float32)
        cache[kk] = [(w.start, w.end, w.word) for s in m.transcribe(seg, language="en", word_timestamps=True, beam_size=5)[0] for w in s.words]
        if ci % 25 == 0: json.dump(cache, open(WC, "w")); print("align", ci, flush=True)
    sw = cache[kk]
    toks = [x for x in text.replace("-", " - ").split() if x != "-"]
    if len(sw) == len(toks):
        tw = [(a, b) for a, b, _ in sw]
    else:
        nprop += 1
        a0 = sw[0][0] if sw else 0.0; a1 = sw[-1][1] if sw else (t1 - t0)
        L = [len(x) + 1 for x in toks]; c = np.cumsum([0] + L); tot = c[-1]
        tw = [(a0 + (a1 - a0) * c[i] / tot, a0 + (a1 - a0) * (c[i + 1] - 1) / tot) for i in range(len(toks))]
    for x, (s, e) in zip(toks, tw):
        words.append({"w": x, "start": round(t0 + s, 3), "end": round(t0 + e, 3)})
json.dump(cache, open(WC, "w"))
json.dump(words, open(os.path.join(HERE, "words.json"), "w"), indent=0)
json.dump({"duration": round(t, 3), "chunks": [{"text": a, "start": round(b, 3), "end": round(c, 3), "chapter": d} for a, b, c, d in spans]},
          open(os.path.join(HERE, "chunks.json"), "w"), indent=1)
# chapters: start = first chunk start (c01 = 0), end = next chapter start
chs = []
for cid, title, _ in CHAPTERS:
    cs = [s for s in spans if s[3] == cid]
    chs.append({"key": cid, "title": title, "start": 0.0 if cid == "c01" else round(cs[0][1] - 0.45, 3),
                "voice_end": round(cs[-1][2], 3), "words": sum(len(s[0].split()) for s in cs)})
for i, c in enumerate(chs): c["end"] = chs[i + 1]["start"] if i + 1 < len(chs) else round(t, 3); c["duration"] = round(c["end"] - c["start"], 3)
json.dump({"duration": round(t, 3), "fps": 30, "chapters": chs}, open(os.path.join(FULL, "chapters.json"), "w"), indent=1)
print("proportional-aligned chunks:", nprop)
for c in chs: print(c["key"], c["start"], c["end"], c["duration"], c["title"])
