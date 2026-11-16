import io

p = '_tools/apply_grammar.py'
s = io.open(p, encoding='utf-8').read()
s = s.replace("import fix_seek2\n", "import fix_ruin2\nimport fix_seek2\n")
s = s.replace("STEMS.setdefault('TWN_SEEK_PRG', {}).update(fix_seek2.FIX)",
              "STEMS.setdefault('TWN_SEEK_PRG', {}).update(fix_seek2.FIX)\n"
              "STEMS.setdefault('TWN_RUIN_PRG', {}).update(fix_ruin2.FIX)")
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
