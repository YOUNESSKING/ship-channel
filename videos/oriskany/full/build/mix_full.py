"""Assemble + mix the full Oriskany video (test v4 build/mix.py chain, whole video at once).
1. join chapter/render_c01..c07.mp4 frame-exact: chapter k gets round(end*30) - round(start*30) frames (trimmed or padded by
   cloning its last frame), so frame n of the join is narration time n/30 for the whole 14:45 (no drift at chapter joins)
2. build/sfx_full.py   -> audio/sfx.wav, punch.wav, beds.wav, build/sfx_placed.json (cues re-timed to the beat frames)
3. build/music_bed.py  -> audio/music_bed.wav (Zabriskie: main -> tension at c06 -> outro for the last 60 s)
4. tools/sound/mix_clip.py v2 (locked: voice stem chain, MUSIC_VOL 0.08 + MUSIC_TRIM_DB -6, sidechains, punch stem,
   oversampled limiter, two-pass LINEAR loudnorm -14 / TP -1.5) -> oriskany_full_v4.mp4 (v3 = owner ending cut 2026-11-05;
   v4 = SFX_FIX_v4 sound, owner 2026-11-05)
5. tools/sound/measure_mix.py + check_sound_lock.py --render (fails on a broken lock).
Resumable: the join is skipped when chapter/joined_silent.mp4 is newer than every chapter render. Run detached:
  nohup python3 build/mix_full.py > build/mix_full.log 2>&1 &"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
SND = os.path.join(ROOT, "tools/sound"); WK = os.path.join(FULL, "audio/mix"); OUT = os.path.join(FULL, "oriskany_full_v4.mp4")
# v4 = SFX_FIX_v4 sound (owner 2026-11-05: horn shorter + 6 dB quieter, cue rings capped; build/SFX_FIX_v4.md).
# AUDIO_ONLY=/path/test.mp4: sound-only test. Skips the join and muxes the full v4 mix onto a tiny colour proxy with exactly the
# frame count of the existing chapter/joined_silent.mp4 (or, if gone, of oriskany_full_v3.mp4) (so audio = video length), written to that path. No picture render.
AUDIO_ONLY = os.environ.get("AUDIO_ONLY")
FPS = 30
py = lambda *a: subprocess.run([sys.executable, *a], check=True)
KEYS = ["c01", "c02", "c03", "c04", "c05", "c06", "c07"]
CH = {k: json.load(open(os.path.join(FULL, "chapter", f"{k}.json"))) for k in KEYS}
JOIN = os.path.join(FULL, "chapter", "joined_silent.mp4")


def frames(p):
    return int(subprocess.check_output(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                                        "stream=nb_read_packets", "-of", "csv=p=0", p]).decode().strip())


def join():
    # c01 = the owner-approved test v4 hook PICTURE, exactly as approved (its first 1459 frames = 0-48.625 s; same voice recording,
    # word times equal to 1 ms). HOOK_SRC=render overrides with this build's own render_c01.mp4.
    hook = os.path.join(ROOT, "videos/oriskany/test_v4/oriskany_test_v4.mp4")
    renders = [hook if (k == "c01" and os.environ.get("HOOK_SRC") != "render") else os.path.join(FULL, "chapter", f"render_{k}.mp4") for k in KEYS]
    for r in renders:
        if not os.path.exists(r): sys.exit(f"missing {r}: run build/render_all.sh first")
    if os.path.exists(JOIN) and all(os.path.getmtime(JOIN) > os.path.getmtime(r) for r in renders) and \
            os.path.exists(os.path.join(HERE, "join_report.json")) and json.load(open(os.path.join(HERE, "join_report.json")))[0].get("source") == renders[0]:
        print("join up to date"); return
    lst, rep = [], []
    for k, r in zip(KEYS, renders):
        a = CH[k]["audio_offset"]; b = a + CH[k]["duration"]
        need = round(b * FPS) - round(a * FPS); have = frames(r)
        fixed = os.path.join(FULL, "chapter", f"fix_{k}.mp4")
        if have == need: lst.append(r)
        else:
            vf = f"tpad=stop_mode=clone:stop={max(0, need - have)},trim=end_frame={need},setpts=PTS-STARTPTS"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", r, "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                            "-pix_fmt", "yuv420p", "-r", str(FPS), fixed], check=True)
            assert frames(fixed) == need, (k, frames(fixed), need); lst.append(fixed)
        rep.append(dict(chapter=k, start=round(a, 3), frames_rendered=have, frames_wanted=need, source=r))
        print(rep[-1], flush=True)
    L = os.path.join(FULL, "chapter", "join_list.txt")
    open(L, "w").write("".join(f"file '{p}'\n" for p in lst))
    # re-encode the join once (chapter renders + fixes may differ in encoder settings): one clean stream, CFR 30
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", L, "-an", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart", JOIN + ".part.mp4"], check=True)
    os.replace(JOIN + ".part.mp4", JOIN)
    tot = round((CH["c07"]["audio_offset"] + CH["c07"]["duration"]) * FPS)
    print("joined", frames(JOIN), "frames (want", tot, ")")
    json.dump(rep, open(os.path.join(HERE, "join_report.json"), "w"), indent=1)
    for k in KEYS:   # v2: the frame-fixed copies are only needed for the concat (disk)
        f = os.path.join(FULL, "chapter", f"fix_{k}.mp4")
        if os.path.exists(f): os.remove(f)


if __name__ == "__main__":
    os.makedirs(WK, exist_ok=True)
    video = JOIN
    if AUDIO_ONLY:
        ref = JOIN if os.path.exists(JOIN) else os.path.join(FULL, "oriskany_full_v3.mp4")   # the v3 picture (same 25,968 frames)
        n = frames(ref); OUT = AUDIO_ONLY; video = AUDIO_ONLY + ".proxy.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s=64x36:r={FPS}", "-frames:v", str(n),
                        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", video], check=True)
        print("audio-only test on a", n, "frame proxy of", ref, flush=True)
    else:
        join()
    py(os.path.join(HERE, "sfx_full.py"))
    py(os.path.join(HERE, "music_bed.py"))
    A = os.path.join(FULL, "audio")
    py(os.path.join(SND, "mix_clip.py"), "--video", video, "--voice", f"{A}/voice.wav", "--chunks", f"{HERE}/chunks.json",
       "--sfx", f"{A}/sfx.wav", "--beds", f"{A}/beds.wav", "--punch", f"{A}/punch.wav", "--music", f"{A}/music_bed.wav",
       "--out", OUT, "--work", WK)
    py(os.path.join(SND, "measure_mix.py"), "--out", OUT, "--work", WK, "--words", f"{HERE}/words.json",
       "--cues", f"{HERE}/sfx_placed.json", "--ref", os.environ.get("REF_DIR", "/home/user/younessking/battle-maps/reference"))
    py(os.path.join(SND, "check_sound_lock.py"), "--render", f"{WK}/master.json", "--cues", f"{HERE}/sfx_placed.json",
       "--measure", f"{WK}/measure.json", "--words", f"{HERE}/words.json")
    if AUDIO_ONLY: os.remove(video)
    print("DONE", OUT)
