"""批量把 02-分章节PDFs/ 下的 13 个 MD 文件转为 PDF"""
import os
import sys
import glob

sys.path.insert(0, r"D:\B166ER-OpenClaw\workspace\toolbox")
from md_to_pdf import md_to_pdf

PDF_DIR = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0\02-分章节PDFs"

md_files = sorted(glob.glob(os.path.join(PDF_DIR, "*.md")))
print(f"Found {len(md_files)} MD files")

success = 0
failed = []
for md_path in md_files:
    base = os.path.splitext(os.path.basename(md_path))[0]
    pdf_path = os.path.join(PDF_DIR, base + ".pdf")
    try:
        md_to_pdf(md_path, pdf_path, base)
        size = os.path.getsize(pdf_path)
        print(f"OK  {base}.pdf  ({size:,} bytes)")
        success += 1
    except Exception as e:
        print(f"FAIL  {base}.pdf  - {e}")
        failed.append((base, str(e)))

print(f"\nResult: {success}/{len(md_files)} succeeded")
if failed:
    print("Failed:")
    for f, e in failed:
        print(f"  - {f}: {e}")