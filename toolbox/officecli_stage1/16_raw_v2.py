"""Look at slide1.xml raw output (corrected path)."""
raw = open(r'D:\OfficeCLI-test\slide1_raw2.bin', 'rb').read()
print(f'Length: {len(raw)}')
print(f'BOM: {raw[:3].hex()}')

# Decode as UTF-16-LE
text = raw.decode('utf-16-le').lstrip('\ufeff')
with open(r'D:\OfficeCLI-test\slide1_xml_utf16.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print(f'Saved {len(text)} chars')

# Find title
import re
m = re.search(r'<a:t>([^<]+)</a:t>', text)
if m:
    title = m.group(1)
    print(f'Title found: len={len(title)}, hex={title.encode("utf-16-le").hex()}')

# Also save bytes
with open(r'D:\OfficeCLI-test\slide1_xml.bin', 'wb') as f:
    f.write(text.encode('utf-8'))
