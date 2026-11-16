// eu_line_format.js — Identify the script-instruction bytes around text
// fragments in EVT000_1.FNT's dialog window. Prints byte patterns only.
const fs = require('fs');
const b = fs.readFileSync('_work/EVT000_1.FNT');
const isP = ch => (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x85 && ch <= 0x91);

const START = 0xc9f200, END = 0xca0500;
// fragments (len>=4)
const fr = [];
let i = START;
while (i < END) {
  if (isP(b[i])) {
    const st = i;
    while (i < END && isP(b[i])) i++;
    if (i - st >= 4) fr.push({ off: st, len: i - st });
  } else i++;
}
console.log('fragments len>=4:', fr.length);

// for each fragment: bytes before / control bytes between fragment and next
console.log('\nfragment gaps with control byte patterns:');
for (let k = 0; k < Math.min(24, fr.length - 1); k++) {
  const g0 = fr[k].off + fr[k].len, g1 = fr[k + 1].off;
  const pre = b.slice(Math.max(START, fr[k].off - 3), fr[k].off).toString('hex');
  const gap = b.slice(g0, g1);
  console.log((k + 1) + '. frag@0x' + fr[k].off.toString(16) + ' len' + fr[k].len
    + ' pre:', pre, ' gap(', gap.length, '):', gap.toString('hex').slice(0, 60));
}

// distinct control bytes frequency (non-printable between fragments)
const cb = {};
for (let k = 0; k < fr.length - 1; k++) {
  const g0 = fr[k].off + fr[k].len, g1 = fr[k + 1].off;
  for (let j = g0; j < g1; j++) {
    const x = b[j];
    if (!isP(x)) cb[x] = (cb[x] || 0) + 1;
  }
}
console.log('\ngap control byte counts (desc):',
  Object.entries(cb).sort((a, c) => c[1] - a[1]).slice(0, 20)
    .map(e => '0x' + Number(e[0]).toString(16) + ':' + e[1]).join(' '));
