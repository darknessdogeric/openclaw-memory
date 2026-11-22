import io
from docx import Document
SRC = r"C:\Users\ericz\Desktop\关于安逸酒店集团2026年度经营情况及.docx"
d = Document(SRC)
out = []
for idx in (8, 9, 15, 20, 31):
    p = d.paragraphs[idx]
    out.append("=== P%d style=%s align=%s first_indent=%s ===" % (
        idx, p.style.name, p.alignment, p.paragraph_format.first_line_indent))
    out.append("  text: " + p.text[:70].replace("\n", " "))
    for j, r in enumerate(p.runs):
        out.append("   run%-2d bold=%-5s sz=%-5s name=%-14s %r" % (
            j, r.bold, r.font.size.pt if r.font.size else None, r.font.name, r.text[:38]))
    out.append("")
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\para_runs.txt","w",encoding="utf-8").write("\n".join(out))
print("OK")
