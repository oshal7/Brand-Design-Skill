const { chromium } = require('playwright');
(async () => {
  const [,, src, outdir] = process.argv;
  const b = await chromium.launch({args:['--allow-file-access-from-files']});
  const p = await b.newPage({ viewport: { width: 1800, height: 1200 }, deviceScaleFactor: 1 });
  await p.goto('file://' + src); await p.waitForTimeout(800);
  const els = await p.$$('[data-name]');
  for (const e of els) { const n = await e.getAttribute('data-name'); await e.screenshot({ path: `${outdir}/${n}.png` }); console.log(n); }
  await b.close();
})();
