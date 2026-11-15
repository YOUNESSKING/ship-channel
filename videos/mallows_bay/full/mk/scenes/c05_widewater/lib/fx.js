// FX kit v2 (Kings-and-Generals-inspired, kept flat and simple): detailed top-down aircraft with ground
// shadows, spinning rotors/props and dotted flight paths; artillery that fires (muzzle flash, smoke, recoil);
// impacts with fireball, rising smoke and a small camera shake; unit counters with icons, flags and size marks.
// Usage in a scene:  const K = FXK(B);  then K.aircraft({...}), K.gun(...), K.impact(...), K.counter(...).
// Everything is placed on the one paused timeline (B.tl), so renders stay deterministic.
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const COL = { carth: "#1f4fc4", rome: "#c4121f" }; // same as --carth / --rome in battle.css (counters, aircraft, arrows)
  // LOCKED territory/front palette (owner-approved 2026-09-27): day lines 30% muted, night lines + tint fully muted (E)
  const LINE_DAY = { carth: "#2c57b7", rome: "#bc2528" }, LINE_NIGHT = { carth: "#4a6a9a", rome: "#a8503c" };
  const TINT = { carth: "#4a6a9a", rome: "#a8503c" };
  const INK = "#f7f3ea";
  // flag badges per nation: pass flag/flagA/flagB = a key below; add the new video's nations + their files in assets/media/
  const FLAGS = { us: "assets/media/us_flag_48star.png", usmc: "assets/media/usmc_flag.png", kpa: "assets/media/kpa_flag.png",
    prc: "assets/media/pva_flag.png", pva: "assets/media/pva_flag.png", uk: "assets/media/uk_flag.png", arg: "assets/media/arg_flag.png", ger: "assets/media/ger_cross.png",
    ussr: "assets/media/ussr_flag.png", reich: "assets/media/ger_reich_flag.png" };  // Rokossovsky #8: period USSR + Reich flags
  const flagSrc = (f, dflt) => FLAGS[f] || (f && /[./]/.test(f) ? f : FLAGS[dflt]);  // a png path also works (Rokossovsky #8)

  // ---- aircraft art: top-down, nose pointing +x, drawn around (0,0) in a -50..50 box ----
  const ART = {
    heli: (c) => `
      <path d="M-4 -2.2 L-40 -1.4 L-40 1.4 L-4 2.2 Z" fill="${c}" stroke="${INK}" stroke-width="1.4"/>
      <rect x="-44" y="-8" width="5" height="16" rx="1.5" fill="${c}" stroke="${INK}" stroke-width="1.2"/>
      <line x1="-2" y1="-12.5" x2="24" y2="-12.5" stroke="#1b1812" stroke-width="2.4" stroke-linecap="round"/>
      <line x1="-2" y1="12.5" x2="24" y2="12.5" stroke="#1b1812" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M-12 0 C-12 -9 0 -11.5 12 -10.5 C22 -9.5 29 -5 29 0 C29 5 22 9.5 12 10.5 C0 11.5 -12 9 -12 0 Z" fill="${c}" stroke="${INK}" stroke-width="1.6"/>
      <path d="M17 -6.5 C24 -5.5 28 -3 28 0 C28 3 24 5.5 17 6.5 C19 3 19 -3 17 -6.5 Z" fill="#bfe3ff" opacity="0.9"/>
      <g class="trotor" transform="translate(-41.5 9)"><rect x="-6" y="-1" width="12" height="2" fill="#1b1812"/></g>
      <g class="rotor" transform="translate(8 0)">
        <circle r="31" fill="rgba(235,235,230,0.16)" stroke="rgba(255,255,255,0.45)" stroke-width="0.8"/>
        <g class="blades"><rect x="-31" y="-1.1" width="62" height="2.2" rx="1" fill="#3b3833" opacity="0.85"/><rect x="-1.1" y="-31" width="2.2" height="62" rx="1" fill="#3b3833" opacity="0.85"/></g>
        <circle r="3" fill="#3a3a3a"/></g>`,
    jet: (c) => `
      <path d="M36 0 L26 -3.2 L-18 -4.2 L-30 -3 L-30 3 L-18 4.2 L26 3.2 Z" fill="${c}" stroke="${INK}" stroke-width="1.5" stroke-linejoin="round"/>
      <path d="M10 -3.5 L-8 -26 L-16 -26 L-8 -3.8 Z M10 3.5 L-8 26 L-16 26 L-8 3.8 Z" fill="${c}" stroke="${INK}" stroke-width="1.5" stroke-linejoin="round"/>
      <path d="M-20 -3.6 L-30 -13 L-35 -13 L-28 -3.4 Z M-20 3.6 L-30 13 L-35 13 L-28 3.4 Z" fill="${c}" stroke="${INK}" stroke-width="1.3" stroke-linejoin="round"/>
      <ellipse cx="20" cy="0" rx="7" ry="2.3" fill="#bfe3ff"/>
      <circle class="burn" cx="-32" cy="0" r="3.6" fill="#ffb347"/>`,
    turboprop: (c) => `
      <path d="M32 0 C30 -3 24 -3.4 18 -3.4 L-30 -2.4 L-30 2.4 L18 3.4 C24 3.4 30 3 32 0 Z" fill="${c}" stroke="${INK}" stroke-width="1.5"/>
      <rect x="-3" y="-34" width="11" height="68" rx="2.5" fill="${c}" stroke="${INK}" stroke-width="1.5"/>
      <rect x="-32" y="-11" width="6" height="22" rx="1.5" fill="${c}" stroke="${INK}" stroke-width="1.3"/>
      <rect x="0" y="-17" width="18" height="6" rx="2.5" fill="${c}" stroke="${INK}" stroke-width="1.3"/>
      <rect x="0" y="11" width="18" height="6" rx="2.5" fill="${c}" stroke="${INK}" stroke-width="1.3"/>
      <ellipse cx="22" cy="0" rx="6.5" ry="2.3" fill="#bfe3ff"/>
      <g class="prop" transform="translate(19 -14)"><circle r="8.5" fill="rgba(235,235,230,0.25)"/><g class="blades"><rect x="-1" y="-8.5" width="2" height="17" fill="#1b1812"/><rect x="-8.5" y="-1" width="17" height="2" fill="#1b1812"/></g></g>
      <g class="prop" transform="translate(19 14)"><circle r="8.5" fill="rgba(235,235,230,0.25)"/><g class="blades"><rect x="-1" y="-8.5" width="2" height="17" fill="#1b1812"/><rect x="-8.5" y="-1" width="17" height="2" fill="#1b1812"/></g></g>`,
    // C-47 Skytrain / Dakota (owner 2026-10-06: a convincing transport, not a drone-like icon): rounded nose, long broad tapered wings,
    // two engine nacelles with propellers, tailplane, D-Day black-and-white invasion stripes on the wings and rear fuselage
    c47: (c) => `
      <path d="M18 -4 L6.5 -48 Q4.6 -50.8 1.6 -48.6 L-5 -4 Z M18 4 L6.5 48 Q4.6 50.8 1.6 48.6 L-5 4 Z" fill="${c}" stroke="${INK}" stroke-width="1.4" stroke-linejoin="round"/>
      <path d="M14.2 -18.0 L13.4 -21.0 L-3.1 -21.0 L-3.4 -18.0 Z M14.2 18.0 L13.4 21.0 L-3.1 21.0 L-3.4 18.0 Z M12.5 -24.0 L11.7 -27.0 L-2.4 -27.0 L-2.7 -24.0 Z M12.5 24.0 L11.7 27.0 L-2.4 27.0 L-2.7 24.0 Z M10.9 -30.0 L10.1 -33.0 L-1.7 -33.0 L-2.0 -30.0 Z M10.9 30.0 L10.1 33.0 L-1.7 33.0 L-2.0 30.0 Z" fill="#f3eee2" opacity="0.9"/><path d="M13.4 -21.0 L12.5 -24.0 L-2.7 -24.0 L-3.1 -21.0 Z M13.4 21.0 L12.5 24.0 L-2.7 24.0 L-3.1 21.0 Z M11.7 -27.0 L10.9 -30.0 L-2.0 -30.0 L-2.4 -27.0 Z M11.7 27.0 L10.9 30.0 L-2.0 30.0 L-2.4 27.0 Z" fill="#1b1812" opacity="0.85"/>
      <path d="M-25 -1.6 L-29.5 -17 L-34.5 -17 L-33 -1.4 Z M-25 1.6 L-29.5 17 L-34.5 17 L-33 1.4 Z" fill="${c}" stroke="${INK}" stroke-width="1.3" stroke-linejoin="round"/>
      <path d="M34 0 C33.5 -3 31 -4.4 26 -4.4 L-8 -4.2 L-34 -1.4 L-34 1.4 L-8 4.2 L26 4.4 C31 4.4 33.5 3 34 0 Z" fill="${c}" stroke="${INK}" stroke-width="1.5"/>
      <path d="M-16 -3.4 L-18.4 -3.4 L-18.4 3.4 L-16 3.4 Z M-21 -2.9 L-23.4 -2.9 L-23.4 2.9 L-21 2.9 Z" fill="#f3eee2" opacity="0.9"/><path d="M-18.4 -3.2 L-20.8 -3.2 L-20.8 3.2 L-18.4 3.2 Z" fill="#1b1812" opacity="0.85"/>
      <rect x="-34" y="-0.7" width="9" height="1.4" fill="${INK}" opacity="0.7"/>
      <rect x="-4" y="-16.2" width="27" height="6.4" rx="3" fill="${c}" stroke="${INK}" stroke-width="1.3"/>
      <rect x="-4" y="9.8" width="27" height="6.4" rx="3" fill="${c}" stroke="${INK}" stroke-width="1.3"/>
      <ellipse cx="29" cy="0" rx="3.4" ry="2.6" fill="#bfe3ff"/>
      <g class="prop" transform="translate(24.5 -13)"><circle r="7.5" fill="rgba(235,235,230,0.25)"/><g class="blades"><rect x="-0.9" y="-7.5" width="1.8" height="15" fill="#1b1812"/><rect x="-7.5" y="-0.9" width="15" height="1.8" fill="#1b1812"/></g></g>
      <g class="prop" transform="translate(24.5 13)"><circle r="7.5" fill="rgba(235,235,230,0.25)"/><g class="blades"><rect x="-0.9" y="-7.5" width="1.8" height="15" fill="#1b1812"/><rect x="-7.5" y="-0.9" width="15" height="1.8" fill="#1b1812"/></g></g>`,
    // glowing C-47 (owner pick 2026-10-06, option B): white body with a soft glow; outline + glow in the side's colour
    // (blue = Allied, red = German) so friend and foe read at a glance
    c47g: (c) => {
      const g = { "#1f4fc4": "#6f9bff", "#c4121f": "#ff5a5a" }[c] || c;
      const nac = (y) => `M25 ${y} C25 ${y - 2.6} 22 ${y - 3.6} 18 ${y - 3.6} L-2 ${y - 3} C-6 ${y - 2.2} -8 ${y - 1} -9 ${y} C-8 ${y + 1} -6 ${y + 2.2} -2 ${y + 3} L18 ${y + 3.6} C22 ${y + 3.6} 25 ${y + 2.6} 25 ${y} Z`;
      const d = "M17 -4.6 L6.5 -45 C5.5 -48.6 2.6 -49.6 0.4 -48 L-6 -4.6 Z M17 4.6 L6.5 45 C5.5 48.6 2.6 49.6 0.4 48 L-6 4.6 Z " +
        "M-24 -2 L-29 -15 C-30 -17.2 -33 -17.6 -34.6 -16 L-33.6 -2 Z M-24 2 L-29 15 C-30 17.2 -33 17.6 -34.6 16 L-33.6 2 Z " +
        "M34 0 C34 -2.6 32 -4.6 27 -4.8 L-6 -4.6 C-16 -4 -26 -2.2 -33 -1 L-35.5 0 L-33 1 C-26 2.2 -16 4 -6 4.6 L27 4.8 C32 4.6 34 2.6 34 0 Z " + nac(-13) + " " + nac(13);
      const prop = (y) => `<g class="prop" transform="translate(26.5 ${y})"><g class="blades"><rect x="-0.9" y="-7.5" width="1.8" height="15" fill="rgba(255,255,255,0.55)"/><rect x="-7.5" y="-0.9" width="15" height="1.8" fill="rgba(255,255,255,0.55)"/></g></g>`;
      const part = (pd) => `<path d="${pd}" fill="#e9eef8" stroke="${c}" stroke-width="2" stroke-linejoin="round"/>`;
      return `<g style="filter:drop-shadow(0 0 3px ${g}) drop-shadow(0 0 7px ${g})">${d.split(/ (?=M)/).reduce((a, x, i) => (i % 2 && i < 4 ? (a[a.length - 1] += " " + x) : a.push(x), a), []).map(part).join("")}</g>${prop(-13)}${prop(13)}`;
    },
    // single-engine fighter-bomber (WW2/Korea prop plane, e.g. F4U Corsair: long nose, wide wings, one big propeller)
    prop: (c) => `
      <path d="M30 0 C29 -3.4 24 -4 18 -4 L-28 -2.2 L-28 2.2 L18 4 C24 4 29 3.4 30 0 Z" fill="${c}" stroke="${INK}" stroke-width="1.5"/>
      <path d="M12 -3.6 L6 -34 L-4 -34 L-2 -3.6 Z M12 3.6 L6 34 L-4 34 L-2 3.6 Z" fill="${c}" stroke="${INK}" stroke-width="1.5" stroke-linejoin="round"/>
      <path d="M-20 -2.4 L-26 -12 L-31 -12 L-29 -2.2 Z M-20 2.4 L-26 12 L-31 12 L-29 2.2 Z" fill="${c}" stroke="${INK}" stroke-width="1.3" stroke-linejoin="round"/>
      <ellipse cx="4" cy="0" rx="6" ry="2.4" fill="#bfe3ff"/>
      <g class="prop" transform="translate(32 0)"><circle r="11" fill="rgba(235,235,230,0.25)"/><g class="blades"><rect x="-1" y="-11" width="2" height="22" fill="#1b1812"/><rect x="-11" y="-1" width="22" height="2" fill="#1b1812"/></g></g>`,
    // twin-boom cargo plane (C-119 Flying Boxcar: fat pod, two engines on booms joined by a tailplane)
    cargo: (c) => `
      <path d="M26 0 C25 -6 20 -7 12 -7 L-10 -6 L-10 6 L12 7 C20 7 25 6 26 0 Z" fill="${c}" stroke="${INK}" stroke-width="1.5"/>
      <rect x="-4" y="-44" width="12" height="88" rx="3" fill="${c}" stroke="${INK}" stroke-width="1.5"/>
      <rect x="-36" y="-17" width="46" height="5" rx="2" fill="${c}" stroke="${INK}" stroke-width="1.3"/>
      <rect x="-36" y="12" width="46" height="5" rx="2" fill="${c}" stroke="${INK}" stroke-width="1.3"/>
      <rect x="-40" y="-20" width="7" height="40" rx="2" fill="${c}" stroke="${INK}" stroke-width="1.3"/>
      <ellipse cx="20" cy="0" rx="4" ry="3.4" fill="#bfe3ff"/>
      <g class="prop" transform="translate(14 -14.5)"><circle r="9" fill="rgba(235,235,230,0.25)"/><g class="blades"><rect x="-1" y="-9" width="2" height="18" fill="#1b1812"/><rect x="-9" y="-1" width="18" height="2" fill="#1b1812"/></g></g>
      <g class="prop" transform="translate(14 14.5)"><circle r="9" fill="rgba(235,235,230,0.25)"/><g class="blades"><rect x="-1" y="-9" width="2" height="18" fill="#1b1812"/><rect x="-9" y="-1" width="18" height="2" fill="#1b1812"/></g></g>`,
  };
  // ---- counter icons (side view silhouettes, like K&G counters) ----
  const ICON = {
    artillery: `<g fill="${INK}"><rect x="30" y="44" width="58" height="11" rx="3" transform="rotate(-24 36 52)"/><circle cx="38" cy="64" r="15" fill="none" stroke="${INK}" stroke-width="7"/><circle cx="38" cy="64" r="4"/><path d="M36 60 L10 82 L16 86 L40 66 Z"/></g>`,
    aa: `<g fill="${INK}"><rect x="46" y="16" width="7" height="46" rx="2" transform="rotate(28 50 62)"/><rect x="58" y="16" width="7" height="46" rx="2" transform="rotate(28 62 62)"/><path d="M22 84 L78 84 L70 64 L30 64 Z"/><circle cx="50" cy="64" r="9"/></g>`,
    infantry: `<line x1="4" y1="4" x2="96" y2="96" stroke="${INK}" stroke-width="8"/><line x1="96" y1="4" x2="4" y2="96" stroke="${INK}" stroke-width="8"/>`,
    hq: `<g fill="${INK}"><rect x="30" y="16" width="5" height="70"/><path d="M35 18 L78 30 L35 44 Z"/></g>`,
    // --- candidates (owner to choose) ---
    art_nato: `<circle cx="50" cy="50" r="19" fill="${INK}"/>`,
    art_gun: `<g fill="${INK}"><rect x="40" y="31" width="56" height="8" rx="3" transform="rotate(-22 44 50)"/><path d="M30 42 L52 36 L56 52 L34 58 Z"/><circle cx="36" cy="66" r="13" fill="none" stroke="${INK}" stroke-width="6"/><circle cx="36" cy="66" r="3.5"/><path d="M33 60 L6 84 L12 89 L40 66 Z"/></g>`,
    tank_nato: `<rect x="18" y="32" width="64" height="36" rx="18" fill="none" stroke="${INK}" stroke-width="8"/>`,
    tank_sil: `<g fill="${INK}"><path d="M10 58 L90 58 L84 74 L16 74 Z"/><path d="M30 44 L64 44 L70 58 L26 58 Z"/><rect x="62" y="46" width="34" height="5" rx="2"/><g fill="#1b1812"><circle cx="24" cy="70" r="4"/><circle cx="37" cy="71" r="4"/><circle cx="50" cy="71" r="4"/><circle cx="63" cy="71" r="4"/><circle cx="76" cy="70" r="4"/></g></g>`,
    mech_nato: `<line x1="4" y1="4" x2="96" y2="96" stroke="${INK}" stroke-width="7"/><line x1="96" y1="4" x2="4" y2="96" stroke="${INK}" stroke-width="7"/><rect x="24" y="36" width="52" height="28" rx="14" fill="none" stroke="${INK}" stroke-width="7"/>`,
  };

  window.FXK = function (B) {
    const tl = B.tl, pins = document.getElementById("pins"), ov = document.getElementById("overlay"), scene = document.getElementById("scene");
    if (!document.getElementById("fxk-css")) {
      const css = document.createElement("style"); css.id = "fxk-css";
      css.textContent = `
        .fxk-air { position:absolute; left:0; top:0; width:0; height:0; }
        .fxk-air svg { position:absolute; overflow:visible; }
        .fxk-puff { position:absolute; border-radius:50%; background: radial-gradient(circle, rgba(70,66,60,0.75) 0%, rgba(90,86,80,0.45) 45%, rgba(110,106,100,0) 72%); }
        .fxk-fire { position:absolute; border-radius:50%; background: radial-gradient(circle, #fffbe6 0%, #ffd34d 22%, rgba(255,120,20,0.9) 48%, rgba(200,40,0,0.5) 62%, rgba(120,20,0,0) 74%); }
        .fxk-ring { position:absolute; border-radius:50%; border: 2px solid rgba(255,230,180,0.9); }
        .fxk-flag { position:absolute; border:1px solid ${INK}; box-shadow:0 1px 3px rgba(0,0,0,0.6); z-index:2; }
        .fxk-size { position:absolute; left:0; right:0; text-align:center; font-weight:700; color:#1b1812; letter-spacing:0.05em; text-shadow: 0 0 2px #f7f3ea, 0 0 2px #f7f3ea; }`;
      document.head.appendChild(css);
    }
    const hide = (el) => gsap.set(el, { autoAlpha: 0 });
    const K = {};
    const div = (cls, x, y, w, h) => {
      const el = document.createElement("div"); el.className = cls;
      Object.assign(el.style, { left: x - w / 2 + "px", top: y - h / 2 + "px", width: w + "px", height: h + "px" });
      pins.appendChild(el); hide(el); return el;
    };

    // rising, spreading smoke puffs
    K.smoke = (x, y, t, o = {}) => {
      const n = o.n || 4, r = o.r || 14, life = o.life || 2.6;
      for (let i = 0; i < n; i++) {
        const el = div("fxk-puff", x + ((i * 7) % 11) - 5, y, r * 2, r * 2);
        const t0 = t + i * (o.gap || 0.18);
        tl.fromTo(el, { autoAlpha: 0, scale: 0.4, x: 0, y: 0 }, { autoAlpha: o.alpha || 0.85, scale: 1, duration: 0.35, ease: "power1.out", immediateRender: false }, t0);
        tl.to(el, { autoAlpha: 0, scale: 2.2, x: (o.drift || 10) + i * 3, y: -(o.rise || 30) - i * 6, duration: life, ease: "sine.out" }, t0 + 0.35);
      }
    };
    // small camera shake (screen space, does not fight the camera)
    K.shake = (t, amp = 5, dur = 0.35) => {
      const n = Math.max(3, Math.round(dur / 0.05));
      for (let i = 0; i < n; i++) tl.to(scene, { x: (i % 2 ? -1 : 1) * amp * (1 - i / n), y: ((i * 3) % 2 ? 1 : -1) * amp * 0.6 * (1 - i / n), duration: 0.05, ease: "none" }, t + i * 0.05);
      tl.to(scene, { x: 0, y: 0, duration: 0.05 }, t + n * 0.05);
    };
    // explosion: fireball + shock ring + smoke (+ shake + sound)
    K.impact = (x, y, t, o = {}) => {
      const r = o.r || 16;
      const f = div("fxk-fire", x, y, r * 2, r * 2);
      tl.fromTo(f, { autoAlpha: 0, scale: 0.2 }, { autoAlpha: 1, scale: 1.15, duration: 0.14, ease: "power2.out", immediateRender: false }, t);
      tl.to(f, { autoAlpha: 0, scale: 1.6, duration: 0.55, ease: "power1.in" }, t + 0.16);
      const ring = div("fxk-ring", x, y, r * 2, r * 2);
      tl.fromTo(ring, { autoAlpha: 0.9, scale: 0.3 }, { autoAlpha: 0, scale: 2.4, duration: 0.5, ease: "power2.out", immediateRender: false }, t);
      K.smoke(x, y - r * 0.2, t + 0.15, { n: o.puffs || 3, r: r * 0.9, rise: r * 2, life: o.life || 2.4 });
      if (o.shake !== false) K.shake(t, o.shake || (r >= 20 ? 6 : 3));
      if (window.SFX && o.sfx !== false) SFX(o.sfx || (r >= 20 ? "explosion" : "impact"), t);
    };
    // artillery piece firing: muzzle flash, smoke and a little recoil on its counter
    K.gun = (x, y, t, o = {}) => {
      const f = div("fxk-fire", x + (o.dx || 10), y + (o.dy || -8), 16, 16);
      tl.fromTo(f, { autoAlpha: 0, scale: 0.3 }, { autoAlpha: 1, scale: 1, duration: 0.06, immediateRender: false }, t);
      tl.to(f, { autoAlpha: 0, scale: 1.4, duration: 0.25 }, t + 0.07);
      K.smoke(x + (o.dx || 10), y + (o.dy || -8), t + 0.05, { n: 2, r: 8, rise: 14, life: 1.8, alpha: 0.7 });
      if (o.unit && B.units[o.unit]) {
        const blk = B.units[o.unit].el.querySelector(".blk");
        tl.to(blk, { x: -3, duration: 0.05 }, t); tl.to(blk, { x: 0, duration: 0.3, ease: "power2.out" }, t + 0.05);
      }
      if (window.SFX && o.sfx !== false) SFX(o.sfx || "fire", t);
    };

    // counter styling: icon, flag chip, size marker ("I" company, "II" battalion, "III" regiment)
    K.counter = (id, o = {}) => {
      const u = B.units[id]; if (!u) return;
      const blk = u.el.querySelector(".blk"), sv = blk.querySelector("svg");
      // LOCKED symbols (owner-approved 2026-09-28): artillery = howitzer silhouette, tank = tank silhouette, mech = NATO mech (X + track)
      const ALIAS = { artillery: "art_gun", tank: "tank_sil", armour: "tank_sil", mech: "mech_nato" };
      if (o.icon && ALIAS[o.icon]) o = Object.assign({}, o, { icon: ALIAS[o.icon] });
      const VB = { art_nato: "14 14 72 72", art_gun: "2 18 96 78", tank_nato: "12 26 76 48", tank_sil: "6 38 92 42" };
      if (o.icon && VB[o.icon]) sv.setAttribute("viewBox", VB[o.icon]);
      if (o.icon && ICON[o.icon]) { sv.setAttribute("preserveAspectRatio", (o.icon === "infantry" || o.icon === "mech_nato") ? "none" : "xMidYMid meet"); sv.innerHTML = ICON[o.icon]; }
      if (o.flag) {
        const img = document.createElement("img"); img.className = "fxk-flag";
        img.src = flagSrc(o.flag, "arg");
        Object.assign(img.style, { height: u.h * 0.55 + "px", left: -u.h * 0.35 + "px", top: -u.h * 0.3 + "px" });
        u.el.appendChild(img);
      }
      if (o.size) {
        const s = document.createElement("div"); s.className = "fxk-size"; s.textContent = o.size;
        s.style.fontSize = Math.max(7, u.h * 0.42) + "px"; s.style.top = -(u.h * 0.55) + "px";
        u.el.insertBefore(s, u.el.firstChild); u.el.style.overflow = "visible";
      }
    };

    // aircraft flying a polyline: o = { kind: heli|jet|turboprop|prop|cargo, side, pts, t, dur, size, alt, path: true,
    //   until, down: time it is hit (smoke trail, spin, crash explosion), land: true (shadow meets the aircraft) }
    K.aircraft = (o) => {
      const size = o.size || 40, c = COL[o.side] || o.side, alt = o.alt != null ? o.alt : size * 0.35;
      const pts = o.pts, segs = [];
      let total = 0;
      for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); segs.push(d); total += d; }
      const t0 = o.t, dur = o.dur || 4, tEnd = t0 + dur;
      const posAt = (tt) => { // position + heading at time tt (linear along the polyline)
        let d = Math.max(0, Math.min(1, (tt - t0) / dur)) * total;
        for (let i = 0; i < segs.length; i++) {
          if (d <= segs[i] || i === segs.length - 1) {
            const a = pts[i], b = pts[i + 1], f = Math.min(1, d / (segs[i] || 1));
            return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI];
          }
          d -= segs[i];
        }
      };
      // dotted flight path
      if (o.path !== false) {
        const pl = document.createElementNS(NS, "polyline");
        pl.setAttribute("points", pts.map((p) => p.join(",")).join(" "));
        pl.setAttribute("fill", "none"); pl.setAttribute("stroke", c); pl.setAttribute("stroke-width", Math.max(1.5, size * 0.05));
        pl.setAttribute("stroke-dasharray", `${size * 0.12} ${size * 0.18}`); pl.setAttribute("opacity", "0");
        ov.appendChild(pl);
        tl.to(pl, { opacity: 0.8, duration: 0.4 }, t0 - 0.4);
        tl.to(pl, { opacity: 0, duration: 0.6 }, (o.down || tEnd) + 0.6);
      }
      // engine sound, timed so its loudest moment (about 2.3 s into the clip) falls mid-flight
      if (window.SFX && o.sfx !== false) SFX(o.sfx || { jet: "jet", turboprop: "prop", heli: "heli" }[o.kind] || "prop", Math.max(0, t0 + Math.min(dur, (o.down || tEnd) - t0) / 2 - 2.3));
      const wrap = document.createElement("div"); wrap.className = "fxk-air"; pins.appendChild(wrap); hide(wrap);
      const k = size / 100;
      const shadow = document.createElementNS(NS, "svg"), body = document.createElementNS(NS, "svg");
      [shadow, body].forEach((s) => { s.setAttribute("viewBox", "-50 -50 100 100"); s.setAttribute("width", size); s.setAttribute("height", size); s.style.left = -size / 2 + "px"; s.style.top = -size / 2 + "px"; });
      shadow.innerHTML = `<g fill="rgba(0,0,0,0.38)" stroke="none" style="filter:blur(1.2px)">${ART[o.kind](c).replace(/fill="[^"]*"/g, 'fill="rgba(0,0,0,0.38)"').replace(/stroke="[^"]*"/g, 'stroke="none"').replace(/style="[^"]*"/g, "")}</g>`;
      body.innerHTML = ART[o.kind](c);
      body.style.filter = "drop-shadow(0 1px 1.5px rgba(0,0,0,0.6))";
      wrap.appendChild(shadow); wrap.appendChild(body);
      gsap.set(shadow, { x: alt * 0.9, y: alt });
      // movement: sample every 0.1 s (straight segments keep their heading)
      const last = o.down ? Math.min(o.down, tEnd) : tEnd;
      const p0 = posAt(t0);
      gsap.set(wrap, { left: p0[0], top: p0[1] });
      gsap.set([shadow, body], { rotation: p0[2] });
      tl.to(wrap, { autoAlpha: 1, duration: 0.3 }, t0);
      let prevRot = p0[2];
      for (let tt = t0; tt < last - 1e-6; tt += 0.1) {
        const step = Math.min(0.1, last - tt), p = posAt(tt + step);
        let r = p[2]; while (r - prevRot > 180) r -= 360; while (r - prevRot < -180) r += 360; prevRot = r;
        tl.to(wrap, { left: p[0], top: p[1], duration: step, ease: "none" }, tt);
        tl.to([shadow, body], { rotation: r, duration: step, ease: "none" }, tt);
      }
      // rotor / prop spin + jet burner flicker
      const spinEnd = o.down ? o.down + 1.4 : (o.until || tEnd + 3);
      body.querySelectorAll(".rotor .blades, .prop .blades").forEach((g) => {
        gsap.set(g, { svgOrigin: "0 0" });
        tl.to(g, { rotation: 360 * 5 * (spinEnd - t0), duration: spinEnd - t0, ease: "none" }, t0);
      });
      body.querySelectorAll(".burn").forEach((b) => tl.to(b, { opacity: 0.35, duration: 0.08, yoyo: true, repeat: Math.round((spinEnd - t0) / 0.08), ease: "none" }, t0));
      if (o.land) tl.to(shadow, { x: 0, y: 0, duration: Math.min(1.5, dur * 0.4), ease: "power1.in" }, tEnd - Math.min(1.5, dur * 0.4));
      if (o.down) { // hit: smoke trail, spiral down, crash
        const p = posAt(o.down);
        K.impact(p[0], p[1], o.down, { r: size * 0.35, puffs: 2, shake: false, sfx: "impact" });
        for (let i = 0; i < 8; i++) {
          const q = [p[0] + Math.cos((p[2] * Math.PI) / 180) * i * size * 0.12, p[1] + Math.sin((p[2] * Math.PI) / 180) * i * size * 0.12];
          K.smoke(q[0], q[1], o.down + 0.1 + i * 0.12, { n: 1, r: size * 0.18, rise: 6, life: 2.2, alpha: 0.7 });
        }
        const crash = [p[0] + Math.cos((p[2] * Math.PI) / 180) * size, p[1] + Math.sin((p[2] * Math.PI) / 180) * size];
        tl.to(wrap, { left: crash[0], top: crash[1], duration: 1.2, ease: "power1.in" }, o.down);
        tl.to(body, { rotation: prevRot + 400, scale: 0.55, duration: 1.2, ease: "power1.in" }, o.down);
        tl.to(shadow, { x: 0, y: 0, scale: 0.55, duration: 1.2, ease: "power1.in" }, o.down);
        K.impact(crash[0], crash[1], o.down + 1.2, { r: size * 0.6, puffs: 4, shake: 5 });
        tl.to(wrap, { autoAlpha: 0, duration: 0.15 }, o.down + 1.25);
      } else if (o.until != null) tl.to(wrap, { autoAlpha: 0, duration: 0.5 }, o.until);
      return wrap;
    };

    // K&G-style front: crisp centre line with a soft glowing colour band on each side (sideA = left of travel
    // direction, sideB = right), drawn on like an arrow; o.to (same point count) morphs it at o.moveT.
    K.front = (o) => {
      const w = o.width || 15, A = LINE_DAY[o.sideA] || o.sideA || LINE_DAY.carth, Bc = LINE_DAY[o.sideB] || o.sideB || LINE_DAY.rome;
      const off = (pts, d) => pts.map((p, i) => { // offset each vertex along the averaged normal
        const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
        const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
        return [p[0] - (dy / L) * d, p[1] + (dx / L) * d];
      });
      const dStr = (pts) => pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" ");
      if (!document.getElementById("fxk-blur")) {
        const defs = document.createElementNS(NS, "defs");
        defs.innerHTML = `<filter id="fxk-blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="${w * 0.35}"/></filter>`;
        ov.insertBefore(defs, ov.firstChild);
      }
      const g = document.createElementNS(NS, "g");
      const layer = (d, col, sw, op, blur) => `<path d="${d}" fill="none" stroke="${col}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round" opacity="${op}" ${blur ? 'filter="url(#fxk-blur)"' : ""}/>`;
      const gl = o.glow != null ? o.glow : 0.47; // glow strength (K&G-style muted look: ~0.3)
      const build = (pts) => [layer(dStr(off(pts, -w * 0.55)), A, w, gl, true), layer(dStr(off(pts, w * 0.55)), Bc, w, gl, true),
        layer(dStr(pts), "rgba(20,16,10,0.55)", w * 0.3, 1, false), layer(dStr(off(pts, -w * 0.09)), A, w * 0.16, 1, false), layer(dStr(off(pts, w * 0.09)), Bc, w * 0.16, 1, false)];
      g.innerHTML = build(o.pts).join("");
      ov.insertBefore(g, ov.children[1] || null);
      const paths = [...g.querySelectorAll("path")];
      const lens = paths.map((p) => p.getTotalLength() + w * 2);
      // gap longer than the dash and offset past the start, so the round cap of the hidden dash never shows as a dot
      paths.forEach((p, i) => gsap.set(p, { strokeDasharray: `${lens[i]} ${lens[i] + w * 2}`, strokeDashoffset: lens[i] + w }));
      tl.to(paths, { strokeDashoffset: 0, duration: o.dur || 2.0, ease: "power1.inOut" }, o.t);
      // gentle glow pulse
      tl.to(paths.slice(0, 2), { opacity: Math.min(1, gl * 1.45), duration: 1.2, yoyo: true, repeat: Math.max(1, Math.round(((o.until || o.t + 20) - o.t) / 1.2)), ease: "sine.inOut" }, o.t + (o.dur || 2));
      if (o.to) {
        const nd = build(o.to).map((h) => h.match(/ d="([^"]*)"/)[1]);
        paths.forEach((p, i) => tl.to(p, { attr: { d: nd[i] }, duration: o.moveDur || 2, ease: "power1.inOut" }, o.moveT));
      }
      if (o.until != null) tl.to(g, { opacity: 0, duration: 0.8 }, o.until);
      return g;
    };

    // screen-space element helper (above the map, under the credit)
    const screen = (html, style) => {
      const el = document.createElement("div"); el.style.cssText = "position:absolute;" + style; el.innerHTML = html;
      scene.insertBefore(el, document.getElementById("credit")); hide(el); return el;
    };
    // commander badge (K&G): round portrait (or initials) on the side's flag, name plate; slides in at a corner.
    // o = { name, role, photo: "assets/media/x.png" | null, flag: key of FLAGS (e.g. "uk"|"arg"|"us"|"prc"), side, corner: "tl"|"tr"|"bl"|"br", t, until }
    K.badge = (o) => {
      const c = COL[o.side] || COL.carth, flag = flagSrc(o.flag, "uk");
      const face = o.photo ? `<img src="${o.photo}" style="position:absolute;left:0;right:0;bottom:0;margin:auto;height:112%;filter:grayscale(1) contrast(1.1)">`
        : `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle, rgba(10,12,24,0.78) 0%, rgba(10,12,24,0.62) 60%, rgba(10,12,24,0.35) 100%);font-size:64px;font-weight:700;color:#f7f3ea;letter-spacing:0.04em;text-shadow:0 3px 6px rgba(0,0,0,0.9)">${o.initials || ""}</div>`;
      const pos = { tl: "left:60px;top:150px;", tr: "right:60px;top:110px;", bl: "left:60px;bottom:140px;", br: "right:60px;bottom:140px;" }[o.corner || "tr"];
      const el = screen(`<div style="display:flex;align-items:center;gap:18px;${o.corner && o.corner[1] === "l" ? "" : "flex-direction:row-reverse;"}">
        <div style="position:relative;width:170px;height:170px;border-radius:50%;overflow:hidden;border:6px solid #f3e7c4;box-shadow:0 0 0 4px ${c},0 12px 26px rgba(0,0,0,0.6);background:url(${flag}) center/cover">${face}</div>
        <div style="padding:10px 20px 12px;background:rgba(18,16,12,0.9);border-${o.corner && o.corner[1] === "l" ? "left" : "right"}:6px solid ${c};color:#f7f3ea;font-weight:700">
          <div style="font-size:34px;letter-spacing:0.06em;white-space:nowrap">${o.name}</div><div style="font-size:20px;letter-spacing:0.14em;color:#d8cfb8;white-space:nowrap">${o.role || ""}</div></div></div>`, pos);
      const dx = o.corner && o.corner[1] === "l" ? -80 : 80;
      tl.fromTo(el, { autoAlpha: 0, x: dx }, { autoAlpha: 1, x: 0, duration: 0.6, ease: "power3.out" }, o.t);
      if (o.until != null) tl.to(el, { autoAlpha: 0, x: dx, duration: 0.5, ease: "power2.in" }, o.until);
      return el; // badges slide in silently (owner 2026-09-30: zoom sound only on the biggest moves)
    };
    // casualty card (K&G): two columns (sideA / sideB) of rows with pictograms. rows: [["killed", "18", "45–55"], ...]
    const PICT = {
      killed: `<svg width="34" height="34" viewBox="0 0 100 100"><path d="M50 8 C24 8 12 26 12 46 C12 60 20 68 28 72 L28 88 L72 88 L72 72 C80 68 88 60 88 46 C88 26 76 8 50 8 Z" fill="#f7f3ea"/><circle cx="35" cy="46" r="10" fill="#1b1812"/><circle cx="65" cy="46" r="10" fill="#1b1812"/><path d="M50 58 L44 68 L56 68 Z" fill="#1b1812"/></svg>`,
      wounded: `<svg width="34" height="34" viewBox="0 0 100 100"><rect x="38" y="10" width="24" height="80" rx="6" fill="#f7f3ea"/><rect x="10" y="38" width="80" height="24" rx="6" fill="#f7f3ea"/><rect x="42" y="42" width="16" height="16" fill="#c4121f"/></svg>`,
      captured: `<svg width="34" height="34" viewBox="0 0 100 100"><rect x="10" y="10" width="80" height="80" rx="6" fill="none" stroke="#f7f3ea" stroke-width="8"/><g fill="#f7f3ea"><rect x="28" y="10" width="8" height="80"/><rect x="46" y="10" width="8" height="80"/><rect x="64" y="10" width="8" height="80"/></g></svg>`,
      aircraft: `<svg width="34" height="34" viewBox="-50 -50 100 100"><path d="M40 0 L28 -5 L-24 -6 L-34 -4 L-34 4 L-24 6 L28 5 Z M12 -5 L-8 -34 L-18 -34 L-8 -5 Z M12 5 L-8 34 L-18 34 L-8 5 Z" fill="#f7f3ea"/></svg>`,
    };
    K.casualties = (o) => {
      const col = (flag, head, c, vals) => `<div style="min-width:230px"><div style="display:flex;align-items:center;gap:12px;padding-bottom:10px;margin-bottom:10px;border-bottom:3px solid ${c}">
          <img src="${flag}" style="height:34px;border:1px solid #f7f3ea"><div style="font-size:30px;letter-spacing:0.08em">${head}</div></div>
          ${o.rows.map((r, i) => `<div style="display:flex;align-items:center;gap:14px;font-size:38px;line-height:1.5">${PICT[r[0]] || ""}<span>${vals[i]}</span></div>`).join("")}</div>`;
      const el = screen(`<div style="display:flex;gap:60px;padding:28px 50px 30px;background:rgba(18,16,12,0.92);border-top:6px solid #c9b48a;color:#f7f3ea;font-weight:700;box-shadow:0 20px 40px rgba(0,0,0,0.55)">
        ${col(flagSrc(o.flagA, "uk"), o.headA || "BRITISH", COL.carth, o.rows.map((r) => r[1]))}${col(flagSrc(o.flagB, "arg"), o.headB || "ARGENTINE", COL.rome, o.rows.map((r) => r[2]))}</div>`,
        `left:0;right:0;top:${o.top || 250}px;display:flex;justify-content:center;`);
      tl.fromTo(el, { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.7, ease: "power3.out" }, o.t);
      if (o.until != null) tl.to(el, { autoAlpha: 0, duration: 0.5 }, o.until);
      if (window.SFX) SFX("hit", o.t + 0.2);
      return el;
    };
    // pulsing objective ring (world space)
    K.target = (x, y, t, o = {}) => {
      const r = o.r || 40, c = COL[o.side] || o.side || "#ffd54a";
      const els = [0, 1].map((k) => {
        const el = div("", x, y, r * 2, r * 2);
        el.style.cssText += `position:absolute;border-radius:50%;border:${Math.max(2, r * 0.08)}px solid ${c};box-shadow:0 0 ${r * 0.4}px ${c};`;
        tl.fromTo(el, { autoAlpha: 0.95, scale: 0.6 }, { autoAlpha: 0, scale: 1.6, duration: 1.6, repeat: Math.max(0, Math.round(((o.until || t + 6) - t) / 1.6) - 1), ease: "sine.out", immediateRender: false }, t + k * 0.8);
        return el;
      });
      return els;
    };
    // faint lat/long grid over the map (world space); pass the scene's projection G and bounds
    K.grid = (G, lat0, lat1, lon0, lon1, step, t) => {
      const g = document.createElementNS(NS, "g");
      let h = "";
      for (let la = Math.ceil(lat0 / step) * step; la <= lat1; la += step) { const a = G(la, lon0), b = G(la, lon1); h += `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}"/>`; }
      for (let lo = Math.ceil(lon0 / step) * step; lo <= lon1; lo += step) { const a = G(lat0, lo), b = G(lat1, lo); h += `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}"/>`; }
      g.innerHTML = h; g.setAttribute("stroke", "rgba(60,50,30,0.22)"); g.setAttribute("stroke-width", "1.5"); g.setAttribute("stroke-dasharray", "6 8");
      ov.insertBefore(g, ov.firstChild); gsap.set(g, { opacity: 0 }); tl.to(g, { opacity: 1, duration: 1.5 }, t || 0);
      return g;
    };

    // TERRITORY (K&G-style): soft translucent fill of the ground each side holds, clipped to land by a mask PNG
    // (e.g. assets/isthmus_land.png, white = land). K.territory returns the polygon; K.lose fades it away
    // (ground lost), K.shift moves its edge (same point count) to show an advance or retreat.
    K.territory = (o) => {
      let layer = document.getElementById("fxk-terr");
      if (!layer) {
        layer = document.createElement("div"); layer.id = "fxk-terr";
        const m = o.mask ? `-webkit-mask-image:url(${o.mask});mask-image:url(${o.mask});-webkit-mask-size:2880px 1620px;mask-size:2880px 1620px;` : "";
        layer.style.cssText = `position:absolute;left:0;top:0;width:2880px;height:1620px;pointer-events:none;${m}`;
        layer.innerHTML = `<svg viewBox="0 0 2880 1620" width="2880" height="1620" style="position:absolute;inset:0"><defs><filter id="fxk-soft" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="${o.soft || 7}"/></filter></defs></svg>`;
        document.getElementById("world").insertBefore(layer, ov);
      }
      const sv = layer.querySelector("svg");
      const poly = document.createElementNS(NS, "polygon");
      poly.setAttribute("points", o.pts.map((q) => q.join(",")).join(" "));
      poly.setAttribute("fill", COL[o.side] || o.side); poly.setAttribute("filter", "url(#fxk-soft)"); poly.setAttribute("opacity", "0");
      sv.appendChild(poly);
      tl.to(poly, { opacity: o.alpha || 0.3, duration: o.dur || 1.5, ease: "sine.inOut" }, o.t);
      if (o.until != null) tl.to(poly, { opacity: 0, duration: 1.2 }, o.until);
      return poly;
    };
    K.lose = (poly, t, dur = 2.2) => { // ground lost: a short flicker, then the colour fades away
      const a = +poly.getAttribute("opacity") || 0.3;
      tl.to(poly, { opacity: 0.12, duration: 0.18, yoyo: true, repeat: 3, ease: "none" }, t);
      tl.to(poly, { opacity: 0, duration: dur, ease: "sine.in" }, t + 0.75);
    };
    // call once at the end of the scene: keeps the territory above night/dawn layers but under units and lines
    K.raiseTerritory = () => { const l = document.getElementById("fxk-terr"); if (l) document.getElementById("world").insertBefore(l, ov); };
    K.shift = (poly, pts, t, dur = 2.5) => tl.to(poly, { attr: { points: pts.map((q) => q.join(",")).join(" ") }, duration: dur, ease: "power1.inOut" }, t);

    // FADE-FROM-THE-FRONT tint (K&G-style): colour strongest right behind a front edge, fading to nothing
    // within `depth` px. dir = +1 tints the side to the right of the edge's travel direction, -1 the left.
    // Stacked layers give the gradient; `to` + moveT/moveDur move it with the front; K.lose works per layer.
    K.frontTint = (o) => {
      const n = o.layers || 5, depth = o.depth || 140, dir = o.dir || 1;
      const off = (pts, d) => pts.map((p, i) => {
        const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
        const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
        return [p[0] - (dy / L) * d, p[1] + (dx / L) * d];
      });
      const band = (edge, k) => { // edge extended at both ends so the tint doesn't stop short
        const ext = (a, b) => { const dx = a[0] - b[0], dy = a[1] - b[1], L = Math.hypot(dx, dy) || 1; return [a[0] + dx / L * 170, a[1] + dy / L * 170]; };
        const e = [ext(edge[0], edge[1]), ...edge, ext(edge[edge.length - 1], edge[edge.length - 2])]; // run a little past the line ends
        return [...e, ...off(e, dir * depth * (k + 1) / n).reverse()];
      };
      const polys = [];
      for (let k = 0; k < n; k++) {
        const pl = K.territory({ pts: band(o.pts, k), side: o.color || TINT[o.side] || o.side, t: o.t, dur: o.dur, alpha: (o.alpha || 0.28) / n * 1.6, mask: o.mask, soft: o.soft || 24, until: o.until });
        if (o.to) K.shift(pl, band(o.to, k), o.moveT, o.moveDur || 2.5);
        polys.push(pl);
      }
      return polys;
    };

    // NIGHT MODE (locked style): while a night overlay is up, front lines switch to the fully muted palette and
    // lines + territory get a brightness boost so they stay readable; everything returns at dawn.
    // K.night({ lines: [frontGroup, ...], tOn, tOff })  — call after the fronts/territory exist.
    K.night = (o) => {
      const toNight = {}; Object.keys(LINE_DAY).forEach((k) => { toNight[LINE_DAY[k]] = LINE_NIGHT[k]; });
      (o.lines || []).forEach((g) => g.querySelectorAll("path").forEach((p, i) => {
        const c = p.getAttribute("stroke"); if (!toNight[c]) return;
        const on = { attr: { stroke: toNight[c] }, duration: 2.5 }, off = { attr: { stroke: c }, duration: 3 };
        if (i < 2) { on.opacity = 0.3; off.opacity = +p.getAttribute("opacity"); }
        tl.to(p, on, o.tOn); if (o.tOff != null) tl.to(p, off, o.tOff);
      }));
      const els = [document.getElementById("fxk-terr"), ...(o.lines || [])].filter(Boolean);
      els.forEach((el) => {
        tl.fromTo(el, { filter: "brightness(1) saturate(1)" }, { filter: "brightness(1.8) saturate(1.25)", duration: 2.5, immediateRender: false }, o.tOn);
        if (o.tOff != null) tl.to(el, { filter: "brightness(1) saturate(1)", duration: 3 }, o.tOff);
      });
    };
    // BOMBING RUN (locked, owner's favourite = the Goose Green Harrier strike): the jet flies the run with its roar, each
    // bomb lands just after it passes (0.25 s apart) with fireball, smoke and the real explosion boom, and the SCREEN
    // SHAKES on the first bomb. Use this for every air strike; don't hand-roll bombs. bombs: [[x, y], ...]
    K.bombRun = (o) => {
      const t0 = o.t, dur = o.dur || 3.2;
      K.aircraft({ kind: o.kind || "jet", side: o.side || "carth", size: o.size || 84, alt: o.alt || 30, pts: o.pts, t: t0, dur, until: t0 + dur });
      o.bombs.forEach((b, k) => K.impact(b[0], b[1], t0 + 1.55 + k * 0.25, { r: 20, shake: k ? false : 5 }));
    };
    return K;
  };
})();
