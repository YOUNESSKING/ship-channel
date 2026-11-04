// BASEMAP: gulf_pan
// "Escambia, in Florida, and Baldwin, in Alabama." Each county lights on its name.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF"), GEO = window.GEO.counties;
S.camera([[0, 1120, 540, 1.3], [END, 1100, 520, 1.42]]);
S.pin(REEF, null, { t: 0.0 });
S.poly(GEO["Escambia"], { t: 0.0, fill: 0.12, dur: 0.01 });
S.poly(GEO["Baldwin"], { t: 0.0, fill: 0.12, dur: 0.01 });
S.poly(GEO["Escambia"], { t: w("Escambia"), fill: 0.32, width: 5 });
S.label("ESCAMBIA, FL", G(30.62, -87.12), { t: w("Escambia"), anchor: "r", gap: 10, size: 44 });
S.poly(GEO["Baldwin"], { t: w("Baldwin"), fill: 0.32, width: 5 });
S.label("BALDWIN, AL", G(30.95, -87.98), { t: w("Baldwin"), anchor: "l", gap: 10, size: 44 });
S.finish();
