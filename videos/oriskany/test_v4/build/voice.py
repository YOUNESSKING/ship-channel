"""Kokoro narration (am_michael, 0.95) synthesized per phrase so pauses are controlled, then word-level
timing from a faster-whisper alignment pass, mapped back onto the exact script words.
Out: audio/voice.wav, build/words.json  ([{"w":word,"start":s,"end":s}] = the template engine's format)."""
import json, os, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
VOICE, SPEED, LEAD = "am_michael", 0.95, 0.35
CHUNKS = [  # (text, pause after)
 ("May seventeenth, two thousand six.", 0.35),
 ("Off the coast of Florida,", 0.12),
 ("Navy demolition divers set off explosive charges inside a retired American aircraft carrier.", 0.45),
 ("Thirty-seven minutes later,", 0.12),
 ("she was gone.", 0.55),
 ("About nine hundred feet of warship,", 0.15),
 ("now sitting two hundred and twelve feet down.", 0.5),
 ("No enemy sank her.", 0.35),
 ("The United States Navy did.", 0.3),
 ("On purpose.", 0.75),
 ("It took three years", 0.1),
 ("and about twenty million dollars", 0.1),
 ("just to get her ready to sink.", 0.55),
 ("So why would the Navy pay millions to send one of its own carriers to the bottom of the sea,", 0.15),
 ("instead of keeping her,", 0.15),
 ("or simply cutting her up for scrap?", 0.6),
 ("The answer starts with what was hidden inside her.", 0.6),
 ("And this month, a second famous American ship is scheduled to go down off the same coast,", 0.15),
 ("for the very same reason.", 1.4),
]
k = Kokoro(os.path.join(ROOT, "tts/kokoro-v1.0.onnx"), os.path.join(ROOT, "tts/voices-v1.0.bin"))
sr = 24000; parts = [np.zeros(int(sr * LEAD), np.float32)]; t = LEAD; spans = []
for text, gap in CHUNKS:
    a, sr = k.create(text, voice=VOICE, speed=SPEED, lang="en-us"); a = a.astype(np.float32)
    # trim Kokoro's leading/trailing near-silence so pauses are exactly ours
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 240): nz[-1] + 480]
    d = len(a) / sr; spans.append((text, t, t + d))
    parts += [a, np.zeros(int(sr * gap), np.float32)]; t += d + gap
voice = np.concatenate(parts)
os.makedirs(os.path.join(HERE, "../audio"), exist_ok=True)
sf.write(os.path.join(HERE, "../audio/voice.wav"), voice, sr)
print("duration", round(t, 2))

# word alignment per chunk: whisper on each chunk's audio, words mapped in order onto the script words
from faster_whisper import WhisperModel
m = WhisperModel("base.en", device="cpu", compute_type="int8")
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
words = []
for text, t0, t1 in spans:
    seg = voice[int(t0 * sr): int(t1 * sr)]
    seg = np.interp(np.arange(0, len(seg), sr / 16000), np.arange(len(seg)), seg).astype(np.float32)  # whisper wants 16 kHz
    sw = [w for s in m.transcribe(seg, language="en", word_timestamps=True, beam_size=5)[0] for w in s.words]
    toks = text.replace("-", " - ").split()
    toks = [x for x in toks if x != "-"]
    # whisper may merge/split numbers ("37" for thirty-seven); align proportionally inside the chunk when counts differ
    if len(sw) == len(toks):
        tw = [(w.start, w.end) for w in sw]
    else:
        # character-weighted spread anchored on whisper's first start / last end
        a0 = sw[0].start if sw else 0.0; a1 = sw[-1].end if sw else (t1 - t0)
        L = [len(x) + 1 for x in toks]; c = np.cumsum([0] + L); tot = c[-1]
        tw = [(a0 + (a1 - a0) * c[i] / tot, a0 + (a1 - a0) * (c[i + 1] - 1) / tot) for i in range(len(toks))]
        print("  proportional:", text, len(sw), "vs", len(toks))
    for x, (s, e) in zip(toks, tw):
        words.append({"w": x, "start": round(t0 + s, 3), "end": round(t0 + e, 3)})
json.dump(words, open(os.path.join(HERE, "words.json"), "w"), indent=0)
json.dump({"duration": round(t, 3), "chunks": [{"text": a, "start": round(b, 3), "end": round(c, 3)} for a, b, c in spans]},
          open(os.path.join(HERE, "chunks.json"), "w"), indent=1)
for i, w in enumerate(words): print(i, w["w"], w["start"])
