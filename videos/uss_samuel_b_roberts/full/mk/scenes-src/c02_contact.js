// BASEMAP: samar
// TAFFY 3 dots; line of red ships on the northern edge on 'masts'; time card on 'quarter'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const T = P("TAFFY");
S.camera([[0, T[0] + 10, T[1] - 80, 1.25], [END, T[0] + 10, T[1] - 95, 1.4]]);
const k = S.scaleAt(0);
[[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]].forEach(([a, i]) => S.dot([T[0] + Math.cos(i * 1.047) * 17, T[1] + Math.sin(i * 1.047) * 17], { t: 0.1, r: 10, color: BLU }));
[0, 1, 2, 3, 4, 5, 6].forEach((i) => S.dot([T[0] + Math.cos(i * 0.8976 + 0.9) * 34, T[1] + Math.sin(i * 0.8976 + 0.9) * 34], { t: 0.1, r: 10, color: BLU }));
S.label("TAFFY 3", [T[0] + 34, T[1] + 20], { t: 0.2, anchor: "r", size: 44, gap: 30, box: true, boxColor: BLUBOX });
S.date("≈06:45", wt("quarter", 0.56));
const tm = wt("masts", 2.82);
const row = [0, 1, 2, 3, 4].map((i) => [T[0] + 10 + i * 48, T[1] - 250 + i * 28]);
row.forEach((p, i) => S.ship(i === 0 ? "bb" : "cru", p, { t: tm - 0.15 + i * 0.12, len: 74 * k / 1.25, rot: 30, fill: JAP, stroke: "#f7f3ea", sw: 2.4 }));
S.label("JAPANESE FLEET · APPROX.", row[4], { t: tm + 0.4, anchor: "r", size: 40, gap: 60, box: true, boxColor: REDBOX });
S.finish();
