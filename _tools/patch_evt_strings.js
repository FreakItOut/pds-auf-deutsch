const fs = require('fs');

// Phase 4 - Patch EVT subtitle strings into disc images
// Reads German translation map, searches for English strings in disc images,
// replaces them with German (same length or shorter, NUL-padded)

// Load translation map
const deMap = JSON.parse(fs.readFileSync('_work/evt_de_map_batch1.json', 'latin1'));
console.log('Loaded ' + Object.keys(deMap).length + ' DE translations from batch 1');

// Disc paths
const discs = {
  1: 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin',
  2: 'Original_CD2/Panzer Dragoon Saga (Europe) (Disc 2) (Track 1).bin',
  3: 'Original_CD3/Panzer Dragoon Saga (Europe) (Disc 3) (Track 1).bin',
  4: 'Original_CD4/Panzer Dragoon Saga (Europe) (Disc 4) (Track 1).bin'
};

// Output paths
const outDir = '_work/patched_discs_evt';
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

let totalApplied = 0;
let totalNotFound = 0;

// Process each disc
for (const [discNum, discPath] of Object.entries(discs)) {
  console.log('\nProcessing ' + discPath + '...');
  const buf = Buffer.from(fs.readFileSync(discPath));
  
  for (const [en, de] of Object.entries(deMap)) {
    const enBuf = Buffer.from(en, 'latin1');
    const deBuf = Buffer.from(de, 'latin1');
    
    if (deBuf.length > enBuf.length) {
      console.log('  SKIP (too long): ' + en.substring(0, 40) + '...');
      totalNotFound++;
      continue;
    }
    
    // Find all occurrences of English string in disc image
    let pos = 0;
    let count = 0;
    while (true) {
      const idx = buf.indexOf(enBuf, pos);
      if (idx < 0) break;
      
      // Check if this is a real string (surrounded by NUL or non-printable)
      const before = idx > 0 ? buf[idx - 1] : 0;
      const after = idx + enBuf.length < buf.length ? buf[idx + enBuf.length] : 0;
      const isString = (before === 0 || before < 0x20 || before > 0x7e) && 
                       (after === 0 || after < 0x20 || after > 0x7e);
      
      if (isString) {
        // Write German text
        deBuf.copy(buf, idx);
        // Pad remaining bytes with NUL
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
  
  // Write patched disc
  const outPath = outDir + '/patched_disc' + discNum + '.bin';
  fs.writeFileSync(outPath, buf);
  console.log('  Written: ' + outPath);
}

console.log('\n=== Phase 4 EVT Patching Batch 1 Complete ===');
console.log('Total applied: ' + totalApplied);
console.log('Total skipped (too long): ' + totalNotFound);