// BASEMAP: oahu_sw
// End screen: wreck pin 'USS NEVADA · 15,400 FT' on the LEFT; right ~45 % of the frame stays clear; slow drift; no other text.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const WR = P("WRECK"), PH = P("PEARL"), h = S.mpx(18520) / 2, s = 1.3;
const cx = WR[0] + (960 - 330) / s, cy = WR[1] + (540 - 440) / s;
S.camera([[0, cx, cy, s], [END, cx + 40, cy - 16, 1.36]]);
S.poly([[[WR[0] - h, WR[1] - h], [WR[0] + h, WR[1] - h], [WR[0] + h, WR[1] + h], [WR[0] - h, WR[1] + h]]], { px: true, t: 0, color: "#8fb0cc", fill: 0.14, width: 4 });
S.route([WR, PH], { t: 0, dur: 0.01, dash: [16, 12], width: 4, color: "rgba(243,238,226,.55)" });
S.pin(WR, "USS NEVADA · 15,400 FT", { t: 0.6, color: "#D9572B", anchor: "r", size: 46, gap: 40, dy: 0, ringR: 38 });
S.finish();
