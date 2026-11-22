import io
from docx import Document
NEW = r"C:\Users\ericz\Desktop\关于安逸酒店集团2026年度经营情况及.docx"
d = Document(NEW)
out = ["段落数=%d 表格数=%d" % (len(d.paragraphs), len(d.tables))]
for i in range(31, 39):
    if i >= len(d.paragraphs):
        break
    p = d.paragraphs[i]
    if not p.text.strip():
        continue
    out.append("")
    out.append("P%d  [%s] first=%s" % (i, p.style.name, p.paragraph_format.first_line_indent))
    for r in p.runs:
        out.append("   bold=%-5s sz=%-5s %-14s %r" % (r.bold, r.font.size.pt if r.font.size else None, r.font.name, r.text[:56]))
out.append("")
out.append("=== 完整性抽查 ===")
for kw in ["一、2026年度任务完成情况", "二、2027年度工作举措", "三是大运管中心建设", "八是轻资产拓展", "1.完善品牌标准", "4.推进存量改造策划", "5.深化平台渠道合作", "三、工作建议", "附件：1."]:
    hit = [i for i, p in enumerate(d.paragraphs) if p.text.strip().startswith(kw)]
    out.append("  %-24s -> %s" % (kw, hit))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\verify_p5.txt","w",encoding="utf-8").write("\n".join(out))
print("OK")
