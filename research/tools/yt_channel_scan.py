"""Scan a YouTube channel's long videos with yt-dlp (no vidIQ needed). usage: python3 research/tools/yt_channel_scan.py @Handle [max_videos]
Writes research/competitors/<handle>.json (raw per-video data) and <handle>.md (table: views, x median, views/day, length, age, likes, comments).
Long-form = duration >= 480 s (Shorts and trailers dropped). Run from /home/user/battle-maps."""
import datetime, json, re, statistics, subprocess, sys, os
handle = sys.argv[1].lstrip("@"); N = int(sys.argv[2]) if len(sys.argv) > 2 else 120
url = f"https://www.youtube.com/@{handle}/videos"
flat = subprocess.run(["yt-dlp", "--flat-playlist", "--dump-json", "--playlist-end", str(N), url], capture_output=True, text=True, timeout=600).stdout
ids = [json.loads(l)["id"] for l in flat.splitlines() if l.strip().startswith("{")]
print(len(ids), "videos listed", flush=True)
rows = []
for i in ids:
    r = subprocess.run(["yt-dlp", "--skip-download", "--dump-json", "--no-warnings", f"https://www.youtube.com/watch?v={i}"], capture_output=True, text=True, timeout=180)
    try: d = json.loads(r.stdout)
    except Exception: print("fail", i, flush=True); continue
    rows.append({"id": i, "title": d.get("title"), "views": d.get("view_count"), "dur": d.get("duration"), "date": d.get("upload_date"), "likes": d.get("like_count"),
                 "comments": d.get("comment_count"), "channel": d.get("channel"), "subs": d.get("channel_follower_count"), "desc": (d.get("description") or "")[:600],
                 "thumb": d.get("thumbnail"), "chapters": [c.get("title") for c in (d.get("chapters") or [])]})
    print(rows[-1]["title"][:70], rows[-1]["views"], flush=True)
today = datetime.date.today()
L = [r for r in rows if (r["dur"] or 0) >= 480]
for r in L:
    r["age"] = max(1, (today - datetime.datetime.strptime(r["date"], "%Y%m%d").date()).days); r["vpd"] = round((r["views"] or 0) / r["age"])
med = statistics.median([r["views"] or 0 for r in L]) if L else 1
for r in L: r["x"] = round((r["views"] or 0) / med, 2)
json.dump({"handle": handle, "median": med, "videos": rows}, open(f"research/competitors/{handle}.json", "w"), indent=1)
L.sort(key=lambda r: -(r["views"] or 0))
mm = lambda s: f"{s // 60}:{s % 60:02d}"
out = [f"# {handle} ({rows[0]['channel'] if rows else ''}, subs {rows[0]['subs'] if rows else '?'}): scanned {today}", f"Long videos {len(L)}, median views {int(med):,}", "",
       "| Title | Views | x median | Views/day | Length | Age (d) | Likes | Comments |", "|---|---|---|---|---|---|---|---|"]
for r in L: out.append(f"| {r['title']} | {r['views']:,} | {r['x']} | {r['vpd']:,} | {mm(r['dur'])} | {r['age']} | {r['likes'] or ''} | {r['comments'] or ''} |")
open(f"research/competitors/{handle}.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
