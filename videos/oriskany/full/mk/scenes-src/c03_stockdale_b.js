// BASEMAP: vietnam
// "was hit by anti aircraft fire over North Vietnam." Closer: flak bursts on 'anti-aircraft'; the blue track ends in a flash.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const TGT = G(19.75, 105.65);
S.clouds(6, 0.14);
S.camera([[0, TGT[0] + 140, TGT[1] + 60, 1.5], [END, TGT[0] + 60, TGT[1] + 10, 1.9]]);
const r = S.route(S.path([[18.8, 107.0], [19.3, 106.4], [19.6, 105.95], [19.75, 105.65]]), { t: 0.0, dur: w("fire"), color: S.BLUE, width: 5, head: "jet", headUntil: w("fire") + 0.1, ease: "none" });
[[19.9, 105.8], [19.6, 105.6], [19.85, 105.5], [19.55, 105.85], [19.75, 105.75]].forEach((p, i) => S.flashAt(G(...p), w("anti") + i * 0.18, { r: 20, sfx: i ? false : "impact" }));
S.flashAt(TGT, w("fire") + 0.05, { r: 44, keep: true });
S.label("NORTH VIETNAM", G(20.6, 105.0), { t: w("North"), anchor: "c", size: 50 });
S.finish();
