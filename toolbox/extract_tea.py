"""提取安逸茶山三个核心文件的内容，写入一个文本文件供后续 read"""
import pdfplumber
from docx import Document
import openpyxl
import sys
import os

OUT = r"D:\B166ER-OpenClaw\workspace\toolbox\tea_extract.txt"
BASE = r"C:\Users\ericz\Desktop\产业发展部\安逸茶山"

# 三个核心文件
PDF_FANSHU = os.path.join(BASE, '"书山茶海"——安逸茶山×帆书李蕾讲经典文化品牌发布会.pdf')
DOCX_CHANSHAN = os.path.join(BASE, '安逸茶山&安逸美舍产品列表2026.8.26.docx')
XLSX_BAOJIA = os.path.join(BASE, '四川蒙顶山茶业有限公司产品报价表-20260828.xlsx')

# 背景文件（Eric 在这个目录有的）
PDF_STRATEGY = os.path.join(BASE, '四川旅游投资集团与乐见育美文化传播有限公司战略合作框架.pdf')
PDF_COMPANY = os.path.join(BASE, '企业介绍-四川蒙顶山茶业有限公司.pdf')
PDF_MEISHE = os.path.join(BASE, '安逸美舍·蒙顶山茶旅融合项目合作推介.pdf')
DOCX_MEISHE = os.path.join(BASE, '安逸美舍简介.docx')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("【文件1】帆书李蕾讲经典 × 安逸茶山「书山茶海」文化品牌发布会方案（PDF）\n")
    f.write("="*80 + "\n")
    try:
        with pdfplumber.open(PDF_FANSHU) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                f.write(f"\n--- Page {i} ---\n")
                text = page.extract_text()
                if text:
                    f.write(text + "\n")
    except Exception as e:
        f.write(f"ERROR: {e}\n")

    f.write("\n\n" + "="*80 + "\n")
    f.write("【文件2】安逸茶山×帆书战略合作框架协议（PDF）\n")
    f.write("="*80 + "\n")
    try:
        with pdfplumber.open(PDF_STRATEGY) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                f.write(f"\n--- Page {i} ---\n")
                text = page.extract_text()
                if text:
                    f.write(text + "\n")
    except Exception as e:
        f.write(f"ERROR: {e}\n")

    f.write("\n\n" + "="*80 + "\n")
    f.write("【文件3】安逸茶山 & 安逸美舍产品列表 2026.8.26（DOCX）\n")
    f.write("="*80 + "\n")
    try:
        doc = Document(DOCX_CHANSHAN)
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                f.write(f"P{i}: {para.text}\n")
        for t_idx, table in enumerate(doc.tables):
            f.write(f"\n--- Table {t_idx} ---\n")
            for r_idx, row in enumerate(table.rows):
                cells = [cell.text.strip() for cell in row.cells]
                f.write(f"R{r_idx}: " + " | ".join(cells) + "\n")
    except Exception as e:
        f.write(f"ERROR: {e}\n")

    f.write("\n\n" + "="*80 + "\n")
    f.write("【文件4】四川蒙顶山茶业有限公司产品报价表 2026-08-28（XLSX）\n")
    f.write("="*80 + "\n")
    try:
        wb = openpyxl.load_workbook(XLSX_BAOJIA, data_only=True)
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            f.write(f"\n=== Sheet: {sheet_name} (dims: {ws.dimensions}) ===\n")
            for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
                if any(cell is not None and str(cell).strip() for cell in row):
                    f.write(f"R{row_idx}: {list(row)}\n")
    except Exception as e:
        f.write(f"ERROR: {e}\n")

    f.write("\n\n" + "="*80 + "\n")
    f.write("【文件5】四川蒙顶山茶业有限公司 企业介绍（PDF）\n")
    f.write("="*80 + "\n")
    try:
        with pdfplumber.open(PDF_COMPANY) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                f.write(f"\n--- Page {i} ---\n")
                text = page.extract_text()
                if text:
                    f.write(text + "\n")
    except Exception as e:
        f.write(f"ERROR: {e}\n")

    f.write("\n\n" + "="*80 + "\n")
    f.write("【文件6】安逸美舍简介（DOCX）\n")
    f.write("="*80 + "\n")
    try:
        doc = Document(DOCX_MEISHE)
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                f.write(f"P{i}: {para.text}\n")
        for t_idx, table in enumerate(doc.tables):
            f.write(f"\n--- Table {t_idx} ---\n")
            for r_idx, row in enumerate(table.rows):
                cells = [cell.text.strip() for cell in row.cells]
                f.write(f"R{r_idx}: " + " | ".join(cells) + "\n")
    except Exception as e:
        f.write(f"ERROR: {e}\n")

    f.write("\n\n" + "="*80 + "\n")
    f.write("【文件7】安逸美舍·蒙顶山茶旅融合项目合作推介（PDF）\n")
    f.write("="*80 + "\n")
    try:
        with pdfplumber.open(PDF_MEISHE) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                f.write(f"\n--- Page {i} ---\n")
                text = page.extract_text()
                if text:
                    f.write(text + "\n")
    except Exception as e:
        f.write(f"ERROR: {e}\n")

# 输出统计
size = os.path.getsize(OUT)
print(f"OK: 写入 {OUT} ({size} 字节)")
