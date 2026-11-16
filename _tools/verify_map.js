// verify_map.js — proof that member0 payload = dir-pair0 * 2048.
// Diff ES slice vs EU file for CAMPSCR0.PNB and BTL_A5.FNT candidates.
const fs = require('fs');
const m0 = fs.readFileSync('_work/cd1_0.bin');

function diff(name, esOff, esSize) {
  const euPath = '_work/' + name;
  if (!fs.existsSync(euPath)) { console.log(name, 'missing EU extract'); return; }
  const eu = fs.readFileSync(euPath);
  const n = Math.min(esSize, eu.length);
  const es = m0.slice(esOff, esOff + n);
  let match = 0;
  for (let i = 0; i < n; i++) if (eu[i] === es[i]) match++;
  console.log(name, ': esOff 0x' + esOff.toString(16), 'size', n,
    'identical bytes:', match, '/', n, '(' + (100 * match / n).toFixed(1) + '%)');
  // report first/last long identical runs
  let runs = [], inRun = false, s = 0;
  for (let i = 0; i < n; i++) {
    const same = eu[i] === es[i];
    if (same && !inRun) { inRun = true; s = i; }
    else if (!same && inRun) { if (i - s >= 64) runs.push([s, i - 1]); inRun = false; }
  }
  if (inRun && n - s >= 64) runs.push([s, n - 1]);
  console.log('  identical runs >=64B:', runs.length,
    runs.slice(0, 5).map(r => '0x' + r[0].toString(16) + '..0x' + r[1].toString(16)).join(' '));
}

// ES dir lookup from previous step
diff('CAMPSCR0.PNB', 15191 * 2048, 115712);
diff('CAMPSCR4.PNB', 15445 * 2048, 131072);
// BTL_A5 candidate
diff('BTL_A5.FNT', 5400 * 2048, 419562);
