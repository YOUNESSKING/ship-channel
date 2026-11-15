// BASEMAP: baycl
// 'And in September 2019, the bay and the river around it became...' date; sanctuary area (approximate) draws in.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const MB = S.P("MALLOWS");
S.camera([[0, MB[0], MB[1] + 100, 1.2], [END, MB[0] - 20, MB[1] + 160, 0.95]]);
S.date("SEPT 2019", wt("September", 0.4));
S.pin(MB, null, { t: 0.0, color: "#D9572B", rings: false });
S.poly([[[-77.3135, 38.4849], [-77.262, 38.486], [-77.250, 38.455], [-77.262, 38.420], [-77.300, 38.397], [-77.335, 38.400], [-77.333, 38.440], [-77.3135, 38.4849]]], { t: wt("river", 1.8), color: "#7fd3d8", fill: 0.22 });
S.finish();
