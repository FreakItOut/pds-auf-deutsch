const fs = require('fs');

// Phase 4 - Patch EVT subtitle strings into disc images
// Version 2 - Supports batch number parameter

const batchNum = process.argv[2] || '1';
const deMap = JSON.parse(fs.readFileSync('_work/evt_de_map_batch' + batchNum + '.json', 'latin1'));
console.log('Loaded ' + Object.keys(deMap).length + ' DE translations from batch ' + batchNum);

// Disc paths
const discs = {
  1: 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin',
  2: 'Original_CD2/Panzer Dragoon Saga (Europe) (Disc 2) (Track 1).bin',
  3: 'Original_CD3/Panzer Dragoon Saga (Europe) (Disc 3) (Track 1).bin',
  4: 'Original_CD4/Panzer Dragoon Saga (Europe) (Disc 4) (Track 1).bin'
};

const outDir = '_work/patched_discs_evt';
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

let totalApplied = 0;
let totalSkipped = 0;
let totalTooLong = 0;

function isStringBoundary(buf, pos, len) {
  const before = pos > 0 ? buf[pos - 1] : 0;
  const after = pos + len < buf.length ? buf[pos + len] : 0;
  const beforeOK = before === 0 || before < 0x20 || before > 0x7e;
  const afterOK = after === 0 || after < 0x20 || after > 0x7e;
  return beforeOK && afterOK;
}

for (const [discNum, discPath] of Object.entries(discs)) {
  console.log('\nProcessing ' + discPath + '...');
  const buf = Buffer.from(fs.readFileSync(discPath));
  
  for (const [en, de] of Object.entries(deMap)) {
    const enBuf = Buffer.from(en, 'latin1');
    const deBuf = Buffer.from(de, 'latin1');
    
    if (deBuf.length > enBuf.length) {
      totalTooLong++;
      continue;
    }
    
    if (enBuf.length < 15) {
      totalSkipped++;
      continue;
    }
    
    let pos = 0;
    let count = 0;
    
    while (true) {
      const idx = buf.indexOf(enBuf, pos);
      if (idx < 0) break;
      
      if (isStringBoundary(buf, idx, enBuf.length)) {
        deBuf.copy(buf, idx);
        for (let k = idx + deBuf.length; k < idx + enBuf.length; k++) {
          buf[k] = 0;
        }
        count++;
        totalApplied++;
      }
      
      pos = idx + 1;
    }
    
    if (count > 0) {
      console.log('  Patched: ' + en.substring(0, 50) + '... (' + count + ' occurrences)');
    }
  }
  
  const outPath = outDir + '/patched_disc' + discNum + '.bin';
  fs.writeFileSync(outPath, buf);
  console.log('  Written: ' + outPath);
}

console.log('\n=== Phase 4 EVT Patching Batch ' + batchNum + ' Complete ===');
console.log('Total applied: ' + totalApplied);
console.log('Total skipped (too short < 15 chars): ' + totalSkipped);
console.log('Total skipped (too long): ' + totalTooLong);