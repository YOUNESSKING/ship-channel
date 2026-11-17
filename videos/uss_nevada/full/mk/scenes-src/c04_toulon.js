// BASEMAP: medit
// TOULON pin on 'Toulon', AUGUST 1944 on 'August'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const TL = P("TOULON");
S.camera([[0, TL[0] - 120, TL[1] - 40, 1.5], [END, TL[0] - 60, TL[1] - 30, 2.0]]);
S.date("AUGUST 1944", wt("August", 0.6));
S.label("MEDITERRANEAN", S.G(42.5, 5.2), { t: wt("Mediterranean", 1.8), anchor: "c", size: 44, color: "#8fb0cc" });
S.pin(TL, "TOULON", { t: Math.min(wt("Toulon", 1.9), END - 1.4), color: "#D9572B", anchor: "r", size: 56, gap: 40, dy: -30, ringR: 34 });
S.finish();
