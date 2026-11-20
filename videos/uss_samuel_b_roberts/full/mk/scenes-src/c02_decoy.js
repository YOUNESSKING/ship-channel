// BASEMAP: wpac
// W. Pacific pushed in on the Philippines; blue arrow U.S. 3RD FLEET runs NORTH off Luzon on 'north'; Samar pin TAFFY 3.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const SM = P("TAFFY");
S.camera([[0, 1362, 748, 3.3], [END, 1366, 742, 3.5]]);
S.pin(SM, "TAFFY 3", { t: 0.3, color: BLU, anchor: "r", size: 44, gap: 36, ringR: 26 });
const A = G(16.3, 126.8), Bn = G(21.2, 126.8);
S.dot(A, { t: wt("battleships", 0.72), r: 12, color: BLU });
S.tag("U.S. 3RD FLEET", A, { t: wt("battleships", 0.72) + 0.1, anchor: "r", size: 42, gap: 36, boxColor: BLUBOX });
S.route([A, G(18.8, 126.8), Bn], { t: wt("north", 4.2) - 0.25, dur: END - wt("north", 4.2) + 0.1, width: 13, color: BLU, head: "ship", headSize: 2.4, ease: "none" });
S.finish();
