// BASEMAP: bikini
// 'SUMMER 1946' on 'summer'; the target fleet's dots appear across the lagoon on 'fleet'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const AIM = P("AIM");
S.camera([[0, 1470, 825, 1.6], [END, 1500, 832, 2.0]]);
S.date("SUMMER 1946", wt("summer", 0.9));
S.label("BIKINI LAGOON", S.G(11.64, 165.4), { t: wt("lagoon", 2.2), anchor: "c", size: 44, color: "#8fb0cc" });
const f = wt("fleet", 3.0);
S.scatter(AIM, 38, 4200, 7, AIM, 450).forEach((p, i) => S.dot(p, { t: f + i * 0.04, r: 8, color: "#f3eee2" }));
S.dot(AIM, { t: f + 1.2, r: 11, color: "#D9572B" });
S.label("THE TARGET FLEET", S.off(AIM, 0, 3600), { t: f, anchor: "c", size: 48 });
S.finish();
