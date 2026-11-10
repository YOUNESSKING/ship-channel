"""Design a channel voice by blending Kokoro voice styles (Apache-2.0 weights, free, commercial use OK).
Kokoro voices are style vectors; a weighted average gives a new, consistent voice that no other channel has as-is.
usage: python3 tts/design_voice.py OUT_DIR    -> one sample per candidate + candidates.json
"""
import json
import os
import sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
k = Kokoro(os.path.join(HERE, "kokoro-v1.0.onnx"), os.path.join(HERE, "voices-v1.0.bin"))

# Candidates for a calm, serious naval-documentary narrator (weights sum to 1).
CANDIDATES = {
    "1_admiral":    ({"am_michael": 0.55, "bm_george": 0.45}, 0.92),   # US base, British gravitas
    "2_deep_water": ({"am_onyx": 0.50, "am_michael": 0.50}, 0.90),     # deeper, slower
    "3_archive":    ({"bm_fable": 0.40, "am_michael": 0.40, "bm_lewis": 0.20}, 0.92),  # storyteller
    "4_captain":    ({"am_fenrir": 0.35, "am_michael": 0.40, "bm_george": 0.25}, 0.93),  # firmer, more edge
}

# Oriskany hook, first lines (the phoneme fix keeps "Oriskany" said right).
TEXT = ("Right now, two hundred and twelve feet under the Gulf of Mexico, lies an aircraft carrier. "
        "No enemy sank her. The United States Navy did. On purpose. "
        "It took thirty-seven minutes. "
        "The answer is buried in her past. And in what was still inside her when she sank.")


def blend(mix):
    return sum(w * k.get_voice_style(v) for v, w in mix.items()).astype(np.float32)


meta = {}
for name, (mix, speed) in CANDIDATES.items():
    style = blend(mix)
    audio, sr = k.create(TEXT, voice=style, speed=speed, lang="en-us")
    sf.write(os.path.join(OUT, f"{name}.wav"), audio, sr)
    np.save(os.path.join(OUT, f"{name}_style.npy"), style)
    meta[name] = {"mix": mix, "speed": speed, "seconds": round(len(audio) / sr, 2)}
    print(name, meta[name], flush=True)
json.dump(meta, open(os.path.join(OUT, "candidates.json"), "w"), indent=1)
