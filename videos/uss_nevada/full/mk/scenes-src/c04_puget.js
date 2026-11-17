// BASEMAP: pacific
// Line from Pearl Harbor to Puget Sound (Bremerton) on 'Puget'; APRIL 1942 on 'April'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const PH = P("PEARL"), PU = P("PUGET"), MID = [(PH[0] + PU[0]) / 2, (PH[1] + PU[1]) / 2];
S.camera([[0, MID[0] - 30, MID[1] + 10, 1.9], [END, MID[0] + 30, MID[1] - 10, 2.1]]);
S.date("APRIL 1942", wt("April", 0.6));
S.pin(PH, "PEARL HARBOR", { t: 0.3, color: "#f3eee2", anchor: "r", size: 40, gap: 30, dy: 10, ringR: 30 });
S.route(S.arcPts(PH, PU, -0.1), { t: wt("Puget", 1.6) - 0.5, dur: 2.6, width: 6, color: "#D9572B", head: "ship" });
S.pin(PU, "PUGET SOUND", { t: wt("Puget", 1.6) + 1.8, color: "#D9572B", anchor: "l", size: 48, gap: 30, dy: -10, ringR: 32 });
S.finish();
