import openpyxl, io
from docx import Document
from docx.shared import Pt
SRC = r"C:\Users\ericz\Desktop\关于安逸酒店集团2026年度经营情况及.docx"
d = Document(SRC)
out = []
for i, p in enumerate(d.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    pf = p.paragraph_format
    info = "pf.first=%s left=%s spacing=%s" % (
        pf.first_line_indent, pf.left_indent, pf.line_spacing)
    runs = []
    for r in p.runs[:3]:
        runs.append("[%s b=%s sz=%s]" % (r.text[:14], r.bold, r.font.size.pt if r.font.size else None))
    out.append("P%-3d %s | %s | %s" % (i, t[:44].replace("\n", " "), info, " ".join(runs)))
out.append("")
out.append("=== 八是段落 run 明细 ===")
for i, p in enumerate(d.paragraphs):
    if p.text.strip().startswith("八是轻资产"):
        out.append("index=%d" % i)
        for j, r in enumerate(p.runs):
            out.append("  run%d %r bold=%s size=%s name=%s" % (j, r.text[:30], r.bold,
                r.font.size.pt if r.font.size else None, r.font.name))
        out.append("  style=%s align=%s" % (p.style.name, p.alignment))
        pf = p.paragraph_format
        out.append("  first_indent=%s left=%s spacing=%s before=%s after=%s" % (
            pf.first_line_indent, pf.left_indent, pf.line_spacing, pf.space_before, pf.space_after))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\jingying_para.txt","w",encoding="utf-8").write("\n".join(out))
print("OK")
