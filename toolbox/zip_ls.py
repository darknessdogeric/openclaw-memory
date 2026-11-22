import zipfile, os
p = r"C:\Users\ericz\Desktop\大运营体系组织构架方案20261026（定稿）.docx"
z = zipfile.ZipFile(p)
out = []
for n in z.namelist():
    info = z.getinfo(n)
    out.append("%-60s %8d" % (n, info.file_size))
out.append("")
out.append("=== media ===")
for n in z.namelist():
    if n.startswith("word/media/") or "embeddings" in n:
        out.append(n)
open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\dzyl_zip.txt","w",encoding="utf-8").write("\n".join(out))
print("\n".join(x for x in out if "media" in x or "embed" in x or "document.xml" in x))
