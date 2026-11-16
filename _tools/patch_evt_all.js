const fs = require('fs');

// Load all German translations
const deMap = JSON.parse(fs.readFileSync('_work/evt_de_map_batch4.json', 'latin1'));
console.log('Loaded ' + Object.keys(deMap).length + ' DE translations');

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

for (const [discNum, discPath] of Object.entries(discs)) {
  console.log('Processing ' + discPath + '...');
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
      
      const before = idx > 0 ? buf[idx - 1] : 0;
      const after = idx + enBuf.length < buf.length ? buf[idx + enBuf.length] : 0;
      const beforeOK = before === 0 || before < 0x20 || before > 0x7e;
      const afterOK = after === 0 || after < 0x20 || after > 0x7e;
      
      if (beforeOK && afterOK) {
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
      console.log('  Patched: ' + en.substring(0, 50) + '... (' + count + 'x)');
    }
  }
  
  fs.writeFileSync(outDir + '/patched_disc' + discNum + '.bin', buf);
  console.log('  Written to ' + outDir + '/patched_disc' + discNum + '.bin');
}

console.log('\n=== Patch Complete ===');
console.log('Total applied: ' + totalApplied);
console.log('Total skipped (too short): ' + totalSkipped);
console.log('Total skipped (too long): ' + totalTooLong);