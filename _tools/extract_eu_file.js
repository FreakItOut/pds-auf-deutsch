// Extract a single file from EU CD1 track by Sega-FS lookup (by name) and save it.
// Usage: node _tools/extract_eu_file.js <name> [outFile]
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const SCAN_FROM = 14 * 2352, SCAN_LEN = 20 * 2352;
const buf = Buffer.alloc(SCAN_LEN);
fs.readSync(fd, buf, 0, SCAN_LEN, SCAN_FROM);

const name = process.argv[2];
if (!name) { console.error('usage: node extract_eu_file.js <FILE.EXT> [out]'); process.exit(1); }

let found = null;
for (let i = 0; i < SCAN_LEN - 40; i++) {
  if (buf[i] === 0x62 && buf[i + 1] === 0x01 && buf[i + 2] === 0x1d) {
    const nl = buf[i + 14];
    if (nl < 1 || nl > 40) continue;
    const nm = buf.slice(i + 15, i + 15 + nl).toString('latin1');
    if (!/^[A-Za-z0-9_\-.]+$/.test(nm) || nm.toUpperCase() !== name.toUpperCase()) continue;
    let p = i + 15 + nl;
    if (buf[p] !== 0) continue;
    p++;
    const recLen = buf.readUInt16LE(p); p += 2;
    const pairs = [];
    for (let k = 0; k + 8 <= 40; k += 8) {
      const a = buf.readUInt32LE(p + k), b2 = buf.readUInt32BE(p + k + 4);
      if (a === b2) pairs.push(a); else break;
    }
    if (pairs.length >= 2 && pairs[0] < 600000 && pairs[1] < 470000000) {
      found = { lba: pairs[0], size: pairs[1], recLen };
      break;
    }
  }
}
if (!found) { console.error('file not found: ' + name); process.exit(1); }
console.log(name, 'LBA 0x' + found.lba.toString(16), 'size', found.size, '(' + (found.size / 1024 | 0) + ' KiB)');

const out = process.argv[3] || ('_work/' + name);
const data = Buffer.alloc(found.size);
let pos = found.lba * 2352;
for (let i = 0; i < found.size; i += 2048) {
  const take = Math.min(2048, found.size - i);
  fs.readSync(fd, data, i, take, pos + (i / 2048) * 2352);
}
fs.writeFileSync(out, data);
console.log('written', out);
fs.closeSync(fd);
