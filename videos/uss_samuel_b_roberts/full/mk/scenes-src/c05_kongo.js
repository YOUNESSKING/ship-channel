// BASEMAP: samar
// Red KONGO north of the blue Roberts icon; time card on 'nine'; red flash on the blue icon on 'finished'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const T = P("TAFFY"), W = P("WRECK");
const taffy = (t, r) => { for (let i = 0; i < 6; i++) S.dot([T[0] + Math.cos(i * 1.047 + 0.3) * 17, T[1] + Math.sin(i * 1.047 + 0.3) * 17], { t, r, color: BLU });
  for (let i = 0; i < 7; i++) S.dot([T[0] + Math.cos(i * 0.8976 + 0.9) * 34, T[1] + Math.sin(i * 0.8976 + 0.9) * 34], { t, r, color: BLU }); };
S.camera([[0, 1400, 745, 2.4], [END, 1400, 742, 2.5]]);
const k = S.scaleAt(0), R = W, K = [1383, 685];
S.ship("bb", K, { t: 0.05, dur: 0.1, len: 70 * k, rot: 60, fill: JAP, stroke: "#f7f3ea", sw: 2.6 });
S.label("KONGO", K, { t: 0.3, anchor: "r", size: 46, gap: 50, box: true, boxColor: REDBOX });
S.ship("dd", R, { t: 0.05, dur: 0.1, len: 66 * k, rot: -110, fill: BLU, stroke: "#ffffff", sw: 2.6 });
S.label("SAMUEL B. ROBERTS", R, { t: 0.3, anchor: "r", size: 42, gap: 50, box: true, boxColor: BLUBOX });
S.date("≈09:00", wt("nine", 0.48));
S.route([[K[0] + 12, K[1] + 26], [R[0] - 8, R[1] - 30]], { t: wt("shells", 1.8), dur: 0.55, width: 5, color: JAP, dash: [14, 9], head: "missile", ease: "power1.in" });
S.burst(R, wt("finished", 2.34), { r: 62, color: RED });
S.tag("POSITIONS APPROX.", [1500, 835], { t: 0.3, anchor: "c", size: 38, color: ST });
S.finish();
