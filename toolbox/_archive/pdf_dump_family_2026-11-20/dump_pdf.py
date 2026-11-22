# -*- coding: utf-8 -*-
import io, sys
import pdfplumber

SRC = r"C:\Users\ericz\Desktop\产业发展部\重要文件\安逸酒店集团2026年第44周工作例会会议纪要.pdf"
out = []
with pdfplumber.open(SRC) as pdf:
    out.append("PAGES: %d" % len(pdf.pages))
    for i, page in enumerate(pdf.pages, 1):
        out.append("")
        out.append("=" * 100)
        out.append("PAGE %d  size=%s" % (i, page.width, ))
        out.append("=" * 100)
        txt = page.extract_text() or ""
        out.append("[TEXT]")
        out.append(txt)
        tables = page.extract_tables()
        for ti, t in enumerate(tables, 1):
            out.append("[TABLE %d]" % ti)
            for row in t:
                cells = ["" if c is None else str(c).replace("\n", " ") for c in row]
                if any(c.strip() for c in cells):
                    out.append(" | ".join(cells))

dest = r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\meeting_44week.txt"
io.open(dest, "w", encoding="utf-8").write("\n".join(out))
print("OK chars=%d" % sum(len(x) for x in out))
