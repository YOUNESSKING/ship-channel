// BASEMAP: pearl_row
// 'The Nevada lay alone, at the end of the line, just astern of the USS Arizona.' Row ships stay; NEVADA alone (orange outline), ARIZONA labelled.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1350, 835, 2.0], [END, 1370, 820, 2.1]]);
const L = S.sl(183, 0, 1.0), rot = 135, ST = { fill: "#8fb0cc", stroke: "#0c1218", sw: 2.2 };
for (const [k, kind] of [["CA", "bb"], ["MD", "bb"], ["OK", "bb"], ["TN", "bb"], ["WV", "bb"], ["AZ", "bb"], ["AZ_O", "tr"]]) S.ship(kind, P(k), { t: 0, len: kind === "tr" ? L * 0.8 : L, rot, ...ST });
const nv = S.ship("bb", P("NV"), { t: wt("Nevada", 0.3), len: L, rot, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
S.ring(P("NV"), { t: wt("Nevada", 0.3), r: 62, color: "#D9572B" });
S.label("USS NEVADA", P("NV"), { t: wt("Nevada", 0.3), anchor: "r", size: 46, gap: 90, dy: -70 });
S.tag("ALONE", P("NV"), { t: wt("alone", 1.4), anchor: "r", size: 48, gap: 90, dy: 5, boxColor: "rgba(150,40,30,.92)" });
S.label("USS ARIZONA", P("AZ_O"), { t: wt("Arizona", 4.6), anchor: "r", size: 44, gap: 80, dy: 30 });
S.finish();
