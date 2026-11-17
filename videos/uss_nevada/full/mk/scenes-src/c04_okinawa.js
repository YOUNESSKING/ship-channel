// BASEMAP: pacific
// OKINAWA pin on 'Okinawa', 27 MARCH 1945 on 'March'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const OK = P("OKI");
S.camera([[0, OK[0] + 60, OK[1] + 20, 2.8], [END, OK[0] + 20, OK[1] + 5, 3.4]]);
S.date("27 MARCH 1945", wt("March", 0.5));
S.pin(OK, "OKINAWA", { t: wt("Okinawa", 1.4), color: "#D9572B", anchor: "r", size: 56, gap: 40, ringR: 36 });
S.finish();
