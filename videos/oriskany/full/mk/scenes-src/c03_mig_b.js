// BASEMAP: korea
// "met seven MiG fifteens. One pilot, Royce Williams, was" Seven red tracks come down from the north and meet the four blue ('4 vs 7'). No result on the map.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const CV = G(40.6, 132.2), N = window.MIG;
S.clouds(6, 0.14);
S.camera([[0, CV[0] - 30, CV[1] - 130, 1.8], [END, CV[0] - 20, CV[1] - 170, 2.0]]);
S.img("assets/media/carrier_top.png", CV, { t: 0.0, w: 120, rot: -70, filter: "brightness(1.7) drop-shadow(0 0 10px rgba(127,180,255,.9))" });
N.blue.forEach((p, i) => { S.route(S.path(p).slice(0, 3), { t: 0.0, dur: 0.01, color: S.BLUE, width: 4, scaleAt: 0 }); S.route(S.path(p).slice(2), { t: 0.0, dur: END, color: S.BLUE, width: 5, head: "jet", headSize: 1.4, ease: "none", scaleAt: 0 }); });
N.red.forEach((p, i) => S.route(S.path(p), { t: w("seven") - 0.3 + i * 0.12, dur: 2.6, color: S.RED, width: 5, head: "jet", headSize: 1.4, ease: "power1.out" }));
S.tag("4 VS 7", G(41.6, 130.6), { t: w("seven"), anchor: "l", gap: 10, size: 50 });
S.label("MiG-15s", G(43.6, 133.9), { t: w("MiG"), anchor: "r", gap: 10, size: 46, color: "#ff9a92" });
S.finish();
