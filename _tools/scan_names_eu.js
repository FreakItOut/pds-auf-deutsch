// Scan EU CD1 track for character names / story words in plaintext, count only.
const fs = require('fs');
const fd = fs.openSync('Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin', 'r');
const total = fs.fstatSync(fd).size;
const W = 8 * 1024 * 1024;
const b = Buffer.alloc(W);
const words = ['Edge', 'Azel', 'Craymen', 'Lundi', 'Gash', 'Panzer', 'Ancients', 'Zoah',
  'Pelluri', 'Peljuri', 'Negeel', 'Uria', 'Sheila', 'Surgh', 'Sarlait', 'Impriali',
  'Edge: ', 'Azel: ', 'Craymen:', 'Lundi:'];
const counts = {}, byRegion = [];
for (const w of words) counts[w] = 0;
for (let base = 0; base < total; base += W - 64) {
  const n = fs.readSync(fd, b, 0, Math.min(W, total - base), base);
  const str = b.toString('latin1', 0, n);
  for (const w of words) {
    let i = 0;
    while ((i = str.indexOf(w, i)) !== -1) { counts[w]++; i++; }
  }
}
fs.closeSync(fd);
console.log('EU CD1 plaintext name-counts:');
for (const [w, c] of Object.entries(counts)) console.log('  ', JSON.stringify(w), c);
