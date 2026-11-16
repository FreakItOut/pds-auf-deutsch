// Scan EU CD1 track for plaintext English UI strings corresponding to the
// Spanish string table we found in the Spanish rebuild member0.
const fs = require('fs');
const fd = fs.openSync('Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin', 'r');
const total = fs.fstatSync(fd).size;
const W = 4 * 1024 * 1024;
const b = Buffer.alloc(W);
const words = [
  'Attack with', 'Laser', 'ontre', 'the Dragon', 'Destruction',
  'Experience', 'Not enough', 'sufficient', 'Weapon', 'enough PL',
  'maximum', 'already done', 'targets in', 'in sight', 'Fire at'
];
for (let base = 0; base < total; base += W - 64) {
  const n = fs.readSync(fd, b, 0, Math.min(W, total - base), base);
  const str = b.toString('latin1', 0, n);
  const found = [];
  for (const w of words) {
    let i = 0;
    while ((i = str.indexOf(w, i)) !== -1) { found.push(w + '@0x' + (base + i).toString(16)); i += w.length; }
  }
  if (found.length) console.log('EU hit @0x' + base.toString(16) + ':', found.slice(0, 12).join(' | '));
}
fs.closeSync(fd);
