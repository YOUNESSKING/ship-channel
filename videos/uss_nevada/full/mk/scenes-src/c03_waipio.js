// BASEMAP: pearl
// Tugs push Nevada across the channel from Hospital Point to Waipio Point; 10:45 on 'quarter'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1470, 840, 1.2], [END, 1440, 850, 1.24]]);
const HOSP = S.G(21.3410, -157.9645), WAIP = S.G(21.3432, -157.9720), A = [1436, 875], Bq = [1372, 840];
S.dot(HOSP, { t: 0, r: 9, color: "#f3eee2" }); S.label("HOSPITAL POINT", HOSP, { t: 0, anchor: "r", size: 40, gap: 40, dy: 100, color: "#8fb0cc" });
const nv = S.ship("bb", A, { t: 0, len: 66, rot: 150, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
const t1 = S.ship("tug", S.off(A, 150, -60), { t: wt("tugs", 0.8), len: 34, rot: 60, fill: "#c9d1d6", stroke: "#0c1218", sw: 2.2 });
const t2 = S.ship("tug", S.off(A, 150, 120), { t: wt("tugs", 0.8) + 0.2, len: 34, rot: 40, fill: "#c9d1d6", stroke: "#0c1218", sw: 2.2 });
S.label("TUGS", S.off(A, 150, -60), { t: wt("tugs", 0.8), anchor: "t", size: 40, gap: 40 });
const go = wt("pushed", 2.0), dur = END - go - 0.6;
S.sail(nv, [A, Bq], { t: go, dur, ease: "power2.inOut", keepRot: true });
S.sail(t1, [S.off(A, 150, -60), S.off(Bq, 150, -60)], { t: go, dur, ease: "power2.inOut", keepRot: true });
S.sail(t2, [S.off(A, 150, 120), S.off(Bq, 150, 120)], { t: go, dur, ease: "power2.inOut", keepRot: true });
S.pin(WAIP, "WAIPIO POINT", { t: wt("across", 3.0), anchor: "l", size: 44, gap: 40, dy: -30, color: "#D9572B" });
S.tag("10:45", WAIP, { t: wt("quarter", 4.2), anchor: "l", size: 48, gap: 70, dy: 60, boxColor: "rgba(150,40,30,.92)" });
S.finish();
