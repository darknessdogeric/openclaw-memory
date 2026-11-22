import os
content = open('anyi-ops-kb/garden-hotel-26-eval-20260804.md', 'rb').read()
print('Total bytes:', len(content))
# Find null bytes or non-printable
null_count = content.count(b'\x00')
print('Null bytes:', null_count)
# Show bytes around position 10600
for i in [10500, 10600, 10700, 10800, 10900, 11000, 12000, 15000, 20000]:
    if i < len(content):
        print(f'@{i}: {content[i:i+16].hex()} | {content[i:i+16]!r}')

# Check if it has BOM or partial UTF-16 inside
if content[:2] in (b'\xff\xfe', b'\xfe\xff'):
    print('UTF-16 BOM detected')
elif content[:3] == b'\xef\xbb\xbf':
    print('UTF-8 BOM detected')

# Try without errors=ignore
try:
    c = content.decode('utf-8')
    print('Strict UTF-8 success:', len(c), 'chars')
except UnicodeDecodeError as e:
    print('Strict UTF-8 fail at', e.start, ':', content[e.start-5:e.start+5].hex())