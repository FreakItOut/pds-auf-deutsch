// es_struct_probe.js — probe structure around ES member0 text region and
// find S!S-style block headers anywhere in member0.
const fs = require('fs');
const m0 = fs.readFileSync('_work/cd1_0.bin');
console.log('len', m0.length);

// probe: 12-byte header 00 / ff x10 / 00 signature
const SIG = Buffer.from([0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00]);
let idx = 0, hits = [];
while ((idx = m0.indexOf(SIG, idx)) !== -1) { hits.push(idx); idx += 12; }
console.log('S!S 12-byte headers in member0:', hits.length);
if (hits.length) {
  console.log('first 10 offsets:', hits.slice(0, 10).map(h => '0x' + h.toString(16)).join(' '));
  // check pitch regularity near our range
  const near = hits.filter(h => h > 0x100000 && h < 0x400000);
  console.log('headers in 0x100000..0x400000:', near.length);
  if (near.length > 2) {
    const pitches = {};
    for (let k = 1; k < Math.min(near.length, 300); k++) {
      const d = near[k] - near[k - 1];
      pitches[d] = (pitches[d] || 0) + 1;
    }
    console.log('pitch histogram (top 8):',
      Object.entries(pitches).sort((a, b) => b[1] - a[1]).slice(0, 8)
        .map(e => e[0] + 'x' + e[1]).join(' '));
    // labels around ES text at 0x1d81a9
    const around = near.filter(h => h > 0x1d7000 && h < 0x1d9000);
    console.log('headers inside 0x1d7000..0x1d9000:', around.map(h => '0x' + h.toString(16)).join(' '));
  }
  // print labels of first 12 headers overall
  const labels = hits.slice(0, 20).map(h =>
    '0x' + h.toString(16) + ':' + m0.slice(h + 12, h + 16).toString('hex'));
  console.log('first labels:\n  ' + labels.join('\n  '));
}
