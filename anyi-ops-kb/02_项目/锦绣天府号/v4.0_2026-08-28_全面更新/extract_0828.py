import sys, os
sys.stdout = sys.stdout  # no encoding override needed for file write

PATH = r"C:\Users\ericz\Desktop\产业发展部\熊猫专列\安逸-铁路成都局-心已远-锦绣天府号经营转委确认书（三方）0828.docx"
OUT_DIR = r"D:\B166ER-OpenClaw\workspace\anyi-ops-kb\02_项目\锦绣天府号\v4.0_2026-08-28_全面更新"

# 1. Unzip docx and inspect structure
import zipfile
with zipfile.ZipFile(PATH, 'r') as z:
    names = z.namelist()
    print("=== DOCX 内部结构 ===")
    for n in names:
        info = z.getinfo(n)
        print(f"  {n}  ({info.file_size} bytes)")

# 2. Extract media (images) for OCR
import zipfile
with zipfile.ZipFile(PATH, 'r') as z:
    media = [n for n in z.namelist() if n.startswith('word/media/')]
    print(f"\n=== Media files: {len(media)} ===")
    for m in media:
        info = z.getinfo(m)
        print(f"  {m} ({info.file_size} bytes)")
        out_path = os.path.join(OUT_DIR, os.path.basename(m))
        with z.open(m) as src, open(out_path, 'wb') as dst:
            dst.write(src.read())
        print(f"  → extracted to {out_path}")

# 3. Read document.xml directly (raw text)
print("\n=== document.xml 前 2000 字符 ===")
with zipfile.ZipFile(PATH, 'r') as z:
    try:
        doc_xml = z.read('word/document.xml').decode('utf-8', errors='replace')
    except KeyError:
        doc_xml = ""
    print(f"document.xml size: {len(doc_xml)} chars")
    # Extract text nodes only
    import re
    texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', doc_xml)
    print(f"Found {len(texts)} <w:t> nodes")
    full = "\n".join(texts)
    print(f"Combined text: {len(full)} chars")
    print("\n--- 全部文本内容 ---")
    print(full)
    print("--- END ---")