// BASEMAP: pan_close
// test v4 endmap re-timed: "She will lie about thirteen nautical miles from the Oriskany." Both pins; dashed '13 NAUTICAL MILES' on 'thirteen'.
// Oriskany FWC 30°02.555'N 87°00.397'W; SS United States 30°07.148'N 86°46.755'W (FACTCHECK_C: 12.68 nmi).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF"), SSUS = S.P("SSUS"), PENS = S.P("PENS"), DES = S.P("DESTIN");
S.clouds(6, 0.14);
S.camera([[0, 1300, 835, 1.12], [END, 1430, 830, 1.0]]);
S.img("assets/media/carrier_top.png", [REEF[0], REEF[1] - 34], { t: 0.0, w: 150, filter: "brightness(1.9) drop-shadow(0 0 12px rgba(227,194,122,.9))" });
S.ring(REEF, { t: 0.0, r: 44 });
S.tag("USS ORISKANY", REEF, { t: 0.0, anchor: "b", gap: 40 });
S.img("assets/media/liner_top.png", [SSUS[0], SSUS[1] - 34], { t: 0.0, w: 170, filter: "drop-shadow(0 0 10px rgba(127,211,216,.8))" });
S.ring(SSUS, { t: 0.0, color: S.TEAL, r: 44 });
S.tag("SS UNITED STATES", SSUS, { t: 0.0, anchor: "t", gap: 80 });
S.route([REEF, [REEF[0] + 160, REEF[1] - 30], SSUS], { t: w("thirteen") - 0.15, dur: 1.0, dash: [18, 12], width: 5, color: S.INK });
S.label("13 NAUTICAL MILES", [(REEF[0] + SSUS[0]) / 2, (REEF[1] + SSUS[1]) / 2], { t: w("thirteen"), anchor: "b", gap: 34, dx: 90, size: 46 });
S.pin(PENS, "PENSACOLA", { t: 0.0, rings: false, r: 9, size: 42 });
S.pin(DES, "DESTIN", { t: 0.0, rings: false, r: 9, size: 42 });
S.finish();
