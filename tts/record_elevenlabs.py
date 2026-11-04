import json, base64, urllib.request, urllib.error, re, os, subprocess
O = "/home/user/prehistory-channel/videos/video02/voice"
K1 = open(os.path.expanduser("~/.el_key3")).read().strip(); K2 = open(os.path.expanduser("~/.el_key2")).read().strip()
VOICE = "bIHbv24MWmeRgasZH58o"; MODEL = "eleven_v4"
txt = open("/home/user/prehistory-channel/research/video02-crocodile-rivers/SCRIPT_v1.md").read().split("## HOOK", 1)[1]
segs, cur, name = [], [], "HOOK"
for l in ("## HOOK" + txt).splitlines():
    if l.startswith("## "):
        if cur: segs.append((name, " ".join(cur)))
        name, cur = re.sub(r" \(.*\)$", "", l[3:].strip()), []
    elif l.strip() and not l.startswith("*") and not l.startswith("(on screen") and l.strip() != "---":
        cur.append(l.strip())
if cur: segs.append((name, " ".join(cur)))
def left(k):
    r = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": k})
    d = json.load(urllib.request.urlopen(r)); return d["character_limit"] - d["character_count"]
rem1 = left(K1) - 150; log = []; t_off = 0.0; words = []
for i, (n, t) in enumerate(segs):
    cost = len(t)
    key, acct = (K1, "key3") if cost <= rem1 else (K2, "key2")
    if acct == "key3": rem1 -= cost
    body = {"text": t, "model_id": MODEL,
            "previous_text": segs[i-1][1][-300:] if i else None, "next_text": segs[i+1][1][:300] if i + 1 < len(segs) else None}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
                                 data=json.dumps(body).encode(), headers={"xi-api-key": key, "Content-Type": "application/json"})
    try: r = json.load(urllib.request.urlopen(req, timeout=600))
    except urllib.error.HTTPError as e: print("FAIL", n, e.code, e.read()[:300]); raise SystemExit(1)
    f = f"{O}/{i:02d}.mp3"; open(f, "wb").write(base64.b64decode(r["audio_base64"]))
    dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
    al = r.get("normalized_alignment") or r["alignment"]; w, s0 = "", None
    for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if w: words.append({"w": w, "start": round(t_off + s0, 3), "end": round(t_off + last, 3), "seg": n}); w = ""
        else:
            if not w: s0 = a
            w += c; last = b
    if w: words.append({"w": w, "start": round(t_off + s0, 3), "end": round(t_off + last, 3), "seg": n})
    log.append({"seg": n, "file": f, "account": acct, "chars": len(t), "start": round(t_off, 3), "dur": round(dur, 3)}); t_off += dur
    print(f"{n[:30]:30s} {acct:12s} {len(t):5d} chars {dur:6.1f}s", flush=True)
json.dump(log, open(O + "/segments.json", "w"), indent=1); json.dump(words, open(O + "/words.json", "w"))
open(O + "/list.txt", "w").write("".join(f"file '{x['file']}'\n" for x in log))
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",O+"/list.txt","-c","copy",O+"/narration_full.mp3"], check=True)
print("TOTAL", round(t_off/60, 2), "min;", len(words), "words incl tags")
