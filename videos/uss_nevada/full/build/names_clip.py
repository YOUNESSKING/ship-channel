"""v8 pronunciation gate, step 4 (tts/PRONUNCIATION.md): every hard name of the USS Nevada script said once by the Archive voice,
with the same fixes as build/voice.py. Out: videos/uss_nevada/voice_sample/names_nevada.mp3"""
import os, subprocess, sys, numpy as np, soundfile as sf
sys.argv = sys.argv[:1]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import voice as V
NAMES = ["The USS Nevada.", "Bikini Atoll.", "The Marshall Islands.", "Operation Crossroads.", "Kwajalein.", "Oahu.", "Ford Island.", "Hospital Point.", "Waipio Point.", "Chief Boatswain Edwin Hill.", "The forecastle.", "Chief Quartermaster Sedberry.", "Ensign Taussig.", "Machinist Donald Ross.", "Attu, in the Aleutians.", "Utah Beach, Normandy.", "Cherbourg.", "Toulon.", "Iwo Jima.", "Okinawa.", "The transport Gilliam.", "The transport Carlisle.", "The cruiser Sakawa.", "The battleship Nagato.", "The Saratoga.", "Dave's Dream.", "Astoria, Pasadena and Iowa.", "Pacific Constructor.", "NOAA."]
sr = 24000; parts = []
for n in NAMES:
    a, _ = V.synth(n, V.SPEED); parts += [a, np.zeros(int(0.4 * sr), np.float32)]
out = os.path.join(V.ROOT, "videos/uss_nevada/voice_sample/names_nevada")
sf.write(out + ".wav", np.concatenate(parts), sr)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".wav", "-c:a", "libmp3lame", "-b:a", "160k", out + ".mp3"], check=True)
os.remove(out + ".wav")
print(out + ".mp3", round(sum(len(p) for p in parts) / sr, 2), "s")
