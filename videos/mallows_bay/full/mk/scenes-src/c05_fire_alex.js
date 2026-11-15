// BASEMAP: dcwide
// 'In October 1922, a fire broke out on two...' date; fire flash at Alexandria on 'fire'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const AL = S.P("ALEX");
S.camera([[0, AL[0], AL[1], 1.5], [END, AL[0], AL[1], 1.8]]);
S.date("OCT 1922", wt("October", 0.3));
S.pin(AL, "ALEXANDRIA", { t: 0.0, anchor: "l", rings: false });
S.flashAt(AL, wt("fire", 2.0), { r: 40, keep: true, sfx: false });
S.tag("FIRE", AL, { t: wt("fire", 2.0) + 0.1, anchor: "t", gap: 56, boxColor: "rgba(150,40,30,.92)" });
S.finish();
