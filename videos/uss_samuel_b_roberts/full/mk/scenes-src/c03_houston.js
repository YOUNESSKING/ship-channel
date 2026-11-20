// BASEMAP: gulf_houston
// HOUSTON, TEXAS pin on 'Houston'; BROWN SHIPBUILDING tag on 'Texas'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.55) contrast(1.06)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const H = P("HOUSTON"), Y = P("BROWNYARD");
S.camera([[0, 1400, 800, 1.5], [END, 1385, 785, 1.9]]);
S.label("GALVESTON", P("GALV"), { t: 0.3, anchor: "r", size: 38, gap: 30, color: ST });
S.pin(H, "HOUSTON, TEXAS", { t: wt("Houston", 1.44), color: RED, anchor: "l", size: 48, gap: 34, ringR: 30, dy: -34 });
S.dot(Y, { t: wt("Texas", 2.1), r: 10, color: WH });
S.tag("BROWN SHIPBUILDING", Y, { t: wt("Texas", 2.1), anchor: "r", size: 44, gap: 40, dy: 40, boxColor: REDBOX });
S.finish();
