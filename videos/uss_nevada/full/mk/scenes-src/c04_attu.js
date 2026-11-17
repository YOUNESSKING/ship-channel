// BASEMAP: northpac
// ATTU pin on 'Attu', ALEUTIAN ISLANDS on 'Aleutians', MAY 1943.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const AT = P("ATTU");
S.camera([[0, AT[0] + 120, AT[1] + 40, 1.7], [END, AT[0] + 60, AT[1] + 10, 2.4]]);
S.date("MAY 1943", 0.5);
S.pin(AT, "ATTU", { t: wt("Attu", 2.2), color: "#D9572B", anchor: "l", size: 56, gap: 40, dy: 40, ringR: 36 });
S.label("ALEUTIAN ISLANDS", S.G(53.6, -176.5), { t: wt("Aleutians", 3.2), anchor: "c", size: 44, color: "#8fb0cc" });
S.finish();
