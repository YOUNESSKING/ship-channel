// BASEMAP: potomac
// End map: bay + White House on the left half; card on 'Tell'; slow drift for the 18 s hold.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const WH = S.P("WH"), MB = S.P("MALLOWS"); const MID = [(WH[0] + MB[0]) / 2, (WH[1] + MB[1]) / 2];
S.clouds(7, 0.12);
S.camera([[0, MID[0] + 420, MID[1], 0.95], [END, MID[0] + 450, MID[1] - 20, 1.02]]);
S.pin(MB, "MALLOWS BAY", { t: 0.0, anchor: "l", color: "#D9572B" });
S.pin(WH, "THE WHITE HOUSE", { t: 0.0, anchor: "l", rings: false });
S.route([WH, MB], { t: 0.0, dur: 0.01, dash: [14, 10], width: 4, color: "rgba(243,238,226,.7)" });
S.card('<div style="font-size:64px;letter-spacing:.08em;line-height:1.15">SAVE IT?<br><span style="color:#D9572B">OR LET IT GO?</span></div><div style="font-size:40px;letter-spacing:.2em;margin-top:14px;color:#cfd8de">TELL US IN THE COMMENTS</div>', wt("Tell", 4.6), { left: 110, top: 150, width: 720 });
S.finish();
