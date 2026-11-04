// ================= Arnold #17 move 1 + ending (map agent a1_: m1a, m1b, ending), appended after gh_kit.js + ar3_kit.js by tools/a1_inline.py =================
// SIDES: Americans = BLUE "carth" (Continental Colours 1775-76; 13-star flag in the ending), British = RED "rome" (Union Flag 1606).
// a sand underlay under every map (so a corner of the world outside the baked maps never shows the dark page)
const UNDER = (() => { const u = document.createElement("div"); u.style.cssText = "position:absolute;left:-30000px;top:-30000px;width:60000px;height:60000px;background:rgb(206,192,150);";
  WORLD.insertBefore(u, WORLD.firstChild); return u; })();
// a map group drawn ON TOP of the base relief (feather only on the listed edges: "t", "b", "l", "r"), returns the group
const mapTop = (name, edges = "t", fe = 4) => { const [z, ox, oy] = GD.maps[name], k = 2 ** (BZ - z), [bx, by] = [GD.base[1], GD.base[2]];
  const r = [ox * k - bx, oy * k - by, 2880 * k, 1620 * k];
  const g = document.createElement("div"); g.style.cssText = `position:absolute;left:${r[0]}px;top:${r[1]}px;width:${r[2]}px;height:${r[3]}px;isolation:isolate;`;
  const lr = `linear-gradient(to right, ${edges.includes("l") ? "transparent 0%, #000 " + fe + "%" : "#000 0%"}, ${edges.includes("r") ? "#000 " + (100 - fe) + "%, transparent 100%" : "#000 100%"})`;
  const tb = `linear-gradient(to bottom, ${edges.includes("t") ? "transparent 0%, #000 " + fe * 1.6 + "%" : "#000 0%"}, ${edges.includes("b") ? "#000 " + (100 - fe * 1.6) + "%, transparent 100%" : "#000 100%"})`;
  g.style.webkitMaskImage = `${lr}, ${tb}`; g.style.maskImage = `${lr}, ${tb}`; g.style.webkitMaskComposite = "source-in"; g.style.maskComposite = "intersect";
  const i = document.createElement("img"); i.src = `assets/a1_${name}.jpg`; i.alt = ""; i.style.cssText = "position:absolute;left:0;top:0;width:100%;height:100%;"; g.appendChild(i);
  WORLD.insertBefore(g, OVL); g.rect = r; g.k = k; return g; };
// ---------- the lake/river craft (copied from tools/va_kit.js, map agent va): top-down, side colour, bow = +x ----------
const LAKESVG = (kind, s, col) => {
  const blue = col === "#1f4fc4", rim = blue ? "#9fc0ff" : "#ffb0a6", gl = blue ? "#6f9bff" : "#ff7a6a", dk = blue ? "#0d2a6e" : "#5e0a10";
  const hull = (L, B, sq) => { const a = -L / 2, b = L / 2; return sq
    ? `M${a} ${-B / 2} L${b - B * 0.45} ${-B / 2} L${b} 0 L${b - B * 0.45} ${B / 2} L${a} ${B / 2} Z`
    : `M${a + B * 0.2} ${-B / 2} L${b - B * 0.9} ${-B / 2} Q${b} ${-B * 0.3} ${b} 0 Q${b} ${B * 0.3} ${b - B * 0.9} ${B / 2} L${a + B * 0.2} ${B / 2} Q${a - B * 0.05} 0 ${a + B * 0.2} ${-B / 2} Z`; };
  const deck = (L, B, sq) => `<path d="${hull(L * 0.78, B * 0.6, sq)}" fill="#c7a26b" stroke="${dk}" stroke-width="0.5" transform="translate(${-L * 0.03} 0)"/>`;
  const sq = (x, w, h = 2.6) => `<path d="M${x - h / 2} ${-w / 2} Q${x + h} 0 ${x - h / 2} ${w / 2} L${x - h * 0.9} ${w / 2} Q${x + h * 0.2} 0 ${x - h * 0.9} ${-w / 2} Z" fill="#f6f1e4" stroke="#6b6458" stroke-width="0.45"/>`;
  const ports = (x0, x1, n, B) => [...Array(n)].map((_, k) => { const x = x0 + (x1 - x0) * k / Math.max(1, n - 1); return `<rect x="${x - 0.8}" y="${-B / 2 - 0.2}" width="1.6" height="1.3" fill="#0b0c0e"/><rect x="${x - 0.8}" y="${B / 2 - 1.1}" width="1.6" height="1.3" fill="#0b0c0e"/>`; }).join("");
  const oars = (x0, x1, n, B) => [...Array(n)].map((_, k) => { const x = x0 + (x1 - x0) * k / Math.max(1, n - 1); return `<line x1="${x}" y1="${-B / 2}" x2="${x - 1.5}" y2="${-B / 2 - 4}" stroke="#e8dcc0" stroke-width="0.8"/><line x1="${x}" y1="${B / 2}" x2="${x - 1.5}" y2="${B / 2 + 4}" stroke="#e8dcc0" stroke-width="0.8"/>`; }).join("");
  const pen = (x) => `<line x1="${x}" y1="0" x2="${x - 3}" y2="0" stroke="#f3eee2" stroke-width="0.8"/><path d="M${x - 2.6} -0.4 L${x - 9} -2.6 L${x - 7.2} -0.3 L${x - 9} 2.0 Z" fill="${col}" stroke="#f3eee2" stroke-width="0.5"/>`;
  const H = (L, B, sqh) => `<path d="${hull(L, B, sqh)}" fill="${col}" stroke="${rim}" stroke-width="1.4"/>${deck(L, B, sqh)}`;
  let body = "", w = 60, h = 24;
  if (kind === "ship") { w = 70; h = 30; body = `<line x1="22" y1="0" x2="32" y2="0" stroke="#e8dcc0" stroke-width="1.1"/>` + H(46, 13) + ports(-16, 14, 9, 13) + sq(12, 20) + sq(1, 22) + sq(-11, 18) + pen(-23); }
  else if (kind === "bateau") { w = 30; h = 16; } if (kind === "bateau") body = oars(-5, 5, 3, 6) + H(20, 6) + [...Array(5)].map((_, k) => `<circle cx="${-6 + k * 3}" cy="0" r="0.9" fill="#2a2420"/>`).join("") + pen(-10);
  else if (kind === "canoe") { w = 26; h = 12; body = H(16, 4) + [...Array(3)].map((_, k) => `<circle cx="${-4 + k * 4}" cy="0" r="0.8" fill="#2a2420"/>`).join(""); }
  const glow = `filter:drop-shadow(0 0 ${(s * 0.16).toFixed(1)}px ${gl}) drop-shadow(0 ${(s * 0.06).toFixed(1)}px ${(s * 0.1).toFixed(1)}px rgba(0,0,0,.7))`;
  return `<div><svg width="${(s * w / 23).toFixed(0)}" height="${(s * h / 23).toFixed(0)}" viewBox="${-w / 2} ${-h / 2} ${w} ${h}" style="display:block;overflow:visible;${glow}">${body}</svg></div>`;
};
// a craft along a path (heading follows the path), constant on screen; t <= 0 = on screen at frame 0
const craft = (kind, pts, t, dur, until, o = {}) => {
  const s = (o.s || 22) * 1.25, col = o.side === "rome" ? "#c4121f" : "#1f4fc4";
  const el = GG.pin(LAKESVG(kind, s, col), pts[0][0], pts[0][1], { t: t > 0 ? t : null, until }); pinS(el); if (!(t > 0)) gsap.set(el, { autoAlpha: 1 });
  const sv = el.querySelector("svg"), n = o.n || 30;
  const head = (f) => { const a = posOn(pts, Math.max(0, f - 0.01)), b = posOn(pts, Math.min(1, f + 0.01)); return Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI; };
  gsap.set(sv, { rotation: pts.length > 1 ? head(0) : (o.rot || 0) });
  if (pts.length > 1 && dur > 0) for (let k = 1; k <= n; k++) { const f0 = (k - 1) / n, f1 = k / n, q = posOn(pts, f1);
    tl.to(el, { left: q[0], top: q[1], duration: dur / n, ease: "none" }, Math.max(0, t) + (k - 1) * dur / n);
    tl.to(sv, { rotation: head((f0 + f1) / 2), duration: Math.min(0.4, dur / n), ease: "none" }, Math.max(0, t) + (k - 1) * dur / n); }
  return el; };
// a river course drawn on the map (the 1775 river where the modern map has a reservoir or shows nothing): pale bank + water line
const river = (pts, w, o = {}) => { const g = document.createElementNS(NS, "g"), d = "M" + pts.map((q) => q.join(" ")).join(" L");
  g.innerHTML = `<path d="${d}" fill="none" stroke="rgba(150,128,90,0.55)" stroke-width="${w * 2.2}" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="${d}" fill="none" stroke="${o.col || "rgb(122,160,190)"}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
  OVL.insertBefore(g, OVL.firstChild); if (o.t != null) { gsap.set(g, { autoAlpha: 0 }); tl.to(g, { autoAlpha: 1, duration: 0.8 }, o.t); } return g; };
// smooth a polyline (Chaikin) so hand-placed river points read as a natural, winding course
const smoothP = (pts, it = 3) => { let p = pts; for (let k = 0; k < it; k++) { const q = [p[0]]; for (let i = 0; i < p.length - 1; i++) { const a = p[i], b = p[i + 1];
  q.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25], [a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); } q.push(p[p.length - 1]); p = q; } return p; };
// white-water marks (rapids/falls) on a river: short white chevrons, constant on screen, shimmering
const rapids = (x, y, t, until, ang = 0, s = 22) => { const el = pinS(GG.pin(`<svg width="${s}" height="${s}" viewBox="-10 -10 20 20" style="display:block;overflow:visible;transform:rotate(${ang}deg)"><path d="M-7 -5 L-3 -1 L-7 3 M-1 -6 L3 -2 L-1 2 M5 -4 L8 -1 L5 2" fill="none" stroke="#f7fbff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 2px #bfe2ff)"/></svg>`, x, y, { t, until }));
  tl.to(el.firstElementChild, { opacity: 0.45, duration: 0.4, yoyo: true, repeat: Math.max(1, Math.round(((until || t + 8) - t) / 0.4)), ease: "sine.inOut" }, t + 0.4); return el; };
// small icons (world space, constant on screen)
const ICO = {
  barrel: (c = "#8a6a44") => `<svg width="18" height="22" viewBox="0 0 18 22" style="display:block;filter:drop-shadow(0 2px 2px rgba(0,0,0,.7))"><path d="M3 2 Q9 0 15 2 Q17 11 15 20 Q9 22 3 20 Q1 11 3 2 Z" fill="${c}" stroke="#f3eee2" stroke-width="1.2"/><path d="M2 7 H16 M2 15 H16" stroke="#2a2420" stroke-width="1.2"/></svg>`,
  cow: `<svg width="30" height="20" viewBox="0 0 30 20" style="display:block;filter:drop-shadow(0 2px 2px rgba(0,0,0,.75))"><path d="M4 6 Q4 3 8 3 L21 3 Q24 3 25 5 L28 4 L28 8 L25 9 L24 13 L22 13 L22 17 L20 17 L20 13 L10 13 L10 17 L8 17 L8 13 Q5 13 4 10 Z" fill="#f3eee2" stroke="#2a2420" stroke-width="1"/><circle cx="12" cy="7" r="2" fill="#5a3e22"/><circle cx="18" cy="9" r="1.6" fill="#5a3e22"/></svg>`,
  sack: `<svg width="18" height="20" viewBox="0 0 18 20" style="display:block;filter:drop-shadow(0 2px 2px rgba(0,0,0,.75))"><path d="M5 3 L13 3 L12 6 Q17 9 16 16 Q15 19 9 19 Q3 19 2 16 Q1 9 6 6 Z" fill="#efe6cf" stroke="#2a2420" stroke-width="1.1"/><path d="M5 4 L13 4" stroke="#8a6a44" stroke-width="1.6"/></svg>`,
  house: `<svg width="22" height="20" viewBox="0 0 22 20" style="display:block;filter:drop-shadow(0 2px 2px rgba(0,0,0,.75))"><path d="M2 9 L11 2 L20 9 Z" fill="#8a3a22" stroke="#f3eee2" stroke-width="1.1"/><rect x="4" y="9" width="14" height="9" fill="#efe6cf" stroke="#2a2420" stroke-width="1.1"/><rect x="9" y="12" width="4" height="6" fill="#5a3e22"/></svg>`,
  tree: `<svg width="26" height="14" viewBox="0 0 26 14" style="display:block;filter:drop-shadow(0 2px 2px rgba(0,0,0,.75))"><path d="M2 9 L20 5" stroke="#5a3e22" stroke-width="3" stroke-linecap="round"/><circle cx="21" cy="5" r="4.5" fill="#4d6b34" stroke="#c9dca0" stroke-width="1"/><path d="M8 7 L10 3 M13 6 L15 2" stroke="#5a3e22" stroke-width="1.4"/></svg>`,
  man: `<svg width="12" height="12" viewBox="0 0 12 12" style="display:block"><circle cx="6" cy="6" r="4.2" fill="#1f4fc4" stroke="#f3eee2" stroke-width="1.4"/></svg>`,
  q: `<div style="font-family:Oswald;font-weight:700;font-size:22px;color:#f7f3ea;text-shadow:0 0 4px #000,0 2px 3px #000">?</div>`,
  barricade: (c = "#c4121f") => `<svg width="38" height="22" viewBox="0 0 38 22" style="display:block;overflow:visible;filter:drop-shadow(0 0 4px ${c}) drop-shadow(0 2px 3px rgba(0,0,0,.8))"><path class="bw" d="M2 18 L36 18 M5 18 L12 4 M14 18 L20 4 M23 18 L29 4 M3 10 L35 10" stroke="#6b4a2a" stroke-width="3.2" stroke-linecap="round"/><path class="bc" d="M2 18 L36 18" stroke="${c}" stroke-width="2" stroke-dasharray="4 3"/></svg>`,
};
const icon = (html, x, y, t, until, o = {}) => { const el = pinS(GG.pin(`<div style="zoom:${o.k || 1.9}">${html}</div>`, x, y, { t, pop: o.pop !== false, until })); return el; };
// a screen card that grows line by line, each line on its spoken word: lines = [[text, t], ...]
const listCard = (kick, lines, css, t, until, o = {}) => { const el = scr(`<div style="padding:14px 40px 16px;background:rgba(18,16,12,0.93);border-top:6px solid ${o.col || "#c9b48a"};font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center;box-shadow:0 20px 40px rgba(0,0,0,.55);min-width:${o.mw || 520}px">
  <div class="kk" style="font-size:20px;letter-spacing:.36em;color:${o.kc || "#c9b48a"};min-height:26px">${kick}</div>${lines.map(([tx], i) => `<div class="ln ln${i}" style="font-size:${o.size || 50}px;letter-spacing:.06em;line-height:1.18">${tx}</div>`).join("")}</div>`, css, t, until);
  lines.forEach(([, tt], i) => { const ln = el.querySelector(".ln" + i); gsap.set(ln, { autoAlpha: 0, display: "none" }); tl.set(ln, { display: "block" }, tt); tl.fromTo(ln, { autoAlpha: 0, x: -24 }, { autoAlpha: 1, x: 0, duration: 0.3, immediateRender: false }, tt); SFX("hit", tt + 0.05);
    if (o.keep && i >= o.keep) tl.set(el.querySelector(".ln" + (i - o.keep)), { display: "none" }, tt); });   // o.keep: only the last N lines stay (finished lines drop)
  if (o.kickT != null) { const kk = el.querySelector(".kk"); gsap.set(kk, { autoAlpha: 0 }); tl.to(kk, { autoAlpha: 1, duration: 0.3 }, o.kickT); }
  return el; };
// casualty card (the K.casualties look, but each value only on its own spoken words): colA/colB = [[text, t], ...]
const casCard = (colA, colB, foot, t, until, top = 250) => { const col = (flag, head, c, vals, k) => `<div style="min-width:300px"><div style="display:flex;align-items:center;gap:12px;padding-bottom:10px;margin-bottom:10px;border-bottom:3px solid ${c}">
    <img src="${flag}" style="height:34px;border:1px solid #f7f3ea"><div style="font-size:30px;letter-spacing:0.08em">${head}</div></div>${vals.map(([tx], i) => `<div class="v${k}${i}" style="font-size:38px;line-height:1.5">${tx}</div>`).join("")}</div>`;
  const el = scr(`<div style="display:flex;gap:70px;padding:28px 50px 22px;background:rgba(18,16,12,0.92);border-top:6px solid #c9b48a;color:#f7f3ea;font-family:Oswald;font-weight:700;box-shadow:0 20px 40px rgba(0,0,0,0.55);flex-wrap:wrap;justify-content:center;max-width:980px">
    ${col(FL.us, "AMERICANS", "#2e5cb2", colA, "a")}${col(FL.gb, "BRITISH", "#be3a2a", colB, "b")}<div style="font-size:16px;letter-spacing:.2em;color:#a8a294;text-align:center;width:100%">${foot}</div></div>`,
    typeof top === "string" ? top : `left:0;right:0;top:${top}px;display:flex;justify-content:center;`, t, until);
  [[colA, "a"], [colB, "b"]].forEach(([vals, k]) => vals.forEach(([, tt], i) => { const v = el.querySelector(".v" + k + i); gsap.set(v, { autoAlpha: 0 }); tl.fromTo(v, { autoAlpha: 0, y: 12 }, { autoAlpha: 1, y: 0, duration: 0.3, immediateRender: false }, tt); SFX("hit", tt + 0.05); }));
  SFX("hit", t + 0.2); return el; };
// the date scroll ticking through several dates (the scroll itself never disappears)
const dateRun = (list, size = 30) => list.forEach(([txt, t, until]) => B.date(txt, t, until, size));
// a time-based crossfade of a whole layer
const fadeL = (el, t, dur, to) => tl.to(el, { autoAlpha: to, duration: dur, ease: "sine.inOut" }, t);
// grey a world-space marker (face marker / icon)
const greyM = (el, t) => tl.to(el.firstElementChild, { filter: "grayscale(1) brightness(0.65)", duration: 0.5 }, t);
// badge rings in 1775-76: the Continental Colours with the Union canton clearly in view (audit #42: never read as the 13-star flag)
(() => { const kb = K.badge; K.badge = (o) => { const el = kb(o); if (/continental/.test(o.flag || "")) { const r = el.querySelector("div[style*='border-radius:50%']");
  const bg = document.createElement("div"); bg.style.cssText = `position:absolute;inset:0;background:url(${o.flag}) 0% 0%/auto 150% no-repeat;`; r.insertBefore(bg, r.firstChild); } return el; }; })();
  // (a child layer, not r.style: re-serialising the ring's style would break the "border-radius:50%" selectors in gh_kit)
// the date scroll ON from frame 0 (no fade-in: the scroll never disappears across a scene cut)
const dateHold = (txt, until, size = 30) => { const box = document.getElementById("date"); gsap.set(box, { autoAlpha: 1, x: 0 });
  const d = document.createElement("div"); d.className = "d"; d.textContent = txt; d.style.fontSize = size + "px"; box.appendChild(d); gsap.set(d, { autoAlpha: 1, y: 0 });
  if (until != null) tl.to(d, { autoAlpha: 0, y: -14, duration: 0.35 }, until); return d; };
