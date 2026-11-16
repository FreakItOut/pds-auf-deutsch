# OBSOLETE - DO NOT RUN.
# This script introduced a regression (2026-11-06): csv-sync clobbered
# neighbouring d2 slots and writes only covered the first offset of
# multi-copy rows. All its work has been superseded and completed by
#   _tools/repair3.py        (idempotent, all offsets x all discs, csv-safe)
#   _tools/verify_full.py    (5-stem green: ok=20935, len=0, mismatch=0)
# Kept only as a historical marker.
import sys

sys.stdout.reconfigure(encoding='latin1')
print('OBSOLETE: use repair3.py (fixes all offsets on all discs, csv-safe).')
print('Current authority: verify_full.py -> ok=20935 len=0 mismatch=0.')
sys.exit(1)
