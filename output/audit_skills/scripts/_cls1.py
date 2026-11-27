# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, hashlib, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
TB = os.path.join(ROOT,"toolbox")

print("="*94); print("### A. 旧克隆 vs 现有两套：功能差异（合并唯一内容的前提）"); print("="*94)
CANDS = ["md_to_docx.py","md_to_docx_clean.py","md_to_docx_v1.0.py","md_to_docx_v2.py","md_to_docx_v3.py",
         "md2docx.py", os.path.join("..","skills","docx-md-bridge","scripts","md_to_docx.py")]
FEATS = {
 "表格": r"add_table|Table Grid",
 "代码块": r"add_code_block|```",
 "引用": r"blockquote|引用|^\s*>",
 "列表": r"List Bullet|list_item|列表",
 "图片": r"add_picture|Inches|\.png|\.jpg",
 "目录": r"TOC|目录",
 "页眉页脚": r"header|footer|页眉|页脚",
 "分页": r"add_page_break|分页|page_break",
 "字体设定": r"set_font|宋体|黑体|方正小标宋",
 "行距缩进": r"line_spacing|first_line_indent|缩进|行距",
 "页边距": r"section\.|margin|页边距",
 "目录/编号": r"numbering|编号",
}
for c in CANDS:
    p = os.path.join(TB, c) if not c.startswith("..") else os.path.join(ROOT, c.replace("/", os.sep))
    if not os.path.exists(p): print("  ★ 缺 %s" % c); continue
    t = open(p, encoding="utf-8", errors="replace").read()
    hits = [k for k,rx in FEATS.items() if re.search(rx, t, re.M|re.I)]
    print("  %-26s %6d B ｜ %2d/%d 能力: %s" % (os.path.basename(c), len(t), len(hits), len(FEATS), ", ".join(hits)))
print()
print("  ★ 各克隆独有能力（相对 docx-md-bridge ＋ md2docx 的并集）:")
union = set()
for c in ["md2docx.py"]:
    p = os.path.join(TB,c); t = open(p,encoding="utf-8",errors="replace").read()
    union = {k for k,rx in FEATS.items() if re.search(rx,t,re.M|re.I)}
p = os.path.join(ROOT,"skills","docx-md-bridge","scripts","md_to_docx.py")
t = open(p,encoding="utf-8",errors="replace").read()
union |= {k for k,rx in FEATS.items() if re.search(rx,t,re.M|re.I)}
for c in ["md_to_docx.py","md_to_docx_clean.py","md_to_docx_v1.0.py","md_to_docx_v2.py","md_to_docx_v3.py"]:
    p = os.path.join(TB,c); t = open(p,encoding="utf-8",errors="replace").read()
    uniq = {k for k,rx in FEATS.items() if re.search(rx,t,re.M|re.I)} - union
    print("     %-26s 独有: %s" % (c, ", ".join(sorted(uniq)) if uniq else "无"))

print()
print("="*94); print("### B. 谁在引用这些旧克隆（不能盲删）"); print("="*94)
for c in ["md_to_docx.py","md_to_docx_clean.py","md_to_docx_v1.0.py","md_to_docx_v2.py","md_to_docx_v3.py","md2docx.py","md2gongwen_docx.py","v4_to_docx.py"]:
    r = subprocess.run(["grep","-rl","--include=*.md","--include=*.py","--include=*.json","--include=*.js",c,ROOT],
                       capture_output=True, timeout=90)
    hits = [x for x in r.stdout.decode("utf-8","replace").split("\n") if x.strip() and "_audit" not in x and "audit_skills" not in x]
    print("  %-26s 引用 %d 处" % (c, len(hits)))
    for h in hits[:4]:
        print("        ", os.path.relpath(h, ROOT).replace(os.sep,"/")[:96])

print()
print("="*94); print("### C. selfcheck.py 现状（要往里加新断言）"); print("="*94)
sc = os.path.join(ROOT,"toolbox","selfcheck.py")
t = open(sc, encoding="utf-8", errors="replace").read()
print("  %d B ｜ 行 %d" % (len(t), t.count("\n")+1))
for m in re.finditer(r"^\s*(?:def\s+)?(c\d\d|C\d\d)\b[^\n]{0,110}", t, re.M):
    print("    ", m.group(0).strip()[:108])
