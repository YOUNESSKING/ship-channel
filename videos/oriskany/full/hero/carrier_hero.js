// ---------- CarrierHero: detailed side profile of USS Oriskany (CV-34) for close-up / cutaway shots (the sinking animation).
// The map silhouettes in kit/ship/ships.js stay simple on purpose; this one is the "hero" drawing: shaded hull, plating, hangar
// gallery openings, empty gun sponsons, hurricane bow, flight-deck overhangs, stepped island, waterline boot-topping.
//
// Drawn in FEET from the fact sheet + public-domain photos (reference only, nothing traced):
//   - NARA 7578428 (27 Apr 1959, after SCB-125A): hurricane bow, angled deck, island position and tiers, deck-edge layout.
//   - NARA 6698609 / 6698610 / 6698597 / 6698600 (May 2006, the stripped hulk): mast and antennas CUT DOWN before scuttling,
//     island reduced to its stepped block + funnel casing, rust-brown hull and deck, hangar openings plated / open.
//   - FACT_SHEET H2/H3 + FACTCHECK_C (FWC): resting on a 212 ft seabed, settled ~10 ft into the sediment (keel ~222 ft),
//     flight deck ~145-150 ft, top of the island 84 ft  =>  keel -> flight deck = 75 ft, flight deck -> island top = 63 ft.
// Elevators: the side view shows the starboard side (bow to the right), where no deck-edge elevator is drawn; the port deck-edge
// elevator (on the angled-deck sponson in NARA 7578428) and the centreline elevators are on the far side / in plan view only.
//
// Coordinates: x = 0 at the stern .. L at the bow (bow = +x), y = 0 at the waterline, + is down (keel at +draught).
//   CarrierHero.svg({ w, id, paint: "hulk" | "service", mast: false })  -> SVG string (w = px of the viewBox width incl. padding)
//   CarrierHero.meta(paint)  -> { L, draught, keel, deckY, islandTopY, islandX, pad, sideY0, sideY1 }  (same fields as ShipKit.meta)
(function (root) {
  "use strict";
  const L = 911, KEEL_TO_DECK = 75, ISLAND_ABOVE_DECK = 63;
  const DRAUGHT = { hulk: 24, service: 30 };           // the stripped 2006 hulk rode light; full-load Essex ~30 ft
  const f = (v) => Math.round(v * 100) / 100;
  const P = (pts, close = true) => "M" + pts.map((p) => f(p[0]) + " " + f(p[1])).join(" L") + (close ? " Z" : "");
  const R = (x0, y0, x1, y1) => P([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]);
  const rnd = (seed) => { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); };

  const PAINT = {
    hulk:    { hullTop: "#6f6a62", hullMid: "#585249", hullBot: "#3e3a35", rust: "rgba(122,64,34,.55)", rust2: "rgba(160,92,48,.35)", boot: "#141516",
               under: "#3b231f", under2: "#26171a", deck: "#6b4a31", deckEdge: "#d9c9a3", gallery: "#101214", sup: "#8a857b", supDark: "#57534c", win: "#16191c", line: "#1a1b1c", hi: "rgba(243,238,226,.55)" },
    service: { hullTop: "#9aa3ab", hullMid: "#7f8a93", hullBot: "#5f6870", rust: "rgba(90,70,60,.18)", rust2: "rgba(90,70,60,.12)", boot: "#16181a",
               under: "#6a2b26", under2: "#45201d", deck: "#3e444b", deckEdge: "#ece6d6", gallery: "#15191c", sup: "#a2abb3", supDark: "#6d767e", win: "#1b2024", line: "#22272c", hi: "rgba(243,238,226,.6)" },
  };

  function meta(paint = "hulk") {
    const D = DRAUGHT[paint] || 24, deckY = D - KEEL_TO_DECK, top = deckY - ISLAND_ABOVE_DECK;
    return { kind: "carrier", name: "USS Oriskany (CV-34), hero side profile", L, beam: 101, draught: D, keel: [[70, D], [800, D]],
      deckY, islandTopY: top, islandX: [468, 602], keelToDeck: KEEL_TO_DECK, islandAboveDeck: ISLAND_ABOVE_DECK,
      sideY0: top - 14, sideY1: D + 2, pad: L * 0.025 };
  }

  function svg(o = {}) {
    const paint = o.paint === "service" ? "service" : "hulk", C = PAINT[paint], M = meta(paint), D = M.draught, yF = M.deckY;
    const id = o.id || "ch", pad = M.pad;
    const vb = [-pad, M.sideY0 - pad, L + 2 * pad, (M.sideY1 - M.sideY0) + 2 * pad];
    const w = o.w || 1200, h = w * vb[3] / vb[2];
    const yH = yF + 20;                                           // hangar deck (gallery band yH .. yF+3)
    // ---- hull outline: transom stern, straight keel, raked stem into the enclosed hurricane bow
    const hull = P([[36, yF + 3], [30, yH], [24, -6], [36, 12], [70, D], [800, D], [838, D - 2], [858, 10], [872, -8], [892, -34], [906, yF + 2]]);
    const parts = [];
    const defs = `
      <linearGradient id="${id}-hg" x1="0" y1="${yF}" x2="0" y2="${D}" gradientUnits="userSpaceOnUse">
        <stop offset="0" stop-color="${C.hullTop}"/><stop offset="0.55" stop-color="${C.hullMid}"/><stop offset="0.72" stop-color="${C.hullBot}"/>
        <stop offset="0.74" stop-color="${C.boot}"/><stop offset="0.8" stop-color="${C.under}"/><stop offset="1" stop-color="${C.under2}"/></linearGradient>
      <linearGradient id="${id}-ao" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
      <linearGradient id="${id}-sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${C.sup}"/><stop offset="1" stop-color="${C.supDark}"/></linearGradient>
      <linearGradient id="${id}-bow" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient>
      <clipPath id="${id}-hc"><path d="${hull}"/></clipPath>`;
    // far-side angled-deck sponson (port side, beyond the deck): a darker plate just visible under the deck amidships
    parts.push(`<path d="${P([[400, yF + 2], [620, yF + 2], [596, yF + 9], [430, yF + 9]])}" fill="${C.supDark}" opacity=".8"/>`);
    // stern overhang supports
    for (const x of [6, 16, 26]) parts.push(`<path d="${P([[x, yF + 3], [x + 2.2, yF + 3], [x + 10, yH], [x + 7.8, yH]])}" fill="${C.supDark}"/>`);
    // hull body + gradient
    parts.push(`<path d="${hull}" fill="url(#${id}-hg)"/>`);
    // hull details, clipped to the hull
    let det = "";
    // plating seams + frames
    for (const y of [-26, -17, -8, 6, 15]) det += `<path d="M0 ${y} L${L} ${y}" stroke="${C.line}" stroke-opacity=".28" stroke-width=".35"/>`;
    for (let x = 60; x < 880; x += 26) det += `<path d="M${x} ${yH} L${x} ${D}" stroke="${C.line}" stroke-opacity=".14" stroke-width=".3"/>`;
    // rust streaks (seeded): run down from scuppers / openings
    const r = rnd(34);
    for (let k = 0; k < (paint === "hulk" ? 70 : 18); k++) {
      const x = 40 + r() * 820, y0 = yH + r() * 6, len = 6 + r() * 26, wd = 0.6 + r() * 2.2;
      det += `<path d="M${f(x)} ${f(y0)} L${f(x + wd)} ${f(y0)} L${f(x + wd * 0.4)} ${f(y0 + len)} Z" fill="${r() < 0.6 ? C.rust : C.rust2}"/>`;
    }
    // portholes / scuttles
    for (let x = 90; x < 860; x += 13 + (x % 7)) det += `<circle cx="${x}" cy="-21" r=".75" fill="${C.win}" opacity=".85"/>`;
    // hangar gallery band: dark openings between frames (Essex open hangar; some plated over on the hulk)
    det += `<path d="${R(40, yF + 3, 800, yH)}" fill="${C.gallery}"/>`;
    for (let x = 44, k = 0; x + 25 < 798; x += 31, k++) {
      const plated = paint === "hulk" ? (k * 7) % 5 === 0 : (k * 3) % 4 === 0;
      det += `<path d="${R(x, yF + 5, x + 25, yH - 1.5)}" fill="${plated ? C.hullMid : "#07090a"}" opacity="${plated ? 0.9 : 1}"/>`;
      if (!plated) det += `<path d="${R(x, yF + 5, x + 25, yF + 9)}" fill="${C.supDark}" opacity=".55"/>`;   // rolled-up curtain
      det += `<path d="M${x + 27.5} ${yF + 3} L${x + 27.5} ${yH}" stroke="${C.supDark}" stroke-width="2"/>`;
    }
    det += `<path d="M40 ${yH} L800 ${yH}" stroke="${C.hi}" stroke-opacity=".5" stroke-width=".6"/>`;
    // ambient occlusion under the flight deck overhang, shade toward the bow
    det += `<path d="${R(0, yF + 2, L, yF + 12)}" fill="url(#${id}-ao)"/>`;
    det += `<path d="${R(780, yF, L, D + 4)}" fill="url(#${id}-bow)"/>`;
    // boot-topping crisp line + waterline highlight
    det += `<path d="${R(0, -1.4, L, 1.4)}" fill="${C.boot}"/><path d="M0 -1.5 L${L} -1.5" stroke="${C.hi}" stroke-opacity=".35" stroke-width=".5"/>`;
    // hull number on the bow (hulk: faded)
    det += `<text x="828" y="${yH + 10}" font-family="Oswald,sans-serif" font-weight="700" font-size="14" fill="${paint === "hulk" ? "rgba(225,215,195,.32)" : "#ece6d6"}">34</text>`;
    parts.push(`<g clip-path="url(#${id}-hc)">${det}</g>`);
    // gun sponsons (guns removed on the hulk), starboard catwalks
    for (const x of [118, 246, 702]) parts.push(`<path d="${P([[x, yF + 6], [x + 34, yF + 6], [x + 30, yF + 14], [x + 4, yF + 14]])}" fill="url(#${id}-sg)" stroke="${C.line}" stroke-width=".4"/>`);
    parts.push(`<path d="${R(30, yF + 2, 790, yF + 4.2)}" fill="${C.supDark}"/>`);
    // flight deck slab (overhangs at both ends) + deck edge highlight
    parts.push(`<path d="${P([[0, yF], [L - 6, yF], [L, yF + 1.5], [L - 4, yF + 3.2], [4, yF + 3.2], [0, yF + 2]])}" fill="${C.deck}" stroke="${C.line}" stroke-width=".4"/>`);
    parts.push(`<path d="M0 ${yF + 0.2} L${L - 6} ${yF + 0.2}" stroke="${C.deckEdge}" stroke-opacity=".75" stroke-width=".7"/>`);
    // bow overhang braces (hurricane bow meets the deck)
    parts.push(`<path d="${P([[880, yF + 3], [906, yF + 2], [898, yF + 10]])}" fill="${C.hullTop}" opacity=".8"/>`);
    // ---- island: stepped block (starboard deck edge), bridge windows, funnel casing raked aft, mast cut down on the hulk
    const ix0 = M.islandX[0], ix1 = M.islandX[1], top = M.islandTopY;
    const isl = [];
    isl.push(`<path d="${P([[ix0, yF], [ix1, yF], [ix1, yF - 14], [ix0 + 6, yF - 14]])}" fill="url(#${id}-sg)"/>`);              // 01-02 levels
    isl.push(`<path d="${P([[ix0 + 10, yF - 14], [ix1 - 8, yF - 14], [ix1 - 8, yF - 26], [ix0 + 14, yF - 26]])}" fill="url(#${id}-sg)"/>`);   // 03-04
    isl.push(`<path d="${P([[ix0 + 44, yF - 26], [ix1 - 6, yF - 26], [ix1 - 2, yF - 30], [ix1 - 10, yF - 37], [ix0 + 48, yF - 37]])}" fill="url(#${id}-sg)"/>`);   // nav bridge (forward)
    isl.push(`<path d="${P([[ix0 + 58, yF - 37], [ix1 - 16, yF - 37], [ix1 - 18, yF - 46], [ix0 + 60, yF - 46]])}" fill="url(#${id}-sg)"/>`);  // pri-fly / flag
    // funnel casing (aft part of the island): the highest point = 63 ft above the deck (84 ft depth on the reef)
    isl.push(`<path d="${P([[ix0 + 8, yF - 26], [ix0 + 52, yF - 26], [ix0 + 46, top + 4], [ix0 + 40, top], [ix0 + 4, top], [ix0 + 2, top + 5]])}" fill="url(#${id}-sg)" stroke="${C.line}" stroke-width=".4"/>`);
    isl.push(`<path d="${R(ix0 + 4, top, ix0 + 40, top + 2.5)}" fill="${C.line}"/>`);
    // windows + level lines
    for (let x = ix0 + 50; x < ix1 - 12; x += 4.2) isl.push(`<path d="${R(x, yF - 34.5, x + 2.6, yF - 31)}" fill="${C.win}"/>`);
    for (let x = ix0 + 62; x < ix1 - 22; x += 4.5) isl.push(`<path d="${R(x, yF - 44, x + 2.8, yF - 41)}" fill="${C.win}"/>`);
    for (const y of [yF - 14, yF - 26, yF - 37]) isl.push(`<path d="M${ix0 + 2} ${y} L${ix1} ${y}" stroke="${C.hi}" stroke-opacity=".45" stroke-width=".5"/>`);
    for (let x = ix0 + 4; x < ix1; x += 9) isl.push(`<path d="M${x} ${yF - 2} L${x} ${yF - 12}" stroke="${C.line}" stroke-opacity=".3" stroke-width=".35"/>`);
    if (paint === "hulk") for (let k = 0; k < 16; k++) { const x = ix0 + 6 + r() * (ix1 - ix0 - 12); isl.push(`<path d="M${f(x)} ${yF - 26 + r() * 20} l1.2 0 l-.4 ${f(4 + r() * 8)} z" fill="${C.rust}"/>`); }
    // mast: the hulk has only a cut stub (removed before scuttling); "service" (or mast:true) gets the pole mast + SPS-43
    const mx = ix0 + 88;
    if (paint === "service" || o.mast) {
      isl.push(`<path d="M${mx} ${yF - 46} L${mx} ${top - 40}" stroke="${C.line}" stroke-width="1.6"/><path d="M${mx - 18} ${top - 26} L${mx + 18} ${top - 26}" stroke="${C.line}" stroke-width="1"/>`);
      isl.push(`<path d="${R(mx - 14, top - 38, mx + 14, top - 31)}" fill="${C.line}"/>`);
    } else {
      isl.push(`<path d="${P([[mx - 3, yF - 46], [mx + 3, yF - 46], [mx + 2.4, top + 2], [mx - 2.4, top + 3]])}" fill="${C.supDark}" stroke="${C.line}" stroke-width=".4"/>`);
      isl.push(`<path d="${R(mx - 7, top + 3, mx + 7, top + 5)}" fill="${C.line}"/>`);
    }
    parts.push(`<g>${isl.join("")}</g>`);
    // hull outline keyline
    parts.push(`<path d="${hull}" fill="none" stroke="${C.line}" stroke-width=".6" stroke-linejoin="round"/>`);
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${f(w)}" height="${f(h)}" viewBox="${vb.map(f).join(" ")}" style="display:block;overflow:visible"><defs>${defs}</defs>${parts.join("")}</svg>`;
  }

  const api = { svg, meta, L, KEEL_TO_DECK, ISLAND_ABOVE_DECK };
  root.CarrierHero = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
