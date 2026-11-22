"""Find correct Chinese in outline.json."""
raw = open(r'D:\OfficeCLI-test\outline.json','rb').read()

# Look for byte pattern e985 (酒) anywhere in raw
patterns = [
    (b'\xe9\x85', '酒 UTF-8 byte1-2'),
    (b'\xe5\xba\x97', '店 UTF-8'),
    (b'\x95\x5b', '酒 UTF-16-LE'),
    (b'\x5b\x91', '酒 UTF-16-LE reversed (low,high)'),
]
for p, name in patterns:
    idx = raw.find(p)
    print(f'{name}: {idx}')

# Print all bytes around first 酒
print()
print('=== Bytes 314-420 ===')
print(raw[314:420].hex())

# Decoded as UTF-16-LE
text = raw[314:420].decode('utf-16-le', errors='replace')
print('UTF-16:', repr(text))

# Now look at full file
text_full = raw.decode('utf-16-le', errors='replace')
print()
print('=== Search for 酒店 in UTF-16-LE decoded ===')
idx = text_full.find('酒店')
print('Index:', idx)
if idx >= 0:
    print('Context:', repr(text_full[max(0,idx-30):idx+50]))

# Hmm, looks like the file IS properly UTF-16-LE, but I had wrong output before
# Look at the file as raw bytes again
print()
print('=== Looking for title key in UTF-16 ===')
# 'title' in utf-16: 74 00 69 00 74 00 6c 00 65 00
idx = raw.find(b'\x74\x00\x69\x00\x74\x00\x6c\x00\x65\x00')
print(f'"title" at byte: {idx}')
# After 'title' comes '"' ':' ' ' '"' and the value
# Let's read the actual value bytes
val_start = idx + 12  # past 'title' + '"' + ':' + ' '
# Find the actual opening quote (it might come right after space)
# In UTF-16-LE: opening quote is 0x22, 0x00
# Skip past colon (3A 00) and space (20 00)
quote_open = raw.find(b'\x22\x00', val_start)
print(f'opening quote at: {quote_open}')
# Now find next quote (closing)
val_bytes_start = quote_open + 2
close = raw.find(b'\x22\x00', val_bytes_start)
print(f'closing quote at: {close}')
val = raw[val_bytes_start:close]
print(f'value bytes ({len(val)}): {val.hex()}')
print(f'value text: {val.decode("utf-16-le", errors="replace")!r}')
