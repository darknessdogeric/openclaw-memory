import fitz, docx, openpyxl, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OUT_DIR = r"D:/B166ER-OpenClaw/workspace/toolbox/chashan_extract"
import os
os.makedirs(OUT_DIR, exist_ok=True)

# 1. PDF 活动策划
print("=" * 60)
print("=== 1. 书山茶海 PDF ===")
print("=" * 60)
d = fitz.open(r"C:\Users\ericz\Desktop\产业发展部\安逸茶山\“书山茶海”——安逸茶山×帆书李蕾讲经典文化品牌发布会.pdf")
pdf_text = ""
for i, page in enumerate(d):
    pdf_text += f"\n=== Page {i+1} ===\n"
    pdf_text += page.get_text()
print(pdf_text)
with open(f"{OUT_DIR}/01_pdf_书山茶海_活动策划.txt", "w", encoding="utf-8") as f:
    f.write(pdf_text)

# 2. docx 产品列表
print("\n\n" + "=" * 60)
print("=== 2. 安逸茶山&安逸美舍产品列表 docx ===")
print("=" * 60)
d2 = docx.Document(r"C:\Users\ericz\Desktop\产业发展部\安逸茶山\安逸茶山&安逸美舍产品列表2026.8.26.docx")
docx_text = ""
for i, t in enumerate(d2.tables):
    docx_text += f"\n--- Table {i} ({len(t.rows)}x{len(t.columns)}) ---\n"
    for r in t.rows:
        docx_text += " | ".join(c.text for c in r.cells) + "\n"
for p in d2.paragraphs:
    if p.text.strip():
        docx_text += p.text + "\n"
print(docx_text)
with open(f"{OUT_DIR}/02_docx_产品列表.txt", "w", encoding="utf-8") as f:
    f.write(docx_text)

# 3. xlsx 产品报价
print("\n\n" + "=" * 60)
print("=== 3. 四川蒙顶山茶业产品报价表 xlsx ===")
print("=" * 60)
wb = openpyxl.load_workbook(r"C:\Users\ericz\Desktop\产业发展部\安逸茶山\四川蒙顶山茶业有限公司产品报价表-20260828.xlsx")
xlsx_text = ""
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    xlsx_text += f"\n=== Sheet: {sheet_name} ===\n"
    for row in ws.iter_rows(values_only=True):
        xlsx_text += " | ".join(str(c) if c is not None else "" for c in row) + "\n"
print(xlsx_text)
with open(f"{OUT_DIR}/03_xlsx_产品报价.txt", "w", encoding="utf-8") as f:
    f.write(xlsx_text)

print(f"\n\n[DONE] Saved to {OUT_DIR}")