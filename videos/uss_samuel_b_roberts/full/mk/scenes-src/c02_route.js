// BASEMAP: leyte
// Red dashed route Sibuyan Sea -> San Bernardino Strait -> south along Samar's east coast -> Taffy 3. NIGHT, 24-25 OCT on 'night'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const T = P("TAFFY");
S.camera([[0, 1290, 735, 1.45], [END, 1330, 760, 1.6]]);
const pts = S.path([[12.7, 122.6], [12.62, 123.5], [12.55, 124.25], [12.72, 124.95], [12.5, 125.6], [12.12, 125.95], [11.82, 126.0]]);
S.route(pts, { t: 0.15, dur: END - 0.5, width: 7, color: JAP, dash: [20, 12], head: "dot", ease: "none" });
S.label("SIBUYAN SEA", pts[0], { t: 0.2, anchor: "b", size: 40, gap: 46, dx: -20, color: ST });
S.label("SAN BERNARDINO STRAIT", P("SANBERN"), { t: wt("Strait", 1.64), anchor: "t", size: 40, gap: 52, box: true, dx: -40 });
S.date("NIGHT, 24-25 OCT", wt("night", 2.72));
S.dot(T, { t: 3.0, r: 12, color: BLU });
S.label("TAFFY 3", T, { t: 3.0, anchor: "r", size: 40, gap: 30, dy: 30 });
S.finish();
