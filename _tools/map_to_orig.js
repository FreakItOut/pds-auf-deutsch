// Fingerprint mapping: find where fragments of the extracted patch members appear
// inside the original PAL-EU data track. Establishes member<->disc offset mapping.
const fs = require('fs');

const origFile = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const memberFile = process.argv[2];

const origSize = fs.statSync(origFile).size;
const orig = fs.openSync(origFile, 'r');
const member = fs.readFileSync(memberFile);

// Index original every 4096 bytes -> hash of first 12 bytes
const WIN = 12;
const PAGE = 1 << 24; // 16MB reads
const index = new Map();
function h(b, o) {
  // simple string hash over 12 bytes
  let x = 2166136261;
  for (let i = 0; i < WIN; i++) x = Math.imul(x ^ b[o + i], 16777619);
  return x >>> 0;
}
{
  const buf = Buffer.alloc(PAGE);
  let fileOff = 0;
  while (fileOff < origSize) {
    const n = fs.readSync(orig, buf, 0, PAGE, fileOff);
    for (let i = 0; i + WIN <= n; i += 4096) {
      const key = h(buf, i);
      const abs = fileOff + i;
      let arr = index.get(key);
      if (!arr) { arr = []; index.set(key, arr); }
      if (arr.length < 3) arr.push(abs);
    }
    fileOff += n;
  }
}
console.error('orig indexed, entries:', index.size);

// For every aligned window in member, look up
function mapMember(label) {
  const hits = [];
  for (let off = 0; off + WIN <= member.length; off += 4096) {
    const arr = index.get(h(member, off));
    if (arr) {
      let first = -1;
      for (const abs of arr) {
        // verify full 12 bytes equality (hash collisions)
        let ok = true;
        for (let j = 0; j < WIN; j++) if (member[off + j] !== origBufAt(abs + j)) { ok = false; break; }
        if (ok) { first = abs; break; }
      }
      if (first >= 0) hits.push([off, first]);
    }
  }
  console.log(`--- ${label}: ${hits.length} matched windows ---`);
  // print compact mapping: first 8, then sample steps where delta changes
  let prevDelta = null;
  let prevOff = null;
  const shown = new Set();
  for (const [off, abs] of hits) {
    const delta = abs - off;
    if (delta !== prevDelta || off === hits[0][0]) {
      console.log(`member@0x${off.toString(16).padStart(8, '0')}  ->  disc@0x${abs.toString(16).padStart(8, '0')}  (delta 0x${delta.toString(16)})`);
      prevDelta = delta;
      prevOff = off;
    }
  }
  return hits;
}

function origBufAt(abs) {
  const T = Buffer.alloc(1);
  fs.readSync(orig, origBufAt.b || (origBufAt.b = Buffer.alloc(1 << 16)), 0, 0, 0); // noop
  return origBufAt.b;
}
// simpler: use a small cache read helper
function byteAt(abs) {
  if (!byteAt.buf) { byteAt.buf = Buffer.alloc(1); }
  fs.readSync(orig, byteAt.buf, 0, 1, abs);
  return byteAt.buf[0];
}
// redo verification with byteAt properly:
function mapMember2(label) {
  const origFd = orig;
  const b2 = Buffer.alloc(WIN);
  const hits = [];
  for (let off = 0; off + WIN <= member.length; off += 4096) {
    const arr = index.get(h(member, off));
    if (!arr) continue;
    let first = -1;
    for (const abs of arr) {
      fs.readSync(origFd, b2, 0, WIN, abs);
      let ok = true;
      for (let j = 0; j < WIN; j++) if (member[off + j] !== b2[j]) { ok = false; break; }
      if (ok) { first = abs; break; }
    }
    if (first >= 0) hits.push([off, first]);
  }
  console.log(`--- ${label}: ${hits.length} matched windows ---`);
  let prevDelta = null;
  for (const [off, abs] of hits) {
    const delta = abs - off;
    if (delta !== prevDelta) {
      console.log(`member@0x${off.toString(16).padStart(8, '0')} -> disc@0x${abs.toString(16).padStart(8, '0')} (delta 0x${delta.toString(16)})`);
      prevDelta = delta;
    }
  }
  return hits;
}

mapMember2(memberFile);
fs.closeSync(orig);
