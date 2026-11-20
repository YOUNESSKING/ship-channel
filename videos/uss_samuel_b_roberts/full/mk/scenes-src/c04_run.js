// BASEMAP: samar
// Roberts (blue) leaves a grey smoke band and heads for 4 red cruisers; time card on 'seven'; tag POSITIONS APPROX.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const T = P("TAFFY"), W = P("WRECK");
const taffy = (t, r) => { for (let i = 0; i < 6; i++) S.dot([T[0] + Math.cos(i * 1.047 + 0.3) * 17, T[1] + Math.sin(i * 1.047 + 0.3) * 17], { t, r, color: BLU });
  for (let i = 0; i < 7; i++) S.dot([T[0] + Math.cos(i * 0.8976 + 0.9) * 34, T[1] + Math.sin(i * 0.8976 + 0.9) * 34], { t, r, color: BLU }); };
S.camera([[0, 1395, 740, 2.1], [END, 1385, 728, 2.25]]);
const k = S.scaleAt(0);
taffy(0.1, 9);
S.label("TAFFY 3", [T[0] - 4, T[1] + 40], { t: 0.2, anchor: "b", size: 40, gap: 24, color: ST });
const col = [[1335, 612], [1365, 634], [1395, 656], [1425, 678]];
col.forEach((p, i) => S.ship("cru", p, { t: 0.5 + i * 0.15, len: 52 * k, rot: 40, fill: JAP, stroke: "#f7f3ea", sw: 2.4 }));
S.label("4 CRUISERS · APPROX.", col[0], { t: 1.0, anchor: "r", size: 40, gap: 50, dy: -50, color: WH });
const pts = [[1450, 835], [1425, 802], [1405, 765], [1385, 732]];
const t0 = 0.3, dur = END - 0.7;
S.route(pts, { t: t0, dur, width: 64, color: "rgba(175,180,186,.62)", ease: "power1.inOut" });
const rb = S.ship("dd", pts[0], { t: t0 - 0.05, len: 62 * k, rot: -120, fill: BLU, stroke: "#ffffff", sw: 2.6, dur: 0.2 });
const at = S.sail(rb, pts, { t: t0, dur, ease: "power1.inOut" });
S.label("SAMUEL B. ROBERTS", S.fpt(at, t0, dur), { t: 0.5, anchor: "r", size: 42, gap: 60, dy: -14, box: true, boxColor: BLUBOX });
S.date("≈07:30", wt("seven", 1.1));
S.tag("POSITIONS APPROX.", [1500, 880], { t: 0.3, anchor: "c", size: 38, color: ST });
S.finish();
