// Extract the two gzip members of the XDZ patch to files, list internal structure
const fs = require('fs');
const zlib = require('zlib');

function parseGzipHeader(buf, pos) {
  if (buf[pos] !== 0x1f || buf[pos + 1] !== 0x8b) return null;
  let p = pos + 10;
  const flg = buf[pos + 3];
  if (flg & 0x04) { const xlen = buf.readUInt16LE(p); p += 2 + xlen; }
  if (flg & 0x08) { while (buf[p] !== 0) p++; p++; }
  if (flg & 0x10) { while (buf[p] !== 0) p++; p++; }
  if (flg & 0x02) p += 2;
  return p;
}

const file = process.argv[2];
const outPrefix = process.argv[3];
const buf = fs.readFileSync(file);
const n1len = buf.readUInt16BE(12), n2len = buf.readUInt16BE(14);
let p = 32 + n1len + n2len;
const name1 = buf.slice(32, 32 + n1len).toString('ascii');
const name2 = buf.slice(32 + n1len, 32 + n1len + n2len).toString('ascii');
console.log('name1=%s name2=%s dataStart=%d', name1, name2, p);

let members = [];
while (p < buf.length) {
  const hdrEnd = parseGzipHeader(buf, p);
  if (hdrEnd == null) { console.log('no gzip header@%d', p); break; }
  const out = zlib.inflateRawSync(buf.subarray(hdrEnd, buf.length), { finishFlush: zlib.constants.Z_FINISH });
  const crc = zlib.crc32(out) >>> 0;
  const tr = Buffer.allocUnsafe(8);
  tr.writeUInt32LE(crc, 0);
  tr.writeUInt32LE(out.length >>> 0, 4);
  const idx = buf.subarray(hdrEnd).indexOf(tr);
  if (idx < 0) { console.log('trailer not found@%d', hdrEnd); break; }
  const end = hdrEnd + idx + 8;
  members.push({ start: p, end, len: out.length, data: out });
  p = end;
}
console.log('members:', members.length);
members.forEach((m, i) => {
  const f = `${outPrefix}_${i}.bin`;
  fs.writeFileSync(f, m.data);
  console.log('member %d: pos %d..%d (%d compressed), inflated %d bytes in %s',
    i, m.start, m.end, m.end - m.start, m.len, f);
  console.log('  first 32: %s', m.data.subarray(0, 32).toString('hex'));
  console.log('  ascii   : %s',
    [...m.data.subarray(0, 32)].map(b => (b >= 32 && b < 127) ? String.fromCharCode(b) : '.').join(''));
});
