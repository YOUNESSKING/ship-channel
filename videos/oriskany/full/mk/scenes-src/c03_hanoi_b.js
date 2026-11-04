// BASEMAP: hanoi
// "He came down in a lake in the middle of the city." Zoom into central Hanoi; pin TRUC BACH LAKE on 'lake' (FACTCHECK_A C12b).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const TB = S.P("TRUCBACH");
S.clouds(5, 0.12);
S.camera([[0, TB[0] + 60, TB[1] + 60, 0.85], [END, TB[0] + 20, TB[1] + 20, 1.6]]);
S.label("HANOI", G(20.9, 105.85), { t: 0.12, anchor: "c", size: 54 });
S.route(S.path([[21.12, 105.97], [21.08, 105.9], [21.047, 105.838]]), { t: 0.1, dur: w("lake") - 0.1, color: S.BLUE, width: 4, dash: [10, 8], head: "dot" });
S.pin(TB, "TRUC BACH LAKE", { t: w("lake"), anchor: "l", r: 13 });
S.finish();
