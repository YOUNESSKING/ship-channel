// BASEMAP: usse
// "The EPA reviewed the Navy's studies." Pin ATLANTA · EPA REGION 4 (FACTCHECK_B B22: EPA Region 4 approval).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const ATL = S.P("ATL"), REEF = S.P("REEF");
S.clouds(5, 0.12);
S.camera([[0, ATL[0] - 120, ATL[1] + 140, 1.2], [END, ATL[0] - 90, ATL[1] + 120, 1.45]]);
S.pin(REEF, null, { t: 0.0, rings: false, r: 9 });
S.pin(ATL, "ATLANTA", { t: 0.05, anchor: "r" });
S.tag("EPA REGION 4", ATL, { t: w("EPA"), anchor: "t", gap: 40, size: 44 });
S.finish();
