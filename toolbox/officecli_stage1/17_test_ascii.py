"""Test with ASCII-only content to isolate encoding bug."""
import subprocess, os

OC = r"D:\OfficeCLI-test\officecli.exe"
PPTX = r"D:\OfficeCLI-test\ascii_test.pptx"

if os.path.exists(PPTX):
    os.remove(PPTX)

# Create
r = subprocess.run([OC, "create", PPTX], capture_output=True, text=True, encoding='utf-8')
print("CREATE:", r.returncode, r.stdout.strip())

# Add ASCII slide
r = subprocess.run([OC, "add", PPTX, "/", "--type", "slide", "--prop", "title=Hello World Test"], capture_output=True, text=True, encoding='utf-8')
print("ADD:", r.returncode, r.stdout.strip())

# Save and close
r = subprocess.run([OC, "save", PPTX], capture_output=True, text=True, encoding='utf-8')
print("SAVE:", r.returncode, r.stdout.strip())
r = subprocess.run([OC, "close", PPTX], capture_output=True, text=True, encoding='utf-8')
print("CLOSE:", r.returncode, r.stdout.strip())

# Now view outline
r = subprocess.run([OC, "view", PPTX, "outline"], capture_output=True, text=True, encoding='utf-8')
print("VIEW outline:", r.returncode, repr(r.stdout.strip()))

# Check if the title is correct
import zipfile, re
with zipfile.ZipFile(PPTX) as z:
    with z.open('ppt/slides/slide1.xml') as f:
        x = f.read().decode('utf-8')
    m = re.search(r'<a:t>([^<]+)</a:t>', x)
    if m:
        print(f"XML title: {m.group(1)!r}")
