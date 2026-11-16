import os, csv
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
SECT=2352; DATA=2048
def read_file(binpath, lba, size):
    out=bytearray(); need=size; s=lba
    with open(binpath,'rb') as f:
        while need>0:
            f.seek(s*SECT+16); c=f.read(min(DATA,need))
            if not c: break
            out+=c; need-=len(c); s+=1
    return bytes(out[:size])
def write_file_regions(binpath, lba, filedata):
    with open(binpath, 'r+b') as f:
        for k in range((len(filedata) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(filedata[k * DATA:(k + 1) * DATA])
def fs_index(disc, name):
    fs='_work/fs_records_all.csv' if disc==1 else f'_work/fs_records_cd{disc}.csv'
    for r in csv.DictReader(open(fs,encoding='latin1'),delimiter=';'):
        if r['name']==name:
            return int(r['lba']), int(r['size'])
    return None
lba,size=fs_index(1,'TWN_RUIN.PRG')
data=bytearray(read_file('_work/patched_disc1.bin',lba,size))
# Replace all 'das Vorzeit' with 'die Vorzeit' (same length)
old = b'das Vorzeit'
new = b'die Vorzeit'
count = data.count(old)
data = data.replace(old, new)
write_file_regions('_work/patched_disc1.bin', lba, bytes(data))
print('replaced', count, 'occurrences')