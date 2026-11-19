// BASEMAP: usa
// Hook frame 0: clean full-country map; camera pushes to the Pacific NW. DECEMBER 2014 on 'December', BREMERTON pin on 'Navy', big red 1c tag on 'cent'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BR = P("BREMERTON");
S.camera([[0, 1440, 810, 0.667], [END - 0.2, BR[0] + 60, BR[1] + 20, 1.7]]);
S.date("DECEMBER 2014", wt("December", 0.5));
S.pin(BR, "BREMERTON, WA", { t: wt("Navy", 3.45), color: RED, anchor: "r", size: 46, gap: 36, ringR: 36 });
S.tag("1¢", BR, { t: wt("cent", 3.95), anchor: "l", size: 110, gap: 60, dy: -20, boxColor: "rgba(150,40,30,.94)" });
S.finish();
