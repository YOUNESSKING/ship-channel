// BASEMAP: pan_close
// "Now it is about to take her title." A gold 'WORLD'S LARGEST REEF' tag slides from the Oriskany pin to the SS United States pin on 'take her title'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF"), SSUS = S.P("SSUS");
S.clouds(6, 0.14);
S.camera([[0, 1430, 840, 1.0], [END, 1460, 870, 1.08]]);
S.img("assets/media/carrier_top.png", [REEF[0], REEF[1] - 34], { t: 0.0, w: 150, filter: "brightness(1.9) drop-shadow(0 0 12px rgba(227,194,122,.9))" });
S.ring(REEF, { t: 0.0, r: 44 });
S.tag("USS ORISKANY", REEF, { t: 0.0, anchor: "b", gap: 40 });
S.img("assets/media/liner_top.png", [SSUS[0], SSUS[1] - 34], { t: 0.0, w: 170, filter: "drop-shadow(0 0 10px rgba(127,211,216,.8))" });
S.ring(SSUS, { t: 0.0, color: S.TEAL, r: 44 });
S.tag("SS UNITED STATES", SSUS, { t: 0.0, anchor: "b", gap: 40 });
// the title tag: rides a moving point from Oriskany to the liner
const t0 = w("take"), t1 = t0 + 1.0, A = [REEF[0], REEF[1] - 120], Bp = [SSUS[0], SSUS[1] - 120];
const e = gsap.parseEase("power2.inOut");
const pt = (t) => { const u = t <= t0 ? 0 : t >= t1 ? 1 : e((t - t0) / (t1 - t0)); return [A[0] + (Bp[0] - A[0]) * u, A[1] + (Bp[1] - A[1]) * u - Math.sin(u * Math.PI) * 60]; };
S.label("WORLD'S LARGEST REEF", pt, { t: 0.1, box: true, anchor: "c", size: 46, boxColor: "rgba(150,110,20,.95)", border: "#f5dc9a" });
S.finish();
