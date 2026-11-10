"""v8: write the chapter timestamps from chapters.json into YOUTUBE_DESCRIPTION_DRAFT.md and upload_kit/upload_kit.html, then
print the upload kit to its PDF (headless Chrome). usage: python3 build/desc_times.py MASTER.mp4"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE)
MASTER = sys.argv[1]
CH = json.load(open(os.path.join(FULL, "chapters.json")))["chapters"]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MASTER]).decode())
mmss = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
NAMES = {"c01": None, "c07": "The Real Reason"}   # c01 keeps each file's own first title
rows = [(c["key"], mmss(c["start"]), NAMES.get(c["key"], c["title"])) for c in CH]


def fill(text, first):
    lines = [f"0:00 {first}"] + [f"{t} {n}" for k, t, n in rows[1:]]
    return re.sub(r"0:00 [^\n]+\n(?:\d+:\d\d [^\n]+\n){5,}", "\n".join(lines) + "\n", text, count=1)


D = os.path.join(FULL, "YOUTUBE_DESCRIPTION_DRAFT.md")
s = open(D).read()
s = fill(s, re.search(r"\n0:00 ([^\n]+)\n", s).group(1))
s = re.sub(r"^# YouTube description draft:[^\n]*", f"# YouTube description draft: USS Oriskany full video ({os.path.basename(MASTER)}, {mmss(dur)}.{int(round(dur % 1 * 10)) % 10}; "
           "chapter timestamps regenerated from chapters.json for the v8 Archive-voice re-time)", s, count=1)
open(D, "w").write(s)
H = os.path.join(FULL, "upload_kit/upload_kit.html")
h = open(H).read()
h = fill(h, re.search(r"\n0:00 ([^\n]+)\n", h).group(1))
h = re.sub(r"Video file: [^ ]+ \([0-9:]+, 1080p\)", f"Video file: Oriskany_Nobody_Wanted_This_Aircraft_Carrier_FINAL_v8_1080p.mp4 ({mmss(round(dur))}, 1080p)", h)
open(H, "w").write(h)
pdf = os.path.join(FULL, "upload_kit/Oriskany_YouTube_Upload_Kit.pdf")
chrome = next((p for p in ["google-chrome", "chromium", "chromium-browser"] if subprocess.run(["which", p], capture_output=True).returncode == 0), None)
if chrome is None:
    import glob
    chrome = (glob.glob("/root/.cache/hyperframes/chrome/**/chrome", recursive=True) + glob.glob("/root/.cache/ms-playwright/**/chrome", recursive=True) + [None])[0]
if chrome:
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", f"--print-to-pdf={pdf}", "--no-pdf-header-footer", "file://" + H],
                   check=True, capture_output=True)
    print("pdf", pdf)
else: print("no chrome found: PDF not rebuilt")
print("\n".join(f"{t} {n or 'Hook'}" for k, t, n in rows), "| length", mmss(dur))
