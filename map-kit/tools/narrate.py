"""Generate narration per script paragraph with Kokoro; write voice.wav + timing.json."""
import json, re, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

VOICE = sys.argv[1] if len(sys.argv) > 1 else "am_michael"
SPEED = 1.0
import os
PROJ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SCRIPT = os.path.join(PROJ, "script.md")
OUT = os.path.join(PROJ, "audio")
MODELS = os.environ.get("KOKORO_DIR", ".")  # folder with kokoro-v1.0.onnx + voices-v1.0.bin
GAP_PARA, GAP_SECTION, GAP_SENT = 0.6, 0.8, 0.28
# pronunciation fixes (spoken only; timing.json keeps the script text)
SAY = {}  # e.g. {"Tarleton": "Tarlton"}: spoken respellings; check with k.tokenizer.phonemize(word, "en-us")

k = Kokoro(os.path.join(MODELS, "kokoro-v1.0.onnx"), os.path.join(MODELS, "voices-v1.0.bin"))
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
        # one clip per sentence -> sentence-level timing for B.at()
        sents, pos, parts, pt = [], 0, [], 0.0
        for m in re.finditer(r"[^.!?]+[.!?]+[\"']?\s*", spoken + " "):
            sent = m.group(0).strip()
            if not sent:
                continue
            say = sent
            for a, b in SAY.items():
                say = say.replace(a, b)
            a_, sr = k.create(say, voice=VOICE, speed=SPEED, lang="en-us")
            if parts:
                parts.append(np.zeros(int(sr * GAP_SENT), dtype=a_.dtype)); pt += GAP_SENT
            sents.append([spoken.index(sent, pos), round(t + pt, 2), round(t + pt + len(a_) / sr, 2)])
            pos = sents[-1][0] + len(sent)
            parts.append(a_); pt += len(a_) / sr
        audio = np.concatenate(parts)
        dur = len(audio) / sr
        timing.append({"section": name, "tag": tag, "start": round(t, 2), "end": round(t + dur, 2), "text": spoken, "sents": sents})
        chunks += [audio, np.zeros(int(sr * GAP_PARA), dtype=audio.dtype)]
        t += dur + GAP_PARA
        print(f"{t:7.1f}s  {tag[:60]}", flush=True)
    chunks.append(np.zeros(int(sr * GAP_SECTION), dtype=np.float32))
    t += GAP_SECTION
import os; os.makedirs(OUT, exist_ok=True)
sf.write(f"{OUT}/voice.wav", np.concatenate(chunks), sr)
json.dump({"voice": VOICE, "speed": SPEED, "duration": round(t, 2), "paragraphs": timing}, open(f"{OUT}/timing.json", "w"), indent=1)
print("total", round(t, 1), "s")
