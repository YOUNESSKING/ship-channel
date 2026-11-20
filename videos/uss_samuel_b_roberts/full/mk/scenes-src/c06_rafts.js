// BASEMAP: samar
// 3 tiny raft dots drift from the APPROX. sinking marker; counter ≈50 HOURS on 'fifty'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
document.getElementById("relief").style.filter = "brightness(1.25)";
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const T = P("TAFFY"), W = P("WRECK");
const taffy = (t, r) => { for (let i = 0; i < 6; i++) S.dot([T[0] + Math.cos(i * 1.047 + 0.3) * 17, T[1] + Math.sin(i * 1.047 + 0.3) * 17], { t, r, color: BLU });
  for (let i = 0; i < 7; i++) S.dot([T[0] + Math.cos(i * 0.8976 + 0.9) * 34, T[1] + Math.sin(i * 0.8976 + 0.9) * 34], { t, r, color: BLU }); };
S.camera([[0, 1395, 770, 2.3], [END, 1380, 775, 2.4]]);
S.xmark(W, 0.1, { r: 22 });
S.label("SINKING SITE · APPROX.", W, { t: 0.3, anchor: "r", size: 40, gap: 46, dy: 46 });
[[-80, 28], [-62, 52], [-96, 6]].forEach(([dx, dy], i) => {
  const d = S.dot([W[0] + i * 6 - 6, W[1] + 10 + i * 4], { t: 0.3 + i * 0.1, r: 9, color: WH });
  d.style.zIndex = 5; tl_move(d, dx, dy);
});
function tl_move(el, dx, dy) { B.tl.fromTo(el, { x: 0, y: 0 }, { x: dx, y: dy, duration: END - 0.4, ease: "none", immediateRender: false }, 0.4); }
S.counter([W[0] + 0, W[1] - 70], (n) => `≈${n} HOURS`, 50, 0.25, wt("fifty", 1.22), { size: 112, anchor: "c" });
S.finish();
