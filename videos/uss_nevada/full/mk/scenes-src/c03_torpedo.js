// BASEMAP: pearl_row
// A torpedo track runs in from the east to Nevada's port bow; hit flash on 'torpedo'; TORPEDO HIT · PORT BOW on 'port'.
const S = ShipK(), END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1370, 820, 2.1], [END, 1375, 815, 2.2]]);
const L = S.sl(183, 0, 1.0), rot = 135, ST = { fill: "#8fb0cc", stroke: "#0c1218", sw: 2.2 };
for (const [k, kind] of [["CA", "bb"], ["MD", "bb"], ["OK", "bb"], ["TN", "bb"], ["WV", "bb"], ["AZ", "bb"], ["AZ_O", "tr"]]) S.ship(kind, P(k), { t: 0, len: kind === "tr" ? L * 0.8 : L, rot, ...ST });
S.ship("bb", P("NV"), { t: 0, len: L, rot, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
const NV = P("NV"), bow = [NV[0] - 11, NV[1] + 31];   // port bow (SE side of the SW-pointing bow)
const tt = Math.max(0.2, wt("torpedo", 1.6) - 0.9);
S.route([[NV[0] + 300, NV[1] - 20], [NV[0] + 150, NV[1] + 8], bow], { t: tt, dur: 0.9, ease: "none", color: "#f3eee2", width: 5, head: "missile", headSize: 0.9 });
S.flashAt(bow, tt + 0.9, { r: 60, keep: true });
S.tag("TORPEDO HIT · PORT BOW", bow, { t: wt("port", 3.0), anchor: "r", size: 44, gap: 110, dy: 60, boxColor: "rgba(150,40,30,.92)" });
S.finish();
