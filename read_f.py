import os, sys, pdfplumber

# Find key PDF files in F: drive
def find_files(root, patterns):
    results = []
    for dp, dn, fn in os.walk(root):
        for f in fn:
            for p in patterns:
                if p in f and f.endswith('.pdf'):
                    results.append(os.path.join(dp, f))
    return results

# Find the most important documents
key_files = []
for base in ['F:/重点项目', 'F:/运营文件', 'F:/行业资料文件夹', 'F:/自我革命', 'F:/商贸提案']:
    if os.path.exists(base):
        found = find_files(base, ['亚朵', '中旅', '中国旅游', '至拓', '至胜', 'IP', '文创'])
        key_files.extend(found)

print(f'Found {len(key_files)} key files:')
for f in key_files[:20]:
    sz = os.path.getsize(f)
    print(f'{sz//1024:>6}KB  {os.path.basename(f)}')

# Read the most important ones
print('\n--- Reading key documents ---\n')

priority = [
    # (path, max_pages_or_chars)
]

# Try to read 中旅 document
ctrip_files = [f for f in key_files if '中国旅游' in f or '中旅' in f]
for f in ctrip_files[:2]:
    if f.endswith('.pdf') and os.path.getsize(f) < 20*1024*1024:  # < 20MB
        try:
            print(f'=== Reading: {os.path.basename(f)} ===')
            with pdfplumber.open(f) as pdf:
                total_pages = len(pdf.pages)
                print(f'Pages: {total_pages}')
                text = ''
                for i, page in enumerate(pdf.pages[:5]):  # First 5 pages
                    t = page.extract_text()
                    if t:
                        text += t + '\n'
                print(text[:2000])
                print('...\n')
        except Exception as e:
            print(f'Error: {e}\n')
