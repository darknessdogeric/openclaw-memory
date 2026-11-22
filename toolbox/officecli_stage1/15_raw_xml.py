"""Look at raw XML output via officecli raw command."""
raw = open(r'D:\OfficeCLI-test\slide1_raw.bin', 'rb').read()
print(f'Length: {len(raw)}')
print(f'BOM: {raw[:3].hex()}')

# Try different decodings
for enc in ['utf-16-le', 'utf-8', 'utf-8-sig']:
    try:
        if enc == 'utf-16-le':
            text = raw.decode('utf-16-le').lstrip('\ufeff')
        elif enc == 'utf-8':
            text = raw.decode('utf-8')
        else:
            text = raw.decode('utf-8-sig')
        # Find title in text
        import re
        m = re.search(r'<a:t>([^<]+)</a:t>', text)
        if m:
            print(f'  {enc}: title bytes in text: {m.group(1).encode("utf-8").hex() if m.group(1).isascii() is False else m.group(1)}')
            print(f'  {enc}: title (raw): {m.group(1)!r}')
    except Exception as e:
        print(f'  {enc}: ERROR {e}')

# Try UTF-8 forced
print()
print('As UTF-8:')
text = raw.decode('utf-8', errors='replace')
# Save to file with explicit UTF-8
with open(r'D:\OfficeCLI-test\slide1_raw_utf8.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print(f'Saved {len(text)} chars to slide1_raw_utf8.txt')

# Also save UTF-16 decoded
text16 = raw.decode('utf-16-le').lstrip('\ufeff')
with open(r'D:\OfficeCLI-test\slide1_raw_utf16.txt', 'w', encoding='utf-8') as f:
    f.write(text16)
print(f'Saved {len(text16)} chars (UTF-16 decoded) to slide1_raw_utf16.txt')
