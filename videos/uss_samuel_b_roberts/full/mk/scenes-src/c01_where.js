// BASEMAP: trench
// Deep sea east of Samar; slow push onto a pulsing '?' at the APPROX. wreck area.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const W = P("WRECK");
S.camera([[0, 1140, 700, 1.0], [END, W[0] + 25, W[1] - 10, 2.1]]);
S.sring(W, { t: 0.5, r: 56, color: RED });
S.icon("q", W, { t: 0.4, size: 110, color: WH });
S.label("WRECK AREA · APPROX.", W, { t: 1.2, anchor: "b", size: 42, gap: 100, color: WH });
S.finish();
