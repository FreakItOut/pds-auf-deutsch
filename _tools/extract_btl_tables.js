// extract_btl_tables.js
// For each EU BTL_*.FNT/PRG file in the CD1 FS table, find its NUL-terminated
// string table (searching for marker 'no use' or 'Counterattack' or 'NOMAL'),
// extract runs (NUL-skip), write _work/strings_eu_btl_tables.csv:
//   file;slot;text
// Print only counts.
const fs = require('fs');
const TRACK = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';

const fd = fs.openSync(TRACK, 'r');
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
    if (!/^BTL_/i.test(name)) continue;
    let p = i + 15 + nl;
    if (buf[p] !== 0) continue;
    p++;
    buf.readUInt16LE(p); p += 2;
    const pairs = [];
    for (let k = 0; k + 8 <= 40; k += 8) {
      const a = buf.readUInt32LE(p + k), b2 = buf.readUInt32BE(p + k + 4);
      if (a === b2) pairs.push(a); else break;
    }
    if (pairs.length >= 2 && pairs[0] < 600000 && pairs[1] < 470000000) {
      if (!files.find(f => f.name === name)) files.push({ name, lba: pairs[0], size: pairs[1] });
    }
  }
}

const isP = ch => (ch >= 0x20 && ch <= 0x7e) || ch === 0x0a || ch === 0x0d;
function extractTable(data) {
  // find marker
  let markerIdx = -1;
  for (const m of ['no use', 'Counterattack', 'NOMAL']) {
    const idx = data.indexOf(m);
    if (idx >= 0 && (markerIdx < 0 || idx < markerIdx)) markerIdx = idx;
  }
  if (markerIdx < 0) return null;
  // walk back to table start: skip backwards over isP/NUL bytes
  let start = markerIdx;
  while (start > 0 && (isP(data[start - 1]) || data[start - 1] === 0)) start--;
  // ensure first byte is isP
  while (start < data.length && !isP(data[start])) start++;
  // extract runs with NUL-skip, stop at non-isP-non-NUL
  const runs = [];
  let i = start;
  while (i < data.length) {
    if (isP(data[i])) {
      const st = i;
      while (i < data.length && isP(data[i])) i++;
      const len = i - st;
      if (len >= 2 && i < data.length && data[i] === 0x00) {
        let t = '';
        for (let j = st; j < i; j++) t += String.fromCharCode(data[j]);
        runs.push(t); i++;
      } else if (len >= 2 && i >= data.length) {
        let t = '';
        for (let j = st; j < i; j++) t += String.fromCharCode(data[j]);
        runs.push(t); break;
      } else break;
    } else if (data[i] === 0x00) i++;
    else break;
  }
  return runs;
}

const CH = Buffer.alloc(2352 * 128);
const rows = [];
const stats = [];
for (const r of files) {
  const lbaByte = r.lba * 2352;
  let pos = lbaByte, userDone = 0, sectIdx = 0;
  const parts = [];
  while (userDone < r.size) {
    const n = fs.readSync(fd, CH, 0, CH.length, pos + sectIdx * 2352);
    if (n <= 0) break;
    const nSectors = Math.floor(n / 2352);
    for (let s = 0; s < nSectors && userDone < r.size; s++) {
      const take = Math.min(2048, r.size - userDone);
      parts.push(CH.slice(s * 2352 + 16, s * 2352 + 16 + take));
      userDone += take;
    }
    sectIdx += nSectors;
  }
  if (!parts.length) continue;
  const data = Buffer.concat(parts);
  const runs = extractTable(data);
  if (!runs || runs.length < 5) { stats.push({ name: r.name, runs: runs ? runs.length : 0 }); continue; }
  for (let k = 0; k < runs.length; k++) {
    rows.push([r.name, k, runs[k].replace(/\\/g, '\\\\').replace(/\r/g, '\\r').replace(/\n/g, '\\n').replace(/;/g, '\\;')].join(';'));
  }
  stats.push({ name: r.name, runs: runs.length });
}

fs.writeFileSync('_work/strings_eu_btl_tables.csv',
  'file;slot;text\n' + rows.join('\n') + '\n', 'utf8');
fs.writeFileSync('_work/strings_eu_btl_files.csv',
  'file;strings\n' + stats.map(s => [s.name, s.runs].join(';')).join('\n') + '\n', 'utf8');

const withT = stats.filter(s => s.runs >= 5);
console.log('BTL files:', files.length, 'extracted tables:', withT.length);
console.log('total BTL table strings:', rows.length);
for (const s of withT.sort((a, b) => b.runs - a.runs)) console.log('  ', s.name.padEnd(16), s.runs);
fs.closeSync(fd);
console.log('written: _work/strings_eu_btl_tables.csv, _work/strings_eu_btl_files.csv');
