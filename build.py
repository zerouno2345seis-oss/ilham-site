#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build.py — يحقن data/entries.json داخل وسم البيانات في index.html.
الاستخدام:  python3 build.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(ROOT, "index.html")
DATA = os.path.join(ROOT, "data", "entries.json")

with open(DATA, encoding="utf-8") as f:
    entries = json.load(f)

data_json = json.dumps(entries, ensure_ascii=False, indent=2)

with open(INDEX, encoding="utf-8") as f:
    html = f.read()

pattern = re.compile(r'(<script type="application/json" id="ilham-data">)([\s\S]*?)(</script>)')
if not pattern.search(html):
    sys.exit("ERROR: data script tag not found in index.html")

html = pattern.sub(lambda m: m.group(1) + "\n" + data_json + "\n" + m.group(3), html, count=1)

with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)

print(f"OK: injected {len(entries)} entries into index.html")
