// @@KITX (move-3 agent additions, appended after tools/m1_kit.js by tools/m3_build.py; FL.us is the 35-star flag for June 1864)
// OWNER 2026-11-02 "minimize the territory colours": where a fill stays (wide shots only) it is about half as strong and less orange/saturated
(() => { const st = document.createElement("style"); st.textContent = ".wimg.terr, .wimg.ext.terrx { filter: saturate(0.55) opacity(0.5); }"; document.head.appendChild(st); })();
// phrase lookup that never throws: first paragraph (of the scene) whose text has the phrase; null if none (the re-voiced ending may add a paragraph)
const atAny = (phrase, off = 0) => { for (const k of Object.keys(B.T.paras)) if (B.T.text[k].indexOf(phrase) >= 0) return at(k, phrase, off); return null; };
// another basemap (or a world-sized image) as a layer in the world, under the territory layers + overlay. box = [left, top, width, height] in world px
const extImg = (src, t, until, o = {}) => { const el = document.createElement("img"); el.className = "wimg ext"; el.src = src; el.alt = "";
  const [l, tp, w, h] = o.box || [0, 0, 2880, 1620];
  Object.assign(el.style, { position: "absolute", left: l + "px", top: tp + "px", width: w + "px", height: h + "px", maxWidth: "none" });
  if (o.mx) { el.style.mixBlendMode = "multiply"; el.classList.add("terrx"); }
  if (o.under) WORLD.insertBefore(el, document.getElementById("relief")); else { const first = WORLD.querySelector(".terr"); WORLD.insertBefore(el, first || OVL); }
  gsap.set(el, { autoAlpha: t > 0 ? 0 : 1 }); if (t > 0) tl.to(el, { autoAlpha: 1, duration: o.dur || 1.0, ease: "sine.inOut" }, t);
  if (until != null) tl.to(el, { autoAlpha: 0, duration: o.outDur || o.dur || 1.0, ease: "sine.inOut" }, until); return el; };
// trench line: dark zig-zag strip that draws on (world px; w = screen px at camera scale s)
const trench = (pts, t, dur, until, s = 1, o = {}) => { const zz = [];
  for (let i = 1; i < pts.length; i++) { const a = pts[i - 1], b = pts[i], L = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.max(1, Math.round(L * s / 10));
    const nx = -(b[1] - a[1]) / L, ny = (b[0] - a[0]) / L;
    for (let k = 0; k < n; k++) { const f = k / n, z = (k % 2 ? 1 : -1) * 2.2 / s; zz.push([a[0] + (b[0] - a[0]) * f + nx * z, a[1] + (b[1] - a[1]) * f + ny * z]); } }
  zz.push(pts[pts.length - 1]);
  return glowPath(zz, o.col || "#2a2118", (o.w || 2.6) / s, t, until, 0, o.op || 0.9, { draw: dur, top: true }); };
// a screen-space clock card: label + an analogue face whose hour hand turns between the keys [[t, hour, "4 PM"], ...]
const clockCard = (keys, css, t, until) => {
  const el = scr(`<div style="display:flex;align-items:center;gap:16px;padding:10px 22px 10px 14px;background:rgba(18,16,12,0.9);border-top:5px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea">
    <svg width="74" height="74" viewBox="-40 -40 80 80"><circle r="36" fill="#f3eee2" stroke="#c9b48a" stroke-width="4"/>${[...Array(12)].map((_, i) => `<line x1="0" y1="-30" x2="0" y2="-25" stroke="#222" stroke-width="3" transform="rotate(${i * 30})"/>`).join("")}
    <line class="hh" x1="0" y1="4" x2="0" y2="-18" stroke="#111" stroke-width="5" stroke-linecap="round"/><line class="mh" x1="0" y1="5" x2="0" y2="-27" stroke="#111" stroke-width="3" stroke-linecap="round"/><circle r="3.5" fill="#c4121f"/></svg>
    <div class="lab" style="font-size:46px;letter-spacing:.06em;min-width:120px">${keys[0][2]}</div></div>`, css, t, until);
  const hh = el.querySelector(".hh"), mh = el.querySelector(".mh"), lab = el.querySelector(".lab");
  gsap.set(hh, { rotation: keys[0][1] * 30, svgOrigin: "0 0" }); gsap.set(mh, { rotation: 0, svgOrigin: "0 0" });
  for (let i = 1; i < keys.length; i++) { const d = Math.max(0.3, keys[i][0] - keys[i - 1][0] - 0.2), h0 = keys[i - 1][1], h1 = keys[i][1];
    tl.to(hh, { rotation: h1 * 30, duration: d, ease: "power1.inOut" }, keys[i - 1][0] + 0.2); tl.to(mh, { rotation: (h1 - h0) * 360, duration: d, ease: "power1.inOut" }, keys[i - 1][0] + 0.2);
    tl.set(mh, { rotation: 0 }, keys[i - 1][0] + 0.2 + d + 0.01); }
  tl.eventCallback("onUpdate", ((prev) => function () { if (prev) prev.apply(this, arguments); let s = keys[0][2]; keys.forEach((k) => { if (tl.time() >= k[0]) s = k[2]; }); if (lab.textContent !== s) lab.textContent = s; })(tl.eventCallback("onUpdate")));
  return el; };
// pontoon bridge: n small boats appear one by one along a->b between t0 and t1 (world px); returns the deck path
const pontoons = (a, b, t0, t1, n = 26, o = {}) => { const L = Math.hypot(b[0] - a[0], b[1] - a[1]), ang = Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI, bw = o.bw || 3.2, bl = o.bl || 9;
  const g = document.createElementNS(NS, "g"); OVL.appendChild(g);
  for (let k = 0; k < n; k++) { const f = (k + 0.5) / n, x = a[0] + (b[0] - a[0]) * f, y = a[1] + (b[1] - a[1]) * f, r = document.createElementNS(NS, "rect");
    r.setAttribute("x", -bw / 2); r.setAttribute("y", -bl / 2); r.setAttribute("width", bw); r.setAttribute("height", bl); r.setAttribute("rx", bw * 0.4);
    r.setAttribute("fill", o.fill || "#e2d3ad"); r.setAttribute("stroke", "#1f4fc4"); r.setAttribute("stroke-width", bw * 0.3); r.setAttribute("transform", `translate(${x} ${y}) rotate(${ang})`);
    g.appendChild(r); gsap.set(r, { opacity: 0 }); tl.to(r, { opacity: 1, duration: 0.25 }, t0 + (t1 - t0) * k / n); }
  const deck = document.createElementNS(NS, "path"); deck.setAttribute("d", `M ${a[0]} ${a[1]} L ${b[0]} ${b[1]}`); deck.setAttribute("stroke", "#f3ead2"); deck.setAttribute("stroke-width", bw * 0.6);
  deck.setAttribute("stroke-linecap", "round"); deck.setAttribute("fill", "none"); g.appendChild(deck);
  gsap.set(deck, { strokeDasharray: `${L} ${L + 5}`, strokeDashoffset: L }); tl.to(deck, { strokeDashoffset: 0, duration: t1 - t0, ease: "none" }, t0);
  return g; };
// small screen-space number card (big value, label above, sub below) with an optional tick-up; spoken words only
const numCard = (label, value, sub, css, t, until, o = {}) => { const el = scr(`<div style="padding:10px 30px 12px;background:rgba(18,16,12,0.92);border-top:6px solid ${o.col || "#2e5cb2"};font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center;box-shadow:0 16px 34px rgba(0,0,0,.55)">
  <div style="font-size:20px;letter-spacing:.3em;color:${o.lc || "#9fc0ea"}">${label}</div><div class="v" style="font-size:${o.vs || 62}px;letter-spacing:.04em;line-height:1.1">${value}</div>${sub ? `<div style="font-size:19px;letter-spacing:.22em;color:#c9c2b2">${sub}</div>` : ""}</div>`, css, t, until);
  if (o.slam !== false) slam(el, t, { sfx: "hit", shake: 3 }); return el; };
// ---------- end of move-3 additions ----------
