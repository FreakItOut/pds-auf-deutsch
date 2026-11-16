// es_btl_a5_blocks.js — Examine ES BTL_A5.FNT payload at member0 0xA8B000
// (size 419562): S!S block headers, pitch, labels. No text output.
const fs = require('fs');
const m0 = fs.readFileSync('_work/cd1_0.bin');
const OFF = 0xA8B000, SIZE = 419562;
const w = m0.slice(OFF, OFF + SIZE);
console.log('window len', w.length);

const SIG = Buffer.from([0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00]);
let i = 0, hits = [];
while ((i = w.indexOf(SIG, i)) !== -1) { hits.push(i); i += 12; }
console.log('S!S headers in ES BTL_A5:', hits.length);
if (hits.length > 2) {
  const pitches = {};
  for (let k = 1; k < hits.length; k++) {
    const d = hits[k] - hits[k - 1];
    pitches[d] = (pitches[d] || 0) + 1;
  }
  console.log('pitch histogram:', Object.entries(pitches).sort((a, b) => b[1] - a[1]).slice(0, 6)
    .map(e => e[0] + 'x' + e[1]).join(' '));
  console.log('first 6 labels:', hits.slice(0, 6).map(h => w.slice(h + 12, h + 16).toString('hex')).join(' '));
}

// EU comparison
const eu = fs.readFileSync('_work/BTL_A5.FNT');
let j = 0, hitsEU = [];
while ((j = eu.indexOf(SIG, j)) !== -1) { hitsEU.push(j); j += 12; }
console.log('S!S headers in EU BTL_A5:', hitsEU.length);
if (hitsEU.length > 2) {
  const p2 = {};
  for (let k = 1; k < hitsEU.length; k++) { const d = hitsEU[k] - hitsEU[k - 1]; p2[d] = (p2[d] || 0) + 1; }
  console.log('EU pitch histogram:', Object.entries(p2).sort((a, b) => b[1] - a[1]).slice(0, 6)
    .map(e => e[0] + 'x' + e[1]).join(' '));
  console.log('EU first 6 labels:', hitsEU.slice(0, 6).map(h => eu.slice(h + 12, h + 16).toString('hex')).join(' '));
}
// compare labels list equality (structure fingerprint)
function lab(hs, d) { return hs.map(h => d.slice(h + 12, h + 16).toString('hex')).join('-'); }
if (hits.length && hitsEU.length) {
  console.log('labels equal prefix:', lab(hits.slice(0, 20), w) === lab(hitsEU.slice(0, 20), eu));
}
