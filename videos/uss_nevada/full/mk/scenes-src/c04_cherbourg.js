// BASEMAP: normandy
// CHERBOURG pin on 'Cherbourg', 25 JUNE 1944 on 'twenty'; Nevada offshore shelling.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const CH = P("CHERB"), OFF = S.G(49.78, -1.5);
S.camera([[0, CH[0] + 30, CH[1] + 60, 1.7], [END, CH[0] + 10, CH[1] + 40, 2.2]]);
S.date("25 JUNE 1944", wt("twenty", 0.9));
S.ship("bb", OFF, { t: 0.2, len: 80, rot: 120, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
S.label("NEVADA", OFF, { t: 0.2, anchor: "r", size: 44, gap: 60 });
S.pin(CH, "CHERBOURG", { t: wt("Cherbourg", 2.4), color: "#D9572B", anchor: "l", size: 52, gap: 40, dy: 40, ringR: 30 });
[0, 1, 2].forEach((i) => S.flashAt(S.off(CH, -10 + i * 14, 8 - i * 9), wt("shelled", 1.8) + 0.3 * i, { r: 34 }));
S.finish();
