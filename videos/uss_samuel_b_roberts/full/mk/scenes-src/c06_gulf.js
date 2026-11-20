// BASEMAP: persian
// Pin USS SAMUEL B. ROBERTS (FFG-58) · MINE · APPROX. in the central Persian Gulf; date card on 'eighty'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const T = P("TAFFY"), W = P("WRECK");
const taffy = (t, r) => { for (let i = 0; i < 6; i++) S.dot([T[0] + Math.cos(i * 1.047 + 0.3) * 17, T[1] + Math.sin(i * 1.047 + 0.3) * 17], { t, r, color: BLU });
  for (let i = 0; i < 7; i++) S.dot([T[0] + Math.cos(i * 0.8976 + 0.9) * 34, T[1] + Math.sin(i * 0.8976 + 0.9) * 34], { t, r, color: BLU }); };
document.getElementById("relief").style.filter = "brightness(1.7) contrast(1.05)";
const M = P("FFG58");
S.camera([[0, M[0] + 40, M[1] - 20, 1.2], [END, M[0] + 20, M[1] - 25, 1.55]]);
S.date("14 APRIL 1988", wt("eighty", 0.62));
S.label("PERSIAN GULF", G(28.4, 49.6), { t: wt("Persian", 3.36) - 0.1, anchor: "c", size: 56, color: ST });
S.pin(M, "USS SAMUEL B. ROBERTS (FFG-58)<br>MINE · APPROX.", { t: 0.4, color: RED, anchor: "r", size: 44, gap: 44, box: true, ringR: 30 });
S.finish();
