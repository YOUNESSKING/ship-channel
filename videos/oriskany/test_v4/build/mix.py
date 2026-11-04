"""v4 sound (copy of test_v3/build/mix_v2.py adapted to v4 shots): sfx_cues_v4.py -> make_music_bed.py -> mix_clip.py v2
(voice stem chain, MUSIC_VOL 0.08 + MUSIC_TRIM_DB -6 ducked, unducked punch stem, oversampled limiter + linear loudnorm)
-> measure_mix.py -> check_sound_lock.py --render (fails on dynamic loudnorm, LRA < 5, beats < +3 LU, cue > 3 frames off).
Out: oriskany_test_v4.mp4 (git-ignored), audio/mix/ stems + master.json + measure.json. MUSIC=path swaps the theme."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
V = os.path.abspath(os.path.join(HERE, "..")); SND = os.path.join(ROOT, "tools/sound"); WK = f"{V}/audio/mix"
MUSIC = os.environ.get("MUSIC", os.path.join(ROOT, "assets/music/candidates/zabriskie/neptuneflux-01.m4a"))
OUT = f"{V}/oriskany_test_v4.mp4"
py = lambda *a: subprocess.run([sys.executable, *a], check=True)
os.makedirs(WK, exist_ok=True)
py(os.path.join(HERE, "sfx_cues_v4.py"))
py(os.path.join(SND, "make_music_bed.py"), f"{V}/audio/music_bed.wav", "50.2", MUSIC, os.environ.get("MUSIC_IN", "0"))
py(os.path.join(SND, "mix_clip.py"), "--video", f"{V}/chapter/render_c01.mp4", "--voice", f"{V}/audio/voice.wav",
   "--chunks", f"{HERE}/chunks.json", "--sfx", f"{V}/audio/sfx.wav", "--beds", f"{V}/audio/beds.wav", "--punch", f"{V}/audio/punch.wav",
   "--music", f"{V}/audio/music_bed.wav", "--out", OUT, "--work", WK)
py(os.path.join(SND, "measure_mix.py"), "--out", OUT, "--work", WK, "--words", f"{HERE}/words.json",
   "--cues", f"{HERE}/sfx_placed.json", "--ref", os.environ.get("REF_DIR", "/home/user/younessking/battle-maps/reference"))
py(os.path.join(SND, "check_sound_lock.py"), "--render", f"{WK}/master.json", "--cues", f"{HERE}/sfx_placed.json",
   "--measure", f"{WK}/measure.json")
