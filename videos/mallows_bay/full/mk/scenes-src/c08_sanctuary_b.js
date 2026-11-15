// BASEMAP: baycl
// 'the Mallows Bay-Potomac River National Marine Sanctuary.' tag 'MARINE SANCTUARY' on 'Sanctuary'; 'APPROXIMATE' note.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const MB = S.P("MALLOWS");
S.camera([[0, MB[0] - 20, MB[1] + 160, 0.95], [END, MB[0] - 20, MB[1] + 170, 1.0]]);
S.pin(MB, null, { t: 0.0, color: "#D9572B", rings: false });
S.poly([[[-77.3135, 38.4849], [-77.262, 38.486], [-77.250, 38.455], [-77.262, 38.420], [-77.300, 38.397], [-77.335, 38.400], [-77.333, 38.440], [-77.3135, 38.4849]]], { t: 0.0, color: "#7fd3d8", fill: 0.22, dur: 0.01 });
S.tag("NATIONAL MARINE SANCTUARY", G(38.44, -77.29), { t: wt("Sanctuary", 2.6), anchor: "c", size: 46, boxColor: "rgba(20,70,90,.92)" });
S.label("BOUNDARY APPROXIMATE", G(38.44, -77.29), { t: wt("Sanctuary", 2.6), anchor: "c", dy: 62, size: 30 });
S.finish();
