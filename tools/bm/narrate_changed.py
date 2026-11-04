"""Re-voice only the paragraphs whose text changed; reuse the rest from the current voice.wav.

usage: run from /home/user/battle-maps/tts:  python3 /home/user/battle-maps/goosegreen/tools/narrate_changed.py
Same voice/speed/gaps as narrate.py (read from audio/timing.json). Rewrites audio/voice.wav + timing.json.
"""
import json, os, re
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
old = json.load(open(f"{ROOT}/audio/timing.json"))
wav, sr = sf.read(f"{ROOT}/audio/voice.wav", dtype="float32")
by_text = {p["text"]: wav[int(p["start"] * sr):int(p["end"] * sr)] for p in old["paragraphs"]}
VOICE, SPEED, GAP_PARA, GAP_SECTION = old["voice"], old["speed"], 0.6, 0.8
k = None
import ast
import sys; sys.path.insert(0, f"{ROOT}/tools"); from tts_names import speak  # same names as narrate.py
sections = open(f"{ROOT}/script.md").read().split("\n## ")[1:]
chunks, timing, t, redone = [], [], 0.0, 0
for sec in sections:
    name = sec.split("\n")[0]
    for p in sec.split("\n\n"):
        if not p.startswith("["):
            continue
        tag = re.match(r"^\[([^\]]*)\]", p).group(1)
        spoken = re.sub(r"^\[[^\]]*\]\s*", "", p).strip()
        if spoken in by_text:
            audio = by_text[spoken]
        else:
            k = k or Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
            audio, sr2 = speak(k, spoken, VOICE, SPEED)
            assert sr2 == sr
            audio = audio.astype("float32"); redone += 1
            print("re-voiced:", tag[:50], flush=True)
        dur = len(audio) / sr
        timing.append({"section": name, "tag": tag, "start": round(t, 2), "end": round(t + dur, 2), "text": spoken})
        chunks += [audio, np.zeros(int(sr * GAP_PARA), dtype="float32")]
        t += dur + GAP_PARA
    chunks.append(np.zeros(int(sr * GAP_SECTION), dtype="float32"))
    t += GAP_SECTION
sf.write(f"{ROOT}/audio/voice.wav", np.concatenate(chunks), sr)
json.dump({"voice": VOICE, "speed": SPEED, "duration": round(t, 2), "paragraphs": timing}, open(f"{ROOT}/audio/timing.json", "w"), indent=1)
print(f"re-voiced {redone} paragraphs, total {t:.1f} s")
