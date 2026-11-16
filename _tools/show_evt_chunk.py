# -*- coding: utf-8 -*-
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
start = int(sys.argv[1])
end = int(sys.argv[2])
lines = io.open('_work/review_fixes/evt_all_review.txt',
                encoding='latin1').read().splitlines()
for ln in lines[start - 1:end]:
    print(ln)
