const { chromium } = require('playwright');
(async () => {
  const [,, src, out, w] = process.argv;
  const b = await chromium.launch({args:['--allow-file-access-from-files']});
  const p = await b.newPage({ viewport: { width: +w || 1600, height: 900 }, deviceScaleFactor: 1 });
  await p.goto('file://' + src); await p.waitForTimeout(300);
  await p.screenshot({ path: out, fullPage: true }); await b.close();
})();
