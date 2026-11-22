import zipfile, re, os

PATH = r"C:\Users\ericz\Desktop\产业发展部\熊猫专列\安逸-铁路成都局-心已远-锦绣天府号经营转委确认书（三方）0828.docx"
OUT = r"D:\B166ER-OpenClaw\workspace\anyi-ops-kb\02_项目\锦绣天府号\v4.0_2026-08-28_全面更新\0828_xml_text.txt"

with zipfile.ZipFile(PATH, 'r') as z:
    doc_xml = z.read('word/document.xml').decode('utf-8', errors='replace')

texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', doc_xml)
full = "\n".join(texts)

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(f"=== 0828 转委确认书 document.xml 文本提取 ===\n")
    f.write(f"段落数 (w:t 节点): {len(texts)}\n")
    f.write(f"总字符: {len(full)}\n\n")
    f.write(full)

print(f"Saved to {OUT}, {len(full)} chars")

# Also dump first 500 chars hex
print("\n=== 前 30 段 w:t 节点（hex）===")
for i, t in enumerate(texts[:30]):
    print(f"[T{i:02d}] {repr(t)}")