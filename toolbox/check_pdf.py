import sys
try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("NEITHER pypdf NOR PyPDF2 INSTALLED")
        sys.exit(0)

pdf_path = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0\02-分章节PDFs\01-主报告-酒店供应链工程全维度体系.pdf"
reader = PdfReader(pdf_path)
print(f"Pages: {len(reader.pages)}")
print("---")
text = reader.pages[0].extract_text()
print(f"First page text (first 600 chars):")
print(text[:600])
print("---")
text2 = reader.pages[1].extract_text()
print(f"Page 2 text (first 600 chars):")
print(text2[:600])