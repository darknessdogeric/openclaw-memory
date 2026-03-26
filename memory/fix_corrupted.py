import json
from docx import Document
import os
import zipfile
import re

corrupted_file = r"C:\Users\ericz\Desktop\自我革命\商业计划书\单体酒店数智化商业计划书.docx"

try:
    with zipfile.ZipFile(corrupted_file, 'r') as z:
        with z.open('word/document.xml') as f:
            xml_content = f.read().decode('utf-8', errors='ignore')
            # Strip XML tags to get text
            text = re.sub(r'<[^>]+>', ' ', xml_content)
            text = re.sub(r'\s+', ' ', text).strip()
            print(f"ZIP OK: {len(text)} chars")
            print(text[:3000])
except Exception as e:
    print(f"ZIP ERROR: {e}")
