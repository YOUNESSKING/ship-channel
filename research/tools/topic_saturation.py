"""How crowded is a topic on YouTube? For each query: top N search results (yt-dlp flat search, public metadata only),
count of videos >=100k and >=1M views, sum of the top-10 views, and how many use the 'Top 3 ... Tactical' format.
usage (from /home/user/battle-maps): python3 research/tools/topic_saturation.py  -> research/saturation/saturation.json + .md"""
import json, subprocess, sys, time
N = 30
TOPICS = {  # video: [commander query, battle/topic query]
 "Thomas (123k)": ["George H. Thomas general", "Battle of Chickamauga"],
 "Morgan (45k)": ["Daniel Morgan general", "Battle of Cowpens"],
 "2 Para (39k)": ["Goose Green battle 2 Para", "Falklands war Goose Green"],
 "Smith (2.2k)": ["O.P. Smith marine general", "Battle of Chosin Reservoir"],
 "Greene (3.4k)": ["Nathanael Greene general", "Battle of Guilford Courthouse"],
 "Patton (135, early)": ["George Patton general", "Battle of the Bulge Bastogne"],
 "Gavin (669)": ["James Gavin general", "Operation Market Garden"],
 "Collins (518)": ["J. Lawton Collins general", "Operation Cobra Normandy"],
 "WAIT Jackson": ["Stonewall Jackson", "Battle of Chancellorsville"],
 "WAIT Meade": ["George Meade general", "Battle of Gettysburg"],
 "WAIT Sherman": ["William Tecumseh Sherman", "Sherman's March to the Sea"],
 "WAIT Rokossovsky": ["Konstantin Rokossovsky", "Operation Bagration"],
 "WAIT Peng": ["Peng Dehuai", "Chinese intervention Korean War 1950"],
 "WAIT Cleburne": ["Patrick Cleburne", "Battle of Ringgold Gap"],
 "NEW Benedict Arnold": ["Benedict Arnold general", "Battle of Saratoga"],
 "NEW Francis Marion": ["Francis Marion Swamp Fox", "Francis Marion guerrilla war"],
 "NEW Anthony Wayne": ["Anthony Wayne general", "Battle of Stony Point"],
 "NEW Grant": ["Ulysses S. Grant general", "Vicksburg campaign"],
 "NEW Chesty Puller": ["Chesty Puller", "Battle for Henderson Field Guadalcanal"],
}
def search(q):
    for k in range(3):
        r = subprocess.run(["yt-dlp", "--flat-playlist", "-j", f"ytsearch{N}:{q}"], capture_output=True, text=True, timeout=180)
        rows = [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]
        if rows: return rows
        time.sleep(5)
    return []
out = {}
for name, qs in TOPICS.items():
    out[name] = {}
    for q in qs:
        rows = search(q)
        v = [(x.get("view_count") or 0, x.get("title", ""), x.get("channel", "")) for x in rows]
        vs = sorted([a for a, _, _ in v], reverse=True)
        out[name][q] = dict(n=len(v), over100k=sum(a >= 100_000 for a in vs), over1m=sum(a >= 1_000_000 for a in vs),
                            top10=sum(vs[:10]), top3=[(a, t[:70], c) for a, t, c in sorted(v, reverse=True)[:3]],
                            top3_format=sum(("Top 3" in t or "Tactical" in t) for _, t, _ in v))
        print(name, "|", q, "|", out[name][q]["over100k"], out[name][q]["over1m"], f'{out[name][q]["top10"]:,}', flush=True)
json.dump(out, open("research/saturation/saturation.json", "w"), indent=1)
