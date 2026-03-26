import sys
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
import os

base = r"C:\Users\ericz\Desktop\自我革命"

files = [
    os.path.join(base, r"AI智能获客方案\AI+实体酒店解决方案.docx"),
    os.path.join(base, r"AI智能获客方案\AI酒店行业应用方案.docx"),
    os.path.join(base, r"商业计划书\下一代AI+去中心化旅行平台商业计划.docx"),
    os.path.join(base, r"商业计划书\单体酒店数智化商业计划书.docx"),
    os.path.join(base, r"商业计划书\亚朵营收分析商业计划书.docx"),
    os.path.join(base, r"单体酒店专题\酒店AI赋能各部门\AI赋能酒店营销.docx"),
    os.path.join(base, r"单体酒店专题\酒店AI赋能各部门\AI赋能酒店收益.docx"),
    os.path.join(base, r"单体酒店专题\酒店AI赋能各部门\AI赋能酒店前厅.docx"),
    os.path.join(base, r"单体酒店专题\酒店AI赋能各部门\AI赋能酒店人资.docx"),
    os.path.join(base, r"单体酒店专题\酒店直客全生命周期数字化.docx"),
]

for f in files:
    if os.path.exists(f):
        size_kb = os.path.getsize(f) / 1024
        doc = Document(f)
        text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
        preview = text[:300].replace('\n', ' ')
        print(f"OK|{os.path.basename(f)}|{size_kb:.1f}KB|{len(text)}chars")
        print(preview[:200])
        print("---")
    else:
        print(f"MISSING|{f}")
