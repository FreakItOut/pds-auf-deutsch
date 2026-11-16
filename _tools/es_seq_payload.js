// es_seq_payload.js — Hypothesis: member0 = sequential payloads in dir order,
// each rounded up to 0x800. Locate BTL_A5.FNT's payload and test for text.
const fs = require('fs');
const entries = fs.readFileSync('_work/es_dir_entries.csv', 'latin1')
  .split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { name: p[0], dirOff: +p[1], p0: +p[2], p1: +p[3] }; });
console.log('entries:', entries.length);

// cumulative offsets, rounded up to 0x800
let off = 0;
const map = [];
for (const e of entries) {
  map.push({ name: e.name, p0: e.p0, p1: e.p1, seqOff: off });
  off += Math.ceil(e.p1 / 2048) * 2048;
}
console.log('total sequential payload size:', off, '(0x' + off.toString(16) + ') member0 len: 0x1BD5FF9');

function show(name) {
  const e = map.find(x => x.name === name);
  if (!e) { console.log(name, 'not in list'); return; }
  console.log(name, 'seqOff 0x' + e.seqOff.toString(16), 'size', e.p1,
    'pair0', e.p0, '(0x' + (e.p0 * 2048).toString(16) + ')');
  return e;
}
// alternative per-file targets
const m0 = fs.readFileSync('_work/cd1_0.bin');
function testWindow(e, off, size) {
  const w = m0.slice(off, off + size);
  const c1 = w.indexOf('Contraataque'), c2 = w.indexOf('Counterattack'),
    c3 = w.indexOf('Personalizar'), c4 = w.indexOf('Customize Gun');
  console.log('   test@0x' + off.toString(16), 'size', size,
    'Contraataque:' + (c1 >= 0 ? 'Y@0x' + c1.toString(16) : 'n'),
    'Counterattack:' + (c2 >= 0 ? 'Y@0x' + c2.toString(16) : 'n'),
    'Personalizar:' + (c3 >= 0 ? 'Y@0x' + c3.toString(16) : 'n'),
    'CustomizeGun:' + (c4 >= 0 ? 'Y@0x' + c4.toString(16) : 'n'));
}
const a5 = show('BTL_A5.FNT;1');
if (a5) testWindow(a5, a5.seqOff, a5.p1);
const a3 = show('BTL_A3.FNT;1');
if (a3) testWindow(a3, a3.seqOff, a3.p1);
// The known Spanish text at 0x1d81a9: which candidate covers 0x1d81a9?
const K = 0x1d81a9;
let prev = null;
for (const e of map) {
  if (e.seqOff > K) break;
  prev = e;
}
console.log('sequential-owner of 0x1d81a9:', prev && prev.name, '(payload 0x' + (prev && prev.seqOff).toString(16), '..', '+', prev && prev.p1, ')');
if (prev) {
  // offset of the Spanish table within its payload:
  const inOff = K - prev.seqOff;
  console.log('  table offset inside payload: 0x' + inOff.toString(16));
  // what does EU say at that offset? EU files exist for some
  const euPath = '_work/' + prev.name.replace(';1', '');
  if (fs.existsSync(euPath)) {
    const eu = fs.readFileSync(euPath);
    const n = Math.min(0x600, eu.length - inOff);
    let printable = 0;
    for (let j = inOff; j < inOff + n; j++) {
      const x = eu[j];
      if ((x >= 0x20 && x <= 0x7e) || (x >= 0x85 && x <= 0x91)) printable++;
    }
    console.log('  EU', prev.name, 'printable at same payload-offset region:', printable + '/' + n, '(' + (100 * printable / n).toFixed(0) + '%)');
    console.log('  EU.exe bytes:', eu.slice(inOff, inOff + 32).toString('hex'));
  }
}
