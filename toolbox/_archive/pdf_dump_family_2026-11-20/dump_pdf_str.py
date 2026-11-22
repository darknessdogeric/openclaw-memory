import io, pdfplumber
SRC = r"C:\Users\ericz\Desktop\STR @Chengdu Seminar 20261119_handout.pdf"
out = []
with pdfplumber.open(SRC) as pdf:
    out.append("PAGES: %d" % len(pdf.pages))
    for i, page in enumerate(pdf.pages, 1):
        out.append("")
        out.append("=" * 90)
        out.append("PAGE %d  size=%s" % (i, page.width))
        out.append("=" * 90)
        t = page.extract_text() or ""
        out.append(t)
        for ti, tb in enumerate(page.extract_tables(), 1):
            out.append("[TABLE %d]" % ti)
            for row in tb:
                cells = ["" if c is None else str(c).replace("\n", " ") for c in row]
                if any(c.strip() for c in cells):
                    out.append(" | ".join(cells))
dest = r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\str_chengdu.txt"
io.open(dest, "w", encoding="utf-8").write("\n".join(out))
print("OK chars=%d" % sum(len(x) for x in out))
