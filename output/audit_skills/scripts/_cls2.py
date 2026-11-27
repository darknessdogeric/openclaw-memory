# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
TB = os.path.join(ROOT,"toolbox")

FEATS = {
 "表格": r"add_table|Table Grid",
 "代码块": r"add_code_block|```",
 "引用": r"blockquote",
 "列表": r"List Bullet|list_item",
 "图片": r"add_picture|Inches\(",
 "目录域": r"TOC|add_toc|目录",
 "页眉页脚": r"\.header|\.footer",
 "分页": r"add_page_break|page_break",
 "字体设定": r"set_font",
 "行距缩进": r"line_spacing|first_line_indent",
 "页边距": r"section\.|margin",
 "主题配色": r"RGBColor|HEX|主题|theme",
}
FILES = [
 ("md_to_docx.py", os.path.join(TB,"md_to_docx.py")),
 ("md_to_docx_clean.py", os.path.join(TB,"md_to_docx_clean.py")),
 ("md_to_docx_v1.0.py", os.path.join(TB,"md_to_docx_v1.0.py")),
 ("md_to_docx_v2.py", os.path.join(TB,"md_to_docx_v2.py")),
 ("md_to_docx_v3.py", os.path.join(TB,"md_to_docx_v3.py")),
 ("md2docx.py", os.path.join(TB,"md2docx.py")),
 ("md2gongwen_docx.py", os.path.join(TB,"md2gongwen_docx.py")),
 ("v4_to_docx.py", os.path.join(TB,"v4_to_docx.py")),
 ("★docx-md-bridge", os.path.join(ROOT,"skills","docx-md-bridge","scripts","md_to_docx.py")),
]
caps = {}
print("="*100); print("### A. 能力矩阵（路径已修正）"); print("="*100)
print("  %-24s %7s  %s" % ("文件","字节","能力"))
for name, p in FILES:
    if not os.path.exists(p):
        print("  %-24s  ★不存在 %s" % (name, p)); continue
    t = open(p, encoding="utf-8", errors="replace").read()
    c = {k for k,rx in FEATS.items() if re.search(rx, t, re.M)}
    caps[name] = c
    print("  %-24s %6dB  %s" % (name[:24], len(t), ", ".join(sorted(c))))

CANON = {"md2docx.py", "★docx-md-bridge"}
union = set().union(*[caps[k] for k in caps if k in CANON]) if CANON & set(caps) else set()
print()
print("  ★ 权威两套并集（%d 项）: %s" % (len(union), ", ".join(sorted(union))))
print()
print("  ★ 各旧克隆相对权威两套的『独有』能力（= 合并前必须保留的）:")
for name,_ in FILES:
    if name in CANON: continue
    uniq = caps.get(name,set()) - union
    print("     %-24s %s" % (name[:24], ", ".join(sorted(uniq)) if uniq else "无 → 可安全归档"))

print()
print("="*100); print("### B. 引用扫描（纯 Python 递归，不用 grep）"); print("="*100)
SKIP = {"\\.git\\", "\\node_modules\\", "\\output\\audit_skills\\", "\\__pycache__\\", "\\.chroma_db\\"}
targets = ["md_to_docx.py","md_to_docx_clean.py","md_to_docx_v1.0.py","md_to_docx_v2.py","md_to_docx_v3.py",
           "md2docx.py","md2gongwen_docx.py","v4_to_docx.py"]
files = []
for base,dirs,fs in os.walk(ROOT):
    if any(s.lower() in base.lower() for s in SKIP): dirs[:] = []; continue
    dirs[:] = [d for d in dirs if d not in (".git","node_modules","__pycache__",".chroma_db","venv",".venv")]
    for f in fs:
        if f.endswith((".md",".py",".json",".js",".txt",".yaml",".yml")):
            files.append(os.path.join(base,f))
print("  扫描 %d 个文本文件" % len(files))
for tg in targets:
    hits = []
    for f in files:
        if f.endswith(os.path.basename(tg)): continue
        try: t = open(f, encoding="utf-8", errors="replace").read()
        except Exception: continue
        if tg in t:
            hits.append(os.path.relpath(f, ROOT).replace(os.sep,"/"))
    print("  %-24s 引用 %d" % (tg, len(hits)))
    for h in hits[:5]: print("        ", h[:100])
