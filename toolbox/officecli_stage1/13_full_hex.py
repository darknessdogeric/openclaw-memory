"""Look at slide1.json get output."""
raw = open(r'D:\OfficeCLI-test\slide1.json', 'rb').read()
print(f'Length: {len(raw)}')
print(f'BOM: {raw[:3].hex()}')
print(f'First 500 bytes hex: {raw[:500].hex()}')
print()
text = raw.decode('utf-16-le').lstrip('\ufeff')
print('As UTF-16-LE text:')
print(text[:1500])
