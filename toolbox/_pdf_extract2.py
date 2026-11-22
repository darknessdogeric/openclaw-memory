"""PDF 全文提取（所有页）"""
import pdfplumber

pdf_path = r"C:\Users\ericz\Desktop\产业发展部\培训资料\酒店品牌市场指数综合排名_2026H2_v3.0_2026-08-20.pdf"
out_path = r"D:\B166ER-OpenClaw\workspace\toolbox\pdf_full.txt"

with pdfplumber.open(pdf_path) as pdf:
    out = []
    for i, page in enumerate(pdf.pages):
        out.append(f"\n=== 第 {i+1} 页 ===")
        text = page.extract_text()
        out.append(text if text else "(空)")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"已提取 {len(pdf.pages)} 页")
    print(f"输出: {out_path}")