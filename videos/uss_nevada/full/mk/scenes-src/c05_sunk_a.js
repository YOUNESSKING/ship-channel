// BASEMAP: bikini_close
// Able, close frame (shared by c05_miss/gilliam/sunk_a/b/c). Burst star west of the orange NEVADA dot.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const AIM = P("AIM"), BU = P("BURSTA"), CAMX = (AIM[0] + BU[0]) / 2, CAMY = AIM[1];
S.camera([[0, CAMX + 4, CAMY, 2.4], [END, CAMX + 6, CAMY, 2.45]]);
const SHIPS = { GILLIAM: [S.off(BU, 25, -35), "tr", "GILLIAM"], CARLISLE: [S.off(BU, 260, 110), "tr", "CARLISLE"], LAMSON: [S.off(BU, -300, -170), "dd", "LAMSON"], ANDERSON: [S.off(BU, -420, 150), "dd", "ANDERSON"], SAKAWA: [S.off(BU, 120, -340), "cru", "SAKAWA"] };
S.scatter(AIM, 14, 1500, 5, AIM, 250).forEach((p) => S.dot(p, { t: 0, r: 7, color: "#8fb0cc" }));
S.dot(AIM, { t: 0, r: 13, color: "#D9572B" }); S.ring(AIM, { t: 0, r: 42, color: "#D9572B" });
S.label("NEVADA", AIM, { t: 0, anchor: "r", size: 44, gap: 40, dy: 45 });
const SH = {};
const place = (k, t, gone) => { const [pt, kind] = SHIPS[k]; SH[k] = S.ship(kind, pt, { t, len: kind === "dd" ? 50 : 62, rot: 90, fill: "#b3cadf", stroke: "#0c1218", sw: 2.2 }); return SH[k]; };
const sink = (k, t, dy = 0, anchor = "l") => { const [pt, , nm] = SHIPS[k]; S.label(nm, pt, { t, anchor, size: 40, gap: 45, dy, until: t + 2.2 }); S.flashAt(pt, t + 0.1, { r: 44 }); S.fade(SH[k].wrap, t + 0.35, 0.5); };

S.burst(BU, 0, { r: 46 });
Object.keys(SHIPS).forEach((k) => place(k, 0));
S.tag("5 SHIPS SUNK", S.off(AIM, 0, 0), { t: wt("Five", 0.3), anchor: "c", size: 60, dx: -80, dy: -250, boxColor: "rgba(150,40,30,.92)" });
sink("GILLIAM", wt("Gilliam", 1.6), 70);
sink("CARLISLE", wt("Carlisle", 3.6), -20, "r");
S.finish();
