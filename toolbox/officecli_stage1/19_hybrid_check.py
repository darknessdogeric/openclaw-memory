"""Check the hybrid_test.pptx using both XML and python-pptx."""
import zipfile, re
from pptx import Presentation

PPTX = r"D:\OfficeCLI-test\hybrid_test.pptx"

# Direct XML
print("=== Direct XML read ===")
with zipfile.ZipFile(PPTX) as z:
    for i in range(1, 3):
        with z.open(f'ppt/slides/slide{i}.xml') as f:
            x = f.read().decode('utf-8')
        m = re.search(r'<a:t>([^<]+)</a:t>', x)
        if m:
            print(f"  Slide {i}: {m.group(1)!r} (utf-8 bytes: {m.group(1).encode('utf-8').hex()})")

# python-pptx
print()
print("=== python-pptx read ===")
p = Presentation(PPTX)
for i, slide in enumerate(p.slides, 1):
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    print(f"  Slide {i}: {run.text!r} (utf-8: {run.text.encode('utf-8').hex()})")

# View outline raw bytes
raw = open(r'D:\OfficeCLI-test\hybrid_outline.bin', 'rb').read()
print()
print(f"=== View outline raw bytes ({len(raw)}) ===")
print(f"BOM: {raw[:3].hex()}")

# Try to find title in raw bytes
text = raw.decode('utf-16-le', errors='replace').lstrip('\ufeff')
print(text[:1000])
