"""Check view outline output for hybrid test."""
raw = open(r'D:\OfficeCLI-test\hybrid_outline.bin', 'rb').read()
print(f'Length: {len(raw)}')
text = raw.decode('utf-16-le').lstrip('\ufeff')
with open(r'D:\OfficeCLI-test\hybrid_outline.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print(f'Saved {len(text)} chars')
