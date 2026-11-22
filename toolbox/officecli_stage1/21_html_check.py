"""Check HTML preview for hybrid test."""
raw = open(r'D:\OfficeCLI-test\hybrid_html.bin', 'rb').read()
text = raw.decode('utf-16-le').lstrip('\ufeff')
with open(r'D:\OfficeCLI-test\hybrid_preview.html', 'w', encoding='utf-8') as f:
    f.write(text)
print(f'Saved {len(text)} chars')

# Search for slide content
import re
# Look for any 'Slide' content
slides = re.findall(r'<div[^>]*>(?:(?!</div>).)*Slide[^<]*', text, re.DOTALL)
print(f"Found {len(slides)} slide mentions")
for s in slides[:5]:
    print(s[:200])
    print('---')

# Search for ASCII title and Chinese title
print()
print(f'"Slide One ASCII" in HTML: {"Slide One ASCII" in text}')
# Search for correct Chinese
print(f'"酒店供应链管理手册" in HTML: {"酒店供应链管理手册" in text}')
print(f'"閰掑簵渚涘簲閾剧" in HTML: {"閰掑簵渚涘簲閾剧" in text}')

# Look for HTML title block
m = re.search(r'<title[^>]*>(.*?)</title>', text, re.DOTALL)
if m:
    print(f'\n<title>: {m.group(1)!r}')

# Look at first few hundred chars
print()
print('First 800 chars:')
print(text[:800])
