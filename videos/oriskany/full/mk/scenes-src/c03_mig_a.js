// BASEMAP: korea
// "On the eighteenth of November, nineteen fifty two," Sea of Japan off north-east Korea; four blue jet tracks leave the carrier.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const CV = G(40.6, 132.2), N = window.MIG;
S.clouds(6, 0.14);
S.camera([[0, CV[0] - 120, CV[1] - 60, 1.4], [END, CV[0] - 30, CV[1] - 130, 1.8]]);
S.img("assets/media/carrier_top.png", CV, { t: 0.05, w: 120, rot: -70, filter: "brightness(1.7) drop-shadow(0 0 10px rgba(127,180,255,.9))" });
S.date("18 NOV 1952", w("eighteenth"));
S.label("SEA OF JAPAN", G(39.6, 133.8), { t: 0.2, anchor: "c", size: 42, color: "rgba(230,240,240,.85)" });
N.blue.forEach((p, i) => S.route(S.path(p), { t: 1.2 + i * 0.25, dur: END - 1.2 - i * 0.25 + 1.0, color: S.BLUE, width: 5, head: "jet", headSize: 1.4, ease: "none" }));
S.finish();
