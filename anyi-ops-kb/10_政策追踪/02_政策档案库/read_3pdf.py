"""R66 v2.1 实战:读取3份酒店调研纪要 PDF"""
import fitz  # PyMuPDF
import os
import sys
from pathlib import Path

# Windows GBK 编码兼容
sys.stdout.reconfigure(encoding='utf-8')

PDFS = [
    ("乐山锦江嘉州宾馆", r"C:\Users\ericz\Desktop\产业发展部\酒店调研\乐山锦江嘉州宾馆考察调研会议纪要0813.pdf"),
    ("安逸花园宾馆", r"C:\Users\ericz\Desktop\产业发展部\酒店调研\安逸花园宾馆考察调研会议纪要0813.pdf"),
    ("都江堰国堰宾馆", r"C:\Users\ericz\Desktop\产业发展部\酒店调研\都江堰国堰宾馆考察调研会议纪要0810.pdf"),
]

OUTPUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\anyi-ops-kb\10_政策追踪\02_政策档案库")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

results = {}
for name, pdf_path in PDFS:
    print(f"\n{'='*60}")
    print(f"读取: {name}")
    print(f"路径: {pdf_path}")
    print(f"{'='*60}")
    if not Path(pdf_path).exists():
        print(f"❌ 文件不存在: {pdf_path}")
        continue
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            full_text += f"\n--- Page {page_num+1} ---\n{text}"
        doc.close()
        results[name] = full_text
        print(f"✅ 读取成功,共 {len(full_text)} 字符")
        # 保存为txt文件
        txt_path = OUTPUT_DIR / f"{name}_0813_0810_extracted.txt"
        txt_path.write_text(full_text, encoding='utf-8')
        print(f"📄 已保存: {txt_path}")
    except Exception as e:
        print(f"❌ 读取失败: {e}")

print(f"\n{'='*60}")
print(f"汇总: 成功 {len(results)}/{len(PDFS)}")
print(f"{'='*60}")