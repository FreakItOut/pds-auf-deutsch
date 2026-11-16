// Diff EU CAMPSCR0.PNB vs ES member0 region at 0x1dab800 (same size 0x1c400).
const fs = require('fs');
const eu = fs.readFileSync('_work/CAMPSCR0.PNB');
const es = fs.readFileSync('_work/cd1_0.bin').slice(0x1dab800, 0x1dab800 + eu.length);
console.log('EU len', eu.length, 'ES slice len', es.length);
// count differing bytes
let diff = 0, firstDiff = -1, lastDiff = -1;
const runs = [];
let inRun = false, runStart = 0;
for (let i = 0; i < eu.length; i++) {
  if (eu[i] !== es[i]) {
    diff++;
    if (!inRun) { inRun = true; runStart = i; }
    lastDiff = i;
  } else {
    if (inRun) { runs.push({ start: runStart, end: i - 1, len: i - runStart }); inRun = false; }
  }
}
if (inRun) runs.push({ start: runStart, end: eu.length - 1, len: eu.length - runStart });
console.log('differing bytes:', diff, 'of', eu.length, '(' + (100 * diff / eu.length).toFixed(2) + '%)');
console.log('diff runs:', runs.length);
console.log('top 10 diff runs by length:');
runs.sort((a, b) => b.len - a.len).slice(0, 10).forEach(r =>
  console.log('  0x' + r.start.toString(16), 'len', r.len));
// show first diff run context
if (runs.length) {
  const r = runs.sort((a, b) => a.start - b.start)[0];
  console.log('first diff run @0x' + r.start.toString(16) + ' len ' + r.len);
  const s = Math.max(0, r.start - 16), e = Math.min(eu.length, r.start + r.len + 16);
  console.log('EU:', eu.slice(s, e).toString('hex'));
  console.log('ES:', es.slice(s, e).toString('hex'));
}
