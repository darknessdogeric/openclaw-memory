# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
for p in [r"D:\B166ER-openclaw\agents\main\agent\workshop-skills\gongwen-report-cn\SKILL.md",
          r"D:\B166ER-openclaw\workspace\skills\gongwen-docx-cn\SKILL.md"]:
    print("="*100); print(p); print("="*100)
    if not os.path.exists(p):
        print("  ★ 不存在"); continue
    t = open(p, encoding="utf-8", errors="replace").read()
    print(t[:5200])
    print()
