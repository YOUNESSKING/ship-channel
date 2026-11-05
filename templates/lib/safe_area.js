// Ship-channel safe-area + type-size pass (chapter key "safe": true, on by default with "font": "oswald").
// Runs once when the page loads (static layout, before any seek), and again after the fonts load:
//  - every text element is at least MIN_PX tall in the 1280x720 stage (25.4 px = 38 px at 1080p = 3.5 % of frame height);
//  - a text block whose bottom falls in the bottom 10 % (YouTube player bar / mobile scrubber) is lifted above it;
//  - a text block in the top-right corner (YouTube card / info overlays: right 20 %, top 12 %) is pushed down out of it.
// Only `top` / `font-size` are changed, never transforms, so GSAP tweens on the same elements keep working.
(function () {
  const W = 1280, H = 720, MIN_PX = 25.4, SAFE_B = H * 0.9, TR_X = W * 0.8, TR_Y = H * 0.12;
  const root = document.getElementById('root'); if (!root) return;
  const textEls = () => Array.from(root.querySelectorAll('*')).filter((e) => !['SCRIPT', 'STYLE', 'VIDEO', 'svg', 'defs', 'clipPath'].includes(e.tagName) &&
    Array.from(e.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim()));
  const blockOf = (e) => e.closest('.blk, .an-a, .abs') || e;
  function pass() {
    const k = root.getBoundingClientRect().width / W || 1;
    const log = [];
    textEls().forEach((e) => { const fs = parseFloat(getComputedStyle(e).fontSize) || 0;
      if (fs && fs < MIN_PX) { e.style.fontSize = MIN_PX + 'px'; log.push(`size ${fs}->${MIN_PX}: ${e.textContent.trim().slice(0, 30)}`); } });
    const seen = new Set();
    textEls().forEach((e) => { const b = blockOf(e); if (seen.has(b)) return; seen.add(b);
      if (getComputedStyle(b).position !== 'absolute') return;
      const r = b.getBoundingClientRect(), rr = root.getBoundingClientRect(); if (!r.height) return;
      const top = (r.top - rr.top) / k, bot = (r.bottom - rr.top) / k, right = (r.right - rr.left) / k, left = (r.left - rr.left) / k;
      const cur = parseFloat(getComputedStyle(b).top) || 0;
      // DROP = runtime.js drop() entry offset (y: 12): the block rises from 12 px lower, so lift it far enough that it stays
      // out of the bottom 10 % during its entry too (Oriskany full c03 "TELL US THEIR STORY" sat 1 px in the zone while fading in)
      const DROP = 12;
      if (bot + DROP > SAFE_B) { b.style.top = (cur - (bot + DROP - SAFE_B) - 6) + 'px'; log.push(`lift ${(bot + DROP - SAFE_B + 6).toFixed(0)}px: ${b.textContent.trim().slice(0, 30)}`); }
      else if (right > TR_X && top < TR_Y && left > W * 0.5) { b.style.top = (cur + (TR_Y - top) + 6) + 'px'; log.push(`down ${(TR_Y - top + 6).toFixed(0)}px: ${b.textContent.trim().slice(0, 30)}`); }
    });
    // shrink-to-fit (Oriskany full v2, critic A M2): a text line wider than its box or than the frame minus a 64 px side margin
    // (96 px at 1080p) is scaled down until it fits; if that would take any text under MIN_PX, the line wraps instead.
    const M = 64, lines = new Set();
    textEls().forEach((e) => { let L = e; while (L && L !== root && getComputedStyle(L).display === 'inline') L = L.parentElement; if (L && L !== root) lines.add(L); });
    lines.forEach((L) => {
      if (L.dataset.fit) return;
      const rg = document.createRange(); rg.selectNodeContents(L); const rt = rg.getBoundingClientRect(), rr = root.getBoundingClientRect();
      if (!rt.width) return;
      const c = blockOf(L), cr = c.getBoundingClientRect(), hasW = !!(c.style && c.style.width);
      const tl = (rt.left - rr.left) / k, tr = (rt.right - rr.left) / k, cl = (cr.left - rr.left) / k, crr = (cr.right - rr.left) / k;
      const aL = Math.max(M, hasW ? cl : Math.min(tl, W - M)), aR = Math.min(W - M, hasW ? crr : W - M), need = tr - tl, avail = aR - aL;
      if (need <= avail + 0.5 && tl >= M - 0.5 && tr <= W - M + 0.5) return;
      const f = Math.min(1, avail / need) * 0.98;
      const els = [L, ...L.querySelectorAll('*')].filter((x) => Array.from(x.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim()));
      const sizes = els.map((x) => parseFloat(getComputedStyle(x).fontSize) || 0);
      L.dataset.fit = '1';
      if (sizes.every((s) => s * f >= MIN_PX)) { els.forEach((x, i) => { x.style.fontSize = (sizes[i] * f).toFixed(2) + 'px'; }); log.push(`fit x${f.toFixed(2)}: ${L.textContent.trim().slice(0, 30)}`); }
      else { L.style.whiteSpace = 'normal'; L.querySelectorAll('*').forEach((x) => { x.style.whiteSpace = 'normal'; }); L.style.maxWidth = avail + 'px'; { const ta = getComputedStyle(L).textAlign; if (ta === 'center') { L.style.marginLeft = L.style.marginRight = 'auto'; } else if (ta === 'right' || ta === 'end') L.style.marginLeft = 'auto'; } if (!hasW && c === L) L.style.width = avail + 'px'; log.push(`wrap: ${L.textContent.trim().slice(0, 30)}`); }
      if (!hasW && tl < M) { const cur = parseFloat(getComputedStyle(c).left) || 0; c.style.left = (cur + (M - tl)) + 'px'; }
    });
    window.__safeLog = (window.__safeLog || []).concat(log);
  }
  pass();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(pass);
})();
