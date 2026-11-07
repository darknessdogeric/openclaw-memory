"""读取 docx 并提取全部内容"""
import os
from docx import Document

path = r"C:\Users\ericz\Desktop\八年辗转回到原点.docx"
doc = Document(path)

# 段落
print("=== 段落 ===")
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f"[{i:3d}] [{p.style.name}] {p.text}")

# 表格
print(f"\n=== 表格 ({len(doc.tables)}) ===")
for ti, tbl in enumerate(doc.tables):
    print(f"\n-- 表格 {ti} ({len(tbl.rows)} 行) --")
    for ri, row in enumerate(tbl.rows):
        cells = [c.text.strip() for c in row.cells]
        print(f"  行{ri}: {cells}")

# 元数据
print(f"\n=== 元数据 ===")
cp = doc.core_properties
for attr in ["author", "title", "subject", "created", "modified", "last_modified_by", "revision"]:
    try:
        v = getattr(cp, attr)
        if v: print(f"  {attr}: {v}")
    except: pass

# 字符数
total_chars = sum(len(p.text) for p in doc.paragraphs)
print(f"\n总段落: {len(doc.paragraphs)}")
print(f"总字符: {total_chars}")
