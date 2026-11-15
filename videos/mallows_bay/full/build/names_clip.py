"""v8 pronunciation gate, step 4 (tts/PRONUNCIATION.md): every hard name of the Mallows Bay script said once by the Archive voice,
with the same fixes as build/voice.py. Out: videos/mallows_bay/voice_sample/names_mallows.mp3"""
import os, subprocess, sys, numpy as np, soundfile as sf
sys.argv = sys.argv[:1]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import voice as V
NAMES = ["Mallows Bay.", "Nanjemoy.", "The Potomac River.", "Charles County, Maryland.", "Widewater, Virginia.", "Quantico.", "Alexandria.", "The Accomac.", "Theodore Ferris.", "The North Bend.", "Aberdeen, Washington.", "Bethlehem Steel.", "Idamont.", "PEPCO.", "Sandy Point.", "NOAA.", "Largemouth bass, striped bass, shad, herring.", "Herbert Hoover."]
sr = 24000; parts = []
for n in NAMES:
    a, _ = V.synth(n, V.SPEED); parts += [a, np.zeros(int(0.12 * sr), np.float32)]
out = os.path.join(V.ROOT, "videos/mallows_bay/voice_sample/names_mallows")
sf.write(out + ".wav", np.concatenate(parts), sr)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".wav", "-c:a", "libmp3lame", "-b:a", "160k", out + ".mp3"], check=True)
os.remove(out + ".wav")
print(out + ".mp3", round(sum(len(p) for p in parts) / sr, 2), "s")
