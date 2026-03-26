import json
from docx import Document
import os
import zipfile
import re

# Get the corrupted file content
corrupted_file = r"C:\Users\ericz\Desktop\自我革命\商业计划书\单体酒店数智化商业计划书.docx"

with zipfile.ZipFile(corrupted_file, 'r') as z:
    with z.open('word/document.xml') as f:
        xml_content = f.read().decode('utf-8', errors='ignore')
        text = re.sub(r'<[^>]+>', ' ', xml_content)
        text = re.sub(r'\s+', ' ', text).strip()

result = {
    'task_name': '单体酒店数智化商业计划书.docx',
    'status': 'CORRUPTED_BUT_XML_RECOVERED',
    'full_path': corrupted_file,
    'rel_path': '自我革命\\商业计划书\\单体酒店数智化商业计划书.docx',
    'name': '单体酒店数智化商业计划书.docx',
    'size_kb': round(os.path.getsize(corrupted_file) / 1024, 1),
    'text_len': len(text),
    'preview': text[:500]
}

with open(r'C:\Users\ericz\.openclaw\workspace\memory\corrupted_recovered.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Recovered: {len(text)} chars")
