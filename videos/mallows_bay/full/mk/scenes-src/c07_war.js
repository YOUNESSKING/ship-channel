// BASEMAP: usa
// 'Then, in 1941, America went to war again.' date; tag 'WAR AGAIN' on 'war'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const DC = S.P("DC");
S.clouds(5, 0.12);
S.camera([[0, 1500, 820, 0.75], [END, DC[0] - 200, DC[1] + 20, 1.0]]);
S.date("1941", wt("forty", 0.5));
S.pin(DC, "WASHINGTON", { t: 0.4, anchor: "l" });
S.tag("WAR AGAIN", DC, { t: wt("war", 2.5), anchor: "t", gap: 56, size: 48, boxColor: "rgba(150,40,30,.92)" });
S.finish();
