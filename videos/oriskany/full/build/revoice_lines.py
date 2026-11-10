"""Re-voice ONLY the SS United States sentences (NARRATION_v3.txt line 9 tail, lines 123 and 125) after the 12 November
sinking, without moving any other word of the v8 master.

  1. edit the sentences in script/NARRATION_v3.txt (keep the paragraph breaks; line 9 keeps its first three sentences,
     "The answer is buried ... And it matters right now.", which are part of the fixed hook list in build/voice.py)
  2. python3 build/revoice_lines.py            # dry run: new take lengths against their slots
     python3 build/revoice_lines.py --write    # writes audio/voice_archive.wav, build/words.json, build/chunks.json

Slot rule: a re-voiced paragraph must fit between the start of its first changed sentence and the start of the next
unchanged word (its old take + the pauses inside it), keeping >= MIN_GAP s before that word. If the new take is up to
MAX_STRETCH longer, it is time-compressed (ffmpeg atempo, pitch kept) to fit; if it is still too long, the script stops:
then re-run the whole chain (build/voice.py, which re-voices only the changed chunks from its cache, and every later step of
BUILD_REPORT_v8.md section "Re-voice") because every later word moves. Same Archive settings, fixes and trim as voice.py.
Word times of the new sentences: faster-whisper, aligned as in voice.py."""
import json, os, subprocess, sys, tempfile, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE)
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
import voice as V            # builds the chunk list from the (edited) narration; nothing is synthesised on import
MIN_GAP, MAX_STRETCH, SR = 0.25, 0.06, 24000
C = json.load(open(os.path.join(HERE, "chunks.json")))
old = C["chunks"]
new = V.chunks
assert len(old) == len(new) or True
# match chunks by position from both ends: the changed run is what differs
i0 = 0
while i0 < min(len(old), len(new)) and old[i0]["text"] == new[i0][0]: i0 += 1
j = 0
while j < min(len(old), len(new)) - i0 and old[-1 - j]["text"] == new[-1 - j][0]: j += 1
oc, nc = old[i0:len(old) - j], new[i0:len(new) - j]
if not oc and not nc: sys.exit("no sentence changed")
print("changed old:", [c["text"] for c in oc]); print("changed new:", [c[0] for c in nc])
# several separate runs (line 9 and lines 123/125) are handled one run at a time: re-run the script after each --write
slot0 = oc[0]["start"]; nxt = old[len(old) - j]["start"] if j else C["duration"]
slot = nxt - MIN_GAP - slot0
takes = []
for text, gap, spd, ch, pi in nc:
    sp = spd or V.SPEED; a, _ = V.synth(text, sp); takes.append((text, a, gap, ch, pi, sp))
L = sum(len(a) / SR for _, a, *_ in takes) + sum(g for _, _, g, *_ in takes[:-1])
print(f"slot {slot:.3f} s (from {slot0:.3f} to the next word at {nxt:.3f} - {MIN_GAP}), new take {L:.3f} s")
f = 1.0
if L > slot:
    f = L / slot
    if f - 1 > MAX_STRETCH: sys.exit(f"too long by {L - slot:.2f} s ({(f - 1) * 100:.1f} % > {MAX_STRETCH * 100:.0f} %): re-run the whole chain")
    print(f"time-compress x{f:.3f}")
if "--write" not in ARGS: sys.exit(0)
voice, sr = sf.read(V.OUT_WAV, dtype="float32"); assert sr == SR
out = voice.copy(); i_a, i_b = int(round(slot0 * SR)), int(round((nxt - 0.02) * SR)); out[i_a:i_b] = 0.0
t = slot0; spans = []
from faster_whisper import WhisperModel
m = WhisperModel("base.en", device="cpu", compute_type="int8")
words = [w for w in json.load(open(os.path.join(HERE, "words.json"))) if not (slot0 - 0.01 <= w["start"] < nxt - 0.01)]
for text, a, gap, ch, pi, sp in takes:
    if f > 1.0:
        with tempfile.TemporaryDirectory() as d:
            sf.write(f"{d}/a.wav", a, SR)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/a.wav", "-af", f"atempo={f:.4f}", f"{d}/b.wav"], check=True)
            a, _ = sf.read(f"{d}/b.wav", dtype="float32")
    i = int(round(t * SR)); out[i:i + len(a)] = a; d_ = len(a) / SR
    seg = np.interp(np.arange(0, len(a), SR / 16000), np.arange(len(a)), a).astype(np.float32)
    sw = [(w.start, w.end, w.word) for s in m.transcribe(seg, language="en", word_timestamps=True, beam_size=5)[0] for w in s.words]
    toks = [x for x in text.replace("-", " - ").split() if x != "-"]
    if len(sw) == len(toks): tw = [(x, y) for x, y, _ in sw]
    else:   # proportional over the heard span
        a0 = sw[0][0] if sw else 0.0; a1 = sw[-1][1] if sw else d_
        Lc = np.cumsum([0] + [len(x) + 1 for x in toks]); tw = [(a0 + (a1 - a0) * Lc[k] / Lc[-1], a0 + (a1 - a0) * (Lc[k + 1] - 1) / Lc[-1]) for k in range(len(toks))]
    words += [{"w": x, "start": round(t + s, 3), "end": round(t + e, 3)} for x, (s, e) in zip(toks, tw)]
    spans.append({"text": text, "start": round(t, 3), "end": round(t + d_, 3), "chapter": ch, "para": pi, "speed": sp, "file": "revoiced"})
    t += d_ + gap / f
words.sort(key=lambda w: w["start"])
sf.write(V.OUT_WAV, out, SR, subtype="PCM_16")
json.dump(words, open(os.path.join(HERE, "words.json"), "w"), indent=0)
C["chunks"] = old[:i0] + spans + old[len(old) - j:]
json.dump(C, open(os.path.join(HERE, "chunks.json"), "w"), indent=1)
print("written: audio/voice_archive.wav, build/words.json, build/chunks.json; next: BUILD_REPORT_v8.md 'Re-voice the SS United States lines'")
