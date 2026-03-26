import os

# Try common F drive paths for Eric's data
paths_to_try = [
    r'F:\自我革命备份',
    r'F:\自我革命',
    r'F:\张实',
    r'F:\资料',
    r'F:\备份',
]

for p in paths_to_try:
    if os.path.exists(p):
        print(f'FOUND: {p}')
        files = []
        total = 0
        for root, dirs, filenames in os.walk(p):
            for f in filenames:
                if f.startswith('~'):
                    continue
                fp = os.path.join(root, f)
                sz = os.path.getsize(fp)
                total += sz
                files.append((os.path.relpath(fp, p), sz, sz//1024))
        files.sort()
        print(f'Total: {len(files)} files, {total//1024//1024}MB')
        for rel, sz, kb in files:
            print(f'{kb:>6}KB  {rel}')
        print()
