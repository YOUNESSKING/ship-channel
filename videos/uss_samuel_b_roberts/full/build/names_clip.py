"""v8 pronunciation gate, step 4 (tts/PRONUNCIATION.md): every hard name of the USS Samuel B. Roberts script said once by the Archive voice,
with the same fixes as build/voice.py. Out: videos/uss_samuel_b_roberts/voice_sample/names_sbr.mp3"""
import os, subprocess, sys, numpy as np, soundfile as sf
sys.argv = sys.argv[:1]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import voice as V
NAMES = ["The USS Samuel B. Roberts.", "The Sammy B.", "Samar.", "Leyte.", "Leyte Gulf.", "Taffy Three.", "Vice Admiral Takeo Kurita.", "The Yamato.", "The Kongo.", "The Chokai.", "The San Bernardino Strait.", "The Philippine Sea.", "Lieutenant Commander Robert Copeland.", "Tacoma, Washington.", "Rear Admiral Clifton Sprague.", "The Johnston, the Hoel and the Heermann.", "Ernest Evans.", "Coxswain Samuel Booker Roberts.", "Guadalcanal.", "Point Cruz.", "Gunner's Mate Paul Carr.", "Checotah, Oklahoma.", "The Gambier Bay.", "The Saint Lo.", "Brown Shipbuilding, Houston.", "John C. Butler class.", "Victor Vescovo.", "The Limiting Factor.", "EYOS Expeditions.", "Parks Stephenson.", "Jeremie Morizet.", "The Petrel.", "Samuel Cox.", "Mount Kilimanjaro.", "Operation Praying Mantis.", "The Spirit of the Sammy B."]
sr = 24000; parts = []
for n in NAMES:
    a, _ = V.synth(n, V.SPEED); parts += [a, np.zeros(int(0.4 * sr), np.float32)]
out = os.path.join(V.ROOT, "videos/uss_samuel_b_roberts/voice_sample/names_sbr")
sf.write(out + ".wav", np.concatenate(parts), sr)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".wav", "-c:a", "libmp3lame", "-b:a", "160k", out + ".mp3"], check=True)
os.remove(out + ".wav")
print(out + ".mp3", round(sum(len(p) for p in parts) / sr, 2), "s")
