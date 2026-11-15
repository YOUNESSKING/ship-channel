"""Upload kit (HTML -> PDF, Oriskany format): title, thumbnails, settings, description (from YOUTUBE_DESCRIPTION_DRAFT.md), tags,
pinned comment, checklist. usage: python3 build/make_kit.py MASTER.mp4"""
import html, os, re, subprocess, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE)
MASTER = sys.argv[1]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MASTER]).decode())
mm = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
D = open(os.path.join(FULL, "YOUTUBE_DESCRIPTION_DRAFT.md")).read()
desc = D.split("\n---\n")[1].strip() + "\n\n#MallowsBay #GhostFleet #NavalHistory"
CSS = open(os.path.join(os.path.dirname(os.path.dirname(FULL)), "oriskany/full/upload_kit/upload_kit.html")).read()
CSS = CSS[CSS.index("<style>"):CSS.index("</style>") + 8]
tags = ("Mallows Bay, ghost fleet, Mallows Bay ghost fleet, Potomac River shipwrecks, Mallows Bay Potomac River National Marine Sanctuary, "
        "WWI wooden ships, Emergency Fleet Corporation, US Shipping Board, wooden steamships, ship graveyard, shipwreck documentary, "
        "Maryland history, Washington DC history, abandoned ships, naval history, World War 1 ships, Bethlehem Steel, NOAA sanctuary")
H = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Mallows Bay YouTube upload kit</title>{CSS}</head><body>
<h1>Mallows Bay: YouTube upload kit</h1>
<div class="sub">Video file: {html.escape(os.path.basename(MASTER))} ({mm(round(dur))}, 1080p) · Fleet's End video #2</div>
<h2>1. Title</h2>
<div class="title">100+ Ships Are Rotting 30 Miles From the White House</div>
<p class="note">Not scored in vidIQ yet (scoring costs credits: owner approval needed). Alternates for Test &amp; Compare: “America Built a Fleet to Beat the U-Boats. Now It's Rotting in This Bay.” · “Why Nobody Could Get Rid of America's Ghost Fleet”. Rule: 3 titles scored ≥ 85 before publishing.</p>
<h2>2. Thumbnails</h2>
<div class="thumbs">
<figure><img src="../../thumbnails/T1_ghost_fleet_1936.jpg"><figcaption><b>T1, upload with this one</b><br>T1_ghost_fleet_1936.jpg</figcaption></figure>
<figure><img src="../../thumbnails/T2_ghost_fleet_today.jpg"><figcaption>T2, Test &amp; Compare<br>T2_ghost_fleet_today.jpg</figcaption></figure>
<figure><img src="../../thumbnails/T3_set_on_fire.jpg"><figcaption>T3, Test &amp; Compare<br>T3_set_on_fire.jpg</figcaption></figure>
</div><p class="note">Judge the Test &amp; Compare winner on day 7–14, not day 1. Space this video ≥ 2 days from the Oriskany upload.</p>
<h2>3. Upload settings</h2><table><tr><th>Setting</th><th>Value</th></tr>
<tr><td>Altered or synthetic content</td><td class="tick">YES (AI narration; maps and graphics made for this channel)</td></tr>
<tr><td>Made for kids</td><td>No</td></tr><tr><td>Category</td><td>Education</td></tr><tr><td>Language / caption language</td><td>English / English</td></tr>
<tr><td>License</td><td>Standard YouTube License</td></tr><tr><td>Chapters</td><td>Automatic from the timestamps in the description</td></tr>
<tr><td>End screen</td><td>The last 18 s are an end-screen map (right half clear): add “subscribe” + one “best for viewer” video</td></tr>
<tr><td>Comments</td><td>On. Post and pin the comment in section 6 right after publishing</td></tr></table>
<h2 class="page-break">4. Description (copy everything in the box)</h2><div class="box">{html.escape(desc)}</div>
<h2 class="page-break">5. Tags</h2><div class="box">{html.escape(tags)}</div>
<h2>6. First comment (post it, then pin it)</h2><div class="box">A fleet built to beat the U-boats, sold for about $3,200 a ship, burned, and then protected by law. 🌊

What should happen to what is left of it?
🛶 Save it (keep it as it is, a sanctuary)
🌿 Let the river finish the job

Have you paddled through Mallows Bay? Tell us what you saw. Spotted a mistake? Reply with a source and we'll pin a correction.</div>
<h2>7. Before you press Publish</h2><table>
<tr><td>☐</td><td>Watched the master once; names sound right (Nanjemoy, Accomac, Potomac, Widewater, Quantico, Idamont, PEPCO)</td></tr>
<tr><td>☐</td><td>3 titles scored ≥ 85 in vidIQ (ask before spending credits)</td></tr>
<tr><td>☐</td><td>“Altered or synthetic content” = Yes</td></tr><tr><td>☐</td><td>Thumbnail T1 uploaded; T2 + T3 added in Test &amp; Compare</td></tr>
<tr><td>☐</td><td>Description pasted; chapters show in the preview</td></tr><tr><td>☐</td><td>Tags pasted; first comment posted and pinned</td></tr></table>
</body></html>"""
out = os.path.join(FULL, "upload_kit/upload_kit.html"); open(out, "w").write(H)
pdf = os.path.join(FULL, "upload_kit/MallowsBay_YouTube_Upload_Kit.pdf")
chrome = (glob.glob("/root/.cache/hyperframes/chrome/**/chrome", recursive=True) + glob.glob("/opt/pw-browsers/**/chrome", recursive=True) + [None])[0]
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", f"--print-to-pdf={pdf}", "--no-pdf-header-footer", "file://" + out], check=True, capture_output=True)
print("pdf", pdf, mm(dur))
