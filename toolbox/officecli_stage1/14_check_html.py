"""Convert raw HTML preview to UTF-8 and verify Chinese."""
raw = open(r'D:\OfficeCLI-test\preview_raw.bin', 'rb').read()
text = raw.decode('utf-16-le').lstrip('\ufeff')

# Save as UTF-8 HTML
with open(r'D:\OfficeCLI-test\preview.html', 'w', encoding='utf-8') as f:
    f.write(text)
print(f'Saved preview.html: {len(text)} chars')

# Check for Chinese titles
titles = [
    "酒店供应链管理手册",
    "采购成本下降 25%",
    "供应商分级管理",
    "应急采购 SOP",
    "¥99 整套 13章节",
]

print()
print('=== Title presence in HTML ===')
for t in titles:
    present = t in text
    safe_t = t.encode('ascii', errors='replace').decode('ascii')
    print(f'  [{safe_t}]: {"YES" if present else "NO"}')

# Also check if garbled versions are in HTML (indicating same bug)
print()
print('=== Garbled versions ===')
for garbled, expected in [
    ("閰掑簵渚涘簲閾剧", "酒店供应链..."),
    ("鎼存梹鈧", "应急采购..."),
    ("楼99", "¥99"),
]:
    present = garbled in text
    print(f'  {garbled} (expected {expected}): {"YES" if present else "NO"}')

# Check HTML structure
print()
print('=== HTML head ===')
print(text[:500])

# Find first slide div
import re
m = re.search(r'(<div[^>]*class="[^"]*slide[^"]*"[^>]*>.*?</div>\s*</div>)', text, re.DOTALL)
if m:
    print()
    print('=== First slide ===')
    print(m.group(1)[:2000])
