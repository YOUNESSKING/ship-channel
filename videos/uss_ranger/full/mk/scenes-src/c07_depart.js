// BASEMAP: puget
// Ranger pulled from the Bremerton pier by 4 tugs; 5 MARCH 2015 on 'March'; 09:00 on 'nine'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BR = P("BREMERTON"), path = S.path([[47.557, -122.632], [47.566, -122.60], [47.58, -122.545], [47.62, -122.47], [47.75, -122.45], [47.9, -122.44]]);
S.camera([[0, 1410, 800, 2.2], [END, 1470, 720, 1.7]]);
S.date("5 MARCH 2015", wt("March", 1.05));
S.date("09:00", wt("nine", 3.41), { top: 150 });
S.pin(BR, "BREMERTON", { t: 0.2, color: ST, anchor: "l", size: 36, gap: 40, dy: 40, rings: false, r: 8 });
const t0 = 1.0, d = END - t0 - 0.3, cv = S.cv(BR, { t: 0.2, len: 100, rot: 0 }); S.sail(cv, path, { t: t0, dur: d, ease: "power2.inOut" });
[[-45, -18], [45, -20], [-45, 20], [45, 22]].forEach(([ox, oy], i) => { const tg = S.ship("tug", [BR[0] + ox * 0.5, BR[1] + oy * 0.5], { t: 0.3 + i * 0.1, len: 26, fill: WH, stroke: "#0c1218", fat: 1.6, sw: 1.6 });
  S.sail(tg, path.map((p) => [p[0] + ox * 0.5, p[1] + oy * 0.5]), { t: t0, dur: d, ease: "power2.inOut" }); });
S.finish();
