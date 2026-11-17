// BASEMAP: oahu_sw
// IOWA / ASTORIA / PASADENA log marks (named on their words) converge to one area on 'worked'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const WR = P("WRECK");
S.camera([[0, 1250, 900, 1.52], [END, 1250, 900, 1.5]]);
S.icon("q", WR, { t: 0, size: 90, color: "#D9572B", bob: 10, until: wt("worked", 3.6) + 0.8 });
const home = [S.off(WR, -11000, 9000), S.off(WR, 12000, 6000), S.off(WR, 1500, -13000)];
const dest = [S.off(WR, -2600, 1800), S.off(WR, 2800, 1200), S.off(WR, 300, -2600)];
const names = [["IOWA", "Iowa"], ["ASTORIA", "Astoria"], ["PASADENA", "Pasadena"]], tw = wt("worked", 3.6);
const at = (i) => (t) => { const u = Math.min(1, Math.max(0, (t - tw) / 1.4)), e = u * u * (3 - 2 * u); return [home[i][0] + (dest[i][0] - home[i][0]) * e, home[i][1] + (dest[i][1] - home[i][1]) * e]; };
home.forEach((p, i) => {
  const el = S.dot(p, { t: 0, r: 12, color: "#f3eee2" });
  B.tl.to(el, { x: dest[i][0] - p[0], y: dest[i][1] - p[1], duration: 1.4, ease: "sine.inOut" }, tw);
  S.label(names[i][0], at(i), { t: wt(names[i][1], 1.0 + i), anchor: i === 0 ? "l" : "r", size: 42, gap: 30, dy: i === 2 ? 40 : -30 });
});
S.circ(WR, 0, { px: 150, t: tw + 1.2, color: "#D9572B", dash: [14, 10], width: 5 });
S.finish();
