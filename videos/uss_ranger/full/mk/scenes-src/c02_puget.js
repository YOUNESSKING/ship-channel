// BASEMAP: puget
// PUGET SOUND on 'Puget'; BREMERTON pin on 'Bremerton'; SEATTLE label; naval shipyard tag.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BR = P("BREMERTON"), SE = P("SEATTLE");
S.camera([[0, 1490, 800, 1.0], [END, 1490, 790, 1.15]]);
S.pin(BR, "BREMERTON", { t: wt("Bremerton", 2.0), color: RED, anchor: "l", size: 48, gap: 34, ringR: 34 });
S.tag("PUGET SOUND NAVAL SHIPYARD", BR, { t: wt("Washington", 2.85), anchor: "b", size: 34, gap: 46, dx: -120 });
S.label("PUGET SOUND", G(47.74, -122.5), { t: wt("Puget", 3.75), anchor: "c", size: 60, color: ST });
S.pin(SE, "SEATTLE", { t: wt("Seattle", 4.7), color: WH, anchor: "r", size: 46, gap: 34, ringR: 30 });
S.finish();
