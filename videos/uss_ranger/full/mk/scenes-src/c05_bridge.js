// BASEMAP: pnw
// camera along the Columbia from mouth to Fairview; red bar on 'bridge' with BRIDGE (APPROX.).
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const FV = P("FAIRVIEW"), MO = P("COLMOUTH"), riv = S.path(S.COL), BG = G(46.1, -122.98);
S.camera([[0, MO[0] + 70, MO[1] - 20, 2.2], [wt("bridge", 2.96) - 0.2, BG[0], BG[1] + 10, 2.4], [END, FV[0] - 40, FV[1] - 40, 2.2]]);
S.route(riv, { t: 0.0, dur: 0.01, width: 7, color: ST });
S.dot(MO, { t: 0.1, r: 9, color: WH });
S.label("MOUTH", MO, { t: 0.1, anchor: "b", size: 36, gap: 36, color: ST });
const t0 = 0.3, cv = S.cv(riv[0], { t: t0, len: 90, rot: -10 });
const pre = riv.slice(0, 6); S.sail(cv, pre, { t: t0, dur: wt("pass", 2.52) - t0 + 0.3, ease: "power1.inOut" });
S.pin(FV, "FAIRVIEW", { t: wt("Fairview", 0.48), color: RED, anchor: "r", size: 40, gap: 30, dy: 30, ringR: 30 });
const tb = wt("bridge", 2.96);
S.route([S.off(BG, 0, 6000), S.off(BG, 0, -6000)], { t: tb, dur: 0.3, width: 12, color: "#e0403a" });
S.tag("BRIDGE (APPROX.)", BG, { t: tb + 0.2, anchor: "t", size: 40, gap: 60, boxColor: "rgba(150,40,30,.92)" });
S.finish();
