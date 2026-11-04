"""v3 NEW SOUND remix: same picture (the video stream of oriskany_test_v3.mp4, copied), same voice + timing
(audio/voice.wav, build/chunks.json), new chain (tools/sound v2) + real Epidemic SFX + the Zabriskie music.
Steps: sfx_cues_v2.py -> make_music_bed.py -> mix_clip.py -> measure_mix.py -> check_sound_lock.py --render.
Out: oriskany_test_v3_newsound.mp4 (git-ignored), audio/v2/ stems + master.json + measure.json."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
V = os.path.abspath(os.path.join(HERE, "..")); SND = os.path.join(ROOT, "tools/sound"); WK = f"{V}/audio/v2"
MUSIC = os.environ.get("MUSIC", os.path.join(ROOT, "assets/music/candidates/zabriskie/neptuneflux-01.m4a"))
OUT = f"{V}/oriskany_test_v3_newsound.mp4"
py = lambda *a: subprocess.run([sys.executable, *a], check=True)
os.makedirs(WK, exist_ok=True)
py(os.path.join(HERE, "sfx_cues_v2.py"))
py(os.path.join(SND, "make_music_bed.py"), f"{V}/audio/music_bed.wav", "53.6", MUSIC, os.environ.get("MUSIC_IN", "0"))
py(os.path.join(SND, "mix_clip.py"), "--video", f"{V}/oriskany_test_v3.mp4", "--voice", f"{V}/audio/voice.wav",
   "--chunks", f"{HERE}/chunks.json", "--sfx", f"{V}/audio/sfx_v2.wav", "--beds", f"{V}/audio/beds_v2.wav", "--punch", f"{V}/audio/punch_v2.wav",
   "--music", f"{V}/audio/music_bed.wav", "--out", OUT, "--work", WK)
py(os.path.join(SND, "measure_mix.py"), "--out", OUT, "--work", WK, "--words", f"{HERE}/words.json",
   "--cues", f"{HERE}/sfx_placed_v2.json", "--ref", os.environ.get("REF_DIR", "/home/user/younessking/battle-maps/reference"))
py(os.path.join(SND, "check_sound_lock.py"), "--render", f"{WK}/master.json", "--cues", f"{HERE}/sfx_placed_v2.json",
   "--measure", f"{WK}/measure.json")
