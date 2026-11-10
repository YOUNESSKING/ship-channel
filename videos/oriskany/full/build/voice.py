"""Full Oriskany narration, v8: the designed voice "Archive" (owner pick 2026-11-10; CLAUDE.md "Voice").

  Kokoro style blend bm_fable 0.40 + am_michael 0.40 + bm_lewis 0.20 (tts/voices/archive_style.npy, passed as voice=<ndarray>),
  speed 0.92; question sentences at 0.92 * 0.88 / 0.95 = 0.852 (the same relative slowdown as the am_michael take: 0.88 vs 0.95).
  Text: script/NARRATION_v3.txt (v2 sentence fix and the v3 ending cut, option A, are already in it).
  Chunks: one per sentence (the hook keeps its approved test-v4 phrase splits and pauses), cached in audio/chunks_archive/
  (resumable; a chunk is re-voiced only when its text, speed or fixes change). Pauses: 0.3 s between sentences, 0.6 s between
  paragraphs, 0.9 s at chapter breaks.
  Pronunciation: TEXT_FIX (respellings) and PHON_FIX (phoneme edits, tts/PRONUNCIATION.md) as before for Oriskany, MiG,
  Okaloosa and porgies, plus the v8 gate fixes (build/PRONUNCIATION_GATE_v8.md).
  Word timing: faster-whisper small.en per chunk (cached), aligned to the script words with a sequence match; words whisper
  did not return are interpolated between their matched neighbours.
Out: audio/voice_archive.wav (raw; the mix applies the voice-stem chain), build/words.json (the v7 words are kept in
build/words_v7.json), build/chunks.json, chapters.json, build/voice_gate.json (whisper text per chunk, for the gate).

  python3 build/voice.py            # voice + timings
  ONLY_VOICE=1 python3 build/voice.py   # voice only (no whisper)"""
import difflib, hashlib, json, os, re, shutil, sys, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
NARR = os.environ.get("NARR", os.path.join(ROOT, "videos/oriskany/script/NARRATION_v3.txt"))
STYLE_FILE = os.path.join(ROOT, "tts/voices/archive_style.npy")
VOICE_TAG, SPEED = "archive", 0.92
QSPEED = round(SPEED * 0.88 / 0.95, 4)          # 0.8522: the am_michael take read questions at 0.88 against 0.95
LEAD, TAIL = 0.35, 1.0
GAP_S, GAP_P, GAP_C = 0.3, 0.6, 0.9
OUT_WAV = os.path.join(FULL, "audio/voice_archive.wav")
CD = os.path.join(FULL, "audio/chunks_archive")
TEXT_FIX = {"MiG-fifteens": "Mig fifteens", "MiG": "Mig"}   # "my-gee" -> mig (order matters)
PHON_FIX = {"ˈɔːɹɪskəni": "ɔːɹˈɪskəni",                           # Oriskany: or-ISS-kuh-nee
            "ˈoʊkɐlˌuːsə": "ˌoʊkɐlˈuːsə",                          # Okaloosa: oh-kuh-LOO-suh
            "pˈɔːɹdʒiz": "pˈɔːɹɡiz"}                               # porgies: hard g
# v8 gate fixes (build/PRONUNCIATION_GATE_v8.md): filled after the gate
TEXT_FIX.update(json.load(open(os.path.join(HERE, "text_fix_v8.json"))) if os.path.exists(os.path.join(HERE, "text_fix_v8.json")) else {})
PHON_FIX.update(json.load(open(os.path.join(HERE, "phon_fix_v8.json"))) if os.path.exists(os.path.join(HERE, "phon_fix_v8.json")) else {})
# hook: the approved test-v4 phrase splits and pauses (speed None = SPEED, else the question speed). The SS United States
# sentences of paragraph 5 are read from the narration file (they will be re-written after 12 November), so they are not here.
HOOK = [
 ("Right now, two hundred and twelve feet under the Gulf of Mexico,", 0.08, None),
 ("lies an aircraft carrier.", 0.45, None), ("No enemy sank her.", 0.3, None), ("The United States Navy did.", 0.25, None),
 ("On purpose.", 0.6, None), ("Navy demolition divers set off twenty-two charges inside the USS Oriskany.", 0.55, None),
 ("Thirty-seven minutes later,", 0.1, None), ("she was gone.", 0.5, None),
 ("Getting her ready to sink took over three years", 0.08, None), ("and about twenty million dollars.", 0.5, None),
 ("So why pay millions to put a carrier on the sea floor?", 0.35, QSPEED), ("Why not keep her?", 0.2, QSPEED),
 ("Why not scrap her?", 0.5, QSPEED), ("The answer is buried in her past.", 0.3, None),
 ("And in what was still inside her when she sank.", 0.5, None), ("And it matters right now.", 0.4, None)]
HOOK_SS_GAPS = [0.2]          # gaps after the file's remaining hook sentences (the last one gets GAP_C)
CHAPTERS = [("c01", "Hook", "Right now"), ("c02", "Nobody Wanted Her", "Start with the day"),
            ("c03", "The Mighty O", "Her keel was laid"), ("c04", "The Bargain", "In November two thousand three"),
            ("c05", "Thirty-Seven Minutes", "On the twenty-second of March"), ("c06", "The Fish Test", "Not all of the PCBs"),
            ("c07", "The Real Reason + Ending", "To answer that")]
SPLIT = lambda p: [s.strip() for s in re.findall(r"[^.?!]+[.?!]+(?:\s|$)", p + " ") if s.strip()]

paras = [p.strip() for p in open(NARR).read().split("\n\n") if p.strip()]
starts = {c[2]: c[0] for c in CHAPTERS}
chunks = []   # (text, gap_after, speed, chapter, paragraph index)
cur = None
hook_text = " ".join(t for t, _, _ in HOOK)
for pi, p in enumerate(paras):
    for k_, v in starts.items():
        if p.startswith(k_): cur = v
    nxt_ch = pi + 1 < len(paras) and any(paras[pi + 1].startswith(k_) for k_ in starts)
    if cur == "c01":
        if nxt_ch:   # last hook paragraph: everything up to the end of the fixed HOOK list, then its own sentences
            done = " ".join(paras[:pi])
            pre = hook_text[len(done) + 1:] if done else hook_text
            assert p.startswith(pre), ("hook text changed", pre[:60], p[:60])
            chunks += [(t, g, s, "c01", pi) for t, g, s in HOOK]
            rest = SPLIT(p[len(pre):].strip())
            for si, s in enumerate(rest):
                chunks.append((s, GAP_C if si == len(rest) - 1 else (HOOK_SS_GAPS[si] if si < len(HOOK_SS_GAPS) else GAP_S), None, "c01", pi))
        continue
    sents = SPLIT(p)
    assert " ".join(sents).replace("  ", " ") == p, ("split", p[:50])
    for si, s in enumerate(sents):
        last = si == len(sents) - 1
        gap = (GAP_C if nxt_ch else GAP_P) if last else GAP_S
        if pi == len(paras) - 1 and last: gap = TAIL
        chunks.append((s, gap, QSPEED if s.endswith("?") else None, cur, pi))
assert " ".join(c[0] for c in chunks) == " ".join(paras), "chunks do not rebuild the narration"

STYLE = np.load(STYLE_FILE).astype(np.float32)
STYLE_MD5 = hashlib.md5(STYLE.tobytes()).hexdigest()[:8]
_k = None
def kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(ROOT, "tts/kokoro-v1.0.onnx"), os.path.join(ROOT, "tts/voices-v1.0.bin"))
    return _k


def say_of(text):
    s = text
    for a_, b_ in TEXT_FIX.items(): s = s.replace(a_, b_)
    return s


def synth(text, sp):
    """one chunk with the Archive style, the fixes and the trim of the v1-v7 builder"""
    k = kokoro(); say = say_of(text)
    ph = k.tokenizer.phonemize(say, "en-us"); fixed = ph
    for a_, b_ in PHON_FIX.items(): fixed = fixed.replace(a_, b_)
    if fixed != ph: a, sr = k.create(fixed, voice=STYLE, speed=sp, lang="en-us", is_phonemes=True)
    else: a, sr = k.create(say, voice=STYLE, speed=sp, lang="en-us")
    a = a.astype(np.float32)
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 240): nz[-1] + 480]
    return a, fixed != ph


def chunk_key(text, sp):
    """v8: keyed on what is actually spoken (respelled text + the phonemes, when a fix changed them), so a new fix
    re-voices only the chunks it touches"""
    say = say_of(text); ph = kokoro().tokenizer.phonemize(say, "en-us"); fixed = ph
    for a_, b_ in PHON_FIX.items(): fixed = fixed.replace(a_, b_)
    return hashlib.md5(f"{VOICE_TAG}|{STYLE_MD5}|{sp}|{say}|{fixed if fixed != ph else ''}".encode()).hexdigest()[:12]


def chunk_key_v1(text, sp):   # the first v8 key (all fixes in the key), used once to rename the cache
    return hashlib.md5(f"{VOICE_TAG}|{STYLE_MD5}|{sp}|{say_of(text)}|{sorted(PHON_FIX.items())}".encode()).hexdigest()[:12]


if __name__ == "__main__":
    os.makedirs(CD, exist_ok=True)
    sr = 24000; parts = [np.zeros(int(sr * LEAD), np.float32)]; t = LEAD; spans = []; fixes = set()
    for i, (text, gap, spd, ch, pi) in enumerate(chunks):
        sp = spd or SPEED
        cf = os.path.join(CD, f"{chunk_key(text, sp)}.wav")
        if os.path.exists(cf): a, _ = sf.read(cf, dtype="float32")
        else:
            a, fx = synth(text, sp); sf.write(cf, a, sr)
            if fx: fixes.add(text[:40])
        d = len(a) / sr; spans.append((text, t, t + d, ch, pi, sp, os.path.basename(cf)))
        parts += [a, np.zeros(int(sr * gap), np.float32)]; t += d + gap
        if i % 20 == 0: print(i, "/", len(chunks), round(t, 1), flush=True)
    voice = np.concatenate(parts)
    sf.write(OUT_WAV, voice, sr, subtype="PCM_16")
    print("duration", round(t, 2), "chunks", len(chunks), "phoneme-fixed (new this run):", sorted(fixes), flush=True)
    json.dump({"voice": "archive (bm_fable 0.40 + am_michael 0.40 + bm_lewis 0.20)", "style_md5": STYLE_MD5, "speed": SPEED,
               "question_speed": QSPEED, "duration": round(t, 3),
               "chunks": [{"text": a, "start": round(b, 3), "end": round(c, 3), "chapter": d, "para": e, "speed": f, "file": g}
                          for a, b, c, d, e, f, g in spans]},
              open(os.path.join(HERE, "chunks.json"), "w"), indent=1)
    if os.environ.get("ONLY_VOICE"): sys.exit(0)

    # ---- word timing: whisper per chunk (cached by chunk file), aligned to the script words
    from faster_whisper import WhisperModel
    WM = os.environ.get("WHISPER", "small.en")   # v8: small.en (base.en word times were up to ~0.5 s off around spoken numbers)
    m = WhisperModel(WM, device="cpu", compute_type="int8")
    WC = os.path.join(CD, f"whisper_{WM}.json")
    cache = json.load(open(WC)) if os.path.exists(WC) else {}
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    words = []; gate = []; nint = 0
    for ci, (text, t0, t1, ch, pi, sp, fn) in enumerate(spans):
        if fn not in cache:
            seg = voice[int(round(t0 * sr)): int(round(t1 * sr))]
            seg = np.interp(np.arange(0, len(seg), sr / 16000), np.arange(len(seg)), seg).astype(np.float32)
            cache[fn] = [(w.start, w.end, w.word) for s in m.transcribe(seg, language="en", word_timestamps=True, beam_size=5)[0] for w in s.words]
            if ci % 25 == 0: json.dump(cache, open(WC, "w")); print("align", ci, flush=True)
        sw = cache[fn]
        toks = [x for x in text.replace("-", " - ").split() if x != "-"]
        gate.append({"i": ci, "start": round(t0, 3), "text": text, "heard": "".join(w[2] for w in sw).strip()})
        a_ = [norm(x) for x in toks]; b_ = [norm(w[2]) for w in sw]
        tw = [None] * len(toks); dur = t1 - t0
        ops = difflib.SequenceMatcher(None, a_, b_, autojunk=False).get_opcodes()
        for op, i1, i2, j1, j2 in ops:
            if op == "equal":
                for q in range(i2 - i1): tw[i1 + q] = (sw[j1 + q][0], sw[j1 + q][1])
            elif op == "replace":   # e.g. "two hundred and twelve" heard as "212": spread the script words over those tokens
                lo, hi = sw[j1][0], sw[j2 - 1][1]
                L = [len(x) + 1 for x in a_[i1:i2]]; c = np.cumsum([0] + L); tot = c[-1]
                for q in range(i1, i2): tw[q] = (lo + (hi - lo) * c[q - i1] / tot, lo + (hi - lo) * (c[q - i1 + 1] - 1) / tot)
        if any(x is None for x in tw): nint += 1
        i = 0
        while i < len(toks):   # words whisper did not return at all: between their neighbours, by character length
            if tw[i] is not None: i += 1; continue
            j = i
            while j < len(toks) and tw[j] is None: j += 1
            lo = tw[i - 1][1] if i > 0 else 0.0
            hi = tw[j][0] if j < len(toks) else dur
            if hi <= lo: hi = min(dur, lo + 0.08 * (j - i))
            L = [len(norm(x)) + 1 for x in toks[i:j]]; c = np.cumsum([0] + L); tot = c[-1]
            for q in range(i, j):
                tw[q] = (lo + (hi - lo) * c[q - i] / tot, lo + (hi - lo) * (c[q - i + 1] - 1) / tot)
            i = j
        for x, (s, e) in zip(toks, tw):
            words.append({"w": x, "start": round(t0 + max(0.0, s), 3), "end": round(t0 + min(dur, e), 3)})
    json.dump(cache, open(WC, "w"))
    WJ = os.path.join(HERE, "words.json"); W7 = os.path.join(HERE, "words_v7.json")
    if not os.path.exists(W7): shutil.copy2(WJ, W7)
    json.dump(words, open(WJ, "w"), indent=0)
    json.dump(gate, open(os.path.join(HERE, "voice_gate.json"), "w"), indent=1, ensure_ascii=False)
    chs = []
    for cid, title, _ in CHAPTERS:
        cs = [s for s in spans if s[3] == cid]
        chs.append({"key": cid, "title": title, "start": 0.0 if cid == "c01" else round(cs[0][1] - 0.45, 3),
                    "voice_end": round(cs[-1][2], 3), "words": sum(len(s[0].split()) for s in cs)})
    for i, c in enumerate(chs): c["end"] = chs[i + 1]["start"] if i + 1 < len(chs) else round(t, 3); c["duration"] = round(c["end"] - c["start"], 3)
    json.dump({"duration": round(t, 3), "fps": 30, "chapters": chs}, open(os.path.join(FULL, "chapters.json"), "w"), indent=1)
    print("chunks with interpolated words:", nint)
    for c in chs: print(c["key"], c["start"], c["end"], c["duration"], c["title"])
