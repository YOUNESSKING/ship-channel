// BASEMAP: korea
// "Then, in June nineteen fifty, war broke out in Korea," Korean peninsula + Sea of Japan; date JUNE 1950; 'KOREA' on 'Korea'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const P38 = S.path([[38.0, 124.6], [38.0, 128.6]]);
S.clouds(6, 0.14);
S.camera([[0, 1300, 820, 0.85], [END, G(38, 127.5)[0] + 80, G(38, 127.5)[1], 1.35]]);
S.date("JUNE 1950", w("June"));
S.route(P38, { t: w("war") - 0.1, dur: 0.8, color: S.RED, width: 6, dash: [14, 8] });
S.flashAt(G(38.0, 127.0), w("broke"), { r: 34 });
S.flashAt(G(38.0, 126.4), w("broke") + 0.25, { r: 26 });
S.flashAt(G(38.0, 127.8), w("broke") + 0.45, { r: 26 });
S.label("KOREA", G(36.6, 127.9), { t: w("Korea"), anchor: "c", size: 54 });
S.finish();
