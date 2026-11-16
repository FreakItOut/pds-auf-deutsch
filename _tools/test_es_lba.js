// Test: for selected files, use the Spanish member0 directory (re-parsed here,
// names kept with their ';1' suffix) and check whether the plaintext strings of
// the EU file appear (Spanish equivalents) at  directory LBA*2048 in member0.
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
const recs = {};
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
  recs[name] = { lba, size };
  const nx = nextHdr(o + 34 + nl - 1);
  if (nx < 0 || nx <= o) { console.log('break near name', name); break; }
  o = nx;
}
console.log('total ES dir records parsed:', Object.keys(recs).length);

const targets = ['BTL_A3.FNT;1', 'BTL_A5.FNT;1', 'CARASCR0.PNB;1', 'CARASCR2.PNB;1', 'CAMPSCR0.PNB;1', 'CAMPSCR4.PNB;1'];
for (const nm of targets) {
  const r = recs[nm];
  if (!r) { console.log(nm, 'not found'); continue; }
  const L = r.lba * 2048, S = Math.min(r.size, 2000000);
  console.log('---', nm, 'ESoff=0x' + L.toString(16), 'ESsize=' + r.size);
  if (L >= s.length) { console.log('   OUT OF MEMBER RANGE'); continue; }
  const str = s.toString('latin1').slice(L, L + S);
  const words = ['Contraataque', 'Atacar con el Arma', 'no use', 'Attack with Gun', 'Atacar con el L' + String.fromCharCode(0x8a) + 'ser', 'gun', 'Customize Gun'];
  for (const w of words) {
    let i = 0, c = 0;
    while ((i = str.indexOf(w, i)) !== -1) { c++; i++; }
    console.log('    ', JSON.stringify(w), 'hits', c);
  }
}
