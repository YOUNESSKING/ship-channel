#!/usr/bin/env python3
"""Builds videos/video01/publish/{description.txt,PUBLISHING_GUIDE.pdf} (+ key frames) from the final master.
Run again whenever the master or chapters file changes. Needs ffmpeg/ffprobe and node+playwright."""
import os, re, json, subprocess, base64, html, sys
S = "/tmp/claude-0/-home-user/fcc32437-de47-5115-87a3-5e7427ef5ff7/scratchpad"
R = "/home/user/prehistory-channel"
OUT = f"{R}/videos/video01/publish"
FINAL = os.environ.get("FINAL", f"{S}/v01/final/v01_FINAL_1080p.mp4")
PREVIEW = f"{S}/v01/final/v01_full_preview_720p.mp4"
CH = next((p for p in (f"{S}/v01/final/v01_FINAL_chapters.txt", f"{S}/v01/final/v01_chapters.txt") if os.path.exists(p)))
have_final = os.path.exists(FINAL)
SRC = FINAL if have_final else PREVIEW
TITLE = "How Long You'd Last in Every Ice Age Ocean?"
ALTS = [("How Long Would You Last in Every Ice Age Ocean?", "the owner's original wording; same skeleton without the contraction"),
        ("Could You Survive Every Ice Age Ocean?", "Fossil's predator-video skeleton (Could You Survive Every ...?)"),
        ("Which Ice Age Ocean Could You Survive?", "Fossil's human-species skeleton (Which ... Could You ...?)")]
e = html.escape
GOFILE = os.environ.get("GOFILE_LINK", "GOFILE_LINK_HERE")  # main session: GOFILE_LINK=<url> python3 tools/build_publish_guide.py

def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True).stdout

# ---------- chapters ----------
chs = []
for l in open(CH):
    m = re.match(r"\s*(\d+):(\d\d)\s+(.+)", l)
    if m: chs.append((int(m[1]) * 60 + int(m[2]), m[3].strip()))
assert chs[0][0] == 0
for a, b in zip(chs, chs[1:]): assert b[0] - a[0] >= 10, (a, b)
assert len({t for t, _ in chs}) == len(chs)
fmt = lambda s: f"{s//60}:{s%60:02d}"
chap_txt = "\n".join(f"{fmt(t)} {n}" for t, n in chs)

# ---------- file facts ----------
def probe():
    j = json.loads(sh(f'ffprobe -v error -print_format json -show_format -show_streams "{SRC}"'))
    v = next(s for s in j["streams"] if s["codec_type"] == "video"); a = next(s for s in j["streams"] if s["codec_type"] == "audio")
    n, d = map(int, v["r_frame_rate"].split("/"))
    dur = float(j["format"]["duration"]); size = int(j["format"]["size"])
    loud = sh(f'ffmpeg -nostats -i "{SRC}" -af ebur128=peak=true -f null - 2>&1 | tail -14')
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", loud); P = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", loud)
    return dict(res=f'{v["width"]}x{v["height"]}', fps=round(n/d, 3), vc=f'{v["codec_name"]} {v.get("profile","")} {v.get("pix_fmt","")}',
                ac=f'{a["codec_name"]} {a.get("sample_rate")} Hz {a.get("channels")} ch', size=f"{size/1e6:.0f} MB", dur=dur,
                lufs=I[-1] if I else "?", peak=P[-1] if P else "?", br=f'{int(j["format"]["bit_rate"])//1000} kbps')
F = probe()
F["len"] = f'{int(F["dur"])//60}:{int(F["dur"])%60:02d}'

# ---------- key frames (first minute) ----------
os.makedirs(f"{OUT}/frames", exist_ok=True)
kf = []
for i, t in enumerate([1, 6, 11, 16, 21, 26, 31, 36, 46, 58]):
    p = f"{OUT}/frames/kf_{i:02d}.jpg"
    sh(f'ffmpeg -y -v error -ss {t} -i "{SRC}" -frames:v 1 -vf scale=480:-2 -q:v 4 "{p}"'); kf.append((t, p))
from PIL import Image
for k in "AB":  # phone-size previews are rebuilt from whatever thumb_A/B.jpg exist now
    Image.open(f"{OUT}/thumb_{k}.jpg").convert("RGB").resize((168, 94), Image.LANCZOS).save(f"{OUT}/thumb_{k}_168.png")
def b64(p): return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()

# ---------- description ----------
DESC = f"""{TITLE}

Fall into the North Atlantic 20,000 years ago and you have maybe fifteen to thirty minutes before you pass out. But sea level was over 120 metres lower, and some Ice Age seas were not what you think: one was a lake, one was so salty the plankton gave up, and one was dry land.

I drop you 100 yards offshore, with no boat and no wetsuit, into ten Ice Age oceans: the North Atlantic, the Southern Ocean, the Bering Sea, the North Sea, the Black Sea, the Mediterranean, the Red Sea, the Gulf of Carpentaria, the Gulf of Mexico and the Sunda Shelf. For each one I check the same five things: how cold the water is, whether you can drink it, whether you can get out, whether there is food, and what wants to eat you. Then it goes on the tier board, from minutes to days.

The safest place to fall into an Ice Age ocean was where the ocean had turned into land. Which ocean would you last longest in, and which would you never try? Tell me in the comments.

Chapters
{chap_txt}

Credits
Music and sound effects: original, made for this video. Narration: AI voice. Visuals: AI-generated images and video clips, animated maps and graphics made for this video. Map terrain data: Mapzen / AWS Terrain Tiles; ice extent approximate. The animals and scenes are artistic reconstructions, not photographs.

Business: [OWNER FILLS IN BUSINESS EMAIL]

#IceAge #Prehistory #Paleontology
"""
assert len(re.findall(r"#\w+", DESC)) == 3 and "http" not in DESC and "www." not in DESC
open(f"{OUT}/description.txt", "w").write(DESC)

TAGS = ["ice age", "prehistory", "prehistoric", "ice age ocean", "ice age oceans", "how long would you last", "survival", "sea level",
        "woolly mammoth", "orca", "leopard seal", "Doggerland", "Beringia", "Black Sea", "Red Sea", "Sundaland", "ice age animals", "prehistoric animals"]
assert 12 <= len(TAGS) <= 18 and len(",".join(TAGS)) <= 500
CLOSING_Q = "Do you agree? Do you disagree? Let me know."
PINNED = "Which ocean would you last longest in, and which one would you never jump into? Do you agree with the tier board? Do you disagree? Let me know."

FACTS = [
 ("Sea level 'over a hundred and twenty metres lower'", "Approximate (estimates run about 120-130 m at the peak). Fine as a round number."),
 ("North Atlantic: 'more than twelve degrees colder than today', 'about zero degrees', winter sea ice 'past Iceland'", "Single source family (GLAMAP 2000: cooling up to more than 12 C west of Ireland; winter ice south of Iceland/Faroes). The exact degrees are an estimate, not measured."),
 ("'Fifteen, thirty minutes before you pass out' at about 0 C; cold shock in the first minute; hands stop closing after ten minutes", "Rule-of-thumb charts (Engineering ToolBox table, 1-10-1 rule). The original USCG / Golden & Tipton table was not opened; the charts are called optimistic by the safety literature."),
 ("Southern Ocean: sea ice 'roughly twice as big', ice cliffs 'in a lot of places', 'taller than a house'", "Twice = Gersonde 2005 (+100 %); another study says +60-70 %. Cliff height is unverified."),
 ("Leopard seal 'three metres long'", "OPEN ITEM: size not re-checked for this video (adult females are commonly given as about 3 to 3.5 m). Check one reference before publishing."),
 ("Leopard seals and orcas in the Ice Age Southern / North Atlantic", "OPEN ITEM: orcas in the Last Glacial Maximum North Atlantic are plausible, not proven. Leopard seal presence is an inference."),
 ("Kirsty Brown 2003; Paul Nicklen 'four days'", "Verified (BAS / peer-reviewed account; National Geographic). Nicklen's 'she was trying to feed me' is his own reading."),
 ("Bering: 'stayed dry for something like twenty thousand years'; 'about a thousand kilometres north to south'", "Check: Farmer et al. 2023 gives about 36,000 to 11,000-13,000 years ago, i.e. roughly 23-25 thousand years. The 1,000 km figure is unverified."),
 ("Bering: sea ice 'stuck around all year, even in summer'", "Single study (Brigham-Grette 2010, southeastern Bering Sea). Says 'seems to'."),
 ("First Americans spent thousands of years in Beringia", "Genetic hypothesis (the 'standstill'), debated. Narration already hedges."),
 ("Doggerland: 'Britain was basically abandoned', no humans", "Supported (no evidence of people for thousands of years around the peak); exact start of the gap not confirmed."),
 ("Doggerland: 'wolves, cave hyenas? Also yes'", "OPEN ITEM: cave hyenas may have died out in Britain/NW Europe before 20,000 years ago. Check, or cut 'cave hyenas'."),
 ("Baltic 'under kilometres of ice'; Channel dry 'a big river valley'", "Ice margin in the southern North Sea is poorly constrained; the Baltic claim is general knowledge, not re-sourced here."),
 ("Black Sea: 'basically nothing' salt, 'about 1' vs today's '18' on screen", "Soulet 2010 (about 1 psu); other studies disagree. Lake level (-45 to -120 m) is debated. Winter ice not stated (no source)."),
 ("Georgian cave flax 'about thirty thousand years ago'", "Single archaeological source (Dzudzuana); not re-verified in FACTCHECK. Check the date."),
 ("Mediterranean: 'maybe around ten degrees' in winter, 'mid to high teens' in summer", "UNCERTAIN: proxy ranges only (Hayes 2005); numbers are estimates."),
 ("Red Sea: 'warm, in the twenties', 'over fifty' vs 'around thirty-five', plankton 'vanished' in parts", "Salinity above 50 is supported (Hemleben 1996, Biton 2008); the warm temperature is not sourced. A 2025 study says corals survived, which the script mentions."),
 ("Carpentaria: lake 'hundreds of kilometres across', warm 'mid-twenties', ocean broke back 'around ten thousand years ago'", "Size possibly about 600 x 300 km (one estimate); temperature not sourced; transgression about 10.8 thousand years ago (so 'around ten' is a little low)."),
 ("Saltwater crocodiles in Lake Carpentaria / Sunda", "Narration says 'we don't know for sure'. No Ice Age fossil of the saltwater crocodile found for either place."),
 ("Gulf of Mexico: 'around 23 degrees', Florida 'twice as wide', river mouth drinkable", "One sediment core (warm-season biased); the drinkable river mouth is our inference (the river is fresh), not a measurement."),
 ("New Mexico footprints suggest people", "Disputed (dating arguments); narration hedges."),
 ("Sundaland 'about 1.8 million square kilometres, bigger than Alaska'", "Area verified (1.8-1.85 million); vegetation (rainforest or savanna) and 'rising water pushed populations' are debated."),
 ("Megalodon 'missed the Ice Age by about three and a half million years'", "Extinction date is debated (about 3.6 million years ago in recent work)."),
 ("Final tier board (minutes / overnight / hours / days)", "Our judgement, not a measurement."),
]

CHECKLIST = ["Play the master once all the way through (picture, sound, no black frames, end screen).",
 "Upload v01_FINAL_1080p_graded.mp4 in YouTube Studio (Create, Upload videos).",
 "Paste the title; paste description.txt (first line is the title: delete it from the description box).",
 "Upload thumb_A.jpg; add thumb_B.jpg in Test & compare.",
 "Add tags (copy from section 8), Education category, not made for kids.",
 "Fill the business email placeholder in the description.",
 "Altered or synthetic content: Yes. Add captions check (hard names list).",
 "Add the end screen and the chapters are picked up from the description (check 0:00 first).",
 "Schedule (see section 8). Then post and pin the comment.",
 "Check CTR and 30-second retention at 24-48 hours; at 3, 7 and 28 days save the numbers in the video folder. If CTR is under 2 % after about 1,000 impressions: switch to the other thumbnail first."]

css = """
@page{size:A4;margin:14mm}
body{font:13px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#111}
h1{font-size:26px;margin:0 0 4px}h2{font-size:18px;margin:22px 0 6px;border-bottom:2px solid #e10600;padding-bottom:3px;page-break-after:avoid}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #bbb;padding:4px 7px;text-align:left;vertical-align:top}th{background:#eee}
.cover{text-align:center;page-break-after:always}.cover img{width:100%;border:1px solid #000}
.strip{display:grid;grid-template-columns:repeat(5,1fr);gap:4px}.strip img{width:100%}.strip div{font-size:10px;text-align:center}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}.two img{width:100%;border:1px solid #000}
pre{white-space:pre-wrap;background:#f5f5f5;border:1px solid #ccc;padding:8px;font:12px/1.4 ui-monospace,Menlo,monospace}
.box{border:3px solid #e10600;padding:8px 12px;background:#fff6f5;page-break-inside:avoid}.open{color:#b00000;font-weight:700}
.pend{background:#ffe9a8;padding:2px 6px}small{color:#555}
"""
rows = lambda items: "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in items)
pend = "" if have_final else '<p class="pend">The final master was not ready when this page was built; the values below are from the 720p preview and must be re-checked (re-run tools/build_publish_guide.py).</p>'
facts_rows = "".join(f'<tr><td>{e(a)}</td><td class="{"open" if b.startswith("OPEN") else ""}">{e(b)}</td></tr>' for a, b in FACTS)
H = f"""<!doctype html><html><head><meta charset=utf-8><style>{css}</style></head><body>
<div class=cover><h1>Publishing guide, Video 01</h1><p><b>{e(TITLE)}</b><br>Prehistory channel, series: "Every Ice Age ..."</p>
<img src="{b64(OUT+'/thumb_A.jpg')}"><p><small>Thumbnail A (main). Made with vidIQ generate_thumbnail, using 4 of Fossil's highest-view thumbnails as style references (brief: research/publishing/VIDIQ_THUMB_BRIEF.md).</small></p></div>

<h2>2. The finished video</h2>{pend}
<table>{rows([("File","v01_FINAL_1080p_graded.mp4"),("Resolution / frame rate",f'{F["res"]} / {F["fps"]} fps'),("Video codec",F["vc"]),("Audio codec",F["ac"]),("Bitrate / size",f'{F["br"]} / {F["size"]}'),("Length",F["len"]),("Loudness",f'{F["lufs"]} LUFS integrated (target -14), true peak {F["peak"]} dBFS'),
("Voice","ElevenLabs v4 voice \"Will\" (paid plan, commercial use allowed)"),("Music","Original, made in-house for this video (no licence needed)"),("Sound effects","Synthesised in-house (no licence needed)"),
("AI video","Wan 2.2, Kling 2.5 (fal.ai), Seedance 2 (via vidIQ)"),("AI images","Z-Image Turbo, Seedream 4.5, Nano Banana Pro"),("Maps","Mapzen / AWS Terrain Tiles. Credit line on screen: Terrain: Mapzen / AWS Terrain Tiles, ice extent approximate"),
("Download","Download: "+GOFILE)])}</table>

<h2>3. Chapters</h2><table><tr><th>Start</th><th>Title</th></tr>{"".join(f"<tr><td>{fmt(t)}</td><td>{e(n)}</td></tr>" for t,n in chs)}</table>
<small>From the chapters file of the final build; first at 0:00, each at least 10 s, no duplicate times (checked by the script).</small>

<h2>4. Key frames, first minute</h2><div class=strip>{"".join(f'<div><img src="{b64(p)}">{t} s</div>' for t,p in kf)}</div>
<p><small>The hook: cold North Atlantic water, 15-30 minutes until you pass out, "one was a lake, one was dry land". Check the hook at a glance before uploading.</small></p>

<h2>5. Title</h2>
<p><b style="font-size:17px">{e(TITLE)}</b> &nbsp; (LOCKED, {len(TITLE)} characters)</p>
<p><b>Score:</b> not scored. The vidIQ balance was already under the 100-credit floor, so no vidIQ calls were allowed. The pattern is Fossil's winning title (the 12M-view "How Long You'd Last in Every Prehistoric Era"). Score it in vidIQ (type long) before uploading if you want a number.</p>
<table><tr><th>Alternative</th><th>Why</th></tr>{rows(ALTS)}</table>
<p><small>Rules applied: no negation, clear and true, no "forgotten / almost / nearly", promise paid in the first 30 seconds (the hook states the cold-water clock and "one was a lake... one was dry land").</small></p>

<h2>6. Thumbnails</h2><div class=two>
<div><img src="{b64(OUT+'/thumb_A.jpg')}"><p><b>A (main): "15 Minutes"</b> (red 15, white Minutes), vidIQ. Text type: time stake, the exact type of Fossil's 12M-view "12 Minutes". Completes the title "How long...".<br><b>Promise paid in the video:</b> "fifteen, thirty minutes before you pass out" at 0:07 (on screen as "15-30 minutes"); you alone in the freezing North Atlantic from 0:00; the orca threat ("if nothing finds you first") at about 0:30.<br><b>Checked:</b> orca with white-dot eye, Ice Age sea ice, the viewer's frozen hand; text reads exactly "15 Minutes"; no boats, logos or extra text; readable at 168x94. vidIQ self-score 53 (it wants one focal point; Fossil's 12M thumbnail splits attention the same way).</p></div>
<div><img src="{b64(OUT+'/thumb_B.jpg')}"><p><b>B (Test &amp; compare): "Adopt You?"</b> (white Adopt, red You?). Text type: a question twist, like Fossil's "Too Easy?" / "New King?": a leopard seal holding a bloody penguin, offering it to you.<br><b>Checked:</b> leopard seal with spotted throat and wide gape, Adélie penguin, sea ice; no people, no modern objects, no text in the AI picture; readable at 168x94. True to the video: the Paul Nicklen penguin story and "the seal adopts you" (2:35).</p></div></div>
<p><small>B is from the thumbnail study (Nano Banana Pro with Fossil style references; text added by tools/make_thumb.py, Anton font). B's promise: the leopard seal appears at 2:05, the lunge at 2:10, "the seal adopts you" at 2:35. A third option for Test &amp; compare: thumb_A_fal_draft.jpg (same orca idea, fal version). Study: research/publishing/THUMBNAIL_STUDY.md.</small></p><p>Both are 1280x720 JPEG. Use A as main and B in Test &amp; compare.</p>
<div class=two><img src="{b64(OUT+'/thumb_A_168.png')}" style="width:168px"><img src="{b64(OUT+'/thumb_B_168.png')}" style="width:168px"></div>

<h2>7. Description, ready to paste</h2><pre>{e(DESC)}</pre>
<small>Same text in description.txt. No links; exactly 3 hashtags; names and numbers are those said in the narration.</small>

<h2>8. Upload settings</h2><table>{rows([
("Tags (comma separated)", ", ".join(TAGS)),("Category","Education"),("Audience","Not made for kids"),
("Altered or synthetic content","YES (realistic AI animals and scenes). Answer the same on every video of the series."),
("Captions","Auto-captions. Check these names: Doggerland, Beringia, Sahul, Sundaland, Carpentaria, Kirsty Brown, Paul Nicklen, Danube, Dnieper, Caucasus, Gibraltar, Sardinia, Corsica, Iberia, Adriatic, Mississippi, sturgeon, Mapzen"),
("Pinned comment (the closing question)", PINNED),("Closing line in the video",CLOSING_Q),("Schedule","Owner decides. Suggested: a weekday evening, US time (Fossil publishes about 19:00-23:00 UTC)."),("Business email","Owner fills in the placeholder")])}</table>

<h2>9. Upload checklist</h2><ol>{"".join(f"<li>{e(c)}</li>" for c in CHECKLIST)}</ol>

<h2>10. Facts to double-check before publishing</h2><div class=box><p>Every approximate, single-source or second-hand number in the narration (from FACTCHECK.md and the script). Items in red are known open items.</p><table><tr><th>Said in the video</th><th>Status</th></tr>{facts_rows}</table></div>
</body></html>"""
open(f"{OUT}/PUBLISHING_GUIDE.html", "w").write(H)
open("/tmp/pdf_build.js", "w").write(f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{OUT}/PUBLISHING_GUIDE.html');await p.pdf({{path:'{OUT}/PUBLISHING_GUIDE.pdf',format:'A4',printBackground:true,margin:{{top:'14mm',bottom:'14mm',left:'14mm',right:'14mm'}}}});await b.close()}})()""")
print(subprocess.run(f"cd {R} && NODE_PATH=$(npm root -g) node /tmp/pdf_build.js", shell=True, capture_output=True, text=True))
print("final" if have_final else "PREVIEW ONLY", F)
