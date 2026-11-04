// BASEMAP: gulf_pan
// "Okaloosa County plans to sink the SS United States." Okaloosa outline + Destin pin; liner icon at the planned site
// (30°07.148'N 86°46.755'W, FACTCHECK_C) on 'SS United States'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const SSUS = S.P("SSUS"), DES = S.P("DESTIN"), REEF = S.P("REEF");
S.clouds(4, 0.12);
S.camera([[0, 1560, 560, 1.25], [w("SS"), 1520, 650, 1.45], [END, 1500, 680, 1.55]]);
S.pin(REEF, null, { t: 0.0, rings: false, r: 8, color: "rgba(227,194,122,.7)" });
S.poly(window.GEO.counties["Okaloosa"], { t: w("Okaloosa"), fill: 0.3 });
S.label("OKALOOSA COUNTY", G(30.78, -86.58), { t: w("Okaloosa") + 0.15, anchor: "c", size: 46 });
S.pin(DES, "DESTIN", { t: w("County"), rings: false, anchor: "r" });
S.img("assets/media/liner_top.png", SSUS, { t: w("SS"), w: 190, filter: "drop-shadow(0 0 10px rgba(127,211,216,.8))" });
S.ring(SSUS, { t: w("SS"), color: S.TEAL, r: 44 });
S.tag("SS UNITED STATES", SSUS, { t: w("United"), anchor: "b", gap: 52 });
S.finish();
