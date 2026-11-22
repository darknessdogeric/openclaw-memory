"""Try different encodings on the JSON title bytes."""
title_bytes = bytes.fromhex('b0959163357c1a6e986d327cbe95675278e11e94d8559c5850933f00')
print(f"Title bytes length: {len(title_bytes)}")
print()

# Try different encodings
encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'utf-16-le', 'utf-16-be', 'utf-16', 'cp936', 'cp950']
for enc in encodings:
    try:
        text = title_bytes.decode(enc)
        print(f'{enc}: {text!r}')
    except Exception as e:
        print(f'{enc}: ERROR {type(e).__name__}: {str(e)[:80]}')

# Try treating as UTF-16-LE pairs, then UTF-8 each pair
print()
print('--- Hybrid attempts ---')

# What if it's UTF-16-LE with swapped byte pairs (BE)?
try:
    text = title_bytes.decode('utf-16-be')
    print(f'utf-16-be: {text!r}')
except Exception as e:
    print(f'utf-16-be: ERROR {e}')

# What if the content is the original UTF-8 of the title, but stored as raw bytes within a UTF-16-LE wrapper?
# That is: each UTF-8 byte was paired with 0x00 instead of being combined into UTF-16.
# Original: e9 85 92 e5 ba 97 ...
# As 0x00 XX pairs: 00 e9 00 85 00 92 00 e5 00 ba 00 97 00 e4 00 be ...
# That doesn't match either.

# Try the inverse: original UTF-16 chars stored as their low bytes only, with garbage high bytes
# UTF-16-LE of 酒店: 5B 91 E8 95
# The JSON bytes start with b0 95 91 63

# Try GBK decoding of those bytes interpreted as text:
text = title_bytes.decode('gbk', errors='replace')
print(f'gbk replace: {text!r}')

# Check if maybe these are UTF-8 bytes that were concatenated to form UTF-16 code units:
# e9 -> 0x85E9 (UTF-16 BE) or 0xE985 (UTF-16 LE)
# 85 -> ...
# Looking at bytes: b0 95
# As UTF-16 LE: 0x95B0 = 閰
# But maybe these are meant to be UTF-8 of garbled output?

# Look at the JSON bytes as if it were UTF-8 with random byte ordering issues
print()
print('Trying to recover correct text via character codepoint matching...')
# 酒店供应链管理手册 codepoints:
target = '酒店供应链管理手册'
print(f'Target codepoints: {[hex(ord(c)) for c in target]}')
# Expected UTF-8:
print(f'Target UTF-8: {target.encode("utf-8").hex()}')
# Expected UTF-16-LE:
print(f'Target UTF-16-LE: {target.encode("utf-16-le").hex()}')

# Are JSON bytes shifted? Like each byte should be at position*2?
print(f'JSON bytes:    {title_bytes.hex()}')

# What if title bytes = UTF-8 byte1 + UTF-8 byte2 of each char?
# For 酒 (UTF-8: e9 85 92): take first 2 = e9 85
# For 店 (UTF-8: e5 ba 97): take first 2 = e5 ba
# That gives e9 85 e5 ba e4 be e5 ba e9 93 e7 ae e7 90 e6 89 e5 86 (18 bytes)
# But we have 27 bytes for 9 chars (3 bytes each)
# What if JSON bytes are: for each UTF-8 char, swap first and third bytes?
# 酒: e9 85 92 -> 92 85 e9
# 店: e5 ba 97 -> 97 ba e5
# That would give: 92 85 e9 97 ba e5 9b be e4 94 ba e5 be 93 e9 a1 ae e7 90 86 ... no, doesn't match
