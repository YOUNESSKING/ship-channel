"""Generate narration per script paragraph with Kokoro; write voice.wav + timing.json."""
import json, re, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
sys.path.insert(0, "/home/user/battle-maps/arnold/tools")
from tts_names import speak  # names: tools/tts_names.py

VOICE = sys.argv[1] if len(sys.argv) > 1 else "am_michael"
SPEED = 1.0
SCRIPT = "/home/user/battle-maps/arnold/script.md"
OUT = "/home/user/battle-maps/arnold/audio"
GAP_PARA, GAP_SECTION = 0.6, 0.8

k = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
text = open(SCRIPT).read()
sections = text.split("\n## ")[1:]
sr, chunks, timing, t = 24000, [], [], 0.0
for si, sec in enumerate(sections):
    name = sec.split("\n")[0]
    for p in sec.split("\n\n"):
        if not p.startswith("["):
            continue
        tag = re.match(r"^\[([^\]]*)\]", p).group(1)
        spoken = re.sub(r"^\[[^\]]*\]\s*", "", p).strip()
        audio, sr = speak(k, spoken, VOICE, SPEED)
        dur = len(audio) / sr
        timing.append({"section": name, "tag": tag, "start": round(t, 2), "end": round(t + dur, 2), "text": spoken})
        chunks += [audio, np.zeros(int(sr * GAP_PARA), dtype=audio.dtype)]
        t += dur + GAP_PARA
        print(f"{t:7.1f}s  {tag[:60]}", flush=True)
    chunks.append(np.zeros(int(sr * GAP_SECTION), dtype=np.float32))
    t += GAP_SECTION
import os; os.makedirs(OUT, exist_ok=True)
sf.write(f"{OUT}/voice.wav", np.concatenate(chunks), sr)
json.dump({"voice": VOICE, "speed": SPEED, "duration": round(t, 2), "paragraphs": timing}, open(f"{OUT}/timing.json", "w"), indent=1)
print("total", round(t, 1), "s")
