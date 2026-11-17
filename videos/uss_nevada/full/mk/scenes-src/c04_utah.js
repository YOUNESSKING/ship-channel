// BASEMAP: normandy
// 6 JUNE 1944 on 'sixth'; UTAH BEACH pin on 'Utah'; Nevada icon offshore.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const UT = P("UTAH"), OFF = S.G(49.47, -1.02);
S.camera([[0, UT[0] + 40, UT[1] - 30, 1.7], [END, UT[0] + 20, UT[1] - 30, 2.1]]);
S.date("6 JUNE 1944", wt("sixth", 0.6));
S.label("NORMANDY", S.G(49.2, -1.45), { t: wt("Normandy", 4.6), anchor: "c", size: 48, color: "#8fb0cc" });
S.pin(UT, "UTAH BEACH", { t: wt("Utah", 3.0), color: "#D9572B", anchor: "l", size: 48, gap: 40, dy: 30, ringR: 30 });
S.ship("bb", OFF, { t: wt("off", 2.6), len: 80, rot: 100, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
S.label("NEVADA", OFF, { t: wt("off", 2.6), anchor: "r", size: 44, gap: 60 });
S.finish();
