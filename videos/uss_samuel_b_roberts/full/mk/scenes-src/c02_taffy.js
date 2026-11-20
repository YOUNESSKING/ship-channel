// BASEMAP: samar
// 13 blue ship dots east of Samar, TAFFY 3 on 'Taffy'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const T = P("TAFFY");
S.camera([[0, T[0] - 20, T[1] - 10, 1.7], [END, T[0] + 10, T[1] - 10, 2.0]]);
const ring6 = [0, 1, 2, 3, 4, 5].map((i) => [T[0] + Math.cos(i * 1.0472 + 0.3) * 17, T[1] + Math.sin(i * 1.0472 + 0.3) * 17]);
const ring7 = [0, 1, 2, 3, 4, 5, 6].map((i) => [T[0] + Math.cos(i * 0.8976 + 0.9) * 34, T[1] + Math.sin(i * 0.8976 + 0.9) * 34]);
ring6.concat(ring7).forEach((p, i) => S.dot(p, { t: 0.2 + i * 0.07, r: 11, color: BLU }));
S.label("TAFFY 3", [T[0] + 34, T[1] - 18], { t: wt("Taffy", 1.76), anchor: "r", size: 62, gap: 40, box: true, boxColor: BLUBOX });
S.finish();
