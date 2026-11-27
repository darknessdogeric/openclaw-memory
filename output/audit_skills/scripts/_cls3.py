# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
TB = os.path.join(ROOT,"toolbox")
HOME = os.path.expanduser("~")

FEATS = {
 "表格": r"add_table|Table Grid", "代码块": r"add_code_block|```", "引用": r"blockquote",
 "列表": r"List Bullet|list_item", "图片": r"add_picture|Inches\(", "目录域": r"TOC|add_toc|目录",
 "页眉页脚": r"\.header|\.footer", "分页": r"add_page_break|page_break", "字体设定": r"set_font",
 "行距缩进": r"line_spacing|first_line_indent", "页边距": r"section\.|margin", "主题配色": r"RGBColor|主题|theme",
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
 ("CANON_A_docx-md-bridge", os.path.join(ROOT,"skills","docx-md-bridge","scripts","md_to_docx.py")),
 ("CANON_B_md2docx", os.path.join(TB,"md2docx.py")),
]
caps = {}
print("="*100); print("### A. 能力矩阵（路径正确）"); print("="*100)
for name, p in FILES:
    if not os.path.exists(p):
        print("  %-28s ★不存在" % name); caps[name]=set(); continue
    t = open(p, encoding="utf-8", errors="replace").read()
    caps[name] = {k for k,rx in FEATS.items() if re.search(rx, t, re.M)}
    print("  %-28s %6dB  %s" % (name[:28], len(t), ", ".join(sorted(caps[name]))))

CANON = {"CANON_A_docx-md-bridge","CANON_B_md2docx"}
union = set().union(*[caps[k] for k in CANON])
print()
print("  ★ 权威两套并集（%d 项）: %s" % (len(union), ", ".join(sorted(union))))
print("  ★ 旧克隆『独有』（归档前必须先合并进去）:")
MUST = {}
for name,_ in FILES:
    if name in CANON: continue
    uniq = caps.get(name,set()) - union
    if uniq:
        MUST[name] = uniq
        print("     %-28s %s" % (name[:28], ", ".join(sorted(uniq))))
if not MUST: print("     无")

print()
print("="*100); print("### B. 定向引用扫描（只扫技能/工具/记忆层）"); print("="*100)
SCAN_DIRS = [os.path.join(ROOT,"toolbox"), os.path.join(ROOT,"skills"), os.path.join(ROOT,"memory"),
              os.path.join(ROOT,"agents"), os.path.join(HOME,".claude","skills")]
SCAN_FILES = [os.path.join(ROOT,"AGENTS.md"), os.path.join(ROOT,"MEMORY.md"), os.path.join(ROOT,"SOUL.md")]
files = []
for d in SCAN_DIRS:
    if not os.path.isdir(d): continue
    for base, dirs, fs in os.walk(d):
        dirs[:] = [x for x in dirs if x not in ("__pycache__",".chroma_db",".git","node_modules")]
        for f in fs:
            if f.endswith((".md",".py",".json",".js",".txt")): files.append(os.path.join(base,f))
for f in SCAN_FILES:
    if os.path.exists(f): files.append(f)
print("  扫描 %d 个文件（定向）" % len(files))
targets = ["md_to_docx.py","md_to_docx_clean.py","md_to_docx_v1.0.py","md_to_docx_v2.py","md_to_docx_v3.py",
           "md2docx.py","md2gongwen_docx.py","v4_to_docx.py"]
REF = {}
for tg in targets:
    hits = []
    for f in files:
        if os.path.basename(f) == tg: continue
        try: t = open(f, encoding="utf-8", errors="replace").read()
        except Exception: continue
        if tg in t: hits.append(os.path.relpath(f, ROOT).replace(os.sep,"/"))
    REF[tg] = hits
    print("  %-24s 引用 %d" % (tg, len(hits)))
    for h in hits[:4]: print("        ", h[:98])
json.dump({k:v for k,v in REF.items()}, open(os.path.join(ROOT,"output","audit_skills","_legacy_refs.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"must_merge": MUST, "union": sorted(union)}, open(os.path.join(ROOT,"output","audit_skills","_docx_capabilities.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
