// es_layout_test.js — Re-test ES member0 payload mapping with correct understanding:
// EU script files consist of 0x800-pitch S!S blocks (12-byte header 00 ff*10 00 +
// 4-byte label). If ES member0 is a rebuild where file payload starts at
// dir-LBA*0x800, then the ES counterpart of EU BTL_A5.FNT's table offset
// 0x5f6c4 should also be plaintext Spanish.
const fs = require('fs');
const m0 = fs.readFileSync('_work/cd1_0.bin');
console.log('member0 len', m0.length);

// 1) parse the member0 directory: records start with 62 01 1d 01
const SIGDIR = Buffer.from([0x62, 0x01, 0x1d, 0x01]);
const entries = [];
let p = 0x63e;
while (p < m0.length - 40) {
  if (m0[p] === 0x62 && m0[p + 1] === 0x01 && m0[p + 2] === 0x1d && m0[p + 3] === 0x01) {
    const nl = m0[p + 14];
    if (nl >= 1 && nl <= 40) {
      const name = m0.slice(p + 15, p + 15 + nl).toString('latin1');
      let ok = /^[A-Za-z0-9_\-.]+(;1)?$/i.test(name);
      if (ok) {
        // mirrored u32 pairs after name + NUL
        let q = p + 15 + nl;
        while (m0[q] === 0) q++;
        const pairs = [];
        for (let k = 0; k + 8 <= 32; k += 8) {
          const a = m0.readUInt32LE(q + k), b2 = m0.readUInt32BE(q + k + 4);
          if (a === b2) pairs.push(a); else break;
        }
        if (pairs.length >= 2) {
          entries.push({ off: p, name, lba: pairs[0], size: pairs[1], ext: pairs.length });
        }
      }
    }
    p = entries.length ? entries[entries.length - 1].off + 1 : p + 1;
    p = Math.max(p, entries.length ? entries[entries.length - 1].off + 15 + nl + 20 : p);
  } else p++;
  if (entries.length > 1700) break;
}
console.log('dir entries parsed:', entries.length);
const btl = entries.filter(e => /^BTL_A5/i.test(e.name));
for (const e of btl) console.log(' ', e.name, 'dirOff 0x' + e.off.toString(16), 'LBA', e.lba, '(0x' + e.lba.toString(16) + ')', 'size', e.size);

// 2) For each candidate LBA, test hypotheses: base = lba*0x800, lba*2352+16, etc.
const EU_TEXT_OFF = 0x5f6c4; // 'Counterattack' in EU BTL_A5.FNT
const eu = fs.readFileSync('_work/BTL_A5.FNT');
console.log('EU BTL_A5 text-off 0x' + EU_TEXT_OFF.toString(16),
  'eu[0x5f6c4..]:', eu.slice(EU_TEXT_OFF, EU_TEXT_OFF + 16).toString('hex'));
console.log('(EU interprets as "Contraataque" line); looking for Spanish equivalent in member0');

const isP = ch => (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x85 && ch <= 0x91);
for (const e of btl.filter(x => /FNT/i.test(x.name))) {
  for (const mul of [2048, 2352]) {
    for (const skip of [0, 16]) {
      const pos = e.lba * mul + skip;
      if (pos < 0 || pos + 0x61000 > m0.length) continue;
      const w = m0.slice(pos + EU_TEXT_OFF - 0x40, pos + EU_TEXT_OFF + 0x80);
      let printable = 0;
      for (const x of w) if (isP(x)) printable++;
      console.log(' ', e.name, 'LBA*' + mul + '+' + skip,
        'offset 0x' + (pos + EU_TEXT_OFF).toString(16),
        'printable/192:', printable, 'hex-', w.slice(0x30, 0x40).toString('hex'));
    }
  }
}

// 3) Also: where exactly is the ES 'Báldor' table (0x1d81a9) — what block /
//     nearby signature belongs there?
const T = 0x1d81a9;
let bx = T - (T % 0x800);
console.log('\nES table at 0x1d81a9; block-aligned start candidates:');
for (const d of [0x800, 0x1000, 0x2000]) {
  const bstart = T - (T % d);
  const sig = m0[bstart] === 0x00 && m0[bstart + 1] === 0xff;
  console.log('   pitch 0x' + d.toString(16), 'block@0x' + bstart.toString(16),
    'header:', sig ? 'S!S?' + m0.slice(bstart + 12, bstart + 16).toString('hex') : m0.slice(bstart, bstart + 8).toString('hex'),
    'delta', '0x' + (T - bstart).toString(16));
}
