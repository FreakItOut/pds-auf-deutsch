// Bucket EU CD1 plaintext name-hits to owning files (via FS table) -> counts per file.
const fs = require('fs');
const TRACK = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(TRACK, 'r');

// FS table
const SCAN_FROM = 14 * 2352, SCAN_LEN = 20 * 2352;
const buf = Buffer.alloc(SCAN_LEN);
fs.readSync(fd, buf, 0, SCAN_LEN, SCAN_FROM);
const files = [];
for (let i = 0; i < SCAN_LEN - 40; i++) {
  if (buf[i] === 0x62 && buf[i + 1] === 0x01 && buf[i + 2] === 0x1d) {
    const nl = buf[i + 14];
    if (nl < 1 || nl > 40) continue;
    const name = buf.slice(i + 15, i + 15 + nl).toString('latin1');
    if (!/^[A-Za-z0-9_\-.]+$/.test(name)) continue;
    let p = i + 15 + nl;
    if (buf[p] !== 0) continue;
    p++;
    p += 2;
    const pairs = [];
    for (let k = 0; k + 8 <= 40; k += 8) {
      const a = buf.readUInt32LE(p + k), b2 = buf.readUInt32BE(p + k + 4);
      if (a === b2) pairs.push(a); else break;
    }
    if (pairs.length >= 2 && pairs[0] < 600000 && pairs[1] < 470000000) {
      const key = name.toUpperCase();
      if (!files.find(f => f.name === key))
        files.push({ name: key, lba: pairs[0], size: pairs[1] });
    }
  }
}
files.sort((a, b) => a.lba - b.lba);

const total = fs.fstatSync(fd).size;
const W = 8 * 1024 * 1024, b = Buffer.alloc(W);
const words = ['Edge', 'Azel', 'Craymen', 'Gash', 'Zoah', 'Panzer', 'Azel:'];
const perFile = new Map();
for (let base = 0; base < total; base += W - 64) {
  const n = fs.readSync(fd, b, 0, Math.min(W, total - base), base);
  const str = b.toString('latin1', 0, n);
  for (const w of words) {
    let i = 0;
    while (i !== -1 && (i = str.indexOf(w, i)) !== -1) {
      const abs = base + i;
      const lba = Math.floor(abs / 2352);
      // owner = last file with lba<=abs lba (claim contiguous; gap -> prev file)
      let owner = null;
      for (const f of files) { if (f.lba > lba) break; owner = f; }
      if (owner) {
        const k = owner.name;
        perFile.set(k, (perFile.get(k) || 0) + 1);
      }
      i++;
    }
  }
}
fs.closeSync(fd);
const arr = [...perFile.entries()].filter(e => e[1] > 3).sort((a, b) => b[1] - a[1]).slice(0, 40);
console.log('per-file plaintext name-hits (top by count):');
for (const [f, c] of arr) console.log('  ', f.padEnd(16), c);
console.log('total files named:', arr.length);
