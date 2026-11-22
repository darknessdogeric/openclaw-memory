"""Look at raw UTF-16-LE output bytes."""
import re
raw = open(r'D:\OfficeCLI-test\outline.json','rb').read()
print('Length:', len(raw))

# Find "title" in utf-16: 't\x00i\x00t\x00l\x00e\x00' = b'\x74\x00\x69\x00\x74\x00\x6c\x00\x65\x00'
pattern = b'\x22\x00\x74\x00\x69\x00\x74\x00\x6c\x00\x65\x00\x22\x00'
idx = raw.find(pattern)
print(f'first title at byte: {idx}')

# The next bytes after 'title":' are the value
# 'title":' = 't\x00i\x00t\x00l\x00e\x00"\x00:\x00' = 14 bytes
val_start = idx + 14
print('Bytes after title: ')
print('hex:', raw[val_start:val_start+80].hex())
# The opening quote is at val_start (assumed), then value, then closing quote
# Find next quote after val_start+2
quote_pos = raw.find(b'\x22\x00', val_start + 2)
value_bytes = raw[val_start + 2:quote_pos]
print('value bytes hex:', value_bytes.hex())
print('value bytes utf-16:', value_bytes.decode('utf-16-le', errors='replace'))

# Also look at actual pptx content
import zipfile
print()
print('=== Look at pptx internals ===')
with zipfile.ZipFile(r'D:\OfficeCLI-test\test_demo.pptx') as z:
    slides = [n for n in z.namelist() if n.startswith('ppt/slides/slide')]
    print(f'Slides: {slides}')
    for sn in slides[:3]:
        with z.open(sn) as f:
            content = f.read()
            print(f'\n--- {sn} (size: {len(content)}) ---')
            print(content.decode('utf-8', errors='replace')[:2000])
