// Theory test: member0 = [dir][payload blobs sequentially, in dir order];
// dir.lba = US-disc sector (write-back target). Match 'Contraataque' hits to
// payload boundaries.
const fs = require('fs');
const s = fs.readFileSync('_work/cd1_0.bin');
const HDR = Buffer.from('62011d01', 'hex');
function nextHdr(from) {
  let i = from;
  for (;;) {
    i = s.indexOf(HDR, i);
    if (i < 0) return -1;
    if (s[i + 4] === 0 && s[i + 5] === 0 && s[i + 6] === 0x04 && s[i + 10] === 0x01) return i;
    i++;
  }
}
let o = 0x63e;
const recs = [];
while (o >= 0 && o < 0x17800) {
  const nl = s[o + 14];
  if (nl < 4 || nl > 40) break;
  const name = s.slice(o + 15, o + 15 + nl).toString('latin1');
  let p = o + 15 + nl, f = -1;
  for (let k = 0; k < 24; k++) {
    if (s[p + k] === s[p + k + 7] && s[p + k + 1] === s[p + k + 6] && s[p + k + 2] === s[p + k + 5] && s[p + k + 3] === s[p + k + 4]) { f = k; break; }
  }
  let lba = 0, size = 0;
  if (f >= 0) {
    const q = p + f;
    lba = s[q] | (s[q + 1] << 8) | (s[q + 2] << 16) | (s[q + 3] << 24);
    size = s[q + 8] | (s[q + 9] << 8) | (s[q + 10] << 16) | (s[q + 11] << 24);
  }
  recs.push({ name, lba, size });
  const nx = nextHdr(o + 34 + nl - 1);
  if (nx < 0) break;
  o = nx;
}
console.log('records:', recs.length);
const dirEnd = o + 34 + s[o + 14];
console.log('dirEnd approx:', '0x' + dirEnd.toString(16));

// cumulative payload offsets
let cum = dirEnd;
const cums = [];
for (const r of recs) {
  cums.push({ name: r.name, start: cum, end: cum + r.size });
  cum += r.size;
}
console.log('total cumulative end:', '0x' + cum.toString(16), '(member size', s.length + ')', cum <= s.length ? 'FITS' : 'OVERFLOWS');

// map 'Contraataque' hits
const hits = [];
{
  let i = 0;
  for (;;) { i = s.indexOf('Contraataque', i); if (i < 0) break; hits.push(i); i++; }
}
console.log('Contraataque hits:', hits.length);
for (const h of hits.slice(0, 10)) {
  const rec = cums.find(r => h >= r.start && h < r.end);
  if (rec) {
    const rel = h - rec.start;
    console.log('0x' + h.toString(16), '->', rec.name, 'rel 0x' + rel.toString(16), '(len', rec.name.length, ')');
  } else {
    // which record (by LBA mapping)? fallback
    console.log('0x' + h.toString(16), '-> NO cumulative match');
  }
}
