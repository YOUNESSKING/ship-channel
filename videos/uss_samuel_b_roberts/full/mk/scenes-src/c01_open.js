// BASEMAP: wpac
// First frame = clean W. Pacific; push to the sea east of Samar. PHILIPPINE SEA on 'Philippine', wreck ring on 'warship' (not in this shot: ~3.1 s), tag on 'feet'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const W = P("WRECK_W"), SM = P("SAMARC");
S.camera([[0, 1440, 810, 0.667], [0.35, 1440, 810, 0.69], [END - 0.1, 1412, 792, 4.0]]);
S.label("SAMAR, PHILIPPINES", SM, { t: 0.9, anchor: "l", size: 40, gap: 30, dy: -34, dx: -10 });
S.tag("NEARLY 23,000 FT DOWN", W, { t: wt("feet", 1.85), anchor: "t", size: 54, gap: 150, dy: -20, boxColor: REDBOX });
S.label("PHILIPPINE SEA", G(14.6, 131.0), { t: wt("Philippine", 2.5), anchor: "c", size: 52, color: ST });
S.sring(W, { t: wt("Philippine", 2.5) + 0.6, r: 34, color: RED });
S.label("WRECK SITE · APPROX.", W, { t: wt("Philippine", 2.5) + 0.7, anchor: "r", size: 40, gap: 54, dy: 20 });
S.finish();
