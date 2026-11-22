import io
from docx import Document
p = r"C:\Users\ericz\Desktop\岭博网关方案_费用对比与三层匹配改造建议_v1.0_2026-11-05.docx"
d = Document(p)
out = []
for i, t in enumerate(d.tables):
    hdr = [c.text.strip() for c in t.rows[0].cells]
    if "错位" in hdr[1] or "三年总拥有成本" in hdr[0]:
        out.append("TABLE %d hdr=%s" % (i, hdr))
        for r in t.rows[1:]:
            out.append("   | " + " | ".join(c.text.strip()[:110] for c in r.cells))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_verify\fee_tables.txt","w",encoding="utf-8").write("\n".join(out))
print("OK")
