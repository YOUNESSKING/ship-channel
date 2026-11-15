"""v8 pronunciation gate, step 4 (tts/PRONUNCIATION.md): every hard name of the Oriskany script said once by the Archive voice,
with the same fixes as build/voice.py. Out: videos/oriskany/voice_sample/names_archive.mp3"""
import os, subprocess, sys, numpy as np, soundfile as sf
sys.argv = sys.argv[:1]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import voice as V
NAMES = ["The USS Oriskany.", "Okaloosa County.", "MiG-fifteens.", "Porgies.", "Bremerton.", "Escambia.", "Pensacola.",
         "Corpus Christi.", "Beaumont.", "Mare Island.", "Tonkin.", "Hanoi.", "Stockdale.", "McCain.", "Essex-class.", "Her keel.",
         "Gustav.", "Skyhawk.", "Vermilion.", "PCBs."]
sr = 24000; parts = []
for n in NAMES:
    a, _ = V.synth(n, V.SPEED); parts += [a, np.zeros(int(0.12 * sr), np.float32)]
out = os.path.join(V.ROOT, "videos/oriskany/voice_sample/names_archive")
sf.write(out + ".wav", np.concatenate(parts), sr)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".wav", "-c:a", "libmp3lame", "-b:a", "160k", out + ".mp3"], check=True)
os.remove(out + ".wav")
print(out + ".mp3", round(sum(len(p) for p in parts) / sr, 2), "s")
