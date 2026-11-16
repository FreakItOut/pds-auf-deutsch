// Inspect structure of segasaturno "%XDZ004%" patch (concatenated gzip members)
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

function parseGzipHeader(buf, pos) {
  if (buf[pos] !== 0x1f || buf[pos + 1] !== 0x8b) return null;
  let p = pos + 10; // magic, method, flags, mtime(4), XFL, OS
  const flg = buf[pos + 3];
  if (flg & 0x04) { // FEXTRA
    const xlen = buf.readUInt16LE(p); p += 2 + xlen;
  }
  if (flg & 0x08) { // FNAME
    while (buf[p] !== 0) p++;
    p++;
  }
  if (flg & 0x10) { // FCOMMENT
    while (buf[p] !== 0) p++;
    p++;
  }
  if (flg & 0x02) p += 2; // FHCRC
  return p; // start of deflate data
}

function findTrailer(result, deflateStart, deflateEndGuessMax) {
  // scan for 8-byte trailer matching crc32+isize right after deflate data
  const crc = zlib.crc32(result) >>> 0;
  const size = result.length >>> 0;
  const tr = Buffer.allocUnsafe(8);
  tr.writeUInt32LE(crc, 0);
  tr.writeUInt32LE(size, 4);
  // brute scan limited window
  for (let e = deflateStart; e < Math.min(deflateStart + deflateEndGuessMax, resultEnd_limit); e++) {
    // compare 8 bytes at offset e
  }
  return null;
}

const file = process.argv[2];
const limit = parseInt(process.argv[3] || '5', 10);
const buf = fs.readFileSync(file);

// header
let pos = 0;
const magic = buf.slice(0, 8).toString('ascii');
pos = 8;
// fixed layout: magic(8) u32BE u16BE u16BE + 16 reserved + names + gzip data at offset 32+n1len+n2len
const u32 = buf.readUInt32BE(8);
const n1len = buf.readUInt16BE(12);
const n2len = buf.readUInt16BE(14);
pos = 32;
const name1 = buf.slice(pos, pos + n1len).toString('ascii'); pos += n1len;
const name2 = buf.slice(pos, pos + n2len).toString('ascii'); pos += n2len;
console.log('magic=%s u32@8=%d(nl) n1len=%d n2len=%d name1=%s name2=%s dataStart=%d totalBytes=%d',
  magic, u32, n1len, n2len, name1, name2, pos, buf.length);

let member = 0;
let p = pos;
while (p < buf.length && member < limit) {
  const hdrEnd = parseGzipHeader(buf, p);
  if (hdrEnd == null) { console.log('offset %d: no gzip header', p); break; }
  // find trailer: brute-force scan for crc+isize match
  // first inflate from hdrEnd ignoring trailing data? use inflateRawSync try by truncation search on end:
  // do a scan over candidate end offsets using expected crc/isize — we don't know result until we inflate.
  // Instead: use node's gunzip on buffer slice; gunzipSync will complain about garbage but still return?
  let out, consumedEnd = -1, err = null;
  try {
    out = zlib.inflateRawSync(buf.subarray(hdrEnd, buf.length), { finishFlush: zlib.constants.Z_FINISH });
    // inflateRawSync with trailing data: node stops at end of stream, but we don't know consumed length. Find trailer bytes:
    const crc = zlib.crc32(out) >>> 0;
    const tr = Buffer.allocUnsafe(8);
    tr.writeUInt32LE(crc, 0);
    tr.writeUInt32LE(out.length >>> 0, 4);
    // scan for trailer within a bounded window after hdrEnd
    const win = 1 << 22; // deflate data can be large; trailer must be somewhere after hdrEnd
    const idx = buf.subarray(hdrEnd, Math.min(hdrEnd + win + out.length, buf.length)).indexOf(tr);
    if (idx >= 0) {
      consumedEnd = hdrEnd + idx + 8;
    } else {
      err = 'trailer not found';
    }
  } catch (e) {
    err = e.message;
  }
  if (out) {
    console.log('member %d: hdr@%d hdrEnd=%d inflLen=%d next@%d headBytes=%s',
      member, p, hdrEnd, out.length, consumedEnd,
      out.subarray(0, 16).toString('hex'));
    // guess first few bytes as text
    let ti = '';
    for (const b of out.subarray(0, 24)) ti += (b >= 32 && b < 127) ? String.fromCharCode(b) : '.';
    console.log('   ascii: %s', ti);
  } else {
    console.log('member %d: hdr@%d hdrEnd=%d inflate failed: %s', member, p, hdrEnd, err);
    break;
  }
  if (consumedEnd < 0) break;
  p = consumedEnd;
  member++;
}
console.log('... stopped at offset %d after %d members', p, member);
