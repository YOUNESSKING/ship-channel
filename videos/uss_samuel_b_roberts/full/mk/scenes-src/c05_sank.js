// BASEMAP: samar
// Blue Roberts icon fades out; marker SANK 10:05 · APPROX. on 'Stern'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const T = P("TAFFY"), W = P("WRECK");
const taffy = (t, r) => { for (let i = 0; i < 6; i++) S.dot([T[0] + Math.cos(i * 1.047 + 0.3) * 17, T[1] + Math.sin(i * 1.047 + 0.3) * 17], { t, r, color: BLU });
  for (let i = 0; i < 7; i++) S.dot([T[0] + Math.cos(i * 0.8976 + 0.9) * 34, T[1] + Math.sin(i * 0.8976 + 0.9) * 34], { t, r, color: BLU }); };
S.camera([[0, 1400, 745, 2.5], [END, 1400, 748, 2.4]]);
const k = S.scaleAt(0), R = W, K = [1383, 685];
S.ship("bb", K, { t: 0, len: 70 * k, rot: 60, fill: JAP, stroke: "#f7f3ea", sw: 2.6, dur: 0.01 });
const rb = S.ship("dd", R, { t: 0, len: 66 * k, rot: -110, fill: BLU, stroke: "#ffffff", sw: 2.6, dur: 0.01 });
S.fade(rb.wrap, 0.35, 0.9);
S.xmark(R, 0.9, { r: 26 });
S.tag("SANK 10:05 · APPROX.", R, { t: wt("Stern", 0.12), anchor: "r", size: 46, gap: 56, boxColor: REDBOX });
S.finish();
