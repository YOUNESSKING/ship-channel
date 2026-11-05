// ---------- ShipSink: side-profile ship scuttled / sinking down a water column to the seabed, with a depth gauge.
// HyperFrames-safe: one GSAP timeline, every frame is a pure function of time (render(t) from a proxy tween's onUpdate, like
// map-kit's camera / board.js); no DOM measurement, no randomness at render time (seeded), works with tl.seek(t) in any order.
//
//   const S = ShipSink(document.getElementById("stage"), { ship: "carrier", depthFt: 212, duration: 8.5, mode: "stern", settleFt: 10 });
//   window.__timelines = { main: S.tl };   S.cues -> [{t, kind}] sound cues (kit/ship/sfx names), S.landT = touchdown time, S.facts
//
// v2 (Oriskany test v3 critique): to-scale depths from the fact sheet (carrier: keel -> flight deck 75 ft, island top 63 ft above
// the deck, so on a 212 ft seabed + ~10 ft settling the deck ends at ~147 ft and the island top at 84 ft); the gauge reads
// "AT THE SURFACE 0 FT" while she floats, then tracks the FLIGHT DECK (clearly labelled) and lands on "212 FT SEABED"; the fact
// markers (island top / flight deck / seabed) appear on the ruler after she settles. Carrier = detailed CarrierHero drawing
// (carrier_hero.js; falls back to ShipKit). Labels >= 38 px (3.5 % of 1080), nothing in the bottom 10 % or the top-right corner.
//
// Config (all optional):
//   ship: "carrier" | "battleship" | "de" | "sub" | "liner" (kit/ship/ships.js)   depthFt: seabed depth (default 212)
//   duration: total seconds (default 8.5)    mode: "stern" (stern-first, lands upright) | "upright" | "bow"
//   pitch: max pitch in degrees (default 8)  units: "ft" | "m" (big number; the other one is shown small)
//   title / sub: optional caption card (top centre), shown 0.3 s - 3.6 s
//   charges: true = demolition flashes at the waterline before it goes (default true)   paint: "hulk" | "service" (hero carrier) / "livery" | "side"
//   settleFt: feet she settles INTO the seabed after landing (Oriskany: 10, FWC 2011)   settleLabel: caption for that step
//   readout: "deck" (track the flight deck; default for carriers) | "keel"     landReadout: "seabed" (default) | "ref"
//   markers: true = fact markers on the ruler after settling (default true)
//   restPitch: pitch (deg) at rest on the seabed (default 0 = upright, as Oriskany sits)
//   scale: px per foot   shipX: ship centre px   sinkStart / landAt: fractions of duration (0.14 / 0.72)
//   gaugeMax: depth at the bottom of the gauge   sonar: pings while sinking (true)
(function (root) {
  "use strict";
  const W = 1920, H = 1080, SAFE_B = H * 0.9;          // nothing below SAFE_B (YouTube player bar)
  const GOLD = "#c9b48a", CREAM = "#f7f3ea", FS = 40;  // FS: minimum label size (>= 38 px = 3.5 % of 1080)
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, k) => a + (b - a) * k;
  const smooth = (k) => { k = clamp(k, 0, 1); return k * k * (3 - 2 * k); };
  const rnd = (seed) => { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); };
  const niceStep = (d) => { const c = [5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000]; return c.find((s) => d / s <= 5) || 10000; };

  function ShipSink(stage, cfg = {}) {
    const gsap = root.gsap, K = root.ShipKit, CH = root.CarrierHero;
    const C = Object.assign({ ship: "carrier", depthFt: 212, duration: 8.5, mode: "stern", pitch: 8, units: "ft", charges: true,
      sinkStart: 0.14, landAt: 0.72, sonar: true, settleFt: 0, markers: true, landReadout: "seabed" }, cfg);
    const hero = C.ship === "carrier" && CH && C.hero !== false;
    if (!C.paint) C.paint = hero ? "hulk" : "livery";
    const D = C.duration, M = hero ? CH.meta(C.paint) : K.meta(C.ship), L = M.L, depth = C.depthFt;
    const deckY = hero ? M.deckY : M.sideY0 * 0.4;      // reference "deck" line (feet, side coords)
    const refMode = C.readout || (hero ? "deck" : "keel");
    const s = C.scale || (W * 0.62) / L;                                   // px per foot
    const SY = 520;                                                        // surface, world px
    const SB = SY + depth * s;                                             // seabed, world px
    const shipX = C.shipX || W * 0.615;
    const dir = C.mode === "bow" ? 1 : C.mode === "upright" ? 0 : -1;      // -1 = stern down (SVG rotation is clockwise)
    const pitchMax = dir * Math.min(C.pitch, Math.asin(clamp((depth - M.draught) / (L * 0.55), 0, 0.99)) * 180 / Math.PI);
    const t1 = D * C.sinkStart, tL = D * C.landAt, tCh = Math.max(0.15, t1 - 0.55);
    const H0 = depth - M.draught;                                          // waterline datum depth when upright on the seabed
    const settle = +C.settleFt || 0;

    // ---------------- motion model (feet, degrees)
    function rawState(t) {
      let h, th;
      if (t < t1) { h = 0.6 * Math.sin(t * 2.1); th = 0.4 * Math.sin(t * 1.3 + 0.5); }
      else {
        const p = clamp((t - t1) / (tL - t1), 0, 1.4);
        h = H0 * 1.06 * Math.pow(Math.min(p, 1.3), 1.55);                  // accelerating, still moving when it hits
        const up = smooth((t - t1) / ((tL - t1) * 0.32)), down = smooth((t - (tL - (tL - t1) * 0.18)) / (D * 0.12));
        th = pitchMax * up * (1 - down) + (+C.restPitch || 0) * down + (dir === 0 ? 0.8 * Math.sin(t * 0.9) * (1 - down) : 0);
      }
      return { h, th };
    }
    function lowest(h, th) {   // deepest keel point (feet below the surface)
      const r = th * Math.PI / 180; let m = -1e9;
      for (const [kx, ky] of M.keel) m = Math.max(m, h + (kx - L / 2) * Math.sin(r) + ky * Math.cos(r));
      return m;
    }
    let landT = D;
    const settleAt = (t) => (landT < D && settle ? settle * smooth((t - landT - 0.7) / 1.5) : 0);
    function state(t) {
      const r = rawState(t); let low = lowest(r.h, r.th);
      const floor = depth + settleAt(t);
      if (low > floor) { r.h -= low - floor; low = floor; r.ground = true; }
      r.low = low; return r;
    }
    for (let t = t1; t < D; t += 1 / 240) if (state(t).ground) { landT = t; break; }
    const ptDepth = (st, fx, fy) => { const r = st.th * Math.PI / 180; return st.h + (fx - L / 2) * Math.sin(r) + fy * Math.cos(r); };
    const refDepth = (st) => refMode === "deck" ? ptDepth(st, L / 2, deckY) : st.low;
    let tUnder = D; for (let t = 0; t < D; t += 1 / 240) if (ptDepth(state(t), L / 2, deckY) > 0.5) { tUnder = t; break; }
    const fin = state(D);
    const facts = { seabed: depth, keel: +fin.low.toFixed(1), flightDeck: +ptDepth(fin, L / 2, deckY).toFixed(1),
      islandTop: hero ? +ptDepth(fin, (M.islandX[0] + 4 + M.islandX[0] + 40) / 2, M.islandTopY).toFixed(1) : null, landT, tUnder };

    // ---------------- DOM
    stage.innerHTML = "";
    stage.style.cssText = `position:absolute;left:0;top:0;width:${W}px;height:${H}px;overflow:hidden;background:#0b141c;font-family:Oswald,sans-serif`;
    const el = (tag, css, html, parent = stage) => { const e = document.createElement(tag); if (css) e.style.cssText = css; if (html != null) e.innerHTML = html; parent.appendChild(e); return e; };
    const worldH = SB + 600;
    const world = el("div", `position:absolute;left:0;top:0;width:${W}px;height:${worldH}px;transform-origin:0 0`);
    // sky (dusk haze, map-kit dark palette)
    el("div", `position:absolute;left:0;top:${SY - 900}px;width:${W}px;height:900px;background:linear-gradient(180deg,#0e171d 0%,#1d2a32 55%,#3b4a52 92%,#55636a 100%)`, null, world);
    // water column: colour by depth (bathy palette: teal near the surface -> navy -> black in the deep)
    const wcol = (d) => { const st = [[0, [44, 104, 112]], [60, [26, 72, 86]], [200, [13, 42, 58]], [800, [8, 24, 40]], [3000, [4, 10, 18]]];
      for (let k = 1; k < st.length; k++) if (d <= st[k][0]) { const a = st[k - 1], b = st[k], q = (d - a[0]) / (b[0] - a[0]); return a[1].map((v, i) => Math.round(lerp(v, b[1][i], q))); }
      return st[st.length - 1][1]; };
    const grad = [0, 0.15, 0.35, 0.6, 1].map((q) => `rgb(${wcol(q * depth).join(",")}) ${(q * 100).toFixed(0)}%`).join(",");
    el("div", `position:absolute;left:0;top:${SY}px;width:${W}px;height:${SB - SY + 600}px;background:linear-gradient(180deg,${grad})`, null, world);
    // light shafts from the surface (screen-blended, soft, slowly swaying)
    const R = rnd(7);
    const rays = [];
    for (let k = 0; k < 11; k++) {
      const x = 40 + k * 175 + R() * 90, w = 50 + R() * 150, len = Math.min(SB - SY, 900) * (0.7 + R() * 0.35);
      rays.push(el("div", `position:absolute;left:${x}px;top:${SY}px;width:${w}px;height:${len}px;transform-origin:50% 0;transform:skewX(${-16 + R() * 10}deg);mix-blend-mode:screen;
        background:linear-gradient(180deg,rgba(170,225,215,${0.12 + R() * 0.08}) 0%,rgba(170,225,215,0.04) 55%,rgba(170,225,215,0) 100%);filter:blur(10px)`, null, world));
    }
    // caustic shimmer under the surface (moving soft light cells, fades with depth)
    const caust = el("div", `position:absolute;left:-200px;top:${SY + 4}px;width:${W + 400}px;height:${Math.min(160 * s, SB - SY)}px;mix-blend-mode:screen;opacity:.55;
      background:radial-gradient(ellipse 60px 14px at 20% 12%,rgba(200,240,230,.22),transparent 70%),radial-gradient(ellipse 90px 18px at 55% 30%,rgba(200,240,230,.18),transparent 70%),radial-gradient(ellipse 70px 12px at 80% 18%,rgba(200,240,230,.2),transparent 70%);
      background-size:340px 120px;-webkit-mask-image:linear-gradient(180deg,#000 0%,rgba(0,0,0,0) 100%);mask-image:linear-gradient(180deg,#000 0%,rgba(0,0,0,0) 100%)`, null, world);
    // marine snow (two depths: small slow far specks + brighter near ones)
    const snow = [];
    for (let k = 0; k < 140; k++) { const near = k % 4 === 0, sz = near ? 4 : 2.2;
      snow.push({ e: el("div", `position:absolute;left:0;top:0;width:${sz}px;height:${sz}px;border-radius:50%;background:rgba(220,235,230,${(near ? 0.35 : 0.15) + R() * 0.3});${near ? "filter:blur(.6px)" : ""}`, null, world),
        x: R() * W, y: SY + 20 + R() * (SB - SY), v: (near ? 10 : 5) + R() * 9, ph: R() * 6 }); }
    // the ship
    const svgW = s * (L + 2 * M.pad), ax = (L / 2 + M.pad) * s, ay = (0 - (M.sideY0 - M.pad)) * s;
    const shipSvg = hero ? CH.svg({ w: svgW, paint: C.paint, id: "sink", mast: C.mast }) : K.svg(C.ship, "side", { w: svgW, paint: C.paint, col: C.col, glow: false, keyline: 1.6, id: "sink" });
    const shipEl = el("div", `position:absolute;left:${shipX - ax}px;top:${SY - ay}px;transform-origin:${ax}px ${ay}px;will-change:transform;filter:drop-shadow(0 6px 10px rgba(0,0,0,.35))`, shipSvg, world);
    // seabed (cross-section), drawn IN FRONT of the hull so the settled keel sinks into the sediment
    let bed = `M0 ${SB + 6}`; for (let x = 0; x <= W; x += 60) bed += ` L${x} ${(SB + 6 + 7 * Math.sin(x / 170) + 4 * Math.sin(x / 53)).toFixed(1)}`;
    const bedTop = bed; bed += ` L${W} ${SB + 600} L0 ${SB + 600} Z`;
    let layers = ""; for (let k = 1; k < 7; k++) { let d = `M0 ${SB + 6 + k * 44}`; for (let x = 0; x <= W; x += 80) d += ` L${x} ${(SB + 6 + k * 44 + 6 * Math.sin(x / (140 + k * 30) + k)).toFixed(1)}`; layers += `<path d="${d}" fill="none" stroke="rgba(30,24,16,0.45)" stroke-width="2" stroke-dasharray="${10 + k * 3} ${6 + k}"/>`; }
    let rocks = ""; for (let k = 0; k < 14; k++) { const x = R() * W, r = 4 + R() * 9; rocks += `<ellipse cx="${x.toFixed(0)}" cy="${(SB + 8 + 7 * Math.sin(x / 170)).toFixed(0)}" rx="${(r * 1.6).toFixed(1)}" ry="${r.toFixed(1)}" fill="#3f382c"/>`; }
    el("div", `position:absolute;left:0;top:0;width:${W}px;height:${worldH}px`, `<svg width="${W}" height="${worldH}" style="position:absolute;left:0;top:0">
      <defs><linearGradient id="sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8c7a58"/><stop offset="0.12" stop-color="#6b5c43"/><stop offset="1" stop-color="#2c261d"/></linearGradient></defs>
      <path d="${bed}" fill="url(#sand)"/>${layers}${rocks}<path d="${bedTop}" fill="none" stroke="#b9a57c" stroke-width="2.5" opacity="0.8"/></svg>`, world);
    // charges (flashes) + bubbles + sediment
    const flashes = [];
    if (C.charges) for (let k = 0; k < 7; k++) {
      const fx = (0.08 + k * 0.13) * L, at = tCh + k * 0.07 + R() * 0.05;
      flashes.push({ fx, at, e: el("div", `position:absolute;left:0;top:0;width:90px;height:90px;margin:-45px 0 0 -45px;border-radius:50%;opacity:0;
        background:radial-gradient(circle,#fffbe6 0%,#ffd34d 28%,rgba(255,120,20,.7) 52%,rgba(255,80,0,0) 72%);mix-blend-mode:screen`, null, world),
        spray: el("div", `position:absolute;left:0;top:0;width:26px;height:120px;margin-left:-13px;opacity:0;transform-origin:50% 100%;
        background:linear-gradient(0deg,rgba(235,245,245,.85),rgba(235,245,245,0));border-radius:50% 50% 20% 20%;filter:blur(1.5px)`, null, world) });
    }
    const bubbles = [];
    for (let k = 0; k < 160; k++) bubbles.push({ e: el("div", `position:absolute;left:0;top:0;border-radius:50%;border:1.5px solid rgba(220,240,240,.75);background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.5),rgba(220,240,240,.08) 60%);opacity:0`, null, world),
      born: t1 + R() * (Math.min(landT + 1.6, D) - t1), fx: R(), r: 2.5 + R() * 9, sp: 90 + R() * 120, wob: R() * 6 });
    const silt = [];
    for (let k = 0; k < 18; k++) silt.push({ e: el("div", `position:absolute;left:0;top:0;border-radius:50%;background:radial-gradient(ellipse,rgba(150,132,98,.55) 0%,rgba(150,132,98,0) 70%);opacity:0;filter:blur(4px)`, null, world),
      fx: k < 9 ? R() * 0.3 : 0.3 + R() * 0.7, vx: (R() - 0.5) * 160, r: 60 + R() * 90, d: R() * 0.3 });
    // water tint IN FRONT of the ship (so it darkens and turns teal as it goes down) + surface line
    const tintTop = `rgba(${wcol(0).join(",")},0.12)`, tintBot = `rgba(${wcol(depth).join(",")},${clamp(0.22 + depth / 900, 0.3, 0.7).toFixed(2)})`;
    el("div", `position:absolute;left:0;top:${SY}px;width:${W}px;height:${SB - SY + 600}px;background:linear-gradient(180deg,${tintTop} 0%,${tintBot} ${((SB - SY) / (SB - SY + 600) * 100).toFixed(0)}%,${tintBot} 100%)`, null, world);
    const wave = (amp, per, y) => { let d = `M-200 ${y}`; for (let x = -200; x < W + 400; x += per) d += ` q${per / 4} ${-amp} ${per / 2} 0 t${per / 2} 0`; return d; };
    const surf = el("div", `position:absolute;left:0;top:${SY - 20}px;width:${W + 400}px;height:40px`, `<svg width="${W + 400}" height="40" style="overflow:visible">
      <path d="${wave(5, 140, 20)}" fill="none" stroke="rgba(235,245,240,.85)" stroke-width="3"/><path d="${wave(3, 90, 24)}" fill="none" stroke="rgba(235,245,240,.35)" stroke-width="2"/></svg>`, world);
    // vignette
    el("div", `position:absolute;inset:0;background:radial-gradient(ellipse at 55% 50%,rgba(0,0,0,0) 50%,rgba(0,0,0,.6) 100%);pointer-events:none`);

    // ---------------- gauge in the anim_gauge "meter" look: track, ticks, fill + dot, big count, land flash + ring
    const gMax = C.gaugeMax || Math.ceil(depth * 1.12 / niceStep(depth)) * niceStep(depth), step = niceStep(gMax);
    const camStart0 = SY - 430, ruler = SB - camStart0 <= SAFE_B - 20;
    const GX = 150, GY0 = ruler ? SY : 330, GY1 = ruler ? SY + gMax * s : SAFE_B - 40, gy = (d) => GY0 + (GY1 - GY0) * clamp(d / gMax, 0, 1);
    const U = C.units === "m" ? { k: 0.3048, u: "M", k2: 1, u2: "FT" } : { k: 1, u: "FT", k2: 0.3048, u2: "M" };
    let gs = `<rect x="${GX - 14}" y="${GY0 - 12}" width="28" height="${GY1 - GY0 + 24}" rx="14" fill="rgba(11,20,28,.55)" stroke="rgba(247,243,234,.4)" stroke-width="2"/>`;
    for (let d = 0; d <= gMax + 1e-6; d += step) gs += `<line x1="${GX - 34}" y1="${gy(d)}" x2="${GX - 18}" y2="${gy(d)}" stroke="rgba(247,243,234,.6)" stroke-width="2"/>
      <text x="${GX - 40}" y="${gy(d) + 13}" text-anchor="end" font-size="${FS - 2}" fill="rgba(247,243,234,.8)">${Math.round(d * U.k)}</text>`;
    const sbY = gy(depth);
    // fact markers: seabed shown from the start; the others after she settles (the to-scale proof)
    const mk = [{ d: depth, label: "SEABED", always: true }];
    if (C.markers && hero) mk.push({ d: facts.flightDeck, label: "FLIGHT DECK", approx: true }, { d: facts.islandTop, label: "ISLAND TOP", x2: shipX + (M.islandX[0] + 4 - L / 2) * s });
    mk.forEach((m, i) => { const y = gy(m.d);
      gs += `<g id="sk-m${i}" opacity="${m.always ? 1 : 0}"><line x1="${GX + 18}" y1="${y}" x2="${GX + 44}" y2="${y}" stroke="${GOLD}" stroke-width="3"/>
        <line x1="${GX + 44}" y1="${y}" x2="${m.always ? W : m.x2 || shipX - L * s / 2 + 20}" y2="${y}" stroke="${GOLD}" stroke-width="2" stroke-dasharray="7 7" opacity="${m.always ? 0.45 : 0.8}"/>
        <rect x="${GX + 50}" y="${y - 25}" width="${(m.label.length + 6) * 21 + 20}" height="50" fill="rgba(11,16,20,.72)"/>
        <text x="${GX + 60}" y="${y + 14}" font-size="${FS}" fill="${CREAM}" font-weight="500" letter-spacing="2">${m.label} <tspan fill="${GOLD}" font-weight="700">${m.approx ? "~" : ""}${Math.round(m.d * U.k)} ${U.u}</tspan></text></g>`; });
    gs += `<line id="sk-fill" x1="${GX}" y1="${GY0}" x2="${GX}" y2="${GY0}" stroke="${GOLD}" stroke-width="16" stroke-linecap="round"/>
      <circle id="sk-ring" cx="${GX}" cy="${sbY}" r="12" fill="none" stroke="${GOLD}" stroke-width="4" opacity="0"/>
      <circle id="sk-dot" cx="${GX}" cy="${GY0}" r="11" fill="${GOLD}" stroke="#14110b" stroke-width="2"/>`;
    const gH = ruler ? worldH : H;
    const gauge = el("div", `position:absolute;left:0;top:0;width:${W}px;height:${gH}px`, `<svg width="${W}" height="${gH}" style="position:absolute;left:0;top:0;font-family:Oswald;font-weight:500;filter:drop-shadow(0 2px 6px rgba(0,0,0,.6))">${gs}</svg>`, ruler ? world : stage);
    const mEls = mk.map((m, i) => gauge.querySelector(`#sk-m${i}`));
    // readout block (top left, on a scrim): kicker = WHAT is measured, big number, small other unit
    el("div", `position:absolute;left:0;top:0;width:760px;height:330px;background:radial-gradient(ellipse at 0% 0%,rgba(5,10,14,.75) 0%,rgba(5,10,14,.45) 45%,rgba(5,10,14,0) 75%);pointer-events:none`);
    const kick = el("div", `position:absolute;left:96px;top:64px;font-size:${FS}px;letter-spacing:.14em;color:${GOLD};font-weight:500;text-shadow:0 2px 10px rgba(0,0,0,.8);white-space:nowrap`);
    const big = el("div", `position:absolute;left:92px;top:116px;font-size:110px;font-weight:700;color:${CREAM};line-height:1;letter-spacing:.02em;text-shadow:0 3px 18px rgba(0,0,0,.75);transform-origin:0 50%;white-space:nowrap`);
    const small = el("div", `position:absolute;left:96px;top:238px;font-size:${FS}px;font-weight:500;color:rgba(247,243,234,.82);letter-spacing:.08em;white-space:nowrap;text-shadow:0 2px 10px rgba(0,0,0,.8)`);
    const flashScr = el("div", `position:absolute;inset:0;background:#fff3d6;opacity:0;mix-blend-mode:screen;pointer-events:none`);
    // caption card (map-kit placeCard look), top centre: never top-right (YouTube overlays) or bottom 10 %
    let card = null;
    if (C.title) card = el("div", `position:absolute;left:50%;top:64px;transform:translateX(-10%);padding:14px 30px 16px;background:rgba(18,16,12,.92);border-top:5px solid ${GOLD};color:${CREAM};font-weight:700;box-shadow:0 14px 30px rgba(0,0,0,.6);opacity:0;white-space:nowrap`,
      `<div style="font-size:${FS}px;letter-spacing:.12em;color:${GOLD};font-weight:500">${C.sub || ""}</div><div style="font-size:66px;letter-spacing:.04em;line-height:1.1">${C.title}</div>`);
    let settleCap = null;
    if (settle && C.settleLabel) settleCap = el("div", `position:absolute;left:${shipX - 380}px;top:${SAFE_B - 80}px;font-size:${FS}px;font-weight:500;color:${CREAM};letter-spacing:.06em;background:rgba(11,16,20,.72);padding:4px 16px;border-left:5px solid ${GOLD};opacity:0;white-space:nowrap`, C.settleLabel);
    const gFill = gauge.querySelector("#sk-fill"), gDot = gauge.querySelector("#sk-dot"), gRing = gauge.querySelector("#sk-ring");

    // ---------------- render(t): everything is a function of t
    const camStart = camStart0, camEnd = ruler ? camStart : Math.max(camStart, SB - 860);
    const fmt = (v) => Math.round(v).toLocaleString("en-US");
    function render(t) {
      const st = state(t);
      const shake = t > landT && t < landT + 0.5 ? Math.sin((t - landT) * 70) * 7 * (1 - (t - landT) / 0.5) : 0;
      const cam = (ruler ? camStart : clamp(SY + st.low * s - 700, camStart, camEnd)) + shake;
      const push = 1 + 0.035 * (t / D);
      world.style.transform = `translate(${(W / 2) * (1 - push)}px, ${-cam * push - (H / 2) * (push - 1)}px) scale(${push})`;
      shipEl.style.transform = `translate(0px, ${(st.h * s).toFixed(2)}px) rotate(${st.th.toFixed(3)}deg)`;
      surf.style.transform = `translateX(${(-((t * 38) % 140)).toFixed(1)}px)`;
      caust.style.backgroundPosition = `${(t * 22).toFixed(1)}px ${(6 * Math.sin(t * 1.3)).toFixed(1)}px, ${(-t * 15).toFixed(1)}px ${(5 * Math.cos(t)).toFixed(1)}px, ${(t * 9).toFixed(1)}px 0px`;
      rays.forEach((r, i) => { r.style.opacity = (0.7 + 0.3 * Math.sin(t * 0.9 + i * 1.7)).toFixed(3); r.style.marginLeft = (14 * Math.sin(t * 0.5 + i)).toFixed(1) + "px"; });
      snow.forEach((p) => { const y = SY + 20 + ((p.y - SY + p.v * t) % (SB - SY - 20)); p.e.style.transform = `translate(${(p.x + 8 * Math.sin(t * 0.7 + p.ph)).toFixed(1)}px,${y.toFixed(1)}px)`; });
      const r = st.th * Math.PI / 180, hullPt = (fx, fy) => { const x = fx - L / 2; return [shipX + (x * Math.cos(r) - fy * Math.sin(r)) * s, SY + st.h * s + (x * Math.sin(r) + fy * Math.cos(r)) * s]; };
      flashes.forEach((f) => { const a = t - f.at; const [x, y] = hullPt(f.fx, M.draught * 0.4);
        const o = a < 0 ? 0 : a < 0.08 ? a / 0.08 : Math.max(0, 1 - (a - 0.08) / 0.35);
        f.e.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${(0.5 + Math.min(a, 0.4) * 2).toFixed(2)})`; f.e.style.opacity = o.toFixed(3);
        const so = a < 0 ? 0 : Math.max(0, 1 - a / 1.1), sh = a < 0 ? 0 : Math.min(1, a / 0.25);
        f.spray.style.transform = `translate(${x.toFixed(1)}px,${(SY - 120).toFixed(1)}px) scaleY(${(0.2 + sh).toFixed(2)})`; f.spray.style.opacity = so.toFixed(3); });
      bubbles.forEach((b) => { const a = t - b.born; if (a < 0 || a > 2.6) { b.e.style.opacity = 0; return; }
        const st0 = state(b.born), r0 = st0.th * Math.PI / 180, x0 = b.fx * L - L / 2, fy = deckY + 4;
        const bx = shipX + (x0 * Math.cos(r0) - fy * Math.sin(r0)) * s, by = SY + st0.h * s + (x0 * Math.sin(r0) + fy * Math.cos(r0)) * s;
        const y = by - b.sp * a - 30 * a * a; if (y < SY + 4) { b.e.style.opacity = 0; return; }
        const rr = b.r * (1 + a * 0.25);
        b.e.style.width = b.e.style.height = (2 * rr).toFixed(1) + "px";
        b.e.style.transform = `translate(${(bx + 10 * Math.sin(a * 5 + b.wob) - rr).toFixed(1)}px,${(y - rr).toFixed(1)}px)`;
        b.e.style.opacity = (Math.min(1, a / 0.15) * Math.max(0, 1 - a / 2.6)).toFixed(3); });
      silt.forEach((p) => { const a = t - landT - p.d * 0.4; if (a < 0) { p.e.style.opacity = 0; return; }
        const x = shipX + (p.fx - 0.5) * L * s + p.vx * Math.min(a, 2.5) * 0.6, rr = p.r * (0.4 + Math.min(a, 3) * 0.5);
        p.e.style.width = (rr * 2.6).toFixed(0) + "px"; p.e.style.height = (rr * 1.2).toFixed(0) + "px";
        p.e.style.transform = `translate(${(x - rr * 1.3).toFixed(1)}px,${(SB - rr * 0.9 - a * 8).toFixed(1)}px)`;
        p.e.style.opacity = (Math.min(1, a / 0.3) * Math.max(0, 1 - (a - 0.3) / 3.5) * 0.9).toFixed(3); });
      // gauge: 0 while afloat -> reference (flight deck) while sinking -> seabed on landing
      const ref = Math.max(0, refDepth(st)), la = t - landT, landK = la >= 0 ? 1 : 0;   // v2 (critic B N7): the count lands ON the touchdown frame
      let shown, kText, sText;
      if (t < tUnder && refMode === "deck") { shown = 0; kText = "AT THE SURFACE"; sText = "FLIGHT DECK ABOVE WATER"; }
      else if (la < 0 || C.landReadout !== "seabed") { shown = ref; kText = refMode === "deck" ? "FLIGHT DECK DEPTH" : "KEEL DEPTH"; sText = `${fmt(ref * U.k2)} ${U.u2}`; }
      else { shown = lerp(ref, depth, landK); kText = "ON THE SEABED"; sText = `${fmt(depth * U.k2)} ${U.u2} DOWN`; }
      const yv = gy(shown);
      gFill.setAttribute("y2", yv.toFixed(1)); gDot.setAttribute("cy", yv.toFixed(1));
      const pre = t < t1 ? 1 + 0.25 * Math.max(0, Math.sin(t * 7)) : 1; gDot.setAttribute("r", (11 * pre).toFixed(2));
      kick.textContent = kText;
      big.innerHTML = `${fmt(shown * U.k)}<span style="font-size:52px;color:${GOLD};margin-left:12px;font-weight:500">${U.u}</span>`;
      small.textContent = sText;
      const pop = la >= 0 && la < 0.4 ? 1.18 - 0.18 * smooth(la / 0.4) : 1;
      big.style.transform = `scale(${pop.toFixed(3)})`;
      gRing.setAttribute("opacity", la >= 0 && la < 1.0 ? (1 - la).toFixed(3) : 0); gRing.setAttribute("r", la >= 0 ? (12 + 70 * Math.min(la, 1)).toFixed(1) : 12);
      flashScr.style.opacity = la >= 0 && la < 0.25 ? (0.22 * (1 - la / 0.25)).toFixed(3) : 0;
      const mA = clamp((t - landT - (settle ? 1.6 : 0.6)) / 0.4, 0, 1);
      mEls.forEach((e, i) => { if (!mk[i].always) e.setAttribute("opacity", clamp(mA * 1.6 - i * 0.3, 0, 1).toFixed(3)); });
      if (settleCap) settleCap.style.opacity = clamp(Math.min((t - landT - 0.7) / 0.3, 1), 0, 1).toFixed(3);
      if (card) card.style.opacity = clamp(Math.min((t - 0.3) / 0.4, (3.6 - t) / 0.4), 0, 1).toFixed(3);
    }

    // ---------------- timeline + sound cues
    const tl = gsap.timeline({ paused: true });
    const proxy = { t: 0 };
    tl.to(proxy, { t: D, duration: D, ease: "none", onUpdate: () => render(proxy.t) }, 0);
    tl.eventCallback("onUpdate", () => render(proxy.t));
    render(0);
    const cues = [{ t: 0, kind: "swell_bed_1", bed: true, until: t1 + 1.0 }, { t: Math.max(0, t1 - 0.2), kind: "underwater_bed_2", bed: true, until: D }];
    if (C.charges) cues.push({ t: tCh, kind: "charges_seq_3" });
    cues.push({ t: t1 + 0.2, kind: "hull_groan_1" }, { t: t1 + 0.9, kind: "sink_whoomp_1" }, { t: t1 + (tL - t1) * 0.5, kind: "metal_creak_2" });
    if (C.sonar) for (let tt = t1 + 0.8; tt < landT - 0.6; tt += 1.6) cues.push({ t: tt, kind: "sonar_ping_3" });
    cues.push({ t: landT, kind: "number_land_1" });
    if (settle) cues.push({ t: landT + 0.7, kind: "hull_groan_2" });
    return { tl, cues: cues.sort((a, b) => a.t - b.t), landT, tUnder, facts, duration: D, render, config: C };
  }
  root.ShipSink = ShipSink;
})(typeof window !== "undefined" ? window : globalThis);
