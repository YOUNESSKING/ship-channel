"""Kokoro narration for the 1-min test. Each chunk is synthesized separately so its start time is known
exactly; visuals are timed to these chunk starts (numbers land on their own chunk)."""
import json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
VOICE, SPEED = "am_michael", 0.95
# (id, text, pause after in seconds)
CHUNKS = [
 ("c01", "Twenty-four miles off the Florida coast,", 0.15),
 ("c02", "two hundred and twelve feet down,", 0.15),
 ("c03", "lies an American aircraft carrier.", 0.35),
 ("c04", "Nearly nine hundred feet long.", 0.3),
 ("c05", "She fought in two wars.", 0.45),
 ("c06", "No enemy sank her.", 0.35),
 ("c07", "The United States Navy did.", 0.25),
 ("c08", "On purpose.", 0.6),
 ("c09", "On May seventeenth, two thousand six,", 0.15),
 ("c10", "engineers set off explosive charges inside her hull.", 0.45),
 ("c11", "Thirty-seven minutes later,", 0.15),
 ("c12", "she was gone.", 0.6),
 ("c13", "It had taken three years", 0.1),
 ("c14", "and about twenty million dollars", 0.1),
 ("c15", "just to get her ready to sink.", 0.6),
 ("c16", "So why would the Navy pay millions to send one of its own carriers to the bottom of the sea,", 0.15),
 ("c17", "instead of keeping her,", 0.15),
 ("c18", "or simply cutting her up for scrap?", 0.6),
 ("c19", "The answer starts with what was hidden inside her.", 0.6),
 ("c20", "And this month, a second famous American ship is scheduled to go down off the same coast,", 0.15),
 ("c21", "for the very same reason.", 1.2),
]
k = Kokoro(os.path.join(ROOT, "tts/kokoro-v1.0.onnx"), os.path.join(ROOT, "tts/voices-v1.0.bin"))
LEAD = 0.6  # silence before first word (first frame = map)
sr = 24000; parts = [np.zeros(int(sr * LEAD), np.float32)]; t = LEAD; timing = []
for cid, text, gap in CHUNKS:
    a, sr = k.create(text, voice=VOICE, speed=SPEED, lang="en-us")
    a = a.astype(np.float32); d = len(a) / sr
    timing.append({"id": cid, "start": round(t, 3), "end": round(t + d, 3), "text": text})
    parts += [a, np.zeros(int(sr * gap), np.float32)]; t += d + gap
    print(f"{cid} {t:6.2f}  {text}", flush=True)
out = os.path.join(HERE, "../audio"); os.makedirs(out, exist_ok=True)
sf.write(os.path.join(out, "voice.wav"), np.concatenate(parts), sr)
json.dump({"voice": VOICE, "speed": SPEED, "lead": LEAD, "duration": round(t, 3), "chunks": timing},
          open(os.path.join(HERE, "timing.json"), "w"), indent=1)
print("total", round(t, 2))
