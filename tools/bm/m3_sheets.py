"""Move-3 agent: snapshots + contact sheets for m3a-m3d + ending -> build/sheet-<scene>.jpg.  usage: python3 tools/m3_sheets.py SCENE [...] (from grant/)"""
import json, os, shutil, subprocess, sys, tempfile
ABS = {"m3a": 719.54, "m3b": 775.18, "m3c": 828.58, "m3d": 854.51, "ending": 906.28}
D = {
 "m3a": [(0, "richmond map, option 1 (12 JUN); Cold Harbor lines, units moving; clean first frame", "-"), (2.5, "JUNE 1864 on the spoken date; trenches draw", "-"),
         (5.5, "GRANT badge; the probe", "-"), (8, "LEE badge; the line's guns fire (visible); COULD NOT BREAK THROUGH", "fire, boom, hit"),
         (11, "the James glows; title MOVE 3 · THE JAMES RIVER (HUD steps out)", "boom"), (13, "PETERSBURG + ring", "pop"), (15.5, "the railroads meet at Petersburg", "-"),
         (19.5, "IF GRANT COULD TAKE IT, RICHMOND WOULD STARVE", "-"), (22.5, "THE PLAN WAS TO DISAPPEAR (blue counters flicker)", "-"), (29.5, "Lee looks in the wrong place", "-"),
         (33.5, "SHERIDAN badge; cavalry rides west (wide)", "-"), (37, "Lee's cavalry after it", "-"), (39.5, "after dark, 12 JUNE 1864", "-"),
         (42.5, "WARREN, Fifth Corps crosses the Chickahominy", "pop"), (46.5, "faces toward Richmond", "-"), (49, "the rest slips out, south by back roads", "-"), (52.5, "MEADE badge", "-"), (55.3, "end", "-")],
 "m3b": [(0, "jamesriver wide, option 1 (14 JUN); columns arriving; dawn", "-"), (3, "14 JUNE 1864", "-"), (5.5, "ferries at WILCOX'S LANDING; colours dissolve (2.8 s)", "pop"),
         (8, "WEYANOKE", "pop"), (11, "engineers; PONTOON BOATS 0 -> 101", "ticks"), (13.5, "ABOUT 2,100 FEET", "pop"), (17, "UP TO NINETY FEET OF WATER", "-"),
         (20.5, "clock 4 PM", "-"), (23.5, "11 PM, night; READY", "hit"), (27.5, "the army crosses", "-"), (31, "ABOUT 115,000 MEN · BY GRANT'S OWN COUNT", "hit"),
         (35, "zoom out, colours back (2.2 s); LEE badge", "-"), (38.5, "guessed Petersburg / would not believe it", "-"), (41, "kept his army around Richmond", "-"),
         (44.5, "16 JUNE: still asking", "-"), (48, "17 JUNE", "-"), (51, "the wire to Beauregard (verbatim)", "ticks"), (53, "end", "-")],
 "m3c": [(0, "petersburg close-up, option 2: Dimmock Line, Smith's corps on the City Point road", "-"), (2.5, "PETERSBURG", "pop"), (5, "15 JUNE 1864; ABOUT 14,000", "pop"),
         (8, "W. F. SMITH badge", "-"), (10.5, "HINKS badge, his division in the lead", "-"), (13.5, "ABOUT 2,200", "pop"), (17, "BEAUREGARD badge; batteries fire (visible)", "fire, boom"),
         (19, "the breach; the front moves", "musketry"), (20.5, "ABOUT TWO MILES WIDE", "pop"), (22.5, "Smith STOPPED, night", "hit"), (24.5, "waited for the morning: ghost arrows", "-"), (25.8, "end", "-")],
 "m3d": [(0, "petersburg option 1 (18 JUN) + front, 16 June", "-"), (3, "HANCOCK", "-"), (6, "Lee's veterans arriving (wide)", "-"), (8.5, "18 JUNE; assaults bounce, guns visible", "fire, boom"),
         (11, "THE UNION LOST ABOUT 11,400 MEN", "hit"), (13.5, "trenches; THE CHANCE WAS GONE", "hit"), (17, "GRANT badge (years later)", "-"),
         (20.5, "PETERSBURG COULD HAVE BEEN EASILY CAPTURED (no quote marks: indirect speech)", "-"), (24, "zoom-out starts", "whoosh"), (26.5, "the move over the James", "-"),
         (28.5, "one continuous zoom onto the richmond map", "-"), (31, "siege lines grow; MORE THAN NINE MONTHS", "hit"), (34, "-", "-"), (37.5, "RICHMOND / PETERSBURG abandoned", "pop"),
         (42, "method: OUT OF A STALEMATE, OVER A RIVER", "-"), (46, "-", "-"), (49, "WHERE LEE COULD NOT FOLLOW", "boom"), (51.7, "end", "-")],
 "ending": [(0, "tennessee map (16 FEB 1862 layer); voice reads the tag junk here (bug)", "-"), (3, "-", "-"), (6.8, "DONELSON, FEBRUARY 1862", "pop"),
            (9, "HE STRUCK WHILE THE ENEMY WAS STILL DECIDING", "-"), (11.2, "mississippi map, VICKSBURG, 1863", "pop"), (13.5, "WHERE THE ENEMY SAID NO ARMY COULD GO", "-"),
            (16, "LIVED OFF THE LAND", "-"), (18.2, "richmond map, THE JAMES, JUNE 1864", "pop"), (21, "A HUNDRED THOUSAND MEN AWAY FROM A STALEMATE", "-"),
            (24, "NO TIME TO CATCH HIS BREATH", "-"), (27, "U. S. GRANT · 1862", "hit"), (30, "initials light up", "pop"), (33, "1865", "-"), (36.4, "GRANT'S METHOD (3 lines)", "boom")],
}
for sc in sys.argv[1:]:
    ts = ",".join(str(t) for t, _, _ in D[sc])
    sd = f"scenes/{sc}/snapshots"; shutil.rmtree(sd, ignore_errors=True)
    subprocess.run(["hyperframes", "snapshot", f"scenes/{sc}", "-o", sd, "--no-end", "--at", ts], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=900)
    fr = [[sc, t, "%d:%04.1f" % divmod(ABS[sc] + t, 60), w, s] for t, w, s in D[sc]]
    spec = {"title": f"Grant #16 · {sc}", "note": "map look v11 + clean screen; Union blue / Confederates red; 35-star US flag (34-star on the 1862 map)", "frames": fr}
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(spec, f); f.close()
    os.makedirs("build", exist_ok=True); subprocess.run([sys.executable, "tools/make_sheet.py", f.name, f"build/sheet-{sc}.jpg"], check=True)
