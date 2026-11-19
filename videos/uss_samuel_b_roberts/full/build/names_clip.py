"""v8 pronunciation gate, step 4 (tts/PRONUNCIATION.md): every hard name of the USS Ranger script said once by the Archive voice,
with the same fixes as build/voice.py. Out: videos/uss_samuel_b_roberts/voice_sample/names_sbr.mp3"""
import os, subprocess, sys, numpy as np, soundfile as sf
sys.argv = sys.argv[:1]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import voice as V
NAMES = ["The USS Ranger.", "Bremerton, Washington.", "Puget Sound.", "International Shipbreaking.", "Brownsville, Texas.", "Coronado.", "North Island.", "Paramount.", "Newport News, Virginia.", "Admiral Arthur Radford.", "The Forrestal class.", "Norfolk Naval Shipyard.", "Charles Booth.", "Cape Horn.", "The Gulf of Tonkin.", "The A-7 Corsair Two.", "The Arabian Sea.", "Desert Storm.", "Somalia.", "Operation Restore Hope.", "The Naval Vessel Register.", "The Intrepid.", "The Midway.", "Fairview, Oregon.", "The Columbia River.", "Portland.", "The Saratoga.", "The Constellation.", "The Kitty Hawk.", "The Crosby Leader.", "South Padre Island.", "The USS Lexington Museum.", "Corpus Christi, Texas.", "Independence."]
sr = 24000; parts = []
for n in NAMES:
    a, _ = V.synth(n, V.SPEED); parts += [a, np.zeros(int(0.4 * sr), np.float32)]
out = os.path.join(V.ROOT, "videos/uss_samuel_b_roberts/voice_sample/names_sbr")
sf.write(out + ".wav", np.concatenate(parts), sr)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".wav", "-c:a", "libmp3lame", "-b:a", "160k", out + ".mp3"], check=True)
os.remove(out + ".wav")
print(out + ".mp3", round(sum(len(p) for p in parts) / sr, 2), "s")
