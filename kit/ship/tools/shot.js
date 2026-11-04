// Screenshot an HTML page with headless Chrome (playwright from the global node modules).
// NODE_PATH=$(npm root -g) node kit/ship/tools/shot.js PAGE.html OUT.png [width height]
const { chromium } = require("playwright");
(async () => {
  const [page_, out, w = "1920", h = "1080"] = process.argv.slice(2);
  const exe = ["/usr/bin/google-chrome", "/usr/bin/chromium"].find((p) => require("fs").existsSync(p));
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await b.newPage({ viewport: { width: +w, height: +h } });
  await p.goto("file://" + require("path").resolve(page_));
  await p.waitForTimeout(400);
  await p.screenshot({ path: out, fullPage: true });
  await b.close(); console.log("wrote", out);
})();
