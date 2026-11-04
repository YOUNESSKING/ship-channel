// BASEMAP: americas
// "A ship nobody would take, dragged around a continent, to wait some more." Pull back: the whole route as one line.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const SF = S.P("SF"), BEAU = S.P("BEAU");
const R = S.path(window.HORN);
S.clouds(6, 0.12);
S.camera([[0, BEAU[0] + 80, BEAU[1] + 150, 1.15], [END, 1480, 1080, 0.70]]);
S.route(R, { t: 0.0, dur: 0.01, dash: [16, 10] });
S.route(R, { t: w("dragged") - 0.1, dur: 1.8, width: 9, color: "rgba(255,226,150,.85)" });
S.pin(SF, "SAN FRANCISCO", { t: 0.0, anchor: "l", rings: false });
S.pin(BEAU, "BEAUMONT", { t: 0.0, anchor: "r" });
S.tag("RESERVE FLEET", BEAU, { t: w("wait"), anchor: "b", gap: 40, size: 42 });
S.finish();
