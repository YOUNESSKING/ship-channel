// BASEMAP: samar
// SAMAR on 'Samar'; PHILIPPINES pops on 'island'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
S.camera([[0, 1215, 750, 1.1], [END, 1240, 745, 1.3]]);
S.label("SAMAR", G(12.0, 125.1), { t: wt("Samar", 2.88), anchor: "c", size: 72, gap: 0 });
S.label("PHILIPPINES", G(12.75, 126.6), { t: wt("island", 3.7) - 0.1, anchor: "c", size: 60, color: ST, from: { y: 0, scale: 0.6 }, ease: "back.out(2)" });
S.finish();
