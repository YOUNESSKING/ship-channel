"""Move-1 agent: contact-sheet specs for m1a-m1f -> build/sheet-<scene>.jpg (tools/make_sheet.py).  usage: python3 tools/m1_sheets.py SCENE [...]"""
import json, os, subprocess, sys, tempfile
ABS = {"m1a": 105.63, "m1b": 128.7, "m1c": 157.33, "m1d": 205.7, "m1e": 257.2, "m1f": 319.75}
D = {
 "m1a": [(0.0, "henry map, option 1 (6 FEB); gunboats already steaming up the Tennessee; clean frame", "-"), (4.5, "title MOVE 1 · FORT HENRY on 'Fort Henry' (legend steps out); date scroll on the spoken date", "boom"),
         (7.0, "push-in: ironclads abreast vs Fort Henry, ship guns -> arc -> impact", "ship-gun fire + booms"), (14.0, "TILGHMAN badge on his name; fort in floodwater", "booms"),
         (19.0, "garrison already marched off toward Donelson; SURRENDERED; ABOUT 90 MEN; ground turns pale then blue (E2)", "hit"), (22.5, "GRANT badge; his columns still on the road; caption", "-")],
 "m1b": [(0.0, "donelson map wide, option 1 (12 FEB layer); Henry blue, Donelson red; reinforcements moving in", "-"), (2.0, "target on Fort Donelson; caption on 'reinforce'", "pop"),
         (5.5, "date 12 FEBRUARY on 'the twelfth'; 15,000 counter", "ticks"), (8.0, "two columns march across country (about a dozen miles)", "-"),
         (10.5, "camera arrives; the outer works glow", "-"), (12.5, "FLOYD / PILLOW / BUCKNER chips + counters on each name", "pops"),
         (15.0, "Grant knew Pillow (Pillow pulses)", "-"), (20.0, "right up to within gunshot: arrows to the works; the ring layer fades in", "-"),
         (26.0, "15,000 ON THE 8TH card (HUD steps out)", "-"), (28.3, "> 50,000 A MONTH LATER", "hit")],
 "m1c": [(0.0, "close-up option 2 (front lines only), 14 FEB", "-"), (3.0, "Foote's ironclads come up; FOOTE badge on his name", "-"), (6.0, "batteries vs ironclads (visible)", "fire + booms"),
         (9.0, "~60 HITS ON THE FLAGSHIP; two ironclads drift back", "ticks, booms"), (12.5, "FOOTE badge: WOUNDED stamp", "hit"), (19.5, "night: rain and snow", "-"),
         (23.5, "blankets thrown away on the march", "-"), (26.5, "15 FEB DAWN, new angle from the Union right", "-"), (30.0, "breakout hits the Union right; front bulges out", "musketry"),
         (33.0, "THREE DAYS OF RATIONS card (HUD steps out)", "hit"), (36.5, "not a last stand: they planned to leave", "-"), (40.0, "the road out glows", "-"),
         (43.5, "Grant badge 'did not know that yet'; right wing BREAKING", "hit"), (47.5, "MUSKETS BUT NO CARTRIDGES", "-")],
 "m1d": [(0.0, "Grant rides back along the line (rider counter); right wing greyed", "-"), (3.0, "HE DID NOT PANIC", "-"), (6.5, "WHOEVER ATTACKS FIRST NOW WILL WIN (paraphrase, no quote marks)", "hit"),
         (13.5, "cartridge boxes filled, back into line", "pop"), (17.0, "IT ACTED LIKE A CHARM", "-"), (25.0, "official report card: as great as his own, possibly greater", "-"),
         (29.0, "they pull back inside the ring; front returns", "-"), (33.5, "the first counterattack: on the left", "-"), (37.5, "C. F. SMITH badge on his name", "-"),
         (41.0, "Smith's division through the felled trees (abatis)", "musketry"), (44.5, "TOOK THE OUTER WORKS; front pushed in", "hit"), (48.0, "night: council at Dover", "pop"), (51.3, "GIVE UP stamp", "hit + shake")],
 "m1e": [(0.0, "15 FEB night, option 2 front, Buckner's pocket", "-"), (3.5, "FLOYD / PILLOW chips; steamers at the Dover landing", "pop"), (7.5, "they leave upriver on the steamers", "-"),
         (11.5, "Floyd: Buchanan's secretary of war", "-"), (15.0, "FORREST cavalry out", "-"), (19.0, "through the flooded backwater (Lick Creek)", "-"), (23.0, "BUCKNER badge; 16 FEB DAWN; letter to Grant", "-"),
         (27.0, "GRANT badge; answer travels back", "-"), (31.0, "verbatim reply, hit + shake on 'immediate'", "hit"), (35.0, "second sentence", "-"), (39.0, "UNGENEROUS AND UNCHIVALROUS", "-"),
         (43.5, "accepted: US flag over the fort; colours return (2.2 s) on the zoom-out; telegram card", "hit"), (48.0, "12,000-15,000 prisoners, 48 field guns, 17 heavy guns", "ticks"),
         (52.5, "map breather", "-"), (57.0, "U.S. -> UNCONDITIONAL SURRENDER GRANT", "hit + shake"), (62.3, "casualty card (old clean card)", "hit")],
 "m1f": [(0.0, "tennessee map, both forts Union (16 FEB layer)", "-"), (3.0, "two river forts, ten days", "pops"), (6.5, "Grant badge; caption", "-"),
         (10.0, "the two rivers glow; gunboats far into Tennessee", "-"), (13.0, "Kentucky line: lost ground pale first (E2)", "-"), (16.0, "turns blue; Confederates fall back; Nashville", "-"),
         (23.0, "method card from the spoken sentence: lines light on their words", "pops"), (26.5, "line 3 on 'attacked the moment the enemy hesitated'", "boom"), (29.5, "dark-to-bluff transition on the question", "-"),
         (32.0, "A FORTRESS ON A HIGH BLUFF", "-"), (34.5, "the supply river", "-"), (37.5, "right under its guns", "fire"), (40.5, "E.subscribe click", "ticks"), (44.5, "NEXT: MOVE 2", "pop")],
}
for sc in sys.argv[1:]:
    fr = [[sc, t, "%d:%04.1f" % divmod(ABS[sc] + t, 60), w, s] for t, w, s in D[sc]]
    spec = {"title": f"Grant #16 · {sc}", "note": "map look v11 + clean screen; Union blue / Confederates red; snapshots at the listed scene times", "frames": fr}
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(spec, f); f.close()
    os.makedirs("build", exist_ok=True); subprocess.run([sys.executable, "tools/make_sheet.py", f.name, f"build/sheet-{sc}.jpg"], check=True)
