"""Turn a finished narration (e.g. Kokoro am_michael) into the owner's voice, keeping its exact pacing and timing.
usage: convert_voice.py IN.wav REF.wav OUT.wav     (Chatterbox voice conversion, MIT; runs in /home/user/cb-venv)
Works in ~20 s chunks cut at silences so long narrations fit in memory; timing.json stays valid.
Each converted chunk is cached in OUT.parts/ so a run killed by a reboot resumes where it stopped."""
import os, subprocess, sys, tempfile, torch, torchaudio
from chatterbox.vc import ChatterboxVC

src, ref, out = sys.argv[1:4]
vc = ChatterboxVC.from_pretrained("cpu")
vc.set_target_voice(ref)
wav, sr = torchaudio.load(src)
wav = wav.mean(0, keepdim=True)
# cut points: quietest 50 ms window between 15 s and 25 s into each chunk
win, pieces, i, k = int(sr * 0.05), [], 0, 0
parts = out + ".parts"; os.makedirs(parts, exist_ok=True)
while i < wav.shape[1]:
    if wav.shape[1] - i <= sr * 25:
        j = wav.shape[1]
    else:
        seg = wav[0, i + sr * 15:i + sr * 25]
        e = seg[: len(seg) // win * win].reshape(-1, win).pow(2).mean(1)
        j = i + sr * 15 + int(e.argmin()) * win + win // 2
    cache = f"{parts}/{k:04d}_{i}_{j}.wav"
    if os.path.exists(cache):
        y = torchaudio.load(cache)[0]
    else:
        tmp = tempfile.mktemp(suffix=".wav"); torchaudio.save(tmp, wav[:, i:j], sr)
        y = vc.generate(tmp).cpu()
        n = round((j - i) * vc.sr / sr)  # keep every chunk exactly as long as the original
        y = y[:, :n] if y.shape[1] >= n else torch.cat([y, torch.zeros(1, n - y.shape[1])], 1)
        torchaudio.save(cache, y, vc.sr); print("chunk", k, round(j / sr, 1), "s", flush=True)
    pieces.append(y); i = j; k += 1
torchaudio.save(out, torch.cat(pieces, 1), vc.sr)
print("wrote", out, round(sum(p.shape[1] for p in pieces) / vc.sr, 2), "s")
