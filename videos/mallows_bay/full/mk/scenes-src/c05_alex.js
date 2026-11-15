// BASEMAP: dcwide
// 'Some went to Alexandria, just across the river from Washington.' pin ALEXANDRIA; WASHINGTON on 'Washington'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const AL = S.P("ALEX"), WH = S.P("WH");
S.camera([[0, AL[0], AL[1], 1.4], [END, AL[0] + 10, AL[1] - 10, 1.9]]);
S.pin(AL, "ALEXANDRIA", { t: wt("Alexandria", 0.3), anchor: "l", color: "#D9572B" });
S.pin(WH, "WASHINGTON", { t: wt("Washington", 3.0), anchor: "r", rings: false });
S.finish();
