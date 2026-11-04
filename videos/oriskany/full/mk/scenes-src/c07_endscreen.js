// BASEMAP: pan_close
// "Tell us in the comments." End map holds both pins on the LEFT half (right half kept clear for the YouTube end screen);
// card 'BEST WAY? OR CHEAPEST?' on 'Tell'; slow drift for the 18 s end-screen hold.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF"), SSUS = S.P("SSUS");
S.clouds(7, 0.14);
const MID = [(REEF[0] + SSUS[0]) / 2, (REEF[1] + SSUS[1]) / 2];
S.camera([[0, MID[0] + 420, MID[1] - 160, 1.1], [END, MID[0] + 470, MID[1] - 190, 1.22]]);
S.img("assets/media/carrier_top.png", [REEF[0], REEF[1] - 34], { t: 0.0, w: 140, filter: "brightness(1.9) drop-shadow(0 0 12px rgba(227,194,122,.9))" });
S.ring(REEF, { t: 0.0, r: 42 });
S.tag("USS ORISKANY", REEF, { t: 0.0, anchor: "b", gap: 40 });
S.img("assets/media/liner_top.png", [SSUS[0], SSUS[1] - 34], { t: 0.0, w: 160, filter: "drop-shadow(0 0 10px rgba(127,211,216,.8))" });
S.ring(SSUS, { t: 0.0, color: S.TEAL, r: 42 });
S.tag("SS UNITED STATES", SSUS, { t: 0.0, anchor: "b", gap: 40 });
S.route([REEF, [REEF[0] + 160, REEF[1] - 30], SSUS], { t: 0.0, dur: 0.01, dash: [18, 12], width: 4, color: "rgba(243,238,226,.7)" });
S.card('<div style="font-size:64px;letter-spacing:.08em;line-height:1.15">BEST WAY?<br><span style="color:#e3c27a">OR CHEAPEST?</span></div><div style="font-size:40px;letter-spacing:.2em;margin-top:14px;color:#cfd8de">TELL US IN THE COMMENTS</div>', w("Tell"), { left: 110, top: 150, width: 720 });
S.finish();
