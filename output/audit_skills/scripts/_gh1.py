# -*- coding: utf-8 -*-
import io, sys, os, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import requests
H = {"User-Agent":"openclaw-audit"}
for url in [
 "https://raw.githubusercontent.com/VoltAgent/awesome-openclaw-skills/main/categories/pdf-and-documents.md",
 "https://raw.githubusercontent.com/VoltAgent/awesome-openclaw-skills/main/README.md",
]:
    try:
        r = requests.get(url, headers=H, timeout=30)
        print("="*94); print(url); print("  rc=%s len=%d" % (r.status_code, len(r.text)))
        print("-"*94)
        print("\n".join(r.text.split("\n")[:26]))
    except Exception as e:
        print("  失败", str(e)[:90])
