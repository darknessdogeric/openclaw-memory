import io
from docx import Document
NEW = r"C:\Users\ericz\Desktop\关于安逸酒店集团2026年度经营情况及.docx"
BAK = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革\关于安逸酒店集团2026年度经营情况及_原件_2026-11-03.docx"
dn, db = Document(NEW), Document(BAK)
out = []
out.append("段落数 原件=%d 新件=%d   表格数 原件=%d 新件=%d" % (
    len(db.paragraphs), len(dn.paragraphs), len(db.tables), len(dn.tables)))
out.append("")
out.append("=== 新件 第31-38 段（插入区域） ===")
for i in range(31, min(39, len(dn.paragraphs))):
    p = dn.paragraphs[i]
    if not p.text.strip():
        continue
    out.append("P%d style=%s first=%s" % (i, p.style.name, p.paragraph_format.first_line_indent))
    for r in p.runs:
        out.append("    bold=%-5s sz=%-5s name=%-12s %r" % (
            r.bold, r.font.size.pt if r.font.size else None, r.font.name, r.text[:46]))
out.append("")
out.append("=== 原文完整性抽查（2026部分 9 条 + 2027部分 八是）===")
for kw in ["1.深化市场改革", "2.“铁旅融合”", "9.健全管理制度体系", "一是加强作为酒店集团", "八是轻资产拓展", "三、工作建议", "附件：1."]:
    hit = [i for i, p in enumerate(dn.paragraphs) if p.text.strip().startswith(kw)]
    out.append("  %-22s -> %s" % (kw, hit))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\verify_add.txt","w",encoding="utf-8").write("\n".join(out))
print("OK")
