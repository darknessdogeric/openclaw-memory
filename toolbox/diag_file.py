import os
size = os.path.getsize('anyi-ops-kb/garden-hotel-26-eval-20260804.md')
print('On disk:', size, 'bytes')
content = open('anyi-ops-kb/garden-hotel-26-eval-20260804.md', 'rb').read()
print('Read raw bytes:', len(content))
try:
    c16 = content.decode('utf-16')
    print('UTF-16 decode success:', len(c16), 'chars')
    if '9 类' in c16:
        print('UTF-16 content HAS 9 类!')
    if '1.5' in c16 and 'Eric' in c16:
        print('UTF-16 content HAS section 1.5 + Eric!')
    if '亚朵 3.0' in c16:
        print('UTF-16 content HAS 亚朵 3.0!')
except Exception as e:
    print('UTF-16 fail:', e)
c8 = content.decode('utf-8', errors='ignore')
print('UTF-8 decoded:', len(c8), 'chars')
print('Has 9 类:', '9 类' in c8)
print('Has 门散:', '门散' in c8)
print('Has section 1.5:', '### 1.5' in c8)
print('First 16 bytes:', content[:16].hex())
print('Last 16 bytes:', content[-16:].hex())