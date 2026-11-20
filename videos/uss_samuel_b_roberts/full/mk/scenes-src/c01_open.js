// BASEMAP: wpac
// Hook v2 (owner 2026-11-20: "hook is weak ... open on something engaging"): frame 0 is already a map MID-ZOOM, a fast dive to the
// sea east of Samar; a depth counter runs 0 -> 22,600 FT and lands on 'feet'; PHILIPPINE SEA on 'Philippine'; wreck ring + APPROX.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", REDBOX = "rgba(150,40,30,.94)";
const W = P("WRECK_W"), SM = P("SAMARC");
S.camera([[0, 1400, 790, 1.15], [END - 0.05, 1412, 792, 4.6]]);
S.sring(W, { t: 0.15, r: 40, color: RED });
S.counter(G(17.5, 129.5), (n) => n.toLocaleString("en-US") + " FT", 22600, 0.2, wt("feet", 1.85), { size: 120 });
S.label("DOWN", G(14.75, 129.5), { t: wt("feet", 1.85), anchor: "c", size: 64, color: WH });
S.label("PHILIPPINE SEA", G(13.2, 131.6), { t: wt("Philippine", 2.5), anchor: "c", size: 52, color: ST });
S.label("SAMAR", SM, { t: wt("Philippine", 2.5) + 0.3, anchor: "l", size: 42, gap: 30, dy: -30, dx: -10 });
S.label("WRECK SITE · APPROX.", W, { t: wt("Philippine", 2.5) + 0.5, anchor: "r", size: 40, gap: 54, dy: 20 });
S.finish();
