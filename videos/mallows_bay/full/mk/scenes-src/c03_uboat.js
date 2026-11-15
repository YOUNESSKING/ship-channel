// BASEMAP: atlantic
// 'In February and March of 1917, German U-boats sank more than a million tons': date; red sinking marks round Britain.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const UK = S.P("BRITAIN");
S.clouds(6, 0.14);
S.camera([[0, UK[0] - 260, UK[1] + 120, 0.95], [END, UK[0] - 120, UK[1] + 60, 1.3]]);
S.date("FEB – MAR 1917", wt("February", 0.1));
S.label("BRITAIN", UK, { t: 0.2, anchor: "r", size: 44 });
[[50.2, -10.5], [48.8, -7.5], [51.8, -12.5], [49.5, -5.0], [47.0, -9.5], [53.5, -14.0], [46.0, -6.0], [50.8, -2.0], [55.0, -10.0], [48.0, -13.0]].forEach((p, i) => S.flashAt(G(p[0], p[1]), 0.5 + i * 0.25, { r: 18, keep: true, sfx: false }));
S.tag("1,000,000+ TONS SUNK", G(48.5, -16), { t: wt("German", 2.2) + 0.6, anchor: "l", boxColor: "rgba(150,40,30,.92)" });
S.finish();
