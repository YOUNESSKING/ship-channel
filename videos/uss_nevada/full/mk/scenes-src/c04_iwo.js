// BASEMAP: pacific
// IWO JIMA pin on 'Iwo', FEB 1945 on 'February'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const IW = P("IWO");
S.camera([[0, IW[0] + 80, IW[1] + 20, 2.6], [END, IW[0] + 30, IW[1], 3.4]]);
S.date("FEB 1945", wt("February", 1.8));
S.pin(IW, "IWO JIMA", { t: wt("Iwo", 2.2), color: "#D9572B", anchor: "r", size: 56, gap: 40, ringR: 36 });
S.finish();
