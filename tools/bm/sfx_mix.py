"""Render build/sfx_cues.json (from tools/sfx_cues.py) into one sound-effects track: build/sfx.wav.

usage (from the project folder): python3 tools/sfx_mix.py
Levels, clip variants and minimum gaps per cue kind live in tools/sfx_mix_lib.py (KINDS).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sfx_mix_lib as M

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
total = json.load(open("audio/timing.json"))["duration"]
cues = json.load(open("build/sfx_cues.json"))
n = M.render(cues, total, "build/sfx.wav")
print(f"placed {n} of {len(cues)} cues -> build/sfx.wav")
