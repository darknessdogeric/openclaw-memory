"""Verify outline.json has correct Chinese."""
import json

with open(r'D:\OfficeCLI-test\outline.json', 'rb') as f:
    raw = f.read()
print(f"Raw bytes: {len(raw)}")
print(f"BOM: {raw[:3].hex()}")

if raw[:2] == b'\xff\xfe':
    text = raw.decode('utf-16-le').lstrip('\ufeff')
    print("Decoded as UTF-16-LE")
elif raw[:3] == b'\xef\xbb\xbf':
    text = raw.decode('utf-8-sig')
    print("Decoded as UTF-8 BOM")
else:
    text = raw.decode('utf-8', errors='replace')
    print("Decoded as UTF-8")

data = json.loads(text)
print()
print(f"Total slides: {data['data']['totalSlides']}")
for s in data['data']['slides']:
    title = s['title']
    # Check Chinese characters
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in title)
    print(f"  Slide {s['index']}: {title!r} (has Chinese: {has_chinese})")
