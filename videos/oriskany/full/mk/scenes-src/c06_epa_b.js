// BASEMAP: usse
// "On the fifteenth of February, two thousand six, it ruled." Date 15 FEB 2006; gold line Atlanta -> the wreck site on 'ruled'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const ATL = S.P("ATL"), REEF = S.P("REEF");
S.clouds(5, 0.12);
S.camera([[0, ATL[0] - 90, ATL[1] + 120, 1.45], [END, (ATL[0] + REEF[0]) / 2, (ATL[1] + REEF[1]) / 2, 1.25]]);
S.pin(ATL, "ATLANTA", { t: 0.0, anchor: "r", rings: false });
S.tag("EPA REGION 4", ATL, { t: 0.0, anchor: "t", gap: 40, size: 44 });
S.date("15 FEB 2006", w("fifteenth"));
S.route(S.arcPts(ATL, REEF, 0.15), { t: w("ruled") - 0.3, dur: 1.0, width: 7, head: "dot" });
S.pin(REEF, "USS ORISKANY", { t: w("ruled") + 0.6, anchor: "r", box: true, size: 40 });
S.finish();
