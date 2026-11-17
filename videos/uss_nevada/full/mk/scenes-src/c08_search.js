// BASEMAP: oahu_sw
// 10 x 10 nmi search box draws on 'searched'; robot track lines sweep it.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const WR = P("WRECK"), h = S.mpx(18520) / 2;
S.camera([[0, 1250, 900, 1.5], [END, 1200, 930, 1.9]]);
S.poly([[[WR[0] - h, WR[1] - h], [WR[0] + h, WR[1] - h], [WR[0] + h, WR[1] + h], [WR[0] - h, WR[1] + h]]], { px: true, t: wt("searched", 0.3), color: "#8fb0cc", fill: 0.16, width: 4 });
S.tag("SEARCH AREA · 10 × 10 NM", [WR[0], WR[1] - h], { t: wt("area", 1.0), anchor: "t", size: 40, gap: 40, boxColor: "rgba(30,64,92,.92)" });
const t0 = wt("underwater", 1.8);
for (let i = 0; i < 6; i++) { const y = WR[1] - h + (i + 0.5) * (2 * h / 6), L = i % 2 ? [[WR[0] + h - 4, y], [WR[0] - h + 4, y]] : [[WR[0] - h + 4, y], [WR[0] + h - 4, y]];
  S.route(L, { t: t0 + i * 0.28, dur: 0.3, ease: "none", color: "#f3eee2", width: 4 }); }
S.label("UNDERWATER ROBOT", [WR[0] + h, WR[1] + h], { t: wt("robot", 2.6), anchor: "r", size: 40, gap: 50, dy: 30 });
S.finish();
