// BASEMAP: atlantic
// 'On the sixth of April, the United States declared war on Germany.' date on 'sixth'; Washington pin; tag on 'war'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const DC = S.P("DC"), BER = S.P("BERLIN");
S.clouds(6, 0.14);
S.camera([[0, DC[0] + 420, DC[1] - 60, 0.82], [END, DC[0] + 520, DC[1] - 80, 0.9]]);
S.date("6 APRIL 1917", wt("sixth", 0.4));
S.pin(DC, "WASHINGTON", { t: 0.2, anchor: "l" });
S.pin(BER, "GERMANY", { t: wt("Germany", 3.6), anchor: "r", color: "#D9572B", rings: false });
S.tag("WAR", DC, { t: wt("war", 2.8), anchor: "t", gap: 54, size: 46, boxColor: "rgba(150,40,30,.92)" });
S.finish();
