// BASEMAP: wpac
// Blue dashed line from the east edge (FROM HOUSTON, VIA PANAMA) across the Pacific to Samar; APRIL → OCTOBER 1944 on 'months'; OFF SAMAR pin on 'Samar'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc", BLU = "#4f8df0", JAP = "#e0403a", REDBOX = "rgba(150,40,30,.94)", BLUBOX = "rgba(24,60,120,.94)";
const SM = P("WRECK_W");
S.camera([[0, 1869, 790, 0.95], [END, 1965, 790, 1.05]]);
const pts = S.path([[11, -102.5], [13.5, -130], [15.5, -160], [16, -178], [14.5, 170], [12.8, 150], [12, 136], [11.7, 127.3]]);
S.route(pts, { t: 0.2, dur: wt("Samar", 3.14) - 0.2, width: 9, color: "#7db4ff", dash: [22, 14], head: "ship", headSize: 1.5, ease: "none" });
S.tag("← FROM HOUSTON, VIA PANAMA", pts[0], { t: 0.3, anchor: "l", size: 40, gap: 30, dy: 70, boxColor: BLUBOX });
S.date("APRIL → OCTOBER 1944", wt("months", 0.42));
S.pin(SM, "OFF SAMAR", { t: wt("Samar", 3.14), color: RED, anchor: "t", size: 48, gap: 50, ringR: 30 });
S.finish();
