// BASEMAP: baycl
// 'Hulls would be floated in, the water pumped out, and the wood burned away on dry ground.' hull into the basin, flash on 'burned'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const BA = S.P("BASIN");
S.camera([[0, BA[0], BA[1], 3.0], [END, BA[0], BA[1], 3.4]]);
S.ring(BA, { t: 0.0, r: 46, color: "#D9572B" });
S.route([[BA[0] - 160, BA[1] - 60], [BA[0] - 60, BA[1] - 20], BA], { t: wt("floated", 0.4), dur: 1.4, head: "ship", headSize: 1.2, width: 3 });
S.tag("PUMP OUT", BA, { t: wt("pumped", 2.2), anchor: "b", gap: 70 });
S.flashAt(BA, wt("burned", 4.2), { r: 40, keep: true, sfx: false });
S.tag("BURN", BA, { t: wt("burned", 4.2) + 0.1, anchor: "t", gap: 70, boxColor: "rgba(150,40,30,.92)" });
S.finish();
