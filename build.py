#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build.py — يحقن data/entries.json داخل index.html بين علامتي ILHAM_DATA.
الاستخدام:  python3 build.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(ROOT, "index.html")
DATA = os.path.join(ROOT, "data", "entries.json")

with open(DATA, encoding="utf-8") as f:
    entries = json.load(f)

# ترتيب حسب التاريخ (الأقدم أولاً كما في الملف)
data_json = json.dumps(entries, ensure_ascii=False, indent=2)

with open(INDEX, encoding="utf-8") as f:
    html = f.read()

START = "<!--ILHAM_DATA_START-->"
END = "<!--ILHAM_DATA_END-->"
if START not in html or END not in html:
    sys.exit("ERROR: placeholders not found in index.html")

html = html[:html.index(START)+len(START)] + "\n" + data_json + "\n" + html[html.index(END):]

with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)

print(f"OK: injected {len(entries)} entries into index.html")
