"""Upload kit (HTML -> PDF, Oriskany format): title, thumbnails, settings, description (from YOUTUBE_DESCRIPTION_DRAFT.md), tags,
pinned comment, checklist. usage: python3 build/make_kit.py MASTER.mp4"""
import html, os, re, subprocess, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE)
MASTER = sys.argv[1]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MASTER]).decode())
mm = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
D = open(os.path.join(FULL, "YOUTUBE_DESCRIPTION_DRAFT.md")).read()
desc = D.split("\n---\n")[1].strip() + "\n\n#USSSamuelBRoberts #BattleOffSamar #NavalHistory"
tail = D.split("\n---\n")[2]
tags = tail.split("Tags (paste in the Tags field):", 1)[1].strip().split("\n")[0].strip() if "Tags (paste" in tail else ""
pinned = tail.split("Pinned comment (post right after upload):", 1)[1].strip().split("\n---")[0].strip() if "Pinned comment" in tail else ""
CSS = open(os.path.join(os.path.dirname(os.path.dirname(FULL)), "oriskany/full/upload_kit/upload_kit.html")).read()
CSS = CSS[CSS.index("<style>"):CSS.index("</style>") + 8]
H = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>USS Samuel B. Roberts YouTube upload kit</title>{CSS}</head><body>
<h1>USS Samuel B. Roberts: YouTube upload kit</h1>
<div class="sub">Video file: {html.escape(os.path.basename(MASTER))} ({mm(round(dur))}, 1080p) · Fleet's End video #5</div>
<h2>1. Title</h2>
<div class="title">This Tiny Warship Charged a Battleship Fleet. Now It's the Deepest Wreck Ever Found</div>
<p class="note">vidIQ score 98. Alternates: “They Found Her 22,000 Feet Down. This Is How She Got There” (97) · “The Deepest Shipwreck Ever Found Was a Tiny Ship That Charged Battleships” (93). The working title “The Deepest Shipwreck Ever Found” scored 83 (below the 85 floor). Not used: “...Charged the Yamato...” (overclaim: her torpedo run was at the cruisers). Before publishing, search the news once more for a deeper wreck. Details: script/TITLES_THUMBS.md.</p>
<h2>2. Thumbnails</h2>
<div class="thumbs">
<figure><img src="../../thumbnails/V1_22000_ft_down.jpg"><figcaption><b>V1 "22,000 FT DOWN", upload with this one</b><br>V1_22000_ft_down.jpg</figcaption></figure>
<figure><img src="../../thumbnails/V2_deepest_wreck.jpg"><figcaption>V2 "DEEPEST WRECK", Test &amp; Compare<br>V2_deepest_wreck.jpg</figcaption></figure>
<figure><img src="../../thumbnails/V3_they_charged.jpg"><figcaption>V3 "THEY CHARGED", Test &amp; Compare<br>V3_they_charged.jpg</figcaption></figure>
</div><p class="note">Judge the Test &amp; Compare winner on day 7–14, not day 1. Space this video ≥ 2 days from the USS Ranger / USS Nevada uploads (2–3 a week max).</p>
<h2>3. Upload settings</h2><table><tr><th>Setting</th><th>Value</th></tr>
<tr><td>Altered or synthetic content</td><td class="tick">YES (AI narration; maps and graphics made for this channel)</td></tr>
<tr><td>Made for kids</td><td>No</td></tr><tr><td>Category</td><td>Education</td></tr><tr><td>Language / caption language</td><td>English / English</td></tr>
<tr><td>License</td><td>Standard YouTube License</td></tr><tr><td>Chapters</td><td>Automatic from the timestamps in the description</td></tr>
<tr><td>End screen</td><td>The last 18 s are an end-screen map (right half clear): add “subscribe” + one “best for viewer” video</td></tr>
<tr><td>Comments</td><td>On. Post and pin the comment in section 6 right after publishing; reply to family/veteran stories in the first 48 h</td></tr></table>
<h2 class="page-break">4. Description (copy everything in the box)</h2><div class="box">{html.escape(desc)}</div>
<h2 class="page-break">5. Tags</h2><div class="box">{html.escape(tags)}</div>
<h2>6. First comment (post it, then pin it)</h2><div class="box">{html.escape(pinned)}</div>
<h2>7. Before you press Publish</h2><table>
<tr><td>☐</td><td>Watched the master once; names sound right (listen to voice_sample/names_sbr.mp3: Samar, Leyte, Kurita, Chokai, Kongo, Copeland, Checotah, Morizet, EYOS)</td></tr>
<tr><td>☐</td><td>“Altered or synthetic content” = Yes</td></tr><tr><td>☐</td><td>Thumbnail V1 uploaded; V2 + V3 added in Test &amp; Compare</td></tr>
<tr><td>☐</td><td>Description pasted; chapters show in the preview</td></tr><tr><td>☐</td><td>Tags pasted; first comment posted and pinned</td></tr></table>
</body></html>"""
out = os.path.join(FULL, "upload_kit/upload_kit.html"); open(out, "w").write(H)
pdf = os.path.join(FULL, "upload_kit/USSSamuelBRoberts_YouTube_Upload_Kit.pdf")
chrome = (glob.glob("/root/.cache/hyperframes/chrome/**/chrome", recursive=True) + glob.glob("/opt/pw-browsers/**/chrome", recursive=True) + [None])[0]
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", f"--print-to-pdf={pdf}", "--no-pdf-header-footer", "file://" + out], check=True, capture_output=True)
print("pdf", pdf, mm(dur))
