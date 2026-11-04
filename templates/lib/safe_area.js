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
      if (bot > SAFE_B) { b.style.top = (cur - (bot - SAFE_B) - 6) + 'px'; log.push(`lift ${(bot - SAFE_B + 6).toFixed(0)}px: ${b.textContent.trim().slice(0, 30)}`); }
      else if (right > TR_X && top < TR_Y && left > W * 0.5) { b.style.top = (cur + (TR_Y - top) + 6) + 'px'; log.push(`down ${(TR_Y - top + 6).toFixed(0)}px: ${b.textContent.trim().slice(0, 30)}`); }
    });
    window.__safeLog = (window.__safeLog || []).concat(log);
  }
  pass();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(pass);
})();
