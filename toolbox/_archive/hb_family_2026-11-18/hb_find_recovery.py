"""Find RECOVERY NOTE in HEARTBEAT.md."""
path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
try:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f, 1):
            if 'RECOVERY NOTE' in line or 'DATA LOSS' in line:
                safe = line.encode('ascii', 'replace').decode('ascii')[:200]
                print(f'[{i}] {safe}')
                if i > 30:
                    break
except Exception as e:
    print(f'ERROR: {e}')