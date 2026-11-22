"""Search for recent HB entries in HEARTBEAT.md."""
path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
target_nums = {3203, 3204, 3205, 3206, 3207}
found = {}
try:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f, 1):
            for n in target_nums:
                if f'HB #{n}' in line:
                    found.setdefault(n, []).append((i, line.rstrip()[:200]))
                    break
    for n in sorted(target_nums):
        hits = found.get(n, [])
        print(f'=== HB #{n} ===')
        if not hits:
            print('  (NOT FOUND)')
        for ln, txt in hits[-2:]:
            print(f'  [{ln}] {txt}')
except Exception as e:
    print(f'ERROR: {e}')