// BASEMAP: gulf_pan
// "...to two counties." Escambia (FL) and Baldwin (AL) outlines appear on 'two counties' (US Census boundaries).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF"), GEO = window.GEO.counties;
S.camera([[0, 1150, 560, 1.15], [END, 1120, 540, 1.3]]);
S.pin(REEF, null, { t: 0.0 });
S.poly(GEO["Escambia"], { t: w("two") - 0.05, fill: 0.16 });
S.poly(GEO["Baldwin"], { t: w("two") + 0.15, fill: 0.16 });
S.label("2 COUNTIES", G(30.95, -87.45), { t: w("counties"), anchor: "c", size: 52 });
S.finish();
