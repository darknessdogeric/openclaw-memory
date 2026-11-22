import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Method 1: open with utf-8
with open('anyi-ops-kb/garden-hotel-26-eval-20260804.md', encoding='utf-8') as f:
    c1 = f.read()
print('Method 1 (utf-8):', len(c1), 'chars')
print('  has 9 类:', '9 类' in c1)
print('  has 开放式卫生间:', '开放式卫生间' in c1)

# Method 2: bytes + decode
raw = open('anyi-ops-kb/garden-hotel-26-eval-20260804.md', 'rb').read()
print('Raw bytes:', len(raw))
c2 = raw.decode('utf-8')
print('Method 2 (bytes+utf-8):', len(c2), 'chars')
print('  has 9 类:', '9 类' in c2)
print('  has 开放式卫生间:', '开放式卫生间' in c2)

# Method 3: chardet
try:
    import chardet
    detected = chardet.detect(raw)
    print('chardet:', detected)
except ImportError:
    pass