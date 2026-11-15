// BASEMAP: baycl
// 'Their shad and herring nets were in the same water.' fish icons around the anchorage; tag.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const WW = S.P("WIDEWATER");
S.camera([[0, WW[0] + 120, WW[1] - 60, 1.0], [END, WW[0] + 100, WW[1] - 40, 1.2]]);
S.label("WIDEWATER", WW, { t: 0.0, anchor: "l", size: 42 });
[[-120, -60], [140, -110], [40, 90], [-60, 140], [210, 40], [90, -170]].forEach((d, i) => S.icon("fish", [WW[0] + 260 + d[0], WW[1] - 60 + d[1]], { t: wt("shad", 0.3) + i * 0.18, size: 56, bob: 5 }));
S.tag("FISHING GROUNDS", [WW[0] + 260, WW[1] - 60], { t: wt("herring", 1.2), anchor: "c", gap: 0 });
S.finish();
