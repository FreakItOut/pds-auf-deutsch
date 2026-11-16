// fs_full_scan.js — Scan disc for ALL records 62 01 1d XX (any 4th byte) and
// note their names and pair counts. This reveals records our FS parse missed.
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const SCAN_FROM = 14 * 2352, SCAN_LEN = 20 * 2352;
const buf = Buffer.alloc(SCAN_LEN);
fs.readSync(fd, buf, 0, SCAN_LEN, SCAN_FROM);

let anyCount = 0, withName = 0;
const seen = new Set();
for (let i = 0; i < SCAN_LEN - 60; i++) {
  if (buf[i] === 0x62 && buf[i + 1] === 0x01 && buf[i + 2] === 0x1d) {
    anyCount++;
    for (let hdr = 13; hdr <= 17; hdr++) {
      const nl = buf[i + hdr];
      if (nl < 2 || nl > 40) continue;
      const nm = buf.slice(i + hdr + 1, i + hdr + 1 + nl).toString('latin1');
      if (!/^[A-Za-z0-9_\-.]+$/.test(nm)) continue;
      const key = nm + '@' + hdr;
      if (seen.has(key)) continue;
      seen.add(key);
      withName++;
      console.log('  0x' + i.toString(16), 'hdrLen', hdr, nl, nm);
      break;
    }
  }
}
console.log('total 62 01 1d XX occurrences:', anyCount, '| named:', withName);
fs.closeSync(fd);
