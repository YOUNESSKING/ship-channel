// Template runtime (from the approved v9 anim.js). All times are absolute chapter seconds (the builder computes them).
const tl = gsap.timeline({ paused: true });
const hidden = (sel) => gsap.set(sel, { opacity: 0 });
// slow push on a whole clip / shot
function kb(sel, a, b, from, to, origin) {
  tl.fromTo(sel, { scale: from, transformOrigin: origin || '50% 50%' }, { scale: to, duration: b - a, ease: 'none' }, a);
}
// instant zoom step (a "jump")
function jump(sel, t, scale, origin) { tl.set(sel, { scale: scale, transformOrigin: origin || '50% 50%' }, t); }
// quiet fade + slight rise (icons: small scale-in)
function pop(sel, t, d, o) {
  o = o || {};
  if (o.icon) { tl.fromTo(sel, { scale: o.from || .5, opacity: 0, svgOrigin: o.svgOrigin, transformOrigin: o.origin }, { scale: 1, opacity: 1, duration: .3, ease: 'power2.out', svgOrigin: o.svgOrigin, transformOrigin: o.origin }, t); return; }
  const b = o.base || 0;
  tl.fromTo(sel, { opacity: 0, y: b + 12 }, { opacity: 1, y: b, duration: .5, ease: 'power2.out' }, t);
}
// slow cinematic fades (no bounce)
function drop(sel, t) { tl.fromTo(sel, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 1.1, ease: 'power2.out' }, t); }
function write(sel, t, d) { tl.fromTo(sel, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: Math.max(d || .8, .8), ease: 'power2.out' }, t); }
function underline(sel, t, d) {
  const el = document.querySelector(sel);
  if (el && el.tagName.toLowerCase() === 'path') tl.fromTo(sel, { strokeDashoffset: 1, opacity: 0 }, { strokeDashoffset: 0, opacity: 1, duration: d || .4, ease: 'power1.out' }, t);
  else tl.fromTo(sel, { scaleX: 0, opacity: 1, transformOrigin: '50% 50%' }, { scaleX: 1, duration: d || .8, ease: 'power2.out', transformOrigin: '50% 50%' }, t);
}
function fadeIn(sel, t, d) { tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: d || 0.12 }, t); }
// stick figure
function pose(p, hx, hy, s, o) {
  const sy = hy - 78 * s;
  gsap.set('#' + p + '-armL', { svgOrigin: hx + ' ' + sy, rotation: o.aL });
  gsap.set('#' + p + '-armR', { svgOrigin: hx + ' ' + sy, rotation: o.aR });
  gsap.set('#' + p + '-legL', { svgOrigin: hx + ' ' + hy, rotation: o.lL });
  gsap.set('#' + p + '-legR', { svgOrigin: hx + ' ' + hy, rotation: o.lR });
}
function flail(p, hx, hy, s, t0, dur, a0, a1, per) {
  const sy = hy - 78 * s, n = Math.max(1, Math.round(dur / per));
  tl.fromTo('#' + p + '-armL', { rotation: a0, svgOrigin: hx + ' ' + sy }, { rotation: a1, svgOrigin: hx + ' ' + sy, duration: per, yoyo: true, repeat: n, ease: 'sine.inOut' }, t0);
  tl.fromTo('#' + p + '-armR', { rotation: -a1, svgOrigin: hx + ' ' + sy }, { rotation: -a0, svgOrigin: hx + ' ' + sy, duration: per, yoyo: true, repeat: n, ease: 'sine.inOut' }, t0 + per * .5);
  tl.fromTo('#' + p + '-legL', { rotation: 8, svgOrigin: hx + ' ' + hy }, { rotation: 28, svgOrigin: hx + ' ' + hy, duration: per * 1.1, yoyo: true, repeat: n, ease: 'sine.inOut' }, t0);
  tl.fromTo('#' + p + '-legR', { rotation: -28, svgOrigin: hx + ' ' + hy }, { rotation: -8, svgOrigin: hx + ' ' + hy, duration: per * 1.1, yoyo: true, repeat: n, ease: 'sine.inOut' }, t0);
}
function bob(sel, t0, dur, amp, per) {
  tl.fromTo(sel, { y: 0 }, { y: amp, duration: per, yoyo: true, repeat: Math.max(1, Math.round(dur / per)), ease: 'sine.inOut' }, t0);
}
function drift(sel, t0, dur, dx) { tl.fromTo(sel, { x: 0 }, { x: dx || -220, duration: dur, ease: 'none' }, t0); }
// timer bar marker + gold progress
function mark(p, t0, from, to, d) {
  gsap.set('#' + p + '-mk', { x: from });
  tl.to('#' + p + '-mk', { x: to, duration: d || .4, ease: 'power2.inOut' }, t0);
  tl.fromTo('#' + p + '-prog', { attr: { x2: from } }, { attr: { x2: to }, duration: d || .4, ease: 'power2.inOut' }, t0);
}
// animated counter: fmt(v) returns the html of the number
function counter(sel, t, dur, from, to, fmt, ease) {
  const o = { v: from }, el = document.querySelector(sel);
  if (el) el.innerHTML = fmt(from);
  tl.fromTo(o, { v: from }, { v: to, duration: dur, ease: ease || 'power2.inOut', immediateRender: false, onUpdate: () => { if (el) el.innerHTML = fmt(o.v); } }, t);
}
