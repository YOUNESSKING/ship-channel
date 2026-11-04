// CLEAN SCREEN (LOCKED, owner 2026-10-31, STYLE_LOCK 2b). Paste/keep these in every map scene (copied from the
// approved test cleburne/scenes/testv11, reference reference/style-reference-maplook-v11.mp4).

// 1) Nation flags: the flag only, NO country name under it ("UNITED STATES", "CONFEDERATE STATES"... are gone).
const flag = (src, name, x, y, t, until, w = 76) => GG.pin(`<div style="display:flex;flex-direction:column;align-items:center"><img src="${src}" style="width:${w}px;display:block;border:${Math.max(0.6, w / 60).toFixed(1)}px solid #1a1712;box-shadow:0 ${w * 0.025}px ${w * 0.07}px rgba(0,0,0,0.55)"></div>`, x, y, { t, pop: true, until });

// 2) Words on screen leave after ~3.5 s: captions (what the narrator says), place-name boxes, town names, map stamps,
//    belief cards. Unit names under the counters stay with their counters.
const LBL_LIFE = 3.5;
const _cap0 = B.caption.bind(B); B.caption = (txt, t, until, ...r) => _cap0(txt, t, Math.min(until ?? 1e9, t + LBL_LIFE), ...r);
const boxS = (txt, x, y, t, until, o = {}) => pinS(box(txt, x, y, t, o.size || 32, Math.min(until ?? 1e9, t + LBL_LIFE), o));
const wstampS = (txt, x, y, t, until, c, size = 22) => pinS(wstamp(txt, x, y, t, Math.min(until ?? 1e9, t + LBL_LIFE), c, size));
// town(): after pinS(el) add   tl.to(el, { autoAlpha: 0, duration: 0.8 }, t + LBL_LIFE + 0.5);
// belief(txt, sub, t, until):  pass Math.min(until, t + LBL_LIFE)

// 3) Option 1 (territory colours) -> option 2 (front lines only) is SEAMLESS: the colour dissolves over ~2.8 s during
//    the camera dive, never switched off in one frame; when colours return they fade in over ~2.2 s.
const terr = (file, t, until, dur = 1.0, outDur = dur) => { const el = document.createElement("img"); el.className = "wimg terr"; el.src = file; el.alt = "";
  Object.assign(el.style, { left: "0px", top: "0px", width: "2880px", height: "1620px", mixBlendMode: "multiply" });
  WORLD.insertBefore(el, OVL); gsap.set(el, { autoAlpha: 0 });
  tl.fromTo(el, { autoAlpha: 0 }, { autoAlpha: 1, duration: dur, immediateRender: false }, t);
  if (until != null) tl.to(el, { autoAlpha: 0, duration: outDur, ease: "sine.inOut" }, until); return el; };
// usage: terr(CTL, 0, T_DIVE_START, 0.01, 2.8);   return:  tl.fromTo(L, { opacity: 0 }, { opacity: 1, duration: 2.2, ease: "sine.inOut", immediateRender: false }, T);
