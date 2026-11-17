// BASEMAP: pearl
// 12 FEB 1942: Nevada afloat again off Waipio Point; AFLOAT tag.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1400, 850, 1.5], [END, 1390, 850, 1.62]]);
const WAIP = S.G(21.3432, -157.9720), Bq = [1372, 840];
S.date("12 FEB 1942", wt("twelfth", 0.6));
S.pin(WAIP, "WAIPIO POINT", { t: 0.3, anchor: "l", size: 40, gap: 40, dy: -40, color: "#8fb0cc" });
const nv = S.ship("bb", Bq, { t: 0, len: 80, rot: 150, fill: "#8fb0cc", stroke: "#8fb0cc", sw: 3.4 });
S.ring(Bq, { t: wt("floated", 2.6), r: 50, color: "#D9572B" });

S.B.tl.to(nv.inner.querySelector("g"), { attr: { fill: "#f3eee2", stroke: "#D9572B" }, duration: 0.5 }, wt("floated", 2.6));
S.tag("AFLOAT", Bq, { t: wt("floated", 2.6), anchor: "r", size: 48, gap: 70, dy: 10, boxColor: "rgba(150,40,30,.92)" });
S.finish();
