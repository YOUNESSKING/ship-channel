// BASEMAP: solomons
// GUADALCANAL label; pin POINT CRUZ on 'Point'; date card SEPTEMBER 1942 on 'September'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.55) contrast(1.06)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const PC = P("POINTCRUZ");
S.camera([[0, 1480, 800, 1.15], [END, PC[0] + 50, PC[1] - 30, 2.4]]);
S.date("SEPTEMBER 1942", wt("September", 0.28));
S.label("GUADALCANAL", G(-9.6, 160.1), { t: 0.3, anchor: "c", size: 64 });
S.pin(PC, "POINT CRUZ", { t: wt("Point", 4.14) - 0.1, color: RED, anchor: "l", size: 48, gap: 36, ringR: 30, dy: -20 });
S.finish();
