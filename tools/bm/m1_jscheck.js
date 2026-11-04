// move-1 agent: load a built scene in headless chrome and print page errors.  node tools/m1_jscheck.js SCENE
const path = require("path"), pp = require("/opt/node22/lib/node_modules/hyperframes/node_modules/puppeteer-core");
(async () => {
  const b = await pp.launch({ executablePath: "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell", args: ["--no-sandbox", "--allow-file-access-from-files"] });
  const p = await b.newPage(); p.on("pageerror", (e) => console.log("ERR", e.message)); p.on("console", (m) => { if (m.type() === "error") console.log("CON", m.text()); });
  await p.goto("file://" + path.resolve("scenes/" + process.argv[2] + "/index.html")); await new Promise((r) => setTimeout(r, 1500)); await b.close(); })();
