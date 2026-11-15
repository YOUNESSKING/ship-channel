"""v2 voice fix (critic A S8): ONE sentence re-voiced, everything else in audio/voice.wav stays sample-identical.

  old: "Four of her sisters were already museums."   (chunk 26, 76.281-78.785 s; false for 1989: only Yorktown 1975 and
        Intrepid 1982 were museums then, Lexington opened 1992 and Hornet 1998)
  new: "Four of her sisters would become museums."    (true; same Kokoro settings as build/voice.py: am_michael, speed 0.95,
        en-us, same trim, same phoneme fixes)
The new take is placed at the same start (76.281 s) and the slot up to the next sentence (79.385 s) is filled with silence,
so no later word moves (the new take must be within +/-0.3 s of the old 2.504 s). build/words.json gets the new chunk's
words (faster-whisper base.en word times, same method as voice.py). Idempotent: run on the v1 voice (backup kept in
audio/voice_v1.wav on first run)."""
import json, os, shutil, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
OLD, NEW = "Four of her sisters were already museums.", "Four of her sisters would become museums."
T0, T_OLD_END, T_NEXT = 76.281, 78.785, 79.385
VOICE, SPEED = "am_michael", 0.95
V = os.path.join(FULL, "audio/voice.wav"); V1 = os.path.join(FULL, "audio/voice_v1.wav")
if not os.path.exists(V1): shutil.copy2(V, V1)
voice, sr = sf.read(V1, dtype="float32")
from kokoro_onnx import Kokoro
k = Kokoro(os.path.join(ROOT, "tts/kokoro-v1.0.onnx"), os.path.join(ROOT, "tts/voices-v1.0.bin"))
a, _ = k.create(NEW, voice=VOICE, speed=SPEED, lang="en-us"); a = a.astype(np.float32)
nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 240): nz[-1] + 480]
d_new, d_old = len(a) / sr, T_OLD_END - T0
assert abs(d_new - d_old) <= 0.3, (d_new, d_old)
i0, i1 = int(round(T0 * sr)), int(round(T_NEXT * sr))
assert i0 + len(a) < i1
out = voice.copy(); out[i0:i1] = 0.0; out[i0:i0 + len(a)] = a
sf.write(V, out, sr, subtype="PCM_16")
sf.write(os.path.join(FULL, "audio/chunks/026_v2_would_become.wav"), a, sr)
# word times for the new chunk
from faster_whisper import WhisperModel
m = WhisperModel("base.en", device="cpu", compute_type="int8")
seg = np.interp(np.arange(0, len(a), sr / 16000), np.arange(len(a)), a).astype(np.float32)
sw = [(w.start, w.end, w.word) for s in m.transcribe(seg, language="en", word_timestamps=True, beam_size=5)[0] for w in s.words]
toks = NEW.split()
assert len(sw) == len(toks), sw
W = json.load(open(os.path.join(HERE, "words.json")))
idx = [i for i, w in enumerate(W) if T0 - 0.05 <= w["start"] < T_OLD_END]
assert [W[i]["w"] for i in idx] == OLD.split() or [W[i]["w"] for i in idx] == toks, [W[i]["w"] for i in idx]
for i, x, (s, e, _) in zip(idx, toks, sw): W[i] = {"w": x, "start": round(T0 + s, 3), "end": round(T0 + e, 3)}
json.dump(W, open(os.path.join(HERE, "words.json"), "w"), indent=0)
C = json.load(open(os.path.join(HERE, "chunks.json")))
for c in C["chunks"]:
    if c["text"] in (OLD, NEW): c["text"] = NEW; c["end"] = round(T0 + d_new, 3); c["v2_note"] = f"re-voiced in v2 (was: {OLD}, {d_old:.3f} s)"
json.dump(C, open(os.path.join(HERE, "chunks.json"), "w"), indent=1)
print(f"new take {d_new:.3f} s (old {d_old:.3f} s, diff {d_new - d_old:+.3f} s); words:", [(W[i]['w'], W[i]['start']) for i in idx])
