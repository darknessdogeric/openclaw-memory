# -*- coding: utf-8 -*-
"""修复 cross_audit_rooms.py 中被转义破坏的插入块；并生成独立的审计首页摘录脚本"""
import io, os, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CALC = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
P = os.path.join(CALC, "cross_audit_rooms.py")
t = open(P, encoding="utf-8").read()

start = t.find('    o.write("\\n\\n## 三、各年审计首页原文')
end = t.find('    o.write(f"\\n\\n**互证结论**')
if start != -1 and end != -1 and end > start:
    t = t[:start] + t[end:]
    print("removed broken block")
else:
    print("broken block not found (start=%s end=%s)" % (start, end))
open(P, "w", encoding="utf-8").write(t)

# 独立脚本：三年审计 PAGE 1-2 原文摘录
EX = os.path.join(CALC, "audit_pages.py")
open(EX, "w", encoding="utf-8").write('''# -*- coding: utf-8 -*-
import io, os, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BF = r"D:\\B166ER-openclaw\\workspace\\anyi-ops-kb\\02_项目\\总府皇冠假日\\_calc\\brand_fit"
DST = os.path.join(BF, "_PAGES.md")

def find(y):
    for p in glob.glob(os.path.join(BF, "*清单_" + y + "_*.txt")):
        if "Non" in os.path.basename(p):
            return p
    for p in glob.glob(os.path.join(BF, "*" + y + "*.txt")):
        b = os.path.basename(p)
        if "Non" in b and ("_" + y + "_") in b:
            return p
    return None

with open(DST, "w", encoding="utf-8") as o:
    for y in ("2024", "2025", "2026"):
        p = find(y)
        o.write("\\n\\n" + "=" * 88 + "\\n## " + y + " 年 IHG 审计 · PAGE 1-2 原文\\n" + "=" * 88 + "\\n\\n")
        if not p:
            o.write("(未找到)\\n"); continue
        t = open(p, encoding="utf-8").read()
        body = t.split("\\n\\n", 1)[1] if "\\n\\n" in t else t
        for pg in body.split("===== PAGE ")[1:3]:
            head = pg.split("\\n", 1)
            o.write("\\n```\\nPAGE " + head[0].strip() + "\\n" + (head[1] if len(head) > 1 else "")[:2600] + "\\n```\\n")
print("pages digest ok")
''')
print("wrote", EX)
