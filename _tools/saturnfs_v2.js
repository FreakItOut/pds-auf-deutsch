// Parse the Sega Saturn on-disc directory (low LBA ~16..24) of a PDS data track.
// Record format (empirically verified):
//   [0] 0x62 01 1d 00 00 00 24 01 00 00 01 00 00 01  (14-byte header; leading variants exist)
//   nameLen (1) | name (ASCII) | 0x00 | u16 recLen
//   then mirrored u32 pairs: u32LE @k == u32BE @k+4, up to 3 pairs.
// We tabulate ALL pairs per record with offsets; cross-record contiguity will be
// checked to infer which pair = LBA and which = size.
const fs = require('fs');

const trackFile = process.argv[2];
const fd = fs.openSync(trackFile, 'r');
const size = fs.fstatSync(fd).size;
const totalSectors = Math.floor(size / 2352);

// The directory was visually located around disc offset 0xb835 (LBA ~20).
// Scan LBA 14..30 for the first record header.
const SCAN_FROM = 14 * 2352;
const SCAN_LEN = 20 * 2352;
const buf = Buffer.alloc(SCAN_LEN);
fs.readSync(fd, buf, 0, SCAN_LEN, SCAN_FROM);

function isHeader(o) {
  return buf[o] === 0x62 && buf[o + 1] === 0x01 && buf[o + 2] === 0x1d;
}

// find first header
let start = -1;
for (let i = 0; i < SCAN_LEN - 512; i++) if (isHeader(i)) { start = i; break; }
if (start < 0) { console.error('no record header found'); process.exit(1); }
console.log('directory starts at disc offset 0x' + (SCAN_FROM + start).toString(16), 'LBA', ((SCAN_FROM + start) / 2352).toFixed(1));

// walk records
let off = start;
const recs = [];
while (off < SCAN_LEN - 40) {
  if (!isHeader(off)) { off++; continue; }
  const hLen = 14;
  const nl = buf[off + hLen];
  if (nl < 1 || nl > 40) { off++; continue; }
  const name = buf.slice(off + hLen + 1, off + hLen + 1 + nl).toString('latin1');
  if (!/^[A-Za-z0-9_\-\.]{1,}$/.test(name)) { off++; continue; }
  let p = off + hLen + 1 + nl;
  if (buf[p] !== 0) { off++; continue; } // terminator
  p++;
  const recLen = buf.readUInt16LE(p); p += 2;
  // mirrored pairs
  const pairs = [];
  for (let k = 0; k + 8 <= recLen - 0; k += 8) {
    const le = buf.readUInt32LE(p + k);
    const be = buf.readUInt32BE(p + k + 4);
    if (le === be && Number.isFinite(le)) pairs.push(le);
    else break;
  }
  recs.push({ name, pairs, off: off + hLen, abs: SCAN_FROM + off });
  off = off + 2 + recLen + hLen; // advance: guessed geometry — refine below
}
// We don't know exact advance; re-walk by scanning sequentially using known header positions:
// simpler robust approach: collect ALL header positions and pair records by ordering
const headerPositions = [];
for (let i = start; i < SCAN_LEN - 40; i++) if (isHeader(i)) headerPositions.push(i);

const table = [];
for (let hi = 0; hi < headerPositions.length; hi++) {
  const o = headerPositions[hi];
  const nl = buf[o + 14];
  if (nl < 1 || nl > 40) continue;
  const name = buf.slice(o + 15, o + 15 + nl).toString('latin1');
  if (!/^[A-Za-z0-9_\-\.]+$/.test(name)) continue;
  let p = o + 15 + nl;
  if (buf[p] !== 0) continue;
  p++;
  const recLen = buf.readUInt16LE(p); p += 2;
  const pairs = [];
  for (let k = 0; k + 8 <= 48; k += 8) {
    const le = buf.readUInt32LE(p + k);
    const be = buf.readUInt32BE(p + k + 4);
    if (le === be) pairs.push(le); else break;
  }
  table.push({ name, recLen, pairs, absOffset: SCAN_FROM + o, absEndGuess: SCAN_FROM + o + 14 + 1 + nl + 1 + 2 + pairs.length * 8 });
}
console.log('records parsed:', table.length);
table.forEach((r, i) => {
  console.log(String(i).padStart(3), r.name.padEnd(16),
    'recLen=' + r.recLen,
    r.pairs.map(v => v.toString(16).padStart(8, '0')).join(' '),
    '@0x' + (r.absOffset).toString(16));
});
fs.closeSync(fd);
