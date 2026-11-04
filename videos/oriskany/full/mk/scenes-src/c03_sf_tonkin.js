// BASEMAP: pacific
// "She was repaired in San Francisco and was back off Vietnam the next summer." SF pin ('REPAIRED') -> line to the Gulf of Tonkin; 1967.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const SF = S.P("SF"), YK = S.P("YANKEE");
const ARC = S.arcPts(SF, YK, 0.1, 40);
S.clouds(7, 0.14);
S.camera([[0, SF[0] - 160, SF[1] - 40, 1.35], [w("back"), (SF[0] + YK[0]) / 2, SF[1] + 60, 0.70], [END, (SF[0] + YK[0]) / 2 - 120, (SF[1] + YK[1]) / 2 - 40, 0.8]]);
S.pin(SF, null, { t: 0.05, rings: false });
S.tag("REPAIRED", SF, { t: w("repaired"), anchor: "b", gap: 46, size: 42 });
S.label("SAN FRANCISCO", SF, { t: w("San"), anchor: "l" });
S.route(ARC, { t: w("back") - 0.2, dur: w("Vietnam") - w("back") + 0.9, dash: [18, 12], width: 6, head: "ship", headSize: 1.3, scaleAt: w("back") });
S.label("VIETNAM", G(16, 106.3), { t: w("Vietnam"), anchor: "l", size: 48 });
S.date("1967", w("next"));
S.finish();
