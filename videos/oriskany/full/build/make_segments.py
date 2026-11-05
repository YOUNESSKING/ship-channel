"""Step 2C: build every FILM and PHOTO segment of the full Oriskany video from build/segments.json
(written by make_shotlists.py) with the archive_shots engine, exactly as test_v4/build/films.py / shots.py do, ARCHIVE_GRADE=ship.

  film   {"reel": "<NARA id>" | "<source stem>", "reel_in": s, "dur": s, "label": ...}
         source = footage/src/film/nara_<reel>.mp4 for NARA reels, footage/src/film/<reel>.mp4 for the generic US-Gov b-roll
         (NOAA / NASA / DVIDS / MARAD, FOOTAGE_LIST "Generic US Government b-roll"). Internal cuts are skipped by film_shot.
  photo  footage/src/photos/nara_<id>.jpg (or <stem>.jpg), 2.5D depth move.
Resumable: an existing output is skipped (delete it, or pass its file name, to rebuild). Missing sources are listed, not fatal.

  ARCHIVE_GRADE=ship python3 build/make_segments.py [film|photo] [file.mp4 ...]
Writes build/films.py-style cut lists for tools/film/make_paperwork.py: build/films.py (FILMS) and build/shots.py (SHOTS)."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/maps"))
os.environ.setdefault("ARCHIVE_GRADE", "ship")
import archive_shots as A
FT = os.path.join(ROOT, "videos/oriskany/footage/src")
OUT = os.path.join(FULL, "segments"); os.makedirs(OUT, exist_ok=True)
ENC = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "veryfast", "-r", "30"]
W, H = 1920, 1080
SEG = json.load(open(os.path.join(HERE, "segments.json")))
FW = json.load(open(os.path.join(HERE, "film_windows.json")))
args = sys.argv[1:]
kinds = [a for a in args if a in ("film", "photo")] or ["film", "photo"]
only = [a for a in args if a.endswith(".mp4")]


def film_src(reel):
    return os.path.join(FT, "film", f"nara_{reel}.mp4" if reel.isdigit() else f"{reel}.mp4")


def tag_png(text, path):
    """small burned-in source tag, top-left (generic US-Gov b-roll is NEVER the Oriskany: the tag stays on for the whole shot)"""
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype(A.FONT, 30); im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x, y = 54, 44; bb = d.textbbox((x, y), text, font=f)
    d.rectangle((bb[0] - 14, bb[1] - 9, bb[2] + 14, bb[3] + 9), fill=(8, 10, 12, 150))
    d.text((x, y), text, font=f, fill=(240, 236, 226, 235)); im.save(path)


def add_tag(out, text):
    import subprocess
    tp = out + ".tag.png"; tag_png(text, tp); tmp = out + ".t.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-loop", "1", "-i", tp, "-filter_complex", "[0:v][1:v]overlay=0:0:shortest=1",
                    *ENC, tmp], check=True)
    os.replace(tmp, out); os.remove(tp)


def still_shot(s, out):
    """v4: a slowly moving still of one frame of an already rendered map / hero segment (backgrounds under cards, the June 2005
    tow map under the $800,000 number). No re-grade (the map look is final). Frame = s["at"] seconds into segments/<src>, or "end"."""
    import subprocess
    src = os.path.join(OUT, s["src"])
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())
    at = d - 0.45 if s["at"] == "end" else float(s["at"])
    png = out + ".still.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.3f}", "-i", src, "-frames:v", "1", png], check=True)
    n = max(2, round(s["dur"] * 30)); mv = s.get("move", "in"); q = f"(on/{n - 1})"
    z, x = {"in": (f"1+0.07*{q}", "(iw-iw/zoom)/2"), "out": (f"1.07-0.07*{q}", "(iw-iw/zoom)/2"),
            "left": ("1.07", f"(iw-iw/zoom)*(1-{q})"), "right": ("1.07", f"(iw-iw/zoom)*{q}"),
            "in_s": (f"1+0.03*{q}", "(iw-iw/zoom)/2")}[mv]   # in_s: a gentle push that keeps a map's corner labels whole
    y = "(ih-ih/zoom)/2"
    vf = (f"scale=3840:2160,zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={W}x{H}:fps=30")
    if s.get("under"):   # under a card: soften the map / document so its own labels never compete with the card text
        vf += ",gblur=sigma=9,eq=brightness=-0.06:saturation=0.85"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", png, "-vf", vf, "-frames:v", str(n), *ENC, out], check=True)
    os.remove(png)


def photo_src(pid):
    for n in (f"nara_{pid}.jpg", f"{pid}.jpg", f"{pid}.png"):
        p = os.path.join(FT, "photos", n)
        if os.path.exists(p): return p
    return None


films, shots, missing = [], [], []
for s in SEG:
    if s["kind"] == "still":
        out = os.path.join(OUT, s["file"])
        if (only and s["file"] in only) or (not only and not os.path.exists(out)):
            if "still" in kinds or not [a for a in args if a in ("film", "photo", "still")]:
                t = time.time(); still_shot(s, out); print(f"{s['file']} ok ({time.time() - t:.0f}s)", flush=True)
        continue
    if s["kind"] not in kinds: continue
    out = os.path.join(OUT, s["file"])
    if s["kind"] == "film":
        clip_in = FW.get(s["clip"], {}).get("clip_in", 0.0)
        films.append((s["file"][:-4], s["clip"], round(s["reel_in"] - clip_in, 2), s["dur"], s.get("label") or s.get("tag") or ""))
    else:
        shots.append((s["file"][:-4], s["photo"], s["dur"], s["move"], [0.5, 0.45], bool(s.get("depth")), s.get("label"), s.get("shake")))
    if only and s["file"] not in only: continue
    if os.path.exists(out) and not only: continue
    t = time.time()
    if s["kind"] == "film":
        src = film_src(s["reel"])
        if not os.path.exists(src): missing.append((s["file"], src)); continue
        sh = {"film": src, "ss": s["reel_in"], "grade": "ship"}
        if s.get("label"): sh["label"] = s["label"]
        if s.get("fit"): sh["fit"] = s["fit"]
        if s["reel"] == "39085": sh["crop"] = "1440:1080:240:0"   # 208-UN-177 is pillarboxed inside 1920x1080 (as cut_clips.sh / film_windows.py)
        if s["reel"] == "87411": sh["crop"] = "666:452:22:14"     # v4 (critic A N2): the 1969 aerials carry film-gate slivers at both edges (the right one drifts in up to ~10 px)
        if s.get("clip") == "b3_aerial_underway2_1969.mp4": sh["crop"] = "612:440:26:20"   # this section's gate edge drifts ~60 px in from the right
        if s.get("slow"):   # a short cut-free window played slowed (test v4 f04 recipe): build the source length, then stretch
            import subprocess
            src_d = round(s["dur"] / s["slow"], 3); A.film_shot(sh, src_d, out, W, H, ENC); tmp = out + ".slow.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf", f"setpts={s['slow']}*PTS,fps=30", *ENC, "-t", str(s["dur"]), tmp], check=True)
            os.replace(tmp, out)
        else:
            A.film_shot(sh, s["dur"], out, W, H, ENC)
        if s.get("tag") and os.environ.get("BURN_TAG") == "1": add_tag(out, s["tag"])   # v2: tags are drawn on top by build_chapter (shot "tag")
    else:
        src = photo_src(s["photo"])
        if not src: missing.append((s["file"], s["photo"] + (" (fallback: " + s["fallback"] + ")" if s.get("fallback") else ""))); continue
        sh = {"photo": src, "move": s["move"], "focus": [0.5, 0.45], "depth": bool(s.get("depth")), "grade": "ship"}
        if s.get("label"): sh["label"] = s["label"]
        A.photo_shot(sh, s["dur"], out, W, H, ENC)
    print(f"{s['file']} ok ({time.time() - t:.0f}s)", flush=True)

# cut lists for make_paperwork.py (literal lists, read with ast; ss = offset from the FOOTAGE_LIST clip in-point)
if set(kinds) == {"film", "photo"}:
    open(os.path.join(HERE, "films.py"), "w").write(
        '"""Generated by make_segments.py: film segments on screen (id, clip, ss from the FOOTAGE_LIST in-point, dur, label)."""\nFILMS = [\n'
        + "".join(f" {f!r},\n" for f in films) + "]\n")
    open(os.path.join(HERE, "shots.py"), "w").write(
        '"""Generated by make_segments.py: photo segments (id, photo id, dur, move, focus, depth, label, shake)."""\nSHOTS = [\n'
        + "".join(f" {x!r},\n" for x in shots) + "]\nMONTAGE = None\nFILMS = []\n")
for f, m in missing: print("MISSING", f, m)
