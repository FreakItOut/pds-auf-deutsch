// add_lb.js — Add LB and size columns to the full FS parse for all 643 records.
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const SCAN_FROM = 14 * 2352, SCAN_LEN = 20 * 2352;
const buf = Buffer.alloc(SCAN_LEN);
fs.readSync(fd, buf, 0, SCAN_LEN, SCAN_FROM);

const rows = [];
for (let i = 0; i < SCAN_LEN - 60; i++) {
  if (buf[i] === 0x62 && buf[i + 1] === 0x01 && buf[i + 2] === 0x1d) {
    for (let hdr = 13; hdr <= 17; hdr++) {
      const nl = buf[i + hdr];
      if (nl < 2 || nl > 40) continue;
      const nm = buf.slice(i + hdr + 1, i + hdr + 1 + nl).toString('latin1');
      if (!/^[A-Za-z0-9_\-.]+$/.test(nm)) continue;
      let p = i + hdr + 1 + nl;
      // find mirrored pair (skip any filler bytes)
      let found = null;
      for (let k = 0; k < 6 && !found; k++) {
        const q = p + k;
        if (q + 16 > SCAN_LEN) break;
        const a1 = buf.readUInt32LE(q), b1 = buf.readUInt32BE(q + 4);
        const a2 = buf.readUInt32LE(q + 8), b2 = buf.readUInt32BE(q + 12);
        if (a1 === b1 && a2 === b2) found = { lba: a1, size: a2, recLen: buf.readUInt16LE(p) };
      }
      if (found) {
        const lb = 1 + found.lba + Math.ceil(found.size / 2048);
        rows.push({ name: nm, lba: found.lba, size: found.size, lb, recLen: found.recLen, dump: i });
        break;
      }
    }
  }
}
console.log('records with LB:', rows.length);
const sorted = [...rows].sort((a, b) => a.lba - b.lba);
const CONTENT_END = Math.floor(274450 / 4) - 150;
// sanity: first/next near sorted?
for (let k = 1; k < sorted.length; k++) {
  const a = sorted[k - 1], b = sorted[k];
  if (a.lb + 1 <= b.lb - 2 || a.lb >= b.lb) {
    console.log('  anomaly:', a.name, 'LB', a.lb, '->', b.name, 'LB', b.lb, '(delta', b.lb - a.lb, ')');
  }
}
console.log('last 3 rows by lba:');
for (const r of sorted.slice(-3)) console.log('  ', r.name, 'lba', r.lba, 'size', r.size, 'LB', r.lb);
const maxLB = Math.max(...rows.map(r => r.lb));
console.log('max LB:', maxLB, 'content_end(sanity):', CONTENT_END);
fs.writeFileSync('_work/fs_cd1_full.csv', 'name;lba;size;LB;recLen;dumpAddr\n' +
  sorted.map(r => [r.name, r.lba, r.size, r.lb, r.recLen, r.dump].join(';')).join('\n') + '\n');
console.log('written _work/fs_cd1_full.csv');
fs.closeSync(fd);
