// find_blob_entry.js — scan the whole disc for mirrored LE/BE u32 pairs whose
// value lies in [235710..235730] (blob start candidates), or 246700..246800
// (blob end candidates). Prints sector, raw hex context. No game text.
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const SECTORS = 274450;
const WIN = new Set();
for (let v = 235710; v <= 235730; v++) WIN.add(v);
for (let v = 246700; v <= 246760; v++) WIN.add(v);

const buf = Buffer.alloc(2000 * 2352);
const found = [];
for (let s = 0; s < SECTORS; s += 2000) {
  const n = Math.min(2000, SECTORS - s);
  fs.readSync(fd, buf, 0, n * 2352, s * 2352);
  const lim = (n - 1) * 2352;
  for (let j = 0; j < lim; j++) {
    for (let q = 0; q + 4 <= 2352; q++) {
      const off = j + q;
      if (off + 8 > buf.length) break;
      // value LE at off; mirrored BE at off+4 => pattern: [v][v>>8][v>>16][v>>24][v>>24]...
      const v = buf.readUInt32LE(off);
      if (WIN.has(v)) {
        // check LE/BE mirror: bytes off..off+3 = value LE; off+4..+7 = value BE
        if (buf[off] === buf[off + 7] && buf[off + 1] === buf[off + 6] &&
            buf[off + 2] === buf[off + 5] && buf[off + 3] === buf[off + 4]) {
          const sec = s + Math.floor(off / 2352);
          found.push({ sec, offInSec: off % 2352, v });
          if (found.length > 200) { console.log('>200 hits, stopping'); print(found); process.exit(0); }
        }
      }
    }
  }
}
print(found);

function print(f) {
  console.log('mirrored-pair hits:', f.length);
  for (const x of f.slice(0, 40)) {
    const b2 = Buffer.alloc(2352);
    fs.readSync(fd, b2, 0, 2352, x.sec * 2352);
    const blobOff = x.offInSec;
    console.log('  sec ' + x.sec + ' +of ' + blobOff, 'v=' + x.v,
      'ctx:', b2.slice(Math.max(0, blobOff - 12), Math.min(2352, blobOff + 32)).toString('hex'));
  }
}
