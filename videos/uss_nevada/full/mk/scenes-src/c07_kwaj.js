// BASEMAP: marshalls
// Tow line BIKINI -> KWAJALEIN; 29 AUG 1946 on 'twenty'; DECOMMISSIONED near the end.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const KW = P("KWAJ"), BK = P("BIKINI"), MID = [(KW[0] + BK[0]) / 2, (KW[1] + BK[1]) / 2];
S.camera([[0, MID[0], MID[1], 1.3], [END, MID[0], MID[1], 1.38]]);
S.date("29 AUG 1946", wt("twenty", 0.8));
S.pin(BK, "BIKINI", { t: 0.1, color: "#D9572B", anchor: "r", size: 44, gap: 40, ringR: 34 });
const a = wt("August", 1.8), d = Math.max(1.2, END - a - 1.0);
S.route([BK, KW], { t: a, dur: d, dash: [16, 12], width: 5, color: "#D9572B", ease: "power1.inOut" });
const nv = S.ship("bb", BK, { t: a - 0.2, len: 60, rot: 0, fill: "#f3eee2", stroke: "#D9572B", sw: 3.2 }); S.sail(nv, [BK, KW], { t: a, dur: d, ease: "power1.inOut" });
S.pin(KW, "KWAJALEIN", { t: a + d - 0.3, color: "#f3eee2", anchor: "r", size: 48, gap: 40, ringR: 34 });
S.tag("DECOMMISSIONED", S.off(KW, 0, 0), { t: wt("six", END - 1.2), anchor: "t", size: 48, gap: 100, boxColor: "rgba(150,40,30,.92)" });
S.finish();
