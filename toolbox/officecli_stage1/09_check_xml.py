"""Compare PPTX XML content vs JSON output for slide titles."""
import zipfile, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with zipfile.ZipFile(r'D:\OfficeCLI-test\test_demo.pptx') as z:
    for i in range(1, 6):
        with z.open(f'ppt/slides/slide{i}.xml') as f:
            x = f.read().decode('utf-8')
        m = re.search(r'<a:t>(.*?)</a:t>', x)
        title = m.group(1) if m else '<no title>'
        print(f'Slide {i} XML: {title!r}')

print()
print('=== Outline JSON (properly decoded) ===')
raw = open(r'D:\OfficeCLI-test\outline.json','rb').read()
text = raw.decode('utf-16-le').lstrip('\ufeff')
pattern = re.compile(r'"title":\s*"([^"]+)"', re.MULTILINE)
for i, m in enumerate(pattern.findall(text), 1):
    print(f'Slide {i} JSON: {m!r}')

print()
print('=== Bytes for first JSON title (hex) ===')
# find first 'title":' then value
m = re.search(r'"title":\s*"([^"]+)"', text)
if m:
    val = m.group(1)
    print(f'UTF-16-LE bytes: {val.encode("utf-16-le").hex()}')
    print(f'UTF-8 bytes: {val.encode("utf-8").hex()}')
