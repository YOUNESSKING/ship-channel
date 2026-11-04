// ---------- ship kit: clean SVG silhouettes (side profile + top-down) for the ship channel, in the map-kit / va_kit look.
// Drawn in-house from the published hull dimensions and public-domain US Navy plans / photos (NHHC, NavSource, HAER) as
// reference only; nothing traced. Simplified on purpose: they must read at 40-200 px on a map and at 1600 px in a cutaway.
//
// Ships (key: what, length): carrier = Essex-class angled-deck carrier, USS Oriskany (CV-34) after the SCB-27A / SCB-125A refits
// (911 ft, hurricane bow, angled deck, starboard island); battleship = Iowa-class style WWII fast battleship (887 ft, 3 triple
// turrets, 2 funnels); de = John C. Butler-class destroyer escort (306 ft, two 5"/38 singles); sub = Gato / Balao fleet submarine
// (312 ft, cut-down fairwater, 5"/25 deck gun); liner = SS United States (990 ft, two winged funnels in red / white / blue).
//
// Coordinates are FEET: x from the stern (0) to the bow (L), bow = +x (right). Side view: y = 0 is the waterline, + is down (keel
// at +draught). Top view: y = 0 is the centreline, port = -y (up when the bow points right).
//
// Use in a HyperFrames / map-kit scene (plain <script src="kit/ship/ships.js">, defines window.ShipKit):
//   ShipKit.svg("carrier", "top", { w: 120 })                     -> SVG string, map look (side colour blue, keyline, glow)
//   ShipKit.svg("liner", "side", { w: 900, paint: "livery" })    -> realistic flat colours
//   const S = ShipKit.map(GG, { tl, posOn, pinS });               // after `const GG = GGK(B)` (gg.js)
//   S.pin("carrier", "top", x, y, { w: 70, t: 2, rot: -30 });    // a counter on the map (GG.pin)
//   S.sail("de", pts, t, dur, until, { w: 40, wake: true });     // follows a path, heading = path direction (va_kit pattern)
//   S.sinkTop(handle, t, { dur: 3 });                            // on-map sinking: list, darken, settle, rings + bubbles
// In Node: const ShipKit = require("./ships.js").
(function (root) {
  "use strict";

  // ---------------- colours (map-kit: blue #1f4fc4 / red #c4121f sides, cream keyline #f3eee2, glow as in va_kit SHIPSVG)
  const SIDE = {
    blue: { col: "#1f4fc4", rim: "#9fc0ff", glow: "#6f9bff", dark: "#12306f" },
    red:  { col: "#c4121f", rim: "#ffb0a6", glow: "#ff7a6a", dark: "#6e0a12" },
    grey: { col: "#5d6874", rim: "#c9d3dc", glow: "#aebccb", dark: "#323941" },
  };
  const CREAM = "#f3eee2", INK = "#0b0c0e";
  const NAVY_LIVERY = { hull: "#7f8a93", under: "#5e2a26", boot: "#1c1e21", shade: "#4f575f", deck: "#545b63", sup: "#8f99a2", sup2: "#a7b0b8",
    turret: "#76818a", det: "#1d2125", line: "#22272c", mark: "#ece6d6", rim: "#14171a", edge: "#2a2f34", funR: "#1d2125", funW: "#1d2125", funB: "#1d2125",
    boat: "#a7b0b8", win: null, glow: "rgba(0,0,0,0)" };
  const LIVERY = {
    carrier: Object.assign({}, NAVY_LIVERY, { deck: "#3e444b" }),
    battleship: Object.assign({}, NAVY_LIVERY, { deck: "#4b5866" }),
    de: Object.assign({}, NAVY_LIVERY),
    sub: Object.assign({}, NAVY_LIVERY, { hull: "#2c3136", sup: "#363c42", sup2: "#40474e", shade: "#22262a", deck: "#3d4349", turret: "#40474e", rim: "#0e1012", line: "#0e1012", under: "#2a2224" }),
    liner: { hull: "#16181b", under: "#a33a2f", boot: "#f1efe8", shade: "#26292d", deck: "#b9976a", sup: "#f1efe8", sup2: "#dcd9d0", turret: "#dcd9d0",
      det: "#202327", line: "#2a2d31", mark: "#f3eee2", rim: "#0d0f11", edge: "#8d8a82", funR: "#c8322b", funW: "#f3f1ea", funB: "#1c3570",
      boat: "#ebe7dc", win: "#3a3e45", glow: "rgba(0,0,0,0)" },
  };
  function sidePaint(kind, view, s) {
    if (view === "side") return { hull: s.col, under: s.col, boot: s.col, shade: s.dark, deck: s.col, sup: s.col, sup2: s.col, turret: s.col,
      det: INK, line: CREAM, mark: CREAM, rim: CREAM, edge: CREAM, funR: s.col, funW: s.col, funB: s.col, boat: s.dark, win: null, glow: s.glow };
    const deck = { carrier: "#3b424c", battleship: "#c7a26b", de: "#5b646e", sub: "#3a4048", liner: "#c7a26b" }[kind];
    return { hull: s.col, under: s.col, boot: s.col, shade: "#2a3038", deck, sup: "#dcd6c8", sup2: "#c4bfb2", turret: "#4a525c", det: INK, line: CREAM,
      mark: CREAM, rim: kind === "carrier" ? s.col : s.rim, edge: "#2a2e33", funR: "#20252e", funW: "#20252e", funB: "#20252e", boat: "#c4bfb2", win: null, glow: s.glow };
  }

  // ---------------- tiny shape builder
  const f1 = (v) => Math.round(v * 10) / 10;
  const P = (pts, close = true) => "M" + pts.map((p) => f1(p[0]) + " " + f1(p[1])).join(" L") + (close ? " Z" : "");
  const R = (x0, y0, x1, y1) => P([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]);
  const RR = (x0, y0, x1, y1, r) => `M${f1(x0 + r)} ${f1(y0)} L${f1(x1 - r)} ${f1(y0)} Q${f1(x1)} ${f1(y0)} ${f1(x1)} ${f1(y0 + r)} L${f1(x1)} ${f1(y1 - r)} Q${f1(x1)} ${f1(y1)} ${f1(x1 - r)} ${f1(y1)} L${f1(x0 + r)} ${f1(y1)} Q${f1(x0)} ${f1(y1)} ${f1(x0)} ${f1(y1 - r)} L${f1(x0)} ${f1(y0 + r)} Q${f1(x0)} ${f1(y0)} ${f1(x0 + r)} ${f1(y0)} Z`;
  const E = (cx, cy, rx, ry) => `M${f1(cx - rx)} ${f1(cy)} A${f1(rx)} ${f1(ry)} 0 1 0 ${f1(cx + rx)} ${f1(cy)} A${f1(rx)} ${f1(ry)} 0 1 0 ${f1(cx - rx)} ${f1(cy)} Z`;
  const mirrorY = (pts) => pts.concat(pts.slice().reverse().map((p) => [p[0], -p[1]]));
  // shape record: { d, role, k: "rim" (keyline) | "thin" (fine outline) | "none", line: stroke-only width factor, dash, clip: "hull" }
  const S_ = (d, role, k = "rim", extra = {}) => Object.assign({ d, role, k }, extra);
  const L_ = (x0, y0, x1, y1, role = "line", w = 0.6, extra = {}) => Object.assign({ d: `M${f1(x0)} ${f1(y0)} L${f1(x1)} ${f1(y1)}`, role, line: w }, extra);

  // a sheer line: deck height (negative = above water) along the length; flat aft, rising quadratically to the bow
  const sheer = (x, xs, yAft, yMid, yBow, L) => x <= xs ? yAft + (yMid - yAft) * (x / xs) : yMid + (yBow - yMid) * ((x - xs) / (L - xs)) ** 2;

  // ======================================================== the ships
  const SHIPS = {};

  // ---- Essex-class angled-deck carrier: USS Oriskany (CV-34) as refitted (SCB-27A 1950, SCB-125A 1959)
  SHIPS.carrier = {
    name: "Essex-class carrier (USS Oriskany, SCB-27A/125A)", L: 911, beam: 101, draught: 30, extremeWidth: 195,
    side: { y0: -160, y1: 30, keel: [[75, 30], [800, 30]], build() {
      const hullD = "M75 30 L800 30 Q852 30 868 10 L908 -55 L760 -55 L760 -27 L40 -27 L36 -10 Q42 20 75 30 Z";
      return [
        S_(R(36, -55, 762, -26), "shade", "none"),                                // open hangar band under the flight deck
        S_(hullD, "hull"),
        S_(R(30, -2, 880, 3), "boot", "none", { clip: hullD }),                    // boot-topping at the waterline
        S_(R(30, 3, 880, 40), "under", "none", { clip: hullD }),                   // below the waterline
        S_(P([[420, -56], [600, -56], [565, -44], [455, -44]]), "hull"),          // angled-deck sponson (port side)
        ...[130, 250, 690].map((x) => S_(R(x, -48, x + 30, -38), "hull", "thin")),  // 5"/38 gun sponsons
        S_("M0 -62 L911 -62 L909 -55 L6 -55 Q0 -57 0 -62 Z", "hull"),             // flight deck
        S_(P([[468, -62], [598, -62], [598, -80], [590, -80], [590, -96], [548, -96], [548, -84], [468, -84]]), "sup"),   // island
        S_(P([[474, -84], [528, -84], [520, -116], [466, -116]]), "sup"),          // funnel (raked aft)
        S_(P([[465, -116], [521, -116], [519, -121], [467, -121]]), "det", "none"),
        L_(560, -96, 560, -158), L_(538, -140, 582, -140),                         // pole mast + yard
        S_(R(546, -154, 574, -146), "det", "thin"),                                // SPS-43 "bedspring" air-search antenna
        S_(R(552, -108, 570, -102), "det", "none"),
      ]; } },
    top: { y0: -150, y1: 70, build() {
      const deck = [[0, -46], [62, -48], [585, -144], [626, -141], [690, -82], [735, -52], [850, -44], [905, -12], [911, 0], [905, 12], [850, 44],
        [740, 50], [604, 50], [604, 58], [458, 58], [458, 50], [0, 48]];
      return [
        S_(P(deck), "deck"),
        S_(R(700, -22, 748, 22), "shade", "thin"),                                // forward centreline elevator
        S_(R(182, -22, 226, 22), "shade", "thin"),                                // aft centreline elevator
        L_(70, -4, 600, -102, "mark", 0.9, { dash: "18 12" }),                      // angled-deck landing line
        L_(70, 40, 610, -60, "mark", 0.5, { dash: "6 10" }),                        // foul line
        L_(660, -15, 890, -6, "mark", 0.6), L_(660, 15, 890, 6, "mark", 0.6),       // C-11 bow catapults
        L_(760, 0, 900, 0, "mark", 0.5, { dash: "10 10" }),
        S_(R(462, 52, 598, 68), "sup"),                                            // island
        S_(E(492, 60, 20, 6), "det", "none"),                                      // funnel
        S_(E(560, 60, 4, 4), "det", "none"),                                       // mast
      ]; } },
  };

  // ---- WWII fast battleship, Iowa-class style
  const bbDeck = (x) => sheer(x, 430, -18, -20, -42, 887);
  const bbTurretSide = (x, raise, aft) => {
    const yb = bbDeck(x) - raise, s = aft ? -1 : 1, X = (dx) => x + s * dx;
    const out = [];
    if (raise) out.push(S_(R(x - 20, yb, x + 20, bbDeck(x) + 1), "hull", "thin"));   // barbette
    out.push(S_(P([[X(-30), yb], [X(-30), yb - 15], [X(-24), yb - 18], [X(16), yb - 18], [X(28), yb - 10], [X(28), yb]]), "turret"));
    out.push(S_(P([[X(26), yb - 11.5], [X(96), yb - 14], [X(96), yb - 10], [X(26), yb - 7.5]]), "turret", "thin"));
    return out;
  };
  const bbTurretTop = (x, aft) => {
    const s = aft ? -1 : 1, X = (dx) => x + s * dx;
    return [...[-8, 0, 8].map((y) => S_(R(Math.min(X(20), X(84)), y - 1.4, Math.max(X(20), X(84)), y + 1.4), "det", "none")),
      S_(P([[X(-28), -18], [X(20), -15], [X(26), -9], [X(26), 9], [X(20), 15], [X(-28), 18], [X(-34), 0]]), "turret", "thin")];
  };
  SHIPS.battleship = {
    name: "WWII fast battleship (Iowa-class style)", L: 887, beam: 108, draught: 37,
    side: { y0: -150, y1: 37, keel: [[62, 37], [800, 37]], build() {
      const pts = []; for (let x = 0; x <= 887; x += 29.567) pts.push([x, bbDeck(x)]);
      const hullD = P([...pts, [865, 0], [848, 26], [800, 37], [62, 37], [20, 30], [4, 0]]);
      return [
        S_(hullD, "hull"),
        S_(R(0, -2, 887, 3), "boot", "none", { clip: hullD }), S_(R(0, 3, 887, 40), "under", "none", { clip: hullD }),
        S_(R(296, -36, 566, bbDeck(296) + 1), "sup"),                              // deckhouse (01 level)
        S_(R(326, -50, 552, -36), "sup"),                                          // 02 level
        ...[340, 400, 470, 530].map((x) => S_(P([[x - 13, -36], [x - 13, -43], [x + 8, -44], [x + 13, -36]]), "turret", "thin")),   // 5"/38 twins
        S_(P([[300, -50], [334, -50], [330, -70], [304, -70]]), "sup"),           // aft director tower
        L_(352, -50, 348, -118), L_(334, -104, 364, -104),                        // main mast
        S_(P([[366, -50], [404, -50], [398, -94], [362, -94]]), "sup"), S_(R(361, -97, 399, -94), "det", "none"),      // aft funnel
        S_(P([[444, -50], [488, -50], [482, -100], [440, -100]]), "sup"), S_(R(439, -103, 483, -100), "det", "none"),  // fore funnel
        S_(P([[498, -50], [558, -50], [556, -76], [546, -90], [506, -90], [500, -72]]), "sup"),                       // fwd tower / conning tower
        S_(R(510, -106, 546, -90), "sup"), L_(528, -106, 528, -146), L_(506, -130, 550, -130),
        S_(R(515, -142, 541, -137), "det", "none"),
        ...bbTurretSide(232, 0, true), ...bbTurretSide(594, 13, false), ...bbTurretSide(662, 0, false),
      ]; } },
    top: { y0: -60, y1: 60, build() {
      const hull = [[0, -26], [10, -46], [50, -53], [540, -54], [700, -44], [800, -26], [887, 0]];
      const deck = [[14, -22], [22, -40], [55, -47], [540, -48], [690, -39], [790, -22], [866, 0]];
      return [
        S_(P(mirrorY(hull)), "hull"), S_(P(mirrorY(deck)), "deck", "none"),
        S_(RR(298, -24, 565, 24, 6), "sup", "thin"), S_(RR(330, -16, 548, 16, 4), "sup2", "thin"),
        ...[340, 400, 460, 520].flatMap((x) => [S_(RR(x - 7, -40, x + 7, -28, 2), "turret", "thin"), S_(RR(x - 7, 28, x + 7, 40, 2), "turret", "thin")]),
        S_(E(382, 0, 17, 10), "det", "none"), S_(E(462, 0, 19, 11), "det", "none"),
        ...bbTurretTop(232, true), ...bbTurretTop(596, false), ...bbTurretTop(660, false),
      ]; } },
  };

  // ---- destroyer escort, John C. Butler class
  const deDeck = (x) => sheer(x, 180, -11, -12, -22, 306);
  const mountSide = (x, aft, h = 8, len = 24) => {
    const yb = deDeck(x), s = aft ? -1 : 1, X = (dx) => x + s * dx;
    return [S_(P([[X(-13), yb], [X(-13), yb - h], [X(-8), yb - h - 2], [X(7), yb - h - 2], [X(13), yb - h / 2], [X(13), yb]]), "turret", "thin"),
      S_(P([[X(12), yb - h / 2 - 1.5], [X(12 + len), yb - h / 2 - 2.5], [X(12 + len), yb - h / 2 - 0.5], [X(12), yb - h / 2 + 0.5]]), "turret", "none")];
  };
  SHIPS.de = {
    name: "Destroyer escort (John C. Butler class)", L: 306, beam: 37, draught: 13.5,
    side: { y0: -70, y1: 14, keel: [[22, 13.5], [268, 13.5]], build() {
      const pts = []; for (let x = 0; x <= 306; x += 10.2) pts.push([x, deDeck(x)]);
      const hullD = P([...pts, [295, 0], [287, 10], [268, 13.5], [22, 13.5], [6, 10], [1, 0]]);
      return [
        S_(hullD, "hull"),
        S_(R(0, -1, 306, 1.5), "boot", "none", { clip: hullD }), S_(R(0, 1.5, 306, 16), "under", "none", { clip: hullD }),
        S_(R(112, -20, 238, deDeck(112) + 0.5), "sup"),                            // deckhouse
        S_(P([[200, -20], [240, -20], [238, -30], [230, -34], [204, -34]]), "sup"),  // bridge
        S_(R(206, -37, 228, -34), "sup", "thin"),
        L_(214, -37, 212, -66, "line", 0.45), L_(202, -56, 224, -56, "line", 0.4), S_(R(207, -64, 219, -61), "det", "none"),
        S_(P([[150, -20], [172, -20], [167, -38], [146, -38]]), "sup"), S_(R(145, -40, 168, -38), "det", "none"),     // funnel
        S_(R(120, -24, 146, -20), "turret", "thin"),                                // torpedo tubes
        S_(R(96, -18, 108, -12), "turret", "thin"), L_(104, -17, 114, -22, "line", 0.5),   // 40 mm
        ...mountSide(255, false), ...mountSide(62, true),
        S_(R(3, -15, 15, -11), "det", "none"),                                      // depth-charge racks
      ]; } },
    top: { y0: -22, y1: 22, build() {
      const hull = [[0, -14], [4, -18], [14, -18.5], [190, -18.5], [250, -14], [306, 0]];
      const deck = [[5, -12], [9, -15.5], [16, -16], [188, -16], [246, -12], [296, 0]];
      return [
        S_(P(mirrorY(hull)), "hull"), S_(P(mirrorY(deck)), "deck", "none"),
        S_(RR(112, -9, 238, 9, 2), "sup", "thin"), S_(RR(200, -11, 238, 11, 3), "sup2", "thin"),
        S_(E(158, 0, 10, 5.5), "det", "none"), S_(R(122, -1.6, 148, 1.6), "turret", "thin"),
        S_(E(255, 0, 6.5, 6.5), "turret", "thin"), S_(R(261, -0.9, 282, 0.9), "det", "none"),
        S_(E(62, 0, 6.5, 6.5), "turret", "thin"), S_(R(38, -0.9, 56, 0.9), "det", "none"),
        S_(R(2, -11, 14, -7), "det", "none"), S_(R(2, 7, 14, 11), "det", "none"),
      ]; } },
  };

  // ---- fleet submarine, Gato / Balao class (surfaced)
  SHIPS.sub = {
    name: "Fleet submarine (Gato / Balao class)", L: 312, beam: 27, draught: 17,
    side: { y0: -48, y1: 18, keel: [[60, 17], [262, 17]], build() {
      const hullD = "M0 -3 L40 -6 L270 -6 Q300 -7 312 -9 L306 0 Q296 17 262 17 L60 17 Q20 15 4 4 Z";
      return [
        S_(hullD, "hull"),
        S_(R(0, 0.5, 312, 20), "under", "none", { clip: hullD }),
        ...Array.from({ length: 22 }, (_, k) => S_(R(48 + k * 10.5, -4.6, 52 + k * 10.5, -2.6), "det", "none")),   // limber holes
        S_(P([[138, -6], [142, -15], [156, -15], [160, -22], [196, -22], [202, -15], [212, -15], [214, -6]]), "sup"),   // fairwater
        L_(178, -22, 178, -44, "line", 0.5), L_(186, -22, 186, -40, "line", 0.5), L_(170, -22, 170, -35, "line", 0.4),
        S_(R(166, -38, 174, -35), "det", "none"),
        S_(R(147, -19, 153, -15), "turret", "thin"), S_(R(205, -19, 211, -15), "turret", "thin"),   // 20 / 40 mm
        S_(R(222, -10, 234, -6), "turret", "thin"),                                 // 5"/25 deck gun
        S_(P([[232, -9.5], [258, -11.5], [258, -10], [232, -8]]), "turret", "none"),
      ]; } },
    top: { y0: -16, y1: 16, build() {
      const hull = [[0, 0], [10, -6], [60, -13.5], [240, -13.5], [295, -9], [312, 0]];
      const deck = [[12, -2.5], [32, -5.5], [60, -6], [280, -6], [300, -3.5], [306, 0]];
      return [
        S_(P(mirrorY(hull)), "hull"), S_(P(mirrorY(deck)), "deck", "none"),
        S_(RR(140, -5.5, 212, 5.5, 3), "sup", "thin"), S_(RR(158, -4, 198, 4, 2), "sup2", "none"),
        S_(E(228, 0, 3.5, 3.5), "turret", "thin"), S_(R(231, -0.7, 252, 0.7), "det", "none"),
      ]; } },
  };

  // ---- SS United States (1952), two winged funnels
  const lnDeck = (x) => sheer(x, 560, -40, -44, -60, 990);
  const funnelSide = (cx, top) => {
    const rk = 18, b = -82, bw = 40, tw = 31;
    const fd = P([[cx - bw, b], [cx + bw, b], [cx + tw - rk, top], [cx - tw - rk, top]]);
    const atY = (y) => (y - b) / (top - b);   // 0 at base -> 1 at top
    const xL = (y) => cx - bw + (bw - tw - rk) * atY(y) - 0, xR = (y) => cx + bw - (bw - tw + rk) * atY(y);
    const band = (y0, y1, role) => S_(P([[xL(y0), y0], [xR(y0), y0], [xR(y1), y1], [xL(y1), y1]]), role, "none");
    return [S_(fd, "funR"), band(top + 16, top + 10, "funW"), band(top + 10, top, "funB"),
      S_(P([[cx - tw - rk - 12, top + 6], [cx - tw - rk, top], [cx + tw - rk, top], [cx + tw - rk + 12, top + 6], [cx + tw - rk + 2, top + 3], [cx - tw - rk - 2, top + 3]]), "funB"),   // sampan fins
      S_(fd, "funR", "rim", { fillNone: true })];
  };
  SHIPS.liner = {
    name: "SS United States (ocean liner, 1952)", L: 990, beam: 101.5, draught: 32,
    side: { y0: -158, y1: 32, keel: [[70, 32], [880, 32]], build() {
      const pts = []; for (let x = 0; x <= 990; x += 33) pts.push([x, lnDeck(x)]);
      const hullD = P([...pts, [950, 0], [930, 26], [880, 32], [70, 32], [22, 28], [8, 0], [2, -20]]);
      const tier = (x0, x1, top, slope) => { const b0 = lnDeck(x0) + 1, b1 = lnDeck(x1) + 1; return S_(P([[x0, b0], [x1, b1], [x1 - slope, top], [x0 + 6, top]]), "sup"); };
      return [
        S_(hullD, "hull"),
        S_(R(0, -1, 990, 2), "boot", "none", { clip: hullD }), S_(R(0, 2, 990, 40), "under", "none", { clip: hullD }),
        tier(140, 822, -58, 10), tier(190, 782, -70, 16), tier(250, 742, -82, 18),
        S_(P([[690, -82], [738, -82], [736, -88], [728, -92], [694, -92]]), "sup"),   // bridge
        L_(150, -51, 815, -54, "win", 1.0, { dash: "3 5" }), L_(200, -64, 775, -64, "win", 1.0, { dash: "3 5" }),
        ...Array.from({ length: 10 }, (_, k) => S_(RR(292 + k * 44, -69.5, 322 + k * 44, -64, 2.5), "boat", "thin")),   // lifeboats
        L_(700, -92, 696, -150, "line", 0.5), L_(684, -136, 710, -136, "line", 0.45),
        ...funnelSide(375, -136), ...funnelSide(560, -140),
      ]; } },
    top: { y0: -56, y1: 56, build() {
      const hull = [[0, -34], [8, -48], [70, -50.5], [620, -50.75], [800, -40], [920, -20], [990, 0]];
      const deck = [[8, -30], [16, -43], [72, -45], [620, -45], [795, -35], [912, -17], [976, 0]];
      const fun = (cx) => [S_(P([[cx - 46, -6], [cx - 36, -27], [cx - 30, -27], [cx - 30, 27], [cx - 36, 27], [cx - 46, 6]]), "funB", "thin"),   // sampan fins
        S_(E(cx, 0, 36, 21), "funR", "thin"), S_(E(cx - 6, 0, 24, 13), "funB", "none")];
      return [
        S_(P(mirrorY(hull)), "hull"), S_(P(mirrorY(deck)), "deck", "none"),
        S_(RR(140, -42, 822, 42, 14), "sup", "thin"), S_(RR(250, -33, 742, 33, 10), "sup2", "thin"),
        ...Array.from({ length: 10 }, (_, k) => [S_(R(292 + k * 44, -44, 322 + k * 44, -39), "boat", "thin"), S_(R(292 + k * 44, 39, 322 + k * 44, 44), "boat", "thin")]).flat(),
        ...fun(366), ...fun(551),
      ]; } },
  };

  // ======================================================== SVG output
  let uid = 0;
  function resolvePaint(kind, view, o) {
    if (o.paint === "livery") return Object.assign({}, LIVERY[kind], o.colors || {});
    const s = typeof o.col === "object" ? o.col : SIDE[o.col || o.side || "blue"] || { col: o.col, rim: o.rim || "#f3eee2", glow: o.glowCol || o.col, dark: o.dark || "#1b1f24" };
    return Object.assign(sidePaint(kind, view, s), o.colors || {});
  }
  /** SVG string. o: { w: on-screen px of the ship's length (default 120), paint: "side" (map counter, default) | "livery",
   *  col: "blue" | "red" | "grey" | "#hex" (side paint), keyline: px (default ~1.4-2.6), glow: true (CSS drop-shadow like va_kit),
   *  flip: true (bow left), colors: {role: colour} overrides, id: prefix for clip ids, attrs: extra <svg> attributes, below: false (side view: hide below the waterline) } */
  function svg(kind, view, o = {}) {
    const sh = SHIPS[kind]; if (!sh) throw new Error("ShipKit: unknown ship " + kind);
    const V = sh[view]; if (!V) throw new Error("ShipKit: view must be side or top");
    const p = resolvePaint(kind, view, o), L = sh.L, w = o.w || 120;
    const pad = L * 0.025, y1 = o.below === false && view === "side" ? 2 : V.y1;
    const vb = [-pad, V.y0 - pad, L + 2 * pad, y1 - V.y0 + 2 * pad], k = vb[2] / w;   // feet per screen px
    const key = (o.keyline != null ? o.keyline : Math.max(1.2, Math.min(2.6, w * 0.016))) * k;
    const h = Math.round(w * vb[3] / vb[2]);
    const pre = (o.id || "shk") + (++uid);
    let defs = "", body = "", nclip = 0;
    for (const s of V.build()) {
      if (o.below === false && view === "side" && (s.role === "under")) continue;
      const fill = s.fillNone || s.line ? "none" : p[s.role];
      if (fill === undefined || (s.role === "win" && !p.win)) continue;
      let attr = "";
      if (s.line) attr = ` stroke="${p[s.role]}" stroke-width="${f1(s.line * key * 10) / 10}" stroke-linecap="round"${s.dash ? ` stroke-dasharray="${s.dash}"` : ""}`;
      else if (s.k === "rim") attr = ` stroke="${p.rim}" stroke-width="${f1(key * 10) / 10}" stroke-linejoin="round"`;
      else if (s.k === "thin") attr = ` stroke="${p.edge}" stroke-width="${f1(key * 0.45 * 10) / 10}" stroke-linejoin="round"`;
      if (s.clip) { const id = `${pre}c${nclip++}`; defs += `<clipPath id="${id}"><path d="${s.clip}"/></clipPath>`; attr += ` clip-path="url(#${id})"`; }
      body += `<path d="${s.d}" fill="${fill}"${attr}/>`;
    }
    if (o.below === false && view === "side") { const id = `${pre}w`; defs += `<clipPath id="${id}"><rect x="${vb[0]}" y="${vb[1]}" width="${vb[2]}" height="${-vb[1] + 1}"/></clipPath>`; body = `<g clip-path="url(#${id})">${body}</g>`; }
    if (o.flip) body = `<g transform="translate(${L} 0) scale(-1 1)">${body}</g>`;
    const glow = o.glow === false || o.paint === "livery" && !o.glow ? "" :
      `filter:drop-shadow(0 0 ${f1(Math.max(2, w * 0.035))}px ${p.glow}) drop-shadow(0 ${f1(w * 0.012)}px ${f1(w * 0.02)}px rgba(0,0,0,.7));`;
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="${vb.map(f1).join(" ")}" style="display:block;overflow:visible;${glow}"${o.attrs ? " " + o.attrs : ""}>${defs ? `<defs>${defs}</defs>` : ""}${body}</svg>`;
  }
  /** geometry for animations: viewBox, keel points, top of the masts, draught (all feet, side view) */
  function meta(kind) {
    const s = SHIPS[kind];
    return { kind, name: s.name, L: s.L, beam: s.beam, draught: s.draught, sideY0: s.side.y0, sideY1: s.side.y1, keel: s.side.keel,
      topY0: s.top.y0, topY1: s.top.y1, pad: s.L * 0.025 };
  }

  // ======================================================== map-kit helpers (HyperFrames scenes)
  /** const S = ShipKit.map(GG, { tl: B.tl, posOn, pinS, SFX }) ; all optional except GG */
  function map(GG, env = {}) {
    const tl = env.tl || (GG && GG.tl) || (root.B && root.B.tl);
    const gs = root.gsap;
    const posOn = env.posOn || ((pts, f) => { let Lt = 0; const seg = []; for (let j = 1; j < pts.length; j++) { const d = Math.hypot(pts[j][0] - pts[j - 1][0], pts[j][1] - pts[j - 1][1]); seg.push(d); Lt += d; }
      let d = f * Lt; for (let j = 0; j < seg.length; j++) { if (d <= seg[j]) { const a = pts[j], b = pts[j + 1], k = d / (seg[j] || 1); return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]; } d -= seg[j]; } return pts[pts.length - 1]; });
    const keep = env.pinS || ((el) => el);
    const SFXf = env.SFX || root.SFX;
    const M = {};
    /** a ship pin on the map. o: svg() options + { t, until, rot (deg, top view: 0 = bow east), pop } */
    M.pin = (kind, view, x, y, o = {}) => {
      const el = keep(GG.pin(`<div>${svg(kind, view, o)}</div>`, x, y, { t: o.t, until: o.until, pop: o.pop }));
      const sv = el.querySelector("svg"); if (o.rot) gs.set(sv, { rotation: o.rot });
      if (o.t == null) gs.set(el, { autoAlpha: 1 });
      return { el, sv, kind, at: () => [x, y] };
    };
    /** a top-down ship along a path; heading follows the path (va_kit ship() pattern). o: svg() options + { n, ease, wake, wakeCol } */
    M.sail = (kind, pts, t, dur, until, o = {}) => {
      const el = keep(GG.pin(`<div>${svg(kind, "top", o)}</div>`, pts[0][0], pts[0][1], { t: t > 0 ? t : null, until }));
      if (!(t > 0)) gs.set(el, { autoAlpha: 1 });
      const sv = el.querySelector("svg"), n = o.n || 40, ease = o.ease || ((u) => u);
      const head = (f) => { const a = posOn(pts, Math.max(0, f - 0.01)), b = posOn(pts, Math.min(1, f + 0.01)); return Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI; };
      gs.set(sv, { rotation: head(0) });
      for (let k = 1; k <= n; k++) { const f0 = ease((k - 1) / n), f1v = ease(k / n), q = posOn(pts, f1v);
        tl.to(el, { left: q[0], top: q[1], duration: dur / n, ease: "none" }, t + (k - 1) * dur / n);
        tl.to(sv, { rotation: head((f0 + f1v) / 2), duration: Math.min(0.4, dur / n), ease: "none" }, t + (k - 1) * dur / n); }
      if (o.wake) M.wake(pts, t, dur, until, o);
      const at = (tt) => posOn(pts, ease(Math.min(1, Math.max(0, (tt - t) / dur))));
      return { el, sv, kind, at };
    };
    /** a fading white wake drawn behind a moving ship (world px). o: { wakeW (px, default 3), wakeCol } */
    M.wake = (pts, t, dur, until, o = {}) => {
      const NS = "http://www.w3.org/2000/svg", ov = document.getElementById("overlay");
      const p = document.createElementNS(NS, "path"); let Lt = 0; for (let j = 1; j < pts.length; j++) Lt += Math.hypot(pts[j][0] - pts[j - 1][0], pts[j][1] - pts[j - 1][1]);
      p.setAttribute("d", "M" + pts.map((q) => q.join(" ")).join(" L")); p.setAttribute("fill", "none"); p.setAttribute("stroke", o.wakeCol || "rgba(243,238,226,0.55)");
      p.setAttribute("stroke-width", o.wakeW || 3); p.setAttribute("stroke-linecap", "round"); p.style.filter = "blur(1px)";
      ov.insertBefore(p, ov.firstChild); gs.set(p, { strokeDasharray: `${Lt} ${Lt + 10}`, strokeDashoffset: Lt, opacity: 0 });
      tl.to(p, { opacity: 1, duration: 0.3 }, t); tl.to(p, { strokeDashoffset: 0, duration: dur, ease: o.ease ? "none" : "none" }, t);
      tl.to(p, { opacity: 0, duration: 2.0 }, until != null ? until : t + dur + 1.5);
      return p;
    };
    /** on-map sinking of a pinned / sailing ship (top view): lists, darkens, shrinks a little, sinks out; rings + bubbles.
     *  o: { dur (s, default 3), list (deg, default 14), sfx: "kind" or false } */
    M.sinkTop = (h, t, o = {}) => {
      const dur = o.dur || 3, sv = h.sv, el = h.el;
      tl.to(sv, { rotation: `+=${o.list || 14}`, duration: dur * 0.5, ease: "sine.inOut" }, t);
      tl.to(sv, { filter: "brightness(0.45) saturate(0.6)", scale: 0.9, duration: dur * 0.7, ease: "power1.in" }, t);
      tl.to(el, { autoAlpha: 0, duration: dur * 0.35, ease: "power1.in" }, t + dur * 0.65);
      const [x, y] = h.at(t);
      for (let k = 0; k < 3; k++) {
        const ring = keep(GG.pin(`<div style="width:40px;height:40px;border-radius:50%;border:2px solid rgba(243,238,226,0.8)"></div>`, x, y, {}));
        tl.fromTo(ring, { autoAlpha: 0.9, scale: 0.3 }, { autoAlpha: 0, scale: 2.4, duration: 1.8, ease: "power1.out", immediateRender: false }, t + dur * 0.55 + k * 0.6);
      }
      for (let k = 0; k < 10; k++) {
        const b = keep(GG.pin(`<div style="width:5px;height:5px;border-radius:50%;background:rgba(243,238,226,0.85)"></div>`, x + ((k * 37) % 23) - 11, y + ((k * 53) % 19) - 9, {}));
        tl.fromTo(b, { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 0.9, scale: 1.2, duration: 0.25, yoyo: true, repeat: 1, immediateRender: false }, t + dur * 0.5 + k * 0.17);
      }
      if (o.sfx !== false && SFXf) SFXf(o.sfx || "sink_whoomp", t + dur * 0.5);
      return el;
    };
    return M;
  }

  const api = { SHIPS, SIDE, LIVERY, svg, meta, map, list: Object.keys(SHIPS) };
  root.ShipKit = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
