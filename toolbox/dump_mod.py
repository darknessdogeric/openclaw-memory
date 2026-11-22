import io
from docx import Document
SRC = r"C:\Users\ericz\Desktop\关于安逸酒店集团2026年度经营情况及.docx"
d = Document(SRC)
out = ["段落数=%d 表格数=%d" % (len(d.paragraphs), len(d.tables))]
for i, p in enumerate(d.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    if i >= 17:
        out.append("P%-3d [%s] %s" % (i, p.style.name, t[:120].replace("\n"," ")))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\jingying_mod.txt","w",encoding="utf-8").write("\n".join(out))
print("OK")
