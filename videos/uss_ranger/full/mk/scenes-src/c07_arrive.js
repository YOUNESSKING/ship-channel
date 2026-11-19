// BASEMAP: brownsville
// Ranger comes in from the Gulf through the jetties at Brazos Santiago; SOUTH PADRE ISLAND on 'Padre'; 12 JULY 2015.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BZ = P("BRAZOS"), SP = P("SOUTHPADRE"), st = G(26.09, -96.95);
S.camera([[0, 1650, 760, 1.6], [END, 1560, 748, 2.2]]);
S.date("12 JULY 2015", 0.3);
const J1 = G(26.074, -97.152), J2 = G(26.074, -97.108), J3 = G(26.062, -97.152), J4 = G(26.062, -97.108);
S.route([J1, J2], { t: 0.1, dur: 0.3, width: 6, color: WH }); S.route([J3, J4], { t: 0.1, dur: 0.3, width: 6, color: WH });
S.label("JETTIES", J2, { t: wt("jetties", 1.02), anchor: "t", size: 34, gap: 40, color: WH });
const cv = S.cv(st, { t: 0.2, len: 120, rot: 180 });
S.sail(cv, [st, G(26.068, -97.12), BZ], { t: 0.3, dur: END - 0.6, ease: "power1.inOut" });
for (let i = 0; i < 14; i++) S.dot(S.off(J2, -i * 150 + 100, i % 2 ? 260 : -260), { t: wt("Crowds", 0.12) + i * 0.04, r: 4, color: WH, rings: false });
S.pin(SP, "SOUTH PADRE ISLAND", { t: wt("Padre", 1.92), color: ST, anchor: "t", size: 38, gap: 50, dx: -40, dy: -60, rings: false, r: 7 });
S.finish();
