"""Compare raw bytes of XML vs JSON."""
import re

# Read slide1.xml raw
import zipfile
with zipfile.ZipFile(r'D:\OfficeCLI-test\test_demo.pptx') as z:
    with z.open('ppt/slides/slide1.xml') as f:
        xml_bytes = f.read()

print("=== Slide1.xml RAW (looking for title) ===")
# Find the title text
idx = xml_bytes.find(b'<a:t>')
end = xml_bytes.find(b'</a:t>', idx)
title_xml_bytes = xml_bytes[idx+5:end]
print(f"XML title bytes ({len(title_xml_bytes)}): {title_xml_bytes.hex()}")
# UTF-8 decode
print(f"XML title UTF-8: {title_xml_bytes.decode('utf-8')}")

# Read JSON
print()
print("=== Outline JSON, find first title ===")
raw = open(r'D:\OfficeCLI-test\outline.json','rb').read()
# Look for byte pattern matching what we expect from UTF-8
# 酒店供应链管理手册 in UTF-8: e98592 e5ba97 e4be9b e5ba94 e993be e7aea1 e79086 e6898b e5868c
target_utf8 = b'\xe9\x85\x92\xe5\xba\x97\xe4\xbe\x9b\xe5\xba\x94\xe9\x93\xbe\xe7\xae\xa1\xe7\x90\x86\xe6\x89\x8b\xe5\x86\x8c'
idx = raw.find(target_utf8)
print(f"Target UTF-8 pattern found in JSON: {idx}")

# Also look for title in UTF-16-LE
target_utf16 = target_utf8.decode('utf-8').encode('utf-16-le')
idx = raw.find(target_utf16)
print(f"Target UTF-16-LE pattern in JSON: {idx}")

# Where exactly is the title field
# 'title":' in UTF-16-LE
title_key_pos = raw.find(b'\x74\x00\x69\x00\x74\x00\x6c\x00\x65\x00\x22\x00\x3a\x00')
print(f"'title\":' key position: {title_key_pos}")
# Skip 'title":' (14 bytes) and space (2 bytes) and open quote (2 bytes)
val_start = title_key_pos + 14 + 2 + 2
# Find close quote
val_end = raw.find(b'\x22\x00', val_start)
title_bytes = raw[val_start:val_end]
print(f"JSON title bytes ({len(title_bytes)}): {title_bytes.hex()}")
print(f"JSON title UTF-16-LE: {title_bytes.decode('utf-16-le', errors='replace')}")
print(f"JSON title UTF-8 (forced): {title_bytes.decode('utf-8', errors='replace')}")

# Compare to XML
print()
print("=== Side-by-side ===")
print(f"XML title (UTF-8):     {title_xml_bytes.hex()}")
print(f"JSON title (UTF-16):   {title_bytes.hex()}")
print(f"Both length: XML={len(title_xml_bytes)}, JSON={len(title_bytes)}")
