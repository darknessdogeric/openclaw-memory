"""Decode the outline.json properly."""
import re
raw = open(r'D:\OfficeCLI-test\outline.json','rb').read()

# Find 酒店 in UTF-16-LE (5B 91 E8 95)
idx = raw.find(b'\x5b\x91\xe8\x95')
print('Hotel (酒店) UTF-16 found at:', idx)

text = raw.decode('utf-16-le').lstrip('\ufeff')

# Find first title field
pattern = re.compile(r'"title":\s*"([^"]*)"')
matches = pattern.findall(text)
print(f'Found {len(matches)} titles:')
for m in matches:
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in m)
    print(f'  {m!r} (has Chinese: {has_chinese})')
