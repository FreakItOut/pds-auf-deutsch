# read key sections of extract_subtitles.py + batch_process_FMVs.py to see how
# the Spanish translator handled the length constraint
import io
import sys
sys.stdout.reconfigure(encoding='latin1')
P = 'C:/Users/FreakItOut/Downloads/pds-tools-master/pds-tools-master/tools/'
for fname in ('extract_subtitles.py', 'batch_process_FMVs.py'):
    print('=====', fname)
    try:
        txt = io.open(P + fname, encoding='latin1').read()
        print(txt[:5000])
    except Exception as e:
        print('err', e)
