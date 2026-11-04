"""v3 sound: battle-maps locked chain (tools/sound). Steps: sfx_cues.py -> audio/sfx.wav ; make_music_bed.py -> audio/music_bed.wav ;
mix_clip.py (music 0.08 ducked, SFX full level ducked lightly, limiter 0.5, two-pass loudnorm -14 / TP -1.5 / LRA 11, AAC 192k).
MUSIC=path swaps the theme (default: Chris Zabriskie, "Stories About the World That Once Was", CC BY 4.0)."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
V = os.path.join(HERE, ".."); SND = os.path.join(ROOT, "tools/sound")
MUSIC = os.environ.get("MUSIC", os.path.join(ROOT, "assets/music/candidates/zabriskie/neptuneflux-01.m4a"))
subprocess.run(["python3", os.path.join(HERE, "sfx_cues.py")], check=True)
subprocess.run(["python3", os.path.join(SND, "make_music_bed.py"), f"{V}/audio/music_bed.wav", "53.6", MUSIC, os.environ.get("MUSIC_IN", "0")], check=True)
subprocess.run(["python3", os.path.join(SND, "mix_clip.py"), f"{V}/chapter/render_c01.mp4", f"{V}/audio/voice.wav", f"{V}/audio/sfx.wav",
                f"{V}/audio/music_bed.wav", f"{V}/oriskany_test_v3.mp4", f"{V}/audio/mix.wav"], check=True)
