// BASEMAP: samar
// Red Japanese icons swing round and head NORTH on 'turned'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const T = P("TAFFY"), W = P("WRECK");
const taffy = (t, r) => { for (let i = 0; i < 6; i++) S.dot([T[0] + Math.cos(i * 1.047 + 0.3) * 17, T[1] + Math.sin(i * 1.047 + 0.3) * 17], { t, r, color: BLU });
  for (let i = 0; i < 7; i++) S.dot([T[0] + Math.cos(i * 0.8976 + 0.9) * 34, T[1] + Math.sin(i * 0.8976 + 0.9) * 34], { t, r, color: BLU }); };
S.camera([[0, 1390, 650, 1.6], [END, 1390, 640, 1.65]]);
const k = S.scaleAt(0);
taffy(0.1, 9);
S.label("TAFFY 3", [T[0] + 34, T[1] + 25], { t: 0.2, anchor: "r", size: 40, gap: 26, color: ST });
const fl = [[1375, 600, "bb"], [1437, 632, "bb"], [1322, 647, "cru"], [1490, 672, "cru"]];
const tt = wt("turned", 1.14);
fl.forEach(([x, y, kind], i) => {
  const sh = S.ship(kind, [x, y], { t: 0.1, len: (kind === "bb" ? 52 : 44) * k, rot: 60, fill: JAP, stroke: "#f7f3ea", sw: 2.4, dur: 0.2 });
  S.turn(sh, 60, -90, tt + i * 0.06, 0.85);
  S.sail(sh, [[x, y], [x - 4, y - 105]], { t: tt + 0.7, dur: END - tt - 0.8, ease: "power1.in", keepRot: true });
});
S.tag("HEADING NORTH", [1420, 430], { t: tt + 0.5, anchor: "c", size: 46, boxColor: REDBOX });
S.tag("POSITIONS APPROX.", [1490, 855], { t: 0.3, anchor: "c", size: 38, color: ST });
S.finish();
