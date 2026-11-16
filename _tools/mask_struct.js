// mask_struct.js — print byte structure of EVT000_1 dialog window with
// printable chars MASKED ('#') to show structure without leaking text.
const fs = require('fs');
const b = fs.readFileSync('_work/EVT000_1.FNT');
const isP = ch => (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x85 && ch <= 0x91);

function row(off, n) {
  const out = [];
  for (let j = 0; j < n; j++) {
    const x = b[off + j];
    out.push(isP(x) ? '#' : (x < 0x10 ? '0' : '') + x.toString(16));
  }
  return out.join(' ');
}
for (let off = 0xc9f200; off < 0xca0220; off += 24) {
  console.log(('0x' + off.toString(16)).padEnd(9), row(off, 24));
}
