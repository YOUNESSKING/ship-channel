"""Map agent hook (Grant #16): snapshot specs + contact sheets for hook-a / hook-b.
usage (from grant/): python3 tools/gh_sheets.py hook-a|hook-b   (snapshots with hyperframes, copied to scenes/<scene>/snapshots/, then
tools/make_sheet.py -> build/sheet-<scene>.jpg)"""
import glob, json, os, shutil, subprocess, sys
scene = sys.argv[1]
A0 = {"hook-a": 0.0, "hook-b": 29.32}[scene]
F = {
 "hook-a": [
  (0, "frame 0: the theatre, Feb 1862, territory, both flags, boats + columns already moving", "-"),
  (2.5, "'two rivers': the Tennessee + Cumberland light up from the Ohio", "pop"),
  (4.0, "'open doors': blue arrows up both rivers, OPEN DOORS", "whoosh, hit"),
  (5.4, "'heart of the Confederacy': Nashville pulses", "pop"),
  (7.3, "'two forts': the forts slam onto the rivers", "hit + shake"),
  (8.0, "'held them shut': red bars across both rivers, HELD SHUT", "hit + shake"),
  (9.3, "ONE continuous zoom (no cut, no flash)", "zoom whoosh"),
  (10.8, "mid-zoom: the henry map, CUMBERLAND RIVER on its words", "-"),
  (12.0, "the donelson map fades in, the Union corridor colours in", "-"),
  (13.1, "lands on 'Fort Donelson': FORT DONELSON, the garrison", "hit + shake"),
  (14.8, "'within a week': blue columns march over from Fort Henry, legend", "whoosh"),
  (16.4, "12,000 card slams on 'twelve thousand', ticks", "hit + shake, ticks"),
  (17.6, "CONFEDERATE SOLDIERS lights on its words, the ring front", "pop"),
  (19.0, "SURRENDERED: the pocket turns blue, garrison greys, white flag", "hit + shake"),
  (20.6, "'to a general': the '?' badge", "-"),
  (22.5, "'almost nobody...heard of': badge pulse, the ring on the HQ", "pop"),
  (25.2, "FIRST MAJOR VICTORY / OF THE WAR", "hit + shake, boom"),
  (27.0, "'it began as...': camera pushes in on the Union right", "-"),
  (28.4, "A DISASTER, red pulse (hook-b starts on this camera)", "hit + shake"),
 ],
 "hook-b": [
  (0, "frame 0 = hook-a's last frame (16 Feb, the pocket blue)", "whoosh (rewind)"),
  (1.6, "rewind: white flag drops, the pocket red again, units step back", "-"),
  (3.4, "'the fifteenth of February': the date rolls back", "ticks"),
  (5.2, "'At dawn': dawn light, push in, colours dissolve into the fronts", "-"),
  (6.8, "'burst out': red columns break out, volleys where lines touch", "whoosh, musket"),
  (8.4, "'broken the Union right': BROKEN, the brigades fall back", "hit + shake, musket"),
  (10.0, "'the road out stood open': the Forge road glows, THE ROAD OUT", "pop, musket"),
  (11.6, "'The Union commander': the '?' badge, the HQ", "-"),
  (13.0, "'not even there': the empty HQ, NOT EVEN THERE", "hit + shake"),
  (14.6, "'away on a gunboat': the flagship, the '?' rides on it", "pop"),
  (16.5, "'the admiral'", "-"),
  (18.0, "'when he rode back': the '?' rides back, dotted trail", "whoosh"),
  (19.8, "'standing in knots, holding muskets': knots of blue men", "pop"),
  (21.8, "NO AMMUNITION", "hit + shake"),
  (23.4, "'tons of it, close at hand': crates glow, TONS OF IT", "pop, hit"),
  (25.7, "the map dims, the '?' comes to the centre", "whoosh"),
  (26.6, "'Ulysses S. Grant': photo + NAME SLAM", "hit + shake"),
  (29.0, "'a few weeks earlier his own superior...' (unnamed: no photo)", "pop"),
  (30.9, "'brushed off his plan': HIS PLAN + BRUSHED OFF", "hit + shake"),
  (32.1, "CUT 1 'He took two rivers': henry map, both forts blue, 1 TWO RIVERS", "whoosh + hit"),
  (33.6, "CUT 2 'the city that held...': Vicksburg at night, boats run the batteries", "whoosh + hit, gun"),
  (35.0, "'...the Mississippi': 2 THE MISSISSIPPI", "gun + impact"),
  (36.9, "CUT 3 'marched a whole army across a river': the pontoon bridge", "whoosh + hit"),
  (38.4, "3 ACROSS A RIVER", "pop"),
  (39.8, "'Robert E. Lee': pull back, Lee's badge + his army", "-"),
  (41.2, "'looking the other way': his army faces north, away", "hit"),
  (44.6, "title card on 'three greatest'", "riser + boom"),
 ]}[scene]
ts = ",".join(str(t) for t, _, _ in F)
r = subprocess.run(["hyperframes", "snapshot", ".", "--at", ts], cwd=f"scenes/{scene}", capture_output=True, text=True, timeout=900)
D = sorted(glob.glob(f"scenes/{scene}/.hyperframes/artifacts/snapshots/*/"), key=os.path.getmtime)[-1]
os.makedirs(f"scenes/{scene}/snapshots", exist_ok=True)
for p in glob.glob(f"scenes/{scene}/snapshots/frame-*.png"): os.remove(p)
for p in glob.glob(D + "frame-*.png"): shutil.copy(p, f"scenes/{scene}/snapshots/")
mm = lambda t: f"{int((A0 + t) // 60)}:{(A0 + t) % 60:04.1f}"
spec = {"title": f"Grant #16 {scene.upper()} ({'hook-1..hook-2' if scene == 'hook-a' else 'hook-3..hook-4'}) - map agent hook, round 3",
        "note": "STYLE_LOCK 1a + 1c + 2b: clean first frame, nothing before it is spoken, one big card at a time, ONE continuous zoom, visible fire only",
        "frames": [[scene, t, mm(t), w, s] for t, w, s in F]}
os.makedirs("build", exist_ok=True); json.dump(spec, open(f"build/gh_sheet_{scene}.json", "w"), indent=1)
print(subprocess.run(["python3", "tools/make_sheet.py", f"build/gh_sheet_{scene}.json", f"build/sheet-{scene}.jpg"], capture_output=True, text=True).stdout)
