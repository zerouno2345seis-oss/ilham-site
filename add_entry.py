#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_entry.py — إضافة تدوينة جديدة إلى موقع «إلهام» ونشرها على GitHub Pages.

الاستخدام:
    python3 add_entry.py <entry.json>          # إضافة + بناء + نشر
    python3 add_entry.py <entry.json> --no-push  # إضافة وبناء فقط دون نشر

يمنع التكرار تلقائياً (لو الرابط موجود من قبل يتجاهل).
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "entries.json")

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 add_entry.py <entry.json> [--no-push]")
    src = sys.argv[1]
    no_push = "--no-push" in sys.argv

    with open(src, encoding="utf-8") as f:
        entry = json.load(f)

    with open(DATA, encoding="utf-8") as f:
        entries = json.load(f)

    # منع التكرار حسب رابط المصدر
    for e in entries:
        if e.get("source") == entry.get("source"):
            sys.exit(f"SKIP: هذا الرابط مضاف من قبل ({e.get('id')})")

    entries.append(entry)
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"ADDED: {entry.get('id','?')} — {entry.get('title','?')[:60]}")

    # بناء الصفحة (حقن البيانات)
    subprocess.run([sys.executable, os.path.join(ROOT, "build.py")], check=True)

    if no_push:
        print("OK (no push)")
        return

    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    r = subprocess.run(["git", "commit", "-q", "-m", "Add entry " + entry.get("id", "")], cwd=ROOT)
    if r.returncode != 0:
        print("WARN: git commit failed (لا جديد؟)")
        return
    subprocess.run(["git", "push", "-q", "origin", "main"], cwd=ROOT, check=True)
    print("PUSHED — GitHub Pages سيحدّث الموقع خلال دقيقة تقريباً")

if __name__ == "__main__":
    main()
