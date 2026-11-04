// BASEMAP: usse
// "Florida, Mississippi, Texas, and Georgia with South Carolina." Each state lights up on its name.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const ST = window.GEO.states;
S.camera([[0, 1300, 920, 1.08], [END, 1320, 900, 1.16]]);
["Florida", "Mississippi", "Texas", "Georgia", "South Carolina"].forEach((n) => S.poly(ST[n], { t: 0.0, dur: 0.01, fill: 0.08, width: 3 }));
const L = { Florida: [28.3, -81.7], Mississippi: [32.7, -89.7], Texas: [31.3, -99.0], Georgia: [32.7, -83.4], "South Carolina": [33.9, -80.9] };
const T = { Florida: w("Florida"), Mississippi: w("Mississippi"), Texas: w("Texas"), Georgia: w("Georgia"), "South Carolina": w("South") };
for (const n in L) { S.poly(ST[n], { t: T[n], fill: 0.4, width: 4.5 }); S.label(n.toUpperCase(), G(...L[n]), { t: T[n], anchor: "c", size: 42 }); }
S.finish();
