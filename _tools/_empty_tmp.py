# list the menu rows counted as neither DE nor exempt (to be resolved)
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')
sys.path.insert(0, '_tools')
from coverage_final import is_exempt
# hack: coverage_final.py runs at import; read by monkey-isolating
