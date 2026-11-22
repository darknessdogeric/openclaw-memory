import io
from docx import Document
SRC = r"C:\Users\ericz\Desktop\关于安逸酒店集团2026年度经营情况及.docx"
d = Document(SRC)
out = []
for i in range(31, 37):
    p = d.paragraphs[i]
    out.append("=== P%d ===" % i)
    for j, r in enumerate(p.runs):
        out.append("  run%d bold=%-5s sz=%-5s %r" % (j, r.bold, r.font.size.pt if r.font.size else None, r.text))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\p32_36.txt","w",encoding="utf-8").write("\n".join(out))
print("OK")
