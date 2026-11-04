// rasterize a kit SVG to a transparent PNG with the preinstalled Chromium (no extra deps)
const { chromium } = require("playwright"); const fs = require("fs");
(async () => {
  const [src, out, w] = process.argv.slice(2); const svg = fs.readFileSync(src, "utf8");
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w, height: 400 } });
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace(/width="\d+" height="\d+"/, `width="${w}"`)}</body></html>`);
  const el = await p.$("svg"); await el.screenshot({ path: out, omitBackground: true }); await b.close();
})();
