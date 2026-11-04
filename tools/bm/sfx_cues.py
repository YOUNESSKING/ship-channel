"""Collect sound-effect cues from the built map scenes -> build/sfx_cues.json (absolute video times).

usage (from the project folder): python3 tools/sfx_cues.py
Every scene calls SFX(kind, t) (lib/battle.js) for blasts, shots and stamps. This loads each
scenes/NAME/index.html in headless Chrome, reads the cues from <html data-sfx>, shifts them by the
scene's start in the narration, and drops cues that fall inside ARCHIVE paragraphs (not on screen).
The picture is not affected, so scenes do not need re-rendering when only cues change: rebuild them
with build_scene.py and run this again.
"""
import glob, html, json, os, re, subprocess

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
os.chdir(ROOT)
CHROME = (glob.glob("/root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell")
          or ["/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"])[0]
paras = json.load(open("audio/timing.json"))["paragraphs"]
archive = [(p["start"], p["end"] + 0.6) for p in paras if p["tag"].startswith("ARCHIVE")]
cues = []
for page in sorted(glob.glob("scenes/*/index.html")):
    name = page.split("/")[1]
    if name.startswith("test"):  # test clips overlap real scenes in time; they use make_clip.py
        continue
    tjs = open(f"scenes/{name}/timing.js").read()
    st = json.loads(tjs[tjs.index("=") + 1:].strip().rstrip(";"))
    # take the scene's start from the CURRENT audio/timing.json (owner 2026-10-09: after the hook was re-voiced 7 s shorter, the
    # scenes built earlier still carried the old abs_start and every bomb/gun/plane sound of moves 1-3 landed ~7 s late)
    first = next(iter(st["paras"]))
    cur = {p["tag"].split("|")[0].replace("MAP:", "").replace("ARCHIVE:", "").strip(): p["start"] for p in paras}
    if first in cur and abs(cur[first] - st["abs_start"]) > 0.01:
        print(f"{name:14s} start {st['abs_start']} -> {cur[first]} (timing.json changed since the scene was built)")
        st["abs_start"] = cur[first]
    dom = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                          "--virtual-time-budget=3000", "--dump-dom", "file://" + os.path.abspath(page)],
                         capture_output=True, text=True, timeout=120).stdout
    m = re.search(r'<html[^>]*data-sfx="([^"]*)"', dom)
    found = json.loads(html.unescape(m.group(1))) if m else []
    n = 0
    for kind, t in found:
        if 0 <= t <= st["duration"]:
            a = round(st["abs_start"] + t, 2)
            if not any(s <= a < e for s, e in archive):
                cues.append([a, kind, name]); n += 1
    print(f"{name:14s} {n:4d} cues")
cues.sort()
os.makedirs("build", exist_ok=True)
json.dump(cues, open("build/sfx_cues.json", "w"), indent=0)
print("total", len(cues), "-> build/sfx_cues.json")
