# -*- coding: utf-8 -*-
"""提取 22 号品牌标准/PIP + 29 号换牌摸底 —— 酒店适配性的品牌方原始依据"""
import io, os, sys, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SRC = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\第一批次文件"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\brand_fit"
os.makedirs(OUT, exist_ok=True)
D22 = os.path.join(SRC, "22.  品牌标准与 PIP 文件 总经理办公室 2026. 11.2")
D29 = os.path.join(SRC, "29. 洲际体系内可换品牌摸底 总经理办公室+总府实业 2026. 11.2")


def dump_docx(p):
    from docx import Document
    doc = Document(p)
    out = []
    for x in doc.paragraphs:
        if x.text.strip():
            out.append(x.text.strip())
    for ti, t in enumerate(doc.tables):
        out.append(f"\n--- TABLE {ti+1} ({len(t.rows)}行 x {len(t.columns)}列) ---")
        for r in t.rows:
            cells = [c.text.strip().replace("\n", " ") for c in r.cells]
            if any(cells):
                out.append(" | ".join(cells))
    return "\n".join(out)


def dump_pdf(p):
    import pymupdf
    doc = pymupdf.open(p)
    pages = []
    for i, page in enumerate(doc):
        pages.append(f"\n===== PAGE {i+1} =====\n" + page.get_text())
    return "\n".join(pages)


def dump_xlsx(p):
    import openpyxl
    wb = openpyxl.load_workbook(p, data_only=True)
    out = []
    for sh in wb.worksheets:
        out.append(f"--- SHEET: {sh.title} ({sh.max_row}x{sh.max_column}) ---")
        for row in sh.iter_rows(values_only=True):
            vals = ["" if v is None else str(v).strip() for v in row]
            if any(vals):
                out.append(" | ".join(vals).rstrip(" |"))
    return "\n".join(out)


def safe(p):
    try:
        e = os.path.splitext(p)[1].lower()
        if e == ".docx":
            return dump_docx(p), "docx"
        if e == ".pdf":
            return dump_pdf(p), "pdf"
        if e == ".xlsx":
            return dump_xlsx(p), "xlsx"
        return None, "skip"
    except Exception as ex:
        return None, f"ERR {ex}"


files = []
for base in (D22, D29):
    for root, dirs, fs in os.walk(base):
        for f in fs:
            files.append(os.path.join(root, f))

print(f"目标 {len(files)} 个文件\n")
index = []
for p in sorted(files):
    rel = os.path.relpath(p, SRC)
    txt, how = safe(p)
    if txt:
        safe_name = re.sub(r'[\\/:*?"<>|]+', "_", rel)
        with open(os.path.join(OUT, safe_name + ".txt"), "w", encoding="utf-8") as f:
            f.write(f"# {rel}\n# {how}\n\n{txt}")
    index.append((rel, how, len(txt) if txt else 0))
    print(f"[{'OK ' if txt else 'ERR'}] {how:>6} {len(txt) if txt else 0:>7} 字符 | {rel}")

print("\n\n" + "=" * 100)
print("【1】换牌至洲际系其他品牌时，洲际方给出的品牌建议与初步标准")
print("=" * 100)
for rel, how, n in index:
    if "品牌建议与初步标准" in rel:
        t = open(os.path.join(OUT, re.sub(r'[\\/:*?"<>|]+', "_", rel) + ".txt"), encoding="utf-8").read()
        print(t.split("\n\n", 1)[1][:9000])

print("\n\n" + "=" * 100)
print("【2】F2-29 沟通纪要 -- 洲际体系内可换品牌摸底")
print("=" * 100)
for rel, how, n in index:
    if "F2-29" in rel:
        t = open(os.path.join(OUT, re.sub(r'[\\/:*?"<>|]+', "_", rel) + ".txt"), encoding="utf-8").read()
        print(t.split("\n\n", 1)[1][:9000])
