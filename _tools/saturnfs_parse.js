// Parse Sega Saturn on-disc file records (format: 0x62-tag header + name;1 + mirrored u32 LBA/size fields)
// and print the file table of the data track.
const fs = require('fs');

const origFile = process.argv[2];

const BLOCK = 1 << 20; // 1MB scan pages

// Known record header signature observed:
//   62 01 1d 01 00 00 04 00 00 00 01 00 00 01 <nameLen> <name "...;1"> 00 <u16 len?> <u32LE LBA> <u32BE LBA> <u32LE size> <u32BE size>
// Some records show variant headers (other bytes between). We search for "<nameLen><name>;1\0" pattern,
// then read surrounding bytes to infer LBA/size by mirrored u32 fields nearby, constrained:
//   LBA must be < totalSectors, size>0, size < 700MB, and (LBA+size/2048) < totalSectors.
const fd = fs.openSync(origFile, 'r');
const size = fs.fstatSync(fd).size;
const nSectors = Math.floor(size / 2352);
console.log('track1: bytes=' + size + ' sectors=' + nSectors);

// build candidate index: offsets where bytes form `<L>=numLen` with ASCII ";1\0" directly after the name.
const records = [];
let buf;
for (let base = 0; base < size; base += BLOCK - 4096) {
  const ln = Math.min(BLOCK, size - base);
  buf = Buffer.alloc(ln);
  fs.readSync(fd, buf, 0, ln, base);
  for (let i = 0; i < ln - 40; i++) {
    if (buf[i + 2] === 0x3b && buf[i + 3] === 0x31 && buf[i + 4] === 0) { // ";1\0"
      const nl = buf[i - 1]; // nameLen byte
      if (nl < 4 || nl > 32) continue;
      // name before ";1" must be printable and length == nl-2
      let ok = true;
      for (let j = 1; j <= nl - 2; j++) {
        const c = buf[i - j];
        if (!(c >= 0x20 && c <= 0x7e)) { ok = false; break; }
      }
      if (!ok) continue;
      const name = buf.slice(i - (nl - 2), i + 2).toString('latin1');
      if (!/^[A-Z0-9_.\-]{1,28};1$/.test(name)) continue;
      records.push({ abs: base + i - (nl + 1), nl, name });
    }
  }
}
console.log('name records found:', records.length);

// For each record, examine following 40 bytes to find mirrored u32 pairs.
function findPairs(b, off) {
  // scan small window for mirrored u32 pattern: bytes L..L+3 == bytes (L+7..L+4) reversed... mirror means b[L+7]=b[L] etc?
  // Observed: `24 01 00 00 00 00 01 24` -> LE value 0x124 at [L..L+3] and BE value 0x124 at [L+4..L+7]
  const pairs = [];
  for (let L = 0; L + 8 <= 56; L++) {
    const le = b.readUInt32LE(off + L);
    const be = b.readUInt32BE(off + L + 4);
    if (le === be && le > 0 && le < 0x200000 && b.readUInt32LE(off + L + 4) === le) {
      pairs.push({ rel: L, value: le });
      L += 7;
    }
  }
  return pairs;
}

for (let idx = 0; idx < records.length; idx++) {
  const r = records[idx];
  const nb = Buffer.alloc(80);
  fs.readSync(fd, nb, 0, 80, r.abs);
  const pairs = findPairs(nb, r.abs + r.nl + 1); // after name+;1+00
  if (pairs.length >= 1) console.log(idx, 'name=' + r.name, 'abs=0x' + r.abs.toString(16), 'pairs=' + JSON.stringify(pairs.map(p => ({rel: p.rel, v: p.value}))));
  else console.log(idx, 'name=' + r.name, 'abs=0x' + r.abs.toString(16), 'no-pairs');
}
fs.closeSync(fd);
