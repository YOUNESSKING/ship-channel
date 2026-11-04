// ---------- AnimScenes: every kit / hero animation scene of the Oriskany full video, one builder per family.
// HyperFrames-safe like kit/ship/sinking.js: one paused GSAP timeline, one proxy tween calls render(t); every frame is a pure
// function of t (seeded randomness, no DOM measurement at render time), so the page seeks in any order.
//
//   AnimScenes.build(stage, "c06_lines_b", SCENES["c06_lines_b"]) -> { tl, duration, beats:[{t,kind,note,main}], cues, missing }
//
// Words: cfg.words = [{w, t, e}] scene-relative (scene start = shot start). S.w("below florida's") -> start of that phrase.
// Every hit / landing is placed ON its spoken word and exported as a beat (build/anim_beats.json) for sound re-timing.
// Look: test v4 hero (ShipSink / CarrierHero), Oswald, cream #f7f3ea + gold #c9b48a, labels >= 40 px (38 px = 3.5 % of 1080),
// nothing in the bottom 10 % (YouTube bar) or the top-right corner (right 20 %, top 12 %), kicker top left.
// Fact rules (FACTCHECK_B): PCB chart shows NO invented ppb values: only the two screening values (Florida 50 ppb, EPA 20 ppb),
// "above both" for the first two years, below Florida at ~2.9 years, below both at ~3.5-3.9 years; the snapper ~7x is attributed
// to environmental groups (2012 petition, from FWC data). Depths (FACTCHECK_C): seabed 212 ft, settled ~10 ft, deck ~145-150 ft,
// island top 84 ft.
(function (root) {
  "use strict";
  const W = 1920, H = 1080, SAFE_B = 972;
  const GOLD = "#c9b48a", GOLD2 = "#e6d3a3", CREAM = "#f7f3ea", INK = "#0b141c", AMBER = "#f2a23a", RUST = "#b8432f", TEAL = "#8fd0c6";
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), lerp = (a, b, k) => a + (b - a) * k;
  const sm = (k) => { k = clamp(k, 0, 1); return k * k * (3 - 2 * k); };
  const ramp = (t, a, d) => clamp((t - a) / Math.max(d, 1e-6), 0, 1);
  const oCub = (k) => 1 - Math.pow(1 - clamp(k, 0, 1), 3);
  const oBack = (k) => { k = clamp(k, 0, 1); const c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
  const rnd = (seed) => { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); };
  const norm = (s) => String(s).toLowerCase().replace(/[’']/g, "'").replace(/[^a-z0-9']/g, "");
  const f1 = (v) => (Math.round(v * 10) / 10).toString();

  // ======================================================== core
  function Base(stage, cfg) {
    stage.innerHTML = "";
    stage.style.cssText = `position:absolute;left:0;top:0;width:${W}px;height:${H}px;overflow:hidden;background:${INK};font-family:Oswald,sans-serif`;
    const S = { stage, cfg, D: cfg.dur, beats: [], fns: [], missing: [], cues: [] };
    S.el = (tag, css, html, parent = stage) => { const e = document.createElement(tag); if (css) e.style.cssText = css; if (html != null) e.innerHTML = html; parent.appendChild(e); return e; };
    S.on = (fn) => { S.fns.push(fn); return fn; };
    S.w = (phrase, dflt, nth = 1) => {
      const toks = phrase.split(/\s+/).map(norm).filter(Boolean), ws = cfg.words; let c = 0;
      for (let i = 0; i <= ws.length - toks.length; i++) if (ws[i].t > -0.2 && toks.every((k, j) => norm(ws[i + j].w) === k)) { if (++c === nth) return ws[i].t; }
      S.missing.push(phrase); return dflt;
    };
    S.beat = (t, kind, note, main) => { S.beats.push({ t: +(+t).toFixed(3), kind, note, main: !!main }); return t; };
    // a pop-in (scale overshoot + fade), optional fade out
    S.pop = (e, t0, o = {}) => S.on((t) => {
      const k = ramp(t, t0, o.d || 0.38); let op = sm(k * 1.8);
      if (o.out != null) op *= 1 - ramp(t, o.out, o.outD || 0.3);
      e.style.opacity = op.toFixed(3);
      e.style.transform = `${o.base || ""} scale(${lerp(o.from == null ? 0.72 : o.from, 1, oBack(k)).toFixed(4)})`;
    });
    S.rise = (e, t0, o = {}) => S.on((t) => {
      const k = oCub(ramp(t, t0, o.d || 0.45)); let op = k;
      if (o.out != null) op *= 1 - ramp(t, o.out, o.outD || 0.3);
      e.style.opacity = op.toFixed(3); e.style.transform = `${o.base || ""} translateY(${((1 - k) * (o.dy == null ? 18 : o.dy)).toFixed(1)}px)`;
    });
    S.kicker = (text, t0 = 0.1, sub, subT) => {
      const k = S.el("div", `position:absolute;left:96px;top:60px;font-size:42px;letter-spacing:.14em;color:${GOLD};font-weight:500;text-shadow:0 2px 12px rgba(0,0,0,.85);white-space:nowrap;opacity:0`, text);
      S.rise(k, t0, { dy: 12 });
      if (sub) { const s = S.el("div", `position:absolute;left:98px;top:114px;font-size:40px;letter-spacing:.06em;color:rgba(247,243,234,.82);font-weight:500;text-shadow:0 2px 10px rgba(0,0,0,.85);white-space:nowrap;opacity:0`, sub); S.rise(s, subT == null ? t0 + 0.15 : subT, { dy: 10 }); }
      return k;
    };
    // gold-edged plate (map-kit placeCard look)
    S.tag = (text, x, y, t0, o = {}) => {
      const e = S.el("div", `position:absolute;left:${x}px;top:${y}px;padding:6px 22px 9px;background:rgba(14,13,10,${o.alpha || 0.88});border-left:6px solid ${o.col || GOLD};
        color:${o.ink || CREAM};font-size:${o.fs || 44}px;font-weight:700;letter-spacing:.06em;white-space:nowrap;box-shadow:0 10px 26px rgba(0,0,0,.55);opacity:0;
        transform-origin:${o.origin || "0% 50%"};z-index:${o.z || 20}`, text, o.parent);
      S.pop(e, t0, o); return e;
    };
    S.cue = (t, kind, note) => S.cues.push({ t: +t.toFixed(3), kind, note });
    return S;
  }

  // shared seeded grain texture (one canvas, tiled, shifted every frame)
  let GRAIN = null;
  function grainURL() {
    if (GRAIN) return GRAIN;
    const c = document.createElement("canvas"); c.width = c.height = 256; const g = c.getContext("2d"), im = g.createImageData(256, 256), r = rnd(99);
    for (let i = 0; i < im.data.length; i += 4) { const v = Math.floor(r() * 255); im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 40; }
    g.putImageData(im, 0, 0); GRAIN = c.toDataURL(); return GRAIN;
  }

  // dark "board" background: deep radial, faint blueprint grid, a slow light beam, drifting dust (the anim_gauge look, ship palette)
  function board(S, o = {}) {
    const hue = o.tint || "27,42,53";
    S.el("div", `position:absolute;inset:0;background:radial-gradient(ellipse at ${o.cx || "46%"} ${o.cy || "42%"},rgb(${hue}) 0%,#0f1a22 46%,#060a0d 100%)`);
    if (o.grid !== false) S.el("div", `position:absolute;inset:-60px;opacity:.55;
      background-image:linear-gradient(rgba(150,200,210,.055) 2px,transparent 2px),linear-gradient(90deg,rgba(150,200,210,.055) 2px,transparent 2px),
      linear-gradient(rgba(150,200,210,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(150,200,210,.03) 1px,transparent 1px);
      background-size:192px 192px,192px 192px,48px 48px,48px 48px;
      -webkit-mask-image:radial-gradient(ellipse at 50% 45%,#000 30%,transparent 78%);mask-image:radial-gradient(ellipse at 50% 45%,#000 30%,transparent 78%)`);
    const beam = S.el("div", `position:absolute;left:-300px;top:-500px;width:1400px;height:1900px;transform-origin:50% 0;mix-blend-mode:screen;filter:blur(30px);
      background:linear-gradient(90deg,rgba(255,236,190,0) 0%,rgba(255,236,190,.07) 40%,rgba(255,236,190,.11) 50%,rgba(255,236,190,.07) 60%,rgba(255,236,190,0) 100%)`);
    const dust = [], R = rnd(o.seed || 5);
    for (let k = 0; k < (o.dust || 60); k++) { const near = k % 5 === 0, sz = near ? 4 : 2;
      dust.push({ e: S.el("div", `position:absolute;left:0;top:0;width:${sz}px;height:${sz}px;border-radius:50%;background:rgba(255,240,210,${(near ? .32 : .16) + R() * .2});${near ? "filter:blur(1px)" : ""}`),
        x: R() * W, y: R() * H, vx: (R() - .5) * 14, vy: -4 - R() * 10, ph: R() * 6 }); }
    S.on((t) => {
      beam.style.transform = `rotate(${(-28 + 3 * Math.sin(t * 0.35)).toFixed(2)}deg)`;
      dust.forEach((p) => { const x = ((p.x + p.vx * t + 10 * Math.sin(t * .6 + p.ph)) % W + W) % W, y = ((p.y + p.vy * t) % H + H) % H;
        p.e.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px)`; });
    });
  }
  function finish(S, o = {}) {
    S.el("div", `position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 50% 48%,rgba(0,0,0,0) ${o.vig || 52}%,rgba(0,0,0,.62) 100%);z-index:40`);
    const gr = S.el("div", `position:absolute;left:-256px;top:-256px;width:${W + 512}px;height:${H + 512}px;pointer-events:none;opacity:.5;mix-blend-mode:overlay;background-image:url(${grainURL()});z-index:41`);
    S.on((t) => { const f = Math.floor(t * 30), r = rnd(f * 7919 + 1); gr.style.transform = `translate(${Math.floor(r() * 256)}px,${Math.floor(r() * 256)}px)`; });
    const gsap = root.gsap, tl = gsap.timeline({ paused: true }), px = { t: 0 };
    const render = (t) => S.fns.forEach((fn) => fn(t));
    tl.to(px, { t: S.D, duration: S.D, ease: "none", onUpdate: () => render(px.t) }, 0);
    render(0);
    return { tl, duration: S.D, beats: S.beats.sort((a, b) => a.t - b.t), cues: S.cues, missing: S.missing };
  }

  // ---------------- small vector icons
  const FISH = (col = "#b9c7cc", w = 60, o = {}) => `<svg width="${w}" height="${w * 0.5}" viewBox="-34 -17 72 34" style="overflow:visible;display:block">
    <path d="M-30 0 C-18 -15 10 -16 26 -4 L34 -12 L33 0 L34 12 L26 4 C10 16 -18 15 -30 0 Z" fill="${col}" stroke="${o.rim || "rgba(10,14,18,.7)"}" stroke-width="1.6"/>
    <path d="M-8 -11 L2 -20 L10 -12 Z" fill="${col}" opacity=".85"/><path d="M-4 9 L4 16 L8 9 Z" fill="${col}" opacity=".8"/>
    <circle cx="-20" cy="-3" r="2.6" fill="#0b0f12"/><path d="M-12 -6 Q-9 0 -12 6" fill="none" stroke="rgba(0,0,0,.35)" stroke-width="1.4"/></svg>`;
  const SNAPPER = (w = 150, col = "#d4655a") => FISH(col, w, { rim: "rgba(40,10,8,.8)" });

  // ======================================================== c02 sisters: four Essex-class silhouettes, MUSEUM tags
  function sisters(S) {
    board(S, { seed: 3 });
    S.kicker("HER ESSEX-CLASS SISTERS", 0.05);
    const K = root.ShipKit, tMus = S.w("museums", 1.66), cells = [[150, 300], [1010, 300], [150, 630], [1010, 630]];
    const tIn = [0.1, S.w("of her", 0.3), S.w("sisters", 0.52), S.w("were", 0.9)];
    cells.forEach(([x, y], i) => {
      const g = S.el("div", `position:absolute;left:${x}px;top:${y}px;width:760px;height:240px;opacity:0`);
      // CarrierHero in service paint (the detailed hero drawing), waterline at y = 190 in the cell
      const CH = root.CarrierHero, M = CH.meta("service"), sc = 740 / (M.L + 2 * M.pad), wl = 190, top = wl + (M.sideY0 - M.pad) * sc;
      S.el("div", `position:absolute;left:0;top:${top.toFixed(1)}px;filter:drop-shadow(0 10px 14px rgba(0,0,0,.6))`, CH.svg({ w: 740, paint: "service", id: "sis" + i, mast: true }), g);
      S.el("div", `position:absolute;left:-20px;top:${wl - 2}px;width:780px;height:4px;background:linear-gradient(90deg,transparent,rgba(190,220,225,.55),transparent)`, null, g);
      const t0 = tIn[i];
      S.on((t) => { const k = oCub(ramp(t, t0, 0.55)); g.style.opacity = k.toFixed(3); g.style.transform = `translateX(${((1 - k) * (i % 2 ? 160 : -160)).toFixed(1)}px)`; });
      const tg = S.tag("MUSEUM", x + 470, y - 10, tMus + i * 0.09, { col: GOLD, fs: 46, bg: 1 });
      tg.style.background = "rgba(201,180,138,.95)"; tg.style.color = "#14110b"; tg.style.borderLeft = "6px solid #fff3d6";
    });
    S.beat(tMus, "pop", "MUSEUM tags pop (x4, 0.09 s apart)", true);
    tIn.forEach((t, i) => S.beat(t, "whoosh", `sister ${i + 1} slides in`));
  }

  // ======================================================== c02 ledger: bill of sale (a: date + buyer, b: price stamp)
  function ledger(S, stage) {
    board(S, { seed: 11, tint: "36,40,44" });
    const b = stage === "b";
    const cam = S.el("div", `position:absolute;left:0;top:0;width:${W}px;height:${H}px;transform-origin:960px 560px`);
    const doc = S.el("div", `position:absolute;left:470px;top:200px;width:980px;height:720px;background:linear-gradient(160deg,#f3ead6 0%,#e7dcc3 60%,#d9cba9 100%);
      box-shadow:0 40px 80px rgba(0,0,0,.7),0 0 0 1px rgba(0,0,0,.25);transform:rotate(-1.6deg);color:#2a241d;overflow:hidden`, null, cam);
    S.el("div", `position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;background-image:url(${grainURL()})`, null, doc);
    S.el("div", `position:absolute;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(255,255,255,.35),transparent 60%),radial-gradient(ellipse at 90% 100%,rgba(120,90,50,.25),transparent 60%)`, null, doc);
    const L = (y, html, css = "") => S.el("div", `position:absolute;left:70px;top:${y}px;white-space:nowrap;${css}`, html, doc);
    L(54, "BILL OF SALE", `font-size:58px;font-weight:700;letter-spacing:.16em`);
    L(128, "", `width:840px;height:5px;background:${GOLD};opacity:.95`);
    L(150, "SHIP: EX-USS ORISKANY (CV-34)", `font-size:44px;font-weight:500;letter-spacing:.05em;color:#3b332a`);
    const ls = L(238, "", `font-size:52px;font-weight:700;letter-spacing:.06em`);
    const lb = L(330, "", `font-size:52px;font-weight:700;letter-spacing:.06em`);
    const lp = L(440, "", `font-size:52px;font-weight:700;letter-spacing:.06em`);
    L(560, "", `width:840px;height:2px;background:rgba(60,50,40,.35)`);
    L(590, "SOLD FOR SCRAP", `font-size:44px;font-weight:500;letter-spacing:.12em;color:#6a5b48`);
    const tSep = b ? -9 : S.w("september", 0.3), tScrap = b ? -9 : S.w("scrap firm", 2.9), tPeg = b ? -9 : S.w("pegasus", 3.99);
    const tMil = b ? S.w("million", 1.09) : 99;
    const type = (txt, t, t0, cps) => txt.slice(0, Math.max(0, Math.min(txt.length, Math.floor((t - t0) * cps))));
    const stamp = S.el("div", `position:absolute;left:280px;top:424px;padding:2px 20px;border:7px solid ${RUST};color:${RUST};font-size:64px;font-weight:700;letter-spacing:.04em;
      white-space:nowrap;opacity:0;mix-blend-mode:multiply;transform-origin:50% 50%`, "OVER $1 MILLION", doc);   // narration: "just over a million" (GAO95 high bid >$1.2M)
    S.on((t) => {
      if (b) { ls.innerHTML = "SALE &middot; SEPTEMBER 1995"; lb.innerHTML = `BUYER: PEGASUS <span style="color:#7a6a55;font-weight:500">(START-UP)</span>`; }
      else {
        ls.innerHTML = t < tSep ? "" : type("SALE · SEPTEMBER 1995", t, tSep, 34);
        const tb = type("BUYER: ", t, tScrap, 20), tp = type("PEGASUS", t, tPeg, 22);
        lb.innerHTML = (t < tScrap ? "" : tb) + (t >= tPeg ? tp + (t > tPeg + 0.45 ? ` <span style="color:#7a6a55;font-weight:500">(START-UP)</span>` : "") : "")
          + (t >= tScrap && Math.floor(t * 3) % 2 === 0 && t < tPeg + 0.8 ? `<span style="opacity:.6">|</span>` : "");
      }
      lp.innerHTML = b ? "PRICE:" : "";
      // stamp slam: big -> lands on "million" with a jolt
      if (b) { const k = ramp(t, tMil - 0.16, 0.16); stamp.style.opacity = (t < tMil - 0.16 ? 0 : 0.92).toFixed(2);
        stamp.style.transform = `rotate(-7deg) scale(${(t < tMil ? lerp(2.4, 1, k * k) : 1 + 0.06 * Math.exp(-(t - tMil) * 9) * Math.cos((t - tMil) * 30)).toFixed(3)})`; }
      const jolt = b && t > tMil ? 7 * Math.exp(-(t - tMil) * 10) * Math.sin((t - tMil) * 60) : 0;
      const z = b ? lerp(1.1, 1.15, t / S.D) : lerp(1.0, 1.1, sm(t / S.D));
      cam.style.transform = `translate(0px,${(b ? -10 : 0) + jolt}px) scale(${z.toFixed(4)})`;
    });
    if (!b) { S.beat(tSep, "pop", "SALE · SEPTEMBER 1995 types in"); S.beat(tPeg, "pop", "PEGASUS types in", true); }
    else S.beat(tMil, "impact", "OVER $1 MILLION stamp lands", true);
    S.kicker("THE SCRAP SALE", 0.05, null);
  }

  // ======================================================== tally board (c02, callback in c07)
  function tally(S, stage) {
    board(S, { seed: 21, tint: "30,38,44" });
    S.kicker("TRYING TO GET RID OF HER", 0.05);
    const c07 = stage === "c07";
    const rows = [
      { y: 330, label: "SCRAP DEALS", stamp: "COLLAPSED", tMarks: [S.w("two", 0.12), S.w("scrap", 0.24) + 0.2], tStamp: S.w("collapsed", 1.08) },
      { y: 610, label: c07 ? "MORE TRIES" : "MORE ATTEMPTS", stamp: "NO TAKER", tMarks: [S.w("two more", 2.1), S.w("two more", 2.1) + 0.32], tStamp: S.w(c07 ? "taker" : "no taker", c07 ? 3.22 : 4.1) },
    ];
    // NB c02: "found no taker at all" -> the stamp lands on "taker" (4.36); "no" (4.10) starts the slam
    if (!c07) rows[1].tStamp = S.w("taker", 4.36);
    const svg = S.el("div", `position:absolute;inset:0`);
    rows.forEach((r, i) => {
      const plate = S.el("div", `position:absolute;left:240px;top:${r.y}px;width:1440px;height:210px;background:linear-gradient(180deg,rgba(20,26,30,.92),rgba(12,16,19,.92));
        border:2px solid rgba(201,180,138,.28);box-shadow:0 22px 50px rgba(0,0,0,.55);opacity:0`);
      S.rise(plate, i === 0 ? 0.0 : r.tMarks[0] - 0.25, { dy: 24 });
      S.el("div", `position:absolute;left:290px;top:62px;font-size:56px;font-weight:700;color:${CREAM};letter-spacing:.06em;white-space:nowrap`, r.label, plate);
      const num = S.el("div", `position:absolute;left:48px;top:18px;font-size:150px;line-height:1;font-weight:700;color:${GOLD};width:200px;text-align:center`, "", plate);
      // two gold tally strokes drawn on their words
      const st = S.el("div", `position:absolute;left:720px;top:40px;width:200px;height:140px`, `<svg width="200" height="140">
        <path id="tm${i}a" d="M40 12 L34 128" stroke="${GOLD2}" stroke-width="14" stroke-linecap="round" fill="none" stroke-dasharray="120" stroke-dashoffset="120"/>
        <path id="tm${i}b" d="M92 10 L86 128" stroke="${GOLD2}" stroke-width="14" stroke-linecap="round" fill="none" stroke-dasharray="120" stroke-dashoffset="120"/></svg>`, plate);
      const ma = st.querySelector(`#tm${i}a`), mb = st.querySelector(`#tm${i}b`);
      const sp = S.el("div", `position:absolute;left:1000px;top:36px;padding:4px 28px 8px;border:7px solid ${RUST};color:#e0563f;font-size:84px;font-weight:700;letter-spacing:.05em;
        white-space:nowrap;opacity:0;transform-origin:50% 50%;text-shadow:0 0 18px rgba(224,86,63,.35)`, r.stamp, plate);
      S.on((t) => {
        ma.setAttribute("stroke-dashoffset", (120 * (1 - oCub(ramp(t, r.tMarks[0], 0.22)))).toFixed(1));
        mb.setAttribute("stroke-dashoffset", (120 * (1 - oCub(ramp(t, r.tMarks[1], 0.22)))).toFixed(1));
        num.textContent = t >= r.tMarks[1] ? "2" : t >= r.tMarks[0] ? "1" : "";
        num.style.transform = `scale(${(1 + 0.25 * Math.exp(-Math.max(0, t - (t >= r.tMarks[1] ? r.tMarks[1] : r.tMarks[0])) * 10)).toFixed(3)})`;
        const k = ramp(t, r.tStamp - 0.15, 0.15);
        sp.style.opacity = t < r.tStamp - 0.15 ? 0 : 1;
        sp.style.transform = `rotate(-6deg) scale(${(t < r.tStamp ? lerp(2.2, 1, k * k) : 1).toFixed(3)})`;
        const j = t > r.tStamp ? 6 * Math.exp(-(t - r.tStamp) * 10) * Math.sin((t - r.tStamp) * 55) : 0;
        plate.style.marginTop = j.toFixed(1) + "px";
      });
      S.beat(r.tMarks[0], "tick", `${r.label}: tally 1`); S.beat(r.tMarks[1], "tick", `${r.label}: tally 2`);
      S.beat(r.tStamp, "impact", `stamp ${r.stamp}`, i === 0 && !c07 ? false : i === 1 || false);
    });
    // main beat = first stamp (COLLAPSED) for the sfx list's single "main graphic beat"
    S.beats.forEach((b) => { b.main = b.note === "stamp COLLAPSED"; });
  }

  // ======================================================== c06 rounds: sampling timeline Dec 2006 -> Nov 2010, 8 rounds
  function rounds(S, stage) {
    board(S, { seed: 31, tint: "22,40,50" });
    const b = stage === "b";
    S.kicker("FISH SAMPLED ON THE WRECK", 0.05);
    const X0 = 260, X1 = 1660, Y = 600;
    const tDec = b ? -1 : S.w("december", 0.44), tNov = b ? -1 : S.w("november", 2.32), tState = b ? -1 : S.w("state", 4.32), tEsc = b ? -1 : S.w("escambia", 4.97);
    const tEight = b ? S.w("eight", 0.64) : 99;
    const sv = S.el("div", `position:absolute;inset:0`, `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0">
      <defs><filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter></defs>
      <line x1="${X0}" y1="${Y}" x2="${X1}" y2="${Y}" stroke="rgba(247,243,234,.12)" stroke-width="10" stroke-linecap="round"/>
      <line id="rl" x1="${X0}" y1="${Y}" x2="${X0}" y2="${Y}" stroke="${GOLD}" stroke-width="10" stroke-linecap="round"/>
      <line id="rlg" x1="${X0}" y1="${Y}" x2="${X0}" y2="${Y}" stroke="${GOLD}" stroke-width="16" stroke-linecap="round" filter="url(#gl)" opacity=".6"/>
      ${Array.from({ length: 8 }, (_, i) => { const x = X0 + (X1 - X0) * (i + 0.5) / 8; return `<g id="rt${i}"><circle cx="${x}" cy="${Y}" r="22" fill="#0e1a20" stroke="rgba(247,243,234,.5)" stroke-width="4"/>
        <circle id="rc${i}" cx="${x}" cy="${Y}" r="13" fill="${GOLD}" opacity="0"/><circle id="rr${i}" cx="${x}" cy="${Y}" r="22" fill="none" stroke="${GOLD}" stroke-width="4" opacity="0"/></g>`; }).join("")}
      <circle cx="${X0}" cy="${Y}" r="16" fill="${CREAM}"/><circle id="rend" cx="${X1}" cy="${Y}" r="16" fill="${CREAM}" opacity="0"/></svg>`);
    const lab = (txt, x, t0, al) => { const e = S.el("div", `position:absolute;left:${x}px;top:${Y + 44}px;font-size:52px;font-weight:700;color:${CREAM};letter-spacing:.05em;white-space:nowrap;opacity:0;${al ? "transform-origin:100% 0" : ""}`, txt);
      if (al) e.style.marginLeft = "-260px", e.style.width = "260px", e.style.textAlign = "right"; S.pop(e, t0, {}); return e; };
    lab("DEC 2006", X0 - 30, b ? -1 : tDec); lab("NOV 2010", X1 + 30, b ? -1 : tNov, true);
    const fish = Array.from({ length: 8 }, (_, i) => { const x = X0 + (X1 - X0) * (i + 0.5) / 8;
      const e = S.el("div", `position:absolute;left:${x - 45}px;top:${Y - 120}px;opacity:0`, FISH(i % 3 === 0 ? "#d4655a" : "#b9c7cc", 90)); return { e, t0: b ? -1 : tState - 0.2 + i * 0.09 }; });
    const credit = S.el("div", `position:absolute;left:0;width:${W}px;text-align:center;top:${Y + 150}px;font-size:46px;font-weight:500;letter-spacing:.12em;color:${GOLD};white-space:nowrap;opacity:0`, "ESCAMBIA COUNTY + FLORIDA FWC");
    S.rise(credit, b ? -1 : tEsc);
    const big = S.el("div", `position:absolute;left:0;width:${W}px;text-align:center;top:230px;font-size:170px;line-height:1;font-weight:700;color:${CREAM};text-shadow:0 6px 30px rgba(0,0,0,.7);opacity:0`);
    const rl = sv.querySelector("#rl"), rlg = sv.querySelector("#rlg"), rend = sv.querySelector("#rend");
    const rc = [...Array(8)].map((_, i) => sv.querySelector("#rc" + i)), rr = [...Array(8)].map((_, i) => sv.querySelector("#rr" + i));
    const tStartCount = tEight - 0.62;
    S.on((t) => {
      const k = b ? 1 : sm(ramp(t, tDec + 0.15, tNov - tDec - 0.1)), x = lerp(X0, X1, k);
      rl.setAttribute("x2", x.toFixed(1)); rlg.setAttribute("x2", x.toFixed(1)); rend.setAttribute("opacity", k >= 0.999 ? 1 : 0);
      fish.forEach((f, i) => { const q = oBack(ramp(t, f.t0, 0.4)); f.e.style.opacity = sm(ramp(t, f.t0, 0.25)).toFixed(3);
        f.e.style.transform = `translateY(${((1 - q) * -60 + 6 * Math.sin(t * 2 + i)).toFixed(1)}px) scaleX(${i % 2 ? -1 : 1})`; });
      // b: counter 1 -> 8 lands on "eight", each round lights in turn
      const n = b ? clamp(Math.floor(1 + 8 * ramp(t, tStartCount, 0.62)), 0, 8) : 0;
      rc.forEach((c, i) => { const ti = tStartCount + 0.62 * i / 8; c.setAttribute("opacity", b && t >= ti ? 1 : 0);
        const a = t - ti; rr[i].setAttribute("opacity", b && a >= 0 && a < 0.5 ? (1 - a / 0.5).toFixed(3) : 0); rr[i].setAttribute("r", (22 + 40 * clamp(a / 0.5, 0, 1)).toFixed(1)); });
      if (b) { big.style.opacity = sm(ramp(t, tStartCount - 0.1, 0.15)).toFixed(3);
        big.innerHTML = `${Math.max(1, n)}<span style="font-size:72px;color:${GOLD};margin-left:22px;font-weight:500;letter-spacing:.08em">ROUNDS</span>`;
        big.style.transform = `scale(${(t >= tEight ? 1 + 0.16 * Math.exp(-(t - tEight) * 8) : 1).toFixed(3)})`; }
    });
    if (!b) { S.beat(tDec, "pop", "DEC 2006 lands"); S.beat(tNov, "pop", "NOV 2010 lands, line complete", true); S.beat(tState, "whoosh", "fish icons drop on the 8 rounds"); }
    else S.beat(tEight, "land", "counter lands on 8 ROUNDS", true);
  }

  // ======================================================== c06 PCB chart (lines a-e, species a-b, down a-d): ONE chart, staged
  const PCB_ORDER = ["lines_a", "lines_b", "lines_c", "lines_d", "lines_e", "species_a", "species_b", "down_a", "down_b", "down_c", "down_d"];
  function pcb(S, stage) {
    board(S, { seed: 41, tint: "24,36,46" });
    const si = PCB_ORDER.indexOf(stage), isSp = stage.startsWith("species"), isDn = stage.startsWith("down");
    // when an element appears: earlier stage -> already there (-9); this stage -> its word; later stage -> never (99)
    const at = (st, ph, dflt, off = 0) => { const k = PCB_ORDER.indexOf(st); return k < si ? -9 : k === si ? S.w(ph, dflt) + off : 99; };
    const PX0 = 380, PX1 = 1300, PY0 = 270, PY1 = 820;           // plot box
    const XY = (yr) => PX0 + (PX1 - PX0) * yr / 4.6;
    const VY = (v) => PY1 - (PY1 - PY0) * v / 80;                // qualitative scale: only the two screening values are numbers
    const yFL = VY(50), yEPA = VY(20);
    S.kicker("PCBs IN FISH FROM THE WRECK", 0.05, "AVERAGE OF ALL FISH SAMPLED · FWC", 0.2);
    // words of this stage
    const T = {
      linesShow: at("lines_a", "not", 1.48, -0.1),
      barUp: at("lines_b", "average", 1.88), barLand: at("lines_b", "above", 4.36),
      flLab: at("lines_c", "florida's", 0.12, 0.1), epaLab: at("lines_c", "epa's", 2.26),
      scr: at("lines_d", "values", 0.52), poison: at("lines_d", "poison", 1.36),
      mag: at("lines_e", "closer", 2.94), magIn: at("lines_e", "levels", 0.62),
      red: at("species_a", "red snapper", 1.5), por: at("species_a", "porgies", 2.46), hi: at("species_a", "highest", 0.2),
      ver: at("species_b", "vermilion", 0.12, 0.05), scamp: at("species_b", "scamp", 1.38), never: at("species_b", "never crossed", 1.74),
      fall: at("down_a", "down", 1.06), y3: at("down_b", "below", 2.58), y3s: at("down_b", "three years", 0.42),
      y4: at("down_c", "both", 1.96), y4s: at("down_c", "four years", 0.36), stop: at("down_d", "stop", 1.36),
      noadv: at("down_d", "sinking", 4.08, -0.3),
    };
    // lines_a (empty gauge) was cut from the shot list: lines_b now opens the chart, axes + both lines draw in its first 0.6 s
    const first = stage === "lines_b" || stage === "lines_a";
    if (stage === "lines_b") T.linesShow = 0.05;

    const svgE = S.el("div", `position:absolute;inset:0`);
    // static chart body
    const yrs = [1, 2, 3, 4].map((y) => `<line x1="${XY(y)}" y1="${PY1}" x2="${XY(y)}" y2="${PY1 + 18}" stroke="rgba(247,243,234,.7)" stroke-width="3"/>
      <text x="${XY(y)}" y="${PY1 + 66}" text-anchor="middle" font-size="44" fill="${CREAM}" font-weight="500">${y}</text>`).join("");
    svgE.innerHTML = `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0;font-family:Oswald;overflow:visible">
      <defs><filter id="pg" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>
        <linearGradient id="barG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${GOLD2}"/><stop offset="1" stop-color="${GOLD}" stop-opacity=".55"/></linearGradient>
        <pattern id="hatch" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="18" stroke="rgba(247,243,234,.16)" stroke-width="6"/></pattern></defs>
      <g id="axes"><line x1="${PX0}" y1="${PY1}" x2="${PX1}" y2="${PY1}" stroke="rgba(247,243,234,.75)" stroke-width="4"/>
        <line x1="${PX0}" y1="${PY0 - 10}" x2="${PX0}" y2="${PY1}" stroke="rgba(247,243,234,.35)" stroke-width="3"/>${yrs}
        <text x="${(PX0 + PX1) / 2}" y="${PY1 + 124}" text-anchor="middle" font-size="40" fill="rgba(247,243,234,.75)" letter-spacing="5" font-weight="500">YEARS AFTER THE SINKING</text></g>
      <rect id="zHi" x="${PX0}" y="${PY0 - 10}" width="${PX1 - PX0}" height="${yFL - PY0 + 10}" fill="${AMBER}" opacity="0"/>
      <rect id="zLo" x="${PX0}" y="${yEPA}" width="${PX1 - PX0}" height="${PY1 - yEPA}" fill="${TEAL}" opacity="0"/>
      <rect id="hatchR" x="${XY(4.05)}" y="${PY0 - 10}" width="${PX1 - XY(4.05) + 40}" height="${PY1 - PY0 + 10}" fill="url(#hatch)" opacity="0"/>
      <g id="bars"></g>
      <g id="lnFL"><line x1="${PX0}" y1="${yFL}" x2="${PX1 + 40}" y2="${yFL}" stroke="${CREAM}" stroke-width="5" stroke-dasharray="22 14"/></g>
      <g id="lnEPA"><line x1="${PX0}" y1="${yEPA}" x2="${PX1 + 40}" y2="${yEPA}" stroke="${CREAM}" stroke-width="5" stroke-dasharray="22 14"/></g>
      <path id="trend" d="" fill="none" stroke="${GOLD2}" stroke-width="5" stroke-dasharray="4 12" stroke-linecap="round" opacity="0"/>
      <line id="qline" x1="${XY(4.05)}" y1="${VY(13)}" x2="${PX1 + 40}" y2="${VY(13)}" stroke="${GOLD2}" stroke-width="5" stroke-dasharray="14 14" opacity="0"/>
    </svg>`;
    const q = (id) => svgE.querySelector("#" + id);
    const axes = q("axes"), lnFL = q("lnFL"), lnEPA = q("lnEPA"), zHi = q("zHi"), zLo = q("zLo"), hatchR = q("hatchR"), barsG = q("bars"), trend = q("trend"), qline = q("qline");
    // average bars: years 0-2 (above both), ~2.9 yr (below Florida, just above EPA), ~3.5-3.9 yr (below both). Heights are QUALITATIVE.
    const bars = [
      { x0: XY(0.25), x1: XY(2.0), v: 60, tUp: T.barUp, tLand: T.barLand, lab: "FIRST 2 YEARS" },
      { x0: XY(2.72), x1: XY(3.08), v: 33, tUp: T.y3s, tLand: T.y3, lab: "≈ 2.9 YRS" },
      { x0: XY(3.45), x1: XY(3.95), v: 13, tUp: T.y4s, tLand: T.y4, lab: "≈ 3.5–3.9 YRS" },
    ];
    barsG.innerHTML = bars.map((b, i) => `<g id="bg${i}" opacity="0"><rect id="bglow${i}" x="${b.x0}" y="${PY1}" width="${b.x1 - b.x0}" height="0" fill="${GOLD}" filter="url(#pg)" opacity=".45"/>
      <rect id="br${i}" x="${b.x0}" y="${PY1}" width="${b.x1 - b.x0}" height="0" fill="url(#barG)" opacity=".82"/><rect id="bt${i}" x="${b.x0}" y="${PY1}" width="${b.x1 - b.x0}" height="7" fill="#fff3d6"/>
      <circle id="bring${i}" cx="${(b.x0 + b.x1) / 2}" cy="${PY1}" r="10" fill="none" stroke="${GOLD2}" stroke-width="5" opacity="0"/></g>`).join("");
    // labels (HTML, >= 40 px)
    const lbl = (html, x, y, css = "") => S.el("div", `position:absolute;left:${x}px;top:${y}px;white-space:nowrap;font-weight:700;letter-spacing:.05em;opacity:0;${css}`, html);
    const flL = lbl("", PX1 + 64, yFL - 34, `font-size:44px;color:${CREAM};line-height:1.05;transform-origin:0% 50%;text-shadow:0 2px 10px rgba(0,0,0,.9)`);
    const epL = lbl("", PX1 + 64, yEPA - 34, `font-size:44px;color:${CREAM};line-height:1.05;transform-origin:0% 50%;text-shadow:0 2px 10px rgba(0,0,0,.9)`);
    const scrNote = lbl("SCREENING VALUES ARE NOT POISON LIMITS", 0, PY0 - 82, `font-size:42px;color:${GOLD};width:${W}px;text-align:center;font-weight:500;letter-spacing:.08em`);
    const barLab = bars.map((b, i) => lbl(i ? "" : b.lab, (b.x0 + b.x1) / 2 - 300, 0, `width:600px;text-align:center;font-size:${i ? 40 : 46}px;color:${GOLD2}`));
    const aboveTag = lbl("ABOVE BOTH LINES", (bars[0].x0 + bars[0].x1) / 2 - 300, 0, `width:600px;text-align:center;font-size:46px;color:#14110b;`);
    aboveTag.innerHTML = `<span style="background:${GOLD2};padding:4px 18px 6px">ABOVE BOTH LINES</span>`;
    const y3Tag = S.tag("≈ 2.9 YEARS · BELOW FLORIDA'S LINE", 400, PY0 - 92, T.y3 + 0.05, { out: T.y4 - 0.1 });
    const y4Tag = S.tag("≈ 3.5–3.9 YEARS · BELOW BOTH", 400, PY0 - 92, T.y4 + 0.05, {});
    const stopTag = S.tag("LAST PUBLISHED RESULTS · FWC 2011", 400, PY0 - 92, T.stop + 0.1, { fs: 44 });
    const qMark = lbl("?", XY(4.32) - 14, VY(13) - 110, `font-size:96px;color:${GOLD2}`);
    const noAdv = lbl("NO FISH ADVISORY WAS EVER ISSUED", 0, VY(70) - 20, `width:${W}px;text-align:center;font-size:46px;color:${CREAM};letter-spacing:.08em`);
    // magnifier (lines_e)
    const mag = S.el("div", `position:absolute;left:0;top:0;width:260px;height:260px;opacity:0`, `<svg width="260" height="260" viewBox="0 0 260 260" style="overflow:visible">
      <circle cx="110" cy="110" r="86" fill="rgba(143,208,198,.12)" stroke="${CREAM}" stroke-width="12"/><circle cx="110" cy="110" r="86" fill="none" stroke="${GOLD}" stroke-width="4" opacity=".8"/>
      <path d="M172 172 L236 236" stroke="${CREAM}" stroke-width="26" stroke-linecap="round"/><path d="M66 74 A52 52 0 0 1 112 52" stroke="rgba(255,255,255,.7)" stroke-width="8" fill="none" stroke-linecap="round"/></svg>`);
    const closer = lbl("= HEALTH OFFICIALS TAKE A CLOSER LOOK", 0, PY0 - 82, `font-size:42px;color:${GOLD};width:${W}px;text-align:center;font-weight:500;letter-spacing:.06em`);
    // species tokens
    const tok = (name, col, x, y, t0, ab) => { const e = S.el("div", `position:absolute;left:${x}px;top:${y}px;display:flex;align-items:center;gap:16px;opacity:0;transform-origin:0 50%;
        padding:6px 20px 6px 12px;background:rgba(10,14,18,.86);border-left:6px solid ${ab ? AMBER : TEAL};box-shadow:0 10px 24px rgba(0,0,0,.5)`,
        `${FISH(col, 96)}<span style="font-size:46px;font-weight:700;color:${CREAM};letter-spacing:.05em;white-space:nowrap">${name}</span>`);
      S.pop(e, t0, {}); return e; };
    const tokens = isSp ? [tok("RED SNAPPER", "#d4655a", 400, VY(66) - 34, T.red, 1), tok("PORGIES", "#d9a0a0", 860, VY(66) - 34, T.por, 1),
      tok("VERMILION SNAPPER", "#e06a4f", 400, VY(10) - 40, T.ver, 0), tok("SCAMP", "#9a8a72", 960, VY(10) - 40, T.scamp, 0)] : [];
    const hiLab = isSp ? lbl("HIGHEST READINGS", PX0 + 24, PY0 - 2, `font-size:42px;color:${AMBER};font-weight:500;letter-spacing:.1em`) : null;
    const neverLab = isSp ? lbl("NEVER CROSSED EITHER LINE", PX0 + 24, VY(20) - 58, `font-size:42px;color:${TEAL};font-weight:500;letter-spacing:.1em`) : null;

    S.on((t) => {
      const show = (t0, d = 0.35) => sm(ramp(t, t0, d));
      axes.setAttribute("opacity", first ? sm(ramp(t, 0.0, 0.4)).toFixed(3) : 1);
      // the two lines draw left -> right (lines_a), labels on their words (lines_c), "screening value" from lines_d on
      [[lnFL, 0], [lnEPA, 0.15]].forEach(([g, d]) => { const k = oCub(ramp(t, T.linesShow + d, 0.6)), ln = g.querySelector("line");
        ln.setAttribute("x2", (PX0 + (PX1 + 40 - PX0) * k).toFixed(1)); g.setAttribute("opacity", k > 0 ? 1 : 0); });
      const scr = t >= T.scr;
      const sv = `<div style="font-size:40px;font-weight:500;color:${GOLD};letter-spacing:.08em">SCREENING VALUE</div>`;
      flL.innerHTML = `FLORIDA <span style="color:${GOLD2}">50 ppb</span>` + (scr ? sv : "");
      epL.innerHTML = `EPA <span style="color:${GOLD2}">20 ppb</span>` + (scr ? sv : "");
      [[flL, T.flLab], [epL, T.epaLab]].forEach(([e, t0]) => { const k = ramp(t, t0, 0.38); e.style.opacity = sm(k * 1.8).toFixed(3);
        const sw = t >= T.scr && t < T.scr + 0.3 ? 1 + 0.12 * Math.sin(ramp(t, T.scr, 0.3) * Math.PI) : 1;
        e.style.transform = `scale(${(lerp(0.7, 1, oBack(k)) * sw).toFixed(4)})`; });
      scrNote.style.opacity = (si >= 3 && si <= 3 ? show(T.poison) : 0).toFixed(3);
      // bars
      bars.forEach((b, i) => {
        const g = q("bg" + i), up = b.tUp, land = b.tLand;
        if (up > 50) { g.setAttribute("opacity", 0); barLab[i].style.opacity = 0; return; }
        // rise starts at "up", lands exactly on "land" (ease out), overshoot settle
        const k = t < land ? oCub(ramp(t, up, land - up)) * 0.985 : 1 + 0.03 * Math.exp(-(t - land) * 8) * Math.cos((t - land) * 22);
        let v = b.v * k;
        // down_a: the first bar dims to a ghost once the numbers "came down"
        const dim = i === 0 && (isDn) ? lerp(1, 0.32, sm(ramp(t, T.fall - 0.4, 0.6))) : isSp ? 0.38 : 1;
        const yTop = VY(v), h = PY1 - yTop;
        ["br", "bglow"].forEach((p) => { const r = q(p + i); r.setAttribute("y", yTop.toFixed(1)); r.setAttribute("height", Math.max(0, h).toFixed(1)); });
        q("bt" + i).setAttribute("y", (yTop - 3).toFixed(1));
        g.setAttribute("opacity", (sm(ramp(t, up, 0.2)) * dim).toFixed(3));
        const la = t - land, ring = q("bring" + i); ring.setAttribute("cy", yTop.toFixed(1));
        ring.setAttribute("opacity", la >= 0 && la < 0.7 ? (1 - la / 0.7).toFixed(3) : 0); ring.setAttribute("r", (10 + 120 * clamp(la / 0.7, 0, 1)).toFixed(1));
        barLab[i].style.top = (i === 0 ? PY1 - 64 : yTop - 58).toFixed(1) + "px";
        barLab[i].style.opacity = (sm(ramp(t, land - 0.1, 0.3)) * (i === 0 ? dim : 1) * (isSp ? 0 : 1)).toFixed(3);
        if (i === 0) { aboveTag.style.top = (yTop - 78).toFixed(1) + "px"; aboveTag.style.opacity = (sm(ramp(t, land + 0.05, 0.25)) * (si <= 4 ? 1 : 0)).toFixed(3);
          aboveTag.style.transform = `scale(${lerp(0.7, 1, oBack(ramp(t, land + 0.05, 0.35))).toFixed(3)})`; }
      });
      // trend dashes between bar tops (down_a on)
      if (isDn) { const pts = [[(bars[0].x0 + bars[0].x1) / 2, VY(60)], [XY(2.9), VY(33)], [XY(3.7), VY(13)]];
        const k = sm(ramp(t, T.fall - 0.2, 0.6)), end = lerp(pts[0][0] + 1, XY(2.9), k);
        let d = `M${pts[0][0]} ${pts[0][1]}`; if (end < XY(2.9)) { const u = (end - pts[0][0]) / (XY(2.9) - pts[0][0]); d += ` L${f1(end)} ${f1(lerp(pts[0][1], pts[1][1], u))}`; } else d += ` L${pts[1][0]} ${pts[1][1]}`;
        if (t > T.y3 && T.y3 < 50) d += ` L${pts[2][0]} ${pts[2][1]}`;
        trend.setAttribute("d", d); trend.setAttribute("opacity", (0.85 * k).toFixed(3)); }
      // zones for species, magnifier, stop
      zHi.setAttribute("opacity", (isSp ? 0.1 * show(T.hi) : 0).toFixed(3));
      zLo.setAttribute("opacity", (stage === "species_b" ? 0.1 * show(T.ver - 0.2) : 0).toFixed(3));
      if (hiLab) { hiLab.style.opacity = show(T.red - 0.2).toFixed(3); neverLab.style.opacity = show(T.never).toFixed(3); }
      if (stage === "lines_e") {
        const k = oCub(ramp(t, T.magIn, T.mag - T.magIn)), x = lerp(PX1 + 300, (XY(2) + PX1) / 2 - 110, k), y = lerp(PY0 - 120, (yFL + yEPA) / 2 - 110, k);
        const land = t - T.mag, bob = land > 0 ? 1 + 0.1 * Math.exp(-land * 7) * Math.cos(land * 18) : 1;
        mag.style.opacity = sm(ramp(t, T.magIn, 0.3)).toFixed(3); mag.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${bob.toFixed(3)})`;
        closer.style.opacity = show(T.mag + 0.05).toFixed(3);
      }
      hatchR.setAttribute("opacity", stage === "down_d" ? show(T.stop, 0.5).toFixed(3) : 0);
      qline.setAttribute("opacity", stage === "down_d" ? show(T.stop, 0.4).toFixed(3) : 0);
      const qe = ramp(t, T.stop + 0.3, 0.4); qMark.style.opacity = (stage === "down_d" ? sm(qe) : 0).toFixed(3); qMark.style.transform = `scale(${lerp(0.5, 1, oBack(qe)).toFixed(3)})`;
      noAdv.style.opacity = (stage === "down_d" ? show(T.noadv) : 0).toFixed(3);
      if (stage === "down_d") { y3Tag.style.opacity = 0; y4Tag.style.opacity = 0; }
    });
    // beats per stage
    const B = {
      lines_a: () => S.beat(T.linesShow, "whoosh", "two screening-value lines draw", true),
      lines_b: () => { S.beat(T.linesShow, "whoosh", "chart + two screening-value lines draw"); S.beat(T.barUp, "riser", "average bar starts to rise"); S.beat(T.barLand, "land", "bar lands ABOVE BOTH LINES", true); },
      lines_c: () => { S.beat(T.flLab, "pop", "label FLORIDA 50 ppb"); S.beat(T.epaLab, "pop", "label EPA 20 ppb", true); },
      lines_d: () => { S.beat(T.scr, "pop", "labels become SCREENING VALUE", true); S.beat(T.poison, "pop", "note: not poison limits"); },
      lines_e: () => S.beat(T.mag, "land", "magnifier lands over the lines", true),
      species_a: () => { S.beat(T.red, "pop", "RED SNAPPER token (above)", true); S.beat(T.por, "pop", "PORGIES token (above)"); },
      species_b: () => { S.beat(T.ver, "pop", "VERMILION SNAPPER token (below)", true); S.beat(T.scamp, "pop", "SCAMP token (below)"); S.beat(T.never, "pop", "NEVER CROSSED EITHER LINE"); },
      down_a: () => S.beat(T.fall, "whoosh", "first bar dims, trend starts down", true),
      down_b: () => { S.beat(T.y3s, "riser", "~2.9 yr bar rises"); S.beat(T.y3, "land", "bar lands below FLORIDA", true); },
      down_c: () => { S.beat(T.y4s, "riser", "~3.5-3.9 yr bar rises"); S.beat(T.y4, "land", "bar lands BELOW BOTH", true); },
      down_d: () => { S.beat(T.stop, "pop", "data stops: hatched, dashed ?", true); S.beat(T.noadv, "pop", "NO FISH ADVISORY WAS EVER ISSUED"); },
    };
    B[stage]();
  }

  // ======================================================== c06 snapper: carrier vs rubble reef, ~7x (attributed)
  function snapper(S, stage) {
    board(S, { seed: 51, tint: "30,34,44" });
    const b = stage === "b";
    S.kicker("RED SNAPPER · SAME DAYS, 2008", 0.05);
    const src = S.el("div", `position:absolute;left:0;width:${W}px;top:848px;text-align:center;font-size:40px;font-weight:500;letter-spacing:.08em;color:rgba(247,243,234,.85);white-space:nowrap`,
      `<span style="background:rgba(10,12,14,.82);padding:6px 22px;border-top:4px solid ${GOLD}">SOURCE: <b style="color:${GOLD2}">ENVIRONMENTAL GROUPS</b> · 2012 PETITION, FROM FWC DATA</span>`);
    const X0 = 700, XMAX = 1580, rows = [{ y: 330, lab: "ON THE CARRIER", v: 55.22 }, { y: 600, lab: "ON A RUBBLE REEF", sub: "8 MILES AWAY", v: 7.6 }];
    const tSn = b ? -9 : S.w("snapper", 0.46), tCar = b ? -9 : S.w("carrier", 1.3), tCarried = b ? -9 : S.w("carried", 1.62);
    const tRub0 = b ? 0.05 : 99, tSeven = b ? S.w("seven", 0.46) : 99, tRubble = b ? S.w("rubble", 4.1) : 99;
    const els = rows.map((r, i) => {
      const fish = S.el("div", `position:absolute;left:150px;top:${r.y - 10}px;opacity:0`, SNAPPER(170));
      const lab = S.el("div", `position:absolute;left:150px;top:${r.y + 82}px;font-size:46px;font-weight:700;color:${CREAM};letter-spacing:.05em;white-space:nowrap;opacity:0`,
        r.lab + (r.sub ? `<div style="font-size:40px;color:${GOLD};font-weight:500">${r.sub}</div>` : ""));
      const tr = S.el("div", `position:absolute;left:${X0}px;top:${r.y + 30}px;width:${XMAX - X0}px;height:30px;border-radius:15px;background:rgba(247,243,234,.08)`);
      const bar = S.el("div", `position:absolute;left:${X0}px;top:${r.y + 30}px;width:0;height:30px;border-radius:15px;background:linear-gradient(90deg,${i ? "#c9d6d6" : GOLD},${i ? "#e8f0f0" : GOLD2});box-shadow:0 0 26px ${i ? "rgba(200,220,220,.3)" : "rgba(226,207,160,.55)"}`);
      return { fish, lab, bar, tr, r };
    });
    const t0s = [tSn, b ? -9 : tSn + 0.25], tLab = [tCar, b ? -9 : tCar + 0.2], tBar = [tCarried, tRub0];
    const brk = S.el("div", `position:absolute;left:0;top:0;opacity:0`, `<svg width="${W}" height="${H}"><path id="bk" d="" fill="none" stroke="${GOLD2}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>`);
    const bk = brk.querySelector("#bk");
    const seven = S.el("div", `position:absolute;left:1240px;top:400px;font-size:150px;line-height:1;font-weight:700;color:${GOLD2};text-shadow:0 6px 30px rgba(0,0,0,.8);white-space:nowrap;opacity:0;transform-origin:0 50%`,
      `≈&thinsp;7<span style="font-size:110px">×</span>`);
    const wC = (XMAX - X0) * 55.22 / 58, wR = (XMAX - X0) * 7.6 / 58;
    S.on((t) => {
      els.forEach((e, i) => {
        const k = oBack(ramp(t, t0s[i], 0.45)); e.fish.style.opacity = sm(ramp(t, t0s[i], 0.25)).toFixed(3);
        e.fish.style.transform = `translateX(${((1 - k) * -120).toFixed(1)}px) translateY(${(5 * Math.sin(t * 2.4 + i * 2)).toFixed(1)}px)`;
        e.lab.style.opacity = sm(ramp(t, tLab[i], 0.3)).toFixed(3);
        const bw = i === 0 ? wC * oCub(ramp(t, tBar[0], 0.8)) : wR * oCub(ramp(t, tBar[1], 0.5));
        e.bar.style.width = bw.toFixed(1) + "px";
        if (i === 1 && b) e.lab.style.color = t > tRubble ? GOLD2 : CREAM;
      });
      // bracket: from the short bar's end up to the long bar's end, "~7x" lands on "seven"
      const k = oCub(ramp(t, tSeven - 0.35, 0.35)), xb = X0 + wC + 40, yA = rows[0].y + 45, yB = rows[1].y + 45;
      const yb = lerp(yA, yB, k);
      bk.setAttribute("d", `M${X0 + wC + 10} ${yA} L${xb} ${yA} L${xb} ${yb.toFixed(1)}` + (k >= 1 ? ` L${X0 + wR + 16} ${yB}` : ""));
      brk.style.opacity = b ? sm(ramp(t, tSeven - 0.35, 0.1)).toFixed(3) : 0;
      const ls = t - tSeven; seven.style.opacity = b && ls >= -0.05 ? 1 : 0;
      seven.style.transform = `translateX(${(xb - 1240 + 30).toFixed(0)}px) scale(${(ls < 0 ? 0.6 : 1 + 0.18 * Math.exp(-ls * 8) * Math.cos(ls * 16)).toFixed(3)})`;
    });
    if (!b) { S.beat(tSn, "whoosh", "two snapper icons in"); S.beat(tCarried, "riser", "carrier bar grows", true); }
    else { S.beat(tSeven, "land", "≈7× lands on 'seven'", true); S.beat(tRubble, "pop", "rubble reef label highlights"); }
  }

  // ======================================================== c04 deck cutaway: exploded flight-deck layers (asphalt / wood), PCBs, catapults
  function deck(S, stage) {
    board(S, { seed: 61, tint: "26,38,48" });
    const CH = root.CarrierHero, M = CH.meta("hulk"), L = M.L, SW = 1640, s = SW / (L + 2 * M.pad), XS = 150, DY = 770, WL = DY - M.deckY * s;
    const X = (x) => XS + x * s, Y = (y) => WL + y * s, len = L * s, x0 = X(0), DX = 70;
    const cam = S.el("div", `position:absolute;left:0;top:0;width:${W}px;height:${H}px;transform-origin:0 0`);
    S.el("div", `position:absolute;left:${XS - M.pad * s}px;top:${WL + (M.sideY0 - M.pad) * s}px;filter:drop-shadow(0 14px 18px rgba(0,0,0,.6))`, CH.svg({ w: SW, paint: "hulk", id: "dk" }), cam);
    S.el("div", `position:absolute;left:0;top:${WL}px;width:${W}px;height:${H - WL}px;background:linear-gradient(180deg,rgba(44,96,104,.62),rgba(8,20,28,.94) 70%);border-top:3px solid rgba(220,240,235,.5)`, null, cam);
    const R = rnd(62);
    let speck = ""; for (let k = 0; k < 160; k++) speck += `<rect x="${(R() * 120).toFixed(1)}" y="${(R() * 20).toFixed(1)}" width="${(1 + R() * 2.5).toFixed(1)}" height="${(0.6 + R() * 1.2).toFixed(1)}" fill="${R() < 0.5 ? "#4a4b4e" : "#1c1d1f"}"/>`;
    const sv = S.el("div", `position:absolute;left:0;top:0;width:${W}px;height:${H}px`, `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0;overflow:visible">
      <defs>
        <pattern id="pl" width="190" height="7.14" patternUnits="userSpaceOnUse"><rect width="190" height="7.14" fill="#8d6b45"/><rect y="3.57" width="190" height="3.57" fill="#7f5f3d"/>
          <path d="M0 0 L190 0 M0 3.57 L190 3.57" stroke="#4a3826" stroke-width=".7"/><path d="M0 0 L0 3.57 M95 3.57 L95 7.14" stroke="#4a3826" stroke-width="1.6"/></pattern>
        <pattern id="as" width="120" height="20" patternUnits="userSpaceOnUse"><rect width="120" height="20" fill="#2b2c2f"/>${speck}</pattern>
        <linearGradient id="curl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#18191b"/><stop offset=".55" stop-color="#5a5b5e"/><stop offset="1" stop-color="#1b1c1e"/></linearGradient>
        <radialGradient id="seep"><stop offset="0" stop-color="${AMBER}" stop-opacity=".95"/><stop offset=".6" stop-color="${AMBER}" stop-opacity=".45"/><stop offset="1" stop-color="${AMBER}" stop-opacity="0"/></radialGradient>
        <filter id="bl"><feGaussianBlur stdDeviation="10"/></filter><filter id="bl2"><feGaussianBlur stdDeviation="4"/></filter>
        <clipPath id="slabC" clipPathUnits="userSpaceOnUse"><rect x="0" y="0" width="${len}" height="100"/></clipPath><clipPath id="peel" clipPathUnits="userSpaceOnUse"><rect id="peelR" x="0" y="-20" width="${len}" height="140"/></clipPath>
      </defs>
      <g id="guides" stroke="rgba(201,180,138,.55)" stroke-width="2.5" stroke-dasharray="8 9" fill="none"><path id="gL"/><path id="gR"/></g>
      <g id="wood"><path id="wF" fill="#5a4129"/><path id="wE" fill="#4b3622"/>
        <g id="wT"><rect width="${len}" height="100" fill="url(#pl)"/><rect id="wAmb" width="${len}" height="100" fill="${AMBER}" opacity="0" style="mix-blend-mode:screen"/>
          <rect id="wAmbB" x="-20" y="-10" width="${len + 40}" height="120" fill="${AMBER}" opacity="0" filter="url(#bl)" style="mix-blend-mode:screen"/>
          <g id="seeps" opacity="0" clip-path="url(#slabC)">${[0, 1].map((i) => `<ellipse id="sp${i}" cx="${(805 * s).toFixed(1)}" cy="${i ? 66 : 30}" rx="1" ry="1" fill="url(#seep)" style="mix-blend-mode:screen"/>`).join("")}</g>
          <g id="cats" opacity="0">${[30, 66].map((v) => `<path d="M${(700 * s).toFixed(1)} ${v} L${(905 * s).toFixed(1)} ${v}" stroke="#15110c" stroke-width="5"/>
            <path class="cg" d="M${(700 * s).toFixed(1)} ${v} L${(905 * s).toFixed(1)} ${v}" stroke="${GOLD2}" stroke-width="3"/>
            <path class="cg" d="M${(700 * s).toFixed(1)} ${v} L${(905 * s).toFixed(1)} ${v}" stroke="${GOLD2}" stroke-width="10" filter="url(#bl2)" opacity=".8"/>`).join("")}</g></g></g>
      <g id="asph"><path id="aF" fill="#17181a"/><path id="aE" fill="#121315"/>
        <g id="aT"><rect width="${len}" height="100" fill="url(#as)" clip-path="url(#peel)"/><rect id="curlR" x="0" y="0" width="26" height="100" fill="url(#curl)" opacity="0"/></g></g>
    </svg>`, cam);
    const q = (id) => sv.querySelector("#" + id);
    const E = { wood: q("wood"), wF: q("wF"), wE: q("wE"), wT: q("wT"), wAmb: q("wAmb"), wAmbB: q("wAmbB"), cats: q("cats"), seeps: q("seeps"), sp: [q("sp0"), q("sp1")],
      asph: q("asph"), aF: q("aF"), aE: q("aE"), aT: q("aT"), peelR: q("peelR"), curlR: q("curlR"), gL: q("gL"), gR: q("gR") };
    const WTH = 22, ATH = 11;
    const slab = (T, F, Ed, yf, dy, th, u0 = 0) => {     // top face matrix + front face + bow end face
      T.setAttribute("transform", `matrix(1,0,${(DX / 100).toFixed(4)},${(-dy / 100).toFixed(4)},${x0.toFixed(1)},${yf.toFixed(1)})`);
      F.setAttribute("d", `M${(x0 + u0).toFixed(1)} ${yf.toFixed(1)} L${(x0 + len).toFixed(1)} ${yf.toFixed(1)} L${(x0 + len).toFixed(1)} ${(yf + th).toFixed(1)} L${(x0 + u0).toFixed(1)} ${(yf + th).toFixed(1)} Z`);
      Ed.setAttribute("d", `M${x0 + len} ${yf} L${x0 + len + DX} ${yf - dy} L${x0 + len + DX} ${yf - dy + th} L${x0 + len} ${yf + th} Z`);
    };
    const A = stage === "a", A2 = stage === "a2", Bs = stage === "b", Cs = stage === "c";
    const tLift = A ? 0.15 : -9, tAs = A ? S.w("asphalt", 1.16) : -9, tFD = A ? S.w("flight deck", 2.08) : -9;
    const tFull = A2 ? S.w("full", 1.32) : -9, tP = A2 ? S.w("pcbs", 1.78) : -9;
    const tCat = Bs ? S.w("catapults", 1.8) : -9, tCame = Cs ? S.w("came out", 1.26) : 99;
    const PEEL = 1.25;
    // flakes from the peel edge (screen space)
    const flakes = [];
    if (A) for (let k = 0; k < 46; k++) flakes.push({ e: S.el("div", `position:absolute;left:0;top:0;width:${6 + R() * 10}px;height:${3 + R() * 5}px;background:${R() < 0.5 ? "#2a2b2e" : "#3c3d40"};opacity:0`, null, cam),
      tb: tAs + R() * PEEL, v: R() * 100, vx: -60 + R() * 140, vy: -160 - R() * 160, rot: R() * 720 - 360 });
    const haze = [];
    for (let k = 0; k < 60; k++) haze.push({ e: S.el("div", `position:absolute;left:0;top:0;width:${3 + R() * 5}px;height:${3 + R() * 5}px;border-radius:50%;background:${AMBER};filter:blur(1px);opacity:0`, null, cam),
      u: R(), v: R() * 100, ph: R(), sp: 30 + R() * 50 });
    const dust = [];
    if (Cs) for (let k = 0; k < 90; k++) dust.push({ e: S.el("div", `position:absolute;left:0;top:0;width:${4 + R() * 8}px;height:${3 + R() * 6}px;background:${R() < 0.5 ? "#9b774c" : AMBER};opacity:0`, null, cam),
      u: R(), v: R() * 100, vx: (R() - 0.5) * 220, vy: -80 - R() * 200, d: R() * 0.5 });
    // tags (screen space, outside the camera)
    const tagAs = S.tag("ASPHALT", 236, 214, A ? 0.75 : 99, { out: A ? tAs + PEEL - 0.1 : null });
    const tagW = S.tag("WOOD DECK", 236, 352, A ? tFD : -9, { out: Cs ? tCame + 0.2 : null });
    const tagP = S.tag(`<span style="color:${AMBER}">PCBs</span> IN THE WOOD`, 820, 250, A2 ? tP : (Bs || Cs ? -9 : 99), { col: AMBER, fs: 60, out: Bs ? 0.3 : Cs ? 0.05 : null });
    const tagC = S.tag(`FLUID FROM THE <span style="color:${AMBER}">CATAPULTS</span>`, 700, 196, Bs ? tCat : 99, { col: AMBER, fs: 54 });
    const tagR = S.tag("THE WHOLE WOODEN DECK: REMOVED", 560, 560, Cs ? tCame + 0.3 : 99, { fs: 54 });
    S.kicker("CLEANUP · CORPUS CHRISTI, TEXAS", 0.05);
    const pt = (u, v, yf, dy) => [x0 + u + DX * v / 100, yf - dy * v / 100];
    S.on((t) => {
      const kL = A ? sm(ramp(t, tLift, 0.9)) : 1;
      let wy = lerp(DY - 2, 566, kL), ay = lerp(DY - 2 - WTH, 436, kL), dy = lerp(4, 100, kL);
      // c: the wood layer lifts away and dissolves
      const kOut = sm(ramp(t, tCame - 0.3, 0.9)); wy -= 300 * kOut;
      E.wood.setAttribute("opacity", (1 - sm(ramp(t, tCame + 0.05, 0.6))).toFixed(3));
      slab(E.wT, E.wF, E.wE, wy, dy, WTH); slab(E.aT, E.aF, E.aE, ay, dy, ATH);
      // asphalt peel (stern -> bow); gone after stage a
      const pk = A ? sm(ramp(t, tAs, PEEL)) : 1, pu = pk * len;
      E.peelR.setAttribute("x", pu.toFixed(1)); E.peelR.setAttribute("width", Math.max(0, len - pu).toFixed(1));
      slab(E.aT, E.aF, E.aE, ay, dy, ATH, pu); E.asph.setAttribute("opacity", pk >= 1 ? 0 : 1);
      E.curlR.setAttribute("x", (pu - 13).toFixed(1)); E.curlR.setAttribute("opacity", pk > 0 && pk < 1 ? 1 : 0);
      E.curlR.setAttribute("transform", `translate(0,${(-6 * Math.sin(pk * Math.PI)).toFixed(1)})`);
      // exploded-view guides from the deck ends up to the layers
      E.gL.setAttribute("d", `M${x0} ${DY} L${x0} ${Math.min(wy, ay)}`); E.gR.setAttribute("d", `M${x0 + len} ${DY} L${x0 + len} ${Math.min(wy, ay)}`);
      q("guides").setAttribute("opacity", (kL * (1 - kOut)).toFixed(3));
      flakes.forEach((f) => { const a = t - f.tb; if (a < 0 || a > 1.3) { f.e.style.opacity = 0; return; }
        const [px, py] = pt(f.tb >= tAs ? sm(ramp(f.tb, tAs, PEEL)) * len : 0, f.v, ay, dy);
        f.e.style.opacity = (1 - a / 1.3).toFixed(3);
        f.e.style.transform = `translate(${(px + f.vx * a).toFixed(1)}px,${(py + f.vy * a + 260 * a * a).toFixed(1)}px) rotate(${(f.rot * a).toFixed(0)}deg)`; });
      // PCB amber: a2 builds on "full of" -> "PCBs"; b keeps it dimmer and seeps from the catapults; c carries it away
      const amb = A2 ? sm(ramp(t, tFull, tP - tFull + 0.15)) * (0.55 + 0.12 * Math.sin(t * 7)) : Bs ? 0.32 + 0.06 * Math.sin(t * 6) : Cs ? 0.4 : 0;
      E.wAmb.setAttribute("opacity", (amb * 0.75).toFixed(3)); E.wAmbB.setAttribute("opacity", (amb * 0.6).toFixed(3));
      haze.forEach((h) => { const on = A2 ? sm(ramp(t, tP - 0.2, 0.4)) : Bs ? 0.5 : 0; const a = ((t * h.sp / 100 + h.ph) % 1);
        if (!on) { h.e.style.opacity = 0; return; } const [px, py] = pt(h.u * len, h.v, wy, dy);
        h.e.style.opacity = (on * Math.sin(a * Math.PI) * 0.8).toFixed(3); h.e.style.transform = `translate(${(px + 10 * Math.sin(a * 6 + h.ph * 9)).toFixed(1)}px,${(py - a * 120).toFixed(1)}px)`; });
      const cg = Bs ? sm(ramp(t, tCat - 0.15, 0.25)) : 0; E.cats.setAttribute("opacity", Bs ? 1 : 0);
      sv.querySelectorAll(".cg").forEach((c) => c.setAttribute("opacity", (cg * (0.75 + 0.25 * Math.sin(t * 10))).toFixed(3)));
      const sk = Bs ? oCub(ramp(t, tCat, 1.4)) : 0; E.seeps.setAttribute("opacity", sk > 0 ? 1 : 0);
      E.sp.forEach((e, i) => { e.setAttribute("rx", (10 + 260 * s * sk).toFixed(1)); e.setAttribute("ry", (4 + 26 * sk).toFixed(1)); });
      dust.forEach((p) => { const a = t - tCame - p.d * 0.5; if (a < 0 || a > 1.4) { p.e.style.opacity = 0; return; }
        const [px, py] = pt(p.u * len, p.v, wy, dy); p.e.style.opacity = (Math.min(1, a / 0.15) * (1 - a / 1.4)).toFixed(3);
        p.e.style.transform = `translate(${(px + p.vx * a).toFixed(1)}px,${(py + p.vy * a).toFixed(1)}px) rotate(${(a * 300).toFixed(0)}deg)`; });
      // camera: b pushes in on the bow
      const z = Bs ? lerp(1, 1.55, sm(ramp(t, 0.05, 1.1))) : 1.0 + 0.02 * t / S.D, fx = 1700, fy = 540;
      cam.style.transform = `translate(${(fx * (1 - z)).toFixed(1)}px,${(fy * (1 - z)).toFixed(1)}px) scale(${z.toFixed(4)})`;
    });
    if (A) { S.beat(tLift, "whoosh", "deck layers lift off (exploded view)"); S.beat(tAs, "scrape", "asphalt starts to peel back", true); S.beat(tFD, "pop", "WOOD DECK tag"); }
    if (A2) S.beat(tP, "pop", "wood glows amber, PCBs tag", true);
    if (Bs) { S.beat(0.05, "whoosh", "camera pushes in on the bow"); S.beat(tCat, "pop", "catapult tracks light, amber seeps", true); }
    if (Cs) S.beat(tCame, "whoosh", "whole wooden layer lifts away and dissolves", true);
  }

  // ======================================================== c07 apart: PCB wiring through the hull, cut lines, the ship splits into sections
  function apart(S) {
    board(S, { seed: 71, tint: "26,36,46" });
    S.kicker("WHY THE PCBs STAYED", 0.05);
    const CH = root.CarrierHero, M = CH.meta("hulk"), L = M.L, SW = 1640, s = SW / (L + 2 * M.pad), XS = (W - L * s) / 2, DYS = 600, WL = DYS - M.deckY * s;
    const X = (x) => XS + x * s, Y = (y) => WL + y * s, R = rnd(72);
    // wiring network (feet -> px): runs on several decks + risers + island
    let wd = "";
    for (const y of [-46, -36, -26, -16, -6, 4, 13]) { let x = 50 + R() * 30; while (x < 840) { const x2 = Math.min(850, x + 80 + R() * 200); wd += `M${X(x).toFixed(1)} ${Y(y).toFixed(1)} L${X(x2).toFixed(1)} ${Y(y).toFixed(1)} `; x = x2 + 8 + R() * 30; } }
    for (let x = 70; x < 840; x += 34 + R() * 40) { const y0 = -48 + R() * 10, y1 = 4 + R() * 12; wd += `M${X(x).toFixed(1)} ${Y(y0).toFixed(1)} L${X(x).toFixed(1)} ${Y(y1).toFixed(1)} `; }
    for (const y of [-60, -72, -84, -96]) wd += `M${X(476).toFixed(1)} ${Y(y).toFixed(1)} L${X(590).toFixed(1)} ${Y(y).toFixed(1)} `;
    wd += `M${X(500).toFixed(1)} ${Y(-48).toFixed(1)} L${X(500).toFixed(1)} ${Y(-100).toFixed(1)} M${X(560).toFixed(1)} ${Y(-48).toFixed(1)} L${X(560).toFixed(1)} ${Y(-96).toFixed(1)}`;
    const cuts = [185, 365, 545, 725], secs = [[-M.pad, 185], [185, 365], [365, 545], [545, 725], [725, L + M.pad]];
    const ship = CH.svg({ w: SW, paint: "hulk", id: "ap" });
    const wrapCss = `position:absolute;left:0;top:0;width:${W}px;height:${H}px;transform-origin:0 0`;
    const parts = secs.map(([a, b], i) => {
      const w = S.el("div", wrapCss + `;clip-path:inset(0px ${(W - X(b)).toFixed(1)}px 0px ${X(a).toFixed(1)}px)`);
      S.el("div", `position:absolute;left:${XS - M.pad * s}px;top:${WL + (M.sideY0 - M.pad) * s}px`, ship.replace(/id="ap-/g, `id="ap${i}-`).replace(/url\(#ap-/g, `url(#ap${i}-`), w);
      const ws = S.el("div", `position:absolute;left:0;top:0`, `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0;overflow:visible">
        <path d="${wd}" fill="none" stroke="${AMBER}" stroke-width="9" opacity=".5" style="filter:blur(5px)" pathLength="1" stroke-dasharray="1 1" class="wg"/>
        <path d="${wd}" fill="none" stroke="${AMBER}" stroke-width="3" pathLength="1" stroke-dasharray="1 1" class="wc"/></svg>`, w);
      return { w, cx: X((Math.max(a, 0) + Math.min(b, L)) / 2), dx: (i - 2) * 64, dy: [10, -12, 8, -8, 12][i], rot: [-2.4, 1.6, -1.2, 1.8, -2.2][i], ws };
    });
    const cutSv = S.el("div", `position:absolute;inset:0`, `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0">${cuts.map((c, i) =>
      `<path id="ct${i}" d="M${X(c).toFixed(1)} ${Y(-70).toFixed(1)} L${X(c).toFixed(1)} ${Y(34).toFixed(1)}" stroke="${GOLD2}" stroke-width="5" stroke-dasharray="14 10" pathLength="200"/>`).join("")}</svg>`);
    const sparks = [];
    cuts.forEach((c) => { for (let k = 0; k < 18; k++) sparks.push({ e: S.el("div", `position:absolute;left:0;top:0;width:${3 + R() * 4}px;height:${3 + R() * 4}px;border-radius:50%;background:#fff1c8;box-shadow:0 0 8px #ffb347;opacity:0`),
      x: X(c), y: Y(-50 + R() * 80), vx: (R() - 0.5) * 520, vy: -120 - R() * 300 }); });
    const flash = S.el("div", `position:absolute;inset:0;background:#fff3d6;mix-blend-mode:screen;opacity:0;pointer-events:none`);
    const tRip = S.w("ripping", 0.78), tTake = S.w("taking", 2.5), tApart = S.w("apart", 3.36);
    S.tag(`<span style="color:${AMBER}">PCBs</span> IN THE WIRING · EVERY DECK`, 520, 250, tRip, { col: AMBER, fs: 50 });
    S.tag("= TAKING THE SHIP APART", 640, 790, tApart + 0.2, { fs: 54 });
    S.on((t) => {
      const draw = oCub(ramp(t, 0.1, 1.1)), pulse = 1 + 0.6 * Math.exp(-Math.max(0, t - tRip) * 3) * (t > tRip ? 1 : 0);
      const k = oBack(ramp(t, tApart - 0.12, 0.55));
      parts.forEach((p) => {
        p.ws.querySelectorAll("path").forEach((pa) => { pa.setAttribute("stroke-dashoffset", (1 - draw).toFixed(4)); });
        p.ws.style.opacity = Math.min(1, 0.85 * pulse).toFixed(3); p.ws.style.filter = `brightness(${pulse.toFixed(2)})`;
        p.w.style.transform = `translate(${(p.dx * k).toFixed(1)}px,${(p.dy * k).toFixed(1)}px) rotate(${(p.rot * k).toFixed(3)}deg)`;
        p.w.style.transformOrigin = `${p.cx.toFixed(0)}px ${DYS}px`;
      });
      cuts.forEach((c, i) => { const e = cutSv.querySelector("#ct" + i), kk = oCub(ramp(t, tTake + i * 0.08, 0.35));
        e.setAttribute("stroke-dashoffset", (200 * (1 - kk)).toFixed(1)); e.setAttribute("opacity", (kk * (1 - sm(ramp(t, tApart, 0.3)))).toFixed(3)); });
      sparks.forEach((p) => { const a = t - tApart; if (a < 0 || a > 0.9) { p.e.style.opacity = 0; return; }
        p.e.style.opacity = (1 - a / 0.9).toFixed(3); p.e.style.transform = `translate(${(p.x + p.vx * a).toFixed(1)}px,${(p.y + p.vy * a + 500 * a * a).toFixed(1)}px)`; });
      flash.style.opacity = t > tApart && t < tApart + 0.25 ? (0.2 * (1 - (t - tApart) / 0.25)).toFixed(3) : 0;
    });
    S.beat(0.1, "whoosh", "wiring draws through the hull"); S.beat(tRip, "pop", "PCBs IN THE WIRING tag, wiring pulses");
    S.beat(tTake, "scrape", "cut lines draw"); S.beat(tApart, "impact", "ship splits into five sections + sparks", true);
  }

  // ======================================================== c05 ShipSink (kit/ship/sinking): a = wide descent + bow due south, b = touchdown 212 ft
  // c05 hero a (re-cut, step 3): the narration says she has ALREADY settled ("She settled upright on the bottom, her bow pointing
  // due south"), so this shot is a plan view of the wreck at rest on the sand, seen from above: no descent on screen. The side-view
  // descent + touchdown on "twelve" stays in stage b.
  function sinkPlan(S) {
    const R = rnd(17), tUp = S.w("upright", 0.28), tS = S.w("south", 3.4);
    S.el("div", `position:absolute;inset:0;background:radial-gradient(ellipse at 52% 46%,#5b6a62 0%,#3c4a47 38%,#1e2a2d 72%,#0b1418 100%)`);
    const cam = S.el("div", `position:absolute;left:0;top:0;width:${W}px;height:${H}px;transform-origin:56% 50%`);
    // sand ripples + specks
    let rip = ""; for (let k = 0; k < 26; k++) { const y = -60 + k * 46 + R() * 10; rip += `<path d="M-100 ${y} Q 300 ${y - 18} 700 ${y} T 1500 ${y} T 2300 ${y}" stroke="rgba(214,205,170,${(.05 + R() * .05).toFixed(3)})" stroke-width="${(3 + R() * 5).toFixed(1)}" fill="none"/>`; }
    for (let k = 0; k < 260; k++) rip += `<circle cx="${(R() * W).toFixed(0)}" cy="${(R() * H).toFixed(0)}" r="${(1 + R() * 3).toFixed(1)}" fill="rgba(${R() < .5 ? "20,26,24" : "190,184,150"},${(.15 + R() * .25).toFixed(2)})"/>`;
    S.el("div", `position:absolute;inset:-40px`, `<svg width="${W + 80}" height="${H + 80}" style="display:block">${rip}</svg>`, cam);
    // the hull, bow DOWN (= south, north up): side view's +x (bow) rotated 90 deg clockwise; port side faces east
    const SL = 860, CX = 1080, CY = 520;
    const shadow = S.el("div", `position:absolute;left:${CX - 95}px;top:${CY - SL / 2 + 30}px;width:190px;height:${SL}px;border-radius:40%;background:rgba(5,10,10,.55);filter:blur(26px)`, null, cam);
    const hull = S.el("div", `position:absolute;left:${CX}px;top:${CY}px;transform:translate(-50%,-50%) rotate(90deg)`,
      root.ShipKit.svg("carrier", "top", { w: SL, paint: "livery", keyline: 2 }), cam);
    hull.style.filter = "saturate(.75) brightness(.92)";
    // silt still hanging round the hull after she settled (fades), caustic light over everything
    const silt = []; for (let k = 0; k < 18; k++) { const a = R() * Math.PI * 2, rr = 0.5 + R() * 0.5;
      silt.push({ e: S.el("div", `position:absolute;left:0;top:0;width:${160 + R() * 160}px;height:${160 + R() * 160}px;border-radius:50%;background:radial-gradient(circle,rgba(200,192,160,.32),rgba(200,192,160,0) 70%);filter:blur(8px)`, null, cam),
        x: CX + Math.cos(a) * 150 * rr - 120, y: CY + Math.sin(a) * (SL / 2) * rr - 120, ph: R() * 6 }); }
    const caus = []; for (let k = 0; k < 9; k++) caus.push({ e: S.el("div", `position:absolute;left:0;top:0;width:520px;height:340px;border-radius:50%;mix-blend-mode:screen;filter:blur(30px);
      background:radial-gradient(ellipse,rgba(190,235,225,.16),rgba(190,235,225,0) 70%)`), x: R() * W - 260, y: R() * H - 170, ph: R() * 6 });
    S.el("div", `position:absolute;inset:0;background:rgba(10,40,48,.28);mix-blend-mode:multiply`);
    // compass (north up), left side, clear of the top-right corner and the bottom 10 %
    const cmp = S.el("div", `position:absolute;left:150px;top:300px;width:300px;height:300px;opacity:0;transform-origin:50% 50%`,
      `<svg width="300" height="300" viewBox="-150 -150 300 300"><circle r="118" fill="rgba(14,13,10,.72)" stroke="${CREAM}" stroke-width="4" opacity=".9"/>
       <path d="M0 -104 L16 -10 L0 0 L-16 -10 Z" fill="rgba(247,243,234,.55)"/><path d="M0 104 L16 10 L0 0 L-16 10 Z" fill="${GOLD2}"/>
       <path d="M-104 0 L-10 -10 L0 0 L-10 10 Z M104 0 L10 -10 L0 0 L10 10 Z" fill="rgba(247,243,234,.3)"/>
       <text x="0" y="-122" fill="${CREAM}" font-size="40" font-weight="700" text-anchor="middle" dominant-baseline="auto" font-family="Oswald">N</text>
       <text x="0" y="150" fill="${GOLD2}" font-size="40" font-weight="700" text-anchor="middle" font-family="Oswald">S</text></svg>`);
    S.pop(cmp, Math.max(0.15, tUp - 0.1), {});
    // arrow along the hull to the bow, then the tag
    const arr = S.el("div", `position:absolute;left:${CX + 190}px;top:${CY - 300}px;width:12px;height:0;background:${GOLD2};box-shadow:0 0 18px rgba(230,211,163,.6)`);
    const head = S.el("div", `position:absolute;left:${CX + 172}px;top:0;width:0;height:0;border-left:24px solid transparent;border-right:24px solid transparent;border-top:36px solid ${GOLD2};opacity:0`);
    S.on((t) => { const k = oCub(ramp(t, tS - 0.7, 0.6)); arr.style.height = (k * 640).toFixed(0) + "px"; head.style.top = (CY - 300 + k * 640).toFixed(0) + "px"; head.style.opacity = k > 0.02 ? 1 : 0; });
    S.tag("UPRIGHT ON THE SEABED", 1330, 360, tUp + 0.1, {});
    S.tag(`BOW <span style="color:${GOLD2}">→ DUE SOUTH</span>`, 1330, 700, tS, {});
    S.on((t) => {
      cam.style.transform = `scale(${lerp(1.0, 1.06, sm(t / S.D)).toFixed(4)})`;
      silt.forEach((p) => { p.e.style.opacity = (0.9 * (1 - sm(ramp(t, 0, S.D * 0.9)))).toFixed(3);
        p.e.style.transform = `translate(${(p.x + 14 * Math.sin(t * .5 + p.ph)).toFixed(1)}px,${(p.y + 10 * Math.cos(t * .4 + p.ph)).toFixed(1)}px) scale(${(1 + t * 0.08).toFixed(3)})`; });
      caus.forEach((c) => { c.e.style.transform = `translate(${(c.x + 60 * Math.sin(t * .7 + c.ph)).toFixed(1)}px,${(c.y + 40 * Math.cos(t * .6 + c.ph)).toFixed(1)}px)`; });
    });
    S.kicker("17 MAY 2006 · SEEN FROM ABOVE", 0.05, "THE WRECK AT REST", 0.25);
    S.beat(tUp + 0.1, "pop", "UPRIGHT ON THE SEABED tag (wreck already at rest)");
    S.beat(tS, "pop", "BOW → DUE SOUTH tag + arrow to the bow", true);
    return finish(S, { vig: 48 });
  }
  function sink(S, stage) {
    if (stage === "a") return sinkPlan(S);
    const SC = root.SCENES, A = SC["c05_hero_a"], B = SC["c05_hero_b"];
    const wB = (p, d) => { const x = B.words.find((w) => norm(w.w) === p && w.t > -0.1); return x ? x.t : d; };
    const off = stage === "b" ? A.shot_dur : 0, D = A.shot_dur + B.dur, tLand = A.shot_dur + wB("twelve", 0.94);
    // tune landAt so the hull touches on "twelve" (the kit lands ~ on landAt*D; search it)
    let lo = 0.3, hi = 0.98, Sk = null;
    const mk = (la) => root.ShipSink(S.stage, { ship: "carrier", depthFt: 212, duration: D, mode: "stern", pitch: 9, charges: false, sinkStart: 0.02, landAt: la, sonar: true, markers: false, settleFt: 0 });
    for (let it = 0; it < 18; it++) { const m = (lo + hi) / 2; Sk = mk(m); if (Sk.landT < tLand) lo = m; else hi = m; }
    Sk = mk((lo + hi) / 2);
    // compass: in this side view the bow (right) points due south
    const tS = stage === "a" ? S.w("south", 3.4) : -9;
    const cmp = S.el("div", `position:absolute;left:860px;top:150px;display:flex;align-items:center;gap:22px;opacity:0;transform-origin:0 50%;padding:10px 26px 12px 16px;
      background:rgba(14,13,10,.86);border-left:6px solid ${GOLD};box-shadow:0 10px 26px rgba(0,0,0,.55)`,
      `<svg width="96" height="96" viewBox="-50 -50 100 100"><circle r="44" fill="none" stroke="${CREAM}" stroke-width="4" opacity=".7"/>
        <path d="M0 -14 L48 0 L0 14 Z" fill="${GOLD2}"/><path d="M0 -10 L-36 0 L0 10 Z" fill="rgba(247,243,234,.45)"/><circle r="6" fill="${CREAM}"/></svg>
       <span style="font-size:48px;font-weight:700;color:${CREAM};letter-spacing:.05em;white-space:nowrap">BOW <span style="color:${GOLD2}">→ DUE SOUTH</span></span>`);
    if (stage === "a") S.pop(cmp, tS, {}); else cmp.style.opacity = 1;
    if (stage === "b") S.on((t) => { cmp.style.opacity = (1 - ramp(t, 0.3, 0.4)).toFixed(3); });
    const R0 = S.fns.slice(); S.fns.length = 0;
    S.on((t) => Sk.render(Math.min(D, t + off))); R0.forEach((f) => S.on(f));
    const gsap = root.gsap, tl = gsap.timeline({ paused: true }), px = { t: 0 }, render = (t) => S.fns.forEach((fn) => fn(t));
    tl.to(px, { t: S.D, duration: S.D, ease: "none", onUpdate: () => render(px.t) }, 0); render(0);
    if (stage === "a") { S.beat(tS, "pop", "compass tag BOW → DUE SOUTH", true); S.beat(0.05, "whoosh", "hull already sinking, stern first"); }
    else S.beat(Sk.landT - off, "land", "touchdown: gauge lands ON THE SEABED 212 FT, silt puff", true);
    const cues = Sk.cues.map((c) => ({ t: +(c.t - off).toFixed(3), kind: c.kind })).filter((c) => c.t >= -0.5 && c.t <= S.D);
    return { tl, duration: S.D, beats: S.beats.sort((a, b) => a.t - b.t), cues, missing: S.missing, landT: Sk.landT - off };
  }
  // ======================================================== c07 reef cross-sections: the hulk upright on the seabed (FWC depths)
  // settle (sinks ~10 ft into the sediment), funnel (casing torn away, late 2009), depths a/b/d (deck 145-150 ft, sport-diving limit),
  // today (the only carrier ever reefed: growth, fish, light shafts); fallbacks: wreck2008 (growth 2006 -> July 2008), depths_c
  // (island top 84 ft), divers (descending to the island).
  const wcol = (d) => { const st = [[0, [44, 104, 112]], [60, [26, 72, 86]], [200, [13, 42, 58]], [800, [8, 24, 40]]];
    for (let k = 1; k < st.length; k++) if (d <= st[k][0]) { const a = st[k - 1], b = st[k], q = (d - a[0]) / (b[0] - a[0]); return a[1].map((v, i) => Math.round(lerp(v, b[1][i], q))); }
    return st[st.length - 1][1]; };
  const DIVER = (w = 60) => `<svg width="${w}" height="${w * 0.45}" viewBox="-40 -18 80 36" style="overflow:visible;display:block">
    <path d="M-34 -2 L-46 -12 L-44 6 Z" fill="#1d2c33"/><path d="M-34 4 L-48 2 L-40 14 Z" fill="#1d2c33"/>
    <rect x="-34" y="-7" width="54" height="14" rx="7" fill="#22343c"/><rect x="-22" y="-15" width="34" height="9" rx="4.5" fill="#c9b48a"/>
    <circle cx="27" cy="-1" r="8" fill="#22343c"/><rect x="25" y="-6" width="9" height="7" rx="2" fill="#8fd0c6"/>
    <path d="M10 6 L20 16 M4 6 L12 17" stroke="#22343c" stroke-width="4" stroke-linecap="round"/></svg>`;
  function reef(S, stage) {
    const CH = root.CarrierHero, M = CH.meta("hulk"), L = M.L, s0 = 2, SEA = 212;
    const WX = (x) => (x + 700) * s0, WY = (d) => (d + 320) * s0, worldW = 2900 * s0, worldH = 800 * s0;
    const w = (p, d, o = 0) => S.w(p, d) + o;
    // ---- per-stage plan: camera keys [t, x, d, z], settle(t) ft, growth(t), storm(t), fish count
    const ease = (keys) => (t) => { if (t <= keys[0][0]) return keys[0].slice(1); for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) { const a = keys[i - 1], b = keys[i], k = sm((t - a[0]) / (b[0] - a[0])); return [1, 2, 3].map((j) => lerp(a[j], b[j], k)); } return keys[keys.length - 1].slice(1); };
    let P;
    if (stage === "settle") { const tSt = w("storms", 2.18), tPu = w("pushed", 2.82), tTen = w("ten", 3.58);
      P = { cam: ease([[0, 470, 140, 1.15], [tSt, 455, 196, 2.5], [S.D, 450, 198, 2.6]]), settle: (t) => 10 * oCub(ramp(t, tPu - 0.25, tTen - tPu + 0.25)),
        storm: (t) => sm(ramp(t, tSt - 0.3, 0.5)) * (1 - 0.6 * sm(ramp(t, tTen + 0.6, 1))), growth: () => 0.35, fish: 6, tTen, tSt, tHalf: w("half", 1.04) }; }
    else if (stage === "funnel") { const tTore = w("tore", 2.26);
      P = { cam: ease([[0, 526, 112, 2.7], [S.D, 520, 106, 3.1]]), settle: () => 10, storm: (t) => sm(ramp(t, w("storm", 1.89) - 0.5, 0.5)) * (1 - sm(ramp(t, tTore + 1.2, 1))),
        growth: () => 0.45, fish: 6, tTore, tLate: w("late", 0.3), tCasing: w("casing", 3.11) }; }
    else if (stage === "depths_a") P = { cam: ease([[0, 430, 132, 1.15], [S.D, 440, 136, 1.25]]), settle: () => 10, growth: () => 0.7, fish: 14, tDeck: w("forty", 3.31) };
    else if (stage === "depths_b") P = { cam: ease([[0, 440, 136, 1.25], [1.2, 330, 150, 2.3], [S.D, 320, 150, 2.4]]), settle: () => 10, growth: () => 0.7, fish: 14, tFifty: w("fifty", 1.36) };
    else if (stage === "depths_d") P = { cam: ease([[0, 360, 148, 2.4], [S.D, 390, 146, 2.0]]), settle: () => 10, growth: () => 0.7, fish: 14, tLim: w("limits", 2.32) };
    else if (stage === "depths_c") P = { cam: ease([[0, 560, 104, 2.3], [S.D, 548, 98, 2.6]]), settle: () => 10, growth: () => 0.8, fish: 16, tIsl: w("eighty", 1.56) };
    else if (stage === "divers") P = { cam: ease([[0, 545, 52, 3.0], [S.D, 545, 60, 3.2]]), settle: () => 10, growth: () => 0.85, fish: 14, tDiv: w("divers", 0.2) };
    else if (stage === "today") P = { cam: ease([[0, 470, 130, 1.18], [S.D, 470, 134, 1.28]]), settle: () => 10, growth: () => 1, fish: 46, tOnly: w("only", 0.72) };
    else if (stage === "wreck2008") { const tSank = w("sank", 2.8);
      P = { cam: ease([[0, 450, 132, 1.18], [S.D, 480, 140, 1.4]]), settle: () => 10, growth: (t) => lerp(0.08, 1, sm(ramp(t, 0.15, tSank - 0.15))), fish: 40, tSank }; }
    else throw new Error("reef stage " + stage);
    P.storm = P.storm || (() => 0);
    // ---- world
    const world = S.el("div", `position:absolute;left:0;top:0;width:${worldW}px;height:${worldH}px;transform-origin:0 0`);
    S.el("div", `position:absolute;left:0;top:0;width:${worldW}px;height:${WY(0)}px;background:linear-gradient(180deg,#0e171d 0%,#1d2a32 60%,#4a5960 100%)`, null, world);
    const grad = [0, 0.15, 0.4, 0.75, 1].map((q) => `rgb(${wcol(q * 260).join(",")}) ${(q * 100).toFixed(0)}%`).join(",");
    S.el("div", `position:absolute;left:0;top:${WY(0)}px;width:${worldW}px;height:${WY(260) - WY(0)}px;background:linear-gradient(180deg,${grad})`, null, world);
    S.el("div", `position:absolute;left:0;top:${WY(260)}px;width:${worldW}px;height:${worldH - WY(260)}px;background:rgb(${wcol(260).join(",")})`, null, world);
    const R = rnd(81), rays = [];
    for (let k = 0; k < 16; k++) { const x = WX(-500 + k * 110 + R() * 60), wd = 30 + R() * 110;
      rays.push(S.el("div", `position:absolute;left:${x}px;top:${WY(0)}px;width:${wd}px;height:${(200 + R() * 80) * s0}px;transform-origin:50% 0;transform:skewX(${-16 + R() * 10}deg);mix-blend-mode:screen;
        background:linear-gradient(180deg,rgba(170,225,215,${0.13 + R() * 0.08}) 0%,rgba(170,225,215,.04) 60%,rgba(170,225,215,0) 100%);filter:blur(8px)`, null, world)); }
    // the hulk (CarrierHero), settled: waterline datum at depth SEA + settle - draught
    const svgW = s0 * (L + 2 * M.pad), h0 = SEA - M.draught;
    const shipBox = S.el("div", `position:absolute;left:${WX(-M.pad)}px;top:${WY(h0 + M.sideY0 - M.pad)}px;width:${svgW}px;filter:drop-shadow(0 6px 10px rgba(0,0,0,.35))`, CH.svg({ w: svgW, paint: "hulk", id: "rf" }), world);
    const vb = [-M.pad, M.sideY0 - M.pad, L + 2 * M.pad, (M.sideY1 - M.sideY0) + 2 * M.pad], svgH = svgW * vb[3] / vb[2];
    // growth + funnel casing overlay, same viewBox (feet, ship coords)
    const yF = M.deckY, top = M.islandTopY, ix = M.islandX[0];
    const casePoly = [[ix + 8, yF - 26], [ix + 52, yF - 26], [ix + 46, top + 4], [ix + 40, top], [ix + 4, top], [ix + 2, top + 5]].map((p) => p.join(" ")).join(" L");
    let blobs = "", bl = [];
    const GC = ["#9a6a4a", "#8a5a6a", "#6a7d58", "#a98a5a", "#6e6688", "#8f7b62"];
    const addB = (x, y, r) => { bl.push({ x, y, r, th: R() * 0.9, c: GC[Math.floor(R() * GC.length)] }); };
    for (let k = 0; k < 260; k++) addB(5 + R() * 900, yF - R() * 1.6, 0.5 + R() * 1.5);                        // flight deck
    for (let k = 0; k < 90; k++) { const x = ix + 4 + R() * (M.islandX[1] - ix - 8); addB(x, yF - 14 - R() * 32, 0.4 + R() * 1.1); }   // island
    for (let k = 0; k < 120; k++) addB(40 + R() * 800, yF + 3 + R() * 40, 0.4 + R() * 1.0);                    // hull side
    for (let k = 0; k < 26; k++) addB(ix + 6 + R() * 40, top + R() * 1.5, 0.5 + R() * 1.1);
    blobs = bl.map((b, i) => `<ellipse id="gb${i}" cx="${b.x.toFixed(1)}" cy="${b.y.toFixed(1)}" rx="${(b.r * 1.3).toFixed(2)}" ry="${b.r.toFixed(2)}" fill="${b.c}" opacity="0"/>`).join("");
    let whips = ""; for (let k = 0; k < 40; k++) { const x = 20 + R() * 880, hh = 3 + R() * 8; whips += `<path class="wh" data-th="${(R() * 0.8).toFixed(2)}" d="M${x.toFixed(1)} ${yF} q${(R() - .5) * 3} ${-hh / 2} ${(R() - .5) * 4} ${-hh}" stroke="${GC[k % 6]}" stroke-width=".7" fill="none" opacity="0"/>`; }
    const bands = [0, 1, 2, 3].map((i) => { const y0 = top + i * (yF - 26 - top) / 4, y1 = top + (i + 1) * (yF - 26 - top) / 4;
      return `<g id="cb${i}"><path d="M${ix} ${y0.toFixed(2)} L${ix + 54} ${y0.toFixed(2)} L${ix + 54} ${y1.toFixed(2)} L${ix} ${y1.toFixed(2)} Z" fill="url(#rfc-g)" clip-path="url(#rfc-clip)"/>
        <path d="M${ix} ${y1.toFixed(2)} L${ix + 54} ${y1.toFixed(2)}" stroke="#2a2826" stroke-width=".35" clip-path="url(#rfc-clip)"/></g>`; }).join("");
    const over = S.el("div", `position:absolute;left:0;top:0`, `<svg width="${svgW.toFixed(1)}" height="${svgH.toFixed(1)}" viewBox="${vb.join(" ")}" style="position:absolute;left:0;top:0;overflow:visible">
      <defs><linearGradient id="rfc-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a857b"/><stop offset="1" stop-color="#57534c"/></linearGradient>
        <clipPath id="rfc-clip"><path d="M${casePoly} Z"/></clipPath><linearGradient id="rfc-in" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#121110"/><stop offset=".5" stop-color="#2b2723"/><stop offset="1" stop-color="#0d0c0b"/></linearGradient></defs>
      <g id="caseIn" opacity="0"><path d="M${casePoly} Z" fill="url(#rfc-in)"/>
        ${[12, 24, 36].map((x) => `<rect x="${ix + x}" y="${top + 2}" width="7" height="${yF - 26 - top - 2}" rx="3" fill="#4a423a"/><rect x="${ix + x + 1}" y="${top + 2}" width="1.5" height="${yF - 26 - top - 2}" fill="#7a6c5c"/>`).join("")}
        ${[0.25, 0.5, 0.75].map((k) => `<path d="M${ix + 3} ${(top + k * (yF - 26 - top)).toFixed(2)} L${ix + 50} ${(top + k * (yF - 26 - top)).toFixed(2)}" stroke="#5a5048" stroke-width=".8"/>`).join("")}</g>
      <g id="caseOut" opacity="0">${bands}</g>${whips}${blobs}</svg>`, shipBox);
    const gbs = bl.map((_, i) => over.querySelector("#gb" + i)), whs = [...over.querySelectorAll(".wh")];
    const caseIn = over.querySelector("#caseIn"), caseOut = over.querySelector("#caseOut"), cbs = [0, 1, 2, 3].map((i) => over.querySelector("#cb" + i));
    // seabed in front of the hull bottom (cross-section): the settled keel disappears into the sediment
    let bed = `M0 ${WY(SEA) + 4}`; for (let x = 0; x <= worldW; x += 50) bed += ` L${x} ${(WY(SEA) + 4 + 3 * Math.sin(x / 170) + 2 * Math.sin(x / 53)).toFixed(1)}`;
    const bedTop = bed; bed += ` L${worldW} ${worldH} L0 ${worldH} Z`;
    let layers = ""; for (let k = 1; k < 9; k++) { let d = `M0 ${WY(SEA) + 6 + k * 26}`; for (let x = 0; x <= worldW; x += 80) d += ` L${x} ${(WY(SEA) + 6 + k * 26 + 5 * Math.sin(x / (140 + k * 30) + k)).toFixed(1)}`; layers += `<path d="${d}" fill="none" stroke="rgba(30,24,16,0.45)" stroke-width="2" stroke-dasharray="${10 + k * 3} ${6 + k}"/>`; }
    let rocks = ""; for (let k = 0; k < 60; k++) { const x = R() * worldW, r = 3 + R() * 7; rocks += `<ellipse cx="${x.toFixed(0)}" cy="${(WY(SEA) + 6 + 3 * Math.sin(x / 170)).toFixed(0)}" rx="${(r * 1.6).toFixed(1)}" ry="${r.toFixed(1)}" fill="#4a4131"/>`; }
    S.el("div", `position:absolute;left:0;top:0`, `<svg width="${worldW}" height="${worldH}" style="position:absolute;left:0;top:0"><defs><linearGradient id="rsand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8c7a58"/><stop offset="0.1" stop-color="#6b5c43"/><stop offset="1" stop-color="#241f18"/></linearGradient></defs>
      <path d="${bed}" fill="url(#rsand)"/>${layers}${rocks}<path d="${bedTop}" fill="none" stroke="#b9a57c" stroke-width="2.5" opacity="0.8"/></svg>`, world);
    // fish (world): schools orbiting the island / over the deck
    const fish = [];
    for (let k = 0; k < P.fish; k++) { const red = R() < 0.3, len = (7 + R() * 7) * s0;
      fish.push({ e: S.el("div", `position:absolute;left:0;top:0;opacity:.92`, FISH(red ? "#c86a5c" : R() < 0.5 ? "#9fb0b6" : "#c8b98e", len, { rim: "rgba(5,10,14,.6)" }), world),
        cx: 300 + R() * 420, cd: 70 + R() * 70, rx: 30 + R() * 160, ry: 4 + R() * 14, sp: (0.12 + R() * 0.2) * (R() < 0.5 ? 1 : -1), ph: R() * 6.28, len, th: R() * 0.8 }); }
    // water tint in front (depth haze)
    S.el("div", `position:absolute;left:0;top:${WY(0)}px;width:${worldW}px;height:${WY(SEA + 60) - WY(0)}px;background:linear-gradient(180deg,rgba(${wcol(0).join(",")},.08),rgba(${wcol(SEA).join(",")},.38))`, null, world);
    // divers (fallback)
    const divers = stage === "divers" ? [0, 1, 2].map((i) => ({ e: S.el("div", `position:absolute;left:0;top:0`, DIVER(8 * s0 * (i ? 0.9 : 1) * 1.6), world), x: 500 + i * 34, d0: -6 - i * 6, d1: 70 + i * 4, t0: P.tDiv + i * 0.18 })) : [];
    const bub = []; if (divers.length) for (let k = 0; k < 36; k++) bub.push({ e: S.el("div", `position:absolute;left:0;top:0;width:6px;height:6px;border-radius:50%;border:1.5px solid rgba(220,240,240,.8);opacity:0`, null, world), i: k % 3, ph: R(), sp: 0.5 + R() * 0.6 });
    // ---- screen space: snow, storm streaks, ruler + markers
    const snow = []; for (let k = 0; k < 90; k++) { const near = k % 4 === 0; snow.push({ e: S.el("div", `position:absolute;left:0;top:0;width:${near ? 4 : 2}px;height:${near ? 4 : 2}px;border-radius:50%;background:rgba(220,235,230,${(near ? .35 : .15) + R() * .3})`), x: R() * W, y: R() * H, v: 8 + R() * 14, ph: R() * 6 }); }
    const streaks = []; for (let k = 0; k < 34; k++) streaks.push({ e: S.el("div", `position:absolute;left:0;top:0;width:${120 + R() * 260}px;height:${2 + R() * 2}px;border-radius:2px;background:linear-gradient(90deg,transparent,rgba(210,230,225,.55),transparent);opacity:0`), y: R() * H, v: 900 + R() * 900, ph: R() });
    const clouds = []; for (let k = 0; k < 14; k++) clouds.push({ e: S.el("div", `position:absolute;left:0;top:0;width:${300 + R() * 300}px;height:${90 + R() * 80}px;border-radius:50%;background:radial-gradient(ellipse,rgba(150,128,92,.6),rgba(150,128,92,0) 70%);filter:blur(6px);opacity:0`), x: R() * W, v: 300 + R() * 300, dy: R() });
    const ov = S.el("div", `position:absolute;inset:0;pointer-events:none`, `<svg id="rov" width="${W}" height="${H}" style="position:absolute;left:0;top:0;font-family:Oswald;font-weight:500;filter:drop-shadow(0 2px 6px rgba(0,0,0,.7))"></svg>`);
    const rov = ov.querySelector("#rov");
    // markers: {d, label, val, t0, x2 (ft, where the dashed line stops)}
    const marks = [{ d: SEA, label: "SEABED", val: "212 FT", t0: stage === "settle" ? 99 : -9, x2: 2000 }];
    const bigTags = [];
    if (stage === "settle") { bigTags.push(S.tag("WITHIN ≈ 2½ YEARS", 760, 170, P.tHalf, { fs: 50, out: P.tSt + 0.1 }));
      bigTags.push(S.tag("STORMS PUSHED HER ≈ 10 FT INTO THE SEABED", 430, 170, P.tTen + 0.05, { fs: 50 })); }
    if (stage === "funnel") { bigTags.push(S.tag("LATE 2009 · A STORM", 760, 170, P.tLate, { fs: 50 }));
      bigTags.push(S.tag("FUNNEL CASING TORN AWAY", 680, 800, P.tCasing, { fs: 52, col: AMBER })); }
    if (stage === "depths_a" || stage === "depths_b" || stage === "depths_d") marks.push({ d: 147, label: "FLIGHT DECK", val: "≈145–150 FT", t0: stage === "depths_a" ? P.tDeck : -9, x2: 30, below: stage === "depths_d" });
    if (stage === "depths_c" || stage === "divers") marks.push({ d: 84, label: "ISLAND TOP", val: "84 FT", t0: stage === "depths_c" ? P.tIsl : -9, x2: ix + 4 });
    if (stage === "today") bigTags.push(S.tag("THE ONLY CARRIER EVER REEFED", 560, 170, P.tOnly, { fs: 60 }));
    if (stage === "wreck2008") bigTags.push(S.tag("THE WRECK · JULY 2008", 650, 170, P.tSank, { fs: 56 }));
    if (stage === "divers") bigTags.push(S.tag("SPORT DIVERS · THE TOP OF THE ISLAND", 560, 170, P.tDiv + 0.3, { fs: 50 }));
    const yearEl = stage === "wreck2008" ? S.el("div", `position:absolute;left:96px;top:110px;font-size:84px;font-weight:700;color:${CREAM};letter-spacing:.02em;text-shadow:0 3px 18px rgba(0,0,0,.75)`) : null;
    S.kicker({ settle: "THE WRECK · 2006 → 2008", funnel: "THE WRECK · 2009", depths_a: "THE WRECK TODAY", depths_b: "THE WRECK TODAY", depths_d: "THE WRECK TODAY", depths_c: "THE WRECK TODAY",
      divers: "THE WRECK · DIVERS", today: "THE WRECK TODAY", wreck2008: "A REEF GROWS" }[stage], 0.05);
    const RX = 150;
    S.on((t) => {
      const [cx, cd, z] = P.cam(t), stl = P.settle(t), storm = P.storm(t);
      const shake = storm > 0.05 ? storm * 3 * Math.sin(t * 37) : 0;
      const tx = W / 2 - WX(cx) * z, ty = H / 2 - WY(cd) * z + shake;
      world.style.transform = `translate(${tx.toFixed(2)}px,${ty.toFixed(2)}px) scale(${z.toFixed(4)})`;
      const SX = (x) => WX(x) * z + tx, SYd = (d) => WY(d) * z + ty;
      shipBox.style.transform = `translateY(${(stl * s0).toFixed(2)}px)`;
      rays.forEach((r, i) => { r.style.opacity = (0.7 + 0.3 * Math.sin(t * 0.9 + i * 1.7)).toFixed(3); });
      const g = P.growth(t);
      gbs.forEach((e, i) => { const k = sm((g - bl[i].th) / 0.12); e.setAttribute("opacity", (0.72 * k).toFixed(3)); e.setAttribute("transform", `translate(${bl[i].x} ${bl[i].y}) scale(${k.toFixed(3)}) translate(${-bl[i].x} ${-bl[i].y})`); });
      whs.forEach((e) => { const k = sm((g - +e.dataset.th) / 0.15); e.setAttribute("opacity", (0.8 * k).toFixed(3)); });
      // funnel casing: hidden overlay until "tore", then four bands peel off aft and up, the dark uptakes show
      if (stage === "funnel") { caseIn.setAttribute("opacity", 1); caseOut.setAttribute("opacity", 1);
        cbs.forEach((e, i) => { const a = t - P.tTore - (3 - i) * 0.07; const k = a < 0 ? 0 : a;
          const dx = -k * (34 + i * 10) - 6 * k * k, dy = -k * (8 - i * 3) + 14 * k * k, rot = -k * (55 + i * 30);
          e.setAttribute("transform", `translate(${dx.toFixed(2)} ${dy.toFixed(2)}) rotate(${rot.toFixed(1)} ${ix + 27} ${(top + (i + 0.5) * (yF - 26 - top) / 4).toFixed(1)})`);
          e.setAttribute("opacity", (1 - ramp(a, 0.5, 0.9)).toFixed(3)); }); }
      fish.forEach((f) => { const a = f.ph + f.sp * t * 2, x = f.cx + f.rx * Math.cos(a), d = f.cd + f.ry * Math.sin(a * 2), vx = -Math.sin(a) * f.sp;
        const vis = stage === "wreck2008" ? sm((g - f.th) / 0.2) : 1;
        f.e.style.opacity = (0.92 * vis).toFixed(3); f.e.style.transform = `translate(${(WX(x) - f.len / 2).toFixed(1)}px,${(WY(d) - f.len / 4).toFixed(1)}px) scaleX(${vx >= 0 ? 1 : -1})`; });
      divers.forEach((dv, i) => { const k = sm(ramp(t, dv.t0, 2.2)), d = lerp(dv.d0, dv.d1, k), kick = Math.sin(t * 7 + i);
        dv.e.style.transform = `translate(${WX(dv.x + 3 * Math.sin(t + i)).toFixed(1)}px,${WY(d).toFixed(1)}px) rotate(${(lerp(70, 18, k) + 4 * kick).toFixed(1)}deg)`; });
      bub.forEach((b) => { const dv = divers[b.i]; if (!dv) return; const a = ((t * b.sp + b.ph) % 1), k = sm(ramp(t, dv.t0, 2.2)), d = lerp(dv.d0, dv.d1, k) - a * 26;
        b.e.style.opacity = t < dv.t0 ? 0 : (Math.sin(a * Math.PI) * 0.8).toFixed(3); b.e.style.transform = `translate(${WX(dv.x + 4 + 2 * Math.sin(a * 9 + b.ph * 6)).toFixed(1)}px,${WY(d).toFixed(1)}px)`; });
      snow.forEach((p) => { const y = ((p.y - p.v * t * 0.4 + p.v * t) % H + H) % H; p.e.style.transform = `translate(${(p.x + 8 * Math.sin(t * 0.7 + p.ph) + storm * 300 * t).toFixed(1) % W}px,${y.toFixed(1)}px)`; });
      streaks.forEach((p) => { const x = ((p.ph * W + p.v * t) % (W + 600)) - 300; p.e.style.opacity = (storm * 0.8).toFixed(3); p.e.style.transform = `translate(${x.toFixed(1)}px,${p.y.toFixed(1)}px)`; });
      const yb = SYd(SEA); clouds.forEach((c) => { const x = ((c.x + c.v * t) % (W + 600)) - 300; c.e.style.opacity = (storm * 0.75).toFixed(3); c.e.style.transform = `translate(${x.toFixed(1)}px,${(yb - 90 - c.dy * 60).toFixed(1)}px)`; });
      // ruler (true scale with the camera), ticks + labels >= 38 px
      const y0 = clamp(SYd(0), 240, 950), y1 = clamp(SYd(SEA + 12), 240, 950), pf = z * s0;
      const step = pf * 10 >= 60 ? 10 : pf * 25 >= 60 ? 25 : 50;
      let o = `<rect x="${RX - 12}" y="${y0 - 10}" width="24" height="${Math.max(0, y1 - y0 + 20)}" rx="12" fill="rgba(11,20,28,.55)" stroke="rgba(247,243,234,.4)" stroke-width="2"/>`;
      for (let d = 0; d <= SEA + 10; d += step) { const y = SYd(d); if (y < 250 || y > 940) continue;
        o += `<line x1="${RX - 32}" y1="${y.toFixed(1)}" x2="${RX - 16}" y2="${y.toFixed(1)}" stroke="rgba(247,243,234,.6)" stroke-width="2"/><text x="${RX - 38}" y="${(y + 13).toFixed(1)}" text-anchor="end" font-size="38" fill="rgba(247,243,234,.82)">${d}</text>`; }
      // markers
      marks.forEach((m) => { const k = ramp(t, m.t0, 0.38); if (k <= 0) return; const y = SYd(m.d + (m.d === SEA ? 0 : 0)); if (y < 180 || y > 950) return;
        const x2 = Math.max(RX + 50, SX(m.x2)), sc = lerp(0.7, 1, oBack(k)), op = sm(k * 1.8), tw = (m.label.length + m.val.length + 2) * 22 + 30;
        o += `<g opacity="${op.toFixed(3)}"><line x1="${RX + 16}" y1="${y.toFixed(1)}" x2="${RX + 44}" y2="${y.toFixed(1)}" stroke="${GOLD}" stroke-width="4"/>
          <line x1="${RX + 44}" y1="${y.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y.toFixed(1)}" stroke="${GOLD}" stroke-width="2.5" stroke-dasharray="8 8" opacity=".85"/>
          <g transform="translate(${RX + 52} ${(m.below ? y + 12 : y - 64).toFixed(1)}) scale(${sc.toFixed(3)})"><rect x="0" y="0" width="${tw}" height="54" fill="rgba(11,16,20,.82)"/><rect x="0" y="0" width="6" height="54" fill="${GOLD}"/>
          <text x="20" y="41" font-size="40" fill="${CREAM}" letter-spacing="2">${m.label} <tspan fill="${GOLD2}" font-weight="700">${m.val}</tspan></text></g></g>`; });
      // stage extras
      if (stage === "settle") { const yk = SYd(SEA), yk2 = SYd(SEA + stl), xr = W / 2 + 260, k = ramp(t, P.tSt + 0.1, 0.4);
        o += `<g opacity="${sm(k).toFixed(3)}"><line x1="${SX(380).toFixed(1)}" y1="${yk.toFixed(1)}" x2="${(xr + 40).toFixed(1)}" y2="${yk.toFixed(1)}" stroke="${CREAM}" stroke-width="3" stroke-dasharray="12 10"/>
          <text x="${(xr - 40).toFixed(1)}" y="${(yk - 14).toFixed(1)}" text-anchor="end" font-size="40" fill="${CREAM}" letter-spacing="2">KEEL, 2006</text></g>`;
        const kb = oCub(ramp(t, P.tTen - 0.05, 0.3));
        if (stl > 0.2) o += `<g><path d="M${(xr - 30).toFixed(1)} ${yk.toFixed(1)} L${(xr + 10).toFixed(1)} ${yk.toFixed(1)} L${(xr + 10).toFixed(1)} ${yk2.toFixed(1)} L${(xr - 30).toFixed(1)} ${yk2.toFixed(1)}" fill="none" stroke="${GOLD2}" stroke-width="6"/>
          <text x="${(xr + 30).toFixed(1)}" y="${((yk + yk2) / 2 + 26).toFixed(1)}" font-size="${(66 * lerp(0.7, 1, oBack(kb))).toFixed(1)}" font-weight="700" fill="${GOLD2}" opacity="${sm(kb * 2).toFixed(3)}">≈ 10 FT</text></g>`; }
      if (stage === "depths_b") { const k = oCub(ramp(t, P.tFifty - 0.3, 0.35)), ya = SYd(145), yb2 = SYd(150);
        o += `<g opacity="${sm(k * 3).toFixed(3)}"><path d="M${RX + 30} ${ya.toFixed(1)} L${RX + 56} ${ya.toFixed(1)} L${RX + 56} ${lerp(ya, yb2, k).toFixed(1)} L${RX + 30} ${lerp(ya, yb2, k).toFixed(1)}" fill="none" stroke="${GOLD2}" stroke-width="7"/>
          <g transform="translate(${RX + 76} ${(ya - 150).toFixed(1)})"><rect x="0" y="0" width="330" height="64" fill="rgba(11,16,20,.82)"/><text x="18" y="50" font-size="52" font-weight="700" fill="${GOLD2}">145–150 FT</text></g></g>`; }
      if (stage === "depths_d") { const k = oCub(ramp(t, P.tLim - 0.35, 0.4)), y = SYd(135), xe = lerp(RX + 20, W, k), yb3 = SYd(SEA);
        o += `<rect x="${RX + 20}" y="${y.toFixed(1)}" width="${(xe - RX - 20).toFixed(1)}" height="${Math.max(0, yb3 - y).toFixed(1)}" fill="rgba(184,67,47,.16)"/>
          <line x1="${RX + 20}" y1="${y.toFixed(1)}" x2="${xe.toFixed(1)}" y2="${y.toFixed(1)}" stroke="#e0563f" stroke-width="5" stroke-dasharray="20 12"/>
          <g opacity="${sm(ramp(t, P.tLim, 0.25)).toFixed(3)}" transform="translate(${W - 760} ${(y - 74).toFixed(1)})"><rect width="640" height="60" fill="rgba(11,16,20,.84)"/><rect width="6" height="60" fill="#e0563f"/>
          <text x="22" y="46" font-size="46" font-weight="700" fill="${CREAM}" letter-spacing="2">SPORT-DIVING LIMIT</text></g>`; }
      rov.innerHTML = o;
      if (yearEl) { const yr = Math.round(lerp(2006, 2008, sm(ramp(t, 0.15, P.tSank - 0.15)))); yearEl.textContent = String(yr);
        yearEl.style.opacity = sm(ramp(t, 0.1, 0.3)).toFixed(3); }
    });
    const mainT = { settle: [P.tTen, "land", "hull settles ~10 ft into the seabed, ≈ 10 FT bracket lands"], funnel: [P.tTore, "impact", "funnel casing tears away (4 panels)"],
      depths_a: [P.tDeck, "pop", "FLIGHT DECK ≈145–150 FT marker lands"], depths_b: [P.tFifty, "land", "145–150 FT bracket lands"],
      depths_d: [P.tLim, "pop", "SPORT-DIVING LIMIT line + band"], depths_c: [P.tIsl, "pop", "ISLAND TOP 84 FT marker lands"],
      divers: [P.tDiv, "whoosh", "divers start their descent"], today: [P.tOnly, "pop", "THE ONLY CARRIER EVER REEFED tag"], wreck2008: [P.tSank, "pop", "growth reaches JULY 2008, tag lands"] }[stage];
    S.beat(mainT[0], mainT[1], mainT[2], true);
    if (stage === "settle") { S.beat(P.tSt, "whoosh", "storm surge starts, camera on the keel"); S.beat(P.tHalf, "pop", "WITHIN ≈ 2½ YEARS tag"); }
    if (stage === "funnel") { S.beat(P.tLate, "pop", "LATE 2009 tag"); S.beat(P.tCasing, "pop", "FUNNEL CASING TORN AWAY tag"); }
  }

  // ======================================================== registry
  const FAM = { sisters, ledger, tally, rounds, pcb, snapper, deck, apart, sink, reef };
  function build(stage, name, cfg) {
    if (!cfg) throw new Error("unknown scene " + name);
    const S = Base(stage, cfg);
    const fam = FAM[cfg.family]; if (!fam) throw new Error("no family " + cfg.family);
    const res = fam(S, cfg.stage);
    if (res && res.tl) return res;          // ShipSink scenes return their own timeline
    return finish(S);
  }
  root.AnimScenes = { build, FAM, Base, finish, board, util: { clamp, lerp, sm, ramp, oCub, oBack, rnd, FISH, SNAPPER, GOLD, GOLD2, CREAM, AMBER, RUST, TEAL, W, H, grainURL } };
})(typeof window !== "undefined" ? window : globalThis);
