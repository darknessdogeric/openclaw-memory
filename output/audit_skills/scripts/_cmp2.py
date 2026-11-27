# -*- coding: utf-8 -*-
import io, sys, os, re, glob, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
TMP = os.path.join(ROOT, "output", "_t")
os.makedirs(TMP, exist_ok=True)
MD = os.path.join(TMP, "cmp.md")
open(MD, "w", encoding="utf-8").write(
"# 标题一\n\n段落正文。\n\n| 列 A | 列 B | 列 C |\n|---|---|---|\n| 1 | 2 | 3 |\n| 4 | 5 | 6 |\n\n> 引用一行\n\n## 二级标题\n\n- 列表项一\n- 列表项二\n")
print("测试 md: 1 标题 + 1 段 + 2 行 3 列表 + 引用 + 二级标题 + 2 列表项")
print()
import docx
CANDS = [
 ("既有轮子 docx-md-bridge", os.path.join(ROOT,"skills","docx-md-bridge","scripts","md_to_docx.py")),
 ("我今天造的 toolbox/md2docx", os.path.join(ROOT,"toolbox","md2docx.py")),
]
for label, script in CANDS:
    if not os.path.exists(script):
        print("  %-30s ★ 脚本不存在" % label); continue
    out = os.path.join(TMP, label.split()[0] + ".docx")
    if os.path.exists(out): os.remove(out)
    try:
        r = subprocess.run([sys.executable, script, MD, out], capture_output=True, timeout=150)
        if not os.path.exists(out):
            print("  %-30s ★ 未产出（rc=%s）%s" % (label, r.returncode, r.stderr.decode("utf-8","replace")[-90:])); continue
        d = docx.Document(out)
        paras = [x.text.strip() for x in d.paragraphs if x.text.strip()]
        tbl = len(d.tables); rows = sum(len(t.rows) for t in d.tables)
        print("  %-30s 段落 %2d ｜ 表格 %d（%d 行）" % (label, len(paras), tbl, rows))
        print("       表格首行: %s" % (d.tables[0].rows[0].cells[0].text if tbl else "★ 无表格"))
    except Exception as e:
        print("  %-30s ★ 失败 %s" % (label, str(e)[:70]))
print()
print("=== docx-md-bridge 的表格判定代码 ===")
p = os.path.join(ROOT,"skills","docx-md-bridge","scripts","md_to_docx.py")
t = open(p, encoding="utf-8", errors="replace").read()
for i,l in enumerate(t.split("\n")):
    if re.search(r"(table|rows|\|)", l) and re.search(r"(start|sep|---|is_table|split|strip)", l):
        print("   L%-4d %s" % (i+1, l.strip()[:122]))
