// BASEMAP: westcoast
// "So in nineteen ninety nine, she was towed out of California." SF Bay; tow line starts south; date 1999 (FACTCHECK_A D8).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const SF = S.P("SF");
const R = S.path(window.HORN.slice(0, 5));
S.clouds(6, 0.14);
S.camera([[0, SF[0] + 40, SF[1] - 40, 1.35], [END, SF[0] + 120, SF[1] + 330, 1.15]]);
S.pin(SF, "SAN FRANCISCO", { t: 0.05, anchor: "l", rings: false });
S.date("1999", w("nineteen"));
S.route(R, { t: w("towed") - 0.1, dur: END - w("towed") + 0.6, dash: [16, 10], head: "ship", headSize: 1.2, ease: "power1.in" });
S.label("CALIFORNIA", G(36.4, -119.6), { t: w("California"), anchor: "c", size: 50 });
S.finish();
