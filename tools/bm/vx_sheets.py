"""vx agent: snapshots + ONE contact sheet per scene -> build/sheet-<scene>.jpg (tools/make_sheet.py).  usage: python3 tools/vx_sheets.py SCENE [...]"""
import glob, json, os, shutil, subprocess, sys, tempfile
ABS = {"m2e": 523.44, "m2f": 546.53, "m2g": 638.03}
D = {
 "m2e": [(0.0, "vicksburg map, option 1 (early May): the army in the bridgehead, red all round; clean frame, legend/date continue", "-"),
         (3.2, "GRANT badge on 'Grant's place'; across the river (arrow)", "-"), (5.5, "deep in enemy country: red rings close round", "-"),
         (8.0, "BANKS badge on his name; Banks' column on the Red River", "-"), (11.6, "PORT HUDSON (south, off the map); NOT BEFORE THE TENTH OF MAY", "pop"),
         (13.9, "ONLY FIFTEEN THOUSAND MEN", "-"), (15.6, "E.decide (B3): legend + badges step out; A pulses on 'wait for Banks'", "hit, pops"),
         (17.5, "B pulses on 'cut loose'; ghost arrows inland keep drawing", "tick"), (19.6, "TELL US IN THE COMMENTS ticks", "ticks"), (22.9, "'And then...': card stays (reveal in m2f)", "tick")],
 "m2f": [(0.0, "frame 0 = the m2e card (continuity)", "-"), (3.4, "B lights on 'cut loose', A greys", "hit"), (5.2, "supply line to Grand Gulf flickers; CUT LOOSE", "hit"),
         (7.0, "SHERMAN WARNED card (spoken words, his photo in the card); one road, wagons", "-"), (10.5, "GRANT badge; NOT WITH FULL RATIONS; wagons fade", "-"),
         (17.0, "GRANT ANSWERED: hard bread, coffee, salt + the verbatim quote", "pops, hit"), (22.8, "two days of food; beef + corn icons; the march inland", "pops"),
         (29.5, "wedge between PEMBERTON (Vicksburg) and JOHNSTON (Jackson)", "-"), (34.4, "one at a time: the two red arrows cannot join (grey)", "-"),
         (36.0, "PORT GIBSON · 1 MAY stamp; date scroll 1 MAY", "hit"), (38.2, "RAYMOND · 12 MAY; territory 12 May", "hit"), (40.0, "JACKSON · 14 MAY", "hit"),
         (43.5, "turned back west; CHAMPION HILL · 16 MAY", "hit"), (47.2, "PEMBERTON badge; the fight (musketry, 2 visible shots)", "mg, booms"),
         (53.0, "ABOUT 15,000 FULLY ENGAGED vs ABOUT 25,000", "hits"), (57.5, "one Union division: more than a third", "-"), (60.5, "a Confederate division CUT OFF", "hit"),
         (63.0, "never made it back (grey arrow)", "-"), (66.0, "BIG BLACK RIVER · THE NEXT DAY; date 17 MAY", "hit, mg, boom"), (69.0, "18 GUNS · 1,700+ PRISONERS", "hits"),
         (78.0, "GRANT HIMSELF COUNTED: OVER 60,000 vs ABOUT 33,000", "hits"), (81.0, "IN EIGHTEEN DAYS: the five battle sites ring", "-"),
         (85.0, "THE FIVE BATTLES COST HIM FEWER THAN 4,500 MEN", "ticks"), (91.3, "18 MAY: ring closes, SHUT INSIDE VICKSBURG", "hit")],
 "m2g": [(0.0, "vicksburg_siege close-up, option 2: the works (red/blue bands), Union siege line, both flags (the siege line is the blue band)", "-"), (1.8, "19 MAY: assaults bounce off; the works fire", "booms, mg"),
         (3.0, "22 MAY: four assaults along the line", "booms"), (4.4, "FAILED stamp", "hit"), (6.4, "GRANT badge; HE REGRETTED THE SECOND ONE", "-"),
         (8.6, "JUNE 1863 + 35-star flag on the date scroll and on the map; saps start to creep", "-"),
         (10.2, "4 JULY: white flags along the works", "pops"), (11.8, "PEMBERTON badge: SURRENDERED", "hit"), (13.8, "~29,500 MEN ticks", "ticks"),
         (16.0, "AND 172 CANNON; 35-star flag over the city", "hit"), (18.6, "Lincoln: the one zoom-out begins (no cut)", "whoosh"),
         (21.0, "LINCOLN WROTE card; the river glows blue top to bottom", "-"), (23.5, "territory dissolves to July 1863: the Confederacy cut in two", "-"),
         (26.0, "the river Union top to bottom; flags on both halves", "-"), (28.5, "GRANT'S METHOD: line 2 on 'Grant cut it / fed his men off the land'", "pop, boom"),
         (31.0, "ring on Vicksburg on 'the gates of Vicksburg'", "-"), (36.5, "fewer men: ring on Vicksburg; map clean for the archive cut", "-")],
}
for sc in sys.argv[1:]:
    fr = D[sc]; times = ",".join(str(t) for t, _, _ in fr)
    r = subprocess.run(["timeout", "900", "hyperframes", "snapshot", ".", "--at", times], cwd=f"scenes/{sc}", capture_output=True, text=True)
    d = sorted(glob.glob(f"scenes/{sc}/.hyperframes/artifacts/snapshots/*/"), key=os.path.getmtime)[-1]
    os.makedirs(f"scenes/{sc}/snapshots", exist_ok=True)
    for f in glob.glob(f"scenes/{sc}/snapshots/frame-*.png"): os.remove(f)
    for f in glob.glob(d + "frame-*-at-*s.png"): shutil.copy(f, f"scenes/{sc}/snapshots/")
    rows = [[sc, t, "%d:%04.1f" % divmod(ABS[sc] + t, 60), w, s] for t, w, s in fr]
    spec = {"title": f"Grant #16 · {sc}", "note": "map look v11 + clean screen; Union blue / Confederates red; snapshots at the listed scene times", "frames": rows}
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(spec, f); f.close()
    os.makedirs("build", exist_ok=True); subprocess.run([sys.executable, "tools/make_sheet.py", f.name, f"build/sheet-{sc}.jpg"], check=True)
