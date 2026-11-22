"""Test 1: Add ASCII slide, then Chinese slide. Compare XML vs view."""
import subprocess, os, zipfile, re

OC = r"D:\OfficeCLI-test\officecli.exe"
PPTX = r"D:\OfficeCLI-test\hybrid_test.pptx"

if os.path.exists(PPTX):
    os.remove(PPTX)

# Create
subprocess.run([OC, "create", PPTX], capture_output=True, text=True, encoding='utf-8')

# Add slides
subprocess.run([OC, "add", PPTX, "/", "--type", "slide", "--prop", "title=Slide One ASCII"], capture_output=True, text=True, encoding='utf-8')
subprocess.run([OC, "add", PPTX, "/", "--type", "slide", "--prop", "title=酒店供应链管理手册"], capture_output=True, text=True, encoding='utf-8')
subprocess.run([OC, "save", PPTX], capture_output=True, text=True, encoding='utf-8')
subprocess.run([OC, "close", PPTX], capture_output=True, text=True, encoding='utf-8')

# Read XML directly
print("=== Direct XML read ===")
with zipfile.ZipFile(PPTX) as z:
    for i in range(1, 3):
        with z.open(f'ppt/slides/slide{i}.xml') as f:
            x = f.read().decode('utf-8')
        m = re.search(r'<a:t>([^<]+)</a:t>', x)
        if m:
            print(f"  Slide {i}: {m.group(1)!r} (bytes: {m.group(1).encode('utf-8').hex()})")

# View outline (UTF-16)
r = subprocess.run([OC, "view", PPTX, "outline"], capture_output=True, encoding='utf-16-le', errors='replace')
print()
print("=== View outline (UTF-16) ===")
print(r.stdout[:500])
print()

# Try opening the file in PowerPoint or LibreOffice to see what happens
# Actually, let me try opening it via python-pptx
try:
    from pptx import Presentation
    p = Presentation(PPTX)
    print("=== python-pptx read ===")
    for i, slide in enumerate(p.slides, 1):
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        print(f"  Slide {i}: {run.text!r}")
except Exception as e:
    print(f"python-pptx: ERROR {e}")

# Save view outline to file for hex inspection
with open(r'D:\OfficeCLI-test\hybrid_outline.bin', 'wb') as f:
    f.write(r.stdout.encode('utf-16-le'))
