"""Narrate text in the owner's cloned voice (Chatterbox, MIT). usage: clone_voice.py REF.wav OUT.wav "text" [exaggeration] [cfg]
Long text is split into sentences and joined with short pauses."""
import re, sys, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
ref, out, text = sys.argv[1:4]
ex = float(sys.argv[4]) if len(sys.argv) > 4 else 0.45
cfg = float(sys.argv[5]) if len(sys.argv) > 5 else 0.45
torch.manual_seed(7)
m = ChatterboxTTS.from_pretrained(device="cpu")
parts, gap = [], torch.zeros(1, int(m.sr * 0.35))
for s in [x.strip() for x in re.split(r"(?<=[.!?])\s+", text) if x.strip()]:
    parts += [m.generate(s, audio_prompt_path=ref, exaggeration=ex, cfg_weight=cfg), gap]
torchaudio.save(out, torch.cat(parts, dim=1), m.sr)
print("wrote", out)
