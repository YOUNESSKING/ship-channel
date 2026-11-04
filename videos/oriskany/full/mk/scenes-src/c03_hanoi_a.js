// BASEMAP: vietnam
// "A surface to air missile tore the wing off his A four Skyhawk." Over Hanoi (FACTCHECK_A C12b): a red missile track rises and meets the blue jet track.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const HN = S.P("HANOI"), HIT = G(21.06, 105.9);
S.clouds(6, 0.14);
S.camera([[0, HN[0] + 160, HN[1] + 60, 1.35], [END, HN[0] + 40, HN[1] + 10, 1.75]]);
S.pin(HN, "HANOI", { t: 0.12, anchor: "t", gap: 30, rings: false, r: 9 });
S.route(S.path([[20.4, 107.0], [20.75, 106.5], [21.0, 106.1], [21.06, 105.9]]), { t: 0.0, dur: w("tore"), color: S.BLUE, width: 5, head: "jet", headUntil: w("tore") + 0.1, ease: "none" });
S.route(S.path([[20.85, 105.78], [20.98, 105.84], [21.06, 105.9]]), { t: w("missile") - 0.3, dur: w("tore") - w("missile") + 0.3, color: S.RED, width: 5, head: "missile", headUntil: w("tore") + 0.1, ease: "power1.in" });
S.flashAt(HIT, w("tore"), { r: 46, keep: true });
S.label("SAM", G(20.85, 105.78), { t: w("missile"), anchor: "b", gap: 26, size: 42, color: "#ff9a92" });
S.finish();
