// BASEMAP: vietnam
// "On the ninth of September, nineteen sixty five," One blue track leaves the Gulf of Tonkin heading inland (FACTCHECK_A C1a).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const YK = S.P("YANKEE"), TGT = G(19.6, 105.9);
S.clouds(6, 0.14);
S.camera([[0, YK[0] - 200, YK[1] - 80, 1.2], [END, (YK[0] + TGT[0]) / 2, (YK[1] + TGT[1]) / 2, 1.4]]);
S.img("assets/media/carrier_top.png", YK, { t: 0.05, w: 110, rot: -30, filter: "brightness(1.7) drop-shadow(0 0 10px rgba(127,180,255,.9))" });
S.date("9 SEPT 1965", w("ninth"));
S.route(S.path([[17.5, 108.5], [18.4, 107.4], [19.3, 106.6], [19.6, 105.9]]), { t: 1.0, dur: END - 0.6, color: S.BLUE, width: 5, head: "jet", ease: "none" });
S.finish();
